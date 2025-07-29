"""
Classifies: CHEBI:132155 hydroxynaphthoquinone
"""
"""
Classifies: CHEBI:XXXXX hydroxynaphthoquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_hydroxynaphthoquinone(smiles: str):
    """
    Determines if a molecule is a hydroxynaphthoquinone based on its SMILES string.
    A hydroxynaphthoquinone is a naphthoquinone with at least one hydroxy group attached to the naphthalene ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxynaphthoquinone, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the naphthoquinone pattern (naphthalene with two ketone groups at positions 1 and 4)
    naphthoquinone_pattern = Chem.MolFromSmarts("c1ccc2c(c1)C(=O)C=CC2=O")
    if not mol.HasSubstructMatch(naphthoquinone_pattern):
        return False, "No naphthoquinone moiety found"

    # Look for at least one hydroxy group attached to the naphthalene ring
    hydroxy_pattern = Chem.MolFromSmarts("[OH]")
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    if len(hydroxy_matches) == 0:
        return False, "No hydroxy group found"

    # Ensure the hydroxy group is attached to the naphthalene ring
    naphthalene_atoms = set()
    for match in mol.GetSubstructMatches(naphthoquinone_pattern):
        naphthalene_atoms.update(match)

    for hydroxy_match in hydroxy_matches:
        hydroxy_atom = mol.GetAtomWithIdx(hydroxy_match[0])
        neighbor_atom = hydroxy_atom.GetNeighbors()[0]
        if neighbor_atom.GetIdx() not in naphthalene_atoms:
            return False, "Hydroxy group not attached to the naphthalene ring"

    return True, "Contains a naphthoquinone moiety with at least one hydroxy group attached to the naphthalene ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132155',
                          'name': 'hydroxynaphthoquinone',
                          'definition': 'Any naphthoquinone in which the '
                                        'naphthaoquinone moiety is substituted '
                                        'by at least one hydroxy group.',
                          'parents': ['CHEBI:132130', 'CHEBI:25481'],
                          'xrefs': ['Wikipedia:Hydroxynaphthoquinone'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 32,
                           'log_lines_of_code': 3.4657359027997265,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmarts',
                                                 'GetSubstructMatches',
                                                 'HasSubstructMatch',
                                                 'GetNeighbors',
                                                 'GetIdx',
                                                 'update',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles'],
                           'methods_called_count': 8,
                           'smarts_strings': [   'c1ccc2c(c1)C(=O)C=CC2=O',
                                                 '[OH]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_hydroxynaphthoquinone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No naphthoquinone moiety '
                                          'found"',
                                          'False, "No hydroxy group found"',
                                          'False, "Hydroxy group not attached '
                                          'to the naphthalene ring"',
                                          'True, "Contains a naphthoquinone '
                                          'moiety with at least one hydroxy '
                                          'group attached to the naphthalene '
                                          'ring"'],
                           'returns_count': 5,
                           'complexity': 4.093147180559945},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CCCCN',
                                     'name': 'Lys-Lys-Ile',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'C1=C2[C@]3(CC[C@]4([C@]([C@@]3(CCC2=C(C(=C1)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)[O-])O)O)O)[H])(CC[C@@H]4O)[H])C)[H]',
                                     'name': '4-hydroxy-17beta-estradiol '
                                             '4-O-(beta-D-glucuronide)(1-)',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'CCC1=CC=C(C=C1)CNCC2=CN=CC=C2',
                                     'name': '1-(4-ethylphenyl)-N-(3-pyridinylmethyl)methanamine',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': '[H]C(C=C([H])C(O)=O)=CC([O-])=O',
                                     'name': '5-carboxypenta-2,4-dienoate',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'CC1CC2=C(S1)C(=O)N(C(=N2)SCC(=O)NC3=NOC(=C3)C)C4=CC=CC=C4',
                                     'name': 'N-(5-methyl-3-isoxazolyl)-2-[(6-methyl-4-oxo-3-phenyl-6,7-dihydrothieno[3,2-d]pyrimidin-2-yl)thio]acetamide',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'C1CCN(C1)C2=NC(=NC(=N2)NCCO)NC3=CC=CC=C3C(=O)N',
                                     'name': '2-[[4-(2-hydroxyethylamino)-6-(1-pyrrolidinyl)-1,3,5-triazin-2-yl]amino]benzamide',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'O=C(NCC(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)[C@H](CC)C',
                                     'name': 'Tyr-Ile-Gly',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': '[O-]C([O-])=O',
                                     'name': 'carbonate',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'CCNC(=O)C[C@@H]1C=C[C@H]([C@@H](O1)CO)NS(=O)(=O)C2=CC=C(C=C2)F',
                                     'name': 'N-ethyl-2-[(2R,3R,6R)-3-[(4-fluorophenyl)sulfonylamino]-2-(hydroxymethyl)-3,6-dihydro-2H-pyran-6-yl]acetamide',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'},
                                 {   'smiles': 'FC(F)=C[C@H]1CN([C@@H](CC)C(=O)N)C(=O)C1',
                                     'name': 'Seletracetam',
                                     'reason': 'No naphthoquinone moiety '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'Oc1cccc2C(=O)C(=CC(=O)c12)c1ccc(O)c2c(O)cccc12',
                                      'name': 'Hypoxylone',
                                      'reason': 'Hydroxy group not attached to '
                                                'the naphthalene ring'},
                                  {   'smiles': 'C1CC(CCC1C2=CC=C(C=C2)Cl)C3=C(C4=CC=CC=C4C(=O)C3=O)O',
                                      'name': '3-[4-(p-chlorophenyl)cyclohexyl]-4-hydroxy-1,2-naphthoquinone',
                                      'reason': 'No naphthoquinone moiety '
                                                'found'},
                                  {   'smiles': 'CC(C)=CC[C@H](O)C1=CC(=O)c2c(O)ccc(O)c2C1=O',
                                      'name': 'Alkannin',
                                      'reason': 'Hydroxy group not attached to '
                                                'the naphthalene ring'},
                                  {   'smiles': 'OCCC1=C(O)C(=O)c2ccccc2C1=O',
                                      'name': '2-hydroxy-3-(2-hydroxyethyl)naphthalene-1,4-dione',
                                      'reason': 'Hydroxy group not attached to '
                                                'the naphthalene ring'},
                                  {   'smiles': '[C@H](C)([C@@H]([C@@H]([C@H](\\C=C\\O[C@]1(OC=2C(C1=O)=C3C(C(C(C=C3[O-])=O)=O)=C(C2C)[O-])C)OC)C)OC(=O)C)[C@H](O)[C@@H]([C@@H](O)[C@@H](C)/C=C/C=C(/C)\\C(N)=O)C',
                                      'name': 'rifamycin SV '
                                              'ortho-naphthoquinone '
                                              'carboxamide(2-)',
                                      'reason': 'No naphthoquinone moiety '
                                                'found'},
                                  {   'smiles': '[C@H](C)([C@@H]([C@@H]([C@H](\\C=C\\O[C@]1(OC=2C(C1=O)=C3C(C(C(C(=C3[O-])/C=N/N4CCN(CC4)C)=O)=O)=C(C2C)[O-])C)OC)C)OC(=O)C)[C@H](O)[C@@H]([C@@H](O)[C@@H](C)/C=C/C=C(/C)\\C(N)=O)C',
                                      'name': 'rifampicin ortho-naphthoquinone '
                                              'carboxamide(2-)',
                                      'reason': 'No naphthoquinone moiety '
                                                'found'},
                                  {   'smiles': '[C@H](C)([C@@H]([C@@H]([C@H](\\C=C\\O[C@]1(OC=2C(C1=O)=C3C(C(C(=CC3=O)[O-])=O)=C(C2C)[O-])C)OC)C)OC(=O)C)[C@H](O)[C@@H]([C@@H](O)[C@@H](C)/C=C/C=C(/C)\\C(N)=O)C',
                                      'name': 'rifamycin SV '
                                              'para-naphthoquinone '
                                              'carboxamide(2-)',
                                      'reason': 'Hydroxy group not attached to '
                                                'the naphthalene ring'},
                                  {   'smiles': 'CC(C)=CC[C@@H](O)C1=CC(=O)c2c(O)ccc(O)c2C1=O',
                                      'name': 'Shikonin',
                                      'reason': 'Hydroxy group not attached to '
                                                'the naphthalene ring'},
                                  {   'smiles': 'CC(C)c1cc(O)c(C=O)c2C(=O)C(=O)C(C)=Cc12',
                                      'name': 'Hibiscoquinone A',
                                      'reason': 'No naphthoquinone moiety '
                                                'found'},
                                  {   'smiles': 'C[C@@H](\\C=C\\C=C(/C)C(O)=O)[C@H](O)[C@@H](C)[C@@H](O)[C@@H](C)[C@H](O)[C@H](C)[C@@H](O)C(C)\\C=C(/C)C(=O)c1c(O)c(C)cc2C(=O)C(N)=CC(=O)c12',
                                      'name': 'rifamycin-undecaketide '
                                              'carboxylic acid',
                                      'reason': 'Hydroxy group not attached to '
                                                'the naphthalene ring'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as hydroxynaphthoquinones, we '
                 'need to identify molecules that contain a naphthoquinone '
                 'moiety (a naphthalene ring with two ketone groups at '
                 'positions 1 and 4) and at least one hydroxy group attached '
                 'to the naphthalene ring. The function '
                 '`is_hydroxynaphthoquinone` will check for these structural '
                 'features.\n'
                 '\n'
                 'Here’s the Python program:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 22,
    'num_false_positives': 90,
    'num_true_negatives': 142176,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.19642857142857142,
    'recall': 0.6470588235294118,
    'f1': 0.3013698630136986,
    'accuracy': 0.9992832044975404,
    'negative_predictive_value': 0.9999156046923791}