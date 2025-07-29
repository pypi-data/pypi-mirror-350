"""
Classifies: CHEBI:17002 cholesteryl ester
"""
"""
Classifies: CHEBI:38048 cholesteryl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_cholesteryl_ester(smiles: str):
    """
    Determines if a molecule is a cholesteryl ester based on its SMILES string.
    A cholesteryl ester is a sterol ester obtained by formal condensation of the carboxy group
    of any carboxylic acid with the 3-hydroxy group of cholesterol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cholesteryl ester, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for cholesterol backbone
    cholesterol_pattern = Chem.MolFromSmarts("[C@@H]1CC[C@@]2([C@@H]3CC[C@@]4(C)[C@H](CC[C@@H]4[C@H]3CC=C2C1)[C@@H](C)CCCC(C)C)C")
    if not mol.HasSubstructMatch(cholesterol_pattern):
        return False, "No cholesterol backbone found"
        
    # Look for ester group (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 1"

    # Check for acyl chain (carbon chain attached to ester)
    acyl_pattern = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]")
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    if not acyl_matches:
        return False, "No acyl chain found"

    # Count rotatable bonds to verify long acyl chain
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 5:
        return False, "Acyl chain too short"

    # Check molecular weight - cholesteryl esters typically >500 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 500:
        return False, "Molecular weight too low for cholesteryl ester"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 30:
        return False, "Too few carbons for cholesteryl ester"
    if o_count != 2:
        return False, "Must have exactly 2 oxygens (ester group)"

    return True, "Contains cholesterol backbone with acyl chain attached via ester bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17002',
                          'name': 'cholesteryl ester',
                          'definition': 'A sterol ester obtained by formal '
                                        'condensation of the carboxy group of '
                                        'any carboxylic acid with the '
                                        '3-hydroxy group of cholesterol.',
                          'parents': ['CHEBI:35915'],
                          'xrefs': ['KEGG:C02530', 'PMID:2474544'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 44,
                           'log_lines_of_code': 3.784189633918261,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'GetSubstructMatches',
                                                 'CalcNumRotatableBonds',
                                                 'CalcExactMolWt'],
                           'methods_called_count': 8,
                           'smarts_strings': [   '[OX2][CX3](=[OX1])',
                                                 '[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]',
                                                 '[C@@H]1CC[C@@]2([C@@H]3CC[C@@]4(C)[C@H](CC[C@@H]4[C@H]3CC=C2C1)[C@@H](C)CCCC(C)C)C'],
                           'smarts_strings_count': 3,
                           'defs': ['is_cholesteryl_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No cholesterol backbone '
                                          'found"',
                                          'False, f"Found {len(ester_matches)} '
                                          'ester groups, need exactly 1"',
                                          'False, "No acyl chain found"',
                                          'False, "Acyl chain too short"',
                                          'False, "Molecular weight too low '
                                          'for cholesteryl ester"',
                                          'False, "Too few carbons for '
                                          'cholesteryl ester"',
                                          'False, "Must have exactly 2 oxygens '
                                          '(ester group)"',
                                          'True, "Contains cholesterol '
                                          'backbone with acyl chain attached '
                                          'via ester bond"'],
                           'returns_count': 9,
                           'complexity': 4.756837926783652},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O(C(C)=C)C(=O)C',
                                     'name': 'Isopropenyl acetate',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'CCC(=O)N1[C@@H]([C@H]([C@H]1CO)C2=CC=CC=C2)CN(C(C)C)S(=O)(=O)C',
                                     'name': 'N-[[(2S,3R,4S)-4-(hydroxymethyl)-1-(1-oxopropyl)-3-phenyl-2-azetidinyl]methyl]-N-propan-2-ylmethanesulfonamide',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'C1(CC(C(C(C1)=O)C(=O)CC)=O)C(=O)O',
                                     'name': 'prohexadione',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'NC(=N)NCCCCNC(=O)c1ccccc1',
                                     'name': 'benzoylagmatine',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'O.OC[C@H](NC1=NC=2N(C=NC2C(=N1)NC3=CC(C4=NC=CC=C4)=CC=C3)C(C)C)CC.Cl',
                                     'name': '(R)-DRF053 hydrochloride hydrate',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'S(OC=1C=C(C=CC1)/C=C/C(O)=O)(O)(=O)=O',
                                     'name': '3-Hydroxycinnamate sulfate',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'COc1ccc2C3COc4cc(O)ccc4C3Oc2c1',
                                     'name': 'medicarpin',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'OC1CC2C(CCCC2(C)C)(C=C1C(O)=O)C',
                                     'name': '3-hydroxy-5,5,8a-trimethyl-3,4,4a,6,7,8-hexahydronaphthalene-2-carboxylic '
                                             'acid',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(18:1(9Z)/20:2(11Z,14Z))',
                                     'reason': 'No cholesterol backbone found'},
                                 {   'smiles': 'O([C@@H]1[C@@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]([C@H]1O)CO)O)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-2-[(2S,3R,4S,5R,6R)-2,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-4-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No cholesterol backbone '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'O([C@@H]1CC=2[C@@]([C@@H]3[C@H]([C@H]4[C@@]([C@H](CC4)[C@@H](CCCC(C)C)C)(CC3)C)CC2)(CC1)C)C(=O)CCCCC(=O)C[C@@H]5[C@H]([C@H](O)C[C@@H]5O)/C=C/[C@@H](O)CCCCC',
                                      'name': 'CE(6 keto-PGF1alpha)',
                                      'reason': 'Must have exactly 2 oxygens '
                                                '(ester group)'},
                                  {   'smiles': 'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@H](CC[C@]4(C)[C@H]3CC[C@]12C)OC(C)=O',
                                      'name': 'cholesteryl acetate',
                                      'reason': 'Molecular weight too low for '
                                                'cholesteryl ester'},
                                  {   'smiles': 'C(\\CCCC(=O)O[C@H]1CC[C@]2(C(C1)=CC[C@@]3([C@@]2(CC[C@]4([C@]3(CC[C@@]4([C@@](CCCC(C)C)(C)[H])[H])[H])C)[H])[H])C)=C\\C/C=C\\CC(/C=C/C=C\\CCCCC)OO',
                                      'name': 'cholesteryl '
                                              '11-hydroperoxy-eicosatetraenoate',
                                      'reason': 'Must have exactly 2 oxygens '
                                                '(ester group)'},
                                  {   'smiles': 'O(C1CC=2C(C3C(C4C(C(CC4)C(CCCC(C)C)C)(CC3)C)CC2)(CC1)C)C(=O)CCCCCCCCCCCCCCC=5OC(=C(C5C)C)CCCCC',
                                      'name': 'CE(15D5)',
                                      'reason': 'Must have exactly 2 oxygens '
                                                '(ester group)'},
                                  {   'smiles': 'C(CCCCCCCCCC(O[C@@H]1CC=2[C@]([C@]3(CC[C@]4([C@]([C@@]3(CC2)[H])(CC[C@@]4([C@H](C)CCCC(C)C)[H])[H])C)[H])(C)CC1)=O)C=5N6[B-]([N+]7=C(C=CC7=CC6=CC5)C=8C=CC(=CC8)OC)(F)F',
                                      'name': 'CholEsteryl BODIPY 542/563 C11',
                                      'reason': 'Must have exactly 2 oxygens '
                                                '(ester group)'},
                                  {   'smiles': 'S(C[C@H](N)C(O[C@@H]1CC=2[C@@]([C@@H]3[C@H]([C@H]4[C@@]([C@H](CC4)[C@@H](CCCC(C)C)C)(CC3)C)CC2)(CC1)C)=O)[C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC',
                                      'name': 'CE(LTE4)',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 1'},
                                  {   'smiles': 'O(C1CC=2C(C3C(C4C(C(CC4)C(CCCC(C)C)C)(CC3)C)CC2)(CC1)C)C(=O)/C=C/C5=CC(OC)=C(O)C=C5',
                                      'name': 'Cholesteryl ferulate',
                                      'reason': 'Must have exactly 2 oxygens '
                                                '(ester group)'}],
    'attempt': 0,
    'reasoning': "Here's a program to classify chemical entities as "
                 'cholesteryl esters based on their SMILES strings:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 34,
    'num_false_positives': 5,
    'num_true_negatives': 142254,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.8717948717948718,
    'recall': 0.8292682926829268,
    'f1': 0.8500000000000001,
    'accuracy': 0.9999156711173577,
    'negative_predictive_value': 0.9999507946661418}