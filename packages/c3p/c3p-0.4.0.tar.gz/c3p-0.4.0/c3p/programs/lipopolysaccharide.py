"""
Classifies: CHEBI:16412 lipopolysaccharide
"""
"""
Classifies: A lipopolysaccharide (LPS)

Heuristic definition:
  - The SMILES string must parse correctly.
  - The molecular weight must be above ~350 Da.
  - The presence of several sugar-like rings. Here we define a sugar-like ring as:
      • a ring whose size is 5–7 atoms,
      • that contains exactly one oxygen atom in the ring.
    We require at least 2 such rings (a loose indication of a trisaccharide/oligosaccharide core).
  - The presence of at least one fatty acid–like fragment. We define this fragment as a substructure
    corresponding to a carboxylic acid attached to CH2–CH(OH)–CH2 followed by a long aliphatic chain.
    Once we seed a match via SMARTS, we check that the chain appended to the terminal CH2 is at least 7 carbons long.
  
Note: This heuristic is approximate and may yield some false positives or negatives.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_lipopolysaccharide(smiles: str):
    """
    Determines if a molecule is a lipopolysaccharide (LPS) based on its SMILES string.

    The heuristic checks: 
      - Valid SMILES parsing and molecular weight > 350 Da.
      - At least 2 sugar-like rings. A sugar-like ring is defined by a ring of size 5–7
        that contains exactly one ring oxygen.
      - At least one fatty acid-like fragment resembling a 3-hydroxytetradecanoic acid unit.
        We detect a seed substructure (O=C(O)[CH2][CH](O)[CH2]) then search for an attached aliphatic chain
        of at least 7 contiguous sp3 carbons.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is likely a lipopolysaccharide; otherwise False.
        str: Explanation of the classification result.
    """
    # Parse SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check molecular weight.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 350:
        return False, f"Molecular weight too low for a lipopolysaccharide (wt = {mol_wt:.1f} Da)"

    # Detect sugar-like rings.
    # We use ring information to check rings of size 5, 6, or 7 that contain exactly one oxygen.
    sugar_count = 0
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) not in (5, 6, 7):
            continue
        # Count number of oxygen atoms that lie in the ring.
        oxy_in_ring = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetSymbol() == "O")
        if oxy_in_ring == 1:
            sugar_count += 1

    if sugar_count < 2:
        return False, f"Only {sugar_count} sugar-like ring(s) detected; at least 2 expected based on a trisaccharide core and side-chains"

    # Define a SMARTS pattern for a fatty acid-like fragment.
    # The pattern corresponds to a carboxylic acid (O=C(O)) linked to CH2-CH(OH)-CH2.
    fa_smarts = "O=C(O)[CH2][CH](O)[CH2]"
    fa_pattern = Chem.MolFromSmarts(fa_smarts)
    if fa_pattern is None:
        return False, "Error in parsing fatty acid SMARTS pattern (internal error)"
    
    fa_matches = mol.GetSubstructMatches(fa_pattern)
    if not fa_matches:
        return False, "No 3-hydroxytetradecanoic acid-like seed fragment detected"

    # Define a helper function to compute the maximum contiguous chain length from a starting carbon.
    def get_chain_length(start_idx):
        max_length = 0
        visited = set()

        def dfs(atom_idx, length):
            nonlocal max_length
            visited.add(atom_idx)
            # Look only for neighboring sp3 carbons (atomic number 6) not already visited.
            for nbr in mol.GetAtomWithIdx(atom_idx).GetNeighbors():
                if nbr.GetAtomicNum() == 6 and nbr.GetIdx() not in visited:
                    # Check that the neighbor is sp3 (and not aromatic).
                    if nbr.GetHybridization() == Chem.rdchem.HybridizationType.SP3:
                        dfs(nbr.GetIdx(), length + 1)
            if length > max_length:
                max_length = length
            visited.remove(atom_idx)

        dfs(start_idx, 0)
        return max_length

    # Look for an attached fatty acid chain.
    fatty_acid_found = False
    for match in fa_matches:
        # The SMARTS match returns indices in order:
        # [carboxylic C, CH2, CH(OH), CH2]. We take the last CH2 atom as the attachment point.
        attach_idx = match[-1]
        # Get maximum contiguous chain length from the attachment point.
        chain_len = get_chain_length(attach_idx)
        if chain_len >= 7:
            fatty_acid_found = True
            break

    if not fatty_acid_found:
        return False, "No attached fatty acid chain of sufficient length (>=7 carbons) detected"

    return True, "Molecule has features consistent with a lipopolysaccharide structure"


# For testing purposes – you may remove or comment out the code below when using this as a module.
if __name__ == "__main__":
    # Example test SMILES: you can test with any of the provided examples.
    test_smiles = "O1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)C(O)[C@H](OC(=O)CCCCCCCCCCCCCCCCC)C1COC(=O)CCCCCCCCCCCCCCCCC"
    result, reason = is_lipopolysaccharide(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16412',
                          'name': 'lipopolysaccharide',
                          'definition': 'Liposaccharide natural compounds '
                                        'consisting of a trisaccharide '
                                        'repeating unit (two heptose units and '
                                        'octulosonic acid) with '
                                        'oligosaccharide side chains and '
                                        '3-hydroxytetradecanoic acid units '
                                        '(they are a major constituent of the '
                                        'cell walls of Gram-negative '
                                        'bacteria).',
                          'parents': ['CHEBI:35740', 'CHEBI:65212'],
                          'xrefs': [   'KEGG:C00338',
                                       'PMID:15589368',
                                       'PMID:24186868',
                                       'PMID:24506665',
                                       'PMID:24642373',
                                       'PMID:24659348'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 67,
                           'log_lines_of_code': 4.204692619390966,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
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
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 0,
                                                 0,
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
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetSymbol',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches',
                                                 'GetRingInfo',
                                                 'CalcExactMolWt',
                                                 'AtomRings'],
                           'methods_called_count': 8,
                           'smarts_strings': ['fa_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_lipopolysaccharide(smiles: str):',
                                       'get_chain_length(start_idx):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight too low '
                                          'for a lipopolysaccharide (wt = '
                                          '{mol_wt:.1f} Da)"',
                                          'False, f"Only {sugar_count} '
                                          'sugar-like ring(s) detected; at '
                                          'least 2 expected based on a '
                                          'trisaccharide core and side-chains"',
                                          'False, "Error in parsing fatty acid '
                                          'SMARTS pattern (internal error)"',
                                          'False, "No 3-hydroxytetradecanoic '
                                          'acid-like seed fragment detected"',
                                          'False, "No attached fatty acid '
                                          'chain of sufficient length (>=7 '
                                          'carbons) detected"',
                                          'True, "Molecule has features '
                                          'consistent with a '
                                          'lipopolysaccharide structure"'],
                           'returns_count': 7,
                           'complexity': 4.840938523878193},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CC(C)(C(\\C=C\\C1=CC=C(C=C1)OC)=O)OC2C(C(C(C(C(=O)O)O2)O)O)O '
               'NAME: '
               '3,4,5-trihydroxy-6-{[5-(4-methoxyphenyl)-2-methyl-3-oxopent-4-en-2-yl]oxy}oxane-2-carboxylic '
               'acid REASON: MISSED Only 0 sugar-like ring(s) detected; at '
               'least 2 expected based on a trisaccharide core and '
               'side-chains\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@H](O)[C@H](O)[C@@H]1O)C(O)=O)[C@H]([C@@H](O)CCCCC)C/C=C\\CCCCCCCC(O)=O '
               'NAME: 12-Hydroxy-13-O-D-glucuronoside-octadec-9Z-enoate '
               'REASON: MISSED Only 0 sugar-like ring(s) detected; at least 2 '
               'expected based on a trisaccharide core and side-chains\n'
               ' * SMILES: '
               'CCCCCCCCCC(=O)O[C@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1O[C@@H](C[C@H](OC(C)=O)C(\\C)=C\\CO[C@H]([C@H](O)CO)[C@H](O)[C@H](O)CO)[C@](C)(O)CCC=C(C)C '
               'NAME: Cosmosporaside D, (rel)- REASON: MISSED Only 0 '
               'sugar-like ring(s) detected; at least 2 expected based on a '
               'trisaccharide core and side-chains\n'
               ' * SMILES: O1C(OC(CC)C(O)=O)C(O)C(O)C(O)C1C(O)=O NAME: '
               '6-(1-carboxypropoxy)-3,4,5-trihydroxyoxane-2-carboxylic acid '
               'REASON: MISSED Molecular weight too low for a '
               'lipopolysaccharide (wt = 280.1 Da)\n'
               ' * SMILES: '
               'O=C(OC[C@H]1O[C@H](O[C@H]2O[C@@H]([C@@H](O)[C@@H]([C@H]2O)O)COC(=O)[C@@H]([C@H](O)CCCCCCCCCCCCCCC)CCCCCCCCCCCCCC)[C@H](O)[C@H]([C@@H]1O)O)[C@@H]([C@H](O)CCCCCCCCCCCCCCC)CCCCCCCCCCCCCC '
               "NAME: Trehalose-6,6'-dicorynomycolate REASON: MISSED Only 0 "
               'sugar-like ring(s) detected; at least 2 expected based on a '
               'trisaccharide core and side-chains\n'
               ' * SMILES: '
               'O1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)C(O)[C@H](OC(=O)CCCCCCCCCCCCCCCCC)C1COC(=O)CCCCCCCCCCCCCCCCC '
               "NAME: alpha,alpha'-Trehalose 4,6-dioleate REASON: MISSED Only "
               '0 sugar-like ring(s) detected; at least 2 expected based on a '
               'trisaccharide core and side-chains\n'
               ' * SMILES: '
               'O=C(O[C@@H]1[C@@H](O[C@H](COC(=O)C)[C@H]([C@@H]1OC(=O)CCCCCCCCCCCCCCC)OC(=O)C)OC[C@@H](O)[C@@H](O)CO)C(C)C '
               'NAME: Ustilipid E3 REASON: MISSED Only 0 sugar-like ring(s) '
               'detected; at least 2 expected based on a trisaccharide core '
               'and side-chains\n'
               ' * SMILES: '
               'O(C1[C@@H](O)[C@H](O)C(O[C@H]1OCCCC)COC(=O)CCCCCCCCCCCCCCC)[C@@H]2OC([C@H](OC(=O)CCC)[C@H](O)C2O)C '
               "NAME: Butyl 4'-O-butanoyl-6-O-hexadecanoyl-neohesperidoside "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; at least 2 '
               'expected based on a trisaccharide core and side-chains\n'
               ' * SMILES: '
               'O=C(O)CCCCC/C=C/C=C/C(O[C@@H]1O[C@@H]([C@@H](OC)[C@@H]([C@H]1O)O)CO)CCCCCCC '
               'NAME: Cordyglycoside A REASON: MISSED Only 0 sugar-like '
               'ring(s) detected; at least 2 expected based on a trisaccharide '
               'core and side-chains\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)COC(=O)C(CC)C)[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: 6-O-(2-methylbutanoyl)-alpha-D-glucopyranosyl '
               'alpha-D-glucopyranoside REASON: MISSED Only 0 sugar-like '
               'ring(s) detected; at least 2 expected based on a trisaccharide '
               'core and side-chains\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]12CCC3=C(C(=O)C[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC(=C)C(C)C)[C@@]1(C)CCC(=O)[C@H]2C',
                                     'name': 'Camphoratin H',
                                     'reason': 'Only 0 sugar-like ring(s) '
                                               'detected; at least 2 expected '
                                               'based on a trisaccharide core '
                                               'and side-chains'},
                                 {   'smiles': 'OC1CC=2C(C3C(C4C(C(CC4)C(C)/C=C\\C(C)C)(CC3)C)CC2)(CC1)C',
                                     'name': '(3beta,22E)-26,27-Dinorergosta-5,22-dien-3-ol',
                                     'reason': 'Only 0 sugar-like ring(s) '
                                               'detected; at least 2 expected '
                                               'based on a trisaccharide core '
                                               'and side-chains'},
                                 {   'smiles': 'COc1ccc(cc1)[C@@H]1CC(=O)c2c(O)c(C)c(O)c(C)c2O1',
                                     'name': 'matteucinol',
                                     'reason': 'Molecular weight too low for a '
                                               'lipopolysaccharide (wt = 314.1 '
                                               'Da)'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](C)C(O)=O)[C@@H](N)C(C)C',
                                     'name': 'Val-Trp-Ala',
                                     'reason': 'Only 0 sugar-like ring(s) '
                                               'detected; at least 2 expected '
                                               'based on a trisaccharide core '
                                               'and side-chains'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCC[C@@H](O)CC(O)=O)[C@H](O)C[C@H]1OC(=O)c1c[nH]c2ccccc12',
                                     'name': 'ibho#18',
                                     'reason': 'Only 1 sugar-like ring(s) '
                                               'detected; at least 2 expected '
                                               'based on a trisaccharide core '
                                               'and side-chains'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No 3-hydroxytetradecanoic '
                                               'acid-like seed fragment '
                                               'detected'},
                                 {   'smiles': 'OC=1C=2N=C(C=CC2C=CC1)C',
                                     'name': '2-Methylquinolin-8-ol',
                                     'reason': 'Molecular weight too low for a '
                                               'lipopolysaccharide (wt = 159.1 '
                                               'Da)'},
                                 {   'smiles': 'O([C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)CO)[C@@H]3C[C@@H](NC(=O)C)C(O[C@@H]3CO)O',
                                     'name': 'N-[(3R,5R,6R)-5-[(2R,3R,4S,5R,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-2-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No 3-hydroxytetradecanoic '
                                               'acid-like seed fragment '
                                               'detected'},
                                 {   'smiles': 'O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@@H]2[C@@H](NC(=O)C)C(O[C@@H]([C@@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)O)[C@@H]1O)CO[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)CO)[C@H](O)[C@H]7NC(=O)C)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R)-5-Acetamido-4-[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-3,6-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No 3-hydroxytetradecanoic '
                                               'acid-like seed fragment '
                                               'detected'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCSC)CC=1C=2C(NC1)=CC=CC2)C(O)=O)C',
                                     'name': 'Met-Trp-Met',
                                     'reason': 'Only 0 sugar-like ring(s) '
                                               'detected; at least 2 expected '
                                               'based on a trisaccharide core '
                                               'and side-chains'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)(C(\\C=C\\C1=CC=C(C=C1)OC)=O)OC2C(C(C(C(C(=O)O)O2)O)O)O',
                                      'name': '3,4,5-trihydroxy-6-{[5-(4-methoxyphenyl)-2-methyl-3-oxopent-4-en-2-yl]oxy}oxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Only 1 sugar-like ring(s) '
                                                'detected; at least 2 expected '
                                                'based on a trisaccharide core '
                                                'and side-chains'},
                                  {   'smiles': 'O([C@H]1O[C@@H]([C@H](O)[C@H](O)[C@@H]1O)C(O)=O)[C@H]([C@@H](O)CCCCC)C/C=C\\CCCCCCCC(O)=O',
                                      'name': '12-Hydroxy-13-O-D-glucuronoside-octadec-9Z-enoate',
                                      'reason': 'Only 1 sugar-like ring(s) '
                                                'detected; at least 2 expected '
                                                'based on a trisaccharide core '
                                                'and side-chains'},
                                  {   'smiles': 'CCCCCCCCCC(=O)O[C@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1O[C@@H](C[C@H](OC(C)=O)C(\\C)=C\\CO[C@H]([C@H](O)CO)[C@H](O)[C@H](O)CO)[C@](C)(O)CCC=C(C)C',
                                      'name': 'Cosmosporaside D, (rel)-',
                                      'reason': 'Only 1 sugar-like ring(s) '
                                                'detected; at least 2 expected '
                                                'based on a trisaccharide core '
                                                'and side-chains'},
                                  {   'smiles': 'O1C(OC(CC)C(O)=O)C(O)C(O)C(O)C1C(O)=O',
                                      'name': '6-(1-carboxypropoxy)-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Molecular weight too low for '
                                                'a lipopolysaccharide (wt = '
                                                '280.1 Da)'},
                                  {   'smiles': 'O=C(OC[C@H]1O[C@H](O[C@H]2O[C@@H]([C@@H](O)[C@@H]([C@H]2O)O)COC(=O)[C@@H]([C@H](O)CCCCCCCCCCCCCCC)CCCCCCCCCCCCCC)[C@H](O)[C@H]([C@@H]1O)O)[C@@H]([C@H](O)CCCCCCCCCCCCCCC)CCCCCCCCCCCCCC',
                                      'name': "Trehalose-6,6'-dicorynomycolate",
                                      'reason': 'No 3-hydroxytetradecanoic '
                                                'acid-like seed fragment '
                                                'detected'},
                                  {   'smiles': 'O1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)C(O)[C@H](OC(=O)CCCCCCCCCCCCCCCCC)C1COC(=O)CCCCCCCCCCCCCCCCC',
                                      'name': "alpha,alpha'-Trehalose "
                                              '4,6-dioleate',
                                      'reason': 'No 3-hydroxytetradecanoic '
                                                'acid-like seed fragment '
                                                'detected'},
                                  {   'smiles': 'O=C(O[C@@H]1[C@@H](O[C@H](COC(=O)C)[C@H]([C@@H]1OC(=O)CCCCCCCCCCCCCCC)OC(=O)C)OC[C@@H](O)[C@@H](O)CO)C(C)C',
                                      'name': 'Ustilipid E3',
                                      'reason': 'Only 1 sugar-like ring(s) '
                                                'detected; at least 2 expected '
                                                'based on a trisaccharide core '
                                                'and side-chains'},
                                  {   'smiles': 'O(C1[C@@H](O)[C@H](O)C(O[C@H]1OCCCC)COC(=O)CCCCCCCCCCCCCCC)[C@@H]2OC([C@H](OC(=O)CCC)[C@H](O)C2O)C',
                                      'name': 'Butyl '
                                              "4'-O-butanoyl-6-O-hexadecanoyl-neohesperidoside",
                                      'reason': 'No 3-hydroxytetradecanoic '
                                                'acid-like seed fragment '
                                                'detected'},
                                  {   'smiles': 'O=C(O)CCCCC/C=C/C=C/C(O[C@@H]1O[C@@H]([C@@H](OC)[C@@H]([C@H]1O)O)CO)CCCCCCC',
                                      'name': 'Cordyglycoside A',
                                      'reason': 'Only 1 sugar-like ring(s) '
                                                'detected; at least 2 expected '
                                                'based on a trisaccharide core '
                                                'and side-chains'},
                                  {   'smiles': 'O([C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)COC(=O)C(CC)C)[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO',
                                      'name': '6-O-(2-methylbutanoyl)-alpha-D-glucopyranosyl '
                                              'alpha-D-glucopyranoside',
                                      'reason': 'No 3-hydroxytetradecanoic '
                                                'acid-like seed fragment '
                                                'detected'}],
    'attempt': 3,
    'reasoning': 'Below is our revised solution. In our reasoning we noticed '
                 'that the previous strategy was too strict for detecting '
                 '“sugar‐like” rings (looking for at least two hydroxyl '
                 'substituents on the ring atoms) so that none of the provided '
                 'lipopolysaccharide examples ever yielded a match. In our new '
                 'version we relax that requirement. Instead we consider any '
                 'ring of size 5–7 that contains exactly one oxygen (a '
                 'hallmark of many cyclic sugars) as evidence for a sugar '
                 'ring. Also, for the fatty acid fragment we use a SMARTS to '
                 '“seed” a match for a 3‐hydroxytetradecanoic acid–like unit '
                 'and then we measure the continuity of an attached aliphatic '
                 'chain by doing a depth‐first search from the last atom of '
                 'that match. If we find a chain of at least 7 connected sp^3 '
                 'carbons (outside the matched fragment) we treat that as a '
                 'positive hit. This combined (though still heuristic) '
                 'approach improved on the previous method.\n'
                 '\n'
                 'Below is our complete Python code:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 128,
    'num_true_negatives': 142069,
    'num_false_negatives': 97,
    'num_negatives': None,
    'precision': 0.04477611940298507,
    'recall': 0.05825242718446602,
    'f1': 0.05063291139240506,
    'accuracy': 0.9984188334504568,
    'negative_predictive_value': 0.9993176990278969}