"""
Classifies: CHEBI:10036 wax ester
"""
"""
Classifies: CHEBI:50447 wax ester
"""
from rdkit import Chem

def is_wax_ester(smiles: str):
    """
    Determines if a molecule is a wax ester based on its SMILES string.
    A wax ester is a fatty acid ester resulting from the condensation of
    the carboxy group of a fatty acid with the alcoholic hydroxy group of
    a fatty alcohol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a wax ester, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define ester functional group pattern: C(=O)O
    ester_pattern = Chem.MolFromSmarts("C(=O)O")
    ester_matches = mol.GetSubstructMatches(ester_pattern)

    if len(ester_matches) == 0:
        return False, "No ester functional group found"
    elif len(ester_matches) > 1:
        return False, f"Multiple ester groups found ({len(ester_matches)}), molecule should have only one ester linkage"

    # Get the atoms involved in the ester group
    ester_atoms = ester_matches[0]
    carbonyl_c_idx = ester_atoms[0]
    carbonyl_o_idx = ester_atoms[1]
    alkoxy_o_idx = ester_atoms[2]

    # Initialize sets for atoms in the acyl and alkoxy chains
    acyl_atoms = set()
    alkoxy_atoms = set()

    # Traverse the acyl chain (excluding ester oxygen)
    def traverse_acyl(atom_idx):
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            n_idx = neighbor.GetIdx()
            bond = mol.GetBondBetweenAtoms(atom_idx, n_idx)
            if n_idx != carbonyl_o_idx and n_idx not in acyl_atoms and bond is not None:
                acyl_atoms.add(n_idx)
                if neighbor.GetAtomicNum() == 6:  # carbon
                    traverse_acyl(n_idx)

    traverse_acyl(carbonyl_c_idx)

    # Traverse the alkoxy chain (excluding carbonyl carbon)
    def traverse_alkoxy(atom_idx):
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            n_idx = neighbor.GetIdx()
            bond = mol.GetBondBetweenAtoms(atom_idx, n_idx)
            if n_idx != carbonyl_c_idx and n_idx not in alkoxy_atoms and bond is not None:
                alkoxy_atoms.add(n_idx)
                if neighbor.GetAtomicNum() == 6:  # carbon
                    traverse_alkoxy(n_idx)

    traverse_alkoxy(alkoxy_o_idx)

    # Count the number of carbons in each chain
    acyl_carbons = [idx for idx in acyl_atoms if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6]
    alkoxy_carbons = [idx for idx in alkoxy_atoms if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6]

    acyl_chain_length = len(acyl_carbons)
    alkoxy_chain_length = len(alkoxy_carbons)

    # Check if both chains are long enough (≥12 carbons)
    if acyl_chain_length < 12:
        return False, f"Acyl chain too short ({acyl_chain_length} carbons), need at least 12"
    if alkoxy_chain_length < 12:
        return False, f"Alkoxy chain too short ({alkoxy_chain_length} carbons), need at least 12"

    # Check for other functional groups
    # Define unwanted functional groups
    unwanted_funcs = {
        'alcohol': '[OX2H]',
        'aldehyde': '[CX3H1](=O)',
        'ketone': '[#6][CX3](=O)[#6]',
        'carboxylic acid': '[CX3](=O)[OX1H1]',
        'amine': '[NX3;H2,H1;!$(NC=O)]',
        'amide': '[NX3][CX3](=O)[#6]',
        'nitrile': '[CX2]#N',
        'nitro': '[NX3](=O)=O',
        'thiol': '[SX2H]',
        'sulfide': '[SX2][#6]',
        'halide': '[F,Cl,Br,I]',
    }

    # Exclude ester group when searching for other functional groups
    ester_atom_indices = set(ester_atoms)

    for name, smarts in unwanted_funcs.items():
        pattern = Chem.MolFromSmarts(smarts)
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            # Check if any of the atoms in the match are not part of the ester group
            if not ester_atom_indices.issuperset(match):
                return False, f"Unwanted functional group ({name}) found"

    # Check for rings
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings, which is not characteristic of wax esters"

    return True, "Molecule is a wax ester with long-chain fatty acid and fatty alcohol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:10036',
                          'name': 'wax ester',
                          'definition': 'A fatty acid ester resulting from the '
                                        'condensation of the carboxy group of '
                                        'a fatty acid with the alcoholic '
                                        'hydroxy group of a fatty alcohol.',
                          'parents': ['CHEBI:35748', 'CHEBI:73702'],
                          'xrefs': [   'KEGG:C01629',
                                       'MetaCyc:Wax-Esters',
                                       'PMID:12831900',
                                       'PMID:17750349',
                                       'PMID:18821728',
                                       'PMID:21247555',
                                       'PMID:21256496',
                                       'PMID:21961954',
                                       'PMID:22058425',
                                       'PMID:22685145',
                                       'PMID:22878160',
                                       'PMID:23087036',
                                       'PMID:23109878',
                                       'PMID:23196873',
                                       'PMID:23272127',
                                       'Wikipedia:Wax_ester'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               "Error: module 'rdkit.Chem.rdMolDescriptors' has no attribute "
               "'CalcNumFunctionalGroups'\n"
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O[C@H]1[C@@H]([C@@H](C(=O)C1)/C=C/[C@H](O)C/C=C\\C/C=C/C/C=C\\CC)CCC(O)=O',
                                     'name': 'ent-11-D4t-NeuroP',
                                     'reason': 'Alkoxy chain too short (0 '
                                               'carbons), need at least 12'},
                                 {   'smiles': 'C1[C@@H]2[C@@H]([C@@H](N2CC3=CC=CC=C3Cl)CO)C4=CC=CC=C4N1S(=O)(=O)C5=CC=C(C=C5)F',
                                     'name': '[(1R,2aS,8bS)-2-[(2-chlorophenyl)methyl]-4-(4-fluorophenyl)sulfonyl-1,2a,3,8b-tetrahydroazeto[2,3-c]quinolin-1-yl]methanol',
                                     'reason': 'No ester functional group '
                                               'found'},
                                 {   'smiles': 'C=CC1C2C[C@]3([C@@]45C(C6=CC=CC=C6N4)[C@@](CN3)(O[C@@](C25C(=O)OC)(O[C@]1(O[C@@H]7[C@H]([C@@H]([C@H]([C@H](CO)O7)O)O)O)[H])[H])[H])[H]',
                                     'name': 'Cymoside',
                                     'reason': 'Alkoxy chain too short (1 '
                                               'carbons), need at least 12'},
                                 {   'smiles': 'CC1(CC2=C(C(NC3=C2C4=CC=CC=C4C=C3)C5=CC(=C(C=C5)OCC(=O)O)OC)C(=O)C1)C',
                                     'name': '2-[4-(2,2-dimethyl-4-oxo-1,3,5,6-tetrahydrobenzo[a]phenanthridin-5-yl)-2-methoxyphenoxy]acetic '
                                             'acid',
                                     'reason': 'Acyl chain too short (2 '
                                               'carbons), need at least 12'},
                                 {   'smiles': 'CC1(C)C2CC(=O)C1(C)CC2O',
                                     'name': '5-hydroxycamphor',
                                     'reason': 'No ester functional group '
                                               'found'},
                                 {   'smiles': 'O1C(C(=O)N2C(CCC2)C(=O)NC(C(CC)C)C(=O)N(C(C(C)C)C(=O)N(C(C(=O)NCCC1=O)C)C)C)CC(O)(C)C',
                                     'name': 'Hydroxydestruxin B',
                                     'reason': 'Acyl chain too short (3 '
                                               'carbons), need at least 12'},
                                 {   'smiles': 'CCC1=NN(C(=O)C2=CC3=C(N21)C=CO3)C(C)C(=O)NC(C)CCC4=CC=CO4',
                                     'name': '2-(1-ethyl-4-oxo-3-furo[3,4]pyrrolo[3,5-c][1,2,4]triazinyl)-N-[4-(2-furanyl)butan-2-yl]propanamide',
                                     'reason': 'No ester functional group '
                                               'found'},
                                 {   'smiles': 'O[C@@H]1C(=C)[C@]2(C(C)(C)[C@H](C1)O)CC=C(CO)CC2',
                                     'name': 'Acaciicolinol D',
                                     'reason': 'No ester functional group '
                                               'found'},
                                 {   'smiles': 'C[N+]1(CCCC(C1)NC(=O)CCCC(O)=O)Cc1ccc(cc1)C(=O)NCCO',
                                     'name': '3-(4-carboxybutanamido)-1-{4-[(2-hydroxyethyl)carbamoyl]benzyl}-1-methylpiperidinium',
                                     'reason': 'Acyl chain too short (5 '
                                               'carbons), need at least 12'},
                                 {   'smiles': 'COC1=CC=CC=C1CNC(=O)C[C@@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NS(=O)(=O)C',
                                     'name': '2-[(1S,3S,4aS,9aR)-1-(hydroxymethyl)-6-(methanesulfonamido)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(2-methoxyphenyl)methyl]acetamide',
                                     'reason': 'No ester functional group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCC(CCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC',
                                      'name': '2-palmitoyloxypalmityl '
                                              'palmitate',
                                      'reason': 'Multiple ester groups found '
                                                '(2), molecule should have '
                                                'only one ester linkage'},
                                  {   'smiles': 'OC(CCCCCCCCOC(=O)CCCCCCCCCCCCCCCCCCCCC)CCCC',
                                      'name': '9-Hydroxytridecyl docosanoate',
                                      'reason': 'Unwanted functional group '
                                                '(alcohol) found'},
                                  {   'smiles': 'CCCCCCCCCCOC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                      'name': 'decyl oleate',
                                      'reason': 'Alkoxy chain too short (10 '
                                                'carbons), need at least 12'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCCCCCCCC',
                                      'name': 'octyl palmitate',
                                      'reason': 'Alkoxy chain too short (8 '
                                                'carbons), need at least 12'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCCCCCCCCC',
                                      'name': 'nonyl palmitate',
                                      'reason': 'Alkoxy chain too short (9 '
                                                'carbons), need at least 12'}],
    'attempt': 1,
    'reasoning': 'In the previous code, the function `is_wax_ester` attempted '
                 'to classify wax esters by checking for the presence of '
                 'exactly one ester functional group, verifying that both '
                 'chains attached to the ester are long (at least 12 carbons), '
                 'and ensuring there are no additional functional groups or '
                 'rings. However, the code used '
                 '`rdMolDescriptors.CalcNumFunctionalGroups(mol)`, which '
                 'raised an error because this function does not exist in '
                 '`rdkit.Chem.rdMolDescriptors`. As a result, the code failed '
                 'to run, leading to an F1 score of 0.\n'
                 '\n'
                 'To fix this issue, we need to find an alternative method to '
                 'check for additional functional groups. One approach is to '
                 'define SMARTS patterns for common functional groups that '
                 'should not be present in wax esters (e.g., alcohols, amines, '
                 'ketones, aldehydes, carboxylic acids, amides, nitriles, '
                 'etc.) and check if the molecule contains any of these '
                 'groups.\n'
                 '\n'
                 'Additionally, we should ensure that the code correctly '
                 'identifies the length of the alkyl chains attached to the '
                 'ester group, even in the presence of unsaturation (double '
                 'bonds), and that it accounts for any possible chain '
                 'branching (although wax esters are typically unbranched).\n'
                 '\n'
                 'Therefore, we can improve the code by:\n'
                 '\n'
                 '- Replacing the non-existent function with a set of SMARTS '
                 'patterns to detect unwanted functional groups.\n'
                 '- Carefully extracting the alkyl chains attached to the '
                 'ester group, including unsaturated chains.\n'
                 '- Ensuring the code is robust and handles possible '
                 'exceptions.\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 90,
    'num_false_positives': 6,
    'num_true_negatives': 142199,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.9375,
    'recall': 0.9473684210526315,
    'f1': 0.9424083769633508,
    'accuracy': 0.9999226985242445,
    'negative_predictive_value': 0.9999648392450282}