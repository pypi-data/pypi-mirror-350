"""
Classifies: CHEBI:28868 fatty acid anion
"""
"""
Classifies: The conjugate base of a fatty acid (fatty acid anion)
Definition: "The conjugate base of a fatty acid, arising from deprotonation of the 
carboxylic acid group of the corresponding fatty acid."
Heuristics used in this version:
  1. The molecule must contain at least one deprotonated carboxylate group: [CX3](=O)[O-].
  2. The carboxylate carbon must be terminal – it is attached (via a C–C bond) to exactly one carbon (the α–carbon).
  3. From that α–carbon a contiguous chain is “traced” by following only non‐aromatic carbons.
  4. Both an absolute chain‐length and the ratio of chain carbons/total carbons are used; 
     these cutoff values are stricter for larger molecules.
  5. In addition, if the α–carbon has additional substituents (besides the carboxylate and the chain)
     that are not “simple” (only carbon, hydrogen or –OH), the candidate is rejected.
  6. If more than one candidate passes the checks the molecule is not classified as a fatty acid anion.
Note: This heuristic is not perfect but has been tuned based on many true and false positives.
"""

from rdkit import Chem

def is_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a fatty acid anion based on its SMILES string.
    A fatty acid anion is defined as the deprotonated form of a fatty acid – that is,
    it contains a terminal carboxylate group (–C(=O)[O-]) in which the carboxyl carbon
    is attached to exactly one carbon (the α–carbon) from which a contiguous aliphatic chain extends.
    
    We compute the longest chain solely along non‐aromatic carbon–carbon bonds and then require that
    (a) the chain is sufficiently long, and (b) the chain carbons represent a high fraction of the overall 
    carbon count. These thresholds depend on the total size of the molecule; very small acids (e.g. 
    2-hydroxyisobutyrate) are treated more leniently.
    
    Additionally, if the α–carbon (the one linked to the carboxylate carbon) has any extra substituents
    other than the carboxylate or carbons (or simple –OH groups), the candidate is rejected.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        (bool, str): True with a message if the molecule is classified as a fatty acid anion;
                     False with a message otherwise.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # Count total carbons in the molecule.
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    
    # Define SMARTS to look for a deprotonated carboxylate group.
    carboxylate_smarts = "[CX3](=O)[O-]"
    carboxylate_pattern = Chem.MolFromSmarts(carboxylate_smarts)
    matches = mol.GetSubstructMatches(carboxylate_pattern)
    if not matches:
        return False, "No deprotonated carboxylate group found."
    
    # Helper to get the longest linear chain (list of atom indices) from a starting atom 
    # using DFS. We only follow non-aromatic carbon atoms.
    def longest_chain_path(start_idx, prev_idx, visited):
        current_atom = mol.GetAtomWithIdx(start_idx)
        best_path = [start_idx]
        for nbr in current_atom.GetNeighbors():
            nbr_idx = nbr.GetIdx()
            # Do not go back to previous or revisit an atom.
            if nbr_idx == prev_idx or nbr_idx in visited:
                continue
            # Only follow carbon atoms.
            if nbr.GetAtomicNum() != 6:
                continue
            # Only follow non‐aromatic carbons so that we do not “jump” into rings.
            if nbr.GetIsAromatic():
                continue
            # Recurse and choose the longest chain 
            new_path = longest_chain_path(nbr_idx, start_idx, visited | {nbr_idx})
            if len(new_path) + 1 > len(best_path):
                best_path = [start_idx] + new_path
        return best_path

    # Allowed elements for substituents on the α–carbon (besides the chain and carboxylate).
    allowed_atomic_nums = {1, 6, 8}  # hydrogen, carbon, oxygen (hydroxyls allowed)
    
    candidate_count = 0
    candidate_reason = ""
    
    # Process each match that is a candidate carboxylate.
    for match in matches:
        # Our SMARTS "[CX3](=O)[O-]" returns (0,1,2) but we consider only the carboxyl carbon:
        carboxyl_c = mol.GetAtomWithIdx(match[0])
        # Get its neighboring carbons.
        carbon_neighbors = [nbr for nbr in carboxyl_c.GetNeighbors() if nbr.GetAtomicNum() == 6]
        # If not exactly one carbon neighbor the group is not terminal.
        if len(carbon_neighbors) != 1:
            continue
        alpha_atom = carbon_neighbors[0]
        
        # Reject if the α–carbon is in a ring (typical fatty acids develop on an open chain).
        if alpha_atom.IsInRing():
            continue
        
        # Compute the longest contiguous chain starting at the α–carbon.
        chain_path = longest_chain_path(alpha_atom.GetIdx(), carboxyl_c.GetIdx(), {alpha_atom.GetIdx()})
        chain_length = len(chain_path)
        chain_ratio = chain_length / total_carbons if total_carbons > 0 else 0
        
        # Now, check the substituents on the α–carbon.
        # The allowed neighbors are the carboxylate carbon and the one that is included in the chain_path.
        # (If there are extra neighbors with heteroatoms (other than H, C, O), we reject this candidate.)
        extra_substituent_found = False
        for nbr in alpha_atom.GetNeighbors():
            nbr_idx = nbr.GetIdx()
            # Skip if this neighbor is the carboxylate.
            if nbr.GetIdx() == carboxyl_c.GetIdx():
                continue
            # Also skip if this neighbor is the one leading into the longest chain path.
            if nbr_idx in chain_path:
                continue
            # If any other neighbor is present and its atomic number is not allowed, reject.
            if nbr.GetAtomicNum() not in allowed_atomic_nums:
                extra_substituent_found = True
                break
        if extra_substituent_found:
            continue

        # Set thresholds that depend on the size of the molecule.
        if total_carbons < 5:
            min_chain = 2
            min_ratio = 0.5
        elif total_carbons <= 10:
            min_chain = 3
            min_ratio = 0.70
        else:
            min_chain = 6
            min_ratio = 0.75

        if chain_length >= min_chain and chain_ratio >= min_ratio:
            candidate_count += 1
            candidate_reason = (f"Contains a terminal deprotonated carboxylate with an acyl chain "
                                f"of {chain_length} carbons out of {total_carbons} (ratio {chain_ratio:.2f}).")

    if candidate_count == 1:
        return True, candidate_reason
    elif candidate_count == 0:
        return False, ("Carboxylate group(s) found but none are attached to a sufficiently long and 'clean' terminal acyl chain.")
    else:
        return False, ("Multiple terminal carboxylate groups were detected; molecule is not a typical fatty acid anion.")

