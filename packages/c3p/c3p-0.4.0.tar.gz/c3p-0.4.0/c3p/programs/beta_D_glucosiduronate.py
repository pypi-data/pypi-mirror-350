"""
Classifies: CHEBI:83411 beta-D-glucosiduronate
"""
"""
Classifies: CHEBI:35615 beta-D-glucosiduronate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_beta_D_glucosiduronate(smiles: str):
    """
    Determines if a molecule is a beta-D-glucosiduronate based on its SMILES string.
    A beta-D-glucosiduronate is a carbohydrate acid derivative anion obtained by deprotonation
    of the carboxy group of any beta-D-glucosiduronic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-D-glucosiduronate, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Look for glucuronic acid moiety ([C@H]1[C@H]([C@@H]([C@H]([C@H](O1)C([O-])=O)O)O)O)
    glucuronic_pattern = Chem.MolFromSmarts("[C@H]1[C@H]([C@@H]([C@H]([C@H](O1)C([O-])=O)O)O)O")
    if not mol.HasSubstructMatch(glucuronic_pattern):
        return False, "No glucuronic acid moiety found"
    
    # Check for beta configuration (look for cis arrangement of H and OH on ring atoms)
    beta_pattern = Chem.MolFromSmarts("[C@H]1[C@@H]([C@@H]([C@@H]([C@@H](O1)C([O-])=O)O)O)O")
    if not mol.HasSubstructMatch(beta_pattern):
        return False, "Not in beta configuration"
    
    # Check molecular weight - glucosiduronates typically >300 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 300:
        return False, "Molecular weight too low for glucosiduronate"
    
    # Count carbons, oxygens, and deprotonated carboxyl groups
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    deprotonated_cooh_count = sum(1 for atom in mol.GetAtoms() if atom.GetFormalCharge() == -1)
    
    if c_count < 6:
        return False, "Too few carbons for glucosiduronate"
    if o_count < 6:
        return False, "Too few oxygens for glucosiduronate"
    if deprotonated_cooh_count != 1:
        return False, "Does not contain exactly one deprotonated carboxyl group"
    
    return True, "Contains glucuronic acid moiety in beta configuration with deprotonated carboxyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:83411',
                          'name': 'beta-D-glucosiduronate',
                          'definition': 'A carbohydrate acid derivative anion '
                                        'obtained by deprotonation of the '
                                        'carboxy group of any '
                                        'beta-D-glucosiduronic acid; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:132367', 'CHEBI:63551'],
                          'xrefs': ['MetaCyc:Beta-D-Glucuronides'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 37,
                           'log_lines_of_code': 3.6109179126442243,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'GetFormalCharge',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum'],
                           'methods_called_count': 7,
                           'smarts_strings': [   '[C@H]1[C@H]([C@@H]([C@H]([C@H](O1)C([O-])=O)O)O)O',
                                                 '[C@H]1[C@@H]([C@@H]([C@@H]([C@@H](O1)C([O-])=O)O)O)O'],
                           'smarts_strings_count': 2,
                           'defs': ['is_beta_D_glucosiduronate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glucuronic acid moiety '
                                          'found"',
                                          'False, "Not in beta configuration"',
                                          'False, "Molecular weight too low '
                                          'for glucosiduronate"',
                                          'False, "Too few carbons for '
                                          'glucosiduronate"',
                                          'False, "Too few oxygens for '
                                          'glucosiduronate"',
                                          'False, "Does not contain exactly '
                                          'one deprotonated carboxyl group"',
                                          'True, "Contains glucuronic acid '
                                          'moiety in beta configuration with '
                                          'deprotonated carboxyl group"'],
                           'returns_count': 8,
                           'complexity': 4.3221835825288455},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)Br)O[C@@H]1CN(C)C(=O)NC3CCCC3)[C@H](C)CO',
                                     'name': '1-[[(4R,5S)-8-bromo-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-3-cyclopentyl-1-methylurea',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'C=1(C(=C2C(OC(C=3C=CC(O)=CC3)=CC2=O)=C(C1O)[C@@H]4[C@@H]([C@H]([C@@H](CO4)O)O)O)O)[C@H]5OC[C@@H]([C@@H]([C@H]5O)O)O',
                                     'name': '6-C-L-arabinopyranosyl-8-C-D-xylopyranosylapigenin',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'CCC(=O)N(C)C[C@@H]1[C@@H](CN(C(=O)C2=C(O1)N=CC(=C2)C#CC(C)C)[C@@H](C)CO)C',
                                     'name': 'N-[[(2S,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-8-(3-methylbut-1-ynyl)-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylpropanamide',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O[C@]2(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)O)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)CO)[C@H]4NC(=O)C)CO',
                                     'name': '(2S,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-3-[(2S,3R,4R,5R,6R)-3-Acetamido-5-hydroxy-4-[(2R,3R,4S,5S,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-4-hydroxy-5-[(2-hydroxyacetyl)amino]-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'O=C1O[C@@H](CC(=O)N(O)CCC[C@@H](NC(=O)C)C(=O)O[C@@H](CC(=O)N(O)CCC[C@H](C(O[C@@H](CC(N(CCC[C@H]1NC(=O)C)O)=O)C)=O)NC(=O)C)C)C',
                                     'name': 'Vicibactin',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCC)(OCCN)(O)=O',
                                     'name': 'PE(14:1(9Z)/19:1(9Z))',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'C#CC#C',
                                     'name': 'buta-1,3-diyne',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'OC1=C(C=C2[C@H](CCCC2=C1)C)C(CO)C',
                                     'name': 'Hypoxylan A',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'CCCCCC(O)CC(=O)OC(CC([O-])=O)C[N+](C)(C)C',
                                     'name': '3-hydroxyoctanoylcarnitine',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'},
                                 {   'smiles': 'O=C1C(=O)C=2C(=O)N\\C(\\C2C(=C1/C=C/CCC)O)=C/C',
                                     'name': 'Pyranterrone A',
                                     'reason': 'No glucuronic acid moiety '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C1(=CC=C(C=C1)CN2C3=C(C(=O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C([O-])=O)O)O)O)C=CC=C3N=C2OCC)C=5C=CC=CC5C6=NN=N[N-]6',
                                      'name': 'candesartan '
                                              'O-beta-D-glucuronoside(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'},
                                  {   'smiles': 'C=1(C2=CC=CC=C2C3=NN=N[N-]3)OC=4C=CC(=CC4C1Br)CN5C(=NC(=C5C(=O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)C([O-])=O)O)O)O)Cl)CCCC',
                                      'name': 'zolarsartan '
                                              'O-beta-D-glucuronoside(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'},
                                  {   'smiles': 'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3([C@@H]([C@@H]([C@@]2(C[C@@H](C1)O)[H])O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)O)[H])(CC[C@@]4([C@@H](CCC(=O)[O-])C)[H])[H])C)[H])C',
                                      'name': 'hyocholate '
                                              '6-O-(beta-D-glucuronide)(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'},
                                  {   'smiles': 'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])[H])(CC[C@@]4([C@@H](CCC([O-])=O)C)[H])[H])C)[H])C',
                                      'name': 'lithocholate '
                                              '3-O-(beta-D-glucuronide)(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'},
                                  {   'smiles': 'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C[C@@H]([C@@]2(C[C@@H](C1)O)[H])O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])(CC[C@@]4([C@@H](CCC(=O)[O-])C)[H])[H])C)[H])C',
                                      'name': 'hyodeoxycholate '
                                              '6-O-(beta-D-glucuronide)(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'},
                                  {   'smiles': 'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])O)[H])(CC[C@@]4([C@@H](CCC([O-])=O)C)[H])[H])C)[H])C',
                                      'name': 'chenodeoxycholate '
                                              '3-O-(beta-D-glucuronide)(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'},
                                  {   'smiles': 'C12=C(C(C)=C(C(=C1O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(=O)[O-])O)O)O)C/C=C(/CCC(=O)[O-])\\C)OC)COC2=O',
                                      'name': 'mycophenolate '
                                              '7-O-beta-D-glucuronide(2-)',
                                      'reason': 'Does not contain exactly one '
                                                'deprotonated carboxyl group'}],
    'attempt': 0,
    'reasoning': "Here's a program that attempts to classify chemical entities "
                 'as beta-D-glucosiduronates based on their SMILES string:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 37,
    'num_false_positives': 39,
    'num_true_negatives': 142217,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.4868421052631579,
    'recall': 0.8409090909090909,
    'f1': 0.6166666666666667,
    'accuracy': 0.9996767392832046,
    'negative_predictive_value': 0.9999507818652267}