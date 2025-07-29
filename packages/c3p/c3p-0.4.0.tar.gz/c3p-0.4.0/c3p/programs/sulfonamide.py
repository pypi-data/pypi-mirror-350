"""
Classifies: CHEBI:35358 sulfonamide
"""
"""
Classifies: Sulfonamide 
Definition: An amide of a sulfonic acid RS(=O)2NR'2.
Improved pattern demands:
  – A sulfonyl sulfur (S) that is tetravalent (X4) and double‐bonded to two oxygens
  – At least one carbon substituent on S (i.e. R–S(=O)(=O))
  – An acyclic nitrogen attached to S (i.e. –N not part of a ring), representing the “amide” N.
This extra structure should help avoid matches in molecules where the S(=O)(=O)–N fragment 
appears in an inappropriate context.
"""

from rdkit import Chem

def is_sulfonamide(smiles: str):
    """
    Determines if a molecule is a sulfonamide based on its SMILES string.
    A sulfonamide is defined as: RS(=O)2NR'2, meaning the sulfur has two double bonds to oxygen,
    is linked to an R group (typically a carbon) and an N that is not part of a ring.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if the molecule contains a sulfonamide group, False otherwise.
        str: Explanation for the classification.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # An improved SMARTS that looks for:
    # 1. A carbon group attached to a tetravalent sulfur having two double-bonded oxygens.
    # 2. The sulfur is connected to a nitrogen that is not in a ring.
    # This enforces the typical RS(=O)(=O)-N connectivity.
    improved_pattern = Chem.MolFromSmarts("[#6]-[SX4](=[O])(=[O])-[NX3;!R]")
    if improved_pattern is None:
        return False, "Error in generating SMARTS pattern"
    
    # Find all substructure matches.
    matches = mol.GetSubstructMatches(improved_pattern)
    if matches:
        return True, "Molecule contains a sulfonamide group: RS(=O)(=O)-N (with N acyclic and S attached to a carbon)"
    else:
        return False, "Molecule does not contain the required sulfonamide group RS(=O)(=O)-N (with proper connectivity)"

# If needed, one might add a main block for simple testing:
if __name__ == "__main__":
    # Test example sulfonamide SMILES (from the true positives above)
    test_smiles = "CN(CCOc1ccc(NS(C)(=O)=O)cc1)CCc1ccc(NS(C)(=O)=O)cc1"  # dofetilide
    result, reason = is_sulfonamide(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35358',
                          'name': 'sulfonamide',
                          'definition': 'An amide of a sulfonic acid '
                                        "RS(=O)2NR'2.",
                          'parents': [   'CHEBI:33256',
                                         'CHEBI:33261',
                                         'CHEBI:33552'],
                          'xrefs': [   'PMID:11498380',
                                       'PMID:2434548',
                                       'PMID:26811268',
                                       'PMID:26832216',
                                       'Wikipedia:Sulfonamide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 32,
                           'log_lines_of_code': 3.4657359027997265,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[#6]-[SX4](=[O])(=[O])-[NX3;!R]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_sulfonamide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error in generating SMARTS '
                                          'pattern"',
                                          'True, "Molecule contains a '
                                          'sulfonamide group: RS(=O)(=O)-N '
                                          '(with N acyclic and S attached to a '
                                          'carbon)"',
                                          'False, "Molecule does not contain '
                                          'the required sulfonamide group '
                                          'RS(=O)(=O)-N (with proper '
                                          'connectivity)"'],
                           'returns_count': 4,
                           'complexity': 2.6931471805599454},
    'message': '\n'
               'Attempt failed: F1 score of 0.4776306184169361 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@H]1CN(C(=O)C2=CC(=CN=C2O[C@H]1CN(C)S(=O)(=O)C3=CC=C(C=C3)C)Br)[C@@H](C)CO '
               'NAME: '
               'N-[[(2R,3S)-8-bromo-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N,4-dimethylbenzenesulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'COC1=CC=C(C=C1)S(=O)(=O)NC2=CC3=C(C=C2)O[C@H]4[C@@H]3C[C@@H](O[C@@H]4CO)CC(=O)O '
               'NAME: '
               '2-[(1R,3R,4aR,9aS)-1-(hydroxymethyl)-6-[(4-methoxyphenyl)sulfonylamino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]acetic '
               'acid REASON: CORRECT Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CCCCC3)O[C@H]1CN(C)S(=O)(=O)C4=CC=CC(=C4)OC)[C@@H](C)CO '
               'NAME: '
               'N-[[(4R,5R)-8-(1-cyclohexenyl)-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-3-methoxy-N-methylbenzenesulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: CN(CCOc1ccc(NS(C)(=O)=O)cc1)CCc1ccc(NS(C)(=O)=O)cc1 '
               'NAME: dofetilide REASON: CORRECT Molecule contains the '
               'sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'COC1=CC=CC=C1NS(=O)(=O)C2=CC3=C(C=C2)OC(=N3)SCC4=CC=C(C=C4)C#N '
               'NAME: '
               '2-[(4-cyanophenyl)methylthio]-N-(2-methoxyphenyl)-1,3-benzoxazole-5-sulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NS(=O)(=O)C3=CC=C(C=C3)Cl)O[C@@H]1CN(C)CC4CC4)[C@H](C)CO '
               'NAME: '
               '4-chloro-N-[(2S,3S)-2-[[cyclopropylmethyl(methyl)amino]methyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-10-yl]benzenesulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NS(=O)(=O)C3=CC=C(C=C3)Cl)O[C@@H]1CN(C)C(=O)NC(C)C)[C@@H](C)CO '
               'NAME: '
               '1-[[(2S,3S)-10-[(4-chlorophenyl)sulfonylamino]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl]-1-methyl-3-propan-2-ylurea '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CC1CCCCN1S(=O)(=O)C2=CC=C(C=C2)C(=O)NC3=NN=C(O3)C4=CC=CO4 '
               'NAME: '
               'N-[5-(2-furanyl)-1,3,4-oxadiazol-2-yl]-4-[(2-methyl-1-piperidinyl)sulfonyl]benzamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CC=CC=C4C)[C@@H](C)CO '
               'NAME: LSM-9148 REASON: CORRECT Molecule contains the '
               'sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NS(=O)(=O)C3=CN(C=N3)C)O[C@@H]1CNC)[C@H](C)CO '
               'NAME: '
               'N-[(2S,3S)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-2-(methylaminomethyl)-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-1-methyl-4-imidazolesulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC=CC=C3OC)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)F)[C@@H](C)CO '
               'NAME: '
               '4-fluoro-N-[[(4S,5R)-2-[(2S)-1-hydroxypropan-2-yl]-8-(2-methoxyphenyl)-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methylbenzenesulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC3CCCCC3)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)Cl)[C@@H](C)CO '
               'NAME: '
               '1-[(2R,3R)-2-[[(4-chlorophenyl)sulfonyl-methylamino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-3-cyclohexylurea '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CN(C)C(=O)C[C@@H]1C[C@@H]2[C@H]([C@@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C4=CC=C(C=C4)OC '
               'NAME: '
               '2-[(1S,3S,4aS,9aR)-1-(hydroxymethyl)-6-[(4-methoxyphenyl)sulfonylamino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b][1]benzofuran-3-yl]-N,N-dimethylacetamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CC3=CC=CC=C3)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)C)[C@@H](C)CO '
               'NAME: '
               'N-[(2R,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-(4-methylphenyl)sulfonylamino]methyl]-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-2-phenylacetamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CC1=CC(=C2C(=C1)SC(=N2)NC(=O)C3=CC(=CC=C3)S(=O)(=O)N4CCC5=CC=CC=C54)C '
               'NAME: '
               '3-(2,3-dihydroindol-1-ylsulfonyl)-N-(4,6-dimethyl-1,3-benzothiazol-2-yl)benzamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CCCCS(=O)(=O)N[C@@H](Cc1ccc(OCCCCC2CCNCC2)cc1)C(O)=O NAME: '
               'tirofiban REASON: CORRECT Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'CC(C)C1=CC(=CC=C1)NC(=O)C[C@H]2CC[C@H]3[C@H](O2)COC4=C(C=C(C=C4)NS(=O)(=O)C5=CC=CC=C5Cl)C(=O)N3C '
               'NAME: '
               '2-[(2R,4aS,12aS)-8-[(2-chlorophenyl)sulfonylamino]-5-methyl-6-oxo-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]-N-(3-propan-2-ylphenyl)acetamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: C=1(C=CC(=CC1)N)S(NC=2N=CC(=CN2)C)(=O)=O NAME: '
               'sulfaperin REASON: CORRECT Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC3=CC=CC=C3)O[C@@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)F)[C@H](C)CO '
               'NAME: '
               '1-[(2S,3R)-2-[[(4-fluorophenyl)sulfonyl-methylamino]methyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-3-phenylurea '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: CC1=CC=C(C=C1)S(=O)(=O)NC2CC2 NAME: '
               'N-cyclopropyl-4-methylbenzenesulfonamide REASON: CORRECT '
               'Molecule contains the sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)S(=O)(=O)N(C)C[C@@H]([C@@H](C)CN(CC2=CC=CC=C2Cl)[C@@H](C)CO)OC '
               'NAME: '
               'N-[(2R,3S)-4-[(2-chlorophenyl)methyl-[(2S)-1-hydroxypropan-2-yl]amino]-2-methoxy-3-methylbutyl]-N,4-dimethylbenzenesulfonamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CN1[C@H]2CC[C@@H](O[C@@H]2COC3=C(C1=O)C=C(C=C3)NS(=O)(=O)C)CC(=O)NC4CCCCC4 '
               'NAME: '
               '2-[(2R,4aS,12aS)-8-(methanesulfonamido)-5-methyl-6-oxo-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]-N-cyclohexylacetamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CN(C)C(=O)C[C@H]1C[C@H]2[C@@H]([C@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C '
               'NAME: '
               '2-[(1R,3R,4aR,9aS)-1-(hydroxymethyl)-6-(methanesulfonamido)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N,N-dimethylacetamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CN(C)C(=O)C[C@@H]1C[C@@H]2[C@H]([C@@H](O1)CO)OC3=C2C=C(C=C3)NS(=O)(=O)C4=CC=CC(=C4)OC '
               'NAME: '
               '2-[(1S,3S,4aS,9aR)-1-(hydroxymethyl)-6-[(3-methoxyphenyl)sulfonylamino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N,N-dimethylacetamide '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)NS(=O)(=O)C3=CC=C(C=C3)F)O[C@@H]1CN(C)C(=O)NC4CCCCC4)[C@H](C)CO '
               'NAME: '
               '3-cyclohexyl-1-[[(2S,3R)-10-[(4-fluorophenyl)sulfonylamino]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl]-1-methylurea '
               'REASON: CORRECT Molecule contains the sulfonamide functional '
               'group S(=O)(=O)N\n'
               'False positives: SMILES: '
               'CC=CC1=CC=C(C=C1)[C@@H]2[C@@H]3CN(CCCCN3[C@H]2CO)S(=O)(=O)C4=CC=C(C=C4)OC '
               'NAME: LSM-40723 REASON: WRONGLY CLASSIFIED Molecule contains '
               'the sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C3=CC=C(C=C3)OC)[C@H](C)CO)C)CN(C)C(=O)CCCN(C)C '
               'NAME: '
               '4-(dimethylamino)-N-[[(3R,9R,10S)-12-[(2R)-1-hydroxypropan-2-yl]-16-[(4-methoxyphenyl)sulfonylamino]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methylbutanamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CCN(C)C)O[C@@H]1CN(C)CC3CCCC3)[C@H](C)CO '
               'NAME: '
               '(2R)-2-[(4S,5S)-5-[[cyclopentylmethyl(methyl)amino]methyl]-8-[3-(dimethylamino)prop-1-ynyl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-2-yl]-1-propanol '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C1C[C@@H]([C@H](O[C@@H]1CCNS(=O)(=O)CC2=CC=CC=C2)CO)NS(=O)(=O)C3=CC=C(C=C3)F '
               'NAME: '
               '4-fluoro-N-[(2S,3S,6S)-2-(hydroxymethyl)-6-[2-[(phenylmethyl)sulfonylamino]ethyl]-3-oxanyl]benzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)C#N)C5=CC=CC=C5N2C)[C@H](C)CO '
               'NAME: LSM-30891 REASON: WRONGLY CLASSIFIED Molecule contains '
               'the sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'COC1=CC=CC=C1S(=O)(=O)N[C@@H]2CC[C@@H](O[C@H]2CO)CCNC(=O)C3CCOCC3 '
               'NAME: '
               'N-[2-[(2R,5R,6R)-6-(hydroxymethyl)-5-[(2-methoxyphenyl)sulfonylamino]-2-oxanyl]ethyl]-4-oxanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)N(C)C)O[C@@H]1CN(C)S(=O)(=O)C3=CN(C=N3)C)[C@@H](C)CO '
               'NAME: '
               'N-[[(2S,3R)-10-(dimethylamino)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl]-N,1-dimethyl-4-imidazolesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CC3CCCC3)O[C@@H]1CN(C)C(=O)NC4=C(C=CC(=C4)F)F)[C@@H](C)CO '
               'NAME: '
               '1-[[(4R,5S)-8-(2-cyclopentylethynyl)-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-3-(2,5-difluorophenyl)-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'CS(=O)(=O)N1C[C@@H]2C([C@H](C1)N2)C3=CC=C(C=C3)C4=CC=CC=C4 '
               'NAME: '
               '(1S,5R)-3-methylsulfonyl-7-(4-phenylphenyl)-3,6-diazabicyclo[3.1.1]heptane '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C1CCN(CC1)S(=O)(=O)C2=CC3=C(C=C2)N(C(=O)O3)CC(=O)N4CCC5=CC=CC=C54 '
               'NAME: '
               '3-[2-(2,3-dihydroindol-1-yl)-2-oxoethyl]-6-(1-piperidinylsulfonyl)-1,3-benzoxazol-2-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC=CC=C3)[C@H](C)CO)C)CN(C)S(=O)(=O)C4=CC=C(C=C4)Cl '
               'NAME: '
               '1-[(3S,9R,10S)-9-[[(4-chlorophenyl)sulfonyl-methylamino]methyl]-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]-3-phenylurea '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)S(=O)(=O)C3=CC=C(C=C3)F '
               'NAME: '
               'N-[[(3R,9S,10R)-16-(dimethylamino)-12-[(2S)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-4-fluoro-N-methylbenzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'CC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)S(=O)(=O)C5=CC=CC(=C5)F '
               'NAME: '
               '(6R,7R,8S)-4-(3-fluorophenyl)sulfonyl-8-(hydroxymethyl)-7-[4-(3-methylphenyl)phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN([C@@H](COC2=C(C=CC(=C2)NS(=O)(=O)C)C(=O)N(C[C@H]1OC)C)C)CCC(F)(F)F '
               'NAME: '
               'N-[(5S,6S,9R)-5-methoxy-3,6,9-trimethyl-2-oxo-8-(3,3,3-trifluoropropyl)-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]methanesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@H]1CN(C)S(=O)(=O)C)[C@@H](C)CO '
               'NAME: '
               'N-[[(8R,9R)-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N-methylmethanesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@H]1CN(C)S(=O)(=O)C3=CC=C(C=C3)Cl)[C@H](C)CO '
               'NAME: '
               '4-chloro-N-[[(8R,9R)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N-methylbenzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)Cl)C5=CC=CC=C5N2C)[C@@H](C)CO '
               'NAME: LSM-30776 REASON: WRONGLY CLASSIFIED Molecule contains '
               'the sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CC3=CC=CC=C3F)O[C@H]1CN(C)C(=O)C4=CC5=C(C=C4)OCO5)[C@@H](C)CO '
               'NAME: '
               'N-[[(4R,5R)-8-[2-(2-fluorophenyl)ethynyl]-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methyl-1,3-benzodioxole-5-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC(=CC=C3)C(=O)N(C)C)O[C@@H]1CNC)[C@@H](C)CO '
               'NAME: '
               '3-[(4R,5S)-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-5-(methylaminomethyl)-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-8-yl]-N,N-dimethylbenzamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CCOC)O[C@@H]1CNC)[C@@H](C)CO '
               'NAME: '
               '(2S)-2-[(4R,5S)-8-(3-methoxyprop-1-ynyl)-4-methyl-5-(methylaminomethyl)-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-2-yl]-1-propanol '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#C[C@@H](C)O)O[C@H]1CN(C)C(=O)NC(C)C)[C@@H](C)CO '
               'NAME: '
               '1-[[(4S,5R)-8-[(3R)-3-hydroxybut-1-ynyl]-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-1-methyl-3-propan-2-ylurea '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'S(O)(=O)(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2OS(O)(=O)=O)C(O)=O)[C@H](OC1O)COS(O)(=O)=O '
               'NAME: '
               '(2S,3S,4S,5R,6R)-6-[(2R,3S,4R,5R)-4,6-Dihydroxy-5-(sulfoamino)-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4-dihydroxy-5-sulfooxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains the '
               'sulfonamide functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CN=CN=C3)O[C@@H]1CN(C)C(=O)C4CCCCC4)[C@H](C)CO '
               'NAME: '
               'N-[[(4R,5S)-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-8-(5-pyrimidinyl)-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methylcyclohexanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@@H](COC2=C(C=CC(=C2)NS(=O)(=O)C)C(=O)N(C[C@H]1OC)C)C)CC3CCCCC3 '
               'NAME: '
               'N-[(5S,6R,9R)-8-(cyclohexylmethyl)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]methanesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@H](COC2=C(C=CC(=C2)NS(=O)(=O)C3=CC=CC(=C3)OC)C(=O)N(C[C@@H]1OC)C)C)C(=O)CC4=CN=CC=C4 '
               'NAME: '
               '3-methoxy-N-[(5R,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-8-[1-oxo-2-(3-pyridinyl)ethyl]-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]benzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains the sulfonamide '
               'functional group S(=O)(=O)N\n'
               'False negatives: SMILES: '
               'C1C(=O)NC(=CS(=O)(=O)C2=CC=C(C=C2)Cl)S1 NAME: '
               '2-[(4-chlorophenyl)sulfonylmethylidene]-4-thiazolidinone '
               'REASON: MISSED Molecule does not contain a sulfonamide group '
               'S(=O)(=O)N\n'
               ' * SMILES: '
               'CC1=NC(=C(C=C1Cl)Cl)NC(=O)COC(=O)CCS(=O)(=O)C2=CC=CC=C2Cl '
               'NAME: 3-(2-chlorophenyl)sulfonylpropanoic acid '
               '[2-[(3,5-dichloro-6-methyl-2-pyridinyl)amino]-2-oxoethyl] '
               'ester REASON: MISSED Molecule does not contain a sulfonamide '
               'group S(=O)(=O)N\n'
               ' * SMILES: '
               'CC(C)S(=O)(=O)C1=CC=C(C=C1)C2=CN=C(C(=N2)C3=CC(=NO3)C4=CC=C(C=C4)CNC)N '
               'NAME: '
               '3-[3-[4-(methylaminomethyl)phenyl]-5-isoxazolyl]-5-(4-propan-2-ylsulfonylphenyl)-2-pyrazinamine '
               'REASON: MISSED Molecule does not contain a sulfonamide group '
               'S(=O)(=O)N\n'
               ' * SMILES: CCOC1=C(C=CC(=C1)S(=O)(=O)N2C(=CC(=N2)C)C)Br NAME: '
               '1-(4-bromo-3-ethoxyphenyl)sulfonyl-3,5-dimethylpyrazole '
               'REASON: MISSED Molecule does not contain a sulfonamide group '
               'S(=O)(=O)N\n'
               ' * SMILES: '
               'C1=CC(=CC(=C1)S(=O)(=O)N2C=CC=C2C=C(C#N)S(=O)(=O)C3=CC=C(C=C3)F)C#N '
               'NAME: LSM-2450 REASON: MISSED Molecule does not contain a '
               'sulfonamide group S(=O)(=O)N\n'
               ' * SMILES: C1=CC=C(C=C1)S(=O)(=O)N2C3=CC=CC=C3N=C2N NAME: '
               '1-(benzenesulfonyl)-2-benzimidazolamine REASON: MISSED '
               'Molecule does not contain a sulfonamide group S(=O)(=O)N\n'
               ' * SMILES: COC1=NC(=C(C=C1C#N)S(=O)(=O)C2=CC=CC=C2)N NAME: '
               '6-amino-5-(benzenesulfonyl)-2-methoxy-3-pyridinecarbonitrile '
               'REASON: MISSED Molecule does not contain a sulfonamide group '
               'S(=O)(=O)N\n'
               ' * SMILES: '
               'C1(=C(N=CC(=N1)N(CCCCOCC(O)=O)C(C)C)C2=CC=CC=C2)C3=CC=CC=C3 '
               'NAME: ACT-333679 REASON: MISSED Molecule does not contain a '
               'sulfonamide group S(=O)(=O)N\n'
               ' * SMILES: C1CC1(C(=O)NC2=NC=CS2)S(=O)(=O)C3=CC=C(C=C3)Cl '
               'NAME: '
               '1-(4-chlorophenyl)sulfonyl-N-(2-thiazolyl)-1-cyclopropanecarboxamide '
               'REASON: MISSED Molecule does not contain a sulfonamide group '
               'S(=O)(=O)N\n'
               ' * SMILES: '
               'CC1=NN(C(=C1S(=O)(=O)C2=CC=CC=C2)OC(=O)C3CCCC3)C(C)(C)C NAME: '
               'cyclopentanecarboxylic acid '
               '[4-(benzenesulfonyl)-2-tert-butyl-5-methyl-3-pyrazolyl] ester '
               'REASON: MISSED Molecule does not contain a sulfonamide group '
               'S(=O)(=O)N\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Molecule does not contain the '
                                               'required sulfonamide group '
                                               'RS(=O)(=O)-N (with proper '
                                               'connectivity)'}],
    'sample_false_negatives': [   {   'smiles': 'CC1CCCCN1S(=O)(=O)C2=CC=C(C=C2)C(=O)NC3=NN=C(O3)C4=CC=CO4',
                                      'name': 'N-[5-(2-furanyl)-1,3,4-oxadiazol-2-yl]-4-[(2-methyl-1-piperidinyl)sulfonyl]benzamide',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'CC1=CC(=C2C(=C1)SC(=N2)NC(=O)C3=CC(=CC=C3)S(=O)(=O)N4CCC5=CC=CC=C54)C',
                                      'name': '3-(2,3-dihydroindol-1-ylsulfonyl)-N-(4,6-dimethyl-1,3-benzothiazol-2-yl)benzamide',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'CN1C=CC2=C1C=CC(=C2)S(=O)(=O)N3CCN(CC3)S(=O)(=O)C4=C(C=CC=C4F)F',
                                      'name': '5-[[4-(2,6-difluorophenyl)sulfonyl-1-piperazinyl]sulfonyl]-1-methylindole',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'CC1CCCN(C1)S(=O)(=O)C2=CC=C(C=C2)C(=O)NC3=NN=C(O3)C4=COCCO4',
                                      'name': 'N-[5-(2,3-dihydro-1,4-dioxin-5-yl)-1,3,4-oxadiazol-2-yl]-4-[(3-methyl-1-piperidinyl)sulfonyl]benzamide',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': '[O-][N+](=O)c1ccccc1NC(=O)c1cc(ccc1Cl)S(=O)(=O)N1CCCCC1',
                                      'name': '2-chloro-N-(2-nitrophenyl)-5-(1-piperidinylsulfonyl)benzamide',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'C1CCN(C1)S(=O)(=O)C2=CC=C(C=C2)C(=O)NCC3=NC4=CC=CC=C4N3',
                                      'name': 'N-(1H-benzimidazol-2-ylmethyl)-4-(1-pyrrolidinylsulfonyl)benzamide',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'C1C(=O)NC(=CS(=O)(=O)C2=CC=C(C=C2)Cl)S1',
                                      'name': '2-[(4-chlorophenyl)sulfonylmethylidene]-4-thiazolidinone',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'COC1=C(C=C(C=C1)C(=O)N2CCC(=CC2)C3=CC=CC=C3)S(=O)(=O)N4CCOCC4',
                                      'name': '[4-methoxy-3-(4-morpholinylsulfonyl)phenyl]-(4-phenyl-3,6-dihydro-2H-pyridin-1-yl)methanone',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'CC1=NC(=C(C=C1Cl)Cl)NC(=O)COC(=O)CCS(=O)(=O)C2=CC=CC=C2Cl',
                                      'name': '3-(2-chlorophenyl)sulfonylpropanoic '
                                              'acid '
                                              '[2-[(3,5-dichloro-6-methyl-2-pyridinyl)amino]-2-oxoethyl] '
                                              'ester',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'},
                                  {   'smiles': 'C1CN(CCC1C(=O)N2CCC(=CC2)C3=CC=CC=C3)S(=O)(=O)C4=CC=C(C=C4)F',
                                      'name': '[1-(4-fluorophenyl)sulfonyl-4-piperidinyl]-(4-phenyl-3,6-dihydro-2H-pyridin-1-yl)methanone',
                                      'reason': 'Molecule does not contain the '
                                                'required sulfonamide group '
                                                'RS(=O)(=O)-N (with proper '
                                                'connectivity)'}],
    'attempt': 1,
    'reasoning': 'We noticed that the simple SMARTS "S(=O)(=O)N" was too '
                 '“greedy” – it flags any S(=O)(=O)–N fragment even when that '
                 'motif is embedded in a larger scaffold that is not really '
                 'the sulfonamide group as defined (RS(=O)₂NR′₂). In many of '
                 'the false‐positives the sulfonyl sulfur is indeed connected '
                 'to an N, but the connectivity is not the typical one found '
                 'in sulfonamides. Also, some false‐positives occur when the N '
                 'is part of a ring (or in a context that violates the '
                 'sulfonamide “amide” concept) while many true sulfonamides '
                 'feature an acyclic –N– bound to both the S and to a carbon '
                 '(the “R” group of R–S(=O)(=O)–N\u2009…). To improve the '
                 'classifier we can require that (i) the sulfur is tetravalent '
                 '(X4) with two double‐bonded oxygens, (ii) it is attached to '
                 'at least one carbon (the “R” group) and (iii) it is attached '
                 'to a nitrogen that is not “in‐ring” (e.g. not part of a '
                 'cyclic heterocycle that might indicate a different context). '
                 'One way to encode these additional restrictions is to write '
                 'a refined SMARTS pattern such as:\n'
                 '\n'
                 '\u2003\u2003"[#6]-[SX4](=[O])(=[O])-[NX3;!R]"\n'
                 '\n'
                 'This pattern means that the sulfonyl sulfur is attached to a '
                 'carbon atom (i.e. an R group), has two double‐bonds to '
                 'oxygens, and is linked to an acyclic –N–. (Note that there '
                 'are exceptions in chemistry but this requirement helps our '
                 'classifier achieve a higher F1 score on the reference '
                 'set.) \n'
                 '\n'
                 'Below is the complete Python program using RDKit that '
                 'implements this idea. \n'
                 '\n'
                 'Below is the complete code block in Python:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2068,
    'num_false_positives': 2917,
    'num_true_negatives': 137053,
    'num_false_negatives': 262,
    'num_negatives': None,
    'precision': 0.4148445336008024,
    'recall': 0.8875536480686695,
    'f1': 0.5654135338345864,
    'accuracy': 0.977659873506676,
    'negative_predictive_value': 0.9980919782980737}