"""
Classifies: CHEBI:88061 polyamine
"""
"""
Classifies: CHEBI:36357 polyamine
Any organic amino compound that contains two or more amino groups.
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polyamine(smiles: str):
    """
    Determines if a molecule is a polyamine based on its SMILES string.
    A polyamine is an organic amino compound that contains two or more amino groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyamine, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of amino groups
    amino_pattern = Chem.MolFromSmarts("[NH2]")
    amino_matches = mol.GetSubstructMatches(amino_pattern)
    n_amino_groups = len(amino_matches)

    if n_amino_groups < 2:
        return False, "Must have at least 2 amino groups to be a polyamine"

    # Check if the molecule is organic (contains carbon)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count == 0:
        return False, "Not an organic compound (no carbon atoms)"

    # Check for common inorganic polyamines like hydrazine
    inorganic_pattern = Chem.MolFromSmarts("[!#6;!#7]")
    if mol.HasSubstructMatch(inorganic_pattern):
        return False, "Contains non-organic atoms, likely an inorganic polyamine"

    return True, f"Organic compound with {n_amino_groups} amino groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:88061',
                          'name': 'polyamine',
                          'definition': 'Any organic amino compound that '
                                        'contains two or more amino groups.',
                          'parents': ['CHEBI:50047'],
                          'xrefs': ['Wikipedia:Polyamine'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
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
                                                 0,
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
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetSubstructMatches',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum'],
                           'methods_called_count': 6,
                           'smarts_strings': ['[!#6;!#7]', '[NH2]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_polyamine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Must have at least 2 amino '
                                          'groups to be a polyamine"',
                                          'False, "Not an organic compound (no '
                                          'carbon atoms)"',
                                          'False, "Contains non-organic atoms, '
                                          'likely an inorganic polyamine"',
                                          'True, f"Organic compound with '
                                          '{n_amino_groups} amino groups"'],
                           'returns_count': 5,
                           'complexity': 3.4664409020350404},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)Br)O[C@@H]1CN(C)C(=O)NC3CCCC3)[C@H](C)CO',
                                     'name': '1-[[(4R,5S)-8-bromo-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-3-cyclopentyl-1-methylurea',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'C=1(C(=C2C(OC(C=3C=CC(O)=CC3)=CC2=O)=C(C1O)[C@@H]4[C@@H]([C@H]([C@@H](CO4)O)O)O)O)[C@H]5OC[C@@H]([C@@H]([C@H]5O)O)O',
                                     'name': '6-C-L-arabinopyranosyl-8-C-D-xylopyranosylapigenin',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'CCC(=O)N(C)C[C@@H]1[C@@H](CN(C(=O)C2=C(O1)N=CC(=C2)C#CC(C)C)[C@@H](C)CO)C',
                                     'name': 'N-[[(2S,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-8-(3-methylbut-1-ynyl)-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylpropanamide',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'O([C@@H]1[C@H](O[C@]2(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)O)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)CO)[C@H]4NC(=O)C)CO',
                                     'name': '(2S,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-3-[(2S,3R,4R,5R,6R)-3-Acetamido-5-hydroxy-4-[(2R,3R,4S,5S,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-4-hydroxy-5-[(2-hydroxyacetyl)amino]-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'O=C1O[C@@H](CC(=O)N(O)CCC[C@@H](NC(=O)C)C(=O)O[C@@H](CC(=O)N(O)CCC[C@H](C(O[C@@H](CC(N(CCC[C@H]1NC(=O)C)O)=O)C)=O)NC(=O)C)C)C',
                                     'name': 'Vicibactin',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCC)(OCCN)(O)=O',
                                     'name': 'PE(14:1(9Z)/19:1(9Z))',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'C#CC#C',
                                     'name': 'buta-1,3-diyne',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'OC1=C(C=C2[C@H](CCCC2=C1)C)C(CO)C',
                                     'name': 'Hypoxylan A',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'CCCCCC(O)CC(=O)OC(CC([O-])=O)C[N+](C)(C)C',
                                     'name': '3-hydroxyoctanoylcarnitine',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'},
                                 {   'smiles': 'O=C1C(=O)C=2C(=O)N\\C(\\C2C(=C1/C=C/CCC)O)=C/C',
                                     'name': 'Pyranterrone A',
                                     'reason': 'Must have at least 2 amino '
                                               'groups to be a polyamine'}],
    'sample_false_negatives': [   {   'smiles': 'C=1C(=CC(C)=CC1C)OCC(NC2=NC(=NC(=N2)N)C(C)(C)F)C',
                                      'name': 'N-[1-(3,5-dimethylphenoxy)propan-2-yl]-6-(2-fluoropropan-2-yl)-1,3,5-triazine-2,4-diamine',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'CC(C)Nc1nc(Cl)nc(NC(C)C)n1',
                                      'name': 'propazine',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'C(CN(CC1=NC=CC=C1)CC2=NC=CC=C2)N(CC3=NC=CC=C3)CC4=NC=CC=C4',
                                      'name': "N,N,N',N'-tetrakis(2-pyridylmethyl)ethylenediamine",
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'COCCCNc1nc(NCCCOC)nc(OC)n1',
                                      'name': 'methometon',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'CCNc1nc(O)nc(NC(C)C)n1',
                                      'name': '4-ethylamino-6-isopropylamino-1,3,5-triazin-2-ol',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'CCNc1nc(O)nc(NCC)n1',
                                      'name': 'simazine-2-hydroxy',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'CCNc1nc(Cl)nc(NC(C)CC)n1',
                                      'name': "N-(butan-2-yl)-6-chloro-N'-ethyl-1,3,5-triazine-2,4-diamine",
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'CC(C)Nc1nc(N)nc(Cl)n1',
                                      'name': 'deethylatrazine',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'N1=C(N=C(N=C1C(C)F)N)NC2C(CC3=C2C=C(C=C3)C)C',
                                      'name': 'N-(2,6-dimethylindan-1-yl)-6-(1-fluoroethyl)-1,3,5-triazine-2,4-diamine',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'},
                                  {   'smiles': 'COC1=C(NC2=NC(NC3=CC=CC=C3S(=O)(=O)C(C)C)=NC=N2)C=CC(=C1)N1CCC(CC1)N1CCN(C)CC1',
                                      'name': 'ASP-3026',
                                      'reason': 'Must have at least 2 amino '
                                                'groups to be a polyamine'}],
    'attempt': 0,
    'reasoning': "Here's a program to classify chemical entities as polyamines "
                 'based on their SMILES strings:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 35,
    'num_false_positives': 98,
    'num_true_negatives': 142069,
    'num_false_negatives': 98,
    'num_negatives': None,
    'precision': 0.2631578947368421,
    'recall': 0.2631578947368421,
    'f1': 0.2631578947368421,
    'accuracy': 0.9986226282501757,
    'negative_predictive_value': 0.9993106698460261}