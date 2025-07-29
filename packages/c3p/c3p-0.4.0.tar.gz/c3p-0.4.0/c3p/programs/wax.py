"""
Classifies: CHEBI:73702 wax
"""
"""
Classifies: Wax (long-chain ester)
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_wax(smiles: str):
    """
    Determines if a molecule is a wax based on its SMILES string.
    Waxes are esters of long-chain alcohols and long-chain fatty acids.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a wax, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES"

    # Check for exactly one ester group
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 1"

    # Get ester oxygen and carbonyl carbon indices
    oxygen_idx = ester_matches[0][0]
    carbonyl_c_idx = ester_matches[0][1]

    # Identify alcohol component (connected to ester oxygen)
    oxygen = mol.GetAtomWithIdx(oxygen_idx)
    alcohol_start = None
    for neighbor in oxygen.GetNeighbors():
        if neighbor.GetIdx() != carbonyl_c_idx:
            alcohol_start = neighbor.GetIdx()
            break
    if alcohol_start is None:
        return False, "No alcohol component found"

    # Identify acid component (connected to carbonyl carbon)
    carbonyl_c = mol.GetAtomWithIdx(carbonyl_c_idx)
    acid_start = None
    for neighbor in carbonyl_c.GetNeighbors():
        if neighbor.GetIdx() == oxygen_idx:
            continue
        bond = mol.GetBondBetweenAtoms(carbonyl_c_idx, neighbor.GetIdx())
        if bond.GetBondType() == Chem.BondType.DOUBLE and neighbor.GetAtomicNum() == 8:
            continue  # Skip carbonyl oxygen
        acid_start = neighbor.GetIdx()
        break
    if acid_start is None:
        return False, "No acid component found"

    # Helper function to analyze component
    def analyze_component(start_idx, exclude):
        visited = set(exclude)
        stack = [start_idx]
        carbon_count = 0
        in_ring = False
        while stack:
            atom_idx = stack.pop()
            if atom_idx in visited:
                continue
            visited.add(atom_idx)
            atom = mol.GetAtomWithIdx(atom_idx)
            
            # Check for rings
            if atom.IsInRing():
                in_ring = True
                
            # Count carbons
            if atom.GetAtomicNum() == 6:
                carbon_count += 1
                
            # Check for forbidden groups (amide, nitrile, etc.)
            for bond in atom.GetBonds():
                neighbor_idx = bond.GetOtherAtomIdx(atom_idx)
                if neighbor_idx in visited:
                    continue
                stack.append(neighbor_idx)
                
        return carbon_count, in_ring

    # Analyze both components
    exclude = {oxygen_idx, carbonyl_c_idx}
    alcohol_carbons, alcohol_in_ring = analyze_component(alcohol_start, exclude)
    acid_carbons, acid_in_ring = analyze_component(acid_start, exclude)

    # Check for rings in components
    if alcohol_in_ring or acid_in_ring:
        return False, "Component in ring structure"

    # Check chain lengths (minimum 8 carbons each)
    if alcohol_carbons < 8 or acid_carbons < 8:
        return False, f"Chain lengths too short (alcohol: {alcohol_carbons}, acid: {acid_carbons})"

    # Check for other functional groups
    forbidden_patterns = {
        "carboxylic_acid": Chem.MolFromSmarts("C(=O)[OH]"),
        "amide": Chem.MolFromSmarts("[NX3][CX3](=[OX1])"),
        "nitrile": Chem.MolFromSmarts("C#N"),
        "sulfonic_acid": Chem.MolFromSmarts("S(=O)(=O)O"),
        "phosphate": Chem.MolFromSmarts("OP(=O)(O)O"),
    }
    for name, pattern in forbidden_patterns.items():
        if mol.HasSubstructMatch(pattern):
            return False, f"Contains {name.replace('_', ' ')} group"

    # Check molecular weight (typical waxes > 300 Da)
    mol_wt = Descriptors.ExactMolWt(mol)
    if mol_wt < 300:
        return False, f"Molecular weight too low ({mol_wt:.1f} Da)"

    return True, "Long-chain ester meeting wax criteria"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:73702',
                          'name': 'wax',
                          'definition': 'A chemical substance that is an '
                                        'organic compound or mixture of '
                                        'compounds that is composed of '
                                        'long-chain molecules and is malleable '
                                        'at ambient temperatures.',
                          'parents': ['CHEBI:59999', 'CHEBI:61697'],
                          'xrefs': [   'PMID:21333071',
                                       'PMID:23050609',
                                       'PMID:23103356',
                                       'PMID:23288373',
                                       'Wikipedia:Wax'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 93,
                           'log_lines_of_code': 4.532599493153256,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import Descriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetBonds',
                                                 'add',
                                                 'GetNeighbors',
                                                 'GetBondType',
                                                 'IsInRing',
                                                 'HasSubstructMatch',
                                                 'replace',
                                                 'ExactMolWt',
                                                 'GetAtomicNum',
                                                 'GetBondBetweenAtoms',
                                                 'GetSubstructMatches',
                                                 'GetIdx',
                                                 'append',
                                                 'items',
                                                 'pop',
                                                 'MolFromSmiles',
                                                 'GetOtherAtomIdx',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts'],
                           'methods_called_count': 19,
                           'smarts_strings': [   'S(=O)(=O)O',
                                                 '[OX2][CX3](=[OX1])',
                                                 '[NX3][CX3](=[OX1])',
                                                 'C#N',
                                                 'C(=O)[OH]',
                                                 'OP(=O)(O)O'],
                           'smarts_strings_count': 6,
                           'defs': [   'is_wax(smiles: str):',
                                       'analyze_component(start_idx, '
                                       'exclude):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES"',
                                          'False, f"Found {len(ester_matches)} '
                                          'ester groups, need exactly 1"',
                                          'False, "No alcohol component found"',
                                          'False, "No acid component found"',
                                          'carbon_count, in_ring',
                                          'False, "Component in ring '
                                          'structure"',
                                          'False, f"Chain lengths too short '
                                          '(alcohol: {alcohol_carbons}, acid: '
                                          '{acid_carbons})"',
                                          'False, f"Contains '
                                          '{name.replace(\'_\', \' \')} group"',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} Da)"',
                                          'True, "Long-chain ester meeting wax '
                                          'criteria"'],
                           'returns_count': 10,
                           'complexity': 8.106519898630651},
    'message': '\n'
               'Attempt failed: F1 score of 0.02440607555497858 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O(CCCCCCCCCCCCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\CCCC NAME: Behenyl '
               'myristoleate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: OC(CCCCCCCCOC(=O)CCCCCCCCCCCCCCCCCCCCC)CCCC NAME: '
               '9-Hydroxytridecyl docosanoate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: CCCCCCCCCCCCOC(=O)CCCCCCC\\C=C/CCCCCC NAME: lauryl '
               'palmitoleate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: O(CCCCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: Myristyl linoleate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCCCCCC)C(=O)CCCCCCCCCCCCCCCCC '
               'NAME: Oleyl stearate REASON: CORRECT Long-chain ester meeting '
               'wax criteria\n'
               ' * SMILES: O(CCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\CCCCC NAME: '
               'Lauryl linoleate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: '
               'O(CCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(=O)CCCCCCC/C=C\\CCCCCCCC '
               'NAME: Linolenyl oleate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'O(CCCCCCCC/C=C\\CCCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\CCCCC NAME: '
               'Palmitoleyl linoleate REASON: CORRECT Long-chain ester meeting '
               'wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\C/C=C\\CCCCC)C(=O)CCCCCCCCCCCCCCCCC '
               'NAME: Linoleyl stearate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C/CCCCCCCC)C(=O)CCCCCCCCCCCCCCC NAME: '
               'Elaidyl palmitate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OCCCCCCCC NAME: octyl palmitate '
               'REASON: CORRECT Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'O(CCCCCCCCCC/C=C\\CCCCCCCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: Gondoyl-linoleate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCC)C(=O)CCCCCCCCCCC NAME: '
               'Myristoleyl laurate REASON: CORRECT Long-chain ester meeting '
               'wax criteria\n'
               ' * SMILES: '
               'O(CCCCCCCC/C=C\\C/C=C\\CCCCC)C(=O)CCCCCCC/C=C\\CCCCCCCC NAME: '
               'Linoleyl oleate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: '
               'O(CCCCCCCCCCCCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: Behenyl linolenate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\C/C=C\\CCCCC)C(=O)CCCCCCCCCCC NAME: '
               'Linoleyl laurate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: '
               'O(CCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(=O)CCCCCCCCCCCCCCCCC NAME: '
               'Linolenyl stearate REASON: CORRECT Long-chain ester meeting '
               'wax criteria\n'
               ' * SMILES: '
               'O(CCCCCCCC/C=C\\C/C=C\\CCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: Linoleyl linolenate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCCCCCC)C(=O)CCCCCCCCCCCCCCCCCCC '
               'NAME: Oleyl arachidate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCOC(=O)CCCCCCCCCCCCCCC NAME: '
               'stearyl palmitate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCCCC)C(=O)CCCCCCC/C=C\\CCCC NAME: '
               'Palmitoleyl myristoleate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCCCCCC)C(=O)CCCCCCCCCCCCCCC NAME: '
               'Oleyl palmitate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OCCCCCCCCC NAME: nonyl '
               'palmitate REASON: CORRECT Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCCCC)C(=O)CCCCCCCCCCCCCCCCCCCCC '
               'NAME: Palmitoleyl behenate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: O(CCCCCCCC/C=C\\CCCC)C(=O)CCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: Myristoleyl linoleate REASON: CORRECT Long-chain ester '
               'meeting wax criteria\n'
               'False positives: SMILES: '
               'O=C1C(O)=CC(C)(C)C(=C1C)/C=C/2\\OC(=O)C=C2C NAME: '
               'Gamma-Abscisolactone REASON: WRONGLY CLASSIFIED Long-chain '
               'ester meeting wax criteria\n'
               ' * SMILES: O1CC=C(CCC=CCC1=O)C NAME: (3E,8E)-suspensolide '
               'REASON: WRONGLY CLASSIFIED Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: '
               'C12(OC3(C(C(Cl)=C4C(C3([H])C1(C(OC(C2C)C)=O)[H])=COC(=C4)/C=C/C(C(C)O)C)=O)C)O '
               'NAME: chaetoviridin D REASON: WRONGLY CLASSIFIED Long-chain '
               'ester meeting wax criteria\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@H]2CC[C@@]3(CO)[C@@H](CC[C@@H]4[C@@H]3CC[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)[C@H](O)[C@H](O)[C@H]1O '
               'NAME: Coroglaucigenin-3-o-alpha-L-rhamnopyranoside REASON: '
               'WRONGLY CLASSIFIED Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)O[C@H](CO)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 2-arachidonoyl-sn-glycero-3-phosphocholine REASON: '
               'WRONGLY CLASSIFIED Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'O=C1O[C@H]2[C@H](O[C@H](C2)[C@@H](O)CC)C=3C1=C(O)C(OC)=C(OC)C3 '
               'NAME: Exserolide E REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'C[C@H]1CC[C@@H]2[C@@H](OC(=O)C2=C)[C@]2(C)C(=O)CC[C@@]12O '
               'NAME: Coronopilin REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'CC1=C(SC=[N+]1CC#N)CCOC(=O)C2=CC(=C(C=C2)N3CCOCC3)[N+](=O)[O-] '
               'NAME: 4-(4-morpholinyl)-3-nitrobenzoic acid '
               '2-[3-(cyanomethyl)-4-methyl-5-thiazol-3-iumyl]ethyl ester '
               'REASON: WRONGLY CLASSIFIED Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: '
               'O1[C@@]2(O)C[C@@]3([C@]([C@@H](CCC3=O)C)(CC2=C(C1=O)C)C)[H] '
               'NAME: Istanbulin A REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'C[N+]12CCC(CC1)C(C2)OC(=O)C(C3=CC=CC=C3)(C4=CC=CC=C4)O NAME: '
               '2-hydroxy-2,2-diphenylacetic acid '
               '(1-methyl-1-azoniabicyclo[2.2.2]octan-3-yl) ester REASON: '
               'WRONGLY CLASSIFIED Long-chain ester meeting wax criteria\n'
               ' * SMILES: O1C(CCCCC)C=CC1=O NAME: 2-nonen-4-olide REASON: '
               'WRONGLY CLASSIFIED Long-chain ester meeting wax criteria\n'
               ' * SMILES: Cc1ccc(cc1)S(=O)(=O)OCC1CC(C)(C)OC1=O NAME: '
               '3-tosyloxymethyl-5,5-dimethylbutyrolactone REASON: WRONGLY '
               'CLASSIFIED Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'CCCC1=CC2=C(CO1)C(=O)[C@](C)(OC(=O)c1c(C)cc(O)cc1OC)[C@H](O)C2 '
               'NAME: comazaphilone A REASON: WRONGLY CLASSIFIED Long-chain '
               'ester meeting wax criteria\n'
               ' * SMILES: '
               'O1C[C@@H]([C@@H](CC2=C(O)C=CC(O)=C2)C1=O)CC3=CC(O)=CC=C3 NAME: '
               '6-Hydroxyenterolactone REASON: WRONGLY CLASSIFIED Long-chain '
               'ester meeting wax criteria\n'
               ' * SMILES: '
               'O=C1O[C@]2(O[C@@H]3[C@@H](O)[C@@H](C)O[C@@H]3C2)C=C1 NAME: '
               'Pyrenolide D REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'CC(=O)Cc1cc(=O)c2c(C)cc(O)c([C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3OC(=O)\\C=C\\c3ccc(O)cc3)c2o1 '
               "NAME: 2''-o-p-Coumaroylaloesin REASON: WRONGLY CLASSIFIED "
               'Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'BrC1=C(O)C(Br)=CC(=C1)/C=C/C=C/C=C/C=C/C(=O)N[C@@H]2C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(O[C@@H]2C)=O)[C@@H](CC)C)=O)CC(=O)N)CC(=O)N)C(C)C '
               'NAME: Dibromoalterochromide A REASON: WRONGLY CLASSIFIED '
               'Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'CC[C@H]1OC(=O)\\C=C\\[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2O)N(C)C)[C@@H](C)C[C@@H](C)C(=O)\\C=C\\C=C\\[C@@H]1CO '
               'NAME: Mycinamicin VII REASON: WRONGLY CLASSIFIED Long-chain '
               'ester meeting wax criteria\n'
               ' * SMILES: O=C1OCC=C1CCC(=O)N(NC(=O)C)/C=C\\CCCC NAME: '
               'Geralcin B REASON: WRONGLY CLASSIFIED Long-chain ester meeting '
               'wax criteria\n'
               ' * SMILES: O=C1O[C@@H]([C@@H](O)[C@H](O)[C@H](O)C)C=C1C NAME: '
               'Xylogiblactone B REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'CO[C@@H](C[C@@H]1OC(=O)C[C@@H](O)C[C@H](C)C[C@H](O)[C@H](C)[C@@H](OC)c2coc(n2)-c2coc(n2)-c2coc(\\C=C\\C[C@H](OC)[C@H]1C)n2)[C@@H](C)CCC(=O)[C@H](C)[C@H](OC)[C@H](C)\\C=C\\N(C)C=O '
               'NAME: kabiramide D REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: '
               'O=C/1NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)O[C@H]([C@@H](C(NC(C(NC(C(N\\C1=C/C)=O)C)=O)CO)=O)NC(=O)/C(/NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C2N(C(=O)/C(/NC(=O)CC(O)CCCCCCCCCCC)=C/C)CCC2)C(C)C)CC(C)C)C)C)CC(C)C)C(C)C)C)C)C(C)C)C)C)=C/C)C)CC3=CC=C(O)C=C3)CCN)CCN)C '
               'NAME: Syringopeptin, SP508 B REASON: WRONGLY CLASSIFIED '
               'Long-chain ester meeting wax criteria\n'
               ' * SMILES: '
               'O=C1OC(C(NC(=O)C(O)C(O)C2NC(NC(C2)=O)(C)C)CC(C)C)CC=3C1=C(O)C=CC3 '
               'NAME: Hetiamacin B REASON: WRONGLY CLASSIFIED Long-chain ester '
               'meeting wax criteria\n'
               ' * SMILES: C\\C=C\\C1OC(\\C=C\\C)C2=CC(O)C(=O)OC12 NAME: '
               'FD-211 REASON: WRONGLY CLASSIFIED Long-chain ester meeting wax '
               'criteria\n'
               ' * SMILES: '
               'O=C1NC(=O)CC(C1)C[C@@H](O)CC(=O)[C@H](/C=C/CCCCCCCCC(=O)C=2C(=O)OC(C2C)O)C '
               'NAME: Gladiofungin A REASON: WRONGLY CLASSIFIED Long-chain '
               'ester meeting wax criteria\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OCC(CCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: 2-palmitoyloxypalmityl palmitate REASON: MISSED Found 2 '
               'ester groups, need exactly 1\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC2=C(O)C(OC)=CC(=C2C=3C1=C(O)C=C(O)C3)O',
                                     'name': 'Graphislactone F',
                                     'reason': 'Found 0 ester groups, need '
                                               'exactly 1'},
                                 {   'smiles': 'O=C1C(O)=CC(C)(C)C(=C1C)/C=C/2\\OC(=O)C=C2C',
                                     'name': 'Gamma-Abscisolactone',
                                     'reason': 'Component in ring structure'},
                                 {   'smiles': 'C(CCCCCC(CC)C)CCCC[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCC)=O)CO',
                                     'name': 'N-docosanoyl-14-methylhexadecasphinganine',
                                     'reason': 'Found 0 ester groups, need '
                                               'exactly 1'},
                                 {   'smiles': 'O=C1C2=C(C(=O)CC3[C@@]2(CC[C@@H]([C@]3(CO)C)O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1OC(=O)C)C)C(CCC(=O)O)C)C',
                                     'name': 'Lucidenic acid R',
                                     'reason': 'Found 2 ester groups, need '
                                               'exactly 1'},
                                 {   'smiles': 'O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CCC(O)=O)C(O)=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2',
                                     'name': 'Trp-Asn-Glu',
                                     'reason': 'Found 2 ester groups, need '
                                               'exactly 1'},
                                 {   'smiles': 'O1[C@H]([C@H](NC(=O)CO)[C@@H](O)CC1(O[C@H]2[C@@H](O)[C@H](O[C@@H](O)[C@@H]2O)CO)C(O)=O)[C@H](O)[C@H](O)CO',
                                     'name': '(4S,5R,6R)-4-Hydroxy-5-[(2-hydroxyacetyl)amino]-2-[(2R,3R,4S,5S,6R)-2,3,5-trihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No alcohol component found'},
                                 {   'smiles': 'C[C@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=NC=C3)[C@@H](C)CO)C)CN(C)C(=O)C4CCCCC4',
                                     'name': 'N-[(3S,9R,10S)-9-[[[cyclohexyl(oxo)methyl]-methylamino]methyl]-12-[(2S)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]-4-pyridinecarboxamide',
                                     'reason': 'Found 0 ester groups, need '
                                               'exactly 1'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CCCCN',
                                     'name': 'Gln-Lys-Phe',
                                     'reason': 'No alcohol component found'},
                                 {   'smiles': 'O=C(NC(CC(O)=O)C(O)=O)C(N)C',
                                     'name': 'Alanyl-Aspartate',
                                     'reason': 'Found 2 ester groups, need '
                                               'exactly 1'},
                                 {   'smiles': 'C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])O',
                                     'name': 'DG(14:0/20:4(5Z,8Z,11Z,14Z)/0:0)',
                                     'reason': 'Found 2 ester groups, need '
                                               'exactly 1'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCC(CCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC',
                                      'name': '2-palmitoyloxypalmityl '
                                              'palmitate',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 1'}],
    'attempt': 2,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's see why the previous code didn't work well. The "
                 'main issue was false positives and some false negatives. The '
                 'false positives like Gamma-Abscisolactone were wrongly '
                 'classified as waxes. Looking at their structures, they have '
                 'the ester group but maybe shorter chains or other functional '
                 'groups. The previous code checked for exactly one ester '
                 'group, which was correct, but maybe the chain length '
                 "calculation wasn't accurate enough. For example, the code "
                 'required both alcohol and acid parts to have at least 8 '
                 'carbons. But some of the false positives might have met this '
                 "but aren't actually waxes because they have rings or other "
                 'structures. Also, the false negatives like '
                 '2-palmitoyloxypalmityl palmitate were missed because they '
                 'have two ester groups, but the code required exactly one. '
                 'However, waxes are typically monoesters, so that check was '
                 'correct. Wait, but that example has three ester groups? Let '
                 'me check. The SMILES is '
                 'CCCCCCCCCCCCCCCC(=O)OCC(CCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC. '
                 "Oh, right, it's a diester (two ester groups), which the code "
                 'would reject. But according to the definition, waxes are '
                 "monoesters, so that's correct. But maybe some examples in "
                 'the training data have more than one ester? Wait, looking at '
                 'the examples provided, all the positives are monoesters. So '
                 "the code's check for exactly one ester is correct. The "
                 'problem with false positives must be due to other reasons.\n'
                 '\n'
                 'Another thing: the previous code checked for carboxylic acid '
                 'groups (-COOH) and excluded those. But some of the false '
                 'positives might have other functional groups, like amides, '
                 'lactones, or other esters. For example, the false positive '
                 '2-arachidonoyl-sn-glycero-3-phosphocholine has a phosphate '
                 "group, which the code didn't check for. So the code needs to "
                 'ensure there are no other functional groups besides the '
                 'ester.\n'
                 '\n'
                 'Also, the chain length calculation might not be sufficient. '
                 'The code counts all carbons in each component, but maybe the '
                 'actual chain length (as in continuous carbon chain) is '
                 'shorter. For example, if the alcohol or acid part has '
                 "branches, the code's count would include all carbons, but "
                 'the actual chain might be shorter. Waxes typically have '
                 'long, straight chains. So maybe checking for long chains '
                 'without branching or other substituents is important.\n'
                 '\n'
                 "Additionally, the code didn't check for unsaturation. Some "
                 'waxes have unsaturated chains, but maybe the false positives '
                 'have conjugated systems or other features that are not '
                 'typical of waxes. However, the examples provided include '
                 "waxes with double bonds, so the code shouldn't exclude "
                 'those. But perhaps the code should check that the chains are '
                 'mainly aliphatic without aromatic rings or other complex '
                 'structures.\n'
                 '\n'
                 'Another point: the code uses a helper function to count '
                 'carbons in each component. But this function counts all '
                 'carbons connected to the starting point, which might include '
                 'branches. For example, if the alcohol part is branched, the '
                 'code would count all carbons in the branch, but waxes are '
                 'usually linear. So maybe the code should check for linear '
                 'chains rather than branched ones. However, detecting '
                 'linearity is tricky with SMARTS patterns. Alternatively, '
                 'maybe the code should require a minimum number of contiguous '
                 'carbons in a chain.\n'
                 '\n'
                 'Alternatively, perhaps using molecular weight as a proxy. '
                 'Waxes are typically high molecular weight. The previous code '
                 "didn't check molecular weight. Adding a check for molecular "
                 'weight above a certain threshold (like 300 or 400) might '
                 'help exclude smaller esters that are not waxes.\n'
                 '\n'
                 "Let's look at the false positives. For example, "
                 'Gamma-Abscisolactone (SMILES: '
                 'O=C1C(O)=CC(C)(C)C(=C1C)/C=C/2\\OC(=O)C=C2C) has an ester '
                 'group but is a cyclic structure with a lactone. The code '
                 "counts the carbons in the components, but since it's cyclic, "
                 'the actual chain length might be shorter. However, the '
                 "code's carbon count might include parts of the ring, leading "
                 'to a false positive. So maybe the code should check that '
                 'both the alcohol and acid parts are acyclic and have long '
                 'chains.\n'
                 '\n'
                 'How to detect if a component is part of a ring? The helper '
                 'function could check if any atom in the component is in a '
                 "ring. If either the alcohol or acid part is in a ring, it's "
                 'not a wax.\n'
                 '\n'
                 'Also, the code should ensure that there are no other ester '
                 'groups. The previous code checked for exactly one ester, '
                 'which is correct. But maybe other functional groups like '
                 'amides, ketones, etc., should be excluded.\n'
                 '\n'
                 'Putting this together, the revised code should:\n'
                 '\n'
                 '1. Check for exactly one ester group.\n'
                 '2. Ensure both alcohol and acid components are long chains '
                 '(maybe at least 12 carbons each, since examples like octyl '
                 'palmitate have 8+16, but wait octyl is C8, palmitate is C16. '
                 'The previous code required 8 each. Maybe increasing the '
                 'minimum to 12 each would help exclude smaller esters.\n'
                 '3. Check that neither component is part of a ring.\n'
                 '4. Ensure there are no other functional groups like '
                 'carboxylic acids, amides, etc.\n'
                 '5. Check molecular weight to be above a certain threshold.\n'
                 '6. Ensure that the chains are mainly aliphatic (no aromatic '
                 'rings in the components).\n'
                 '\n'
                 "Let's adjust the code accordingly. Increase the minimum "
                 'chain length for both alcohol and acid parts to 12 carbons. '
                 'Add a check for rings in either component. Add checks for '
                 'other functional groups. Also, calculate molecular weight.\n'
                 '\n'
                 'Wait, looking at the examples: octyl palmitate (C8 alcohol, '
                 'C16 acid) is considered a wax. So if the code requires at '
                 'least 12 carbons for both, that would exclude octyl '
                 'palmitate, which is a valid example. So maybe the minimum '
                 'should be lower. Alternatively, maybe the sum of both chains '
                 "should be above a certain value, but that's more complex. "
                 'Alternatively, require at least 12 carbons in one of the '
                 'chains and 8 in the other. But how to balance this?\n'
                 '\n'
                 'Alternatively, look for at least 12 carbons in the acid part '
                 'and 8 in the alcohol, as fatty acids in waxes are typically '
                 'long. But this might vary. Maybe setting both to at least 12 '
                 "would exclude some valid examples. The example 'nonyl "
                 "palmitate' has a C9 alcohol and C16 acid. If the code "
                 "requires at least 8 for both, that's okay, but maybe the "
                 'false positives have shorter chains. Wait, the previous code '
                 'required 8 each, but some false positives like '
                 'Gamma-Abscisolactone might have components that sum to more '
                 'than 8 but are in rings. So perhaps the main issue is not '
                 'chain length but the presence of rings or other functional '
                 'groups.\n'
                 '\n'
                 'So, the revised code should:\n'
                 '\n'
                 '- Check for exactly one ester group.\n'
                 '- Ensure both components (alcohol and acid) are acyclic.\n'
                 '- Check that each component has at least 8 carbons (as '
                 'before).\n'
                 '- Check for absence of other functional groups (like '
                 'carboxylic acids, amides, etc.).\n'
                 '- Maybe check molecular weight to be above 300.\n'
                 '\n'
                 'Additionally, the code should traverse the alcohol and acid '
                 'chains to count contiguous carbons without branching. But '
                 'how to do that with RDKit?\n'
                 '\n'
                 'Alternatively, use the number of rotatable bonds as a proxy '
                 'for chain length. Long chains have more rotatable bonds. But '
                 'this might not be reliable.\n'
                 '\n'
                 'Another approach: after identifying the alcohol and acid '
                 'parts, check if they are linear aliphatic chains. For '
                 'example, using SMARTS patterns for long alkyl chains. But '
                 'creating a SMARTS pattern for a chain of at least 8 carbons '
                 'is challenging.\n'
                 '\n'
                 'Alternatively, after isolating each component, check that '
                 'the component is a straight chain by ensuring that each '
                 'carbon (except the ends) has two single bonds (no '
                 'branching). But this is complex.\n'
                 '\n'
                 'Perhaps the best approach is to:\n'
                 '\n'
                 '1. Check for exactly one ester group.\n'
                 '2. Ensure that both the alcohol and acid parts are acyclic '
                 '(not in any rings).\n'
                 '3. Each part has at least 8 carbons.\n'
                 '4. No other functional groups present (like -COOH, -NH2, '
                 'etc.).\n'
                 '5. Molecular weight above 300.\n'
                 '\n'
                 "Let's modify the code accordingly.\n"
                 '\n'
                 'Also, in the previous code, the false negative '
                 '2-palmitoyloxypalmityl palmitate was missed because it has '
                 'two ester groups. But according to the definition, waxes are '
                 "monoesters, so that's correct. So the code correctly "
                 'excluded it.\n'
                 '\n'
                 'The false positives were due to esters with rings or other '
                 'functional groups. So adding checks for rings in the '
                 'components and other functional groups should help.\n'
                 '\n'
                 "Let's update the code:\n"
                 '\n'
                 '- After identifying the alcohol and acid components, check '
                 'if any atom in those components is in a ring.\n'
                 '- Check for other functional groups like amides, nitriles, '
                 'etc.\n'
                 '- Increase the minimum chain length to 12 for acid and 8 for '
                 'alcohol? Or keep at 8 each but add other checks.\n'
                 '\n'
                 "Testing with the example 'octyl palmitate' (C8 alcohol, C16 "
                 'acid), the code should accept it. If the code requires at '
                 "least 8 for both, it's okay. But if the acid part is in a "
                 "ring, it's rejected.\n"
                 '\n'
                 'So, adding code to check that neither component is in a '
                 'ring.\n'
                 '\n'
                 'Also, check for other functional groups. For example, if the '
                 "molecule has an amide group, it's not a wax.\n"
                 '\n'
                 'So, adding SMARTS patterns for other functional groups:\n'
                 '\n'
                 '- Amide: [NX3][CX3](=[OX1])\n'
                 '- Nitrile: C#N\n'
                 '- Sulfonic acid: S(=O)(=O)O\n'
                 '- Etc.\n'
                 '\n'
                 'Also, check for the presence of any charged atoms, which are '
                 'uncommon in waxes.\n'
                 '\n'
                 'Putting all this together, the revised code would:\n'
                 '\n'
                 '- Parse the molecule.\n'
                 '- Check for exactly one ester.\n'
                 '- Check that the ester components are acyclic.\n'
                 '- Check chain lengths (>=8 each).\n'
                 '- Check for absence of other functional groups.\n'
                 '- Check molecular weight.\n'
                 '\n'
                 'This should reduce false positives by excluding molecules '
                 'with rings, other functional groups, or insufficient chain '
                 'length.\n'
                 '\n'
                 'Another point: in the previous code, the helper function '
                 'counted all carbons in the component, including branches. '
                 'For example, if the alcohol is branched, like '
                 '(CH2)10CH(CH2)5CH3, the code counts all 16 carbons. But '
                 'waxes are typically linear. However, detecting linearity is '
                 'difficult. Maybe allowing some branching but ensuring that '
                 'the main chain is long enough. Alternatively, if the code '
                 'counts all carbons, even in branches, but requires a higher '
                 'minimum, that might help. For example, requiring at least 12 '
                 'carbons in each component. But octyl palmitate would have 8 '
                 "in alcohol, which is below 12. So that's a problem.\n"
                 '\n'
                 'Hmm, this is tricky. The examples include octyl palmitate '
                 '(C8 alcohol) and nonyl palmitate (C9), which are valid '
                 "waxes. So the minimum can't be raised to 12. So the previous "
                 "code's requirement of 8 each is correct. The problem must be "
                 'elsewhere.\n'
                 '\n'
                 'So, the main issues causing false positives are:\n'
                 '\n'
                 '1. Components in rings.\n'
                 '2. Presence of other functional groups.\n'
                 '3. Insufficient checks on molecular weight or chain '
                 'structure.\n'
                 '\n'
                 'So, adding checks for rings in components and other '
                 'functional groups should help.\n'
                 '\n'
                 "Let's modify the code:\n"
                 '\n'
                 '- After identifying the alcohol and acid components, check '
                 'if any atom in those components is part of a ring.\n'
                 '- Add checks for other functional groups (amide, nitrile, '
                 'etc.).\n'
                 '- Check molecular weight to be above, say, 300.\n'
                 '\n'
                 'Testing this should reduce false positives.\n'
                 '\n'
                 "Another thing: the previous code didn't check for "
                 'unsaturation, but waxes can have unsaturated chains. '
                 'However, some false positives might have conjugated esters '
                 'or other unsaturated systems that are not typical. But since '
                 "the examples include unsaturated waxes, the code shouldn't "
                 'exclude based on double bonds.\n'
                 '\n'
                 'So, the revised code would include:\n'
                 '\n'
                 '- Check for exactly one ester.\n'
                 '- Check that alcohol and acid components are acyclic (no '
                 'rings).\n'
                 '- Each component has >=8 carbons.\n'
                 '- No other functional groups (like carboxylic acid, amide, '
                 'etc.).\n'
                 '- Molecular weight >= 300 (or similar).\n'
                 '\n'
                 'This should help reduce false positives.\n'
                 '\n'
                 "Now, let's implement these changes in the code.\n"
                 '</think>',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 94,
    'num_false_positives': 53,
    'num_true_negatives': 142152,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.6394557823129252,
    'recall': 0.9894736842105263,
    'f1': 0.7768595041322315,
    'accuracy': 0.9996205200281096,
    'negative_predictive_value': 0.9999929653260923}