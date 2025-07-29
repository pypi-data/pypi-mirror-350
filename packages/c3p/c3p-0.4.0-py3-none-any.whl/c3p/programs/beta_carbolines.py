"""
Classifies: CHEBI:60834 beta-carbolines
"""
#!/usr/bin/env python
"""
Classifies: beta-carbolines 
Definition: Any pyridoindole containing a beta-carboline skeleton and their hydrogenated derivatives.
A beta‐carboline core is built on a fused bicyclic system in which a five‐membered “indole” ring 
(with an –NH group) is fused to a six‐membered ring that contains at least one nitrogen (making it a pyridine).
This approach analyzes the rings present in a molecule and checks for a fused 5– and 6–membered system with these features.
Note: This method is an approximation and may still mis‐classify some edge cases.
"""
from rdkit import Chem

def is_beta_carbolines(smiles: str):
    """
    Determines whether a molecule (given by its SMILES string) 
    appears to contain a beta-carboline (or hydrogenated beta-carboline) scaffold.
    
    The strategy is:
      1. Parse the SMILES into an RDKit molecule.
      2. Obtain the ring information.
      3. Look for a fused ring pair where one ring is five-membered containing exactly one nitrogen
         (the “indole” part) and the other is six-membered containing at least one nitrogen (the “pyridine” part).
      
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        (bool, str): Tuple (True, reason) if the scaffold is found; otherwise (False, reason).
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # Get ring information (list of tuples; each tuple contains indices of atoms in the ring)
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if not rings:
        return False, "No rings found in the molecule."
    
    # Iterate through all pairs of rings and check for fused rings sharing at least 2 atoms.
    for i, ring1 in enumerate(rings):
        set1 = set(ring1)
        for ring2 in rings[i+1:]:
            set2 = set(ring2)
            shared_atoms = set1.intersection(set2)
            if len(shared_atoms) < 2:
                # not a fused ring system
                continue
            
            # Look for a pair where one ring is 5-membered and the other is 6-membered.
            if (len(ring1) == 5 and len(ring2) == 6) or (len(ring1) == 6 and len(ring2) == 5):
                # Identify which ring is 5-membered (expected to be the indole part) and which is 6-membered (expected pyridine)
                ring5 = ring1 if len(ring1) == 5 else ring2
                ring6 = ring1 if len(ring1) == 6 else ring2
                
                # Count nitrogen atoms in the 5-membered ring.
                n_count_ring5 = sum(1 for idx in ring5 if mol.GetAtomWithIdx(idx).GetAtomicNum() == 7)
                # For a proper indole-like ring, we expect exactly one nitrogen.
                if n_count_ring5 != 1:
                    continue
                
                # Count nitrogen atoms in the 6-membered ring.
                n_count_ring6 = sum(1 for idx in ring6 if mol.GetAtomWithIdx(idx).GetAtomicNum() == 7)
                if n_count_ring6 < 1:
                    # This excludes fused systems with a benzene ring instead of a pyridine.
                    continue

                # Additional check: you might require that the nitrogen in the five-membered ring has at least one hydrogen,
                # but in hydrogenated variants the explicit hydrogen may not be present. So here we simply require one nitrogen.
                
                return True, ("Molecule contains a fused 5- and 6-membered ring system with appropriate nitrogen counts "
                              "(expected for a beta-carboline or its hydrogenated derivative).")
    
    return False, "Molecule does not appear to contain the beta-carboline scaffold (a fused indole-pyridine system) based on ring analysis."

# Example usage (for testing) when running the script directly.
if __name__ == "__main__":
    test_examples = {
        "Aromatic harmine": "COc1ccc2c(c1)[nH]c1cnccc12",  # harmine core (modified to force pyridine N)
        "Hydrogenated variant": "O(C1=CC=2C3=C(NC2C=C1)CN(CC3)C)",  # one of the provided examples
        "Carbazole (should be false positive)": "c1ccc2c(c1)[nH]c1ccccc12",
    }
    
    for name, smi in test_examples.items():
        result, reason = is_beta_carbolines(smi)
        print(f"{name}: {result}\n  Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:60834',
                          'name': 'beta-carbolines',
                          'definition': 'Any pyridoindole containing a '
                                        'beta-carboline skeleton and their '
                                        'hydrogenated derivatives',
                          'parents': ['CHEBI:48888'],
                          'xrefs': ['PMID:1967844'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 55,
                           'log_lines_of_code': 4.007333185232471,
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
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtomWithIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'items',
                                                 'intersection',
                                                 'AtomRings'],
                           'methods_called_count': 7,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_beta_carbolines(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "No rings found in the '
                                          'molecule."',
                                          'False, "Molecule does not appear to '
                                          'contain the beta-carboline scaffold '
                                          '(a fused indole-pyridine system) '
                                          'based on ring analysis."'],
                           'returns_count': 3,
                           'complexity': 4.001466637046494},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'O1[C@@H](N2C3=C4NC=5C=CC=CC5C4=CC=C3C6=C2C=CC=C6)[C@H](O)[C@@H](O)[C@@H]([C@@H]1C)O '
               'NAME: Tjipanazole G2 REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C(O)[C@@]1([C@@H](O)CC[C@]2([C@H]1CCC3=C2C=C4C5=C(C=CC=C5)NC4=C3N6C7=C(C=C8[C@@]9([C@H]([C@](C(=O)O)([C@@H](O)CC9)C)CCC8=C7)C)C%10=C6C=CC=C%10)C)C '
               'NAME: Xiamycin dimer REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: C[C@H](C(O)=O)c1ccc2c(c1)[nH]c1ccc(Cl)cc21 NAME: '
               '(S)-carprofen REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: c1ccc2c(c1)[nH]c1ccccc21 NAME: 9H-carbazole REASON: '
               'WRONGLY CLASSIFIED Molecule contains an aromatic '
               'beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: O(C1=CC=2C3=C(NC2C=C1)C=CC(=C3)C(OC)=O)C NAME: '
               'Methyl 6-methoxy-9H-carbazole-3-carboxylate REASON: WRONGLY '
               'CLASSIFIED Molecule contains an aromatic beta-carboline '
               '(pyridoindole) skeleton.\n'
               ' * SMILES: BrC1=CC=2NC=3C=C(Br)C=CC3C2C=C1 NAME: '
               '2,7-Dibromocarbazole REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'CO[C@@H]1[C@@H](CO)O[C@H]([C@H](O)[C@H]1O)n1c2c(Cl)cccc2c2c3C(=O)NC(=O)c3c3c4cccc(Cl)c4[nH]c3c12 '
               'NAME: rebeccamycin REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: O(C=1C=2NC=3C(C2C=C(C1)C)=CC=CC3)C NAME: '
               'Murrayafoline A REASON: WRONGLY CLASSIFIED Molecule contains '
               'an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: COC1=CC2=C(C=C1)NC3=CC=CC=C32 NAME: '
               '3-methoxy-9H-carbazole REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: O(C=1C=C2NC=3C(C2=CC1C(OC)=O)=CC=CC3)C NAME: '
               'Clausine L REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: ClC1=CC2=C(NC3=C2C=CC4=C3NC=5C=CC=CC45)C=C1 NAME: '
               'Tjipanazole I REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: OC=1C=2NC=3C(C2C=C(C1)C(O)=O)=CC=CC3 NAME: Mukeic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains an aromatic '
               'beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'ClC1=C2C(=CC3=C1NC=4C=CC=CC34)[C@@]5([C@H]([C@](C(=O)O)([C@@H](O)CC5)C)CC2)C '
               'NAME: Chloroxiamycin REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: BrC1=CC2=C(NC3=C2C=C(Br)C=C3)C=C1 NAME: '
               '3,6-Dibromocarbazole REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'OC1=C(C(=C2NC3=C(C2=C1)C=CC=C3)CCCCCCC/C=C\\C/C=C\\CCCCC)C '
               'NAME: Lipocarbazole A2 REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O1[C@@H](N2C=3C(C=4C2=CC=CC4)=C5C(=C6C3NC=7C6=CC=CC7)CNC5=O)C[C@@H](N)[C@@H](O)[C@@H]1C '
               'NAME: Holyrine A REASON: WRONGLY CLASSIFIED Molecule contains '
               'an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: Oc1cc(C=O)cc2c3ccccc3[nH]c12 NAME: '
               'O-Demethylmurrayanine REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: O(C=1C=2NC=3C(C2C=C(C1)C(OC)=O)=CC=CC3)C NAME: '
               'Mukonine REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C(O)[C@@]1([C@@H](O)CC[C@]2([C@H]1CCC3=C2C=C4C5=C(C=CC=C5)N(C4=C3)C6=CC7=C(NC8=C7C=C9[C@@]%10([C@H]([C@](C(=O)O)([C@@H](O)CC%10)C)CCC9=C8)C)C=C6)C)C '
               'NAME: '
               '(16R,17S,18S,21S)-6-[(16R,17S,18S,21S)-17-carboxy-18-hydroxy-17,21-dimethyl-10-azapentacyclo[11.8.0.03,11.04,9.016,21]henicosa-1,3(11),4,6,8,12-hexaen-10-yl]-18-hydroxy-17,21-dimethyl-10-azapentacyclo[11.8.0.03,11.04,9.016,21]henicosa-1,3(11),4(9),5,7,12-hexaene-17-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains an aromatic '
               'beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@H](O)[C@@H](C4)N)C)C5=C3C=C(O)C=C5)=C6NC7=C(C26)C=CC=C7 '
               'NAME: 3-hydroxyholyrine A REASON: WRONGLY CLASSIFIED Molecule '
               'contains an aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'ClC1=CC=2C3=C(C=4NC=5C=CC=CC5C4C6=C3C(=O)NC6=O)NC2C=C1 NAME: '
               'Tjipanazole M REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@H](O)[C@@H](C4)NC(=O)C)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=CC=C7 '
               'NAME: 3′-N-acetyl-holyrine A REASON: WRONGLY CLASSIFIED '
               'Molecule contains an aromatic beta-carboline (pyridoindole) '
               'skeleton.\n'
               ' * SMILES: '
               'ClC1=CC=2C3=C(C=4NC=5C=CC(=CC5C4C6=C3C(=O)NC6)Cl)NC2C=C1 NAME: '
               'Tjipanazole K REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: C[C@@H](C(O)=O)c1ccc2c(c1)[nH]c1ccc(Cl)cc21 NAME: '
               '(R)-carprofen REASON: WRONGLY CLASSIFIED Molecule contains an '
               'aromatic beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@H](O)[C@@H](C4)NC(=O)C)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=C(O)C=C7 '
               "NAME: 9-hydroxy-3'-N-acetylholyrine A REASON: WRONGLY "
               'CLASSIFIED Molecule contains an aromatic beta-carboline '
               '(pyridoindole) skeleton.\n'
               'False negatives: SMILES: '
               'CN1C=C(N=C1)S(=O)(=O)N2CCC3(CC2)CN([C@H](C4=C3C5=C(N4C)C=C(C=C5)OC)CO)CC6=CC(=CC(=C6)OC)OC '
               'NAME: '
               "[(1R)-2-[(3,5-dimethoxyphenyl)methyl]-7-methoxy-9-methyl-1'-[(1-methyl-4-imidazolyl)sulfonyl]-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol "
               'REASON: MISSED Molecule does not appear to contain a '
               'beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'COC(=O)C(=C/O)\\[C@H]1C[C@H]2c3[nH]c4ccccc4c3CC[N+]2=C[C@@H]1C=C '
               'NAME: 4,21-Dehydrocorynantheine aldehyde REASON: MISSED '
               'Molecule does not appear to contain a beta-carboline '
               '(pyridoindole) skeleton.\n'
               ' * SMILES: '
               'CCS(=O)(=O)N1CCC2(CC1)CN([C@@H](C3=C2C4=C(N3C)C=C(C=C4)OC)CO)C(=O)NC5=C(ON=C5C)C '
               'NAME: '
               "(1S)-N-(3,5-dimethyl-4-isoxazolyl)-1'-ethylsulfonyl-1-(hydroxymethyl)-7-methoxy-9-methyl-2-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]carboxamide "
               'REASON: MISSED Molecule does not appear to contain a '
               'beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C1N2[C@H](C(=O)N3[C@@]1(OC)CC=4C5=C(C=C(OC)C=C5)NC4[C@@H]3C=C(C)C)CCC2 '
               'NAME: 9-methoxyfumitremorgin C REASON: MISSED Molecule does '
               'not appear to contain a beta-carboline (pyridoindole) '
               'skeleton.\n'
               ' * SMILES: '
               'C=1C=CC2=C(C1)C=3CC=[N+]4[C@](C3N2)(C[C@]5([C@]([C@@H](OC=C5C(OC)=O)C)(C4)[H])[H])[H] '
               'NAME: dihydroalstonine(1+) REASON: MISSED Molecule does not '
               'appear to contain a beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'O=C1N2C(C(=O)N([C@@]2(OC)C)/C=C/C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C '
               'NAME: Marinacarboline E REASON: MISSED Molecule does not '
               'appear to contain a beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: '
               'CN1CC2(CCN(CC2)C(=O)C3=CN=CC=C3)C4=C([C@@H]1CO)N(C5=C4C=CC(=C5)OC)C '
               'NAME: '
               "[(1R)-1-(hydroxymethyl)-7-methoxy-2,9-dimethyl-1'-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]-(3-pyridinyl)methanone "
               'REASON: MISSED Molecule does not appear to contain a '
               'beta-carboline (pyridoindole) skeleton.\n'
               ' * SMILES: COc1ccc2c(c1)[nH]c1c(C)nccc21 NAME: harmine REASON: '
               'MISSED Molecule does not appear to contain a beta-carboline '
               '(pyridoindole) skeleton.\n'
               ' * SMILES: O(C1=CC=2C3=C(NC2C=C1)CN(CC3)C)C NAME: '
               '2-Methyl-6-methoxy-1,2,3,4-tetrahydro-beta-carboline REASON: '
               'MISSED Molecule does not appear to contain a beta-carboline '
               '(pyridoindole) skeleton.\n'
               ' * SMILES: '
               'COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CN(C4)CC5=NOC(=C5)C6=CC=CC=C6)C(=O)NC7=CC=C(C=C7)F)CO '
               'NAME: '
               "(1R)-N-(4-fluorophenyl)-1-(hydroxymethyl)-7-methoxy-1'-[(5-phenyl-3-isoxazolyl)methyl]-2-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]carboxamide "
               'REASON: MISSED Molecule does not appear to contain a '
               'beta-carboline (pyridoindole) skeleton.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'No rings found in the '
                                               'molecule.'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'No rings found in the '
                                               'molecule.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'Molecule does not appear to '
                                               'contain the beta-carboline '
                                               'scaffold (a fused '
                                               'indole-pyridine system) based '
                                               'on ring analysis.'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'We can try a different approach rather than solely depending '
                 'on fixed SMARTS queries. The previous code was “hard‐coded” '
                 'to look for one aromatic SMARTS and one for a supposedly '
                 'hydrogenated variant. However, many beta‐carbolines (and '
                 'their derivatives) are defined by a fused bicyclic system in '
                 'which a five‐membered (indole, containing an –NH) ring is '
                 'fused to a six‐membered ring that has at least one nitrogen '
                 '(making it “pyrido” rather than a simple benzene as in '
                 'carbazole). Carbazole is a common false positive because it '
                 'has essentially the same fused ring sizes but the '
                 'six‐membered ring has no nitrogen. Also, many hydrogenated '
                 'variants do not exactly preserve the “aromatic” bond orders '
                 'predicted by RDKit. \n'
                 '\n'
                 'A strategy that overcomes these limitations is to “read” the '
                 'molecule’s ring information and examine the fused rings '
                 'directly. In the code below we do the following:\n'
                 '\u2003• Parse the molecule from a SMILES string.\n'
                 '\u2003• Pull the list of rings from the molecule.\n'
                 '\u2003• Look for a pair of rings that share at least two '
                 'atoms (i.e. a fused ring system).\n'
                 '\u2003• Among these, look for one five‐membered ring and one '
                 'six‐membered ring.\n'
                 '\u2003• Require that the five‐membered ring (the indole '
                 '“pyrrole” portion) contains exactly one nitrogen atom and '
                 'that the six‐membered ring contains at least one nitrogen '
                 '(thus excluding e.g. carbazole, which has the five‐membered '
                 'ring with “–NH” but a six‐membered benzene ring with no '
                 'nitrogen).\n'
                 'If such a fused ring pair is found, we classify the molecule '
                 'as belonging to the beta‐carboline (or hydrogenated '
                 'beta‐carboline) class. (Of course many edge cases may still '
                 'be mis‐classified, but this approach attempts to capture the '
                 'key scaffold features without being overly dependent on '
                 'fixed SMARTS.)\n'
                 '\n'
                 'Below is the complete Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 789,
    'num_false_positives': 3126,
    'num_true_negatives': 138385,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.20153256704980843,
    'recall': 1.0,
    'f1': 0.3354591836734694,
    'accuracy': 0.9780323260716796,
    'negative_predictive_value': 1.0}