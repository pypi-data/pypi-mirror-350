"""
Classifies: CHEBI:33704 alpha-amino acid
"""
"""
Classifies: CHEBI:16669 alpha-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is an alpha-amino acid based on its SMILES string.
    An alpha-amino acid is an amino acid in which the amino group is located on the carbon atom
    at the position alpha to the carboxyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alpha-amino acid, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define SMARTS pattern for alpha-amino acid
    alpha_amino_acid_pattern = Chem.MolFromSmarts("[N;H2][C;X4][C;X3](=O)[O;H1]")

    # Check if the molecule matches the pattern
    if mol.HasSubstructMatch(alpha_amino_acid_pattern):
        # Assign stereochemistry and check if the matched substructure is alpha
        AllChem.AssignStereochemistry(mol)
        matches = mol.GetSubstructMatches(alpha_amino_acid_pattern)
        for match in matches:
            alpha_carbon = mol.GetAtomWithIdx(match[1])
            if alpha_carbon.GetHybridization() == Chem.HybridizationType.SP3:
                return True, "Contains an amino group at the alpha position to a carboxyl group"

    return False, "No alpha-amino acid substructure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33704',
                          'name': 'alpha-amino acid',
                          'definition': 'An amino acid in which the amino '
                                        'group is located on the carbon atom '
                                        'at the position alpha to the carboxy '
                                        'group.',
                          'parents': ['CHEBI:33709'],
                          'xrefs': ['KEGG:C00045', 'KEGG:C05167'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 26,
                           'log_lines_of_code': 3.258096538021482,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts',
                                                 'GetHybridization',
                                                 'AssignStereochemistry',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 7,
                           'smarts_strings': ['[N;H2][C;X4][C;X3](=O)[O;H1]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_alpha_amino_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains an amino group at '
                                          'the alpha position to a carboxyl '
                                          'group"',
                                          'False, "No alpha-amino acid '
                                          'substructure found"'],
                           'returns_count': 3,
                           'complexity': 3.651619307604297},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'OC1=C(CC2(C3C(CCC2C)(C(=CCC3)C)C)C)C(=O)C(=O)C=C1NCC(O)=O '
               'NAME: SCHEMBL21397201 REASON: MISSED No amino and/or carboxyl '
               'groups found\n'
               ' * SMILES: CC(=O)CNCCCCC(N)C(O)=O NAME: N(6)-acetonyllysine '
               'REASON: MISSED No amino and/or carboxyl groups found\n'
               ' * SMILES: N[C@@H](CS\\C(Cl)=C/Cl)C(O)=O NAME: '
               'S-(trans-1,2-dichlorovinyl)-L-cysteine REASON: MISSED No amino '
               'and/or carboxyl groups found\n'
               ' * SMILES: N[C@@H](CCP(O)=O)C(O)=O NAME: '
               'Demethylphosphinothricin REASON: MISSED No amino and/or '
               'carboxyl groups found\n'
               ' * SMILES: NC(CC1=CC=C(CP(O)(O)=O)C=C1)C(O)=O NAME: '
               '4-(phosphonomethyl)phenylalanine REASON: MISSED No amino '
               'and/or carboxyl groups found\n'
               ' * SMILES: OC(=O)[C@@H](N(C)C)CCCCN NAME: N,N-Dimethyllysine '
               'REASON: MISSED No amino and/or carboxyl groups found\n'
               ' * SMILES: NC(Cc1ccc(Oc2ccc(O)cc2)cc1)C(O)=O NAME: thyronine '
               'REASON: MISSED No amino and/or carboxyl groups found\n'
               ' * SMILES: O=C(O)[C@@]1(N[C@@](C(=O)O)(C)C1)CC(C)C NAME: '
               '(-)-monascumic acid REASON: MISSED No amino and/or carboxyl '
               'groups found\n'
               ' * SMILES: NC(CCCNC(=N)NO)C(O)=O NAME: '
               'N(5)-[(hydroxyamino)(imino)methyl]ornithine REASON: MISSED No '
               'amino and/or carboxyl groups found\n'
               ' * SMILES: CC(CC[C@H](N)C(O)=O)NC(N)=N NAME: '
               '5-methyl-L-arginine REASON: MISSED No amino and/or carboxyl '
               'groups found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O[C@H]1[C@H](O[C@H]2[C@@H](O[C@@H]([C@@H](O)[C@@H]2O)C([O-])=O)Oc2cc(O)c3c(c2)oc(cc3=O)-c2ccc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)c(O)c2)O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O',
                                     'name': 'luteolin '
                                             '7-O-[(beta-D-glucosyluronate)-(1->2)-(beta-D-glucosiduronate)] '
                                             "4'-O-beta-D-glucosiduronate",
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'C1(=CNC2=C1C=CC=C2)CC(C(=O)O)=N',
                                     'name': '2-imino-3-(indol-3-yl)propanoic '
                                             'acid',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3CCCCC3)[C@H](C)CO)C)CN(C)C(=O)C4=CC=NC=C4',
                                     'name': 'N-[[(3R,9S,10R)-16-[[cyclohexyl(oxo)methyl]amino]-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methyl-4-pyridinecarboxamide',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'CC(C)C[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](C)C(O)=O',
                                     'name': 'Glu-Leu-Phe-Ala',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC=2NC=NC2',
                                     'name': 'Tyr-His-Lys',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'CC(=O)NCCNc1cccc2c(cccc12)S(O)(=O)=O',
                                     'name': '5-[(2-acetamidoethyl)amino]naphthalene-1-sulfonic '
                                             'acid',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'FC(F)(F)C1=NC(=C(C=C1)C(=O)NC=2C(F)=CC=CC2)C',
                                     'name': 'N-(2-fluorophenyl)-2-methyl-6-(trifluoromethyl)nicotinamide',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'O(C(COP(=O)(O)O)COC(=O)CCCCCCCC=CCCCCCCCC)C(=O)CCCCCCCC=CCCCCCCCC',
                                     'name': '1,2-bis(octadec-9-enoyl)phosphatidic '
                                             'acid',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(18:1(11Z)/14:0/18:3(9Z,12Z,15Z))',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'},
                                 {   'smiles': 'CCCNC(=O)NC1=CC2=C(C=C1)OC[C@@H](N(C[C@@H]([C@H](CN(C2=O)C)OC)C)C(=O)CC)C',
                                     'name': '1-[(4S,7S,8R)-8-methoxy-4,7,10-trimethyl-11-oxo-5-(1-oxopropyl)-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-3-propylurea',
                                     'reason': 'No alpha-amino acid '
                                               'substructure found'}],
    'sample_false_negatives': [   {   'smiles': 'OC1=C(CC2(C3C(CCC2C)(C(=CCC3)C)C)C)C(=O)C(=O)C=C1NCC(O)=O',
                                      'name': 'SCHEMBL21397201',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'OC(=O)[C@@H](N(C)C)CCCCN',
                                      'name': 'N,N-Dimethyllysine',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'O=C(O)[C@@]1(N[C@@](C(=O)O)(C)C1)CC(C)C',
                                      'name': '(-)-monascumic acid',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'O=C1C(OC)=C(NC(C(=O)O)CCCN=C2C(OC)C(NCCCC(NC3=C(OC)C(=O)CC(C3)(O)CO)C(=O)O)=CC(C2)(O)CO)CC(C1)(O)CO',
                                      'name': 'Nostoc-756',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': '[C@@H]1([C@H](CCN1)O)C(O)=O',
                                      'name': 'cis-3-hydroxy-D-proline',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'CN[C@@H](Cc1ccccc1)C(O)=O',
                                      'name': 'N-methyl-L-phenylalanine',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'N\\C(=C/C=C/C(O)=O)C(O)=O',
                                      'name': '(2Z,4E)-2-aminomuconic acid',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'OC1CNC(C1)C(O)=O',
                                      'name': '4-hydroxyproline',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': '[H][C@@](\\N=C1CC(O)(CO)CC(NCC(O)=O)=C\\1OC)([C@H](C)O)C(O)=O',
                                      'name': 'porphyra-334',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'},
                                  {   'smiles': 'OC(=O)C1CC(\\C=C(N1)C(O)=O)=C/C=N\\CCc1ccc(O)cc1',
                                      'name': 'Miraxanthin-III',
                                      'reason': 'No alpha-amino acid '
                                                'substructure found'}],
    'attempt': 3,
    'reasoning': 'The previous code attempts to identify alpha-amino acids by '
                 'looking for the presence of an amino group and a carboxyl '
                 'group in the molecule, and then checking if the amino group '
                 'is located on the carbon atom at the alpha position relative '
                 'to the carboxyl group. However, there are a few issues with '
                 'this approach:\n'
                 '\n'
                 '1. **Stereochemistry handling**: The code tries to handle '
                 'stereochemistry by checking the bond stereo between the '
                 'alpha carbon and the carboxyl carbon. However, this approach '
                 'is not robust enough to handle all possible cases. For '
                 "example, it doesn't account for cases where the "
                 'stereochemistry is not specified or is specified incorrectly '
                 'in the SMILES string.\n'
                 '\n'
                 '2. **Terminal groups**: The code avoids checking terminal '
                 'atoms for the alpha position, but this might exclude some '
                 'valid alpha-amino acids where the amino or carboxyl group is '
                 'terminal.\n'
                 '\n'
                 '3. **Missed substructures**: The code only checks for the '
                 'presence of a single amino and carboxyl group. However, some '
                 'alpha-amino acids might have additional functional groups or '
                 'substituents, which the current code might miss.\n'
                 '\n'
                 "4. **Molecular features**: The code doesn't consider other "
                 'molecular features that could be used to identify '
                 'alpha-amino acids, such as molecular weight, hydrogen bond '
                 'donors/acceptors, or specific substructure patterns.\n'
                 '\n'
                 'To improve the program, here are some suggestions:\n'
                 '\n'
                 '1. **Use a substructure matching approach**: Instead of '
                 'checking for individual functional groups and their relative '
                 'positions, it might be more robust to use a substructure '
                 'matching approach. This involves defining a SMARTS pattern '
                 'that represents the core structure of an alpha-amino acid '
                 'and checking if the given SMILES matches this pattern.\n'
                 '\n'
                 '2. **Handle stereochemistry more robustly**: Instead of '
                 'relying on bond stereo, consider using the '
                 '`AllChem.AssignStereochemistry` function from RDKit to '
                 'assign stereochemistry based on the SMILES string and '
                 'molecular geometry. This could help handle cases where '
                 'stereochemistry is not specified or is specified '
                 'incorrectly.\n'
                 '\n'
                 '3. **Consider additional molecular features**: Incorporate '
                 'other molecular features, such as molecular weight, hydrogen '
                 'bond donors/acceptors, or specific substructure patterns, to '
                 'improve the classification accuracy.\n'
                 '\n'
                 '4. **Use machine learning or rule-based approaches**: '
                 'Depending on the complexity of the problem, you could '
                 'explore using machine learning models or more sophisticated '
                 'rule-based approaches to classify alpha-amino acids.\n'
                 '\n'
                 '5. **Test with a larger dataset**: Evaluate the performance '
                 'of the program on a larger and more diverse dataset of '
                 'alpha-amino acids and non-alpha-amino acids to identify any '
                 'remaining issues or edge cases.\n'
                 '\n'
                 "Here's an example of how you could use a substructure "
                 'matching approach with SMARTS patterns:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 674,
    'num_false_positives': 1121,
    'num_true_negatives': 140313,
    'num_false_negatives': 192,
    'num_negatives': None,
    'precision': 0.3754874651810585,
    'recall': 0.7782909930715936,
    'f1': 0.506576475009395,
    'accuracy': 0.9907730147575544,
    'negative_predictive_value': 0.9986335005871677}