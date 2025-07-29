"""
Classifies: CHEBI:18154 polysaccharide
"""
"""
Classifies: Polysaccharide
Definition: A biomacromolecule consisting of large numbers of monosaccharide residues linked glycosidically.
Only structures that contain more than ten monosaccharide residues (i.e. >10 sugar rings) and a sufficiently high molecular weight are classified.
This improved version uses SMARTS patterns to detect typical sugar ring scaffolds (both pyranoses and furanoses) and counts non-overlapping matches.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polysaccharide(smiles: str):
    """
    Determines if a molecule is a polysaccharide based on its SMILES string.
    
    The detection is based on the following criteria:
      - The SMILES string must be valid.
      - The molecule is searched for sugar ring moieties. For our purposes, we assume that
        a monosaccharide ring is either a five-membered (furanose) or six-membered (pyranose) ring
        that is aliphatic, contains exactly one oxygen, and the remaining ring atoms are carbons.
        To improve detection, we search with SMARTS patterns for these motifs.
      - Only nonoverlapping matches (i.e. distinct sugar units) are counted.
      - To be classified as a polysaccharide, the molecule must have >10 sugar units and possess a 
        molecular weight above a threshold (here set to 1000 Da).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a polysaccharide, False otherwise.
        str: Explanation of the classification.
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define SMARTS patterns for typical sugar rings
    # Pyranose: 6-membered ring with 1 O and 5 C (nonaromatic, fully saturated)
    pyranose_smarts = "[C;R;!$(C=*)][C;R;!$(C=*)][C;R;!$(C=*)][C;R;!$(C=*)][O;R][C;R;!$(C=*)]"
    # Furanose: 5-membered ring with 1 O and 4 C
    furanose_smarts = "[C;R;!$(C=*)][C;R;!$(C=*)][O;R][C;R;!$(C=*)][C;R;!$(C=*)]"
    
    pyranose_pat = Chem.MolFromSmarts(pyranose_smarts)
    furanose_pat = Chem.MolFromSmarts(furanose_smarts)
    
    sugar_matches = []
    
    # Get matches for pyranose
    if pyranose_pat is not None:
        matches = mol.GetSubstructMatches(pyranose_pat, useChirality=True)
        sugar_matches.extend(matches)
    
    # Get matches for furanose
    if furanose_pat is not None:
        matches = mol.GetSubstructMatches(furanose_pat, useChirality=True)
        sugar_matches.extend(matches)
    
    # To avoid counting overlapping sugar rings, we filter the matches so that each atom is used only once.
    # We use a greedy algorithm: sort matches by size (all same length here) and take matches that do not share atoms.
    used_atoms = set()
    distinct_sugar_units = []
    for match in sorted(sugar_matches, key=lambda x: len(x)):
        match_set = set(match)
        if match_set & used_atoms:
            continue
        distinct_sugar_units.append(match)
        used_atoms |= match_set
    
    sugar_unit_count = len(distinct_sugar_units)
    
    # Check sugar residue count threshold (>10)
    if sugar_unit_count <= 10:
        return False, f"Found only {sugar_unit_count} sugar ring(s); a polysaccharide requires more than 10 residues."
    
    # Check molecular weight (must be high enough for a biomacromolecule)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 1000:
        return False, f"Molecular weight ({mol_wt:.1f} Da) is too low for a typical polysaccharide."
    
    return True, f"Detected {sugar_unit_count} sugar ring(s) with a molecular weight of {mol_wt:.1f} Da indicative of a polysaccharide."

