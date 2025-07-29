"""
Classifies: CHEBI:17297 UDP-sugar
"""
#!/usr/bin/env python
"""
Classifies: UDP-sugar 
Definition:
    A pyrimidine nucleotide-sugar having UDP as the nucleotide component attached to an unspecified sugar via an anomeric diphosphate linkage.
    This program detects the uracil (pyrimidine) moiety, the characteristic diphosphate linkage, and the presence of two sugar rings.
Example usage:
    result, reason = is_UDP_sugar("OC[C@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H](O)[C@@H]1O")
"""

from rdkit import Chem

def is_UDP_sugar(smiles: str):
    """
    Determines if a molecule is a UDP-sugar based on its SMILES string.
    A UDP-sugar contains a uracil moiety (as part of the nucleotide), a diphosphate linkage,
    and two sugar rings (one from the uridine and the other the sugar moiety).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a UDP-sugar, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # 1. Look for the uracil moiety.
    # SMARTS for uracil: a five-membered pyrimidine with two carbonyl groups.
    uracil_smarts = "n1ccc(=O)[nH]c1=O"
    uracil_mol = Chem.MolFromSmarts(uracil_smarts)
    if not mol.HasSubstructMatch(uracil_mol):
        return False, "Uracil moiety not found; UDP requires a pyrimidine base (uracil)"
    
    # 2. Look for the diphosphate linkage.
    # SMARTS for diphosphate (a phosphate linked to another phosphate).
    dp_smarts = "OP(O)(=O)OP(O)(=O)"
    dp_mol = Chem.MolFromSmarts(dp_smarts)
    if not mol.HasSubstructMatch(dp_mol):
        return False, "Diphosphate linkage not found; UDP requires a diphosphate chain"
    
    # 3. Check for sugar rings.
    # UDP-sugars must have two sugar components (the ribose in uridine and the separate sugar).
    # We assume a sugar ring is a ring of size 5 or 6 that contains at least one oxygen atom.
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    sugar_rings = 0
    for ring in rings:
        if len(ring) in (5, 6):
            # Count oxygen atoms in the ring.
            oxygen_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8)
            if oxygen_count >= 1:  # typical sugars have one ring oxygen at least
                sugar_rings += 1
                
    if sugar_rings < 2:
        return False, f"Insufficient sugar rings detected (found {sugar_rings}, need at least 2: one ribose and one sugar moiety)"
    
    # If we passed all checks, we consider it a UDP-sugar.
    return True, "Contains uracil, a diphosphate linkage, and multiple sugar rings consistent with a UDP-sugar"

# Example test calls (these can be removed in production)
if __name__ == "__main__":
    test_smiles = "OC[C@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H](O)[C@@H]1O"  # UDP-D-glucose
    result, reason = is_UDP_sugar(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17297',
                          'name': 'UDP-sugar',
                          'definition': 'A pyrimidine nucleotide-sugar having '
                                        'UDP as the nucleotide component '
                                        'attached to an unspecified sugar via '
                                        'an anomeric diphosphate linkage.',
                          'parents': ['CHEBI:61109'],
                          'xrefs': ['KEGG:C05227'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 46,
                           'log_lines_of_code': 3.828641396489095,
                           'indent_by_line': [   1,
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
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'AtomRings',
                                                 'GetRingInfo',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum'],
                           'methods_called_count': 7,
                           'smarts_strings': ['uracil_smarts', 'dp_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_UDP_sugar(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Uracil moiety not found; '
                                          'UDP requires a pyrimidine base '
                                          '(uracil)"',
                                          'False, "Diphosphate linkage not '
                                          'found; UDP requires a diphosphate '
                                          'chain"',
                                          'False, f"Insufficient sugar rings '
                                          'detected (found {sugar_rings}, need '
                                          'at least 2: one ribose and one '
                                          'sugar moiety)"',
                                          'True, "Contains uracil, a '
                                          'diphosphate linkage, and multiple '
                                          'sugar rings consistent with a '
                                          'UDP-sugar"'],
                           'returns_count': 5,
                           'complexity': 4.165728279297819},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Uracil moiety not found; UDP '
                                               'requires a pyrimidine base '
                                               '(uracil)'}],
    'sample_false_negatives': [],
    'attempt': 0,
    'reasoning': 'We can approach the UDP‐sugar classification by detecting '
                 'three key pieces:\n'
                 '\n'
                 '1. A uracil moiety – UDP carries a pyrimidine base (usually '
                 'uracil). We can search for a substructure pattern '
                 'corresponding to uracil (here we use the SMARTS '
                 '"n1ccc(=O)[nH]c1=O").\n'
                 '2. A diphosphate linkage – UDP‐sugars contain a diphosphate '
                 'chain. Although there are many ways to depict phosphate '
                 'groups, here we look for a characteristic diphosphate '
                 'fragment by matching the SMARTS "OP(O)(=O)OP(O)(=O)".\n'
                 '3. Two sugar rings – A UDP‐sugar is a nucleotide–sugar. (One '
                 'sugar is part of the uridine unit and one is the “sugar” '
                 'that is attached via an anomeric diphosphate linkage.) '
                 'Because sugars are typically five‐ or six‐membered '
                 'oxygenated rings, we can iterate over ring systems and count '
                 'how many rings have a size of 5 or 6 and contain at least '
                 'one oxygen atom.\n'
                 '\n'
                 'If all of these criteria are met, we classify the molecule '
                 'as a UDP‐sugar.\n'
                 '\n'
                 'Below is the complete Python program that implements this '
                 'logic.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 62,
    'num_false_positives': 238,
    'num_true_negatives': 142000,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.20666666666666667,
    'recall': 1.0,
    'f1': 0.3425414364640884,
    'accuracy': 0.9983274771609276,
    'negative_predictive_value': 1.0}