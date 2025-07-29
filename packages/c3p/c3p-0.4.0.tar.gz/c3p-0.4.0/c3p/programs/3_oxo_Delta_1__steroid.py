"""
Classifies: CHEBI:20156 3-oxo-Delta(1) steroid
"""
#!/usr/bin/env python
"""
Classifies: 3-oxo-Delta(1) steroid, defined as any 3-oxo steroid that contains a
double bond between positions 1 and 2.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_3_oxo_Delta_1__steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo-Delta(1) steroid.
    This function uses a simplified algorithm that:
      1. Checks if the molecule has four fused rings (steroid nucleus).
      2. Searches for a ring carbonyl ([R]C(=O)[R]) as the 3-oxo feature.
      3. Checks if the carbonyl carbon has an adjacent double bond (C=C) in the same ring,
         as an approximation of the Delta(1) (1,2-double bond) feature.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a 3-oxo-Delta(1) steroid, False otherwise.
        str: Reason for the classification.
    """
    # Parse the SMILES string into an RDKit molecule object.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get ring information. Steroid nucleus (cyclopenta[a]phenanthrene) consists of 4 fused rings.
    ring_info = mol.GetRingInfo().AtomRings()
    if len(ring_info) != 4:
        return False, f"Expected 4 fused rings for a steroid nucleus, found {len(ring_info)} rings"
    
    # Find a ring carbonyl group by matching the SMARTS pattern that enforces the carbonyl to be in a ring.
    # [R] means the atom is in a ring.
    carbonyl_pattern = Chem.MolFromSmarts("[R]C(=O)[R]")
    carbonyl_matches = mol.GetSubstructMatches(carbonyl_pattern)
    if not carbonyl_matches:
        return False, "No ring carbonyl (3-oxo) group found"
    
    # Convert each ring (tuple of atom indices) into a set for membership testing.
    rings = [set(r) for r in ring_info]
    
    # Check each matched ring carbonyl group and see if the carbonyl carbon has an adjacent C=C
    # bond where both atoms are contained in at least one common ring.
    has_delta1 = False
    for match in carbonyl_matches:
        # match tuple: (carbonyl carbon index, oxygen index, adjacent carbon index)
        carbonyl_idx = match[0]
        # Get all rings that contain the carbonyl atom:
        rings_with_carbonyl = [r for r in rings if carbonyl_idx in r]
        if not rings_with_carbonyl:
            continue  # should not happen because of the [R] in the SMARTS
        
        # Inspect all bonds from the carbonyl carbon
        atom = mol.GetAtomWithIdx(carbonyl_idx)
        for bond in atom.GetBonds():
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                neighbor_idx = bond.GetOtherAtomIdx(carbonyl_idx)
                # Check if the neighbor also lies in one of the same rings as the carbonyl.
                for ring in rings_with_carbonyl:
                    if neighbor_idx in ring:
                        has_delta1 = True
                        break
            if has_delta1:
                break
        if has_delta1:
            break
    
    if not has_delta1:
        return False, "No double bond adjacent to the ring carbonyl found (Delta(1) feature missing)"
    
    return True, "Molecule has a steroid nucleus with a 3-oxo group and a Delta(1) double bond"

