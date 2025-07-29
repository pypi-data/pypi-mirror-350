"""
Classifies: CHEBI:26208 polyunsaturated fatty acid
"""
"""
Classifies: Polyunsaturated Fatty Acid
Definition: A fatty acid is defined here as a molecule having a terminal carboxylic acid group 
attached to a single, linear, non‐aromatic aliphatic chain containing more than one 
non‐aromatic C=C double bond.
Additional criteria:
  - The acid carbon in the terminal –COOH group must be attached to exactly one carbon.
  - The chain is “traced” by starting from that unique neighbor and then following the only 
    available non‐aromatic, non‐ring carbon link at each step. If at any stage a branching is encountered,
    we reject the molecule.
  - Bonds of type triple are not allowed in the chain.
  - The chain must have a minimum number of carbons (here 8) and at least two non‐aromatic C=C bonds.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polyunsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule qualifies as a polyunsaturated fatty acid (PUFA).
    The criteria are:
      1. The molecule has a terminal carboxylic acid group. The carbon in the COOH must
         be bonded to exactly one carbon (thus marking the start of the chain).
      2. Starting from the chain-start carbon (the unique neighbor of the acid carbon),
         we trace a linear (non-branched), acyclic, non-aromatic chain comprising carbon atoms.
         If branching (more than one candidate) is encountered, the molecule is rejected.
      3. The chain must be at least MIN_CHAIN_LENGTH carbons long.
      4. Along the chain (i.e. between consecutive carbons in the traversed path), there must be 
         at least 2 non-aromatic double bonds (and no triple bonds).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule qualifies as a PUFA, False otherwise.
        str: Explanation for the classification decision.
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Identify a carboxylic acid (COOH) group using SMARTS.
    # The pattern matches a carbon (sp2) with one double-bonded oxygen and one hydroxyl.
    ca_smarts = "[CX3](=O)[O;H]"
    ca_group = Chem.MolFromSmarts(ca_smarts)
    ca_matches = mol.GetSubstructMatches(ca_group)
    if not ca_matches:
        return False, "No carboxylic acid group found; not a fatty acid"
    
    # 2. Among the acid groups, select one that is terminal.
    # That is, the acid carbon should be attached to exactly one carbon (the start of the chain).
    terminal_acid_found = False
    acid_atom = None
    chain_start = None
    for match in ca_matches:
        # match[0] is taken as the acid carbon (which is part of the COOH group)
        acid_c = mol.GetAtomWithIdx(match[0])
        # Look for neighboring carbon atoms (atomic number 6)
        carbon_neighbors = [nbr for nbr in acid_c.GetNeighbors() if nbr.GetAtomicNum() == 6]
        if len(carbon_neighbors) == 1:
            terminal_acid_found = True
            acid_atom = acid_c
            chain_start = carbon_neighbors[0]
            break
    if not terminal_acid_found or chain_start is None:
        return False, "Carboxylic acid group is not terminal; not a typical fatty acid"

    # 3. Trace the acyl chain starting at chain_start.
    # We “walk” along the chain by taking at each step the only possible non-aromatic,
    # non-ring carbon neighbor (excluding the atom we came from).
    chain_indices = []  # indices of carbon atoms in the chain
    current = chain_start
    previous = acid_atom  # the acid carbon is the previous atom at start
    chain_indices.append(current.GetIdx())

    while True:
        # Get neighbors that are carbons, non-aromatic, not in a ring
        candidates = []
        for nbr in current.GetNeighbors():
            # Exclude the atom we came from
            if nbr.GetIdx() == previous.GetIdx():
                continue
            if nbr.GetAtomicNum() != 6:
                continue
            if nbr.GetIsAromatic() or nbr.IsInRing():
                continue
            candidates.append(nbr)
        if len(candidates) == 0:
            # reached an endpoint
            break
        if len(candidates) > 1:
            return False, "Acyl chain is branched; expected a single linear chain for a typical fatty acid"
        # Proceed to the only candidate neighbor
        next_atom = candidates[0]
        chain_indices.append(next_atom.GetIdx())
        previous = current
        current = next_atom

    chain_length = len(chain_indices)
    MIN_CHAIN_LENGTH = 8
    if chain_length < MIN_CHAIN_LENGTH:
        return False, f"Fatty acid chain length only {chain_length} carbons; too short to be typical"
    
    # 4. Count the number of non-aromatic double bonds along the traced chain.
    double_bond_count = 0
    for i in range(len(chain_indices)-1):
        bond = mol.GetBondBetweenAtoms(chain_indices[i], chain_indices[i+1])
        if bond is None:
            continue
        # Reject if a triple bond is found in the chain.
        if bond.GetBondType() == Chem.BondType.TRIPLE:
            return False, "Chain contains a carbon–carbon triple bond which is not allowed in typical fatty acids"
        # Count non-aromatic double bonds.
        if bond.GetBondType() == Chem.BondType.DOUBLE and not bond.GetIsAromatic():
            double_bond_count += 1

    if double_bond_count <= 1:
        return False, f"Found {double_bond_count} non-aromatic C=C bond(s) in chain; need more than one to qualify as polyunsaturated"

    # Form a reason message including chain length and double bond count.
    reason = (f"Contains a terminal carboxylic acid group attached to a linear chain of {chain_length} carbons "
              f"with {double_bond_count} non-aromatic double bonds; qualifies as a polyunsaturated fatty acid")
    return True, reason


# Example usage:
if __name__ == "__main__":
    # Test with one example, resolvin D6
    test_smiles = "C(C(O)=O)C[C@@H](/C=C/C=C\\C/C=C\\C/C=C\\C=C\\[C@H](C/C=C\\CC)O)O"
    result, explanation = is_polyunsaturated_fatty_acid(test_smiles)
    print(result, explanation)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26208',
                          'name': 'polyunsaturated fatty acid',
                          'definition': 'Any fatty acid containing more than '
                                        'one double bond. Acids in this group '
                                        'are reported to have cardioprotective '
                                        'effects; and levels are lowered in '
                                        'chronic fatigue syndrome.',
                          'parents': ['CHEBI:27208'],
                          'xrefs': [   'PMID:14977874',
                                       'PMID:16380690',
                                       'PMID:17891522'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 100,
                           'log_lines_of_code': 4.605170185988092,
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
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
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
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetIdx',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetBondType',
                                                 'IsInRing',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['ca_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_polyunsaturated_fatty_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No carboxylic acid group '
                                          'found; not a fatty acid"',
                                          'False, "Carboxylic acid group is '
                                          'not terminal; not a typical fatty '
                                          'acid"',
                                          'False, "Acyl chain is branched; '
                                          'expected a single linear chain for '
                                          'a typical fatty acid"',
                                          'False, f"Fatty acid chain length '
                                          'only {chain_length} carbons; too '
                                          'short to be typical"',
                                          'False, "Chain contains a '
                                          'carbon–carbon triple bond which is '
                                          'not allowed in typical fatty acids"',
                                          'False, f"Found {double_bond_count} '
                                          'non-aromatic C=C bond(s) in chain; '
                                          'need more than one to qualify as '
                                          'polyunsaturated"',
                                          'True, reason'],
                           'returns_count': 8,
                           'complexity': 5.921034037197619},
    'message': '\n'
               'Attempt failed: F1 score of 0.5995694294940795 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C(C(O)=O)C[C@@H](/C=C/C=C\\C/C=C\\C/C=C\\C=C\\[C@H](C/C=C\\CC)O)O '
               'NAME: resolvin D6 REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 21 carbons '
               'and 6 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: CCCCCCC/C=C/C=C/C=C/C=C/C=C/C(=O)O NAME: '
               '(2E,4E,6E,8E,10E)-octadecapentaenoic acid REASON: CORRECT '
               'Contains a terminal carboxylic acid group attached to a linear '
               'chain of 17 carbons and 5 non-aromatic double bonds; qualifies '
               'as a polyunsaturated fatty acid\n'
               ' * SMILES: CC\\C(CC[C@H]1O[C@@]1(C)CC)=C/CC\\C(C)=C\\C(O)=O '
               'NAME: juvenile hormone I acid REASON: CORRECT Contains a '
               'terminal carboxylic acid group attached to a linear chain of 8 '
               'carbons and 2 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C[C@H](\\C=C\\C=C/C=C/C=C/[C@H]([C@@H](C/C=C\\CC)O)O)O '
               'NAME: aspirin-triggered resolvin D2 REASON: CORRECT Contains a '
               'terminal carboxylic acid group attached to a linear chain of '
               '21 carbons and 6 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: CC(C)=CCCC(C)=CCCC(C)=CC(O)=O NAME: farnesoic acid '
               'REASON: CORRECT Contains a terminal carboxylic acid group '
               'attached to a linear chain of 11 carbons and 3 non-aromatic '
               'double bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@@H]1O[C@H]1\\C=C\\[C@H](O)C\\C=C/CCCC(O)=O '
               'NAME: (8R)-hydroxy-(11S,12S)-epoxyicosa-(5Z,9E,14Z)-trienoic '
               'acid REASON: CORRECT Contains a terminal carboxylic acid group '
               'attached to a linear chain of 9 carbons and 2 non-aromatic '
               'double bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: O[C@H](CCC)C/C=C\\C/C=C\\CCCCCCCC(O)=O NAME: '
               'Avenoleic acid REASON: CORRECT Contains a terminal carboxylic '
               'acid group attached to a linear chain of 17 carbons and 2 '
               'non-aromatic double bonds; qualifies as a polyunsaturated '
               'fatty acid\n'
               ' * SMILES: '
               'C(C(/C=C/C=C/C=C\\[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC=O NAME: '
               '12,20-dioxoleukotriene B4 REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: CC\\C=C/C\\C=C/C[C@H](OO)\\C=C\\CCCCCCC(O)=O NAME: '
               '(8E,10S,12Z,15Z)-10-hydroperoxyoctadeca-8,12,15-trienoic acid '
               'REASON: CORRECT Contains a terminal carboxylic acid group '
               'attached to a linear chain of 17 carbons and 3 non-aromatic '
               'double bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: OC(=O)CCCCCCC\\C=C/C=C/C(=O)C/C=C\\CC NAME: '
               '13-keto-9Z,11E,15Z-octadecatrienoic acid REASON: CORRECT '
               'Contains a terminal carboxylic acid group attached to a linear '
               'chain of 17 carbons and 3 non-aromatic double bonds; qualifies '
               'as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@@H](O)\\C=C\\C=C/C=C/[C@@H](O)CCCC(O)=O NAME: '
               'Delta(6)-trans,Delta(8)-cis-leukotriene B4 REASON: CORRECT '
               'Contains a terminal carboxylic acid group attached to a linear '
               'chain of 19 carbons and 4 non-aromatic double bonds; qualifies '
               'as a polyunsaturated fatty acid\n'
               ' * SMILES: CCCCC[C@H](OO)\\C=C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 15(S)-HPETE REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: CCCCC\\C=C/C=C/[C@H](O)C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 11(R)-HETE REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: [H]C(CCC=C([H])C=C([H])CCCC(O)=O)=CCC([H])=CCCCCC '
               'NAME: icosa-5,7,11,14-tetraenoic acid REASON: CORRECT Contains '
               'a terminal carboxylic acid group attached to a linear chain of '
               '19 carbons and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'C(/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)=C\\[C@H]([C@H](CCCC(O)=O)O)O '
               'NAME: '
               '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoic '
               'acid REASON: CORRECT Contains a terminal carboxylic acid group '
               'attached to a linear chain of 19 carbons and 4 non-aromatic '
               'double bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C=C/[C@@H](C\\C=C/CCCC(O)=O)OO '
               'NAME: 8(R)-HPETE REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C/C=C\\C/C=C\\C\\C=C/C=C/C(C/C=C\\CC)=O NAME: '
               '(4Z,7Z,10Z,13Z,15E,19Z)-17-oxodocosahexaenoic acid REASON: '
               'CORRECT Contains a terminal carboxylic acid group attached to '
               'a linear chain of 21 carbons and 6 non-aromatic double bonds; '
               'qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'C(\\CC)=C\\C\\C=C/C=C/[C@@H](C/C=C\\C/C=C\\CCCCCC(=O)O)O NAME: '
               '(7Z,10Z,13R,14E,16Z,19Z)-13-hydroxydocosapentaenoic acid '
               'REASON: CORRECT Contains a terminal carboxylic acid group '
               'attached to a linear chain of 21 carbons and 5 non-aromatic '
               'double bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: CCCCC[C@@H](O)\\C=C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 15(R)-HETE REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'S([C@H]([C@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\C/C=C\\CC)C[C@H](N)C(=O)NCC(O)=O '
               'NAME: Leukotriene D5 REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 5 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: C(C(O)=O)CCCC/C=C\\C/C=C\\C\\C=C/C=C/C(C/C=C\\CC)=O '
               'NAME: (7Z,10Z,13Z,15E,19Z)-17-oxodocosapentaenoic acid REASON: '
               'CORRECT Contains a terminal carboxylic acid group attached to '
               'a linear chain of 21 carbons and 5 non-aromatic double bonds; '
               'qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: C(=CC=C/C=C/C(C(C/C=C\\CC)O)O)C=CC(CCCCCC(O)=O)O '
               'NAME: '
               '7,16,17-trihydroxy-(14E,19Z)-docosa-8,10,12,14,19-pentaenoic '
               'acid REASON: CORRECT Contains a terminal carboxylic acid group '
               'attached to a linear chain of 21 carbons and 5 non-aromatic '
               'double bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC)C[C@H](N)C(=O)N[C@H]([C@H](O)\\C=C\\CCCCCCCCCCCC)CO '
               'NAME: Cer(d17:1/LTE4) REASON: CORRECT Contains a terminal '
               'carboxylic acid group attached to a linear chain of 19 carbons '
               'and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: C(\\C=C/CCCCCCCC(=O)O)=C/C(C/C=C\\CC)OO NAME: '
               '(9Z,11E,15Z)-13-hydroperoxyoctadecatrienoic acid REASON: '
               'CORRECT Contains a terminal carboxylic acid group attached to '
               'a linear chain of 17 carbons and 3 non-aromatic double bonds; '
               'qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: OC(=O)CCCCCCCC/C=C/C=C/C=C/CCC NAME: '
               '10,12,14-octadecatrienoic acid REASON: CORRECT Contains a '
               'terminal carboxylic acid group attached to a linear chain of '
               '17 carbons and 3 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               'False positives: SMILES: '
               'OC(=O)\\C=C(/C=C/C=C(\\C=C\\C=1C(CCCC1C)(C)C)/C)\\C NAME: '
               '9,13-cis-Retinoic acid REASON: WRONGLY CLASSIFIED Contains a '
               'terminal carboxylic acid group attached to a linear chain of 8 '
               'carbons and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: OC(=O)CCCC/C=C/C=C/C#C\\C=C\\C=C\\C NAME: '
               '6E,8E,12E,14E-Hexadecatetraen-10-ynoic acid REASON: WRONGLY '
               'CLASSIFIED Contains a terminal carboxylic acid group attached '
               'to a linear chain of 15 carbons and 4 non-aromatic double '
               'bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: CCCCCC/C=C\\C/C=C\\CCCCCCCCCCCCC(O)=O NAME: '
               'Prenateic acid REASON: WRONGLY CLASSIFIED Contains a terminal '
               'carboxylic acid group attached to a linear chain of 23 carbons '
               'and 2 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'CC(=O)NC(CS[C@H](\\C=C\\C=C\\C=C/C\\C=C/CCCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O '
               'NAME: omega-Carboxy-N-acetyl-LTE4 REASON: WRONGLY CLASSIFIED '
               'Contains a terminal carboxylic acid group attached to a linear '
               'chain of 19 carbons and 4 non-aromatic double bonds; qualifies '
               'as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'O=C(O)C(C(O)/C(=C/C(C(O)/C=C/C(C(O)/C=C/C(C(O)/C(=C/C(CO)CC(CC)C)/C)C)C)C)/C)C '
               'NAME: Cubensic acid REASON: WRONGLY CLASSIFIED Contains a '
               'terminal carboxylic acid group attached to a linear chain of '
               '21 carbons and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'O[C@@H](CCCC(O)=O)\\C=C/C=C/C=C/[C@H](O)C\\C=C/CCC(O)=O NAME: '
               '18-hydroxy-18-oxo-dinorleukotriene B4 REASON: WRONGLY '
               'CLASSIFIED Contains a terminal carboxylic acid group attached '
               'to a linear chain of 17 carbons and 4 non-aromatic double '
               'bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: O=C(O)CC/C=C/C[C@H](OC)/C=C(/CCCCCCC)\\C NAME: '
               '7-methoxy-9-methylhexadecadienoic acid REASON: WRONGLY '
               'CLASSIFIED Contains a terminal carboxylic acid group attached '
               'to a linear chain of 15 carbons and 2 non-aromatic double '
               'bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'O=C(O)/C(=C/C=C/C=C/C=C/CC/C=C/C(C(O)C(C(O)/C=C/C=C/C=CC=C/C=C/CC(O)C(C(=O)CC(O)CC(O)CC(O)/C=C/CC(O)CC(O)CC(O)CC(O)/C=C/CC(O)/C=C/CC(O)CC(O)CCCN)C)C)C)/C '
               'NAME: Linearmycin A REASON: WRONGLY CLASSIFIED Contains a '
               'terminal carboxylic acid group attached to a linear chain of '
               '59 carbons and 13 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: O=C(O)CCCCC=C=CC#CC#CC(O)CC NAME: Phomallenic acid '
               'A REASON: WRONGLY CLASSIFIED Contains a terminal carboxylic '
               'acid group attached to a linear chain of 14 carbons and 2 '
               'non-aromatic double bonds; qualifies as a polyunsaturated '
               'fatty acid\n'
               ' * SMILES: CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC(O)=O NAME: '
               'Vaneic acid REASON: WRONGLY CLASSIFIED Contains a terminal '
               'carboxylic acid group attached to a linear chain of 21 carbons '
               'and 3 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: OC(=O)CCCCC/C=C/C=C\\CCCCCCCC NAME: '
               '7-trans,9-cis-octadecadienoic acid REASON: WRONGLY CLASSIFIED '
               'Contains a terminal carboxylic acid group attached to a linear '
               'chain of 17 carbons and 2 non-aromatic double bonds; qualifies '
               'as a polyunsaturated fatty acid\n'
               ' * SMILES: '
               'O[C@@H](CCCC(O)=O)\\C=C/C=C/C=C/[C@H](O)C\\C=C/CCCCC(O)=O '
               'NAME: 20-hydroxy-20-oxoleukotriene B4 REASON: WRONGLY '
               'CLASSIFIED Contains a terminal carboxylic acid group attached '
               'to a linear chain of 19 carbons and 4 non-aromatic double '
               'bonds; qualifies as a polyunsaturated fatty acid\n'
               ' * SMILES: Cl\\C(=C/C=C/C=C/C=C/C=C/C(O)=O)\\C NAME: aurantoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a terminal carboxylic '
               'acid group attached to a linear chain of 11 carbons and 5 '
               'non-aromatic double bonds; qualifies as a polyunsaturated '
               'fatty acid\n'
               ' * SMILES: '
               'O=C(O)/C=C/C=C/C=C/CCNC(=O)[C@H]([C@@H](O)CNC(=O)C/C=C(/C=C/C(O)CCCCCCCCC)\\C)C '
               'NAME: Pseudotrienic acid A REASON: WRONGLY CLASSIFIED Contains '
               'a terminal carboxylic acid group attached to a linear chain of '
               '8 carbons and 3 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: OC(=O)CCC/C=C\\CC/C=C\\CCCCCCCCCC/C=C\\CCCCCC NAME: '
               '28:3(5Z,9Z,21Z) REASON: WRONGLY CLASSIFIED Contains a terminal '
               'carboxylic acid group attached to a linear chain of 27 carbons '
               'and 3 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: OC(=O)\\C=C\\CCCC/C=C\\CCC NAME: '
               '2E,8Z-dodecadienoic acid REASON: WRONGLY CLASSIFIED Contains a '
               'terminal carboxylic acid group attached to a linear chain of '
               '11 carbons and 2 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: OC(CCCCC(C/C(/C)=C/C(/C)=C/C(O)=O)C)C(CO)C(OC)=O '
               'NAME: '
               '(2E,4E)-12-Hydroxy-13-(hydroxymethyl)-14-methoxy-3,5,7-trimethyl-14-oxotetradeca-2,4-dienoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a terminal carboxylic '
               'acid group attached to a linear chain of 13 carbons and 2 '
               'non-aromatic double bonds; qualifies as a polyunsaturated '
               'fatty acid\n'
               ' * SMILES: '
               'O=C(O)/C=C/C=C/C=C/C=C/[C@@]1([C@@H](C(=C[C@H]2[C@H]1CC[C@@H]([C@@H]2O)C)C)/C(=C/C)/C)C '
               'NAME: Janthinopolyenemycin A REASON: WRONGLY CLASSIFIED '
               'Contains a terminal carboxylic acid group attached to a linear '
               'chain of 8 carbons and 4 non-aromatic double bonds; qualifies '
               'as a polyunsaturated fatty acid\n'
               ' * SMILES: O=C(O)C/C=C/C=C/C=C(\\C1=C(C=C(C)C=C1)/C=C\\CC)/C '
               'NAME: MF-EA-705beta REASON: WRONGLY CLASSIFIED Contains a '
               'terminal carboxylic acid group attached to a linear chain of 8 '
               'carbons and 3 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC NAME: '
               'TrHA REASON: WRONGLY CLASSIFIED Contains a terminal carboxylic '
               'acid group attached to a linear chain of 22 carbons and 6 '
               'non-aromatic double bonds; qualifies as a polyunsaturated '
               'fatty acid\n'
               ' * SMILES: O=C(O)/C=C/C=C\\[C@@H](O)CCCCCCCCCCCCCCCC NAME: '
               'Pantheric acid A REASON: WRONGLY CLASSIFIED Contains a '
               'terminal carboxylic acid group attached to a linear chain of '
               '21 carbons and 2 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: O=C(O)CC/C(=C/CC/C=C/C(CC(C(=O)C)C)C)/C NAME: '
               'Streptoone B REASON: WRONGLY CLASSIFIED Contains a terminal '
               'carboxylic acid group attached to a linear chain of 13 carbons '
               'and 2 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: CC(\\C=C\\C1=C(C)CCCC1(C)C)=C\\C=C\\C(C)=C\\C(O)=O '
               'NAME: 9-cis-retinoic acid REASON: WRONGLY CLASSIFIED Contains '
               'a terminal carboxylic acid group attached to a linear chain of '
               '8 carbons and 4 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               ' * SMILES: '
               'O=C(OC1OC(C(O)C(C1OC(=O)CCCCCCCCCC=CCCCCCC)O)CO)C(=CC=CC(=CC=CC(=CC=CC=C(C=CC=C(C=CC=C(C(=O)O)C)C)C)C)C)C '
               'NAME: '
               '4-[2-O-11Z-octadecenoyl-beta-glucopyranosyl]-4,4′-diapolycopene-4,4′-dioic '
               'acid REASON: WRONGLY CLASSIFIED Contains a terminal carboxylic '
               'acid group attached to a linear chain of 23 carbons and 11 '
               'non-aromatic double bonds; qualifies as a polyunsaturated '
               'fatty acid\n'
               ' * SMILES: '
               'O=C1C=C([C@@H](O)[C@H]([C@H]1CC=C(CCC=C(CCC(=O)O)C)C)O)C NAME: '
               'Peniginsengin C REASON: WRONGLY CLASSIFIED Contains a terminal '
               'carboxylic acid group attached to a linear chain of 9 carbons '
               'and 2 non-aromatic double bonds; qualifies as a '
               'polyunsaturated fatty acid\n'
               'False negatives: SMILES: '
               'CCCCC\\C=C/C\\C=C/C=C/C=C/[C@@H]1O[C@H]1CCCC(O)=O NAME: '
               'leukotriene A4 REASON: MISSED Fatty acid chain length only 3 '
               'carbons; too short to be typical\n'
               ' * SMILES: [H]C(C)=CC([H])=CC(O)=O NAME: sorbic acid REASON: '
               'MISSED Fatty acid chain length only 5 carbons; too short to be '
               'typical\n'
               ' * SMILES: '
               'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\C/C=C\\CCC(O)=O '
               'NAME: '
               '16(S)-glutathionyl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
               'acid REASON: MISSED Fatty acid chain length only 4 carbons; '
               'too short to be typical\n'
               ' * SMILES: OC(CCCCC)/C=C/C(=O)CCCCCCCCC(O)=O NAME: '
               '(11E)-13-hydroxy-10-oxo-11-octadecenoic acid REASON: MISSED '
               'Found 1 non-aromatic C=C bond(s) in chain; need more than one '
               'to qualify as polyunsaturated\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/CC1OC1CCCC(O)=O NAME: '
               '5,6-EET REASON: MISSED Fatty acid chain length only 3 carbons; '
               'too short to be typical\n'
               ' * SMILES: '
               'N[C@H](C(=O)O)CS[C@H](/C=C/C=C/C=C\\C/C=C\\CCC(O)=O)[C@H](C/C=C\\C/C=C\\CC)O '
               'NAME: '
               '(13R)-S-cysteinyl-(14S)-hydroxy-(4Z,7Z,9E,11E,16Z,19Z)-docosahexaenoic '
               'acid REASON: MISSED Fatty acid chain length only 2 carbons; '
               'too short to be typical\n'
               ' * SMILES: OC(=O)C(\\O)=C\\C=C NAME: '
               '(2Z)-2-hydroxypenta-2,4-dienoic acid REASON: MISSED Fatty acid '
               'chain length only 4 carbons; too short to be typical\n'
               ' * SMILES: C(CCCO)C/C=C\\C/C=C\\CC1C(C/C=C\\CCCC(O)=O)O1 NAME: '
               '8,9-epoxy-20-hydroxy-(5Z,11Z,14Z)-icosatrienoic acid REASON: '
               'MISSED Fatty acid chain length only 6 carbons; too short to be '
               'typical\n'
               ' * SMILES: CCCCCCCCC#CCC#CCC#CCCCC(O)=O NAME: '
               '5,8,11-icosatriynoic acid REASON: MISSED Found 0 non-aromatic '
               'C=C bond(s) in chain; need more than one to qualify as '
               'polyunsaturated\n'
               ' * SMILES: '
               'CCCCC[C@H](O)\\C=C\\C=C/C=C/C=C/[C@@H]1O[C@H]1CCCC(O)=O NAME: '
               '5,6-Ep-15S-HETE REASON: MISSED Fatty acid chain length only 3 '
               'carbons; too short to be typical\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Fatty acid chain length only 1 '
                                               'carbons; too short to be '
                                               'typical'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No carboxylic acid group '
                                               'found; not a fatty acid'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCC\\C=C/C\\C=C/C=C/C=C/[C@@H]1O[C@H]1CCCC(O)=O',
                                      'name': 'leukotriene A4',
                                      'reason': 'Fatty acid chain length only '
                                                '3 carbons; too short to be '
                                                'typical'},
                                  {   'smiles': 'CC\\C(CC[C@H]1O[C@@]1(C)CC)=C/CC\\C(C)=C\\C(O)=O',
                                      'name': 'juvenile hormone I acid',
                                      'reason': 'Acyl chain is branched; '
                                                'expected a single linear '
                                                'chain for a typical fatty '
                                                'acid'},
                                  {   'smiles': 'CC(C)=CCCC(C)=CCCC(C)=CC(O)=O',
                                      'name': 'farnesoic acid',
                                      'reason': 'Acyl chain is branched; '
                                                'expected a single linear '
                                                'chain for a typical fatty '
                                                'acid'},
                                  {   'smiles': '[H]C(C)=CC([H])=CC(O)=O',
                                      'name': 'sorbic acid',
                                      'reason': 'Fatty acid chain length only '
                                                '5 carbons; too short to be '
                                                'typical'},
                                  {   'smiles': 'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\C/C=C\\CCC(O)=O',
                                      'name': '16(S)-glutathionyl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
                                              'acid',
                                      'reason': 'Fatty acid chain length only '
                                                '4 carbons; too short to be '
                                                'typical'},
                                  {   'smiles': 'OC(CCCCC)/C=C/C(=O)CCCCCCCCC(O)=O',
                                      'name': '(11E)-13-hydroxy-10-oxo-11-octadecenoic '
                                              'acid',
                                      'reason': 'Found 1 non-aromatic C=C '
                                                'bond(s) in chain; need more '
                                                'than one to qualify as '
                                                'polyunsaturated'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/CC1OC1CCCC(O)=O',
                                      'name': '5,6-EET',
                                      'reason': 'Fatty acid chain length only '
                                                '3 carbons; too short to be '
                                                'typical'},
                                  {   'smiles': 'O=C1OC(=O)C2C(C(C(C)=CC3C2CCC(C3O[C@H]4O[C@H]([C@H](O)C([C@@H]4O)=O)C)C)/C=C/C=C/C=C(/CC(CC(O)C(C(=O)O)C)C)\\C)=C5C(=C1C)CC(O)C5C',
                                      'name': 'Aurantinin B',
                                      'reason': 'Acyl chain is branched; '
                                                'expected a single linear '
                                                'chain for a typical fatty '
                                                'acid'},
                                  {   'smiles': 'N[C@H](C(=O)O)CS[C@H](/C=C/C=C/C=C\\C/C=C\\CCC(O)=O)[C@H](C/C=C\\C/C=C\\CC)O',
                                      'name': '(13R)-S-cysteinyl-(14S)-hydroxy-(4Z,7Z,9E,11E,16Z,19Z)-docosahexaenoic '
                                              'acid',
                                      'reason': 'Fatty acid chain length only '
                                                '2 carbons; too short to be '
                                                'typical'},
                                  {   'smiles': 'CC(\\C=C\\C=C(/C)C(O)=O)=C/C=C/C=C(C)/C=C/C=C(\\C)C(O)=O',
                                      'name': 'crocetin',
                                      'reason': 'Acyl chain is branched; '
                                                'expected a single linear '
                                                'chain for a typical fatty '
                                                'acid'}],
    'attempt': 4,
    'reasoning': 'Below is one way to improve the extraction of the “aliphatic '
                 'chain” so that false positives (due to including unsuitably '
                 'branched, aromatic, or triple‐bond–containing structures) '
                 'and false negatives (chains that are too short) are reduced. '
                 'One idea is to “trace” the chain directly from the acid '
                 'group by following a unique non‐aromatic, non‐ring, sp2/sp3 '
                 'carbon‐to‐carbon connection. (If at any point more than one '
                 'forward step is possible the chain is taken to be branched '
                 'and the molecule is rejected.) In addition, we explicitly '
                 'reject any bond that is a triple bond and only count the '
                 'non‐aromatic double bonds along the traced path. Finally, we '
                 'require a minimum chain length (here 8 carbons) and at least '
                 'two non‐aromatic C=C bonds. One may tune these criteria '
                 'further if needed.\n'
                 '\n'
                 'Below is the complete Python program using RDKit in a single '
                 'code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 536,
    'num_false_positives': 368,
    'num_true_negatives': 141324,
    'num_false_negatives': 72,
    'num_negatives': None,
    'precision': 0.5929203539823009,
    'recall': 0.881578947368421,
    'f1': 0.7089947089947091,
    'accuracy': 0.9969079409697822,
    'negative_predictive_value': 0.9994907918187219}