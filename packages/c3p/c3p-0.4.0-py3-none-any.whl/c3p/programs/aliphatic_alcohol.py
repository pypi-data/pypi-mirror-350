"""
Classifies: CHEBI:2571 aliphatic alcohol
"""
"""
Classifies:An aliphatic alcohol, defined as 'An alcohol derived from an aliphatic compound.'
Improvement rationale (as gleaned from previous outcomes):
 - Disqualify molecules that contain free carboxylic acid/carboxylate groups.
 - For each –OH group, require that it is attached to a saturated (sp³), non‐aromatic carbon.
 - From that candidate carbon (ignoring the –OH oxygen) perform a DFS search over contiguous 
   chain carbons (acyclic and non‐aromatic). In the DFS we allow a tolerance of up to 2 sp2 centers 
   (isolated) but disallow any carbonyl-like carbons (i.e. a carbon double bonded to oxygen).
 - If any adjoining chain (not counting the candidate carbon itself) has at least 6 carbons then
   the molecule is classified as an aliphatic alcohol.
"""

from rdkit import Chem

def is_aliphatic_alcohol(smiles: str):
    """
    Determines if a molecule is an aliphatic alcohol based on its SMILES string.
    An aliphatic alcohol has at least one hydroxyl (-OH) group attached to a saturated (sp3),
    non‐aromatic carbon and that candidate carbon is connected to a contiguous, open-chain 
    aliphatic (acyclic) region (allowing up to 2 isolated sp2 centres) of at least 6 carbons.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classified as an aliphatic alcohol, False otherwise
        str: Reason for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # --- 1. Disqualify molecules that contain free carboxylic acid/carboxylate groups.
    acid_patterns = [
        Chem.MolFromSmarts("[CX3](=O)[O;H1]"),  # carboxylic acid group
        Chem.MolFromSmarts("[CX3](=O)[O-]")     # carboxylate group
    ]
    for patt in acid_patterns:
        if mol.HasSubstructMatch(patt):
            return False, "Molecule contains carboxylic acid/carboxylate functionality"

    # --- Helper: determine if a carbon atom is allowed as part of the aliphatic chain.
    #    Returns "sp3" if the carbon is allowed as sp3, "sp2" if it is allowed as an isolated sp2, or False otherwise.
    def allowed_chain_atom(atom):
        if atom.GetAtomicNum() != 6:
            return False  # Only carbons allowed.
        # Disallow aromatic atoms and those in rings.
        if atom.GetIsAromatic() or atom.IsInRing():
            return False
        # Exclude carbons having a double bond to oxygen (carbonyl-like)
        for bond in atom.GetBonds():
            if bond.GetBondTypeAsDouble() == 2.0:
                other = bond.GetOtherAtom(atom)
                if other.GetAtomicNum() == 8:
                    return False
        # Allow sp3; allow sp2 only as isolated (tolerance will be enforced in DFS)
        hyb = atom.GetHybridization()
        if hyb == Chem.rdchem.HybridizationType.SP3:
            return "sp3"
        elif hyb == Chem.rdchem.HybridizationType.SP2:
            return "sp2"
        return False

    # --- DFS function to compute maximum contiguous chain length along allowed (acyclic, non‐aromatic) carbons.
    # We use backtracking with a visited set per branch and a tolerance counter for sp2 centres.
    def dfs(atom, visited, sp2_count):
        max_length = 0  # length counted from this starting atom.
        for nbr in atom.GetNeighbors():
            # Only consider carbon neighbors.
            if nbr.GetAtomicNum() != 6:
                continue
            if nbr.GetIdx() in visited:
                continue  # avoid cycles
            typ = allowed_chain_atom(nbr)
            if not typ:
                continue
            new_sp2 = sp2_count + (1 if typ == "sp2" else 0)
            if new_sp2 > 2:  # exceed allowed sp2 tolerance
                continue
            visited.add(nbr.GetIdx())
            current_length = 1 + dfs(nbr, visited, new_sp2)
            visited.remove(nbr.GetIdx())
            if current_length > max_length:
                max_length = current_length
        return max_length

    # --- Main search: iterate over oxygens to spot hydroxyl (-OH) groups.
    for oxygen in mol.GetAtoms():
        if oxygen.GetAtomicNum() != 8:
            continue
        # Check that oxygen has at least one hydrogen (to signify -OH instead of, e.g., ether)
        if oxygen.GetTotalNumHs() < 1:
            continue

        # For each neighbor of the oxygen, check if it is a candidate carbon (bearing the –OH)
        for cand_carbon in oxygen.GetNeighbors():
            if cand_carbon.GetAtomicNum() != 6:
                continue
            # Must be saturated (sp3) and non-aromatic.
            if cand_carbon.GetHybridization() != Chem.rdchem.HybridizationType.SP3 or cand_carbon.GetIsAromatic():
                continue
            
            # For each neighbor of the candidate carbon (except the -OH oxygen), attempt to find a contiguous chain.
            for neigh in cand_carbon.GetNeighbors():
                if neigh.GetIdx() == oxygen.GetIdx():
                    continue  # Don't go back to the -OH oxygen.
                typ = allowed_chain_atom(neigh)
                if not typ:
                    continue
                # Start a DFS from this neighbor.
                visited = set([neigh.GetIdx()])
                chain_length = dfs(neigh, visited, 1 if typ=="sp2" else 0)
                # chain_length here is the count of chain carbons from the starting neighbor.
                if chain_length >= 6:
                    return True, ("Found -OH group attached to a sp3, non-aromatic carbon that is connected "
                                  "to an acyclic aliphatic chain (chain length = {}).".format(chain_length))
    return False, ("No qualifying -OH group found attached to a sp3, non-aromatic carbon with an adjoining "
                   "acyclic aliphatic chain of at least 6 carbons.")
    
# (Optional) Testing examples.
if __name__ == "__main__":
    test_cases = [
        # True positives from the provided outcomes:
        ("CCCCCCC(C)O", "octan-2-ol"),
        ("O=C(OC)/C=C/CC(O)CCCCCC(O)C", "Cladosporester A"),
        ("CCCCCC(O)CC(=O)CCc1ccc(O)c(O)c1", "1-(3,4-Dihydroxyphenyl)-5-hydroxy-3-decanone"),
        ("OCCCCCC/C=C/CCCC", "7E-dodecen-1-ol"),
        ("O[C@@H](CCC/C=C\\CC)C", "6Z-Nonen-2R-ol"),
        ("OCCCCCCCCCCC1=CC=CC=C1", "10-Phenyl-1-decanol"),
        ("CCCCCCCCCCCCCCCCCCCCCCO", "tricosan-1-ol"),
        # A few false positives/negatives reported before could be tested as well.
    ]
    
    for smi, name in test_cases:
        result, reason = is_aliphatic_alcohol(smi)
        print("SMILES:", smi)
        print("Name:", name)
        print("Classification:", result)
        print("Reason:", reason)
        print("-" * 60)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2571',
                          'name': 'aliphatic alcohol',
                          'definition': 'An  alcohol derived from an aliphatic '
                                        'compound.',
                          'parents': ['CHEBI:30879'],
                          'xrefs': ['KEGG:C02525'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 92,
                           'log_lines_of_code': 4.5217885770490405,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
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
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
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
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetOtherAtom',
                                                 'GetTotalNumHs',
                                                 'GetIdx',
                                                 'GetHybridization',
                                                 'GetAtomicNum',
                                                 'GetBondTypeAsDouble',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'GetBonds',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'remove',
                                                 'GetNeighbors',
                                                 'add',
                                                 'IsInRing',
                                                 'GetIsAromatic'],
                           'methods_called_count': 16,
                           'smarts_strings': [   '[CX3](=O)[O-]',
                                                 '[CX3](=O)[O;H1]'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_aliphatic_alcohol(smiles: str):',
                                       'allowed_chain_atom(atom):',
                                       'dfs(atom, visited, sp2_count):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains '
                                          'carboxylic acid/carboxylate '
                                          'functionality"',
                                          'False  # Only carbons allowed.',
                                          'False',
                                          'False',
                                          '"sp3"',
                                          '"sp2"',
                                          'False',
                                          'max_length',
                                          'False, ("No qualifying -OH group '
                                          'found attached to a sp3, '
                                          'non-aromatic carbon with an '
                                          'adjoining "'],
                           'returns_count': 10,
                           'complexity': 7.704357715409808},
    'message': '\n'
               'Attempt failed: F1 score of 0.1525017135023989 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCC(C)O NAME: octan-2-ol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 6).\n'
               ' * SMILES: O=C(OC)/C=C/CC(O)CCCCCC(O)C NAME: Cladosporester A '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 9).\n'
               ' * SMILES: CCCCCC(O)CC(=O)CCc1ccc(O)c(O)c1 NAME: '
               '1-(3,4-Dihydroxyphenyl)-5-hydroxy-3-decanone REASON: CORRECT '
               'Found -OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 7).\n'
               ' * SMILES: OCCCCCC/C=C/CCCC NAME: 7E-dodecen-1-ol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 11).\n'
               ' * SMILES: O[C@@H](CCC/C=C\\CC)C NAME: 6Z-Nonen-2R-ol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 7).\n'
               ' * SMILES: OCCCCC/C=C/CCCCC NAME: 6E-Dodecen-1-ol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 11).\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCCCCCCCCCO)CCCCCC NAME: '
               '28-Hydroxy-7-octacosanone REASON: CORRECT Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 20).\n'
               ' * SMILES: CCCCCCCCCCCCCCC(O)CCCC NAME: nonadecan-5-ol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 14).\n'
               ' * SMILES: O=C1OC(=CC(=C1C)O)C[C@@H](O)CCCCCCCO NAME: '
               '(S)-6-(2,9-dihydroxynonyl)-4-hydroxy-3-methyl-2H-pyran-2-one '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 9).\n'
               ' * SMILES: OCCCCCCCCCCC1=CC=CC=C1 NAME: 10-Phenyl-1-decanol '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 9).\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)CCCCCCCCCCC NAME: pentacosan-12-ol '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 13).\n'
               ' * SMILES: OCCCCCCCCCCCCO NAME: 1,12-dodecanediol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 11).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCO NAME: tricosan-1-ol '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 22).\n'
               ' * SMILES: OC(\\C=C\\CC(CCO)C)(C)C NAME: '
               '3,7-Dimethyl-5-octene-1,7-diol REASON: CORRECT Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: O=C(OCCO)CCCCCCC/C=C/[C@@H](O)CCCCC NAME: '
               '2-hydroxyethyl-11-hydroxyhexadec-9-enoate REASON: CORRECT '
               'Found -OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 9).\n'
               ' * SMILES: OC(CC(O)CO)C(O)CO NAME: 3-deoxyhexitol REASON: '
               'CORRECT Found -OH group attached to a sp3, non-aromatic carbon '
               'that is connected to an acyclic aliphatic chain (chain length '
               '= 6).\n'
               ' * SMILES: O[C@H](CCC[C@H](O)C)CCO NAME: '
               '(3R,7R)-1,3,7-Octanetriol REASON: CORRECT Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 7).\n'
               ' * SMILES: O=C(CCC(/C=C/C(O)(CO)CCCO)C(C)C)C NAME: '
               '(6E)-8,11-Dihydroxy-8-(hydroxymethyl)-5-(1-methylethyl)undec-6-en-2-one '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 7).\n'
               ' * SMILES: OCCCCCCCCC1CC2C3C(C4C3CC4)C2CC1 NAME: '
               '8-[3]-ladderane-1-octanol REASON: CORRECT Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 7).\n'
               ' * SMILES: CCCCCCCCCCCCC(O)CCCCCCCC NAME: henicosan-9-ol '
               'REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 12).\n'
               ' * SMILES: O=C(OCC/C(=C\\[C@H](O)[C@H](O)C1=CC=CC=C1)/C)C '
               'NAME: [(Z,5S,6R)-5,6-dihydroxy-3-methyl-6-phenylhex-3-enyl] '
               'acetate REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 6).\n'
               ' * SMILES: OC(CCCCCCCCCCCCCCCCCCCCCCCCCCCC)CC(O)CCCCC NAME: '
               '6,8-Hexatriacontanediol REASON: CORRECT Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 28).\n'
               ' * SMILES: O=C1OC(=O)C(=C1/C=C/CCC/C=C/CO)C NAME: Tricladolide '
               'B REASON: CORRECT Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 6).\n'
               ' * SMILES: O=C1O[C@H]([C@H](O)[C@H](O)/C=C\\CCCCC(=O)C)CC1 '
               'NAME: Pseudonocardide G REASON: CORRECT Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 7).\n'
               ' * SMILES: '
               'C(=C/[C@H](C(CCCC)(C)C)O)\\[C@@H]1[C@@H](CCCC/C=C/C(OC)=O)C(C[C@H]1O)=O '
               'NAME: gemeprost REASON: CORRECT Found -OH group attached to a '
               'sp3, non-aromatic carbon that is connected to an acyclic '
               'aliphatic chain (chain length = 7).\n'
               'False positives: SMILES: '
               'O=C([C@@H](C[C@H](C[C@@H](CC[C@@H](O)C[C@@H](O)[C@H]([C@@H](O)C1=CC(O)=CC(=C1)O)CC(C)C)C)C)C)CC '
               'NAME: Baulamycin A REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 8).\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: '
               'beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-[(15Z)-tetracosenoyl]sphingosine '
               'REASON: WRONGLY CLASSIFIED Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 15).\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H]2O[C@@H]([C@@H](O)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO)[C@@H]2O)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5S)-5-Acetamido-1,2,4,6-tetrahydroxyhexan-3-yl]oxy-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 6).\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O[C@@H]([C@H](O)[C@@H](O)CO)[C@H](O)CO)CO[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: '
               '(2S,3R,4R,5R)-4-[(2S,3R,4S,5S,6R)-3,4,5-Trihydroxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]oxan-2-yl]oxyhexane-1,2,3,5,6-pentol '
               'REASON: WRONGLY CLASSIFIED Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 6).\n'
               ' * SMILES: '
               'O=C(OC)[C@@H](NC(=O)C[C@@](O)(CC(=O)O[C@H]1[C@H](O)C([C@@H]2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4[C@@H](CC[C@@H](O)C(O)(C)C)C)C)C)(C)C)C)[C@@H](O)C5=CC=CC=C5 '
               'NAME: Pardinol C REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'O1C(CCC1C(O)CCCCCCCCCCCC)C(O)CCCCCC(O)CCCCC2OC(=O)C(C2)CC(=O)C '
               'NAME: Isoannoreticuin REASON: WRONGLY CLASSIFIED Found -OH '
               'group attached to a sp3, non-aromatic carbon that is connected '
               'to an acyclic aliphatic chain (chain length = 12).\n'
               ' * SMILES: '
               'C[C@@H]1[C@H](CC2(C([C@@H](C(O2)[C@@H](C[C@H]([C@@H](C)[C@H]([C@@H](C)C=C(C)C(=CC=CC(=CC#N)C)C)O)O)OC)OP(=O)(O)O)(C)C)O[C@@H]1CC=CC3=COC(=N3)[C@H](C)CCNC(=O)[C@@H]([C@@H]([C@@H](COC)N(C)C)O)O)O '
               'NAME: '
               '[(3S,7R,8R,9S)-2-[(1R,3R,4R,5S,6S)-14-cyano-3,5-dihydroxy-1-methoxy-4,6,8,9,13-pentamethyltetradeca-7,9,11,13-tetraenyl]-7-[3-[2-[(2R)-4-[[(2R,3R,4R)-4-(dimethylamino)-2,3-dihydroxy-5-methoxy-1-oxopentyl]amino]butan-2-yl]-4-oxazolyl]prop-2-enyl]-9-hydroxy-4,4,8-trimethyl-1,6-dioxaspiro[4.5]decan-3-yl] '
               'dihydrogen phosphate REASON: WRONGLY CLASSIFIED Found -OH '
               'group attached to a sp3, non-aromatic carbon that is connected '
               'to an acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)NC(OC)CC(C)C)CCC(=O)N)[C@@H](NC(=O)C[C@H](O)CCCCCCCCC)CC(=O)N '
               'NAME: Penicimutalide C/D REASON: WRONGLY CLASSIFIED Found -OH '
               'group attached to a sp3, non-aromatic carbon that is connected '
               'to an acyclic aliphatic chain (chain length = 11).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCC(=O)NC(CO)CCCCCCCCCC NAME: '
               'N-(1-hydroxydodecan-2-yl)tetracosanamide REASON: WRONGLY '
               'CLASSIFIED Found -OH group attached to a sp3, non-aromatic '
               'carbon that is connected to an acyclic aliphatic chain (chain '
               'length = 11).\n'
               ' * SMILES: '
               'Cl/C=C(\\C[C@H](O)CC[C@H](C[C@H]([C@H](O)CCCC[C@H]([C@H](O)CC=C)C)C)C)/CCCC#C '
               'NAME: Trichophycin H REASON: WRONGLY CLASSIFIED Found -OH '
               'group attached to a sp3, non-aromatic carbon that is connected '
               'to an acyclic aliphatic chain (chain length = 17).\n'
               ' * SMILES: '
               'O=C1N[C@@H](CC2=CC=C(O)C=C2)C(C1=C(O)/C=C/C(=C/[C@@H]([C@@H](O)C)C)/C)=O '
               'NAME: Syn-12-hydroxypretenellin A REASON: WRONGLY CLASSIFIED '
               'Found -OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'CC(C)\\C=C(/C)[C@H](O)[C@H](C)\\C=C(C)\\C=C\\C=C/C=C/C=C(\\C)C(=O)N[C@@H](C)CO '
               'NAME: Myxalamid B REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@@H](CC=CCCCC(OC[C@@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COP(O1)(O)=O)=O)C=CC(=O)[C@@H]([C@H](O)[C@@H]2O)/C=C/[C@@H](O)CCCCC)(O)=O '
               'NAME: CDP-DG(PGJ2/20:2(11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Found -OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 7).\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCC(=O)C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCC)(OCCN)(O)=O '
               'NAME: PE(18:1(11Z)/6 keto-PGF1alpha) REASON: WRONGLY '
               'CLASSIFIED Found -OH group attached to a sp3, non-aromatic '
               'carbon that is connected to an acyclic aliphatic chain (chain '
               'length = 7).\n'
               ' * SMILES: '
               'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCC)\\C)CO)[C@H](O)CCCCCCCCCCCCCC '
               'NAME: '
               '(2S,2′R,3R,4E,8E)-N-2′-hydroxyhexadecanoyl-2-amino-9-methyl-4,8-octadecadiene-1,3-diol '
               'REASON: WRONGLY CLASSIFIED Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 6).\n'
               ' * SMILES: '
               'OC1=CC=C(C[C@@H](NC)[C@H](O)CC/C=C/[C@H](C[C@H](CC)C)C)C=C1 '
               'NAME: Tyroscherin REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 11).\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)C[C@@H](CC)C(C)C '
               'NAME: (22S)-hydroxysitosterol REASON: WRONGLY CLASSIFIED Found '
               '-OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'CO[C@H]([C@H](O)CC(=O)[C@@H](C)[C@@H](O)CC[C@@H](C)[C@@H]1O[C@]2(CC[C@@H](C)[C@H](CC[C@H](C)C(C)=O)O2)CC[C@@H]1C)[C@H](OC(=O)C[C@@H](O)C1=C(C)C(=O)OC1=O)C(C)C '
               'NAME: Tautomycin REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'O=C(O[C@@H]1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/CO)\\C)C)CC4)(C)CC3)C)=CC2)(C)CC1)(C)C)C '
               'NAME: 3-acetyl-ganodermadiol REASON: WRONGLY CLASSIFIED Found '
               '-OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (3R,17Z,20Z,23Z,26Z)-3-hydroxydotriacontatetraenoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 16).\n'
               ' * SMILES: '
               'O=C(OCC(O)C(O)C(O)CO)/C(=C/C(C(O)/C(=C/C(C(O)/C(=C/C(C(O[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@@H]1O)O)CO)/C(=C/C(CC(CC)C)C)/C)C)/C)C)/C)C)/C '
               'NAME: Bionectriol A REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@H](O)CCC(C)C '
               'NAME: (22R)-22-hydroxycholesterol REASON: WRONGLY CLASSIFIED '
               'Found -OH group attached to a sp3, non-aromatic carbon that is '
               'connected to an acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'O=C1OC(C2=C(O)C=CC(=C2)O)C=C1CC/C=C(/C(O)C/C=C(/COC(=O)/C=C/C3=CC=C(O)C=C3)\\C)\\CO '
               'NAME: Zizhine H REASON: WRONGLY CLASSIFIED Found -OH group '
               'attached to a sp3, non-aromatic carbon that is connected to an '
               'acyclic aliphatic chain (chain length = 6).\n'
               ' * SMILES: '
               'O=C1N[C@@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@@H](CC(N[C@@H](C(N[C@@H]1[C@H](O)C2=CC=C(O)C=C2)=O)CO)=O)C[C@@H](O)[C@@H](O)[C@@H](O[C@@H]3OC[C@@H](O)[C@@H]([C@H]3O)O)CCCCCCCCCCC)=O)[C@H](O)C(=O)N)CO)CC(=O)N)CCN '
               'NAME: Burkholidine 1215 REASON: WRONGLY CLASSIFIED Found -OH '
               'group attached to a sp3, non-aromatic carbon that is connected '
               'to an acyclic aliphatic chain (chain length = 15).\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]([C@@H](NC(=O)C)CO)[C@@H](O)[C@H](O)CO)[C@@H]1O)CO[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO)[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]6O)CO)[C@H]5NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5R,6R)-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5S,6R)-3-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-acetamido-6-[(2S,3R,4S,5R)-2-acetamido-1,4,5,6-tetrahydroxyhexan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-4-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Found -OH group attached to a sp3, '
               'non-aromatic carbon that is connected to an acyclic aliphatic '
               'chain (chain length = 6).\n'
               'False negatives: SMILES: O=C1OC([C@@H](O)\\C=C/C=C/C)CC1 NAME: '
               'Sapinofuranone A REASON: MISSED No qualifying -OH group found '
               'attached to a sp3, non-aromatic carbon with an adjoining '
               'acyclic aliphatic chain of at least 6 carbons.\n'
               ' * SMILES: '
               'O1C(C(OCC=C(C)C)COC2=C1C=C(C=C2)\\C=C/C=C(/CO)\\C(\\C(OC)=O)=C\\OC)(C)C '
               'NAME: Hydroxystrobilurin D REASON: MISSED No qualifying -OH '
               'group found attached to a sp3, non-aromatic carbon with an '
               'adjoining acyclic aliphatic chain of at least 6 carbons.\n'
               ' * SMILES: O=C(O)C[C@@H]1[C@H](CCCC(O)(C(O)C)C)C1 NAME: '
               'Cis-[2-(4,5-dihydroxy-4-methylhexyl)cyclopropyl]-acetic acid '
               'REASON: MISSED Molecule contains carboxylic acid/carboxylate '
               'functionality\n'
               ' * SMILES: O=C(CCCCC)CCO NAME: 1-Hydroxy-3-octanone REASON: '
               'MISSED No qualifying -OH group found attached to a sp3, '
               'non-aromatic carbon with an adjoining acyclic aliphatic chain '
               'of at least 6 carbons.\n'
               ' * SMILES: '
               'O=C(O[C@H]1C=CC2=C[C@@H](O)[C@@H](C[C@@]2([C@H]1C)C)O)/C=C/C=C/[C@@H](CO)CC '
               'NAME: Chaetopenoid D REASON: MISSED No qualifying -OH group '
               'found attached to a sp3, non-aromatic carbon with an adjoining '
               'acyclic aliphatic chain of at least 6 carbons.\n'
               ' * SMILES: '
               'O=C1O[C@](C(O)C(O)C=CC=C(C(=O)C)C)(C)[C@@H](C1(C)C)O NAME: '
               'Qinlactone C REASON: MISSED No qualifying -OH group found '
               'attached to a sp3, non-aromatic carbon with an adjoining '
               'acyclic aliphatic chain of at least 6 carbons.\n'
               ' * SMILES: '
               'O=C1C(=C(O)C(=C(O)C=CC=CCO)[C@H]2[C@@]1(O[C@@]3(O)[C@@](O)(CC(C([C@@]23C)=O)C(=O)CCC=CCO)C)C)C '
               'NAME: Trichobisvertinol C REASON: MISSED No qualifying -OH '
               'group found attached to a sp3, non-aromatic carbon with an '
               'adjoining acyclic aliphatic chain of at least 6 carbons.\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](C(=O)O)C)[C@@]([C@H]1C)(C=CC=CC=C(C=C(C(O)C(=CC)C)C)C)C '
               'NAME: Aspernidgulene B2 REASON: MISSED Molecule contains '
               'carboxylic acid/carboxylate functionality\n'
               ' * SMILES: '
               'O1[C@@]2(C[C@H]3C=C(C)[C@H]([C@H]([C@@H]3C[C@H]12)/C=C/C=C(/[C@@H](O)[C@H](CO)C)\\C)/C(=C/C)/C)C '
               'NAME: Fusarielin C REASON: MISSED No qualifying -OH group '
               'found attached to a sp3, non-aromatic carbon with an adjoining '
               'acyclic aliphatic chain of at least 6 carbons.\n'
               ' * SMILES: '
               'O=C1C=C([C@@H](O)[C@H]2[C@@]1(O2)[C@@H](O)/C=C(/CC[C@@]3(C(=CCC[C@H]3C)C)C)\\C)COC(=O)C[C@H](O)C '
               'NAME: Nectrianolin B REASON: MISSED No qualifying -OH group '
               'found attached to a sp3, non-aromatic carbon with an adjoining '
               'acyclic aliphatic chain of at least 6 carbons.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule contains carboxylic '
                                               'acid/carboxylate '
                                               'functionality'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule contains carboxylic '
                                               'acid/carboxylate '
                                               'functionality'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No qualifying -OH group found '
                                               'attached to a sp3, '
                                               'non-aromatic carbon with an '
                                               'adjoining acyclic aliphatic '
                                               'chain of at least 6 carbons.'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1OC([C@@H](O)\\C=C/C=C/C)CC1',
                                      'name': 'Sapinofuranone A',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O1C(C(OCC=C(C)C)COC2=C1C=C(C=C2)\\C=C/C=C(/CO)\\C(\\C(OC)=O)=C\\OC)(C)C',
                                      'name': 'Hydroxystrobilurin D',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O=C(O)C[C@@H]1[C@H](CCCC(O)(C(O)C)C)C1',
                                      'name': 'Cis-[2-(4,5-dihydroxy-4-methylhexyl)cyclopropyl]-acetic '
                                              'acid',
                                      'reason': 'Molecule contains carboxylic '
                                                'acid/carboxylate '
                                                'functionality'},
                                  {   'smiles': 'O=C(CCCCC)CCO',
                                      'name': '1-Hydroxy-3-octanone',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O=C(O[C@H]1C=CC2=C[C@@H](O)[C@@H](C[C@@]2([C@H]1C)C)O)/C=C/C=C/[C@@H](CO)CC',
                                      'name': 'Chaetopenoid D',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O=C1O[C@](C(O)C(O)C=CC=C(C(=O)C)C)(C)[C@@H](C1(C)C)O',
                                      'name': 'Qinlactone C',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O=C1C(=C(O)C(=C(O)C=CC=CCO)[C@H]2[C@@]1(O[C@@]3(O)[C@@](O)(CC(C([C@@]23C)=O)C(=O)CCC=CCO)C)C)C',
                                      'name': 'Trichobisvertinol C',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O=C1O[C@@H]([C@H](C(=O)O)C)[C@@]([C@H]1C)(C=CC=CC=C(C=C(C(O)C(=CC)C)C)C)C',
                                      'name': 'Aspernidgulene B2',
                                      'reason': 'Molecule contains carboxylic '
                                                'acid/carboxylate '
                                                'functionality'},
                                  {   'smiles': 'OC(CC(O)CO)C(O)CO',
                                      'name': '3-deoxyhexitol',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 carbons.'},
                                  {   'smiles': 'O1[C@@]2(C[C@H]3C=C(C)[C@H]([C@H]([C@@H]3C[C@H]12)/C=C/C=C(/[C@@H](O)[C@H](CO)C)\\C)/C(=C/C)/C)C',
                                      'name': 'Fusarielin C',
                                      'reason': 'No qualifying -OH group found '
                                                'attached to a sp3, '
                                                'non-aromatic carbon with an '
                                                'adjoining acyclic aliphatic '
                                                'chain of at least 6 '
                                                'carbons.'}],
    'attempt': 5,
    'reasoning': 'Below is one possible solution. In our reasoning we noticed '
                 'that the previous code was “triggering” on any –OH that '
                 'happens to sit on a sp³ carbon with any detectable aliphatic '
                 'chain—yet many molecules (or parts of molecules) that '
                 'otherwise are highly decorated with functional groups (or '
                 'have remote aromatic/carbonyl groups) can “fake” a chain. '
                 'Our improved version first excludes carboxylic '
                 'acid/carboxylate groups, then for each free –OH we require '
                 'that it be attached to a saturated (sp³), non‐aromatic '
                 'carbon. From that candidate carbon we “walk” along '
                 'contiguous chain carbons (disallowing rings and aromatic '
                 'atoms and also avoiding “carbonyl‐like” carbons) using a DFS '
                 'that (in each branch) allows at most two isolated sp² '
                 'centers. (Note that our DFS is a backtracking search so that '
                 'each branch has its own visited set.) If one branch returns '
                 'a chain (not counting the –OH–bearing carbon itself) of at '
                 'least six carbons then we classify the molecule as an '
                 'aliphatic alcohol. You can adjust the tolerance (here, two '
                 'allowed sp² atoms) and the minimum chain length if needed.\n'
                 '\n'
                 'Below is our complete code in one Python code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 377,
    'num_false_positives': 3039,
    'num_true_negatives': 138530,
    'num_false_negatives': 354,
    'num_negatives': None,
    'precision': 0.11036299765807962,
    'recall': 0.5157318741450069,
    'f1': 0.1818181818181818,
    'accuracy': 0.9761560084328883,
    'negative_predictive_value': 0.9974511102790818}