# Example usage (uncomment the following lines to test):
# smiles_example = "C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)C=C[C@]34C)[C@@H]1CC[C@@H]2O"  # example steroid SMILES
# print(is_3_oxo_Delta_1__steroid(smiles_example))


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20156',
                          'name': '3-oxo-Delta(1) steroid',
                          'definition': 'Any 3-oxo steroid that contains a '
                                        'double bond between positions 1 and '
                                        '2.',
                          'parents': ['CHEBI:47788', 'CHEBI:51689'],
                          'xrefs': [   'KEGG:C02941',
                                       'MetaCyc:3-Oxo-Delta-1-Steroids'],
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
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetOtherAtomIdx',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetBonds',
                                                 'MolFromSmarts',
                                                 'GetBondType',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 9,
                           'smarts_strings': ['[R]C(=O)[R]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_3_oxo_Delta_1__steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Expected 4 fused rings for '
                                          'a steroid nucleus, found '
                                          '{len(ring_info)} rings"',
                                          'False, "No ring carbonyl (3-oxo) '
                                          'group found"',
                                          'False, "No double bond adjacent to '
                                          'the ring carbonyl found (Delta(1) '
                                          'feature missing)"',
                                          'True, "Molecule has a steroid '
                                          'nucleus with a 3-oxo group and a '
                                          'Delta(1) double bond"'],
                           'returns_count': 5,
                           'complexity': 5.00507033814703},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 3 '
                                               'rings'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 0 '
                                               'rings'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 2 '
                                               'rings'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 0 '
                                               'rings'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No ring carbonyl (3-oxo) group '
                                               'found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 3 '
                                               'rings'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 2 '
                                               'rings'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 5 '
                                               'rings'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 0 '
                                               'rings'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Expected 4 fused rings for a '
                                               'steroid nucleus, found 0 '
                                               'rings'}],
    'sample_false_negatives': [   {   'smiles': 'C=1[C@@]2([C@@]3(CC[C@@]/4([C@@]([C@]3(C([C@H]([C@]2([C@@H](C(C1)=O)C)[H])OC(=O)C)=O)C)(C[C@@H](\\C4=C(\\CCC=C(C)C)/C(=O)OC)OC(=O)C)C)[H])[H])C',
                                      'name': 'helvolic acid methyl ester',
                                      'reason': 'No double bond adjacent to '
                                                'the ring carbonyl found '
                                                '(Delta(1) feature missing)'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)C=C[C@]4(C)[C@@]3([H])CC[C@]12COC(C)=O)[C@H](C)[C@H]1CC(C)=C(C)C(=O)O1',
                                      'name': 'minabeolide 2',
                                      'reason': 'Expected 4 fused rings for a '
                                                'steroid nucleus, found 5 '
                                                'rings'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1(F)[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@H]2OC3(CCCC3)O[C@@]12C(=O)COC(C)=O',
                                      'name': 'amcinonide',
                                      'reason': 'Expected 4 fused rings for a '
                                                'steroid nucleus, found 6 '
                                                'rings'},
                                  {   'smiles': 'C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)C=C[C@]34C)[C@@H]1CC[C@@H]2O',
                                      'name': '17beta-hydroxy-5beta-androst-1-en-3-one',
                                      'reason': 'No double bond adjacent to '
                                                'the ring carbonyl found '
                                                '(Delta(1) feature missing)'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)C=C[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@H]1CC[C@H](C)C(=O)O1',
                                      'name': 'minabeolide 4',
                                      'reason': 'Expected 4 fused rings for a '
                                                'steroid nucleus, found 5 '
                                                'rings'},
                                  {   'smiles': 'C[C@H](CCC[C@H](C)C(O)=O)[C@H]1CC[C@H]2C3=CC[C@H]4CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C',
                                      'name': 'Delta(1),Delta(7)-dafachronic '
                                              'acid',
                                      'reason': 'No double bond adjacent to '
                                                'the ring carbonyl found '
                                                '(Delta(1) feature missing)'},
                                  {   'smiles': 'CCC(=O)O[C@H]1CC[C@H]2[C@@H]3CC[C@H]4CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C',
                                      'name': '17beta-hydroxy-5alpha-androst-1-en-3-one '
                                              'propionate',
                                      'reason': 'No double bond adjacent to '
                                                'the ring carbonyl found '
                                                '(Delta(1) feature missing)'},
                                  {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12COC(C)=O)[C@H]1C[C@H](C)[C@H](C)C(=O)O1',
                                      'name': 'paraminabeolide B',
                                      'reason': 'Expected 4 fused rings for a '
                                                'steroid nucleus, found 5 '
                                                'rings'},
                                  {   'smiles': 'C1C[C@@]2([C@@]([C@@]3([C@@]1(CC(C=C3)=O)[H])C)(CC[C@@]4(C(=O)CC[C@@]24[H])C)[H])[H]',
                                      'name': '5alpha-androst-1-ene-3,17-dione',
                                      'reason': 'No double bond adjacent to '
                                                'the ring carbonyl found '
                                                '(Delta(1) feature missing)'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)C=C[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@H]1CC(C)=C(C)C(=O)O1',
                                      'name': 'minabeolide 1',
                                      'reason': 'Expected 4 fused rings for a '
                                                'steroid nucleus, found 5 '
                                                'rings'}],
    'attempt': 0,
    'reasoning': 'Below is one way to approach the problem. Note that '
                 '“3‑oxo‐Delta(1) steroid” requires finding a steroid nucleus '
                 '(the typical four‐ring system), a ring carbonyl (the '
                 '“3‑oxo”) and—crucially—a C=C double bond in the same ring '
                 '(the “Delta(1)” feature). In the code we:\n'
                 '\n'
                 '1. Parse the SMILES string.\n'
                 '2. Check that the molecule has four fused rings (expected '
                 'for a steroid nucleus).\n'
                 '3. Use a SMARTS pattern ([R]C(=O)[R]) to look for a carbonyl '
                 'group that is part of a ring.\n'
                 '4. For each such carbonyl group, examine its bonds to see if '
                 'one of its neighbors (in the same ring) is connected by a '
                 'double bond—this is our approximation for having a Delta(1) '
                 '(C=C) feature.\n'
                 '5. If both criteria are met, we classify the molecule as a '
                 '3‑oxo‑Delta(1) steroid.\n'
                 '\n'
                 'Keep in mind that detecting steroid substructures by “ring '
                 'count” and relative bond types is a simplified approach and '
                 'may not work in all edge cases.\n'
                 '\n'
                 'Below is the complete Python code in a single code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 59,
    'num_false_positives': 1754,
    'num_true_negatives': 140472,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.03254274682846112,
    'recall': 0.7972972972972973,
    'f1': 0.06253312135665076,
    'accuracy': 0.9875685172171469,
    'negative_predictive_value': 0.9998932285549552}