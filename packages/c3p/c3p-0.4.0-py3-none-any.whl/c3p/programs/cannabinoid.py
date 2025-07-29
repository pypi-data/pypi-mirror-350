"""
Classifies: CHEBI:67194 cannabinoid
"""
"""
Classifies: Cannabinoids
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_cannabinoid(smiles: str):
    """
    Determines if a molecule is a cannabinoid based on its SMILES string.
    Cannabinoids are characterized by specific structural features such as
    the dibenzopyran ring system in phytocannabinoids (e.g., THC, CBD),
    long-chain polyunsaturated fatty acid derivatives linked to ethanolamine
    or glycerol (e.g., endocannabinoids like anandamide and 2-AG),
    and synthetic cannabinoids with varied core structures but common pharmacophores.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cannabinoid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define pattern for phytocannabinoids like THC, CBD (dibenzopyran core)
    dibenzopyran_pattern = Chem.MolFromSmarts('c1ccc2c(c1)Oc3ccccc3c2')  # General dibenzopyran ring

    # Check for phytocannabinoid features
    if mol.HasSubstructMatch(dibenzopyran_pattern):
        return True, "Contains dibenzopyran ring system characteristic of phytocannabinoids"

    # Define pattern for endocannabinoids like anandamide (N-acylethanolamines)
    n_acylethanolamine_pattern = Chem.MolFromSmarts('C(=O)NCCO')

    # Define pattern for 2-acylglycerols like 2-AG (monoacylglycerols)
    monoacylglycerol_pattern = Chem.MolFromSmarts('C(=O)OCC(O)CO')

    # Function to analyze fatty acid chains
    def _analyze_fatty_acid_chain(mol, carbonyl_carbon_idx):
        """
        Analyzes the fatty acid chain attached to the carbonyl carbon.

        Args:
            mol: RDKit Mol object
            carbonyl_carbon_idx: Index of the carbonyl carbon

        Returns:
            chain_length: Number of carbons in the chain
            num_double_bonds: Number of double bonds in the chain
        """
        atom = mol.GetAtomWithIdx(carbonyl_carbon_idx)
        neighbors = [nbr.GetIdx() for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() == 6]
        chain_start_idx = None
        for idx in neighbors:
            if idx != carbonyl_carbon_idx:
                chain_start_idx = idx
                break
        if chain_start_idx is None:
            return 0, 0

        visited = set()
        to_visit = [(chain_start_idx, None)]  # (atom_idx, bond)
        chain_length = 0
        num_double_bonds = 0

        while to_visit:
            current_idx, bond = to_visit.pop()
            if current_idx in visited:
                continue
            visited.add(current_idx)
            atom = mol.GetAtomWithIdx(current_idx)
            if atom.GetAtomicNum() != 6:
                continue
            chain_length += 1
            if bond is not None and bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                num_double_bonds += 1
            for neighbor in atom.GetNeighbors():
                neighbor_idx = neighbor.GetIdx()
                if neighbor_idx not in visited and neighbor.GetAtomicNum() == 6:
                    b = mol.GetBondBetweenAtoms(current_idx, neighbor_idx)
                    to_visit.append((neighbor_idx, b))
        return chain_length, num_double_bonds

    # Check for endocannabinoid features (N-acylethanolamines)
    if mol.HasSubstructMatch(n_acylethanolamine_pattern):
        for match in mol.GetSubstructMatches(n_acylethanolamine_pattern):
            carbonyl_carbon_idx = match[0]  # Index of the carbonyl carbon
            chain_length, num_double_bonds = _analyze_fatty_acid_chain(mol, carbonyl_carbon_idx)
            if chain_length >= 16 and num_double_bonds >= 2:
                return True, "Contains long-chain polyunsaturated fatty acid amide linked to ethanolamine characteristic of endocannabinoids"
        return False, "Amide group found but fatty acid chain too short or not sufficiently unsaturated"

    # Check for endocannabinoid features (monoacylglycerols)
    if mol.HasSubstructMatch(monoacylglycerol_pattern):
        for match in mol.GetSubstructMatches(monoacylglycerol_pattern):
            carbonyl_carbon_idx = match[0]  # Index of the carbonyl carbon
            chain_length, num_double_bonds = _analyze_fatty_acid_chain(mol, carbonyl_carbon_idx)
            if chain_length >= 16 and num_double_bonds >= 2:
                return True, "Contains long-chain polyunsaturated fatty acid ester linked to glycerol characteristic of endocannabinoids"
        return False, "Ester group found but fatty acid chain too short or not sufficiently unsaturated"

    # Define pattern for synthetic cannabinoids (indole-based)
    indole_pattern = Chem.MolFromSmarts('c1ccc2c(c1)[nH]cc2')  # Indole core

    # Check for synthetic cannabinoid features (indole-based)
    if mol.HasSubstructMatch(indole_pattern):
        # Additional check for acyl or alkyl side chains
        side_chain_pattern = Chem.MolFromSmarts('n1cc(c2ccc(Cl)cc2)c(c1)C(=O)')
        if mol.HasSubstructMatch(side_chain_pattern):
            return True, "Contains indole core with acyl side chain characteristic of synthetic cannabinoids"
        return True, "Contains indole core characteristic of some synthetic cannabinoids"

    # Include pattern for naphthoylindole cannabinoids
    naphthoylindole_pattern = Chem.MolFromSmarts('c1ccc2c(c1)cccc2C(=O)N3CCCCC3')

    if mol.HasSubstructMatch(naphthoylindole_pattern):
        return True, "Contains naphthoylindole structure characteristic of synthetic cannabinoids"

    return False, "No characteristic cannabinoid structural features found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:67194',
                          'name': 'cannabinoid',
                          'definition': 'A diverse group of pharmacologically '
                                        'active secondary metabolite '
                                        'characteristic to Cannabis plant as '
                                        'well as produced naturally in the '
                                        'body by humans and animals. '
                                        'Cannabinoids contain oxygen as a part '
                                        'of the heterocyclic ring or in the '
                                        'form of various functional groups. '
                                        'They are subdivided on the basis of '
                                        'their origin.',
                          'parents': ['CHEBI:36963'],
                          'xrefs': [   'PMID:22234284',
                                       'PMID:22530636',
                                       'PMID:22555283',
                                       'Wikipedia:Cannabinoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 60,
                           'log_lines_of_code': 4.0943445622221,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
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
                                                 3,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 4,
                           'smarts_strings': [   'C(=O)NCCO',
                                                 'C(=O)OCC(O)CO',
                                                 'c1ccc2c(c1)[nH]cc2',
                                                 'n1cc(c2ccc(Cl)cc2)c(c1)C(=O)',
                                                 'c1ccc2c(c1)cccc2C(=O)N3CCCCC3',
                                                 'c1ccc2c(c1)Oc3ccccc3c2'],
                           'smarts_strings_count': 6,
                           'defs': [   'is_cannabinoid(smiles: str):',
                                       '_analyze_fatty_acid_chain(mol, '
                                       'carbonyl_carbon_idx):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains dibenzopyran ring '
                                          'system characteristic of '
                                          'phytocannabinoids"',
                                          'True, "Contains long-chain '
                                          'polyunsaturated fatty acid amide '
                                          'linked to ethanolamine '
                                          'characteristic of endocannabinoids"',
                                          'False, "Amide group found but fatty '
                                          'acid chain too short or not '
                                          'sufficiently unsaturated"',
                                          'True, "Contains long-chain '
                                          'polyunsaturated fatty acid ester '
                                          'linked to glycerol characteristic '
                                          'of endocannabinoids"',
                                          'False, "Ester group found but fatty '
                                          'acid chain too short or not '
                                          'sufficiently unsaturated"',
                                          'True, "Contains indole core with '
                                          'acyl side chain characteristic of '
                                          'synthetic cannabinoids"',
                                          'True, "Contains indole core '
                                          'characteristic of some synthetic '
                                          'cannabinoids"',
                                          'True, "Contains naphthoylindole '
                                          'structure characteristic of '
                                          'synthetic cannabinoids"',
                                          'False, "No characteristic '
                                          'cannabinoid structural features '
                                          'found"'],
                           'returns_count': 10,
                           'complexity': 4.818868912444421},
    'message': '\n'
               'Attempt failed: F1 score of 0.002892611787393034 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)NCCO NAME: '
               'oleoyl ethanolamide REASON: CORRECT Contains long-chain fatty '
               'acid amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: C(CCC)C/C=C\\C/C=C\\C/C=C\\CC1C(CCCC(NCCO)=O)O1 '
               'NAME: N-[(8Z,11Z,14Z)-5,6-epoxyicosatrienoyl]ethanolamine '
               'REASON: CORRECT Contains long-chain fatty acid amide linked to '
               'ethanolamine characteristic of endocannabinoids\n'
               ' * SMILES: CCCCCC\\C=C/CCCCCCCC(=O)NCCO NAME: palmitoleoyl '
               'ethanolamide REASON: CORRECT Contains long-chain fatty acid '
               'amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: C(CCC)CC1C(C/C=C\\C/C=C\\C/C=C\\CCCC(NCCO)=O)O1 '
               'NAME: N-[(5Z,8Z,11Z)-14,15-epoxyicosatrienoyl]ethanolamine '
               'REASON: CORRECT Contains long-chain fatty acid amide linked to '
               'ethanolamine characteristic of endocannabinoids\n'
               ' * SMILES: C(CCC)C/C=C\\C/C=C\\CC1C(C/C=C\\CCCC(NCCO)=O)O1 '
               'NAME: N-[(5Z,11Z,14Z)-8,9-epoxyicosatrienoyl]ethanolamine '
               'REASON: CORRECT Contains long-chain fatty acid amide linked to '
               'ethanolamine characteristic of endocannabinoids\n'
               ' * SMILES: '
               'O=C(O[C@@H]([C@@H](O)[C@H](O)CO)CO)C(=CC(C(O)C(=CC(C(O)C(=CC(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)C(=CC(CC(CC)C)C)C)C)C)C)C)C)C '
               'NAME: Roselipin 3E REASON: CORRECT Contains long-chain fatty '
               'acid ester linked to glycerol characteristic of '
               'endocannabinoids\n'
               ' * SMILES: '
               'O=C(O[C@@H]([C@H](O)[C@H](O)CO)CO)C(=CC(C(O)C(=CC(C(O)C(=CC(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)C(=CC(CC(CC)C)C)C)C)C)C)C)C)C '
               'NAME: Roselipin 3D REASON: CORRECT Contains long-chain fatty '
               'acid ester linked to glycerol characteristic of '
               'endocannabinoids\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)NCCO NAME: palmitoyl '
               'ethanolamide REASON: CORRECT Contains long-chain fatty acid '
               'amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: C(CCCCCCCCCCCCC/C=C\\CCCCCCCC)(NCCO)=O NAME: '
               'N-(15Z-tetracosenoyl)ethanolamine REASON: CORRECT Contains '
               'long-chain fatty acid amide linked to ethanolamine '
               'characteristic of endocannabinoids\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)NCCO NAME: '
               'anandamide REASON: CORRECT Contains long-chain fatty acid '
               'amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: '
               'O=C(O[C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)/C(=C/[C@@H]([C@H](O)/C(=C/[C@@H]([C@H](O)/C(=C/[C@@H]([C@H](O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)/C(=C/[C@H](C[C@H](CC)C)C)/C)C)/C)C)/C)C)/C '
               'NAME: TMC-171A REASON: CORRECT Contains long-chain fatty acid '
               'ester linked to glycerol characteristic of endocannabinoids\n'
               ' * SMILES: C(CCCO)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(NCCO)=O '
               'NAME: N-(20-hydroxyarachidonoyl)ethanolamine REASON: CORRECT '
               'Contains long-chain fatty acid amide linked to ethanolamine '
               'characteristic of endocannabinoids\n'
               'False positives: SMILES: '
               'S(=O)(=O)(CC[C@@H]1NC(=O)[C@H](NC(=O)C(N(C(=O)CC[C@@H](NC([C@H]([C@@H](NC([C@@H](NC(C[C@@H](NC1=O)C(=O)O)=O)CCCN=C(N)N)=O)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)C)=O)C(=O)O)C)=C)C)C '
               'NAME: [D-Asp3]MC-M(O2)R REASON: WRONGLY CLASSIFIED Contains '
               'long-chain fatty acid amide linked to ethanolamine '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: '
               '(2S)-2-amino-3-({hydroxy[(2R)-2-[(11Z,14Z)-icosa-11,14-dienoyloxy]-3-(tetracosanoyloxy)propoxy]phosphoryl}oxy)propanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains long-chain fatty acid '
               'ester linked to glycerol characteristic of endocannabinoids\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O)[H])[H])(CC[C@@]4([C@@H](CCC(NCC(O)=O)=O)C)[H])[H])C)O)[H])C '
               'NAME: glycodeoxycholic acid REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid amide linked to ethanolamine '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'O(P(=O)(OCCNC(=O)CCCCCCCCCCCCCCC)O)C[C@H](OC(CCCCCCC/C=C\\CCCCCCCC)=O)COC(CCCCCCC/C=C\\CCCCCCCC)=O '
               'NAME: '
               'N-palmitoyl-1,2-dioleoyl-sn-glycero-3-phosphoethanolamine '
               'REASON: WRONGLY CLASSIFIED Contains long-chain fatty acid '
               'amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: '
               'CC(C)C[C@@H](C(=O)O)NC(=O)C1=C(C=C(C=C1)NC[C@H](CS)N)C2=CC=CC3=CC=CC=C32 '
               'NAME: '
               '(2S)-2-[[[4-[[(2R)-2-amino-3-mercaptopropyl]amino]-2-(1-naphthalenyl)phenyl]-oxomethyl]amino]-4-methylpentanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains long-chain fatty acid '
               'amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](O)COC(=O)CCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)([O-])=O '
               'NAME: PC(19:3(10Z,13Z,16Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCC/C=C\\C/C=C\\CCCC)C[C@@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: '
               'TG(17:2(9Z,12Z)/20:4(5Z,8Z,11Z,14Z)/20:4(5Z,8Z,11Z,14Z))[iso3] '
               'REASON: WRONGLY CLASSIFIED Contains long-chain fatty acid '
               'ester linked to glycerol characteristic of endocannabinoids\n'
               ' * SMILES: '
               'O=C1NCCC(O)C2NC(=O)C(C2=O)=C(O)C=C[C@H]3[C@H](CC=C1)[C@@H]4[C@H]([C@@H]5[C@H]([C@@H](CC)C[C@@H]5C4)C)[C@H](C3)O '
               'NAME: Dihydromaltophilin REASON: WRONGLY CLASSIFIED Contains '
               'long-chain fatty acid amide linked to ethanolamine '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCCCC)C[C@H](OC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: TG(22:0/20:4(8Z,11Z,14Z,17Z)/20:4(5Z,8Z,11Z,14Z)) '
               'REASON: WRONGLY CLASSIFIED Contains long-chain fatty acid '
               'ester linked to glycerol characteristic of endocannabinoids\n'
               ' * SMILES: '
               'OC12C(C(O)(CC1)C(O)(C3OC(=O)C(=C(C3)C)C)C)(CCC4C2CC(O)C5(O)C4(C)C(=O)C=CC5O)C '
               'NAME: Withaperuvin B REASON: WRONGLY CLASSIFIED Contains '
               'long-chain fatty acid ester linked to glycerol characteristic '
               'of endocannabinoids\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CC=CCCCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d40:2) REASON: WRONGLY CLASSIFIED Contains long-chain '
               'fatty acid amide linked to ethanolamine characteristic of '
               'endocannabinoids\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])O '
               'NAME: DG(20:2(11Z,14Z)/18:1(11Z)/0:0) REASON: WRONGLY '
               'CLASSIFIED Contains long-chain fatty acid ester linked to '
               'glycerol characteristic of endocannabinoids\n'
               ' * SMILES: '
               'C(CCCCCC(CC)C)CCCC[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCC)=O)CO '
               'NAME: N-pentacosanoyl-14-methylhexadecasphinganine REASON: '
               'WRONGLY CLASSIFIED Contains long-chain fatty acid amide linked '
               'to ethanolamine characteristic of endocannabinoids\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)C(O)CCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyhexadecanoyl)eicosasphinganine REASON: '
               'WRONGLY CLASSIFIED Contains long-chain fatty acid amide linked '
               'to ethanolamine characteristic of endocannabinoids\n'
               ' * SMILES: O=C(N1[C@@H](CCC1)C(O)=O)CCCCCCCCCCCCCCC NAME: '
               'N-Palmitoyl proline REASON: WRONGLY CLASSIFIED Contains '
               'long-chain fatty acid amide linked to ethanolamine '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCC(=O)C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)(O)(O)=O '
               'NAME: PA(6 keto-PGF1alpha/14:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCC)=O)(OC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)[H])(O)=O '
               'NAME: PI(16:0/22:5(7Z,10Z,13Z,16Z,19Z)) REASON: WRONGLY '
               'CLASSIFIED Contains long-chain fatty acid ester linked to '
               'glycerol characteristic of endocannabinoids\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(18:0/20:1(11Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'WRONGLY CLASSIFIED Contains long-chain fatty acid ester linked '
               'to glycerol characteristic of endocannabinoids\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OCC(CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC NAME: '
               '1-stearoyl-2-oleoylglycerol REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PI(16:1(9Z)/17:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(18:1(9Z)/18:3(9Z,12Z,15Z)) REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               '[C@](COC(=O)CCCCCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCC)([H])COP(OCCN)(O)=O '
               'NAME: PE(19:0/15:0) REASON: WRONGLY CLASSIFIED Contains '
               'long-chain fatty acid ester linked to glycerol characteristic '
               'of endocannabinoids\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: PC(24:0/18:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(19:0/0:0) REASON: WRONGLY CLASSIFIED Contains '
               'long-chain fatty acid ester linked to glycerol characteristic '
               'of endocannabinoids\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(20:0/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED '
               'Contains long-chain fatty acid ester linked to glycerol '
               'characteristic of endocannabinoids\n'
               'False negatives: SMILES: '
               'CCCCCCC(C)(C)C=1C=CC([C@@]2(C[C@](CC[C@]2(CCCO)[H])([H])O)[H])=C(C1)O '
               'NAME: CP-55940 REASON: MISSED No characteristic cannabinoid '
               'structural features found\n'
               ' * SMILES: '
               '[H][C@@]12CCC(C)=C[C@@]1([H])c1c(O)cc(CCCCC)cc1OC2(C)C NAME: '
               'Delta(9)-tetrahydrocannabinol REASON: MISSED No characteristic '
               'cannabinoid structural features found\n'
               ' * SMILES: '
               '[H]C(CO)(CO)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC NAME: '
               '2-arachidonoylglycerol REASON: MISSED No characteristic '
               'cannabinoid structural features found\n'
               ' * SMILES: O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO '
               'NAME: MG(0:0/20:4(8Z,11Z,14Z,17Z)/0:0) REASON: MISSED No '
               'characteristic cannabinoid structural features found\n'
               ' * SMILES: '
               '[H][C@]1(C=C(C)CC[C@H]1C(C)=C)c1c(O)cc(CCCCC)c(C(O)=O)c1O '
               'NAME: cannabidiolic acid REASON: MISSED No characteristic '
               'cannabinoid structural features found\n'
               ' * SMILES: '
               'O(C(C(O)([2H])[2H])(C(O)([2H])[2H])[2H])C(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: 2-arachidonoyl glycerol-d5 REASON: MISSED No '
               'characteristic cannabinoid structural features found\n'
               ' * SMILES: CCCCCc1cc(O)c(C\\C=C(/C)CCC=C(C)C)c(O)c1C(O)=O '
               'NAME: cannabigerolic acid REASON: MISSED No characteristic '
               'cannabinoid structural features found\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO '
               'NAME: MG(0:0/20:3(11Z,14Z,17Z)/0:0) REASON: MISSED No '
               'characteristic cannabinoid structural features found\n'
               ' * SMILES: C1(=C(C=C(CCCCC)C=C1O)O)C/C=C(/CCC=C(C)C)\\C NAME: '
               'cannabigerol REASON: MISSED No characteristic cannabinoid '
               'structural features found\n'
               ' * SMILES: '
               '[H][C@]1(CCC(C)=C[C@H]1C1=C(O)C=C(CCCCC)C=C1O)C(C)=C NAME: '
               'cannabidiol REASON: MISSED No characteristic cannabinoid '
               'structural features found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCOC(=O)CC(C1=CC=CC=C1Cl)NC2=NC(=NC(=N2)N3CCOCC3)N4CCOCC4',
                                     'name': '3-[[4,6-bis(4-morpholinyl)-1,3,5-triazin-2-yl]amino]-3-(2-chlorophenyl)propanoic '
                                             'acid ethyl ester',
                                     'reason': 'No characteristic cannabinoid '
                                               'structural features found'},
                                 {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@]1(C=2C=3OC(=CC(=O)C3C(O)=CC2O)C4=CC(O)=C(O)C=C4)[H])CO)[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)CO',
                                     'name': "2''-O-beta-L-Galactopyranosylorientin",
                                     'reason': 'No characteristic cannabinoid '
                                               'structural features found'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](NC(C)=O)[C@@H](O[C@H](CO)[C@H]2O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)O[C@@H]2[C@@H](O)[C@@H](O)O[C@H](CO)[C@@H]2O)[C@@H](O)[C@H](O)[C@@H]1O',
                                     'name': 'beta-D-GalpNAc-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->3)-alpha-D-Galp',
                                     'reason': 'Amide group found but fatty '
                                               'acid chain too short or not '
                                               'sufficiently unsaturated'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CCC(F)(F)F)O[C@H]1CN(C)CC3=CC4=C(C=C3)OCO4)[C@@H](C)CO',
                                     'name': 'N-[(2R,3S)-2-[[1,3-benzodioxol-5-ylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-4,4,4-trifluorobutanamide',
                                     'reason': 'Amide group found but fatty '
                                               'acid chain too short or not '
                                               'sufficiently unsaturated'},
                                 {   'smiles': 'C1CC(C1)C(=O)N[C@@H]2C=C[C@H](O[C@H]2CO)CC(=O)NCCCN3CCOCC3',
                                     'name': 'N-[(2R,3R,6R)-2-(hydroxymethyl)-6-[2-[3-(4-morpholinyl)propylamino]-2-oxoethyl]-3,6-dihydro-2H-pyran-3-yl]cyclobutanecarboxamide',
                                     'reason': 'Amide group found but fatty '
                                               'acid chain too short or not '
                                               'sufficiently unsaturated'},
                                 {   'smiles': 'O=C1O[C@@H](CC[C@H](O)C=C[C@H](C1)O)C',
                                     'name': 'Decarestrictine C1',
                                     'reason': 'No characteristic cannabinoid '
                                               'structural features found'},
                                 {   'smiles': '[H]P(O)(=O)OP([H])(O)=O',
                                     'name': 'diphosphonic acid',
                                     'reason': 'No characteristic cannabinoid '
                                               'structural features found'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)C3=NOC(=C3)C4=CC=CC=C4)[C@H](C)CO',
                                     'name': 'N-[[(8S,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N-methyl-5-phenyl-3-isoxazolecarboxamide',
                                     'reason': 'Amide group found but fatty '
                                               'acid chain too short or not '
                                               'sufficiently unsaturated'},
                                 {   'smiles': 'OCCCCCCC[C@@H](O)CC(O)=O',
                                     'name': '(3R)-3,10-dihydroxydecanoic acid',
                                     'reason': 'No characteristic cannabinoid '
                                               'structural features found'},
                                 {   'smiles': 'O=C1C2=C(OC3=C1C(=CC(=C3)CO)CO)C=C(O)C=C2O',
                                     'name': 'Phomoxanthone J',
                                     'reason': 'No characteristic cannabinoid '
                                               'structural features found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)NCCO',
                                      'name': 'oleoyl ethanolamide',
                                      'reason': 'Amide group found but fatty '
                                                'acid chain too short or not '
                                                'sufficiently unsaturated'},
                                  {   'smiles': 'CCCCCCC(C)(C)C=1C=CC([C@@]2(C[C@](CC[C@]2(CCCO)[H])([H])O)[H])=C(C1)O',
                                      'name': 'CP-55940',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': 'CCCCCC\\C=C/CCCCCCCC(=O)NCCO',
                                      'name': 'palmitoleoyl ethanolamide',
                                      'reason': 'Amide group found but fatty '
                                                'acid chain too short or not '
                                                'sufficiently unsaturated'},
                                  {   'smiles': '[H][C@@]12CCC(C)=C[C@@]1([H])c1c(O)cc(CCCCC)cc1OC2(C)C',
                                      'name': 'Delta(9)-tetrahydrocannabinol',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': '[H]C(CO)(CO)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                      'name': '2-arachidonoylglycerol',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': 'O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO',
                                      'name': 'MG(0:0/20:4(8Z,11Z,14Z,17Z)/0:0)',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': '[H][C@]1(C=C(C)CC[C@H]1C(C)=C)c1c(O)cc(CCCCC)c(C(O)=O)c1O',
                                      'name': 'cannabidiolic acid',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': 'O(C(C(O)([2H])[2H])(C(O)([2H])[2H])[2H])C(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC',
                                      'name': '2-arachidonoyl glycerol-d5',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': 'CCCCCc1cc(O)c(C\\C=C(/C)CCC=C(C)C)c(O)c1C(O)=O',
                                      'name': 'cannabigerolic acid',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'},
                                  {   'smiles': 'O(C(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO',
                                      'name': 'MG(0:0/20:3(11Z,14Z,17Z)/0:0)',
                                      'reason': 'No characteristic cannabinoid '
                                                'structural features found'}],
    'attempt': 2,
    'reasoning': 'Analyzing the previous program and the outcomes, it appears '
                 'that the classifier failed to correctly identify several '
                 'known cannabinoids, particularly phytocannabinoids like '
                 'Delta(9)-tetrahydrocannabinol (THC), cannabidiol (CBD), '
                 'cannabigerol, and their acidic counterparts. This is likely '
                 'because the SMARTS patterns for phytocannabinoids were too '
                 "specific and didn't account for variations in the core "
                 'structures and side chains of these compounds.\n'
                 '\n'
                 'Additionally, the classifier incorrectly identified many '
                 'non-cannabinoid molecules as cannabinoids (false positives). '
                 'This happened because the patterns for endocannabinoids were '
                 'too broad—any molecule with a long-chain fatty acid linked '
                 'to ethanolamine or glycerol was classified as a cannabinoid, '
                 'even if it lacked other characteristic features.\n'
                 '\n'
                 'To improve the classifier, the following changes are '
                 'necessary:\n'
                 '\n'
                 '1. **Expand the SMARTS patterns for phytocannabinoids** to '
                 'capture the core dibenzopyran ring system common to many '
                 'cannabinoids, allowing for variations in side chains and '
                 'substitutions.\n'
                 '\n'
                 '2. **Refine the patterns for endocannabinoids** by ensuring '
                 'that the fatty acid chains are not only long but also '
                 'polyunsaturated, reflecting the nature of endocannabinoids '
                 'like anandamide and 2-arachidonoylglycerol.\n'
                 '\n'
                 '3. **Enhance synthetic cannabinoid detection** by including '
                 'additional patterns for commonly found scaffolds, such as '
                 'indole and naphthoylindole cores.\n'
                 '\n'
                 '4. **Implement stricter criteria** to avoid false positives, '
                 'such as requiring specific chain lengths, degrees of '
                 'unsaturation, and the presence of key functional groups '
                 'unique to cannabinoids.\n'
                 '\n'
                 'By making these adjustments, the classifier should more '
                 'accurately distinguish cannabinoids from non-cannabinoids, '
                 'reducing both false negatives and false positives.\n'
                 '\n'
                 'Here is the updated code implementing these improvements:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 5372,
    'num_true_negatives': 136890,
    'num_false_negatives': 30,
    'num_negatives': None,
    'precision': 0.001486988847583643,
    'recall': 0.21052631578947367,
    'f1': 0.0029531192321889995,
    'accuracy': 0.962037947997189,
    'negative_predictive_value': 0.9997808939526731}