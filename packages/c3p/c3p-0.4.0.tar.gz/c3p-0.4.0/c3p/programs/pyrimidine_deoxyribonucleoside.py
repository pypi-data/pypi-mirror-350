"""
Classifies: CHEBI:68472 pyrimidine deoxyribonucleoside
"""
"""
Classifies: pyrimidine deoxyribonucleoside
"""

from rdkit import Chem

def is_pyrimidine_deoxyribonucleoside(smiles: str):
    """
    Determines if a molecule is a pyrimidine deoxyribonucleoside based on its SMILES string.
    A pyrimidine deoxyribonucleoside consists of a pyrimidine base attached to a deoxyribose sugar via a β-N1-glycosidic bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a pyrimidine deoxyribonucleoside, False otherwise
        str: Reason for classification
    """

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phosphate group (to exclude nucleotides)
    phosphate_pattern = Chem.MolFromSmarts("P(=O)(O)O")
    if phosphate_pattern is None:
        return None, "Invalid phosphate SMARTS pattern"
    if mol.HasSubstructMatch(phosphate_pattern):
        return False, "Molecule is a nucleotide (contains phosphate group)"

    # Find pyrimidine ring
    pyrimidine_pattern = Chem.MolFromSmarts("n1cnccc1")
    if pyrimidine_pattern is None:
        return None, "Invalid pyrimidine SMARTS pattern"
    pyrimidine_matches = mol.GetSubstructMatches(pyrimidine_pattern)
    if not pyrimidine_matches:
        return False, "No pyrimidine base found"

    # Find sugar ring (five-membered ring containing oxygen)
    sugar_pattern = Chem.MolFromSmarts("C1OC(CO)C(O)C1")
    if sugar_pattern is None:
        return None, "Invalid sugar SMARTS pattern"
    sugar_matches = mol.GetSubstructMatches(sugar_pattern)
    if not sugar_matches:
        return False, "No deoxyribose sugar found"

    # Now check for glycosidic bond between N1 of pyrimidine and C1' of sugar
    # For each pyrimidine ring
    for pyrimidine in pyrimidine_matches:
        n1_idx = pyrimidine[0]  # N1 atom index
        n1_atom = mol.GetAtomWithIdx(n1_idx)
        # Check bonds from N1
        for bond in n1_atom.GetBonds():
            neighbor_atom = bond.GetOtherAtom(n1_atom)
            neighbor_idx = neighbor_atom.GetIdx()
            if neighbor_atom.GetAtomicNum() == 6:
                # Check if neighbor atom is part of sugar ring
                for sugar in sugar_matches:
                    if neighbor_idx in sugar:
                        # Found potential glycosidic bond
                        # Now check for deoxyribose (no OH at 2' position)
                        # Identify the carbons in the sugar ring
                        carbon_indices = [idx for idx in sugar if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6]
                        # Check for OH group at 2' position
                        has_2prime_OH = False
                        for c_idx in carbon_indices:
                            c_atom = mol.GetAtomWithIdx(c_idx)
                            # Count how many carbons in ring the carbon atom is connected to
                            ring_carbons = [nbr for nbr in c_atom.GetNeighbors() if nbr.GetIdx() in carbon_indices]
                            if len(ring_carbons) == 2:
                                # This is likely C2' position
                                for neighbor in c_atom.GetNeighbors():
                                    if neighbor.GetAtomicNum() == 8 and neighbor.GetIdx() not in sugar:
                                        # Found OH group at 2' position
                                        has_2prime_OH = True
                        if has_2prime_OH:
                            return False, "Sugar is ribose (has OH at 2' position)"
                        else:
                            return True, "Contains pyrimidine base attached to deoxyribose via N-glycosidic bond"

    return False, "No glycosidic bond between pyrimidine base and sugar found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:68472',
                          'name': 'pyrimidine deoxyribonucleoside',
                          'definition': 'A deoxyribonucleoside containing a '
                                        'pyrimidine base.',
                          'parents': ['CHEBI:23636', 'CHEBI:26440'],
                          'xrefs': ['MetaCyc:Pyrimidine-Deoxyribonucleosides'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Error: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)\n'
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
    'sample_true_negatives': [   {   'smiles': 'CNC(=O)CC[C@H](N)C(O)=O',
                                     'name': 'N(5)-methyl-L-glutamine',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'C[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)C(O)=O',
                                     'name': "L-lactyl-2-diphospho-5'-guanosine",
                                     'reason': 'Molecule is a nucleotide '
                                               '(contains phosphate group)'},
                                 {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])CC[C@]1([H])[C@@]3(C)CCCC(C)(C)[C@]3([H])CC[C@@]21C)C(=C)CCC=C(C)C',
                                     'name': 'dammara-20,24-diene',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'O=C1C2=C(O)C3=C(O)C=CC=C3C(=C2C(C(=O)C)C(C1)(O)C)C=4C=5C(C(O)=C6C4C(C(=O)C)C(O)(C)CC6=O)=C(O)C=CC5',
                                     'name': 'A 39183A',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'C[C@H](O)[C@@H](O)C1=Nc2c(NC1)[nH]c(N)nc2=O',
                                     'name': 'L-threo-7,8-dihydrobiopterin',
                                     'reason': 'No deoxyribose sugar found'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)CC3=CC=C(C=C3)F',
                                     'name': 'N-[(4S,7R,8S)-5-[(4-fluorophenyl)methyl]-8-methoxy-4,7,10-trimethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'C(CCN1CCCCC1)(CCN(C(C)C)C(C)=O)(C(N)=O)C2=C(Cl)C=CC=C2',
                                     'name': 'bidisomide',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'OCCCCCCCCCCC#CC=C',
                                     'name': '13-Tetradece-11-yn-1-ol',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)CC3=CC=C(C=C3)OC',
                                     'name': '(3R,9S,10R)-16-(dimethylamino)-12-[(2S)-1-hydroxypropan-2-yl]-9-[[(4-methoxyphenyl)methyl-methylamino]methyl]-3,10-dimethyl-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-13-one',
                                     'reason': 'No pyrimidine base found'},
                                 {   'smiles': 'O(CCC12CC3CC(C1)CC(C2)C3)C(=O)CC4=CC=C(OCC(O)CNC(C)C)C=C4',
                                     'name': 'Adaprolol',
                                     'reason': 'No pyrimidine base found'}],
    'sample_false_negatives': [   {   'smiles': 'NC1=NC(=O)N(C=C1)[C@@H]1OC(CO)=C[C@H]1O',
                                      'name': "3'-deoxy-3',4'-didehydro-cytidine",
                                      'reason': 'No deoxyribose sugar found'},
                                  {   'smiles': 'C1=C(CCCC(CO)O)C(NC(N1[C@@H]2O[C@H](CO)[C@H](C2)O)=O)=O',
                                      'name': "2'-deoxy-5-(4,5-dihydroxypentyl)uridine",
                                      'reason': 'No glycosidic bond between '
                                                'pyrimidine base and sugar '
                                                'found'},
                                  {   'smiles': 'Nc1ccn([C@H]2CC[C@@H](CO)O2)c(=O)n1',
                                      'name': 'zalcitabine',
                                      'reason': 'No deoxyribose sugar found'},
                                  {   'smiles': 'O1[C@@H](C(N=[N+]=[N-])CC1N2C=C(C(=O)NC2=O)C)COC3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C(O)=O',
                                      'name': "3'-Azido-3'-deoxy-5'-O-beta-D-glucopyranuronosylthymidine",
                                      'reason': 'No deoxyribose sugar found'},
                                  {   'smiles': 'Cc1cn([C@H]2C[C@H](N=[N+]=[N-])[C@@H](CO)O2)c(=O)[nH]c1=O',
                                      'name': 'zidovudine',
                                      'reason': 'No deoxyribose sugar found'},
                                  {   'smiles': 'O1[C@@H](N2C(=O)NC(=O)C=C2)CC[C@H]1CO',
                                      'name': '2,3-dideoxyuridine',
                                      'reason': 'No deoxyribose sugar found'},
                                  {   'smiles': 'O=C1N(C(=O)C=CN1[C@@H]2O[C@H](CO)[C@H](C2)O)C(=O)C',
                                      'name': '3-acetyl-2′-deoxyuridine',
                                      'reason': 'No glycosidic bond between '
                                                'pyrimidine base and sugar '
                                                'found'},
                                  {   'smiles': 'S(N1C(=O)N(C=C(C1=O)C)[C@@H]2O[C@H](CO)[C@H](C2)O)NC(=O)O',
                                      'name': 'Thymidine-3-mercaptocarbamic '
                                              'acid',
                                      'reason': 'No glycosidic bond between '
                                                'pyrimidine base and sugar '
                                                'found'},
                                  {   'smiles': 'O1[C@@H](N2C(O)C(O)(C(=O)NC2=O)C)C[C@H](O)[C@H]1CO',
                                      'name': 'Thymidine glycol',
                                      'reason': 'No pyrimidine base found'},
                                  {   'smiles': '[C@@H]1(N2C(NC(=O)C(C2)C)=O)O[C@H](CO)[C@H](C1)O',
                                      'name': '5,6-dihydrothymidine',
                                      'reason': 'No pyrimidine base found'}],
    'attempt': 1,
    'reasoning': 'The error in the previous code indicates that some of the '
                 'SMARTS patterns used were invalid, causing '
                 '`Chem.MolFromSmarts()` to return `None`. Specifically, the '
                 'SMARTS patterns that included stereochemistry annotations '
                 'may not have been correctly specified, leading to the '
                 '`NoneType` error when calling `mol.HasSubstructMatch()`. \n'
                 '\n'
                 'To fix this, we can:\n'
                 '\n'
                 '- Remove stereochemistry from the SMARTS patterns or ensure '
                 "it's correctly specified.\n"
                 "- Use a more robust approach by analyzing the molecule's "
                 'graph to find the pyrimidine base, the deoxyribose sugar, '
                 'and the glycosidic bond connecting them.\n'
                 '- Handle cases where `Chem.MolFromSmarts()` returns `None` '
                 'by checking if the pattern is `None` before using it.\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 28,
    'num_false_positives': 20,
    'num_true_negatives': 142234,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.5833333333333334,
    'recall': 0.6086956521739131,
    'f1': 0.5957446808510638,
    'accuracy': 0.9997329585382994,
    'negative_predictive_value': 0.9998734639934763}