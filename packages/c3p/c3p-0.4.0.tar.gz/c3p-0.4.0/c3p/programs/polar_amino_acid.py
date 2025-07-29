"""
Classifies: CHEBI:26167 polar amino acid
"""
"""
Classifies: Polar amino acids (CHEBI: ???)
"""
from rdkit import Chem
from rdkit.Chem import MolFromSmiles, MolFromSmarts

def is_polar_amino_acid(smiles: str):
    """
    Determines if a molecule is a polar amino acid based on its SMILES string.
    Polar amino acids have side chains capable of forming hydrogen bonds.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polar amino acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES"
    
    # Amino acid pattern: amino group (NH2/NH3+) connected to alpha carbon with carboxyl group
    amino_acid_pattern = MolFromSmarts("[NX3;H2,H3+]-[CX4H]([CX3](=[OX1])[OX2H1,O-])-[!H0]")
    if not mol.HasSubstructMatch(amino_acid_pattern):
        return False, "Not an amino acid"
    
    # Find alpha carbon (second atom in the match)
    matches = mol.GetSubstructMatches(amino_acid_pattern)
    if not matches:
        return False, "No alpha carbon found"
    alpha_carbon_idx = matches[0][1]
    alpha_carbon = mol.GetAtomWithIdx(alpha_carbon_idx)
    
    # Identify side chain starting atom (non-amino, non-carboxyl substituent)
    side_chain_start = None
    for neighbor in alpha_carbon.GetNeighbors():
        # Check if neighbor is part of amino group
        if neighbor.GetAtomicNum() == 7 and neighbor.GetTotalNumHs() >= 2:
            continue
        # Check if neighbor is part of carboxyl group
        if neighbor.GetAtomicNum() == 6:
            carboxyl_oxygen = any(a.GetAtomicNum() == 8 and a.GetTotalNumHs() >=1 
                                 for a in neighbor.GetNeighbors())
            if carboxyl_oxygen:
                continue
        side_chain_start = neighbor
        break
    
    if not side_chain_start:
        return False, "No side chain found"
    
    # Collect all side chain atoms (excluding alpha carbon)
    side_chain_atoms = set()
    stack = [side_chain_start]
    while stack:
        atom = stack.pop()
        if atom.GetIdx() == alpha_carbon_idx or atom.GetIdx() in side_chain_atoms:
            continue
        side_chain_atoms.add(atom.GetIdx())
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() not in side_chain_atoms and nbr.GetIdx() != alpha_carbon_idx:
                stack.append(nbr)
    
    # Check for polar groups in side chain atoms
    polar_patterns = {
        "hydroxyl": MolFromSmarts("[OX2H]"),
        "thiol": MolFromSmarts("[SX2H]"),
        "amide": MolFromSmarts("[CX3](=O)[NX3H2]"),
        "guanidine": MolFromSmarts("[NH]C(=N)N"),
        "imidazole": MolFromSmarts("[nH]1cccn1"),
        "carboxyl": MolFromSmarts("[CX3](=O)[OX2H1,O-]"),
        "amino": MolFromSmarts("[NX3H2]"),
        "ether_oxygen": MolFromSmarts("[OX2H0][#6]"),
        "aromatic_nitrogen": MolFromSmarts("[nH]"),
    }
    
    for group_name, pattern in polar_patterns.items():
        if pattern is None:
            continue
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            if any(idx in side_chain_atoms for idx in match):
                return True, f"Side chain contains {group_name} group"
    
    # Special case: aromatic rings with polar substituents (e.g., tyrosine)
    for atom_idx in side_chain_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetIsAromatic():
            for nbr in atom.GetNeighbors():
                if nbr.GetAtomicNum() == 8 and nbr.GetTotalNumHs() == 1:
                    return True, "Aromatic ring with hydroxyl group"
    
    return False, "No polar groups in side chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26167',
                          'name': 'polar amino acid',
                          'definition': 'Any amino acid whose side chain is '
                                        'capable of forming one or more '
                                        'hydrogen bonds.',
                          'parents': ['CHEBI:33709'],
                          'xrefs': [   'MetaCyc:Polar-amino-acids',
                                       'PMID:12016058'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 77,
                           'log_lines_of_code': 4.343805421853684,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'MolFromSmiles, MolFromSmarts'],
                           'imports_count': 2,
                           'methods_called': [   'GetNeighbors',
                                                 'GetIsAromatic',
                                                 'append',
                                                 'add',
                                                 'GetAtomWithIdx',
                                                 'GetTotalNumHs',
                                                 'items',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'GetIdx',
                                                 'HasSubstructMatch',
                                                 'pop'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_polar_amino_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES"',
                                          'False, "Not an amino acid"',
                                          'False, "No alpha carbon found"',
                                          'False, "No side chain found"',
                                          'True, f"Side chain contains '
                                          '{group_name} group"',
                                          'True, "Aromatic ring with hydroxyl '
                                          'group"',
                                          'False, "No polar groups in side '
                                          'chain"'],
                           'returns_count': 7,
                           'complexity': 5.868761084370737},
    'message': '\n'
               'Error: Error executing '
               "is_polar_amino_acid('OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H]'):\n"
               ' Python argument types in\n'
               '    rdkit.Chem.rdmolops.ReplaceSidechains(Mol, list)\n'
               'did not match C++ signature:\n'
               '    ReplaceSidechains(RDKit::ROMol mol, RDKit::ROMol '
               'coreQuery, bool useChirality=False)\n'
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
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'CO[C@@H]1[C@H](O)[C@@H](CO)O[C@H]1n1cc(C)c(=O)[nH]c1=O',
                                     'name': "2'-O-methyl-5-methyluridine",
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'O(C1O[C@@H]([C@@H](O)[C@H](O)[C@H]1NC(=O)C)CO)[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2O)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-2-[(2S,3S,4S,5S,6R)-2,4,5-trihydroxy-6-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]acetamide',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'O[C@@H](C1=CC(=CC=C1)C=C)CO',
                                     'name': '(1S)-(3-Ethenylphenyl)-1,2-ethanediol',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'ClCCCCCCCC/C=C/CC(=O)O[C@H](C(=O)OCCC(=O)N1O[C@@H](CC(=N1)CCCCC)CCCCC)C',
                                     'name': 'Nocuolactylate A',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCOC[C@@H](O)CO',
                                     'name': '1-O-octadecyl-sn-glycerol',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O[C@@H]%19O[C@@H]([C@@H](O[C@@H]%20O[C@@H]([C@H](O)[C@H](O[C@]%21(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%21)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%20O)CO)[C@H](O)[C@H]%19NC(=O)C)CO)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO',
                                     'name': 'CID 146015963',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'O1OC(CC1C(OO)/C=C/C(OO)CCCCC)/C=C/C=C/CCCC(OC)=O',
                                     'name': 'Methyl '
                                             '9,11-epidioxy-12,15-dihydroperoxy-5,7,13-eicosatrienoate',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCCSC',
                                     'name': 'glucoerucin',
                                     'reason': 'Not an amino acid'},
                                 {   'smiles': 'O1C(=O)C([C@H](CC(=O)C)C2=CC=CC=C2)=C(O)C3=C1C(O)=CC=C3',
                                     'name': 'R-8-Hydroxywarfarin',
                                     'reason': 'Not an amino acid'}],
    'sample_false_negatives': [   {   'smiles': 'N[C@H](CO)C(O)=O',
                                      'name': 'D-serine',
                                      'reason': 'No side chain found'},
                                  {   'smiles': 'NC(CO)C(O)=O',
                                      'name': 'serine',
                                      'reason': 'No side chain found'},
                                  {   'smiles': 'N[C@@H](CO)C(O)=O',
                                      'name': 'L-serine',
                                      'reason': 'No side chain found'},
                                  {   'smiles': 'C[C@H](O)[C@@H](N)C(O)=O',
                                      'name': 'D-threonine',
                                      'reason': 'No side chain found'},
                                  {   'smiles': 'C[C@@H](O)[C@H](N)C(O)=O',
                                      'name': 'L-threonine',
                                      'reason': 'No side chain found'},
                                  {   'smiles': 'O=C([O-])[C@@H]([NH3+])[C@@H](CCNC(=[NH2+])N)C',
                                      'name': '(3R)-3-methyl-L-arginine '
                                              'zwitterion',
                                      'reason': 'Not an amino acid'}],
    'attempt': 3,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's see why the previous code didn't work. The error "
                 "message says there's a problem with ReplaceSidechains, and "
                 'the F1 score was zero. Hmm.\n'
                 '\n'
                 'Looking at the error: the user tried to call '
                 'ReplaceSidechains with (mol, list), but the C++ signature '
                 "expects a coreQuery. Oh right, ReplaceSidechains isn't used "
                 'like that. The previous code tried to use it to extract the '
                 "side chain by passing a list of tuples, but that's not how "
                 'the function works. ReplaceSidechains actually requires a '
                 "core structure, and it replaces the parts that aren't part "
                 'of the core. So that approach was wrong.\n'
                 '\n'
                 'So, the main issue is in extracting the side chain. The code '
                 'tried to use ReplaceSidechains incorrectly. Instead, maybe '
                 'we should find the side chain atoms and check for polar '
                 'groups directly without extracting a submol.\n'
                 '\n'
                 'Let me think about how to correctly identify the side chain. '
                 'The amino acid has an alpha carbon connected to an amino '
                 'group, a carboxyl group, a hydrogen, and the side chain. The '
                 'side chain is the fourth substituent. So, for the alpha '
                 'carbon, we can iterate through its neighbors and find which '
                 "one isn't part of the amino or carboxyl groups.\n"
                 '\n'
                 'Once we have the side chain atom (the first atom of the side '
                 'chain), we can traverse all connected atoms starting from '
                 'there to get the entire side chain. Then, check if any part '
                 'of that side chain has polar groups capable of hydrogen '
                 'bonding.\n'
                 '\n'
                 'The previous code tried to use ReplaceSidechains which '
                 "probably isn't the right tool here. Instead, we can use a "
                 'substructure match to find the side chain atoms and then '
                 'check those atoms for polar groups.\n'
                 '\n'
                 'Another thing: the amino acid pattern might not be correctly '
                 'matching all cases. The SMARTS pattern should ensure that '
                 'the alpha carbon is connected to both the amino and carboxyl '
                 'groups. Maybe the previous pattern was too restrictive, '
                 'especially considering different protonation states (like '
                 'COO- instead of COOH).\n'
                 '\n'
                 "Let's adjust the amino acid pattern to be more inclusive. "
                 'The amino group could be NH2, NH3+, and the carboxyl could '
                 'be COOH or COO-.\n'
                 '\n'
                 'Once the amino acid is confirmed, extract the side chain by '
                 "finding the substituent on the alpha carbon that's not part "
                 'of the amino or carboxyl groups. Then, check that side chain '
                 'for any polar groups like -OH, -SH, amide, guanidine, etc.\n'
                 '\n'
                 'So, the steps should be:\n'
                 '\n'
                 '1. Check if the molecule is an amino acid (has alpha carbon '
                 'with amino and carboxyl groups).\n'
                 '2. Identify the side chain atoms.\n'
                 '3. Check if the side chain contains any polar groups that '
                 'can form hydrogen bonds.\n'
                 '\n'
                 'To extract the side chain correctly without '
                 'ReplaceSidechains, perhaps use a recursive approach to '
                 'collect all atoms starting from the side chain atom '
                 'connected to the alpha carbon.\n'
                 '\n'
                 'Testing the example SMILES like L-arginine: the side chain '
                 'has a guanidine group, which should be detected. The '
                 "previous code's ReplaceSidechains failed here, leading to no "
                 'detection.\n'
                 '\n'
                 'So, fixing the side chain extraction by traversing the atoms '
                 'from the side chain start and then checking for polar groups '
                 'in that subset.\n'
                 '\n'
                 'Also, need to handle cases where the side chain might have '
                 "multiple polar groups, like serine's -OH.\n"
                 '\n'
                 'Let me adjust the code:\n'
                 '\n'
                 '- Remove the ReplaceSidechains part.\n'
                 '- Once the side chain starting atom is found, collect all '
                 'connected atoms (except the alpha carbon) as the side '
                 'chain.\n'
                 '- Then, check those atoms for any polar groups using SMARTS '
                 'patterns.\n'
                 '\n'
                 'That way, even if the side chain is branched, all parts are '
                 'checked.\n'
                 '\n'
                 'Also, the initial amino acid pattern might need adjustment. '
                 "Let's use a SMARTS that matches the general amino acid "
                 'structure: [NH2,NH3+] connected to a carbon connected to a '
                 'carboxyl group (C(=O)[OH,O-]).\n'
                 '\n'
                 'So, the revised code would:\n'
                 '\n'
                 '- Parse the SMILES.\n'
                 '- Check for amino acid structure.\n'
                 "- Find the alpha carbon's side chain atom.\n"
                 '- Traverse all atoms in the side chain.\n'
                 '- Check those atoms for presence of polar groups.\n'
                 '\n'
                 'This approach should avoid the ReplaceSidechains error and '
                 'correctly identify polar side chains.\n'
                 '\n'
                 "Another thing: the previous code's aromatic ring check might "
                 'not have worked because it was looking for atoms in the ring '
                 'with N or O, but maybe the substituents are outside. Like '
                 'tyrosine has a hydroxyl on the benzene ring. So checking for '
                 '-OH attached to an aromatic ring would be better.\n'
                 '\n'
                 'But perhaps using the existing polar patterns (like '
                 'hydroxyl) would catch that anyway.\n'
                 '\n'
                 'So, the key fix is correctly identifying the side chain '
                 'atoms and checking them for polar groups without using '
                 "ReplaceSidechains. Let's implement that.\n"
                 '\n'
                 'Now, writing the code:\n'
                 '\n'
                 'First, the amino acid pattern: '
                 '[NX3;H2,H1+0][CX4H]([CX3](=[OX1])[OX2H1,O-])[!H0]\n'
                 '\n'
                 'Wait, maybe better to use a SMARTS that captures the amino '
                 'group (NH2 or NH3+), the alpha carbon connected to that '
                 'amino group and a carboxyl group (COOH or COO-), and the '
                 'side chain.\n'
                 '\n'
                 'The SMARTS pattern could be: '
                 '[NX3;H2,H3+][CX4H]([CX3](=[OX1])[OX2H1,O-])[!$([NH2,NH3+,CO,COO])]\n'
                 '\n'
                 'But perhaps a better approach is to split into two parts: '
                 'first check for the amino and carboxyl groups, then find the '
                 'alpha carbon.\n'
                 '\n'
                 'Alternatively, use a SMARTS that matches the general amino '
                 'acid backbone.\n'
                 '\n'
                 'Once the alpha carbon is identified, the side chain is the '
                 "substituent that's not part of the amino or carboxyl "
                 'groups.\n'
                 '\n'
                 'Then, collect all atoms connected to the alpha carbon except '
                 'those in the amino or carboxyl groups. That would be the '
                 'side chain.\n'
                 '\n'
                 'Once the side chain atoms are identified, check each atom in '
                 'the side chain for polar groups.\n'
                 '\n'
                 'So, in code:\n'
                 '\n'
                 'After finding the alpha carbon, iterate through its '
                 'neighbors. The amino group is the N, the carboxyl is the C '
                 'connected to O. The remaining neighbor is the start of the '
                 'side chain.\n'
                 '\n'
                 'Then, perform a depth-first search from that starting atom '
                 'to collect all side chain atoms.\n'
                 '\n'
                 'Once we have all side chain atoms, create a submol or check '
                 'those atoms for polar groups.\n'
                 '\n'
                 'But creating a submol might be complex. Alternatively, check '
                 'the entire molecule but restrict the matches to the side '
                 'chain atoms.\n'
                 '\n'
                 'Alternatively, use SMARTS patterns that are present in the '
                 'side chain.\n'
                 '\n'
                 'So, the code steps:\n'
                 '\n'
                 "1. Check if it's an amino acid.\n"
                 '2. Find the alpha carbon.\n'
                 '3. Identify the side chain atoms.\n'
                 '4. Check if any of those atoms are part of a polar group.\n'
                 '\n'
                 'To implement step 3:\n'
                 '\n'
                 'After finding the alpha carbon, for each neighbor:\n'
                 '\n'
                 '- If the neighbor is part of the amino group (N with H2 or '
                 'H3+), skip.\n'
                 '- If the neighbor is part of the carboxyl group (C connected '
                 'to O via double bond), skip.\n'
                 '- The remaining neighbor is the side chain start.\n'
                 '\n'
                 'Then, collect all atoms connected to that start, excluding '
                 'the alpha carbon.\n'
                 '\n'
                 'Once we have all side chain atoms, check if any of them are '
                 'part of a polar group.\n'
                 '\n'
                 'So, in code:\n'
                 '\n'
                 'matches = mol.GetSubstructMatches(amino_acid_pattern)\n'
                 'alpha_carbon_idx = matches[0][1]\n'
                 'alpha_carbon = mol.GetAtomWithIdx(alpha_carbon_idx)\n'
                 '\n'
                 'side_chain_start = None\n'
                 'for neighbor in alpha_carbon.GetNeighbors():\n'
                 '    # Check if neighbor is part of amino group\n'
                 '    if neighbor.GetAtomicNum() == 7:\n'
                 "        # Amino group: check if it's NH2 or NH3+\n"
                 '        if neighbor.GetTotalNumHs() >= 2 or '
                 'neighbor.GetFormalCharge() == 1:\n'
                 '            continue\n'
                 '    # Check if neighbor is part of carboxyl group\n'
                 '    if neighbor.GetAtomicNum() == 6:\n'
                 '        for bond in neighbor.GetBonds():\n'
                 '            if bond.GetBondType() == Chem.BondType.DOUBLE:\n'
                 '                other_atom = bond.GetOtherAtom(neighbor)\n'
                 '                if other_atom.GetAtomicNum() == 8:\n'
                 '                    continue  # part of carboxyl\n'
                 "    # If not amino or carboxyl, it's the side chain start\n"
                 '    side_chain_start = neighbor\n'
                 '    break\n'
                 '\n'
                 'if not side_chain_start:\n'
                 '    return False, "No side chain"\n'
                 '\n'
                 '# Collect all atoms in the side chain\n'
                 'side_chain_atoms = set()\n'
                 'stack = [side_chain_start]\n'
                 'while stack:\n'
                 '    atom = stack.pop()\n'
                 '    if atom.GetIdx() in side_chain_atoms or atom.GetIdx() == '
                 'alpha_carbon_idx:\n'
                 '        continue\n'
                 '    side_chain_atoms.add(atom.GetIdx())\n'
                 '    for neighbor in atom.GetNeighbors():\n'
                 '        if neighbor.GetIdx() not in side_chain_atoms and '
                 'neighbor.GetIdx() != alpha_carbon_idx:\n'
                 '            stack.append(neighbor)\n'
                 '\n'
                 '# Now check if any of these atoms are part of polar groups\n'
                 'polar_patterns = {\n'
                 '    "hydroxyl": MolFromSmarts("[OX2H]"),  # -OH\n'
                 '    "thiol": MolFromSmarts("[SX2H]"),     # -SH\n'
                 '    "amide": MolFromSmarts("[CX3](=O)[NX3H2]"),  # -CONH2\n'
                 '    "guanidine": MolFromSmarts("[NH]C(=N)N"),    # '
                 "arginine's group\n"
                 '    "imidazole": MolFromSmarts("[nH]1cccn1"),    # '
                 'histidine\n'
                 '    "carboxyl": MolFromSmarts("[CX3](=O)[OX2H1,O-]"),  # '
                 '-COOH or COO-\n'
                 '    "amino": MolFromSmarts("[NX3H2]"),           # -NH2 '
                 '(lysine)\n'
                 '    "ether_oxygen": MolFromSmarts("[OX2H0]([#6])[#6]"), # '
                 'ether oxygen\n'
                 '    "aromatic_nitrogen": MolFromSmarts("[nH]"),   # aromatic '
                 'N (histidine)\n'
                 '    "sulfoxide": MolFromSmarts("[SX3](=O)"),      # '
                 'sulfoxide (maybe not present)\n'
                 '    "nitro": MolFromSmarts("[NX3+](=O)[O-]"),     # nitro '
                 'group (uncommon)\n'
                 '}\n'
                 '\n'
                 'for group_name, pattern in polar_patterns.items():\n'
                 '    if pattern is None:\n'
                 '        continue\n'
                 '    matches = mol.GetSubstructMatches(pattern)\n'
                 '    for match in matches:\n'
                 '        # Check if any atom in the match is in the side '
                 'chain atoms\n'
                 '        if any(atom_idx in side_chain_atoms for atom_idx in '
                 'match):\n'
                 '            return True, f"Side chain contains {group_name} '
                 'group"\n'
                 '\n'
                 '# Also check for aromatic rings with polar substituents in '
                 'the side chain\n'
                 'for atom_idx in side_chain_atoms:\n'
                 '    atom = mol.GetAtomWithIdx(atom_idx)\n'
                 '    if atom.GetIsAromatic():\n'
                 '        for neighbor in atom.GetNeighbors():\n'
                 '            if neighbor.GetAtomicNum() == 8 and '
                 'neighbor.GetTotalNumHs() == 1:  # -OH attached to aromatic\n'
                 '                return True, "Aromatic ring with hydroxyl '
                 'group"\n'
                 '\n'
                 'return False, "No polar groups in side chain"\n'
                 '\n'
                 'This approach avoids ReplaceSidechains and instead collects '
                 'the side chain atoms, then checks if any of those atoms are '
                 'part of a polar group.\n'
                 '\n'
                 'Testing this with the example SMILES:\n'
                 '\n'
                 'For L-arginine (SMILES: N[C@@H](CCCNC(N)=N)C(O)=O), the side '
                 'chain is CCCNC(N)=N. The guanidine group should match the '
                 '"guanidine" pattern.\n'
                 '\n'
                 'Similarly, serine (SMILES: NC(CO)C(O)=O) has a side chain '
                 'CO, which includes a hydroxyl group.\n'
                 '\n'
                 'This should correctly identify the polar groups in the side '
                 'chain.\n'
                 '\n'
                 'Also, the initial amino acid pattern should be adjusted to '
                 'correctly identify amino acids. The previous pattern might '
                 "have been too strict. Let's use a SMARTS that looks for an "
                 "amino group (NH2 or NH3+) connected to a carbon that's also "
                 'connected to a carboxyl group (COOH or COO-).\n'
                 '\n'
                 'The amino_acid_pattern could be: '
                 '[NX3;H2,H3+][CX4H]([CX3](=[OX1])[OX2H1,O-])[!H0]\n'
                 '\n'
                 'But perhaps a better way is to split into two parts: first '
                 'check for the amino group and the carboxyl group.\n'
                 '\n'
                 'Alternatively, use a SMARTS like:\n'
                 '\n'
                 'amino_acid_pattern = '
                 'MolFromSmarts("[NH2,NH3+]-[CH](-C(=O)[OH,O-])-*")\n'
                 '\n'
                 'This would match the amino group connected to the alpha '
                 'carbon, which is connected to the carboxyl group and another '
                 'group (the side chain).\n'
                 '\n'
                 'Putting it all together, the code should now correctly '
                 'identify the side chain and check for polar groups without '
                 'using ReplaceSidechains.\n'
                 '\n'
                 'Let me write the corrected code now.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 31,
    'num_false_positives': 1455,
    'num_true_negatives': 140808,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.02086137281292059,
    'recall': 0.8378378378378378,
    'f1': 0.040709126723571895,
    'accuracy': 0.9897329585382993,
    'negative_predictive_value': 0.9999573906003665}