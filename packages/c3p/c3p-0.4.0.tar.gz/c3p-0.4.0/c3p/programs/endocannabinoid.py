"""
Classifies: CHEBI:67197 endocannabinoid
"""
"""
Classifies: Endocannabinoids – A class of cannabinoids present in mammalian biological fluids
and tissues that activate cannabinoid receptors.
This classifier uses improved heuristics:
  • Excludes molecules with phosphorus.
  • Requires that the molecule have exactly one acyl linkage:
       – For N‐acylethanolamines: exactly one amide (C(=O)N) with an ethanolamide fragment (C(=O)NCCO) and exactly one nitrogen.
       – For monoacylglycerols/glyceryl ethers: a glycerol fragment that is directly linked (via an ester or an ether) to one long fatty acyl chain.
  • In addition, the overall molecule must be “lipid‐like” with at least 18 carbons, at least 15 rotatable bonds,
    and a molecular weight between 250 and 900 Da.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_endocannabinoid(smiles: str):
    """
    Determines whether a molecule is an endocannabinoid based on its SMILES string.
    Endocannabinoids are expected to contain either:
      (a) an N‐acylethanolamine head group defined by an amide bond and an ethanolamine fragment (SMARTS: C(=O)NCCO) 
          with exactly one amide and one nitrogen in the whole molecule, or
      (b) a monoacylglycerol/glyceryl ether head group defined by the presence of a glycerol fragment (SMARTS: OC(CO)CO)
          that is directly linked to a long fatty chain via either an ester bond or an ether linkage.
    In addition, molecules with phosphorus are excluded and the overall molecule’s size must be “lipid‐like”
    (at least 18 carbons, at least 15 rotatable bonds, molecular weight between 250 and 900 Da).

    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as an endocannabinoid, False otherwise.
        str: Reason for the classification decision.
    """
    # Parse SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Exclude any molecule containing phosphorus (atomic number 15)
    if any(atom.GetAtomicNum() == 15 for atom in mol.GetAtoms()):
        return False, "Contains phosphorus; likely a phospholipid rather than an endocannabinoid"

    # --- Define SMARTS patterns ---
    # Ethanolamide head group: should include a C(=O)NCCO fragment.
    ethanolamide_pat = Chem.MolFromSmarts("C(=O)NCCO")
    # A general amide group for counting (C(=O)N)
    amide_pat = Chem.MolFromSmarts("C(=O)N")
    # Glycerol head group (we use a relaxed pattern that ignores chirality): O[C@@H](CO)CO, written without stereo here.
    glycerol_pat = Chem.MolFromSmarts("OC(CO)CO")
    # Ester (acyl) bond pattern: C(=O)O
    ester_pat = Chem.MolFromSmarts("C(=O)O")

    # Count total nitrogen (for ethanolamide, we expect exactly 1)
    nN = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)

    head_valid = False
    head_type = None  # "ethanolamide" or "glycerol"
    head_reason = ""

    # --- Strategy A: Ethanolamide head group ---
    eth_matches = mol.GetSubstructMatches(ethanolamide_pat)
    if eth_matches:
        # To be an ethanolamide, we expect (ideally) one ethanolamide fragment,
        # exactly one amide group and one nitrogen (the head group nitrogen).
        amide_matches = mol.GetSubstructMatches(amide_pat)
        if len(eth_matches) == 1 and len(amide_matches) == 1 and nN == 1:
            head_valid = True
            head_type = "ethanolamide"
            head_reason = "Ethanolamide head group found with correct amide and nitrogen counts (1 each)"
        else:
            head_reason = (f"Ethanolamide fragment count = {len(eth_matches)}, amide count = {len(amide_matches)}, "
                           f"and nitrogen count = {nN} (expected 1, 1, and 1 respectively)")

    # --- Strategy B: Glycerol-based head group (monoacylglycerol or glyceryl ether) ---
    if not head_valid:
        gly_matches = mol.GetSubstructMatches(glycerol_pat)
        if gly_matches:
            # For glycerol-based endocannabinoids,
            # we require that one of the glycerol fragments is linked to exactly one acyl chain.
            # We'll check two possibilities:
            # Option 1. The acyl chain is attached as an ester:
            ester_matches = mol.GetSubstructMatches(ester_pat)
            acyl_count = 0
            # Count ester bonds that appear to connect a glycerol fragment to an acyl chain.
            for gmatch in gly_matches:
                # gmatch is a tuple of atom indices corresponding to the glycerol fragment.
                gset = set(gmatch)
                for ematch in ester_matches:
                    # In an ester match, the oxygen (the second atom) is the one connecting to the alcohol.
                    # If that oxygen is part of our glycerol fragment, then count that ester as the acyl linkage.
                    if ematch[1] in gset:
                        acyl_count += 1
            if acyl_count == 1 and nN == 0:
                head_valid = True
                head_type = "glycerol (ester)"
                head_reason = "Glycerol head group found with one ester acyl linkage and no nitrogen"
            else:
                # Option 2. If no ester bond was found from the glycerol fragment, try to detect an ether linkage.
                # We check each glycerol fragment: for each oxygen atom in the fragment, consider neighbors
                # not in the fragment. If one such neighbor is carbon and is part of a long alkyl chain, count it.
                def count_ether_acyl(gmatch):
                    count = 0
                    for idx in gmatch:
                        atom = mol.GetAtomWithIdx(idx)
                        if atom.GetSymbol() == "O":
                            for nbr in atom.GetNeighbors():
                                if nbr.GetIdx() not in gmatch and nbr.GetAtomicNum() == 6:
                                    # Count carbons in the branch starting from nbr (simple DFS, not counting rings)
                                    seen = set()
                                    stack = [nbr]
                                    branch_carbons = 0
                                    while stack:
                                        a = stack.pop()
                                        if a.GetIdx() in seen:
                                            continue
                                        seen.add(a.GetIdx())
                                        if a.GetAtomicNum() == 6:
                                            branch_carbons += 1
                                        # Only follow non-oxygen neighbors to stay in the hydrocarbon chain
                                        for nn in a.GetNeighbors():
                                            if nn.GetIdx() not in seen and nn.GetAtomicNum() == 6:
                                                stack.append(nn)
                                    # If the branch has at least 6 carbons, consider it an acyl chain.
                                    if branch_carbons >= 6:
                                        count += 1
                    return count

                ether_acyl_total = 0
                for gmatch in gly_matches:
                    ether_count = count_ether_acyl(gmatch)
                    ether_acyl_total += ether_count
                if ether_acyl_total == 1 and nN == 0:
                    head_valid = True
                    head_type = "glycerol (ether)"
                    head_reason = "Glycerol head group found with one ether-linked acyl chain and no nitrogen"
                else:
                    head_reason = (f"Glycerol head group found but acyl linkage count from ester bonds = {acyl_count} "
                                   f"and ether-linked count = {ether_acyl_total} (expected exactly 1) "
                                   f"with nitrogen count = {nN} (expected 0)")

    if not head_valid:
        return False, "No valid head group found. " + head_reason

    # --- Global lipid criteria ---
    # Total carbon atoms (require at least 18)
    nC = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if nC < 18:
        return False, f"Too few carbon atoms ({nC}); expected at least 18 for a fatty acyl chain."

    # At least 15 rotatable bonds
    n_rot = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rot < 15:
        return False, f"Too few rotatable bonds ({n_rot}); expected at least 15 for a flexible lipid chain."

    # Molecular weight in [250, 900] Da
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 250:
        return False, f"Molecular weight ({mw:.1f} Da) is too low for an endocannabinoid."
    if mw > 900:
        return False, f"Molecular weight ({mw:.1f} Da) is too high for an endocannabinoid."

    overall_reason = (f"Valid head group ({head_reason}), no phosphorus, exactly one acyl linkage "
                      f"({head_type} based), {nC} carbons, {n_rot} rotatable bonds and a molecular weight of {mw:.1f} Da "
                      "indicate a lipid‐like structure typical of an endocannabinoid.")
    
    return True, overall_reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:67197',
                          'name': 'endocannabinoid',
                          'definition': 'A class of cannabinoids present in '
                                        'mammalian biological fluids and '
                                        'tissues that activate cannabinoid '
                                        'receptors.',
                          'parents': ['CHEBI:18059', 'CHEBI:67194'],
                          'xrefs': ['Patent:US2012165388'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 123,
                           'log_lines_of_code': 4.812184355372417,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 8,
                                                 9,
                                                 9,
                                                 9,
                                                 9,
                                                 9,
                                                 10,
                                                 10,
                                                 11,
                                                 10,
                                                 10,
                                                 11,
                                                 10,
                                                 10,
                                                 11,
                                                 12,
                                                 9,
                                                 9,
                                                 10,
                                                 5,
                                                 0,
                                                 0,
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
                                                 2,
                                                 0,
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
                           'max_indent': 12,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcNumRotatableBonds',
                                                 'append',
                                                 'add',
                                                 'MolFromSmarts',
                                                 'GetSymbol',
                                                 'pop',
                                                 'GetAtoms',
                                                 'CalcExactMolWt',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetIdx'],
                           'methods_called_count': 14,
                           'smarts_strings': [   'C(=O)N',
                                                 'C(=O)O',
                                                 'OC(CO)CO',
                                                 'C(=O)NCCO'],
                           'smarts_strings_count': 4,
                           'defs': [   'is_endocannabinoid(smiles: str):',
                                       'count_ether_acyl(gmatch):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains phosphorus; likely '
                                          'a phospholipid rather than an '
                                          'endocannabinoid"',
                                          'count',
                                          'False, "No valid head group found. '
                                          '" + head_reason',
                                          'False, f"Too few carbon atoms '
                                          '({nC}); expected at least 18 for a '
                                          'fatty acyl chain."',
                                          'False, f"Too few rotatable bonds '
                                          '({n_rot}); expected at least 15 for '
                                          'a flexible lipid chain."',
                                          'False, f"Molecular weight ({mw:.1f} '
                                          'Da) is too low for an '
                                          'endocannabinoid."',
                                          'False, f"Molecular weight ({mw:.1f} '
                                          'Da) is too high for an '
                                          'endocannabinoid."',
                                          'True, overall_reason'],
                           'returns_count': 9,
                           'complexity': 8.362436871074483},
    'message': '\n'
               'Attempt failed: F1 score of 0.06810035842293907 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O(C(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)C(CO)CO NAME: '
               'MG(0:0/20:2(11Z,14Z)/0:0) REASON: CORRECT Valid head group '
               '(Glycerol head group found with correct ester and nitrogen '
               'counts (1 and 0, respectively)), no phosphorus, exactly one '
               'acyl linkage, 23 carbons, 19 rotatable bonds and a molecular '
               'weight of 382.3 Da indicate a lipid‐like structure typical of '
               'an endocannabinoid.\n'
               ' * SMILES: CCCCCC\\C=C/CCCCCCCC(=O)NCCO NAME: palmitoleoyl '
               'ethanolamide REASON: CORRECT Valid head group (Ethanolamide '
               'head group found with correct amide and nitrogen counts (1 '
               'each)), no phosphorus, exactly one acyl linkage, 18 carbons, '
               '15 rotatable bonds and a molecular weight of 297.3 Da indicate '
               'a lipid‐like structure typical of an endocannabinoid.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\CCCCCCCC)C(CO)CO NAME: '
               'MG(0:0/20:1(11Z)/0:0) REASON: CORRECT Valid head group '
               '(Glycerol head group found with correct ester and nitrogen '
               'counts (1 and 0, respectively)), no phosphorus, exactly one '
               'acyl linkage, 23 carbons, 20 rotatable bonds and a molecular '
               'weight of 384.3 Da indicate a lipid‐like structure typical of '
               'an endocannabinoid.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO '
               'NAME: MG(0:0/20:3(11Z,14Z,17Z)/0:0) REASON: CORRECT Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 23 carbons, 18 rotatable bonds and a '
               'molecular weight of 380.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: C(CCCO)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(NCCO)=O '
               'NAME: N-(20-hydroxyarachidonoyl)ethanolamine REASON: CORRECT '
               'Valid head group (Ethanolamide head group found with correct '
               'amide and nitrogen counts (1 each)), no phosphorus, exactly '
               'one acyl linkage, 22 carbons, 17 rotatable bonds and a '
               'molecular weight of 363.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: CCCCCC=CCC=CCC=CCC=CCCCC(=O)OC(CO)CO NAME: '
               'eicosa-5,8,11,14-tetraenoic acid 1,3-dihydroxypropan-2-yl '
               'ester REASON: CORRECT Valid head group (Glycerol head group '
               'found with correct ester and nitrogen counts (1 and 0, '
               'respectively)), no phosphorus, exactly one acyl linkage, 23 '
               'carbons, 17 rotatable bonds and a molecular weight of 378.3 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)NCCO NAME: oleoyl '
               'ethanolamide REASON: CORRECT Valid head group (Ethanolamide '
               'head group found with correct amide and nitrogen counts (1 '
               'each)), no phosphorus, exactly one acyl linkage, 20 carbons, '
               '17 rotatable bonds and a molecular weight of 325.3 Da indicate '
               'a lipid‐like structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               '[H]C(CO)(CO)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC NAME: '
               '2-arachidonoylglycerol REASON: CORRECT Valid head group '
               '(Glycerol head group found with correct ester and nitrogen '
               'counts (1 and 0, respectively)), no phosphorus, exactly one '
               'acyl linkage, 23 carbons, 17 rotatable bonds and a molecular '
               'weight of 378.3 Da indicate a lipid‐like structure typical of '
               'an endocannabinoid.\n'
               ' * SMILES: C(CCC)C/C=C\\C/C=C\\CC1C(C/C=C\\CCCC(NCCO)=O)O1 '
               'NAME: N-[(5Z,11Z,14Z)-8,9-epoxyicosatrienoyl]ethanolamine '
               'REASON: CORRECT Valid head group (Ethanolamide head group '
               'found with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 22 carbons, 16 rotatable '
               'bonds and a molecular weight of 363.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O(C(C(O)([2H])[2H])(C(O)([2H])[2H])[2H])C(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: 2-arachidonoyl glycerol-d5 REASON: CORRECT Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 23 carbons, 17 rotatable bonds and a '
               'molecular weight of 383.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O(C(CO)CO)C(=O)CCC/C=C\\C/C=C\\C=C\\[C@@H](O)C/C=C\\CCCCC '
               'NAME: 12-HETE-G REASON: CORRECT Valid head group (Glycerol '
               'head group found with correct ester and nitrogen counts (1 and '
               '0, respectively)), no phosphorus, exactly one acyl linkage, 23 '
               'carbons, 17 rotatable bonds and a molecular weight of 394.3 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: C(CCCCCCCCCCCCC/C=C\\CCCCCCCC)(NCCO)=O NAME: '
               'N-(15Z-tetracosenoyl)ethanolamine REASON: CORRECT Valid head '
               'group (Ethanolamide head group found with correct amide and '
               'nitrogen counts (1 each)), no phosphorus, exactly one acyl '
               'linkage, 26 carbons, 23 rotatable bonds and a molecular weight '
               'of 409.4 Da indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: C(CCC)CC1C(C/C=C\\C/C=C\\C/C=C\\CCCC(NCCO)=O)O1 '
               'NAME: N-[(5Z,8Z,11Z)-14,15-epoxyicosatrienoyl]ethanolamine '
               'REASON: CORRECT Valid head group (Ethanolamide head group '
               'found with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 22 carbons, 16 rotatable '
               'bonds and a molecular weight of 363.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)NCCO NAME: palmitoyl '
               'ethanolamide REASON: CORRECT Valid head group (Ethanolamide '
               'head group found with correct amide and nitrogen counts (1 '
               'each)), no phosphorus, exactly one acyl linkage, 18 carbons, '
               '16 rotatable bonds and a molecular weight of 299.3 Da indicate '
               'a lipid‐like structure typical of an endocannabinoid.\n'
               ' * SMILES: O(C(CO)CO)C(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC '
               'NAME: MG(0:0/20:3(5Z,8Z,11Z)/0:0) REASON: CORRECT Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 23 carbons, 18 rotatable bonds and a '
               'molecular weight of 380.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O[C@@H](CCCCC)/C=C/C=C\\C/C=C\\C/C=C\\CCCC(OC(CO)CO)=O NAME: '
               '15-HETE-G REASON: CORRECT Valid head group (Glycerol head '
               'group found with correct ester and nitrogen counts (1 and 0, '
               'respectively)), no phosphorus, exactly one acyl linkage, 23 '
               'carbons, 17 rotatable bonds and a molecular weight of 394.3 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)NCCO NAME: '
               'anandamide REASON: CORRECT Valid head group (Ethanolamide head '
               'group found with correct amide and nitrogen counts (1 each)), '
               'no phosphorus, exactly one acyl linkage, 22 carbons, 16 '
               'rotatable bonds and a molecular weight of 347.3 Da indicate a '
               'lipid‐like structure typical of an endocannabinoid.\n'
               ' * SMILES: O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO '
               'NAME: MG(0:0/20:4(8Z,11Z,14Z,17Z)/0:0) REASON: CORRECT Valid '
               'head group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 23 carbons, 17 rotatable bonds and a '
               'molecular weight of 378.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: C(CCC)C/C=C\\C/C=C\\C/C=C\\CC1C(CCCC(NCCO)=O)O1 '
               'NAME: N-[(8Z,11Z,14Z)-5,6-epoxyicosatrienoyl]ethanolamine '
               'REASON: CORRECT Valid head group (Ethanolamide head group '
               'found with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 22 carbons, 16 rotatable '
               'bonds and a molecular weight of 363.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               'False positives: SMILES: '
               'O=C(O)C(CC(=O)OC(C(OC(=O)CC(C(=O)O)CC(=O)O)CC(CC(O)CCCCC(O)C(O)C(O)CNC(=O)C)C)C(CCCC)C)CC(=O)O '
               'NAME: '
               '2-[2-[19-acetamido-6-(3,4-dicarboxybutanoyloxy)-11,16,17,18-tetrahydroxy-5,9-dimethylnonadecan-7-yl]oxy-2-oxoethyl]butanedioic '
               'acid REASON: WRONGLY CLASSIFIED Valid head group (Ethanolamide '
               'head group found with correct amide and nitrogen counts (1 '
               'each)), no phosphorus, exactly one acyl linkage, 35 carbons, '
               '30 rotatable bonds and a molecular weight of 765.4 Da indicate '
               'a lipid‐like structure typical of an endocannabinoid.\n'
               ' * SMILES: O(C(=O)CCCCCCCC=CCCCCCCCCC)C(CO)CO NAME: '
               '1,3-dihydroxypropan-2-yl nonadec-9-enoate REASON: WRONGLY '
               'CLASSIFIED Valid head group (Glycerol head group found with '
               'correct ester and nitrogen counts (1 and 0, respectively)), no '
               'phosphorus, exactly one acyl linkage, 22 carbons, 19 rotatable '
               'bonds and a molecular weight of 370.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O=C(O[C@@H]1C[C@@]2(O)[C@]([C@@H]3C([C@H]4[C@]([C@@H]([C@@H](/C=C/[C@@H](C(C)C)C)C)CC4)(C)CC3)=C[C@@H]2O)(C)CC1)CCCCCCCCCCCCCCCCC '
               'NAME: Erinarol E REASON: WRONGLY CLASSIFIED Valid head group '
               '(Glycerol head group found with correct ester and nitrogen '
               'counts (1 and 0, respectively)), no phosphorus, exactly one '
               'acyl linkage, 46 carbons, 21 rotatable bonds and a molecular '
               'weight of 696.6 Da indicate a lipid‐like structure typical of '
               'an endocannabinoid.\n'
               ' * SMILES: '
               'S(=O)(=O)(O)C[C@@H](NC(=O)C[C@H](O)CCCCCCCCCCCC(C)C)[C@H](O)/C=C/CCCCCCCCCC(C)C '
               'NAME: Flavocristamide A REASON: WRONGLY CLASSIFIED Valid head '
               'group (Ethanolamide head group found with correct amide and '
               'nitrogen counts (1 each)), no phosphorus, exactly one acyl '
               'linkage, 34 carbons, 29 rotatable bonds and a molecular weight '
               'of 617.5 Da indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: '
               'O(C(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)C[C@@H](O)CO '
               'NAME: MG(22:4(7Z,10Z,13Z,16Z)/0:0/0:0) REASON: WRONGLY '
               'CLASSIFIED Valid head group (Glycerol head group found with '
               'correct ester and nitrogen counts (1 and 0, respectively)), no '
               'phosphorus, exactly one acyl linkage, 25 carbons, 19 rotatable '
               'bonds and a molecular weight of 406.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: O=C(C[C@H](CCCCCCCCCCCCCCC)O)O NAME: '
               '(S)-3-hydroxyoctadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Valid head group (Glycerol head group found with correct ester '
               'and nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 18 carbons, 16 rotatable bonds and a '
               'molecular weight of 300.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCCCCC(=O)CC(O)=O)[C@H](O)C[C@H]1O '
               'NAME: bkos#38 REASON: WRONGLY CLASSIFIED Valid head group '
               '(Glycerol head group found with correct ester and nitrogen '
               'counts (1 and 0, respectively)), no phosphorus, exactly one '
               'acyl linkage, 27 carbons, 22 rotatable bonds and a molecular '
               'weight of 486.4 Da indicate a lipid‐like structure typical of '
               'an endocannabinoid.\n'
               ' * SMILES: '
               'O[C@H](CCCCCCCC(OC[C@@H](O)CO)=O)[C@H](O)C/C=C\\CCCCC NAME: '
               'MG(18:1(12Z)-2OH(9,10)/0:0/0:0) REASON: WRONGLY CLASSIFIED '
               'Valid head group (Glycerol head group found with correct ester '
               'and nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 21 carbons, 18 rotatable bonds and a '
               'molecular weight of 388.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: O1OC(CC1C(OO)/C=C/C(OO)CCCCC)/C=C/C=C/CCCC(OC)=O '
               'NAME: Methyl '
               '9,11-epidioxy-12,15-dihydroperoxy-5,7,13-eicosatrienoate '
               'REASON: WRONGLY CLASSIFIED Valid head group (Glycerol head '
               'group found with correct ester and nitrogen counts (1 and 0, '
               'respectively)), no phosphorus, exactly one acyl linkage, 21 '
               'carbons, 15 rotatable bonds and a molecular weight of 414.2 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-stearoyl-sn-glycerol REASON: WRONGLY CLASSIFIED Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 21 carbons, 19 rotatable bonds and a '
               'molecular weight of 358.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: O1C(C1)COC(=O)CCCC=CCC=CCC=CCC=CCCCCC NAME: '
               'O-Arachidonoyl Glycidol REASON: WRONGLY CLASSIFIED Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 23 carbons, 16 rotatable bonds and a '
               'molecular weight of 360.3 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: '
               'C(CCC)C[C@@H](\\C=C\\C=C/C/C=C\\C/C=C\\CCCC(NCC([O-])=O)=O)OO '
               'NAME: '
               'N-[(15S)-hydroperoxy-(5Z,8Z,11Z,13E)-icosatetraenoyl]glycinate '
               'REASON: WRONGLY CLASSIFIED Valid head group (Ethanolamide head '
               'group found with correct amide and nitrogen counts (1 each)), '
               'no phosphorus, exactly one acyl linkage, 22 carbons, 17 '
               'rotatable bonds and a molecular weight of 392.2 Da indicate a '
               'lipid‐like structure typical of an endocannabinoid.\n'
               ' * SMILES: CCCCCCCCC=CCC=CCC=CCCCC(=O)NCCO NAME: '
               'N-(2-hydroxyethyl)eicosa-5,8,11-trienamide REASON: WRONGLY '
               'CLASSIFIED Valid head group (Ethanolamide head group found '
               'with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 22 carbons, 17 rotatable '
               'bonds and a molecular weight of 349.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: O=C(OC)[C@@H](NC(=O)CCCCCCC/C=C\\CCCCCC)CC NAME: '
               'N-[(Z)-hexadec-9-enoyl]-2-aminobutyric acid methyl ester '
               '(C16:1-NABME) REASON: WRONGLY CLASSIFIED Valid head group '
               '(Ethanolamide head group found with correct amide and nitrogen '
               'counts (1 each)), no phosphorus, exactly one acyl linkage, 21 '
               'carbons, 16 rotatable bonds and a molecular weight of 353.3 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: N([C@H](C([O-])=O)CC1=CC=CC=C1)C(CCCCCCCCCCCCCCC)=O '
               'NAME: N-palmitoyl-L-phenylalanine(1-) REASON: WRONGLY '
               'CLASSIFIED Valid head group (Ethanolamide head group found '
               'with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 25 carbons, 18 rotatable '
               'bonds and a molecular weight of 402.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: OC(CCCCC)/C=C/C=C\\C/C=C\\C/C=C\\CCCC(=O)NCCO NAME: '
               '15-HETE-EA REASON: WRONGLY CLASSIFIED Valid head group '
               '(Ethanolamide head group found with correct amide and nitrogen '
               'counts (1 each)), no phosphorus, exactly one acyl linkage, 22 '
               'carbons, 16 rotatable bonds and a molecular weight of 363.3 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCC(=O)CC(O)=O)[C@H](O)C[C@H]1O '
               'NAME: bkos#32 REASON: WRONGLY CLASSIFIED Valid head group '
               '(Glycerol head group found with correct ester and nitrogen '
               'counts (1 and 0, respectively)), no phosphorus, exactly one '
               'acyl linkage, 24 carbons, 19 rotatable bonds and a molecular '
               'weight of 444.3 Da indicate a lipid‐like structure typical of '
               'an endocannabinoid.\n'
               ' * SMILES: '
               'C(CCCCCCCCC(C)C)CCCC(OC[C@]([H])(CO)OCCCCCCCCC1CCC2C(C1)C3C2C4C3CC4)=O '
               'NAME: '
               '1-(14-methyl-pentadecanoyl)-2-(8-[3]-ladderane-octanyl)-sn-glycerol '
               'REASON: WRONGLY CLASSIFIED Valid head group (Glycerol head '
               'group found with correct ester and nitrogen counts (1 and 0, '
               'respectively)), no phosphorus, exactly one acyl linkage, 39 '
               'carbons, 26 rotatable bonds and a molecular weight of 602.5 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: C[C@@H](O)CCCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R,22R)-3,22-dihydroxytricosanoic acid REASON: WRONGLY '
               'CLASSIFIED Valid head group (Glycerol head group found with '
               'correct ester and nitrogen counts (1 and 0, respectively)), no '
               'phosphorus, exactly one acyl linkage, 23 carbons, 21 rotatable '
               'bonds and a molecular weight of 386.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O(CCNC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)C1=CC=CC=C1 '
               'NAME: N-(2-phenoxy-ethyl) arachidonoyl amine REASON: WRONGLY '
               'CLASSIFIED Valid head group (Ethanolamide head group found '
               'with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 28 carbons, 18 rotatable '
               'bonds and a molecular weight of 423.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               '[C@@H](C(CCCCCCCCCCCCCCC)=O)(CO)NC(=O)CCCCCCCCCCCCCCC NAME: '
               'N-palmitoyl-3-ketodihydrosphingosine REASON: WRONGLY '
               'CLASSIFIED Valid head group (Ethanolamide head group found '
               'with correct amide and nitrogen counts (1 each)), no '
               'phosphorus, exactly one acyl linkage, 34 carbons, 31 rotatable '
               'bonds and a molecular weight of 537.5 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O1[C@](CC[C@@]1([C@H](O)CCCCCCCCCC)[H])([C@H](O)C[C@@H](O)CCCCCC[C@H](O)CCCCCCCC2=C[C@@H](OC2=O)C)[H] '
               'NAME: Asitrilobin D REASON: WRONGLY CLASSIFIED Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 37 carbons, 28 rotatable bonds and a '
               'molecular weight of 624.5 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               ' * SMILES: '
               'O=C(O[C@@H]1C=C2[C@H](CC[C@]3([C@H]2CC[C@@H]3[C@@H](/C=C/[C@@H](C(C)C)C)C)C)[C@@]4([C@]1(O)C[C@@H](O)CC4)C)CCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: 22E, '
               '24R-ergosta-7,22-diene-3beta,5alpha-diol-6beta-inoleate '
               'REASON: WRONGLY CLASSIFIED Valid head group (Glycerol head '
               'group found with correct ester and nitrogen counts (1 and 0, '
               'respectively)), no phosphorus, exactly one acyl linkage, 46 '
               'carbons, 19 rotatable bonds and a molecular weight of 692.6 Da '
               'indicate a lipid‐like structure typical of an '
               'endocannabinoid.\n'
               ' * SMILES: C(=C/CCCCCCCC(O)=O)\\C(C(C(CCCCC)O)O)OC NAME: '
               '12,13-dihydroxy-11-methoxy-9-octadecenoic acid REASON: WRONGLY '
               'CLASSIFIED Valid head group (Glycerol head group found with '
               'correct ester and nitrogen counts (1 and 0, respectively)), no '
               'phosphorus, exactly one acyl linkage, 19 carbons, 16 rotatable '
               'bonds and a molecular weight of 344.3 Da indicate a lipid‐like '
               'structure typical of an endocannabinoid.\n'
               ' * SMILES: '
               'C(O)(=O)[C@H]([C@H]([C@H](C[C@H](CCCCCCCCCCCCCCC)C)C)O)C NAME: '
               'Mycolipanolic acid (C24) REASON: WRONGLY CLASSIFIED Valid head '
               'group (Glycerol head group found with correct ester and '
               'nitrogen counts (1 and 0, respectively)), no phosphorus, '
               'exactly one acyl linkage, 24 carbons, 19 rotatable bonds and a '
               'molecular weight of 384.4 Da indicate a lipid‐like structure '
               'typical of an endocannabinoid.\n'
               'False negatives: SMILES: '
               'O=C(O[C@@H]([C@@H](O)[C@H](O)CO)CO)C(=CC(C(O)C(=CC(C(O)C(=CC(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)C(=CC(CC(CC)C)C)C)C)C)C)C)C)C '
               'NAME: Roselipin 3E REASON: MISSED No valid head group found. '
               'Glycerol fragment count = 8 and nitrogen count = 0 (expected 1 '
               'and 0, respectively)\n'
               ' * SMILES: '
               'O=C(O[C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)/C(=C/[C@@H]([C@H](O)/C(=C/[C@@H]([C@H](O)/C(=C/[C@@H]([C@H](O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)/C(=C/[C@H](C[C@H](CC)C)C)/C)C)/C)C)/C)C)/C '
               'NAME: TMC-171A REASON: MISSED No valid head group found. '
               'Glycerol fragment count = 9 and nitrogen count = 0 (expected 1 '
               'and 0, respectively)\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCOC(CO)CO NAME: '
               '2-arachidonyl glyceryl ether REASON: MISSED No valid head '
               'group found. Glycerol fragment found but number of ester '
               'groups is 0 (expected 1)\n'
               ' * SMILES: '
               'O=C(O[C@@H]([C@H](O)[C@H](O)CO)CO)C(=CC(C(O)C(=CC(C(O)C(=CC(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)C(=CC(CC(CC)C)C)C)C)C)C)C)C)C '
               'NAME: Roselipin 3D REASON: MISSED No valid head group found. '
               'Glycerol fragment count = 8 and nitrogen count = 0 (expected 1 '
               'and 0, respectively)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No valid head group found. '},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'Contains phosphorus; likely a '
                                               'phospholipid rather than an '
                                               'endocannabinoid'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No valid head group found. '},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No valid head group found. '
                                               'Glycerol head group found but '
                                               'acyl linkage count from ester '
                                               'bonds = 0 and ether-linked '
                                               'count = 18 (expected exactly '
                                               '1) with nitrogen count = 2 '
                                               '(expected 0)'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No valid head group found. '
                                               'Glycerol head group found but '
                                               'acyl linkage count from ester '
                                               'bonds = 0 and ether-linked '
                                               'count = 5 (expected exactly 1) '
                                               'with nitrogen count = 0 '
                                               '(expected 0)'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No valid head group found. '
                                               'Glycerol head group found but '
                                               'acyl linkage count from ester '
                                               'bonds = 0 and ether-linked '
                                               'count = 18 (expected exactly '
                                               '1) with nitrogen count = 4 '
                                               '(expected 0)'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No valid head group found. '},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No valid head group found. '},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No valid head group found. '},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No valid head group found. '
                                               'Glycerol head group found but '
                                               'acyl linkage count from ester '
                                               'bonds = 0 and ether-linked '
                                               'count = 86 (expected exactly '
                                               '1) with nitrogen count = 9 '
                                               '(expected 0)'}],
    'sample_false_negatives': [   {   'smiles': 'O=C(O[C@@H]([C@@H](O)[C@H](O)CO)CO)C(=CC(C(O)C(=CC(C(O)C(=CC(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)C(=CC(CC(CC)C)C)C)C)C)C)C)C)C',
                                      'name': 'Roselipin 3E',
                                      'reason': 'No valid head group found. '
                                                'Glycerol head group found but '
                                                'acyl linkage count from ester '
                                                'bonds = 0 and ether-linked '
                                                'count = 6 (expected exactly '
                                                '1) with nitrogen count = 0 '
                                                '(expected 0)'},
                                  {   'smiles': 'O=C(O[C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)/C(=C/[C@@H]([C@H](O)/C(=C/[C@@H]([C@H](O)/C(=C/[C@@H]([C@H](O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)/C(=C/[C@H](C[C@H](CC)C)C)/C)C)/C)C)/C)C)/C',
                                      'name': 'TMC-171A',
                                      'reason': 'No valid head group found. '
                                                'Glycerol head group found but '
                                                'acyl linkage count from ester '
                                                'bonds = 0 and ether-linked '
                                                'count = 7 (expected exactly '
                                                '1) with nitrogen count = 0 '
                                                '(expected 0)'},
                                  {   'smiles': 'O=C(O[C@@H]([C@H](O)[C@H](O)CO)CO)C(=CC(C(O)C(=CC(C(O)C(=CC(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)C(=CC(CC(CC)C)C)C)C)C)C)C)C)C',
                                      'name': 'Roselipin 3D',
                                      'reason': 'No valid head group found. '
                                                'Glycerol head group found but '
                                                'acyl linkage count from ester '
                                                'bonds = 0 and ether-linked '
                                                'count = 6 (expected exactly '
                                                '1) with nitrogen count = 0 '
                                                '(expected 0)'}],
    'attempt': 5,
    'reasoning': 'Below is our “thinking‐out‐loud” summary followed by the '
                 'complete Python code.\n'
                 '\n'
                 'We noticed that the previous approach relied on counting '
                 'matches for a “head group” SMARTS pattern (for ethanolamides '
                 'and glycerol derivatives) and then requiring that the '
                 'overall molecule contain exactly one acyl linkage. However, '
                 'many false negatives arose when a molecule (for example, '
                 'Roselipin 3E or TMC‐171A) contained multiple fragments that '
                 'matched the simple glycerol SMARTS. Also, some true '
                 'endocannabinoids such as 2‑arachidonoyl glyceryl ether do '
                 'not contain an ester (C(=O)O) but an ether linkage. To fix '
                 'this we now (i) relax the “exactly one match” rule for the '
                 'glycerol head group by instead “searching for a glycerol '
                 'fragment that is directly linked (via an oxygen) to a long '
                 'acyl chain” and (ii) explicitly test for both types of acyl '
                 'linkage at the head: either the (amide) ethanolamide case or '
                 'the glycerol-based case. In the glycerol case we first try '
                 'to see whether a glycerol oxygen is attached to an ester '
                 'bond (by checking that the oxygen from a “C(=O)O” pattern '
                 'falls within the glycerol fragment) and if not we try to '
                 'detect a direct alkyl/ether bond that leads to a long fatty '
                 'chain. Moreover, we retain the overall “lipid‐like” criteria '
                 'of having enough carbons, rotatable bonds and a molecular '
                 'weight in range and we continue to reject any molecules '
                 'containing phosphorus.\n'
                 '\n'
                 'Below is the complete Python program in a single code '
                 'block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 20,
    'num_false_positives': 421,
    'num_true_negatives': 141856,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.045351473922902494,
    'recall': 0.8695652173913043,
    'f1': 0.08620689655172414,
    'accuracy': 0.9970203794799719,
    'negative_predictive_value': 0.9999788522406051}