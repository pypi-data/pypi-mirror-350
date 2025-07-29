"""
Classifies: CHEBI:80291 aliphatic nitrile
"""
"""
Classifies: aliphatic nitrile (any nitrile derived from an aliphatic compound)

An aliphatic nitrile is defined as any molecule that contains at least one nitrile (–C≡N)
where the nitrile carbon is not aromatic and its single substituent (i.e. the atom attached
to the nitrile carbon besides the nitrile nitrogen) is an sp3 carbon that does not lead into 
a structurally extended (e.g. >6 carbons) or functionalized (e.g. carbonyl, extra nitrile)
branch and does not include any aromatic atoms.
"""

from rdkit import Chem

def is_aliphatic_nitrile(smiles: str):
    """
    Determines if the molecule is an aliphatic nitrile based on its SMILES string.
    
    The procedure is as follows:
      1. Parse the SMILES and search for a nitrile substructure matching [C;X2]#[N;X1].
      2. For each nitrile match, take the C (nitrile carbon) and verify that it is not aromatic.
      3. Identify the substituent branch (the neighbor of the nitrile carbon that is not the nitrogen).
      4. Require that this substituent is a carbon atom (i.e. symbol=="C"), that is sp3,
         and that it bears at least one hydrogen.
      5. Check that none of its other bonds (to atoms other than the nitrile carbon) is directly
         to a polarized group like a carbonyl (a double bond to oxygen) or forms part of another nitrile.
      6. Walk the branch (using a breadth-first search) to count carbon atoms and to ensure that
         no aromatic atoms are encountered. If the branch contains too many carbons (a cutoff of 6 is used)
         we assume that the nitrile is derived from a long fatty or cyanolipid chain and reject it.
    
    Args:
        smiles (str): SMILES representation of the molecule.
    
    Returns:
        bool: True if classified as an aliphatic nitrile, False otherwise.
        str: Explanation for the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define the nitrile SMARTS pattern: C#N where the carbon has exactly two bonds.
    nitrile_pattern = Chem.MolFromSmarts("[C;X2]#[N;X1]")
    if nitrile_pattern is None:
        return False, "Error creating nitrile pattern"
    
    matches = mol.GetSubstructMatches(nitrile_pattern)
    if not matches:
        return False, "No nitrile group found in the molecule"
    
    # Helper: recursively check if any atom in the branch is aromatic.
    def branch_contains_aromatic(atom, banned_idx, visited):
        if atom.GetIdx() in visited:
            return False
        visited.add(atom.GetIdx())
        if atom.GetIsAromatic():
            return True
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() == banned_idx:
                continue
            if branch_contains_aromatic(nbr, banned_idx, visited):
                return True
        return False
    
    # Helper: count how many carbon atoms (unique indices) are in the branch.
    def count_branch_carbons(start_atom, banned_idx):
        queue = [start_atom]
        visited = {banned_idx}
        carbon_count = 0
        while queue:
            current = queue.pop(0)
            if current.GetIdx() in visited:
                continue
            visited.add(current.GetIdx())
            if current.GetSymbol() == "C":
                carbon_count += 1
            for nbr in current.GetNeighbors():
                if nbr.GetIdx() not in visited:
                    queue.append(nbr)
        return carbon_count

    # Loop over every nitrile match
    for match in matches:
        # match[0] is the nitrile carbon; match[1] is the nitrile nitrogen.
        nitrile_c = mol.GetAtomWithIdx(match[0])
        nitrile_n = mol.GetAtomWithIdx(match[1])
        
        # Skip if the nitrile carbon is aromatic or not a carbon.
        if nitrile_c.GetSymbol() != "C" or nitrile_c.GetIsAromatic():
            continue
        
        # Collect substituents excluding the nitrile nitrogen.
        subs = [nbr for nbr in nitrile_c.GetNeighbors() if nbr.GetIdx() != nitrile_n.GetIdx()]
        if not subs:
            continue  # Unusual, but go to next match

        # We expect exactly one substituent (terminal nitrile), so if multiple exist, we process each.
        for sub in subs:
            # Rule 1: The substituent must be carbon.
            if sub.GetSymbol() != "C":
                continue
            
            # Rule 2: It should be sp3 (if available, to indicate a saturated, aliphatic center).
            # (Note: sometimes hybridization info is not set; in that case, we try to check degree.)
            if sub.GetHybridization() != Chem.rdchem.HybridizationType.SP3:
                continue

            # Rule 3: It should have at least one attached hydrogen.
            if sub.GetTotalNumHs() < 1:
                continue
            
            # Rule 4: Check that none of its other bonds (besides to the nitrile carbon) is directly
            #         to atoms that are part of a polar function (eg, carbonyl oxygen or another nitrile).
            bad_attachment = False
            for nbr in sub.GetNeighbors():
                if nbr.GetIdx() == nitrile_c.GetIdx():
                    continue
                bond = mol.GetBondBetweenAtoms(sub.GetIdx(), nbr.GetIdx())
                if bond is not None:
                    # Check for carbonyl: if neighbor is O and bond is double.
                    if nbr.GetSymbol() == "O" and bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                        bad_attachment = True
                        break
                    # Check if neighbor is part of another nitrile bond.
                    if nbr.GetSymbol() == "N":
                        nbonds = nbr.GetBonds()
                        for b in nbonds:
                            if b.GetBondType() == Chem.rdchem.BondType.TRIPLE:
                                bad_attachment = True
                                break
                        if bad_attachment:
                            break
            if bad_attachment:
                continue
            
            # Rule 5: Recursively ensure the substituent’s branch contains no aromatic atoms.
            if branch_contains_aromatic(sub, nitrile_c.GetIdx(), set()):
                continue
            
            # Rule 6: Count carbons in the branch. If there are too many (here >6), reject.
            branch_carbons = count_branch_carbons(sub, nitrile_c.GetIdx())
            if branch_carbons > 6:
                continue
            
            # Passed all checks: classify as an aliphatic nitrile.
            return True, "Contains a nitrile group attached to an exclusively aliphatic substituent branch"
    
    # If none of the nitrile groups pass, provide an explanation.
    return False, "Nitrile group(s) found but none have a qualifying aliphatic substituent branch"


# Example usages (uncomment to test):
# print(is_aliphatic_nitrile("N#CCC#N"))                         # malononitrile -> expected True.
# print(is_aliphatic_nitrile("CC#N"))                             # acetonitrile -> expected True.
# print(is_aliphatic_nitrile("OCC#N"))                            # glycolonitrile -> expected False.
# print(is_aliphatic_nitrile("CCOC(=O)C(C)C#N"))                 # ethyl 2-cyanopropionate -> expected False.


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:80291',
                          'name': 'aliphatic nitrile',
                          'definition': 'Any nitrile derived from an aliphatic '
                                        'compound.',
                          'parents': ['CHEBI:18379', 'CHEBI:33653'],
                          'xrefs': ['KEGG:C16072'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 72,
                           'log_lines_of_code': 4.276666119016055,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'append',
                                                 'add',
                                                 'GetIsAromatic',
                                                 'MolFromSmarts',
                                                 'pop',
                                                 'GetSymbol',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetIdx'],
                           'methods_called_count': 11,
                           'smarts_strings': ['[C;X2]#[N;X1]'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_aliphatic_nitrile(smiles: str):',
                                       'branch_contains_aromatic(atom, '
                                       'banned_idx, visited):',
                                       'count_branch_carbons(start_atom, '
                                       'banned_idx):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error creating nitrile '
                                          'pattern"',
                                          'False, "No nitrile group found in '
                                          'the molecule"',
                                          'False',
                                          'True',
                                          'True',
                                          'False',
                                          'carbon_count',
                                          'False, "Nitrile group(s) found but '
                                          'none have a qualifying aliphatic '
                                          'substituent branch"'],
                           'returns_count': 9,
                           'complexity': 6.455333223803211},
    'message': '\n'
               'Attempt failed: F1 score of 0.3157894736842105 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: N#CCC#N NAME: malononitrile REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: OC(=O)CNCC#N NAME: N-(cyanomethyl)glycine REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: CCN(CC)C(=O)CC#N NAME: N,N-diethylcyanoacetamide '
               'REASON: CORRECT Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               ' * SMILES: N[C@H](CCC(O)=O)C#N NAME: '
               '(R)-gamma-amino-gamma-cyanobutanoic acid REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: C[C@H](N)C#N NAME: (S)-alpha-aminopropionitrile '
               'REASON: CORRECT Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               ' * SMILES: O=C1CCC(C1)C#N NAME: 3-oxocyclopentanecarbonitrile '
               'REASON: CORRECT Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               ' * SMILES: N[C@@H](CCC(O)=O)C#N NAME: '
               '(S)-gamma-amino-gamma-cyanobutanoic acid REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: N[C@@H](CCC(=O)NCCC#N)C(O)=O NAME: '
               'gamma-glutamyl-beta-aminopropiononitrile REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: CCC(C)C#N NAME: 2-methylbutanenitrile REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: N[C@@H](CC#N)C(O)=O NAME: 3-cyano-L-alanine REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: CC(C)CC#N NAME: isovaleronitrile REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: ClC(Cl)C#N NAME: Dichloroacetonitrile REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: CCCC#N NAME: butyronitrile REASON: CORRECT Contains '
               'a nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: BrC(Br)C#N NAME: Dibromoacetonitrile REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H]([C@@H](C[C@@]21[H])C#N)C(C)=O '
               'NAME: pregnenolone 16alpha-carbonitrile REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: CC#N NAME: acetonitrile REASON: CORRECT Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: C(C#N)C(C(=O)O)N NAME: 3-cyanoalanine REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: BrCC(Br)(CCC#N)C#N NAME: '
               '2-bromo-2-(bromomethyl)pentanedinitrile REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: C(CCCCS(C)=O)CCCC#N NAME: '
               '1-cyano-8-(methylsulfinyl)octane REASON: CORRECT Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: NCCC#N NAME: beta-aminopropionitrile REASON: '
               'CORRECT Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: C=CCC#N NAME: allyl cyanide REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: N#CCNCC#N NAME: iminodiacetonitrile REASON: CORRECT '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: C(CCCCS(C)=O)CCC#N NAME: '
               '1-cyano-8-(methylsulfinyl)heptane REASON: CORRECT Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: NC(CCC#N)C(O)=O NAME: '
               'alpha-amino-gamma-cyanobutanoic acid REASON: CORRECT Contains '
               'a nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: C[C@@H](N)C#N NAME: (R)-alpha-aminopropionitrile '
               'REASON: CORRECT Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               'False positives: SMILES: CCOC(=O)C(C)C#N NAME: ethyl '
               '2-cyanopropionate REASON: WRONGLY CLASSIFIED Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: N#CC(CCC#N)C NAME: 2-methyl-Pentanedinitrile '
               'REASON: WRONGLY CLASSIFIED Contains a nitrile group attached '
               'to an exclusively aliphatic fragment\n'
               ' * SMILES: C(CCCCCCCC#N)CCCCCCCCC NAME: stearonitrile REASON: '
               'WRONGLY CLASSIFIED Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               ' * SMILES: OCC#N NAME: glycolonitrile REASON: WRONGLY '
               'CLASSIFIED Contains a nitrile group attached to an exclusively '
               'aliphatic fragment\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1OCC(O)(CO)CC#N)CO NAME: '
               '(3R)-3,4-Dihydroxy-3-(hydroxymethyl)butanenitrile 4-glucoside '
               'REASON: WRONGLY CLASSIFIED Contains a nitrile group attached '
               'to an exclusively aliphatic fragment\n'
               ' * SMILES: O(C(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(C(C)=C)C#N '
               'NAME: Type IV cyanolipid 18:3 ester REASON: WRONGLY CLASSIFIED '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: COC1=C(Br)[C@H](O)[C@](O)(CC#N)C=C1Br NAME: '
               'Aeroplysinin 1 REASON: WRONGLY CLASSIFIED Contains a nitrile '
               'group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: '
               'O([C@@H]/1C[C@H](OC)[C@H](OC)[C@@H](O)\\C1=C\\C#N)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: Simmondsin REASON: WRONGLY CLASSIFIED Contains a nitrile '
               'group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: N#CC/C=C\\CCCCCCCCCC(C)C NAME: '
               '(Z)-14-methylpentadec-3-enenitrile REASON: WRONGLY CLASSIFIED '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: '
               'O=C1C(N)=CC(=O)C2=C1C(N3C(C#N)C4CC5C6N(C2C3C5N4C)CCO6)CO NAME: '
               'Dnacin A1 REASON: WRONGLY CLASSIFIED Contains a nitrile group '
               'attached to an exclusively aliphatic fragment\n'
               ' * SMILES: N#CCCCCCCC/C=C\\CCCCCC NAME: '
               '(Z)-hexadec-9-enenitrile REASON: WRONGLY CLASSIFIED Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: '
               'C(O)(=O)C=1N2[C@@]([C@@H](C2=O)NC(CC#N)=O)(SCC1COC(C)=O)[H] '
               'NAME: cefacetrile REASON: WRONGLY CLASSIFIED Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: O1N(C(CC1C#N)(C(OC)=O)C(OC)=O)C NAME: '
               '3-Cyano-5,5-dimethoxycarbonyl-N-methylisoxazolidine REASON: '
               'WRONGLY CLASSIFIED Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               ' * SMILES: N#CC/C=C\\CCCCCCCCCCCC NAME: '
               '(Z)-hexadec-3-enenitrile REASON: WRONGLY CLASSIFIED Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: N[C@@H](CC#N)C([O-])=O NAME: 3-cyano-L-alaninate '
               'REASON: WRONGLY CLASSIFIED Contains a nitrile group attached '
               'to an exclusively aliphatic fragment\n'
               ' * SMILES: O=C(O)C(N)C(C#N)CC(=O)O NAME: Beta-Cyanoglutamic '
               'acid REASON: WRONGLY CLASSIFIED Contains a nitrile group '
               'attached to an exclusively aliphatic fragment\n'
               ' * SMILES: N#CC/C=C\\CCCCCCCC(C)C NAME: '
               '(Z)-12-methyltridec-3-enenitrile REASON: WRONGLY CLASSIFIED '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: CCOC(=O)C(C#N)C(C)=O NAME: ethyl '
               '2-cyanoacetoacetate REASON: WRONGLY CLASSIFIED Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: '
               'O(C(C(OC(=O)C)C(OC(=O)C)C#N)C(OC(=O)C)COC(=O)C)C(=O)C NAME: '
               '2,3-di(acetyloxy)-3-cyano-1-[1,2-di(acetyloxy)ethyl]propyl '
               'acetate REASON: WRONGLY CLASSIFIED Contains a nitrile group '
               'attached to an exclusively aliphatic fragment\n'
               ' * SMILES: N#CCCCCCCCCCCCCCCC NAME: Hexadecanenitrile REASON: '
               'WRONGLY CLASSIFIED Contains a nitrile group attached to an '
               'exclusively aliphatic fragment\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCCCCCC)C/C(/C)=C/C#N NAME: Type III '
               'cyanolipid 16:0 ester REASON: WRONGLY CLASSIFIED Contains a '
               'nitrile group attached to an exclusively aliphatic fragment\n'
               ' * SMILES: [O-]C(=O)CNCC#N NAME: N-(cyanomethyl)glycinate '
               'REASON: WRONGLY CLASSIFIED Contains a nitrile group attached '
               'to an exclusively aliphatic fragment\n'
               ' * SMILES: C(C[C@@H](C#N)O)C NAME: '
               '(2S)-2-hydroxypentanenitrile REASON: WRONGLY CLASSIFIED '
               'Contains a nitrile group attached to an exclusively aliphatic '
               'fragment\n'
               ' * SMILES: OC(CC#N)C=C NAME: 1-Cyano-2-hydroxy-3-butene '
               'REASON: WRONGLY CLASSIFIED Contains a nitrile group attached '
               'to an exclusively aliphatic fragment\n'
               ' * SMILES: CN(C)CC#N NAME: 2-(Dimethylamino)acetonitrile '
               'REASON: WRONGLY CLASSIFIED Contains a nitrile group attached '
               'to an exclusively aliphatic fragment\n'
               'False negatives: SMILES: '
               'C\\C(=C\\CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)C#N NAME: '
               'rhodiocyanoside A REASON: MISSED Nitrile group(s) found but '
               'none have an exclusively aliphatic substituent branch\n'
               ' * SMILES: '
               'COC1=CC(=O)N(C)[C@@H](O)[C@@]1(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)C#N '
               'NAME: acalyphin REASON: MISSED Nitrile group(s) found but none '
               'have an exclusively aliphatic substituent branch\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](O[C@@]2(C[C@@H](O)C=C2)C#N)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: volkenin REASON: MISSED Nitrile group(s) found but none '
               'have an exclusively aliphatic substituent branch\n'
               ' * SMILES: O1C2=C(C(C3CCC=CC3)C(=C1N)C#N)C(=O)CC(C2)(C)C NAME: '
               '2-amino-4-(3-cyclohexen-1-yl)-7,7-dimethyl-5-oxo-5,6,7,8-tetrahydrochromene-3-carbonitrile '
               'REASON: MISSED Nitrile group(s) found but none have an '
               'exclusively aliphatic substituent branch\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No nitrile group found in the '
                                               'molecule'}],
    'sample_false_negatives': [   {   'smiles': 'C\\C(=C\\CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)C#N',
                                      'name': 'rhodiocyanoside A',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': 'COC1=CC(=O)N(C)[C@@H](O)[C@@]1(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)C#N',
                                      'name': 'acalyphin',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': 'N[C@@H](CCC(=O)NCCC#N)C(O)=O',
                                      'name': 'gamma-glutamyl-beta-aminopropiononitrile',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H]([C@@H](C[C@@]21[H])C#N)C(C)=O',
                                      'name': 'pregnenolone '
                                              '16alpha-carbonitrile',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': 'C(CCCCS(C)=O)CCCC#N',
                                      'name': '1-cyano-8-(methylsulfinyl)octane',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](O[C@@]2(C[C@@H](O)C=C2)C#N)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'volkenin',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': 'O1C2=C(C(C3CCC=CC3)C(=C1N)C#N)C(=O)CC(C2)(C)C',
                                      'name': '2-amino-4-(3-cyclohexen-1-yl)-7,7-dimethyl-5-oxo-5,6,7,8-tetrahydrochromene-3-carbonitrile',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent branch'},
                                  {   'smiles': 'C(CCCCS(C)=O)CCC#N',
                                      'name': '1-cyano-8-(methylsulfinyl)heptane',
                                      'reason': 'Nitrile group(s) found but '
                                                'none have a qualifying '
                                                'aliphatic substituent '
                                                'branch'}],
    'attempt': 3,
    'reasoning': 'Below is one complete Python‐code solution. In our reasoning '
                 'we noticed that merely finding a nitrile substructure with a '
                 '“non‐nitrogen” substituent that is free of aromatic atoms '
                 'isn’t enough. Many “false positives” (so‐called simple '
                 'nitriles or compounds that bear extra functional groups) '
                 'were incorrectly flagged. We therefore added extra checks: '
                 'first we require that the nitrile “stem” (the nitrile '
                 'carbon) has exactly one non‐nitrogen neighbor and that this '
                 'atom is a (saturated) carbon (i.e. its hybridization is SP3 '
                 'and it carries at least one hydrogen). Next, we check that '
                 'none of its “other” bonds (to atoms other than the nitrile '
                 'carbon) is directly involved in a carbonyl (or another '
                 'nitrile) event. Finally, we “walk” outward from that '
                 'substituent (without going back to the nitrile carbon) to '
                 'count the total number of carbons in the branch; if the '
                 'branch is very long (as in some cyanolipids) we reject it as '
                 'not “derived from an aliphatic compound.” (The parameter '
                 'chosen here is a maximum of six carbons in the substituent '
                 'branch.) Hopefully these extra conditions improve the '
                 'F1‐score, while still accepting most of the listed true '
                 'positives. \n'
                 '\n'
                 'Below is the complete code (all inside a single Python code '
                 'block):\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 39,
    'num_true_negatives': 142230,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.3709677419354839,
    'recall': 0.7419354838709677,
    'f1': 0.49462365591397855,
    'accuracy': 0.9996697118763176,
    'negative_predictive_value': 0.9999437562395421}