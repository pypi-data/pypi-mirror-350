"""
Classifies: CHEBI:51006 unsaturated fatty acyl-CoA
"""
"""
Classifies: unsaturated fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_unsaturated_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is an unsaturated fatty acyl-CoA based on its SMILES string.
    An unsaturated fatty acyl-CoA is a molecule containing a coenzyme A moiety linked to an
    unsaturated fatty acid via a thioester bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an unsaturated fatty acyl-CoA, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for charges
    if any(atom.GetFormalCharge() != 0 for atom in mol.GetAtoms()):
        return False, "Molecule contains charges"
    
    # Define the CoA substructure using SMARTS
    coa_pattern = Chem.MolFromSmarts("SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(=O)(O)O)n1cnc2c(N)ncnc12")
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "No CoA moiety found"

    # Check for the thioester bond (-C(=O)-S-)
    thioester_pattern = Chem.MolFromSmarts("C(=O)SC")
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if len(thioester_matches) != 1:
        return False, f"Found {len(thioester_matches)} thioester groups, need exactly 1"

    # Find the carbon atom of the carbonyl group in thioester
    thioester_c_index = thioester_matches[0][0]
    
    # Find the fatty acid chain connected to the thioester
    fatty_acid_atoms = set()
    queue = [thioester_c_index]
    visited = {thioester_c_index}

    while queue:
        current_idx = queue.pop(0)
        current_atom = mol.GetAtomWithIdx(current_idx) # get atom object
        for neighbor in current_atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if neighbor_idx not in visited:
                if neighbor.GetSymbol() == 'C':
                    fatty_acid_atoms.add(neighbor_idx)
                    queue.append(neighbor_idx)
                visited.add(neighbor_idx)
            
    # Check for at least one double bond (C=C) in the acyl chain (exclude double bonds in the CoA)
    double_bond_pattern = Chem.MolFromSmarts("[CH]=[CH]")
    double_bond_matches = mol.GetSubstructMatches(double_bond_pattern)
    acyl_double_bonds = 0

    for match in double_bond_matches:
        atom1_idx = mol.GetAtomWithIdx(match[0]).GetIdx()
        atom2_idx = mol.GetAtomWithIdx(match[1]).GetIdx()
        if atom1_idx in fatty_acid_atoms and atom2_idx in fatty_acid_atoms:
            acyl_double_bonds += 1

    if acyl_double_bonds < 1:
      return False, "No double bond found in the fatty acid chain"
    
    # Check the number of carbons in the fatty acid chain.
    chain_carbon_count = len(fatty_acid_atoms)
    if chain_carbon_count < 4 :
      return False, f"Fatty acid chain too short, found {chain_carbon_count} carbons"
      
    # Check molecular weight - Acyl-CoAs typically > 600 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 600:
        return False, "Molecular weight too low for unsaturated fatty acyl-CoA"

    return True, "Contains CoA moiety linked to an unsaturated fatty acid via a thioester bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:51006',
                          'name': 'unsaturated fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA that results from '
                                        'the formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any unsaturated fatty acid.',
                          'parents': ['CHEBI:37554'],
                          'xrefs': ['PMID:13152086'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 62,
                           'log_lines_of_code': 4.127134385045092,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 4,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'add',
                                                 'GetSubstructMatches',
                                                 'GetNeighbors',
                                                 'MolFromSmarts',
                                                 'pop',
                                                 'GetAtoms',
                                                 'CalcExactMolWt',
                                                 'GetFormalCharge',
                                                 'HasSubstructMatch',
                                                 'append',
                                                 'GetSymbol',
                                                 'MolFromSmiles',
                                                 'GetIdx',
                                                 'GetAtomWithIdx'],
                           'methods_called_count': 14,
                           'smarts_strings': [   'C(=O)SC',
                                                 '[CH]=[CH]',
                                                 'SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(=O)(O)O)n1cnc2c(N)ncnc12'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_unsaturated_fatty_acyl_CoA(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains charges"',
                                          'False, "No CoA moiety found"',
                                          'False, f"Found '
                                          '{len(thioester_matches)} thioester '
                                          'groups, need exactly 1"',
                                          'False, "No double bond found in the '
                                          'fatty acid chain"',
                                          'False, f"Fatty acid chain too '
                                          'short, found {chain_carbon_count} '
                                          'carbons"',
                                          'False, "Molecular weight too low '
                                          'for unsaturated fatty acyl-CoA"',
                                          'True, "Contains CoA moiety linked '
                                          'to an unsaturated fatty acid via a '
                                          'thioester bond"'],
                           'returns_count': 8,
                           'complexity': 6.425426877009019},
    'message': '\n'
               'Error: Error executing '
               "is_unsaturated_fatty_acyl_CoA('C[C@H](C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C'):\n"
               " 'Mol' object has no attribute 'GetAtom'\n"
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
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No CoA moiety found'}],
    'sample_false_negatives': [   {   'smiles': 'CC=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': 'but-2-enoyl-CoA',
                                      'reason': 'Fatty acid chain too short, '
                                                'found 3 carbons'},
                                  {   'smiles': 'CCCCCCCCCCCCC=C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '2-methylpentadec-2-enoyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'CC(=C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '3-methylbut-3-enoyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(=CCCC)C)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '2-methylhexenoyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC=C',
                                      'name': 'vinylacetyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'C\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N',
                                      'name': 'trans-3-methylglutaconyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'CC(=O)CC[C@H](CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(C)=C',
                                      'name': '(3R)-3-isopropenyl-6-oxoheptanoyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'CC(C)=CCC\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '3-(4-methylpent-3-en-1-yl)pent-2-enedioyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'CC(C)CCCC(C)CCCC(C)CC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(E)-2,3-didehydropristanoyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'},
                                  {   'smiles': 'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCCCC=C',
                                      'name': '9-decenoyl-CoA',
                                      'reason': 'No double bond found in the '
                                                'fatty acid chain'}],
    'attempt': 3,
    'reasoning': "Okay, let's analyze the previous attempt and the provided "
                 'outcomes.\n'
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 'The previous code attempted to identify unsaturated fatty '
                 'acyl-CoAs by looking for the CoA moiety, a thioester bond, '
                 'and an unsaturated fatty acid chain. The error message " '
                 '\'Mol\' object has no attribute \'GetAtom\' " indicates that '
                 'the code was trying to use `mol.GetAtom(index)` on an object '
                 'where that method does not exist, which is likely happening '
                 'because we are iterating through a `match` that is not an '
                 'atom index, but a tuple of atom indexes. Specifically this '
                 'is happening in the code where I was trying to find the '
                 'fatty acid chain connected to the thioester by doing '
                 '`mol.GetAtom(current).GetNeighbors()`. This means that the '
                 '`current` variable is not a single atom index, as I assumed, '
                 'and is likely a tuple with the atom indexes of a '
                 'substructure match.\n'
                 '\n'
                 'The overall strategy of finding the CoA moiety, thioester '
                 'bond, and unsaturated fatty acid is sound. The issue is that '
                 'the implementation details related to tracing the carbon '
                 'chain and checking for double bonds had some bugs. \n'
                 'Specifically:\n'
                 '- It seems we are getting an error when we try to do '
                 '`mol.GetAtom(current)` because `current` is an index *within '
                 'the match*, and not an index of the atom in the whole '
                 'molecule.\n'
                 '- The "fatty acid pattern" is too restrictive. It requires '
                 "specific numbers of methyl groups which isn't general for "
                 "fatty acid chains. Also, it's not used correctly to extract "
                 'the fatty acid chain. The chain extraction logic was '
                 'flawed.\n'
                 '- The double bond check also needs to be done carefully. We '
                 'should iterate through the double bond matches to determine '
                 'whether it belongs to the fatty acid part.\n'
                 '\n'
                 "Here's how we can improve:\n"
                 '\n'
                 '1.  **Correct Fatty Acid Chain Traversal:** Instead of '
                 'assuming that `GetSubstructMatches` returns indices in `mol` '
                 'we should iterate the matches and get the corresponding '
                 '`Atom` objects, and get their index `GetIdx()`\n'
                 '2.  **General Fatty Acid Chain SMARTS:** Use a more general '
                 'SMARTS pattern for the fatty acid chain, such as a series of '
                 'connected carbon atoms (`[CX4][CX4]...`).\n'
                 '3.  **Double Bond Check:** Implement the double bond check '
                 'in the fatty acid chain correctly by getting the index and '
                 'checking if it belongs to our set of fatty acid atoms.\n'
                 '4.  **Correct charge checking** - Make sure that we are '
                 'checking the formal charge, and not something else.\n'
                 '\n'
                 '**New Code:**',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 246,
    'num_false_positives': 80,
    'num_true_negatives': 141962,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.754601226993865,
    'recall': 0.9534883720930233,
    'f1': 0.8424657534246576,
    'accuracy': 0.999353478566409,
    'negative_predictive_value': 0.9999154774817924}