# Example usage (uncomment for testing):
# result, reason = is_polysaccharide("O(C1C(O)C(O)C(O)C1O)...")  # Provide a valid polysaccharide SMILES here
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18154',
                          'name': 'polysaccharide',
                          'definition': 'A biomacromolecule consisting of '
                                        'large numbers of monosaccharide '
                                        'residues linked glycosidically. This '
                                        'term is commonly used only for those '
                                        'containing more than ten '
                                        'monosaccharide residues.',
                          'parents': [   'CHEBI:16646',
                                         'CHEBI:167559',
                                         'CHEBI:33694'],
                          'xrefs': ['KEGG:C00420'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 56,
                           'log_lines_of_code': 4.02535169073515,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'append',
                                                 'MolFromSmarts',
                                                 'CalcExactMolWt',
                                                 'extend',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 6,
                           'smarts_strings': [   'pyranose_smarts',
                                                 'furanose_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_polysaccharide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Found only '
                                          '{sugar_unit_count} sugar ring(s); a '
                                          'polysaccharide requires more than '
                                          '10 residues."',
                                          'False, f"Molecular weight '
                                          '({mol_wt:.1f} Da) is too low for a '
                                          'typical polysaccharide."',
                                          'True, f"Detected {sugar_unit_count} '
                                          'sugar ring(s) with a molecular '
                                          'weight of {mol_wt:.1f} Da '
                                          'indicative of a polysaccharide."'],
                           'returns_count': 4,
                           'complexity': 3.60507033814703},
    'message': '\n'
               'Attempt failed: F1 score of 0.7300596082883906 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-[(2R,3S,4S,5S,6R)-3,5-bis[[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy]-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 14 sugar ring(s) with a '
               'molecular weight of 2879.0 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@@H]3[C@@H](O)[C@H](O[C@H]4[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)OC[C@H]6OC(O)[C@H](NC(=O)C)[C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]6O)O[C@@H]([C@@H]3O)CO)[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)CO)[C@H](O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)[C@H]9NC(=O)C)CO)[C@H]8O)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4R,5R)-5-acetamido-3,6-dihydroxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methoxy]-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 12 sugar ring(s) with a '
               'molecular weight of 2207.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO)CO)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-[[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 11 sugar ring(s) with a molecular '
               'weight of 1841.6 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H](O)[C@@H]9O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO '
               'NAME: CID 91861369 REASON: CORRECT Detected 14 sugar ring(s) '
               'with a molecular weight of 2791.0 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: CID 91861924 REASON: CORRECT Detected 15 sugar ring(s) '
               'with a molecular weight of 3170.1 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)O)[C@H]1O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]7NC(=O)C)CO)CO)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O[C@@H]%17O[C@H]([C@@H](O)[C@@H](O)[C@@H]%17O)C)CO[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%15NC(=O)C)CO '
               'NAME: CID 91850586 REASON: CORRECT Detected 18 sugar ring(s) '
               'with a molecular weight of 3520.3 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O[C@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)C)[C@H]5NC(=O)C)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 11 sugar ring(s) with a '
               'molecular weight of 2077.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@@H]8O[C@@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 11 sugar ring(s) with a molecular '
               'weight of 2005.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO '
               'NAME: CID 91846326 REASON: CORRECT Detected 15 sugar ring(s) '
               'with a molecular weight of 3170.1 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@@H]5[C@H](O)[C@@H](O[C@@H]([C@H]5O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]7NC(=O)C)CO)CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%11CO[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)O)CO)[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-[(2R,3S,4S,5S,6R)-3,5-bis[[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy]-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 15 sugar ring(s) with a '
               'molecular weight of 3025.1 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6R)-4-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-6-[[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 11 sugar ring(s) with a '
               'molecular weight of 2222.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 11 sugar ring(s) with a molecular '
               'weight of 1989.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H]7[C@H](O)[C@H](O[C@@H](O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO)O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O)[C@H]7O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO[C@]%13(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO '
               'NAME: CID 91855164 REASON: CORRECT Detected 15 sugar ring(s) '
               'with a molecular weight of 2969.0 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4R,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3-hydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 11 sugar ring(s) with a '
               'molecular weight of 2093.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@@H]%18O[C@@H]([C@@H](O[C@@H]%19O[C@@H]([C@H](O)[C@H](O[C@]%20(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%20)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%19O)CO)[C@H](O)[C@H]%18NC(=O)C)CO)[C@H]%17O)CO)[C@H](O[C@@H]%21O[C@H]([C@@H](O)[C@@H](O)[C@@H]%21O)C)[C@H]%16NC(=O)C)CO '
               'NAME: CID 71298018 REASON: CORRECT Detected 21 sugar ring(s) '
               'with a molecular weight of 4192.5 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO '
               'NAME: CID 91853844 REASON: CORRECT Detected 14 sugar ring(s) '
               'with a molecular weight of 2879.0 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO)CO)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-[[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 12 sugar ring(s) with a molecular '
               'weight of 2044.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10NC(=O)C)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2R,3R,4S,5S,6S)-2-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-6-[[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Detected 11 sugar ring(s) with a '
               'molecular weight of 2263.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO '
               'NAME: CID 91848271 REASON: CORRECT Detected 15 sugar ring(s) '
               'with a molecular weight of 3025.1 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H]8O)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO '
               'NAME: CID 91862461 REASON: CORRECT Detected 14 sugar ring(s) '
               'with a molecular weight of 3027.1 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO)[C@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@H](O)[C@@H]%11O[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3,5-bis[[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy]-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 15 sugar ring(s) with a molecular '
               'weight of 2736.0 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-6-[[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 13 sugar ring(s) with a molecular '
               'weight of 2313.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO[C@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)C)O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 12 sugar ring(s) with a molecular '
               'weight of 2151.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@@H](O)[C@@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@@H]5O)CO)[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO '
               'NAME: CID 91861462 REASON: CORRECT Detected 17 sugar ring(s) '
               'with a molecular weight of 3535.2 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Detected 11 sugar ring(s) with a molecular '
               'weight of 1932.7 Da indicative of a polysaccharide.\n'
               'False positives: SMILES: '
               'O[C@@H]1[C@H]([C@H](O[C@@H]([C@@H]1O[C@@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)N)C(O)=O)O[C@@H]3[C@H](O)[C@H](O[C@@]([C@H]3O)([C@@H](OP(=O)(OCCN)O)CO[C@H]4O[C@@]([C@H]([C@@H]([C@@H]4O)O)O)([C@@H](O)CO)[H])[H])O[C@@H]5[C@H](O)[C@H](O[C@@]([C@H]5O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)([C@@H](O)CO)[H])O[C@@H]7[C@@H](C[C@@](O[C@@]7([C@H](O)CO[C@@H]8[C@@H]([C@H]([C@H](CO8)N)O)O)[H])(C(=O)O)O)O[C@@]9(C[C@H]([C@H]([C@](O9)([C@H](O)CO)[H])O)O)C(O)=O)O[C@H]%10O[C@@]([C@H]([C@@H]([C@@H]%10O[C@H]%11O[C@@]([C@H]([C@@H]([C@@H]%11O)O)O)([C@@H](O)CO)[H])O)O)([C@H](O)CO)[H] '
               'NAME: '
               'alpha-D-GalN-(1->4)-[alpha-LD-Hep-(1->2)-alpha-DD-Hep-(1->2)]-alpha-D-GalA-(1->3)-[alpha-LD-Hep-(1->7)]-alpha-LD-Hep6PEtn-(1->3)-[beta-D-Glc-(1->4)]-alpha-LD-Hep-(1->5)-[alpha-Kdo-(2->4)][beta-L-Arap4N-(1->8)]-alpha-Kdo '
               'REASON: WRONGLY CLASSIFIED Detected 11 sugar ring(s) with a '
               'molecular weight of 2171.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H]1O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@H]2O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O)[C@H]1NC(C)=O '
               'NAME: '
               '[->2)-beta-Man-(1->2)-alpha-Man-(1->2)-[alpha-Glc-(1->3)]-alpha-Man(1->2)-alpha-Man(1->3)-beta-GlcNAc-(1->]2 '
               'REASON: WRONGLY CLASSIFIED Detected 12 sugar ring(s) with a '
               'molecular weight of 2044.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]8O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: CID 91849921 REASON: WRONGLY CLASSIFIED Detected 13 '
               'sugar ring(s) with a molecular weight of 2881.0 Da indicative '
               'of a polysaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OC[C@H]2OC(O)[C@H](NC(C)=O)[C@@H](O)[C@@H]2O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O[C@@H]7O[C@H](CO)[C@@H](O[C@@H]8O[C@H](CO)[C@H](O)[C@H](O[C@@H]9O[C@H](CO)[C@@H](O[C@@H]%10O[C@H](CO)[C@H](O)[C@H](O[C@@H]%11O[C@H](CO)[C@@H](O[C@@H]%12O[C@H](CO)[C@H](O)[C@H](O[C@@H]%13O[C@H](CO)[C@@H](O[C@@H]%14O[C@H](CO)[C@H](O)[C@H](O)[C@H]%14O)[C@H](O)[C@H]%13NC(C)=O)[C@H]%12O)[C@H](O)[C@H]%11NC(C)=O)[C@H]%10O)[C@H](O)[C@H]9NC(C)=O)[C@H]8O)[C@H](O)[C@H]7NC(C)=O)[C@H]6O)[C@H](O)[C@H]5NC(C)=O)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O[C@@H]6O[C@H](CO)[C@@H](O[C@@H]7O[C@H](CO)[C@H](O)[C@H](O[C@@H]8O[C@H](CO)[C@@H](O[C@@H]9O[C@H](CO)[C@H](O)[C@H](O[C@@H]%10O[C@H](CO)[C@@H](O[C@@H]%11O[C@H](CO)[C@H](O)[C@H](O[C@@H]%12O[C@H](CO)[C@@H](O[C@@H]%13O[C@H](CO)[C@H](O)[C@H](O)[C@H]%13O)[C@H](O)[C@H]%12NC(C)=O)[C@H]%11O)[C@H](O)[C@H]%10NC(C)=O)[C@H]9O)[C@H](O)[C@H]8NC(C)=O)[C@H]7O)[C@H](O)[C@H]6NC(C)=O)[C@H]5O)[C@H](O)[C@H]4NC(C)=O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O[C@@H]6O[C@H](CO)[C@@H](O[C@@H]7O[C@H](CO)[C@H](O)[C@H](O[C@@H]8O[C@H](CO)[C@@H](O[C@@H]9O[C@H](CO)[C@H](O)[C@H](O[C@@H]%10O[C@H](CO)[C@@H](O[C@@H]%11O[C@H](CO)[C@H](O)[C@H](O[C@@H]%12O[C@H](CO)[C@@H](O[C@@H]%13O[C@H](CO)[C@H](O)[C@H](O)[C@H]%13O)[C@H](O)[C@H]%12NC(C)=O)[C@H]%11O)[C@H](O)[C@H]%10NC(C)=O)[C@H]9O)[C@H](O)[C@H]8NC(C)=O)[C@H]7O)[C@H](O)[C@H]6NC(C)=O)[C@H]5O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-2)-[beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-6)]-alpha-D-Man-(1-6)-[beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-3)-beta-D-Gal-(1-4)-beta-D-GlcNAc-(1-2)-alpha-D-Man-(1-3)]-beta-D-Man-(1-4)-beta-D-GlcNAc-(1-4)-[alpha-L-Fuc-(1-6)]-beta-D-GlcNAc '
               'REASON: WRONGLY CLASSIFIED Detected 36 sugar ring(s) with a '
               'molecular weight of 6533.4 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@@H](O)[C@H]5NC(=O)C)CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H]%12O[C@@H]%14O[C@H]([C@@H](O)[C@@H](O)[C@@H]%14O)C)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: CID 146015968 REASON: WRONGLY CLASSIFIED Detected 14 '
               'sugar ring(s) with a molecular weight of 2500.9 Da indicative '
               'of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@@H]%10NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2R,3R,4S,5S,6S)-2-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Detected 12 sugar ring(s) with '
               'a molecular weight of 2409.9 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]2O[C@@H]2[C@@H](CO)O[C@@H](O[C@H]3[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O)[C@H]5O[C@@H]5O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]5O)[C@H](O[C@@H]5O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]5O)[C@H]4NC(C)=O)[C@@H](O[C@H]4[C@H](O)[C@@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H](O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H]5NC(C)=O)O[C@@H](O[C@H]5[C@H](O)[C@@H](NC(C)=O)[C@H](O[C@H]6[C@H](O)[C@@H](NC(C)=O)[C@H](O)O[C@@H]6CO)O[C@@H]5CO)[C@H]4O)O[C@@H]3CO)[C@H](NC(C)=O)[C@H]2O[C@@H]2O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]2O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-L-Fucp-(1->2)-beta-D-Galp-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->6)-{alpha-L-Fucp-(1->2)-beta-D-Galp-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->2)-[alpha-L-Fucp-(1->2)-beta-D-Galp-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->4)]-alpha-D-Manp-(1->3)}-beta-D-Manp-(1->4)-beta-D-GlcpNAc-(1->4)-beta-D-GlcpNAc '
               'REASON: WRONGLY CLASSIFIED Detected 17 sugar ring(s) with a '
               'molecular weight of 2882.1 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@@H]8O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@@H]%10NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 11 sugar ring(s) with a '
               'molecular weight of 2046.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO)CO)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O)CO[C@H]%13O[C@@H]([C@@H](O)[C@@H](O)[C@@H]%13O[C@H]%14O[C@@H]([C@@H](O)[C@H](O)[C@@H]%14O)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 14 sugar ring(s) with a '
               'molecular weight of 2368.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@H]2O)CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@H]3O)CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@H]4O)CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@H]5O)CO[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO[C@H]7[C@@H]([C@H]([C@@H]([C@H](O7)CO[C@H]8[C@@H]([C@H]([C@@H]([C@H](O8)CO[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O)O)O)O)O)O)O)O)O)O)O[C@@H]%10[C@H]([C@@H](O[C@@H]([C@H]%10O)CO)O[C@@H]%11[C@H]([C@@H](O[C@@H]([C@H]%11O)CO)O[C@@H]%12[C@H]([C@@H](O[C@@H]([C@H]%12O)CO)O[C@@H]%13[C@H]([C@@H](O[C@@H]([C@H]%13O)CO)OCCN)O)O)O)O)O)O)O)O '
               'NAME: '
               'beta-D-Glc-(1->3)-beta-D-Glc-(1->3)-beta-D-Glc-(1->3)-beta-D-Glc-(1->3)-[beta-D-Glc-(1->6)-beta-D-Glc-(1->6)-beta-D-Glc-(1->6)-beta-D-Glc-(1->6)-beta-D-Glc-(1->6)]-beta-D-Glc-(1->3)-beta-D-Glc-(1->3)-beta-D-Glc-(1->3)-beta-D-Glc-(1->3)-beta-D-Glc-O[CH2]2NH2 '
               'REASON: WRONGLY CLASSIFIED Detected 13 sugar ring(s) with a '
               'molecular weight of 2167.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               '[C@@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@H]7[C@@H]([C@H]([C@@H]([C@H](O7)CO)O)O[C@H]8[C@@H]([C@H]([C@H]([C@H](O8)CO)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O)NC(C)=O)O)O)O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O[C@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O[C@H]%11[C@@H]([C@H]([C@@H]([C@H](O%11)CO)O[C@H]%12[C@@H]([C@H]([C@H]([C@H](O%12)CO)O)O[C@H]%13[C@@H]([C@H]([C@@H]([C@H](O%13)CO)O)O[C@H]%14[C@@H]([C@H]([C@H]([C@H](O%14)CO)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O)NC(C)=O)O)O[C@@H]%15[C@H]([C@H]([C@@H]([C@H](O%15)CO)O)O)O[C@H]%16[C@@H]([C@H]([C@@H]([C@H](O%16)CO)O[C@H]%17[C@@H]([C@H]([C@H]([C@H](O%17)CO)O)O[C@H]%18[C@@H]([C@H]([C@@H]([C@H](O%18)CO)O[C@H]%19[C@@H]([C@H]([C@H]([C@H](O%19)CO)O)O[C@H]%20[C@@H]([C@H]([C@@H]([C@H](O%20)CO)O)O[C@H]%21[C@@H]([C@H]([C@H]([C@H](O%21)CO)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O)NC(C)=O)O)O[C@H]%22[C@@H]([C@H]([C@@H](O[C@@H]%22CO)O[C@H]%23[C@@H]([C@H]([C@@H](O[C@@H]%23CO[C@H]%24[C@H]([C@@H]([C@@H]([C@@H](O%24)C)O)O)O)O)NC(=O)C)O)NC(=O)C)O '
               'NAME: '
               'beta-D-Gal-(1->3)-beta-D-GlcNAc-(1->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc-(1->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc-(1->2)-[beta-D-Gal-(1->3)-beta-D-GlcNAc-(1->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc-(1->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc-(1->6)]-alpha-D-Man-(1->6)-[beta-D-Gal-(1->3)-beta-D-GlcNAc-(1->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc-(1->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc-(1->2)-alpha-D-Man-(1->3)]-beta-D-Man-(1->4)-beta-D-GlcNAc-(1->4)-[alpha-L-Fucp-(1->6)]-beta-D-GlcNAc '
               'REASON: WRONGLY CLASSIFIED Detected 24 sugar ring(s) with a '
               'molecular weight of 4342.6 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15O)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@H]%18O[C@@H]([C@H](O)[C@H](O)[C@H]%18O)CO)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91846202 REASON: WRONGLY CLASSIFIED Detected 18 '
               'sugar ring(s) with a molecular weight of 3423.2 Da indicative '
               'of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2R,3R,4S,5S,6S)-2-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5S,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Detected 11 sugar ring(s) with '
               'a molecular weight of 2222.8 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@H](O)[C@@H]%11O[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15O)CO)[C@H](O)[C@@H]%14NC(=O)C)CO)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-6-[[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3,5-bis[[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy]-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 15 sugar ring(s) with a '
               'molecular weight of 2736.0 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@@H]%13NC(=O)C)CO)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: CID 71298047 REASON: WRONGLY CLASSIFIED Detected 16 '
               'sugar ring(s) with a molecular weight of 2898.0 Da indicative '
               'of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%10NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2R,3R,4R,5S,6S)-2-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-hydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Detected 12 sugar ring(s) with '
               'a molecular weight of 2466.9 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](OP(O)(=O)OC[C@H]3O[C@H](C[C@@H]3OP(O)(=O)OC[C@H]3O[C@H](C[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cnc4c(N)ncnc34)n3cc(C)c(=O)[nH]c3=O)n3cc(C)c(=O)[nH]c3=O)[C@@H](COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(=O)O[C@@H]3[C@@H](COP(O)(=O)O[C@@H]4[C@@H](COP(O)(=O)O[C@@H]5[C@@H](COP(O)(=O)O[C@@H]6[C@@H](COP(O)(=O)O[C@@H]7[C@@H](COP(O)(=O)O[C@@H]8[C@@H](COP(O)(=O)O[C@@H]9[C@@H](COP(O)(=O)O[C@@H]%10[C@@H](CO)O[C@H]([C@@H]%10O)n%10cnc%11c(N)ncnc%10%11)O[C@H]([C@@H]9O)n9cnc%10c(N)ncnc9%10)O[C@H]([C@@H]8O)n8cnc9c(N)ncnc89)O[C@H]([C@@H]7O)n7cnc8c(N)ncnc78)O[C@H]([C@@H]6O)n6cnc7c(N)ncnc67)O[C@H]([C@@H]5O)n5cnc6c(N)ncnc56)O[C@H]([C@@H]4O)n4cnc5c(N)ncnc45)O[C@H]([C@@H]3O)n3cnc4c(N)ncnc34)n3cc(C)c(=O)[nH]c3=O)n3cc(C)c(=O)[nH]c3=O)O2)c(=O)[nH]c1=O '
               'NAME: A8dT5A8 REASON: WRONGLY CLASSIFIED Detected 21 sugar '
               'ring(s) with a molecular weight of 6723.1 Da indicative of a '
               'polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7NC(=O)C)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@@H](O)[C@H]8NC(=O)C)CO)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12NC(=O)C)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 12 sugar ring(s) with a '
               'molecular weight of 2274.9 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@@H]6[C@H](O)[C@@H](O[C@@H]([C@H]6O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)[C@@H]7O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%11CO)O '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3,5-bis[[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy]-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 11 sugar ring(s) with a '
               'molecular weight of 1964.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO[C@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)C)O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 11 sugar ring(s) with a '
               'molecular weight of 1973.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@H]2[C@@H](O[C@H](CO)[C@H](O)[C@@H]2O[C@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)O[C@H]2[C@H](O)[C@@H](CO)O[C@@H](O[C@H]3[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]3OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]4CO)O[C@H]4[C@H](O)[C@@H](NC(C)=O)[C@H](O)O[C@@H]4CO)[C@@H](O)[C@@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O[C@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O)[C@H]5O[C@@H]5O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]5O)[C@H]4NC(C)=O)[C@@H]3O)[C@@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-D-Gal-(1->3)-[alpha-L-Fuc-(1->2)]-beta-D-Gal-(1->3)-beta-D-GlcNAc-(1->2)-alpha-D-Man-(1->3)-{alpha-D-Gal-(1->3)-[alpha-L-Fuc-(1->2)]-beta-D-Gal-(1->3)-beta-D-GlcNAc-(1->2)-alpha-D-Man-(1->6)}-beta-D-Man-(1->4)-beta-D-GlcNAc-(1->4)-beta-D-GlcNAc '
               'REASON: WRONGLY CLASSIFIED Detected 13 sugar ring(s) with a '
               'molecular weight of 2256.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](O)C(O[C@@H]4CO)O)[C@H](O)[C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]5NC(=O)C)CO)[C@H]3O)C8O[C@@H]([C@H](O)[C@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H]9NC(=O)C)CO)[C@H]8O)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3S,4S,5R)-6-[(2R,3S,4R,5R,6R)-5-Acetamido-6-[[(2R,3S,4S,5R,6S)-4-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-2-yl]methoxy]-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 13 sugar ring(s) with a '
               'molecular weight of 2240.8 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OC[C@H]2O[C@@H](O)[C@H](NC(C)=O)[C@@H](O)[C@@H]2O[C@@H]2O[C@H](CO[C@@H]3O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]3O)[C@@H](O[C@@H]3O[C@H](CO)[C@@H](O[C@@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H]5NC(C)=O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H]5NC(C)=O)[C@@H]4O)[C@H](O)[C@H]3NC(C)=O)[C@H](O)[C@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-L-Fucp-(1->2)-beta-D-Galp-(1->3)-[alpha-L-Fucp-(1->4)]-beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-L-Fucp-(1->2)-beta-D-Galp-(1->3)-[alpha-L-Fucp-(1->4)]-beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-D-GlcpNAc-(1->4)-[alpha-L-Fucp-(1->6)]-beta-D-GlcpNAc(1->4)-[alpha-L-Fucp-(1->6)]-beta-D-GlcpNAc '
               'REASON: WRONGLY CLASSIFIED Detected 16 sugar ring(s) with a '
               'molecular weight of 2720.0 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O)CO)[C@@H]9O)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Detected 11 sugar ring(s) with a '
               'molecular weight of 1948.7 Da indicative of a polysaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H]%10NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O)[C@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H]%13NC(=O)C)CO)CO)[C@@H]%16O[C@@H]([C@@H](O)[C@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@@H]%16NC(=O)C)CO '
               'NAME: CID 71297969 REASON: WRONGLY CLASSIFIED Detected 18 '
               'sugar ring(s) with a molecular weight of 3681.3 Da indicative '
               'of a polysaccharide.\n'
               'False negatives: SMILES: '
               'OC[C@H]1O[C@@H]2O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O[C@@H]5[C@@H](CO)O[C@H](O[C@@H]6[C@@H](CO)O[C@H](O[C@@H]7[C@@H](CO)O[C@H](O[C@@H]8[C@@H](CO)O[C@H](O[C@H]1[C@H](O)[C@H]2O)[C@H](O)[C@H]8O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O '
               'NAME: beta-cyclodextrin REASON: MISSED Found only 7 sugar '
               'ring(s); a polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](O)[C@@H](O[C@@H]6CO)O)[C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
               'acid REASON: MISSED Found only 9 sugar ring(s); a '
               'polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](O)C(O[C@@H]6CO)O)[C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
               'acid REASON: MISSED Found only 9 sugar ring(s); a '
               'polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'C1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O)O)O)O)O '
               'NAME: laminarihexaose REASON: MISSED Found only 6 sugar '
               'ring(s); a polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'O=C[C@H](O)[C@@H](O)[C@H](O[C@H]1O[C@@H]([C@@H](O[C@H]2O[C@@H]([C@@H](O[C@H]3O[C@@H]([C@@H](O[C@H]4O[C@@H]([C@@H](N[C@H]5O[C@@H]([C@@H](O[C@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@H](N[C@H]8O[C@@H]([C@@H](O[C@H]9O[C@@H]([C@@H](O[C@H]%10O[C@@H]([C@@H](O)[C@@H]([C@H]%10O)O)CO)[C@@H]([C@H]9O)O)CO)[C@@H]([C@H]8O)O)CO)[C@@H]([C@H]7O)O)C)[C@@H]([C@H]6O)O)CO)[C@@H]([C@H]5O)O)CO)[C@@H]([C@H]4O)O)C)[C@@H]([C@H]3O)O)CO)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO)[C@H](O)CO '
               'NAME: Acarviostatin II23 REASON: MISSED Found only 10 sugar '
               'ring(s); a polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](O)C(O[C@@H]6CO)O)[C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
               'acid REASON: MISSED Found only 9 sugar ring(s); a '
               'polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@H]2O)CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@H]3O)CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@H]4O)CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@H]5O)CO)O)O)O)O)O '
               'NAME: [3)-beta-D-Glcp-(1->]5 REASON: MISSED Found only 5 sugar '
               'ring(s); a polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](O)[C@@H](O[C@@H]7CO)O)[C@@H]1O)CO)[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
               'acid REASON: MISSED Found only 9 sugar ring(s); a '
               'polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H]2O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O[C@@H]5[C@@H](CO)O[C@H](O[C@@H]6[C@@H](CO)O[C@H](O[C@@H]7[C@@H](CO)O[C@H](O[C@@H]8[C@@H](CO)O[C@H](O[C@@H]9[C@@H](CO)O[C@H](O[C@H]1[C@H](O)[C@H]2O)[C@H](O)[C@H]9O)[C@H](O)[C@H]8O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O '
               'NAME: gamma-cyclodextrin REASON: MISSED Found only 8 sugar '
               'ring(s); a polysaccharide requires more than 10 residues.\n'
               ' * SMILES: '
               '[C@H]12O[C@@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@@H]5[C@@H]([C@H]([C@H](O[C@@H]6[C@@H]([C@H]([C@H](O[C@@H]7[C@@H]([C@H]([C@H](O[C@H]([C@@H]([C@H]1O)O)O[C@@H]2CO)[C@H](O7)CO)O)O)[C@H](O6)CO)O)O)[C@H](O5)CO)O)O)O)O)O)O '
               'NAME: alpha-cyclodextrin REASON: MISSED Found only 6 sugar '
               'ring(s); a polysaccharide requires more than 10 residues.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Found only 10 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Found only 0 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Found only 2 sugar ring(s); a '
                                               'polysaccharide requires more '
                                               'than 10 residues.'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@H]1O[C@@H]2O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O[C@@H]5[C@@H](CO)O[C@H](O[C@@H]6[C@@H](CO)O[C@H](O[C@@H]7[C@@H](CO)O[C@H](O[C@@H]8[C@@H](CO)O[C@H](O[C@H]1[C@H](O)[C@H]2O)[C@H](O)[C@H]8O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O',
                                      'name': 'beta-cyclodextrin',
                                      'reason': 'Found only 6 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': 'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](O)[C@@H](O[C@@H]6CO)O)[C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O',
                                      'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Found only 9 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': 'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](O)C(O[C@@H]6CO)O)[C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O',
                                      'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Found only 9 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': 'C1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O)O)O)O)O',
                                      'name': 'laminarihexaose',
                                      'reason': 'Found only 6 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': 'O=C[C@H](O)[C@@H](O)[C@H](O[C@H]1O[C@@H]([C@@H](O[C@H]2O[C@@H]([C@@H](O[C@H]3O[C@@H]([C@@H](O[C@H]4O[C@@H]([C@@H](N[C@H]5O[C@@H]([C@@H](O[C@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@H](N[C@H]8O[C@@H]([C@@H](O[C@H]9O[C@@H]([C@@H](O[C@H]%10O[C@@H]([C@@H](O)[C@@H]([C@H]%10O)O)CO)[C@@H]([C@H]9O)O)CO)[C@@H]([C@H]8O)O)CO)[C@@H]([C@H]7O)O)C)[C@@H]([C@H]6O)O)CO)[C@@H]([C@H]5O)O)CO)[C@@H]([C@H]4O)O)C)[C@@H]([C@H]3O)O)CO)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO)[C@H](O)CO',
                                      'name': 'Acarviostatin II23',
                                      'reason': 'Found only 10 sugar ring(s); '
                                                'a polysaccharide requires '
                                                'more than 10 residues.'},
                                  {   'smiles': 'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](O)C(O[C@@H]6CO)O)[C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O',
                                      'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Found only 9 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@H]2O)CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@H]3O)CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@H]4O)CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@H]5O)CO)O)O)O)O)O',
                                      'name': '[3)-beta-D-Glcp-(1->]5',
                                      'reason': 'Found only 5 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': 'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O)CO)C(O)=O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](O)[C@@H](O[C@@H]7CO)O)[C@@H]1O)CO)[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)CO)C(O)=O',
                                      'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5R,6R)-3-acetamido-2-[(2R,3S,4R,5R,6S)-4-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-6-[(1S,2R)-2-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,3-dihydroxypropyl]-2-carboxy-4-hydroxyoxan-2-yl]oxy-1,3-dihydroxypropyl]-4-hydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Found only 9 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': 'OC[C@H]1O[C@@H]2O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O[C@@H]5[C@@H](CO)O[C@H](O[C@@H]6[C@@H](CO)O[C@H](O[C@@H]7[C@@H](CO)O[C@H](O[C@@H]8[C@@H](CO)O[C@H](O[C@@H]9[C@@H](CO)O[C@H](O[C@H]1[C@H](O)[C@H]2O)[C@H](O)[C@H]9O)[C@H](O)[C@H]8O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O',
                                      'name': 'gamma-cyclodextrin',
                                      'reason': 'Found only 7 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'},
                                  {   'smiles': '[C@H]12O[C@@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@@H]5[C@@H]([C@H]([C@H](O[C@@H]6[C@@H]([C@H]([C@H](O[C@@H]7[C@@H]([C@H]([C@H](O[C@H]([C@@H]([C@H]1O)O)O[C@@H]2CO)[C@H](O7)CO)O)O)[C@H](O6)CO)O)O)[C@H](O5)CO)O)O)O)O)O)O',
                                      'name': 'alpha-cyclodextrin',
                                      'reason': 'Found only 6 sugar ring(s); a '
                                                'polysaccharide requires more '
                                                'than 10 residues.'}],
    'attempt': 1,
    'reasoning': 'Below is my reasoning:\n'
                 '\n'
                 'The last version of our polysaccharide classifier simply '
                 'looped over every ring (as returned by GetRingInfo) and '
                 'counted those rings having exactly one oxygen and all other '
                 'atoms carbon. In our test outcomes many “true positives” '
                 'were correctly flagged, but many “false positives” '
                 '(non‐polysaccharide glyco conjugates that nevertheless have '
                 'many sugar rings) were mis‐classified as polysaccharides. '
                 'Also, some known polysaccharides (for example, branched or '
                 'fused sugars, or popular cyclic oligosaccharides in which '
                 'the rings “merge”) were either over‐ or under‐counted. In '
                 'short, the “raw ring count” approach was too naïve.\n'
                 '\n'
                 'One way to improve is to detect “sugar units” with a more '
                 'robust method. Rather than relying on ring size and atom '
                 'counts alone, we can use SMARTS patterns designed to capture '
                 'typical pyranose and furanose substructures. We can then use '
                 'substructure matching (with the caveat of filtering out '
                 'overlapping occurrences) to count the number of discrete '
                 'sugar residues. (Optionally one might also require that the '
                 'sugars are linked via glycosidic bonds to form a network.) '
                 'Finally, we check that the overall molecular weight is high '
                 'enough.\n'
                 '\n'
                 'Using this more focused approach (with SMARTS for pyranose '
                 'and furanose) we may minimize the mis‐detection of very '
                 '“sugar‐rich” compounds that are not truly polysaccharides '
                 'plus “misses” where the ring detection fails (for example, '
                 'when rings are fused). In the code below I define two SMARTS '
                 'strings (one for six‐member rings and one for five‐member '
                 'rings) that are typical for sugars (avoiding unsaturation) '
                 'and then count only nonoverlapping substructure matches '
                 '(using set unions of involved atoms). I then require that '
                 'the total number of distinct sugar “units” is greater than '
                 '10 (i.e. at least 11). This should improve our F1 score by '
                 'reducing both false positives and false negatives.\n'
                 '\n'
                 'Below is the complete improved code in a single Python code '
                 'block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1286,
    'num_false_positives': 938,
    'num_true_negatives': 140065,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.5782374100719424,
    'recall': 0.9915188897455667,
    'f1': 0.7304742970746947,
    'accuracy': 0.993330990864371,
    'negative_predictive_value': 0.9999214712013479}