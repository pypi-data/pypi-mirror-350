"""
Classifies: CHEBI:59845 3-hydroxy fatty acid
"""
"""
Classifies: CHEBI entry for 3-hydroxy fatty acids.
Definition: Any fatty acid with a hydroxy functional group in the beta- (3-) position.
This implementation checks that the molecule contains a terminal (free) carboxylic acid 
group, that the carbon directly alpha to the acid is linked to a beta carbon bearing an –OH,
and that the attached alkyl chain is sufficiently long and linear.
"""

from rdkit import Chem

def is_3_hydroxy_fatty_acid(smiles: str):
    """
    Determines if a molecule is a 3-hydroxy fatty acid based on its SMILES string.
    A valid 3-hydroxy fatty acid must have:
      1. A free (terminal) carboxylic acid group (COOH).
      2. The carbon directly alpha to the acid must be connected to a beta carbon 
         that carries an –OH group.
      3. The aliphatic chain (from the acid group onward) should be sufficiently long,
         suggesting a fatty acid rather than a fragment of a larger (e.g., polycyclic) structure.
         
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is a 3-hydroxy fatty acid, False otherwise.
        str: Explanation of the classification decision.
    """
    # Attempt to parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # First, search for a free carboxylic acid group.
    # The SMARTS below looks for a carbon (sp2) with a double bond to O and a single bond to an OH.
    acid_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")
    acid_matches = mol.GetSubstructMatches(acid_pattern)
    if not acid_matches:
        return False, "No carboxylic acid (COOH) group found"
    
    # For each carboxylic acid match, try to verify the beta-hydroxy fatty acid motif.
    for match in acid_matches:
        # In this SMARTS, match[0] is the acid carbon.
        acid_idx = match[0]
        acid_atom = mol.GetAtomWithIdx(acid_idx)
        
        # For a terminal (free) acid group, the acid carbon should be attached to exactly one carbon.
        # (The other bond goes to the -OH.)
        carbon_neighbors = [n for n in acid_atom.GetNeighbors() if n.GetAtomicNum() == 6]
        if len(carbon_neighbors) != 1:
            # Skip if acid carbon is not terminal (e.g. if it is connected to more than one carbon).
            continue
        
        # Also, if the acid carbon is in a ring, it likely does not belong to a fatty acid.
        if acid_atom.IsInRing():
            continue
        
        # Identify the alpha carbon (the carbon bonded to the acid carbon).
        alpha_atom = carbon_neighbors[0]
        
        # Look for the beta carbon. For a conventional fatty acid, the alpha carbon should have 
        # one carbon neighbor besides the acid carbon.
        beta_candidates = [n for n in alpha_atom.GetNeighbors() if n.GetIdx() != acid_idx and n.GetAtomicNum() == 6]
        if not beta_candidates:
            continue  # no beta carbon found, so move to next acid match.
        
        # Check whether any beta candidate carries a hydroxy group (–OH).
        beta_has_OH = False
        for beta_atom in beta_candidates:
            for nb in beta_atom.GetNeighbors():
                # Look for oxygen atoms that have at least one hydrogen attached.
                if nb.GetAtomicNum() == 8 and nb.GetTotalNumHs() > 0:
                    beta_has_OH = True
                    break
            if beta_has_OH:
                break
        if not beta_has_OH:
            continue  # this acid group does not have a beta-OH arrangement.
        
        # Next, check that the alkyl chain is long enough to be considered a fatty acid.
        # We perform a simple depth-first search (DFS) from the alpha carbon (excluding the acid)
        # along carbon atoms that are not in rings.
        def dfs_chain(atom, prev_idx, count, visited):
            max_len = count
            for neighbor in atom.GetNeighbors():
                if neighbor.GetAtomicNum() == 6 and neighbor.GetIdx() != prev_idx:
                    # Skip if the carbon is in a ring; we favor flexible acyclic chains.
                    if neighbor.IsInRing():
                        continue
                    if neighbor.GetIdx() in visited:
                        continue
                    visited.add(neighbor.GetIdx())
                    new_len = dfs_chain(neighbor, atom.GetIdx(), count + 1, visited)
                    visited.remove(neighbor.GetIdx())
                    if new_len > max_len:
                        max_len = new_len
            return max_len
        
        visited = set([acid_atom.GetIdx(), alpha_atom.GetIdx()])
        chain_length = dfs_chain(alpha_atom, acid_atom.GetIdx(), 1, visited)
        
        # Require a minimum chain length; here 6 (alpha plus five more carbons) is set arbitrarily.
        if chain_length < 6:
            continue
        
        # If all criteria are met, classify the molecule as a valid 3-hydroxy fatty acid.
        return True, ("Contains a terminal carboxylic acid with a beta-hydroxy substituent "
                      "on a sufficiently long, acyclic aliphatic chain")
    
    # If no acid group led to a valid disposition, then classify as not a 3-hydroxy fatty acid.
    return False, "No suitable beta-hydroxy fatty acid motif found"

