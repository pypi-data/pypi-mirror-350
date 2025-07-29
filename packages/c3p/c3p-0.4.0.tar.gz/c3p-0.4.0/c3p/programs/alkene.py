"""
Classifies: CHEBI:32878 alkene
"""
"""
Classifies: CHEBI:32878 alkene
"""
from rdkit import Chem

def is_alkene(smiles: str):
    """
    Determines if a molecule is an alkene based on its SMILES string.
    An alkene is an acyclic hydrocarbon with exactly one carbon-carbon double bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkene, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for hydrocarbon (only C and H atoms)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in {1, 6}:
            return False, "Contains non-carbon/hydrogen atoms"

    # Count double bonds and check for triple bonds
    double_bonds = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            double_bonds += 1
        elif bond.GetBondType() == Chem.BondType.TRIPLE:
            return False, "Contains triple bonds"

    if double_bonds != 1:
        return False, f"Found {double_bonds} double bonds, need exactly 1"

    # Check for acyclic structure (no rings)
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings"

    return True, "Acyclic hydrocarbon with exactly one carbon-carbon double bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32878',
                          'name': 'alkene',
                          'definition': 'An acyclic branched or unbranched '
                                        'hydrocarbon having one carbon-carbon '
                                        'double bond and the general formula '
                                        'CnH2n. Acyclic branched or unbranched '
                                        'hydrocarbons having more than one '
                                        'double bond are alkadienes, '
                                        'alkatrienes, etc.',
                          'parents': ['CHEBI:33645'],
                          'xrefs': ['KEGG:C01372'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 30,
                           'log_lines_of_code': 3.4011973816621555,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'NumRings',
                                                 'MolFromSmiles',
                                                 'GetAtoms',
                                                 'GetBonds',
                                                 'GetAtomicNum',
                                                 'GetRingInfo'],
                           'methods_called_count': 7,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_alkene(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains '
                                          'non-carbon/hydrogen atoms"',
                                          'False, "Contains triple bonds"',
                                          'False, f"Found {double_bonds} '
                                          'double bonds, need exactly 1"',
                                          'False, "Molecule contains rings"',
                                          'True, "Acyclic hydrocarbon with '
                                          'exactly one carbon-carbon double '
                                          'bond"'],
                           'returns_count': 6,
                           'complexity': 4.080239476332431},
    'message': '\n'
               'Error: unexpected indent (<string>, line 1)\n'
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
    'sample_true_negatives': [   {   'smiles': 'O1[C@@]2([C@@H]([C@H]([C@@](C2)(C1)[H])/C=C/[C@@H](O)CCCCC)C/C=C\\CCCC(O)=O)[H]',
                                     'name': 'U-44069',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'CO[C@@H]1[C@H](O)[C@@H](CO)O[C@H]1n1cc(C)c(=O)[nH]c1=O',
                                     'name': "2'-O-methyl-5-methyluridine",
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'O(C1O[C@@H]([C@@H](O)[C@H](O)[C@H]1NC(=O)C)CO)[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2O)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-2-[(2S,3S,4S,5S,6R)-2,4,5-trihydroxy-6-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]acetamide',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'O[C@@H](C1=CC(=CC=C1)C=C)CO',
                                     'name': '(1S)-(3-Ethenylphenyl)-1,2-ethanediol',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'ClCCCCCCCC/C=C/CC(=O)O[C@H](C(=O)OCCC(=O)N1O[C@@H](CC(=N1)CCCCC)CCCCC)C',
                                     'name': 'Nocuolactylate A',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCOC[C@@H](O)CO',
                                     'name': '1-O-octadecyl-sn-glycerol',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O[C@@H]%19O[C@@H]([C@@H](O[C@@H]%20O[C@@H]([C@H](O)[C@H](O[C@]%21(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%21)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%20O)CO)[C@H](O)[C@H]%19NC(=O)C)CO)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO',
                                     'name': 'CID 146015963',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'O1OC(CC1C(OO)/C=C/C(OO)CCCCC)/C=C/C=C/CCCC(OC)=O',
                                     'name': 'Methyl '
                                             '9,11-epidioxy-12,15-dihydroperoxy-5,7,13-eicosatrienoate',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCCSC',
                                     'name': 'glucoerucin',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'},
                                 {   'smiles': 'O1C(=O)C([C@H](CC(=O)C)C2=CC=CC=C2)=C(O)C3=C1C(O)=CC=C3',
                                     'name': 'R-8-Hydroxywarfarin',
                                     'reason': 'Contains non-carbon/hydrogen '
                                               'atoms'}],
    'sample_false_negatives': [   {   'smiles': 'C(CCCC(CCCC(C=C)=C)C)(CCCC(C)C)C',
                                      'name': 'neophytadiene',
                                      'reason': 'Found 2 double bonds, need '
                                                'exactly 1'},
                                  {   'smiles': 'C=CCCCCCCC1OC1',
                                      'name': '1,2-epoxy-9-decene',
                                      'reason': 'Contains non-carbon/hydrogen '
                                                'atoms'}],
    'attempt': 1,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's try to figure out why the previous code didn't "
                 'work. The user mentioned an "unexpected indent" error, which '
                 "usually means there's a problem with the code's formatting. "
                 'Looking at the previous code, I notice that the examples '
                 "list is written as part of the code block, which isn't valid "
                 'Python. The user probably included the examples in the code '
                 'by mistake, causing syntax errors.\n'
                 '\n'
                 'Now, focusing on the actual task: create a function '
                 '`is_alkene` that checks if a SMILES string represents an '
                 'alkene. The definition says alkenes have exactly one '
                 'carbon-carbon double bond, are acyclic, and are hydrocarbons '
                 '(only C and H).\n'
                 '\n'
                 'First, I need to parse the SMILES into a molecule. Then, '
                 'check for exactly one double bond. Also, ensure there are no '
                 'rings (acyclic) and no heteroatoms.\n'
                 '\n'
                 'Steps:\n'
                 '1. Parse the SMILES. If invalid, return False.\n'
                 '2. Check that all atoms are C or H.\n'
                 '3. Count the number of double bonds. Must be exactly one.\n'
                 '4. Ensure the molecule is acyclic (no rings).\n'
                 '5. Exclude molecules with more than one double bond or any '
                 'triple bonds.\n'
                 '\n'
                 'Wait, but the problem statement says "acyclic branched or '
                 'unbranched hydrocarbon having one carbon-carbon double '
                 'bond". So the molecule must be acyclic, only C and H, '
                 'exactly one double bond (not triple), and no rings.\n'
                 '\n'
                 'So in code:\n'
                 '- Use RDKit to get the molecule.\n'
                 '- Check for Hydrocarbon: all atoms are C or H.\n'
                 "- Count double bonds: use GetSubstructMatches for 'C=C' "
                 'pattern, but need to count actual double bonds in the '
                 'molecule.\n'
                 "- Check for rings: if the molecule has any rings, it's not "
                 'an alkene.\n'
                 '- Also, ensure there are no triple bonds.\n'
                 '\n'
                 'Let me think about possible edge cases. For example, allenes '
                 '(consecutive double bonds like C=C=C) should be excluded. '
                 'The function should only allow one double bond.\n'
                 '\n'
                 'So, the plan is:\n'
                 '1. Parse SMILES.\n'
                 '2. Check for valid molecule.\n'
                 '3. Check all atoms are C or H.\n'
                 "4. Check that there's exactly one double bond (and no triple "
                 'bonds).\n'
                 '5. Check the molecule is acyclic (no rings).\n'
                 '\n'
                 'Implementing this in RDKit:\n'
                 '\n'
                 '- To count double bonds: iterate through all bonds and count '
                 'those with bond type DOUBLE.\n'
                 '- Check that the count is exactly 1.\n'
                 '- Check that there are no rings using '
                 'Mol.GetRingInfo().NumRings() > 0.\n'
                 "- Check all atoms' atomic numbers are 6 (C) or 1 (H).\n"
                 '\n'
                 'Putting this together into the function.\n'
                 '\n'
                 'Testing examples: ethene (C=C) should return True. '
                 '1,3-butadiene (C=CC=C) has two double bonds, should return '
                 'False. Cyclohexene (with a ring) should return False. Any '
                 'molecule with O or N should be rejected.\n'
                 '\n'
                 "Potential issues: stereochemistry (like cis/trans) shouldn't "
                 'matter. Also, branched structures are allowed as long as '
                 'they meet the criteria.\n'
                 '\n'
                 'So the code should:\n'
                 '\n'
                 '- Use Chem.MolFromSmiles to parse.\n'
                 '- Check for validity.\n'
                 "- Check each atom's atomic number.\n"
                 '- Count double bonds.\n'
                 '- Check rings.\n'
                 '- Return True only if all conditions are met.\n'
                 '\n'
                 'Now, writing the code with these steps.\n'
                 '\n'
                 '</reasoning>',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 57,
    'num_false_positives': 39,
    'num_true_negatives': 142202,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.59375,
    'recall': 0.9661016949152542,
    'f1': 0.7354838709677419,
    'accuracy': 0.9997118763176388,
    'negative_predictive_value': 0.9999859356980113}