# Example usage:
if __name__ == "__main__":
    # Test one accepted fatty acid anion:
    test_smiles = "CCCCCCCCCCCCC[C@@H](O)C([O-])=O"  # (R)-2-hydroxyhexadecanoate
    result, reason = is_fatty_acid_anion(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28868',
                          'name': 'fatty acid anion',
                          'definition': 'The conjugate base of a fatty acid, '
                                        'arising from deprotonation of the '
                                        'carboxylic acid group of the '
                                        'corresponding fatty acid.',
                          'parents': ['CHEBI:18059', 'CHEBI:35757'],
                          'xrefs': ['KEGG:C02403', 'PMID:18628202'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 98,
                           'log_lines_of_code': 4.584967478670572,
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
                                                 2,
                                                 2,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
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
                                                 4,
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
                                                 2,
                                                 2,
                                                 2,
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
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'IsInRing',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 10,
                           'smarts_strings': ['carboxylate_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_fatty_acid_anion(smiles: str):',
                                       'longest_chain_path(start_idx, '
                                       'prev_idx, visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "No deprotonated carboxylate '
                                          'group found."',
                                          'best_path',
                                          'True, candidate_reason',
                                          'False, ("Carboxylate group(s) found '
                                          'but none are attached to a '
                                          "sufficiently long and 'clean' "
                                          'terminal acyl chain.")',
                                          'False, ("Multiple terminal '
                                          'carboxylate groups were detected; '
                                          'molecule is not a typical fatty '
                                          'acid anion.")'],
                           'returns_count': 6,
                           'complexity': 5.316993495734114},
    'message': '\n'
               'Attempt failed: F1 score of 0.4511041009463722 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCCCCCCCCC[C@@H](O)C([O-])=O NAME: '
               '(R)-2-hydroxyhexadecanoate REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 15 carbons out '
               'of 16 (ratio 0.94).\n'
               ' * SMILES: '
               'C1[C@H]2[C@@H]([C@H]([C@@H]1OO2)/C=C/[C@H](CCCCC)O)CCCCCCC([O-])=O '
               'NAME: prostaglandin H1(1-) REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 19 carbons out '
               'of 20 (ratio 0.95).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCC(O)C([O-])=O NAME: '
               '2-hydroxyarachidate REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 19 carbons out '
               'of 20 (ratio 0.95).\n'
               ' * SMILES: '
               'C1[C@@H]([C@@H]([C@H](OC1=O)/C=C/[C@H](CCCCC)O)C/C=C\\CCCC(=O)[O-])O '
               'NAME: 11-dehydro-thromboxane B2(1-) REASON: CORRECT Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 16 '
               'carbons out of 20 (ratio 0.80).\n'
               ' * SMILES: '
               'C(C([O-])=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC1C(CC)O1 NAME: '
               '(7Z,10Z,13Z,16Z)-19,20-epoxydocosatetraenoate REASON: CORRECT '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 21 carbons out of 22 (ratio 0.95).\n'
               ' * SMILES: '
               'C(/C=C/C=C\\C/C=C\\CCCCC)=C\\[C@@H]([C@H](CCCC([O-])=O)O)O '
               'NAME: (5S,6S)-dihydroxy-(7E,9E,11Z,14Z)-icosatetraenoate '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 19 carbons out of 20 (ratio 0.95).\n'
               ' * SMILES: C(CCCCCCCCCCC(=O)[O-])(=O)[H] NAME: '
               '12-oxododecanoate REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 11 carbons out '
               'of 12 (ratio 0.92).\n'
               ' * SMILES: CCCCCCCCCCCCC\\C=C\\C([O-])=O NAME: '
               '(E)-hexadec-2-enoate REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 15 carbons out '
               'of 16 (ratio 0.94).\n'
               ' * SMILES: CCCC\\C=C/CCCCCCCCCCCC([O-])=O NAME: '
               '(13Z)-octadecenoate REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 17 carbons out '
               'of 18 (ratio 0.94).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCC([O-])=O NAME: cerotate '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 25 carbons out of 26 (ratio 0.96).\n'
               ' * SMILES: C(CCCCCCCCCC(CC([O-])=O)=O)CCCCCCCCCCCCCCCCC NAME: '
               '3-oxotriacontanoate(1-) REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 29 carbons out '
               'of 30 (ratio 0.97).\n'
               ' * SMILES: '
               'CCCCC[C@H](O)\\C=C\\[C@H]1[C@H](O)CC(=O)[C@@H]1C\\C=C/CCCC([O-])=O '
               'NAME: prostaglandin E2(1-) REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 19 carbons out '
               'of 20 (ratio 0.95).\n'
               ' * SMILES: CCC\\C=C/C\\C=C\\C=C/CCCCCCCC([O-])=O NAME: '
               '(9Z,11E,14Z)-octadeca-9,11,14-trienoate REASON: CORRECT '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 17 carbons out of 18 (ratio 0.94).\n'
               ' * SMILES: '
               'C(CCC[C@@H]([C@@H](/C=C/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)O)O)([O-])=O '
               'NAME: '
               '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoate '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 19 carbons out of 20 (ratio 0.95).\n'
               ' * SMILES: '
               'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H]([NH3+])C(=O)NCC(=O)[O-])=C\\C/C=C\\CCC([O-])=O '
               'NAME: '
               '16(S)-glycinylcystein-S-yl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoate(1-) '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 21 carbons out of 27 (ratio 0.78).\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C[C@H]([C@@H](C/C=C\\C/C=C\\CCCC([O-])=O)O)O '
               'NAME: (5Z,8Z,11R,12R,14Z)-11,12-dihydroxyicosatrienoate '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 19 carbons out of 20 (ratio 0.95).\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCC\\C=C/CCCC([O-])=O NAME: '
               '(5Z,11Z,14Z)-icosatrienoate REASON: CORRECT Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 19 '
               'carbons out of 20 (ratio 0.95).\n'
               ' * SMILES: '
               'O([C@@H]1O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]1O)O)O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)[O-] '
               'NAME: '
               '20-O-(beta-D-glucuronosyl)-(5Z,8Z,11Z,14Z)-eicosatetraenoate(2-) '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 19 carbons out of 26 (ratio 0.73).\n'
               ' * SMILES: CC(C)(O)C([O-])=O NAME: 2-hydroxyisobutyrate '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 2 carbons out of 4 (ratio 0.50).\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C[C@H]1[C@@H](C/C=C\\C/C=C\\CCCC([O-])=O)O1 NAME: '
               '(11R,12S)-EET(1-) REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 19 carbons out '
               'of 20 (ratio 0.95).\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C=C/[C@H](CCCC([O-])=O)OO '
               'NAME: 5(S)-HPETE(1-) REASON: CORRECT Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 19 carbons out '
               'of 20 (ratio 0.95).\n'
               ' * SMILES: C(CCCCCCCC)C[C@H](C([O-])=O)OO NAME: '
               '(2R)-2-hydroperoxydodecanoate REASON: CORRECT Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 11 '
               'carbons out of 12 (ratio 0.92).\n'
               ' * SMILES: CC(C)[C@H](O)CC[C@H](C)CC([O-])=O NAME: '
               '(3S,6R)-6-hydroxy-3,7-dimethyloctanoate REASON: CORRECT '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 7 carbons out of 10 (ratio 0.70).\n'
               ' * SMILES: C(CCCCCCCC(C(=O)[O-])=O)CC NAME: 2-oxododecanoate '
               'REASON: CORRECT Contains a terminal deprotonated carboxylate '
               'with an acyl chain of 11 carbons out of 12 (ratio 0.92).\n'
               ' * SMILES: CCCC\\C=C\\O\\C=C\\C=C/CCCCCCCC([O-])=O NAME: '
               'etheroleate REASON: CORRECT Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 11 carbons out of 18 (ratio '
               '0.61).\n'
               'False positives: SMILES: '
               'O=C(NCC[NH3+])C[C@](CC(=O)NC[C@@H](C([O-])=O)[NH3+])(C([O-])=O)O '
               'NAME: '
               '2-[(L-alanin-3-ylcarbamoyl)methyl]-3-(2-aminoethylcarbamoyl)-2-hydroxypropanoate '
               'REASON: WRONGLY CLASSIFIED Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 3 carbons out of 11 (ratio '
               '0.27).\n'
               ' * SMILES: O(P([O-])([O-])=O)CC([C@H](C(=O)[O-])O)=O NAME: '
               '(R)-2-hydroxy-3-oxo-4-(phosphonatooxy)butanoate(3-) REASON: '
               'WRONGLY CLASSIFIED Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 3 carbons out of 4 (ratio '
               '0.75).\n'
               ' * SMILES: C(C([O-])=O)(CO)(CO)[NH3+] NAME: '
               'alpha-(hydroxymethyl)serine zwitterion REASON: WRONGLY '
               'CLASSIFIED Contains a terminal deprotonated carboxylate with '
               'an acyl chain of 2 carbons out of 4 (ratio 0.50).\n'
               ' * SMILES: C([C@H](CCP(=O)(C)[O-])[NH3+])([O-])=O NAME: '
               'glufosinate-P zwitterion(1-) REASON: WRONGLY CLASSIFIED '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 3 carbons out of 5 (ratio 0.60).\n'
               ' * SMILES: [H]C(C[N+](C)(C)C)=CC([O-])=O NAME: '
               '4-(trimethylammonio)but-2-enoate REASON: WRONGLY CLASSIFIED '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 3 carbons out of 7 (ratio 0.43).\n'
               ' * SMILES: O[C@@H]1C=CC=C([C@H]1C([O-])=O)C(=O)CCC([O-])=O '
               'NAME: '
               '(1R,6R)-2-(3-carboxylatopropanoyl)-6-hydroxycyclohexa-2,4-diene-1-carboxylate '
               'REASON: WRONGLY CLASSIFIED Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 10 carbons out of 11 (ratio '
               '0.91).\n'
               ' * SMILES: CC(=O)N[C@@H](CCP([O-])=O)C([O-])=O NAME: '
               'N-Acetyldemethylphosphinothricinate (2-) REASON: WRONGLY '
               'CLASSIFIED Contains a terminal deprotonated carboxylate with '
               'an acyl chain of 3 carbons out of 6 (ratio 0.50).\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C=C/C=C/[C@@H](SC[C@H]([NH3+])C(=O)NCC([O-])=O)[C@@H](O)CCCC([O-])=O '
               'NAME: leukotriene D4(1-) REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 19 '
               'carbons out of 25 (ratio 0.76).\n'
               ' * SMILES: '
               'C=12NC3(C(C4=NC(=CC=5NC=6C(=C7N=C(C1)[C@H]([C@@H]7CCC([O-])=O)C)[C-](C(C6C5C)=O)C(=O)OC)C(=C4C)CC)O3)C(=C2C)C=C '
               'NAME: epoxypheophorbide a(2-) REASON: WRONGLY CLASSIFIED '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 16 carbons out of 35 (ratio 0.46).\n'
               ' * SMILES: CC(C)C(=O)CC([O-])=O NAME: 4-methyl-3-oxopentanoate '
               'REASON: WRONGLY CLASSIFIED Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 4 carbons out of 6 (ratio '
               '0.67).\n'
               ' * SMILES: [O-]C(=O)\\C=C/c1ccccc1 NAME: cis-cinnamate REASON: '
               'WRONGLY CLASSIFIED Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 2 carbons out of 9 (ratio '
               '0.22).\n'
               ' * SMILES: C(NC(=[NH2+])N(C)C)CCC(C(=O)[O-])=O NAME: '
               '5-(3,3-dimethylguanidino)-2-oxopentanoate REASON: WRONGLY '
               'CLASSIFIED Contains a terminal deprotonated carboxylate with '
               'an acyl chain of 4 carbons out of 8 (ratio 0.50).\n'
               ' * SMILES: '
               '[Na+].CC(C)n1c(\\C=C\\[C@H](O)C[C@H](O)CC([O-])=O)c(-c2ccc(F)cc2)c2ccccc12 '
               'NAME: (3S,5R)-fluvastatin sodium REASON: WRONGLY CLASSIFIED '
               'Contains a terminal deprotonated carboxylate with an acyl '
               'chain of 6 carbons out of 24 (ratio 0.25).\n'
               ' * SMILES: CC[C@H](C)[C@H]([NH3+])C([O-])=O NAME: L-isoleucine '
               'zwitterion REASON: WRONGLY CLASSIFIED Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 4 carbons out '
               'of 6 (ratio 0.67).\n'
               ' * SMILES: C([O-])(=O)/C=C/C=1C=C(C(O)=CC1)N NAME: '
               '(E)-3-aminocoumarate REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 2 '
               'carbons out of 9 (ratio 0.22).\n'
               ' * SMILES: '
               '[H][C@]12CCC(C)=C1[C@@H](CC[C@H]2C)\\C=C(/C)C([O-])=O NAME: '
               'valerenate REASON: WRONGLY CLASSIFIED Contains a terminal '
               'deprotonated carboxylate with an acyl chain of 11 carbons out '
               'of 15 (ratio 0.73).\n'
               ' * SMILES: '
               'C([C@H](NC(CC[C@H]([NH3+])C(=O)[O-])=O)C([O-])=O)S[C@H](\\C=C\\C=C\\C=C/C/C=C\\CCCCC)[C@@H](O)CCCC(=O)[O-] '
               'NAME: leukotriene F4(2-) REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 19 '
               'carbons out of 28 (ratio 0.68).\n'
               ' * SMILES: C(CNC(=O)CC(C)C)(=O)[O-] NAME: '
               'N-isovalerylglycinate REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 1 '
               'carbons out of 7 (ratio 0.14).\n'
               ' * SMILES: OC[C@@H](O)[C@H](O)[C@H](O)C(=O)C([O-])=O NAME: '
               '2-dehydro-D-galactonate REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 5 '
               'carbons out of 6 (ratio 0.83).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C4=C([C@@H](CCC4=O)C)CCC([O-])=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: '
               '(3E)-2-(2-carboxylatoethyl)-3-methyl-6-oxocyclohex-1-ene-1-carboxyl-CoA(5-) '
               'REASON: WRONGLY CLASSIFIED Contains a terminal deprotonated '
               'carboxylate with an acyl chain of 9 carbons out of 32 (ratio '
               '0.28).\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C([O-])=O '
               'NAME: 3-oxo-23,24-bisnorchol-4-en-22-oate REASON: WRONGLY '
               'CLASSIFIED Contains a terminal deprotonated carboxylate with '
               'an acyl chain of 19 carbons out of 22 (ratio 0.86).\n'
               ' * SMILES: C(=O)([C@@H](NC(=O)CC)CCSC)[O-] NAME: '
               'N-propanoyl-L-methioninate REASON: WRONGLY CLASSIFIED Contains '
               'a terminal deprotonated carboxylate with an acyl chain of 3 '
               'carbons out of 8 (ratio 0.38).\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCC/C=C/C([O-])=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O '
               'NAME: ascr#23(1-) REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 13 '
               'carbons out of 20 (ratio 0.65).\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC([C@]4([C@]([C@@]3([C@H](C[C@@]2(CC(C1)=O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC([O-])=O)C)[H])C)=O)[H])C '
               'NAME: 7beta-hydroxy-3,12-dioxo-5beta-cholanate REASON: WRONGLY '
               'CLASSIFIED Contains a terminal deprotonated carboxylate with '
               'an acyl chain of 21 carbons out of 24 (ratio 0.88).\n'
               ' * SMILES: '
               'C1=2N3C(C=C4N5=C(C=C6N7C(=CC8=N(C(=C1)C(=C8CCC([O-])=O)C([H])=O)[Fe+]735)C(=C6C)CCC([O-])=O)C(=C4C)C=C)=C(C2C)[C@H](CC/C=C(\\C)/CC/C=C(/CCC=C(C)C)\\C)O '
               'NAME: ferriheme a(1-) REASON: WRONGLY CLASSIFIED Contains a '
               'terminal deprotonated carboxylate with an acyl chain of 6 '
               'carbons out of 49 (ratio 0.12).\n'
               'False negatives: SMILES: C[C@H](CC([O-])=O)[NH2+]C(C(=O)[O-])O '
               'NAME: (3R)-3-{[carboxy(hydroxy)methyl]amino}butanoic acid '
               'zwitterion(1-) REASON: MISSED Multiple terminal carboxylate '
               'groups were detected; molecule is not a typical fatty acid '
               'anion.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCCCCCCC(O)C(O)=O NAME: '
               '2-hydroxynervonic acid REASON: MISSED No deprotonated '
               'carboxylate group found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'},
                                 {   'smiles': 'CCCCC\\C=C/C\\C=C/CCCCCCCCCC(=O)NCCO',
                                     'name': 'N-(11Z,14Z)-eicosadienoylethanolamine',
                                     'reason': 'No deprotonated carboxylate '
                                               'group found.'}],
    'sample_false_negatives': [   {   'smiles': 'O([C@@H]1O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]1O)O)O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)[O-]',
                                      'name': '20-O-(beta-D-glucuronosyl)-(5Z,8Z,11Z,14Z)-eicosatetraenoate(2-)',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': 'CCCC\\C=C\\O\\C=C\\C=C/CCCCCCCC([O-])=O',
                                      'name': 'etheroleate',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': 'C[C@H](CC([O-])=O)[NH2+]C(C(=O)[O-])O',
                                      'name': '(3R)-3-{[carboxy(hydroxy)methyl]amino}butanoic '
                                              'acid zwitterion(1-)',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': '[O-]C(CCCCCCC/C=C\\CCCCCCC(C)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)=O',
                                      'name': '(9Z)-17-hydroxyoctadec-9-enoate '
                                              '17-O-beta-D-glucoside',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': '[C@H]([C@H](C[C@H](/C=C/CCCCCC[C@@H](CCCCCC)O)O)O)(C(=O)[O-])[NH3+]',
                                      'name': 'sphingofungin B1 zwitterion',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': 'CC(C)C(=O)C([O-])=O',
                                      'name': '3-methyl-2-oxobutanoate',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': '[C@H]1(O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]1O)O)O)O[C@H](\\C=C\\C2=C(C(CC2)=O)CCCCCCC([O-])=O)CCCCC',
                                      'name': '15-O-(beta-D-glucuronosyl)-prostaglandin '
                                              'B1(2-)',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': 'CCCCC\\C=C/C=C/O\\C=C\\CCCCCCC([O-])=O',
                                      'name': 'colneleate',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': 'C(CCCCCCCCC1C(CCCCCCCCCCC2C(CCCCCCCCCCCCCCCCC[C@@H](O)[C@H](C([O-])=O)CCCCCCCCCCCCCCCCCCCCCCCC)C2)C1)CCCCCCCCCC',
                                      'name': '(2R)-2-[(1R)-1-hydroxy-18-{2-[10-(2-nonadecylcyclopropyl)decyl]cyclopropyl}octadecyl]hexacosanoate',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'},
                                  {   'smiles': 'CCCC(C)C([O-])=O',
                                      'name': '2-methylvalerate',
                                      'reason': 'Carboxylate group(s) found '
                                                'but none are attached to a '
                                                "sufficiently long and 'clean' "
                                                'terminal acyl chain.'}],
    'attempt': 5,
    'reasoning': 'Below is our revised solution. In our reasoning we noted '
                 'that the earlier code (which “traced” a contiguous chain '
                 'from the α–carbon of a –COO– group) was too lenient on '
                 'candidates that have a deprotonated carboxylate even when '
                 'that group is embedded in a more complex (poly‐functional) '
                 'molecule. In our new version we (1) require that the '
                 'carboxylate carbon is “terminal” (attached to exactly one '
                 'carbon), (2) “trace” the longest strictly non‐aromatic '
                 'carbon‐only path starting at that α–carbon, (3) compute both '
                 'an absolute chain‐length and the fraction of all carbons '
                 'that form the “fatty” chain, and (4) additionally check that '
                 'the α–carbon does not have “extra” substituents (other than '
                 'other carbons, hydrogens and –OH’s) that would signal that '
                 'the deprotonated –COO– group is part of a more complex '
                 'functionality. (We use relaxed cutoff thresholds for very '
                 'small molecules [e.g. 2–hydroxyisobutyrate] but require '
                 'longer chains and higher “chain ratios” for larger '
                 'molecules.) Our heuristic now accepts most true fatty acid '
                 'anions (whose long acyl chains typically cover >75% of the '
                 'carbons) while rejecting many false‐positive cases. \n'
                 '\n'
                 'Below is the complete code in one Python block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 640,
    'num_false_positives': 507,
    'num_true_negatives': 141076,
    'num_false_negatives': 77,
    'num_negatives': None,
    'precision': 0.5579773321708805,
    'recall': 0.8926080892608089,
    'f1': 0.6866952789699571,
    'accuracy': 0.9958959943780745,
    'negative_predictive_value': 0.9994544926427352}