# Example (uncomment to test):
# test_smiles = "OCCCCCCCCCCCCCC[C@@H](O)CC(O)=O"  # (3R)-3,17-dihydroxymargaric acid
# result, reason = is_3_hydroxy_fatty_acid(test_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:59845',
                          'name': '3-hydroxy fatty acid',
                          'definition': 'Any fatty acid with a hydroxy '
                                        'functional group in the beta- or '
                                        '3-position. beta-Hydroxy fatty acids '
                                        'accumulate during cardiac hypoxia, '
                                        'and can also be used as chemical '
                                        'markers of bacterial endotoxins.',
                          'parents': ['CHEBI:24654', 'CHEBI:35969'],
                          'xrefs': [   'PMID:1226425',
                                       'PMID:17392575',
                                       'PMID:3094448',
                                       'PMID:7406063'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 85,
                           'log_lines_of_code': 4.442651256490317,
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
                                                 1,
                                                 1,
                                                 2,
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
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
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
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 3,
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
                                                 1,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'remove',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetIdx',
                                                 'GetNeighbors',
                                                 'add',
                                                 'IsInRing',
                                                 'GetTotalNumHs'],
                           'methods_called_count': 11,
                           'smarts_strings': ['[CX3](=O)[OX2H1]'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_3_hydroxy_fatty_acid(smiles: str):',
                                       'dfs_chain(atom, prev_idx, count, '
                                       'visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No carboxylic acid (COOH) '
                                          'group found"',
                                          'max_len',
                                          'True, ("Contains a terminal '
                                          'carboxylic acid with a beta-hydroxy '
                                          'substituent "',
                                          'False, "No suitable beta-hydroxy '
                                          'fatty acid motif found"'],
                           'returns_count': 5,
                           'complexity': 5.688530251298063},
    'message': '\n'
               'Attempt failed: F1 score of 0.08219178082191782 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: OCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,17-dihydroxymargaric acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: C(C(O)=O)C(CCCC)O NAME: 3-hydroxyheptanoic acid '
               'REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: OCCCCCCCCCC(O)CC(O)=O NAME: 3,12-dihydroxylauric '
               'acid REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: OCCCCCCCCCCCCCC(O)CC(O)=O NAME: '
               '3,16-dihydroxyhexadecanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,9-dihydroxynonanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,22-dihydroxytricosanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,13-dihydroxytridecanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OC(C[C@@H](CC)O)=O NAME: (R)-3-hydroxypentanoic '
               'acid REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: C(CCCCCCCCCCO)CCCC[C@H](CC(O)=O)O NAME: '
               '(3R)-3,18-dihydroxyoctadecanoic acid REASON: CORRECT Contains '
               'a carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,15-dihydroxypentadecanoic acid REASON: CORRECT Contains '
               'a carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OC(C[C@H](CC)O)=O NAME: (S)-3-hydroxypentanoic acid '
               'REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCC(O)CC(O)=O NAME: '
               '3-hydroxyicosanoic acid REASON: CORRECT Contains a carboxylic '
               'acid group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: CCCCC[C@H](O)CC(O)=O NAME: (S)-3-hydroxyoctanoic '
               'acid REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: OCCCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,21-dihydroxyhenicosanoic acid REASON: CORRECT Contains '
               'a carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,10-dihydroxydecanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCCCCCCCCCCCC(O)CC(O)=O NAME: '
               '3,18-dihydroxyoctadecanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: CCCCCC(O)CC(O)=O NAME: 3-hydroxyoctanoic acid '
               'REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: OCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,12-dihydroxylauric acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: CCCCCCCCCCCCC[C@H](O)CC(O)=O NAME: '
               '(S)-3-hydroxypalmitic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: CCCCCCCCC[C@@H](O)CC(O)=O NAME: (R)-3-hydroxylauric '
               'acid REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: OCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,11-dihydroxyundecanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: CCCCCCCCC[C@H](O)CC(O)=O NAME: (S)-3-hydroxylauric '
               'acid REASON: CORRECT Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: C(CCCCCCCCCCO)CC[C@H](CC(O)=O)O NAME: '
               '(3R)-3,16-dihydroxyhexadecanoic acid REASON: CORRECT Contains '
               'a carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: OCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,19-dihydroxynonadecanoic acid REASON: CORRECT Contains '
               'a carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCC(O)CC(O)=O NAME: '
               '3-hydroxyhexacosanoic acid REASON: CORRECT Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               'False positives: SMILES: '
               'CC1=CC=CC=C1S(=O)(=O)NC2=CC3=C(C=C2)OC[C@@H]4[C@H](CC[C@@H](O4)CC(=O)O)N(C3=O)C '
               'NAME: '
               '2-[(2R,4aS,12aS)-5-methyl-8-[(2-methylphenyl)sulfonylamino]-6-oxo-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]acetic '
               'acid REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: C[N+](C)(C)CC(CC([O-])=O)OC(=O)CCCCCC(O)=O NAME: '
               'O-pimelylcarnitine REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: C[N+](C)(C)CC(CC([O-])=O)OC(=O)\\C=C\\CC(O)=O NAME: '
               'O-glutaconylcarnitine REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: N[C@@H]([C@H](O)CC(O)=O)C(O)=O NAME: '
               '(R)-3-hydroxy-L-glutamic acid REASON: WRONGLY CLASSIFIED '
               'Contains a carboxylic acid group with a beta-hydroxy '
               '(3-hydroxy) substituent\n'
               ' * SMILES: O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCCCCCCC/C=C\\CCCCCC '
               'NAME: ACar 18:1 REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: CCCC[C@H](C)[C@@H](O)CC(O)=O NAME: '
               '(3S,4S)-3-hydroxy-4-methyloctanoic acid REASON: WRONGLY '
               'CLASSIFIED Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'CN1[C@@H]2CC[C@H](O[C@@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)C4=CC(=CC=C4)C(F)(F)F)CC(=O)O '
               'NAME: '
               '2-[(2S,4aR,12aS)-5-methyl-6-oxo-8-[[oxo-[3-(trifluoromethyl)phenyl]methyl]amino]-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]acetic '
               'acid REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'C1CC1CC(=O)NC2=CC3=C(C=C2)O[C@H]4[C@@H]3C[C@H](O[C@H]4CO)CC(=O)O '
               'NAME: '
               '2-[(1S,3S,4aR,9aS)-6-[(2-cyclopropyl-1-oxoethyl)amino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]acetic '
               'acid REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'O=C(NC(C(=O)NC(C(O)CC(=O)NC(C(=O)NC(C(O)CC(=O)O)CC1=CC=CC=C1)C)CC2=CC=CC=C2)C(C)C)C(NC(=O)CC3=CC=CC=C3)C(C)C '
               'NAME: YF-044-P-D REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N[C@H]([C@@H](O)CC(=O)N[C@H](C(=O)N[C@H]([C@@H](O)CC(=O)O)CC1=CC=CC=C1)C)CC(C)C)C(C)C)[C@@H](NC(=O)CC)C(C)C '
               'NAME: Ahpatinin Pr REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: O(C(C[N+](C)(C)C)CC(O)=O)C(=O)/C=C/C=C/C NAME: CAR '
               '6:2 REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'S1[C@H](NC(C1)C(=O)N[C@H](C(=O)O[C@H]([C@H]2N(C(=O)[C@@H](N)[C@H](CC)C)CCC2)CC(=O)O)CCSC)[C@H]3N(C(=O)[C@@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)/C(/NC(=O)N[C@H](C(=O)O)CC4=CC=CC=C4)=C/C)CO)=C/C)CO)=C/C)CCCN=C(N)N)CCC3 '
               'NAME: Chitinimide G REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCCCCC/C=C\\C=C\\C=C\\C=C\\CC '
               'NAME: ACar 18:4 REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'CCCCCCCCCCC[C@@H](O)CC(=O)N[C@H]1[C@H](OC[C@H]2O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]2O)O[C@H](CO[C@@]2(C[C@@H](O[C@@]3(C[C@@H](O)[C@@H](O)[C@H](O3)[C@H](O)CO)C(O)=O)[C@@H](O)[C@H](O2)[C@H](O)CO)C(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OC(=O)C[C@H](O)CCCCCCCCCCC '
               'NAME: (KDO)2-lipid IVA REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCCC/C=C/C=C/C=C/C=C/C=C\\C=C\\C=C\\CC '
               'NAME: ACar 22:7 REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'O1C(OC(CCCCCCC)CC(OC(CCCCCCC)CC(O)=O)=O)[C@@H](OC(=O)/C=C/CCCCCCC)C(O)[C@@H](O)C1C '
               'NAME: '
               '3-O-(2-O-(2E-decenoyl)-alpha-L-rhamnopyranosyl)-3-hydroxydecanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               '[H][C@@]1(CC(O)=O)OC(C)(C)[C@]([H])(CC(O)=O)[C@@]1(CO)[C@@]1([H])CC[C@@]2(C)[C@@H](OC(=O)CC2=C1C)c1ccoc1 '
               'NAME: deoxylimonoic acid D-ring-lactone REASON: WRONGLY '
               'CLASSIFIED Contains a carboxylic acid group with a '
               'beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'BrC=1C(=O)[C@](OC(=O)C[C@H](O)C[C@H](O)C)(C(=O)[C@@]2(C1C=C(OC2)/C=C/C=C/C=C/C(=O)O)CC3=C(C(O)=C(O)C(=C3)OC)C(=O)C)C '
               'NAME: Bromophilone A REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O)[C@H](O)C[C@H]1O '
               'NAME: bhos#40 REASON: WRONGLY CLASSIFIED Contains a carboxylic '
               'acid group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'C1[C@H](O[C@H]([C@H]2[C@@H]1C3=C(O2)C=CC(=C3)NC(=O)CC4=CC=NC=C4)CO)CC(=O)O '
               'NAME: '
               '2-[(1S,3S,4aS,9aR)-1-(hydroxymethyl)-6-[(1-oxo-2-pyridin-4-ylethyl)amino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]acetic '
               'acid REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               ' * SMILES: '
               'O=C1N(C(C(=O)O)C(OC(=O)CC(OC(=O)CC(CC(=O)O)C)CCCCCCCCCCCCC)CN(C1C(OC2OC(CN)C(C2O)O)C3OC(N4C(=O)NC(=O)C=C4)C(C3O)O)C)C '
               'NAME: Liposidomycin M-(III) REASON: WRONGLY CLASSIFIED '
               'Contains a carboxylic acid group with a beta-hydroxy '
               '(3-hydroxy) substituent\n'
               ' * SMILES: '
               'O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCC/C=C/C/C=C/C/C=C/C/C=C\\C/C=C\\C/C=C/CC '
               'NAME: ACar 24:6 REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: C[N+](C)(C)CC(CC([O-])=O)OC(=O)CCC(O)=O NAME: '
               'O-succinylcarnitine REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'O=C(O)[C@@]1(O)[C@@]2(O[C@](CCC(=C)[C@@H](OC(=O)C)[C@@H](CC3=CC=CC=C3)C)(O[C@@H]1C(=O)O)[C@@H]([C@H]2OC(=O)CC(O)C(CC(CC)C)C)O)C(=O)O '
               'NAME: Squalestatin U1 REASON: WRONGLY CLASSIFIED Contains a '
               'carboxylic acid group with a beta-hydroxy (3-hydroxy) '
               'substituent\n'
               ' * SMILES: '
               'C1[C@@H](O[C@@H]([C@H]2[C@@H]1C3=C(O2)C=CC(=C3)NC(=O)NC4=CC=C(C=C4)F)CO)CC(=O)O '
               'NAME: '
               '2-[(1R,3R,4aS,9aR)-6-[[(4-fluoroanilino)-oxomethyl]amino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]acetic '
               'acid REASON: WRONGLY CLASSIFIED Contains a carboxylic acid '
               'group with a beta-hydroxy (3-hydroxy) substituent\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-{(1R)-1-hydroxy-16-[(1R,2S)-2-(20-methyl-19-oxooctatriacontyl)cyclopropyl]hexadecyl}hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCCCC[C@H](O)[C@@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-16-{(1S,2R)-2-[(19S,20S)-19-hydroxy-20-methyloctatriacontyl]cyclopropyl}hexadecyl]hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'C([C@H]([C@@H](CCCCCCCCCCCCCCCC[C@@H]1[C@H](CCCCCCCCCCCCCCC[C@@H](O)[C@H](C(O)=O)CCCCCCCCCCCCCCCCCCCCCCCC)C1)OC)C)CCCCCCCCCCCCCCCCC '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-16-{(1R,2S)-2-[(17R,18R)-17-methoxy-18-methylhexatriacontyl]cyclopropyl}hexadecyl]hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-{(1R)-1-hydroxy-12-[(1S,2R)-2-{14-[(1S,2R)-2-icosylcyclopropyl]tetradecyl}cyclopropyl]dodecyl}hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCC[C@@H]1C[C@@H]1[C@H](C)CCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-17-{(1R,2R)-2-[(2R,21R,22R)-21-hydroxy-22-methyltetracontan-2-yl]cyclopropyl}heptadecyl]hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCCCCCC[C@H](O)[C@@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-16-{(1R,2S)-2-[(20S)-20-methyl-19-oxooctatriacontyl]cyclopropyl}hexadecyl]hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-{(1R)-1-hydroxy-12-[(1R,2S)-2-{14-[(1R,2S)-2-icosylcyclopropyl]tetradecyl}cyclopropyl]dodecyl}hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCC[C@@H](OC)[C@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-18-{(1S,2R)-2-[(17R,18R)-17-methoxy-18-methylhexatriacontyl]cyclopropyl}octadecyl]hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCC[C@@H]1C[C@@H]1[C@H](C)CCCCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-17-{(1R,2R)-2-[(2R)-22-methyl-21-oxotetracontan-2-yl]cyclopropyl}heptadecyl]hexacosanoic '
               'acid REASON: MISSED No beta-hydroxy group found relative to '
               'the carboxyl group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(CCCCCCCCCCCCCC)C(O)=O NAME: '
               'R. ruber mycolic acid REASON: MISSED No beta-hydroxy group '
               'found relative to the carboxyl group\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'No suitable beta-hydroxy fatty '
                                               'acid motif found'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'No carboxylic acid (COOH) '
                                               'group found'}],
    'sample_false_negatives': [   {   'smiles': 'OC(C[C@@H](CC)O)=O',
                                      'name': '(R)-3-hydroxypentanoic acid',
                                      'reason': 'No suitable beta-hydroxy '
                                                'fatty acid motif found'},
                                  {   'smiles': 'OC(C[C@H](CC)O)=O',
                                      'name': '(S)-3-hydroxypentanoic acid',
                                      'reason': 'No suitable beta-hydroxy '
                                                'fatty acid motif found'},
                                  {   'smiles': 'OC(CC(CC)O)=O',
                                      'name': '3-hydroxypentanoic acid',
                                      'reason': 'No suitable beta-hydroxy '
                                                'fatty acid motif found'}],
    'attempt': 1,
    'reasoning': 'Below is one approach. In our reasoning the previous code '
                 'simply looked for a matching SMARTS pattern '
                 '“O=C(O)[CH2][CH](O)” without verifying that the acid group '
                 'is terminal or that its alpha carbon leads into a long, '
                 'mostly aliphatic fatty‐acid chain. As seen in the outcomes '
                 'the simple pattern both picks up non–fatty acid molecules '
                 'that merely “borrow” that fragment and misses cases where '
                 'minor variations (or extra substituents) make the SMARTS '
                 'fail. In the revised version we first search for a free '
                 '(terminal) carboxylic acid group using a SMARTS and then '
                 '“walk” one bond away to the (alpha) carbon. From there we '
                 'check that one of its other neighbors (the beta carbon) '
                 'carries an –OH. Finally, to avoid false positives we require '
                 'that the chain coming off the acid group (starting at the '
                 'alpha carbon) is long enough and not part of a ring. (The '
                 'chain‐length cutoff was set arbitrarily to 6 “steps” – one '
                 'may adjust this to be more or less permissive.) This '
                 'multi‐step approach makes the detection more robust against '
                 'the failure modes encountered previously.\n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 45,
    'num_false_positives': 269,
    'num_true_negatives': 141983,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.14331210191082802,
    'recall': 0.9375,
    'f1': 0.24861878453038672,
    'accuracy': 0.9980885453267744,
    'negative_predictive_value': 0.9999788711563112}