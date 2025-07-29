"""
Classifies: CHEBI:74716 withanolide
"""
#!/usr/bin/env python
"""
Classifies: Withanolide – “Any steroid lactone that is a C28 steroid with a modified side chain forming a lactone ring and its substituted derivatives.”
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_withanolide(smiles: str):
    """
    Determines if a molecule is a withanolide based on its SMILES string.
    Withanolides are defined as steroid lactones that have a fused steroid nucleus
    (typically four fused rings; the nucleus itself should contain 17 carbons) and
    a side chain that forms a lactone (cyclic ester) ring. The total molecule should have at least 28 carbons.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if molecule is classified as a withanolide, False otherwise.
        str: Explanation / reason for the classification.
    """
    # Parse the SMILES string into a molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check total carbon count; allow substitutions so require at least 28 C atoms.
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if total_carbons < 28:
        return False, f"Total carbon count is {total_carbons}, which is too low for a typical withanolide."
    
    # Retrieve ring information from the molecule.
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()  # List of tuples (atom indices) for each ring.
    
    # Filter rings that are characteristic of steroid nucleus: 5- or 6-membered rings.
    rings_filtered = [set(ring) for ring in all_rings if len(ring) in {5, 6}]
    if not rings_filtered:
        return False, "No 5- or 6-membered rings detected; expected a steroid nucleus."
    
    # Group fused rings (rings sharing at least one atom) into clusters.
    # We will build clusters of rings (each cluster is a set of atom indices).
    clusters = []
    for ring in rings_filtered:
        found_cluster = None
        for cluster in clusters:
            if cluster & ring:  # if there is any overlap
                found_cluster = cluster
                break
        if found_cluster:
            found_cluster.update(ring)
        else:
            clusters.append(set(ring))
    
    # Heuristically assume the largest fused cluster is the steroid nucleus.
    nucleus_atoms = max(clusters, key=lambda s: len(s))
    
    # Additionally, we expect the steroid nucleus to arise from about 4 fused rings.
    # Count how many rings in rings_filtered are largely contained (>=80%) in the nucleus.
    fused_ring_count = sum(1 for ring in rings_filtered if ring.issubset(nucleus_atoms))
    if fused_ring_count < 4:
        return False, f"Only {fused_ring_count} fused rings detected in nucleus; expected at least 4 for a steroid nucleus."
    
    # Count how many carbons are in the nucleus (core steroid nucleus is expected to have 17 carbons).
    nucleus_carbons = sum(1 for idx in nucleus_atoms if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
    if nucleus_carbons != 17:
        return False, f"Steroid nucleus has {nucleus_carbons} carbons, expected 17."

    # Look for a lactone ring, i.e. a cyclic ester.
    # We use a SMARTS that matches an ester where the oxygen is part of a ring (r5 or r6).
    lactone_smarts = "[$([CX3](=O)[OX2;r5]),$([CX3](=O)[OX2;r6])]"
    lactone_pattern = Chem.MolFromSmarts(lactone_smarts)
    lactone_matches = mol.GetSubstructMatches(lactone_pattern)
    
    lactone_found = False
    # For each lactone candidate, check if the ester fragment is not completely part of the steroid nucleus.
    for match in lactone_matches:
        match_set = set(match)
        if not match_set.issubset(nucleus_atoms):
            lactone_found = True
            break
    
    if not lactone_found:
        return False, "No side chain lactone detected. Withanolides require a modified side chain that forms a lactone ring."
    
    # If all conditions are met, classify the molecule as a withanolide.
    return True, "Molecule is a withanolide: Contains a steroid nucleus with 17 core carbons and a side chain lactone."

# Example usage:
# result, reason = is_withanolide("C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3CC[C@]12C)[C@H]1CC(C)=C(CO)C(=O)O1")
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:74716',
                          'name': 'withanolide',
                          'definition': 'Any steroid lactone that is a C28 '
                                        'steroid with a modified side chain '
                                        'forming a lactone ring and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:26766'],
                          'xrefs': [   'LIPID_MAPS_instance:LMST01160000',
                                       'Wikipedia:Withanolide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 66,
                           'log_lines_of_code': 4.189654742026425,
                           'indent_by_line': [   1,
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
                                                 2,
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
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'AtomRings',
                                                 'MolFromSmarts',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'issubset',
                                                 'update',
                                                 'MolFromSmiles',
                                                 'GetRingInfo'],
                           'methods_called_count': 11,
                           'smarts_strings': ['lactone_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_withanolide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Total carbon count is '
                                          '{total_carbons}, which is too low '
                                          'for a typical withanolide."',
                                          'False, "No 5- or 6-membered rings '
                                          'detected; expected a steroid '
                                          'nucleus."',
                                          'False, f"Only {fused_ring_count} '
                                          'fused rings detected in nucleus; '
                                          'expected at least 4 for a steroid '
                                          'nucleus."',
                                          'False, f"Steroid nucleus has '
                                          '{nucleus_carbons} carbons, expected '
                                          '17."',
                                          'False, "No side chain lactone '
                                          'detected. Withanolides require a '
                                          'modified side chain that forms a '
                                          'lactone ring."',
                                          'True, "Molecule is a withanolide: '
                                          'Contains a steroid nucleus with 17 '
                                          'core carbons and a side chain '
                                          'lactone."'],
                           'returns_count': 7,
                           'complexity': 5.437930948405286},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@H](CC(=O)[C@]4(CO)[C@H]3CC[C@]12C)OS(O)(=O)=O)[C@H]1CC(C)=C(CO)C(=O)O1 '
               'NAME: withalongolide G REASON: MISSED No lactone ring '
               'detected. Withanolides require a side chain lactone '
               'functionality.\n'
               ' * SMILES: '
               'O=C1C=C2C=CC3=C4[C@]([C@@H](/C(=C/[C@H]5OC(=O)[C@H]([C@@H]5C)C)/C)CC4)(C)CC[C@@H]3[C@@]2(C)CC1 '
               'NAME: Penijanthoid B REASON: MISSED No lactone ring detected. '
               'Withanolides require a side chain lactone functionality.\n'
               ' * SMILES: '
               'OC12C(C(CC1)C(O)(C3OC(=O)C(=C(C3)C)CO)C)(CCC4C2CC(O)C5(O)C4(C(=O)CCC5)C)C '
               'NAME: '
               '(5alpha,6beta,14alpha,20R,22R)-5,6,14,20,27-Pentahydroxy-1-oxowith-24-enolide '
               'REASON: MISSED No lactone ring detected. Withanolides require '
               'a side chain lactone functionality.\n'
               ' * SMILES: '
               'O1[C@@]23[C@]([C@@]4([C@]([C@]5([C@@]([C@@]6([C@@](O[C@@]7(OC(=O)[C@@H]([C@H]7C)C)[C@@H](O)[C@@]6(O)C)(C5)[H])[H])(CC4)C)[H])(C[C@@]12[H])[H])[H])(C)C(=O)C=C[C@@H]3O '
               'NAME: Ixocarpalactone B REASON: MISSED No lactone ring '
               'detected. Withanolides require a side chain lactone '
               'functionality.\n'
               ' * SMILES: '
               'CC1=C(C)C(=O)O[C@H](C1)[C@](C)(O)[C@@]12O[C@@H]1C[C@H]1[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3CC[C@]21C '
               'NAME: 20-hydroxytubocapsanolide A REASON: MISSED No lactone '
               'ring detected. Withanolides require a side chain lactone '
               'functionality.\n'
               ' * SMILES: '
               'O=C1O[C@@H](C[C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5([C@H](C([C@H](OC(=O)C[C@@](O)(CC(=O)O)C)CC5)(C)C)CC4)C)C[C@@H]3O)(C)CC2)C)C)C(=C1C)C '
               'NAME: Palustrisolide B REASON: MISSED Carbon count is 37, '
               'expected 28 for a typical withanolide.\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5([C@H](C([C@@H](O)CC5)(C)C)CC4)C)CC3)(C)CC2)C)C)CC=C1C '
               'NAME: Colobetaolactone I REASON: MISSED Carbon count is 30, '
               'expected 28 for a typical withanolide.\n'
               ' * SMILES: '
               'OC12C(C(O)(CC1)C(O)(C3OC(=O)C(=C(C3)C)C)C)(CCC4C2CC(O)C5(O)C4(C)C(=O)C=CC5O)C '
               'NAME: Withaperuvin B REASON: MISSED No lactone ring detected. '
               'Withanolides require a side chain lactone functionality.\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C=O)[C@H]1CC(C)=C(C)C(=O)O1 '
               'NAME: paraminabeolide A REASON: MISSED No lactone ring '
               'detected. Withanolides require a side chain lactone '
               'functionality.\n'
               ' * SMILES: '
               'O=C1O[C@]2(O[C@H]3[C@]4([C@](C=5CC[C@@H]6[C@@](C5C3)(CC[C@H](C6(C)C)OC(=O)C)C)(CC[C@@H]4[C@@H](C2)C)C)C)[C@H]([C@@H]1C)C '
               'NAME: Fomlactone A REASON: MISSED Carbon count is 33, expected '
               '28 for a typical withanolide.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'Total carbon count is 13, '
                                               'which is too low for a typical '
                                               'withanolide.'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No 5- or 6-membered rings '
                                               'detected; expected a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'Only 3 fused rings detected in '
                                               'nucleus; expected at least 4 '
                                               'for a steroid nucleus.'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Only 1 fused rings detected in '
                                               'nucleus; expected at least 4 '
                                               'for a steroid nucleus.'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Total carbon count is 20, '
                                               'which is too low for a typical '
                                               'withanolide.'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Only 1 fused rings detected in '
                                               'nucleus; expected at least 4 '
                                               'for a steroid nucleus.'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'Total carbon count is 6, which '
                                               'is too low for a typical '
                                               'withanolide.'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'Only 2 fused rings detected in '
                                               'nucleus; expected at least 4 '
                                               'for a steroid nucleus.'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'Total carbon count is 12, '
                                               'which is too low for a typical '
                                               'withanolide.'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Only 1 fused rings detected in '
                                               'nucleus; expected at least 4 '
                                               'for a steroid nucleus.'}],
    'sample_false_negatives': [   {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@H](CC(=O)[C@]4(CO)[C@H]3CC[C@]12C)OS(O)(=O)=O)[C@H]1CC(C)=C(CO)C(=O)O1',
                                      'name': 'withalongolide G',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'O=C1C=C2C=CC3=C4[C@]([C@@H](/C(=C/[C@H]5OC(=O)[C@H]([C@@H]5C)C)/C)CC4)(C)CC[C@@H]3[C@@]2(C)CC1',
                                      'name': 'Penijanthoid B',
                                      'reason': 'Only 3 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'O1[C@@]23[C@]([C@@]4([C@]([C@]5([C@@]([C@@]6([C@@](O[C@@]7(OC(=O)[C@@H]([C@H]7C)C)[C@@H](O)[C@@]6(O)C)(C5)[H])[H])(CC4)C)[H])(C[C@@]12[H])[H])[H])(C)C(=O)C=C[C@@H]3O',
                                      'name': 'Ixocarpalactone B',
                                      'reason': 'Steroid nucleus has 23 '
                                                'carbons, expected 17.'},
                                  {   'smiles': 'CC1=C(C)C(=O)O[C@H](C1)[C@](C)(O)[C@@]12O[C@@H]1C[C@H]1[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3CC[C@]21C',
                                      'name': '20-hydroxytubocapsanolide A',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C=O)[C@H]1CC(C)=C(C)C(=O)O1',
                                      'name': 'paraminabeolide A',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3CC[C@]12C)[C@H]1CC(C)=C(CO)C(=O)O1',
                                      'name': 'withaferin A',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'O1C2C3C4(O)C(C(CC4)C(C5OC(=O)C(C(C5)C)C)C)(CCC3C6(C(O)(C12)CC=CC6=O)C)C',
                                      'name': 'Vamonolide',
                                      'reason': 'Only 3 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'O[C@@H]1[C@@]2([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H]([C@@]5(OC(=O)C(=C(C5)C)C)[H])C)[H])(CC3)C)[H])(CC=C2C[C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO)C1)[H])[H])C',
                                      'name': 'Withanoside V',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'CC1=C(C)C(=O)O[C@H](C1)[C@](C)(O)[C@@]1(O)CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3CC[C@]12C',
                                      'name': '17alpha-hydroxywithanolide D',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'},
                                  {   'smiles': 'OC1C2(C3C(C4C(C(CC4)C(C5OC(=O)C(=C(C5)CO)C)C)(CC3)C)CC=C2CC(OC6OC(C(O)C(O)C6O)COC7OC(C(O)C(O)C7O)CO)C1)C',
                                      'name': '2-[1-[1-hydroxy-10,13-dimethyl-3-[3,4,5-trihydroxy-6-[[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxy-2,3,4,7,8,9,11,12,14,15,16,17-dodecahydro-1H-cyclopenta[a]phenanthren-17-yl]ethyl]-4-(hydroxymethyl)-5-methyl-2,3-dihydropyran-6-one',
                                      'reason': 'Only 2 fused rings detected '
                                                'in nucleus; expected at least '
                                                '4 for a steroid nucleus.'}],
    'attempt': 1,
    'reasoning': 'Below is our reasoning followed by the complete Python code '
                 'in a single code block.\n'
                 '\n'
                 'We first analyzed the previous attempt and the error '
                 'outcomes. Many of the failures were due to two issues. '
                 'First, the original code strictly checked that the total '
                 'molecule had exactly 28 carbons—even for substituted '
                 'derivatives—and it did not “see” the lactone ring in many '
                 'cases. In reality, withanolides are defined as steroid '
                 'lactones deriving from a fused steroid nucleus (typically '
                 'four fused rings whose “core” has 17 carbons) plus a '
                 'modified side‐chain that forms a lactone ring. Therefore, '
                 'instead of checking the overall carbon count one must (a) '
                 'verify that the fused steroid nucleus (three six‐membered '
                 'plus one five‐membered ring) contains a “core” of 17 carbon '
                 'atoms and (b) look for a cyclic ester (lactone) that is not '
                 'entirely contained in that nucleus. To do so we (1) filter '
                 'the rings in the molecule for those of size 5 or 6, then '
                 'cluster those rings by fusions (shared atoms) and select the '
                 'largest cluster; (2) count its carbon atoms (expecting 17) '
                 'and (3) search for a lactone using a SMARTS pattern that '
                 'requires the ester function to be in a ring (r5 or r6) and '
                 'then confirm that its atoms do not lie completely within the '
                 'nucleus. In addition, we allow molecules with a total carbon '
                 'count above 28 (substituted derivatives) but require at '
                 'least 28 carbons overall. This approach should help avoid '
                 'missing the side‐chain lactone feature and also '
                 'mis‐classifying molecules that deviate from the steroid '
                 '“core.”\n'
                 '\n'
                 'Below is the complete code implementing these improvements.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 54,
    'num_false_positives': 91,
    'num_true_negatives': 142083,
    'num_false_negatives': 72,
    'num_negatives': None,
    'precision': 0.3724137931034483,
    'recall': 0.42857142857142855,
    'f1': 0.3985239852398524,
    'accuracy': 0.9988545326774421,
    'negative_predictive_value': 0.9994935106046218}