"""
Classifies: CHEBI:37143 organofluorine compound
"""
"""
Classifies: CHEBI:37143 organofluorine compound
An organofluorine compound is a compound containing at least one carbon-fluorine bond.
"""
from rdkit import Chem

def is_organofluorine_compound(smiles: str):
    """
    Determines if a molecule is an organofluorine compound based on its SMILES string.
    An organofluorine compound is defined as a compound containing at least one carbon-fluorine bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organofluorine compound, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for at least one carbon-fluorine bond
    c_f_bond_pattern = Chem.MolFromSmarts("[C]-[F]")
    if mol.HasSubstructMatch(c_f_bond_pattern):
        return True, "Contains at least one carbon-fluorine bond"
    else:
        return False, "No carbon-fluorine bonds found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:37143',
                          'name': 'organofluorine compound',
                          'definition': 'An organofluorine compound is a '
                                        'compound containing at least one '
                                        'carbon-fluorine bond.',
                          'parents': ['CHEBI:17792', 'CHEBI:24062'],
                          'xrefs': ['MetaCyc:Fluorides'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 19,
                           'log_lines_of_code': 2.9444389791664403,
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
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': ['[C]-[F]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_organofluorine_compound(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains at least one '
                                          'carbon-fluorine bond"',
                                          'False, "No carbon-fluorine bonds '
                                          'found"'],
                           'returns_count': 3,
                           'complexity': 2.388887795833288},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'N[C@@H](Cc1cc(Br)c(O)c(Br)c1)C(O)=O',
                                     'name': '3,5-dibromo-L-tyrosine',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC=2NC=NC2',
                                     'name': 'Gln-His-Phe',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'C[C@@H]1C[C@H](O)C=C(C)[C@]11CC[C@H](C1)C(C)=C',
                                     'name': 'solavetivol',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'OC(C[C@H](CC)O)=O',
                                     'name': '(S)-3-hydroxypentanoic acid',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'O=C1C2=C3[C@]([C@]4([C@@H]([C@@]5([C@H](C([C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@@H]([C@H]6O)O)CO)[C@@H](C5)OC(=O)C)(C)C)CC4)CO)CC3)C)(CCC2(C)C(C1)C(C)C)C',
                                     'name': 'Hyalodendroside B',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=C(O)C=C1)C(=O)N[C@@H](C)C(O)=O)[C@@H](N)CC=2C=3C(NC2)=CC=CC3',
                                     'name': 'Trp-Tyr-Ala',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'C1CN(CCC12OCCO2)C(=O)C3=NN4C(=CC(=NC4=C3)C5=CC=CC=C5)C6=CC=CC=C6',
                                     'name': '1,4-dioxa-8-azaspiro[4.5]decan-8-yl-(5,7-diphenyl-2-pyrazolo[1,5-a]pyrimidinyl)methanone',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'O1[C@@]2([C@@H](/C(=C/C)/C)[C@@H](/C=C/C=C(/[C@@H](O)[C@H](CO)C)\\C)[C@H]3[C@H]([C@H]12)C[C@](O)(C)[C@@H](C3)O)C',
                                     'name': 'Fusarielin B',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)CC(OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCCC',
                                     'name': 'TG(16:0/16:1(9Z)/16:0)',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'},
                                 {   'smiles': 'S1CC(NC(=O)C(NC(=O)C(NC(=O)CN)CC(=O)O)CC(C)C)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(NC(C(NC(C(NC(C1)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)C(=O)NC2C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(O)C)C(NC(C(NC(CNC(CSC2)C(=O)CC(C(=O)O)CC(C)C)CC(C)C)=O)CC(C)C)=O)=C)CC3=CC=CC=C3)C)CC4=CC=CC=C4)CCCCN)CC(=O)O)=O)CC(C)C)=O)CC(C)C)=O)CC(C)C)=C)C)=C',
                                     'name': 'Curvopeptin-3',
                                     'reason': 'No carbon-fluorine bonds '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'OB(O)c1ccc(F)cc1',
                                      'name': '4-fluorophenylboronic acid',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'N[C@@H](Cc1cc(O)c(O)cc1[18F])C(O)=O',
                                      'name': '6-((18)F)fluoro-L-dopa',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'Nc1nc(=O)n(cc1F)[C@@H]1CS[C@H](CO)O1',
                                      'name': 'emtricitabine',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'C1=CC(=C(C=C1F)O)C2=CC=C(O2)C=C3C(=O)NC(=O)S3',
                                      'name': '5-[[5-(4-fluoro-2-hydroxyphenyl)-2-furanyl]methylidene]thiazolidine-2,4-dione',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC=CC=C3F)O[C@@H]1CN(C)CC4=CN=CC=C4)[C@@H](C)CO',
                                      'name': '(2S)-2-[(4R,5S)-8-(2-fluorophenyl)-4-methyl-5-[[methyl(3-pyridinylmethyl)amino]methyl]-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-2-yl]-1-propanol',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'CC(C)c1nc(nc(-c2ccc(F)cc2)c1\\C=C\\[C@@H](O)C[C@@H](O)CC(O)=O)N(C)S(C)(=O)=O',
                                      'name': 'rosuvastatin',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'CC(C)OC(=O)N[C@@H](C(C)C)C(=O)N[C@H](C)c1nc2ccc(F)cc2s1',
                                      'name': 'benthiavalicarb-isopropyl',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'Fc1cccc(F)c1C(=O)NC(=O)Nc1ccc(CON=C(C2CC2)c2ccc(Cl)cc2)cc1',
                                      'name': 'flucycloxuron',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'C1=NC(=C2N1C=3C(C(N(C2)C)=O)=CC(=CC3)F)C(OCC)=O',
                                      'name': 'flumazenil',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'},
                                  {   'smiles': 'C[C@H]1CN(C(=O)C2=C(N=CC(=C2)C#CC3=CC=CC=C3F)O[C@H]1CN(C)C(=O)C4CCCCC4)[C@H](C)CO',
                                      'name': 'N-[[(2R,3S)-8-[2-(2-fluorophenyl)ethynyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylcyclohexanecarboxamide',
                                      'reason': 'No carbon-fluorine bonds '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'To classify a chemical entity as an organofluorine compound, '
                 'we need to check if the molecule contains at least one '
                 'carbon-fluorine (C-F) bond. This can be done by searching '
                 'for the presence of fluorine atoms bonded to carbon atoms in '
                 'the molecule. The function `is_organofluorine_compound` will '
                 'take a SMILES string as input, parse it into a molecule, and '
                 'then check for the presence of at least one C-F bond.\n'
                 '\n'
                 'Here is the Python code to achieve this:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 706,
    'num_false_positives': 2129,
    'num_true_negatives': 138939,
    'num_false_negatives': 526,
    'num_negatives': None,
    'precision': 0.2490299823633157,
    'recall': 0.573051948051948,
    'f1': 0.3471846569953282,
    'accuracy': 0.9813422347153901,
    'negative_predictive_value': 0.9962284444125766}