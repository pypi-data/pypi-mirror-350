"""
Classifies: CHEBI:61910 very long-chain fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_very_long_chain_fatty_acyl_CoA(smiles: str) -> tuple[bool, str]:
    """
    Determines if a molecule is a very long-chain fatty acyl-CoA based on its SMILES string.
    Very long-chain fatty acyl-CoAs have fatty acid chains longer than C22.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        tuple[bool, str]: (is_vlcfa_coa, reason)
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for CoA moiety
    # Look for adenine
    adenine_pattern = Chem.MolFromSmarts("c1nc(N)c2ncnc2n1")
    if not mol.HasSubstructMatch(adenine_pattern):
        return False, "No CoA moiety found (missing adenine)"
    
    # Look for thioester group (C(=O)S)
    thioester_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[SX2]")
    if not mol.HasSubstructMatch(thioester_pattern):
        return False, "No thioester group found"

    # Look for phosphate groups (need at least 3 for CoA)
    phosphate_pattern = Chem.MolFromSmarts("[OX2]P(=O)([OX2])[OX2]")
    if len(mol.GetSubstructMatches(phosphate_pattern)) < 3:
        return False, "Missing phosphate groups characteristic of CoA"

    # Count carbons in the main chain
    # First get the carbon atoms in the thioester group
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    thioester_carbon = thioester_matches[0][0]  # First carbon of the thioester group
    
    # Get all carbon atoms
    carbon_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    
    # Find the longest carbon chain starting from the thioester carbon
    visited = set()
    def dfs_carbon_chain(atom_idx, depth=0):
        if atom_idx not in carbon_atoms or atom_idx in visited:
            return depth
        visited.add(atom_idx)
        max_depth = depth
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 6:  # Only follow carbon atoms
                max_depth = max(max_depth, dfs_carbon_chain(neighbor.GetIdx(), depth + 1))
        return max_depth

    # Get chain length starting from thioester carbon
    chain_length = dfs_carbon_chain(thioester_carbon)
    
    if chain_length <= 22:
        return False, f"Fatty acid chain length (C{chain_length}) not greater than C22"
    
    if chain_length > 40:
        return False, f"Fatty acid chain length (C{chain_length}) unreasonably long"

    # Check for characteristic functional groups that may be present
    modifications = []
    
    # Check for double bonds
    double_bond_pattern = Chem.MolFromSmarts("CC=CC")
    if mol.HasSubstructMatch(double_bond_pattern):
        modifications.append("unsaturated")
    
    # Check for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts("CC(O)C")
    if mol.HasSubstructMatch(hydroxyl_pattern):
        modifications.append("hydroxylated")
    
    # Check for oxo groups
    oxo_pattern = Chem.MolFromSmarts("CC(=O)C")
    if mol.HasSubstructMatch(oxo_pattern):
        modifications.append("oxo")

    modification_str = " and ".join(modifications)
    if modification_str:
        modification_str = f" ({modification_str})"
    
    return True, f"Very long-chain fatty acyl-CoA with C{chain_length} fatty acid chain{modification_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61910',
                          'name': 'very long-chain fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA in which the fatty '
                                        'acyl group has a chain length greater '
                                        'than C22.',
                          'parents': ['CHEBI:37554'],
                          'xrefs': [   'PMID:16768463',
                                       'PMID:20360933',
                                       'PMID:20530735',
                                       'PMID:20798351'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               "Error: 'Mol' object has no attribute 'HasSubstructMatches'\n"
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
    'sample_true_negatives': [   {   'smiles': 'C1C=C(N=C2N1NN=N2)C3=CC=CC=C3',
                                     'name': '5-phenyl-1,7-dihydrotetrazolo[1,5-a]pyrimidine',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                     'name': 'TG(14:1(9Z)/22:1(13Z)/18:1(11Z))',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1O',
                                     'name': 'beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-D-Manp-(1->3)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-GlcpNAc-(1->4)-beta-D-GlcpNAc',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': '[C@@]12([C@@]([C@]([C@@H](CC1)C)(CCC(CC)C)C)(CCC[C@@H]2C)[H])C',
                                     'name': 'clerodane',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4R,5R,6R)-3,4-dihydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'O=C(NC(CC(C)C)C(=O)N[C@@H](CCCN=C(N)N)C=O)C(NC(=O)CC)CC(C)C',
                                     'name': 'Leupeptin Pr-LL',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'COC1=CC=C(C=C1)CCNC(=O)C(=C2C3=CC=CC=C3C(=N2)NC(=O)C4=CC=CS4)C#N',
                                     'name': 'N-[3-[1-cyano-2-[2-(4-methoxyphenyl)ethylamino]-2-oxoethylidene]-1-isoindolyl]-2-thiophenecarboxamide',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'O=C1O[C@@H](CC=2C1=C(OC)C(O)=CC2)CCC[C@@H](O)C',
                                     'name': 'Penicimarin C',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'},
                                 {   'smiles': 'CO[C@@H]1[C@@H]2[C@@H](C[C@@H]3[C@@](O2)([C@H]([C@@H]([C@H](O3)C(=O)OC)O)O)O)OC1N4C=NC5=C4N=CN=C5N',
                                     'name': 'LSM-4497',
                                     'reason': 'No thioester group found'},
                                 {   'smiles': 'C[C@@H]1[C@H](O)CCC2=CC[C@H](C[C@]12C)C(C)=C',
                                     'name': '1-deoxycapsidiol',
                                     'reason': 'No CoA moiety found (missing '
                                               'adenine)'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(10Z,13Z,16Z)-3-oxodocosatrienoyl-CoA',
                                      'reason': 'Fatty acid chain length (C22) '
                                                'not greater than C22'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCCCCCCCCCCCCCCCCCCCC)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': 'docosanoyl-CoA',
                                      'reason': 'Fatty acid chain length (C22) '
                                                'not greater than C22'}],
    'attempt': 1,
    'reasoning': 'Let me analyze what went wrong and propose improvements:\n'
                 '\n'
                 '1. The main error was using `HasSubstructMatches` instead of '
                 '`HasSubstructMatch` - this was a simple syntax error as the '
                 'RDKit method is named `HasSubstructMatch`.\n'
                 '\n'
                 '2. The approach of checking for CoA moiety, thioester group, '
                 'and fatty acid chain length is correct, but we should make '
                 'the code more robust.\n'
                 '\n'
                 '3. The example structures show that we need to handle:\n'
                 '   - Saturated and unsaturated chains\n'
                 '   - Chains with hydroxyl groups\n'
                 '   - Chains with oxo groups\n'
                 '   - Various chain lengths from C24 to C38\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 104,
    'num_false_positives': 33,
    'num_true_negatives': 142161,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.7591240875912408,
    'recall': 0.9811320754716981,
    'f1': 0.8559670781893004,
    'accuracy': 0.9997540407589599,
    'negative_predictive_value': 0.9999859316418478}