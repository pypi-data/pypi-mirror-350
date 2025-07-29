"""
Classifies: CHEBI:26888 tetrachlorobenzene
"""
"""
Classifies: Tetrachlorobenzene
Definition:
  Any member of the class of chlorobenzenes carrying four chlorine atoms attached directly 
  to a benzene ring. Valid molecules may have an extra substituent if it is either a simple group 
  (e.g. –OH or –CN) or a benzene ring linkage as in biphenyls. Extra substituents that carry exotic 
  features (e.g. nonzero formal charge, or larger multi–atom groups that are not directly a benzene ring)
  disfavor the classification.
  
Improved heuristic:
  1. Parse the molecule and (if needed) select its largest fragment.
  2. For every 6–membered ring composed of aromatic carbons (a benzene candidate) do:
      – For each ring atom, consider every neighbor that is not part of the ring.
      – If the neighbor is Cl, count it.
      – Otherwise, if the substituent is allowed (see allowed_substituent) then ignore it.
         Otherwise, flag the ring as having disallowed extra groups.
      – If the candidate benzene ring has exactly four Cl substituents and no disallowed extras, 
        then return True (with a proper explanation).
  3. If no candidate ring qualifies, return False.
  
Note: This heuristic is not perfect – if the analysis is too ambiguous the function returns (None, None).
"""

from rdkit import Chem

def is_tetrachlorobenzene(smiles: str):
    """
    Determines if a molecule is a tetrachlorobenzene based on its SMILES string.
  
    The function first looks for candidate benzene rings (6 aromatic carbons). For each candidate, it
    counts how many chlorine atoms are directly bonded to ring carbons. Non–chlorine substituents
    are allowed only if they are simple groups – either a single atom such as –OH, a –CN group,
    or a direct benzene–benzene (biphenyl) linkage.
  
    Args:
       smiles (str): SMILES string of the molecule.
  
    Returns:
       (bool, str): A tuple where the first element is True if a qualifying benzene ring is found,
                    and False otherwise; the second element gives a reason.
       If the analysis cannot be confidently done, returns (None, None).
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    try:
        Chem.SanitizeMol(mol)
    except Exception as e:
        return False, f"Sanitization error: {e}"

    # If multiple fragments are present, use the largest fragment.
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    if len(frags) > 1:
        mol = max(frags, key=lambda m: m.GetNumHeavyAtoms())
    
    ring_info = mol.GetRingInfo()
    if not ring_info or ring_info.NumRings() == 0:
        return False, "No rings found in the molecule"
    
    # Helper: decide whether a substituent (atom) is allowed.
    # Allowed if:
    #   - It is chlorine (handled separately in the main loop).
    #   - It is a small simple group such as –OH (oxygen with degree 1).
    #   - It is a carbon that is part of a cyanide (triple bond to nitrogen).
    #   - It is an aromatic carbon that belongs to a six-membered aromatic ring
    #     (which we interpret as a biphenyl linkage).
    def allowed_substituent(neigh, candidate_ring):
        # Exclude substituents carrying a formal charge.
        if neigh.GetFormalCharge() != 0:
            return False
        symbol = neigh.GetSymbol()
        # Allow single–atom substituents (–OH, –F, –I, etc.) except we already count Cl separately.
        if neigh.GetDegree() == 1:
            return True
        # Allow a carbon that is connected via a triple bond to a nitrogen (–CN)
        if symbol == "C":
            for bond in neigh.GetBonds():
                if bond.GetBondType() == Chem.BondType.TRIPLE:
                    other = bond.GetOtherAtom(neigh)
                    if other.GetAtomicNum() == 7:
                        return True
        # Allow biphenyl linkages: if the neighbor is an aromatic carbon that belongs to a six-membered ring
        # (other than the candidate ring), then permit.
        if symbol == "C" and neigh.GetIsAromatic():
            for r in ring_info.AtomRings():
                if len(r) == 6 and neigh.GetIdx() in r:
                    # check that this ring is not the candidate ring
                    if set(r) != set(candidate_ring):
                        return True
        return False

    # Loop over rings: only consider 6-membered rings that are all aromatic carbons (benzene candidates).
    for candidate_ring in ring_info.AtomRings():
        if len(candidate_ring) != 6:
            continue
        is_benzene = True
        for idx in candidate_ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6 or not atom.GetIsAromatic():
                is_benzene = False
                break
        if not is_benzene:
            continue
        
        # Examine substituents attached directly to the benzene candidate.
        cl_count = 0
        disallowed_extras = 0
        for idx in candidate_ring:
            atom = mol.GetAtomWithIdx(idx)
            for neigh in atom.GetNeighbors():
                # Only consider atoms that are not in the candidate ring.
                if neigh.GetIdx() in candidate_ring:
                    continue
                if neigh.GetAtomicNum() == 17:
                    cl_count += 1
                else:
                    if not allowed_substituent(neigh, candidate_ring):
                        disallowed_extras += 1
        # To qualify, require exactly 4 Cl atoms and no disallowed extra substituents.
        if cl_count == 4 and disallowed_extras == 0:
            return True, "Found benzene ring with exactly 4 chlorine substituents and acceptable additional groups"
    
    # If none of the candidate benzene rings qualifies, report failure.
    return False, "No benzene ring with exactly 4 chlorine substituents (and acceptable extra groups) found"

# Example usage:
if __name__ == "__main__":
    # Test with one known tetrachlorobenzene:
    test_smiles = "Clc1cc(Cl)c(Cl)c(Cl)c1"
    is_tc, reason = is_tetrachlorobenzene(test_smiles)
    print(is_tc, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26888',
                          'name': 'tetrachlorobenzene',
                          'definition': 'Any member of the class of '
                                        'chlorobenzenes carrying four chloro '
                                        'groups at unspecified positions.',
                          'parents': ['CHEBI:23132'],
                          'xrefs': ['CAS:12408-10-5'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 93,
                           'log_lines_of_code': 4.532599493153256,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
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
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
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
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 6,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetOtherAtom',
                                                 'GetMolFrags',
                                                 'GetNumHeavyAtoms',
                                                 'GetSymbol',
                                                 'GetIdx',
                                                 'GetIsAromatic',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetBonds',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'SanitizeMol',
                                                 'GetDegree',
                                                 'GetNeighbors',
                                                 'GetBondType',
                                                 'GetRingInfo',
                                                 'GetFormalCharge'],
                           'methods_called_count': 18,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_tetrachlorobenzene(smiles: str):',
                                       'allowed_substituent(neigh, '
                                       'candidate_ring):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Sanitization error: {e}"',
                                          'False, "No rings found in the '
                                          'molecule"',
                                          'False',
                                          'True',
                                          'True',
                                          'True',
                                          'False',
                                          'True, "Found benzene ring with '
                                          'exactly 4 chlorine substituents and '
                                          'acceptable additional groups"',
                                          'False, "No benzene ring with '
                                          'exactly 4 chlorine substituents '
                                          '(and acceptable extra groups) '
                                          'found"'],
                           'returns_count': 10,
                           'complexity': 8.106519898630651},
    'message': '\n'
               'Attempt failed: F1 score of 0.7906976744186047 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: Clc1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               '1,2,3,5-tetrachlorobenzene REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Clc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,3',4,5-pentachlorobiphenyl REASON: CORRECT Found benzene "
               'ring with exactly 4 chlorine substituents and acceptable '
               'additional groups\n'
               ' * SMILES: Clc1ccc(Cl)c(Cl)c1Cl NAME: '
               '1,2,3,4-tetrachlorobenzene REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Oc1c(Cl)c(Cl)cc(Cl)c1Cl NAME: '
               '2,3,5,6-tetrachlorophenol REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: C1(O)=C(C(=C(C(=C1)Cl)Cl)Cl)Cl NAME: '
               '2,3,4,5-tetrachlorophenol REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Oc1c(Cl)c(Cl)cc(c1Cl)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,2',3',4,4',5,5'-Heptachloro-3-biphenylol REASON: CORRECT "
               'Found benzene ring with exactly 4 chlorine substituents and '
               'acceptable additional groups\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,3',4,4',5-Hexachlorobiphenyl REASON: CORRECT Found benzene "
               'ring with exactly 4 chlorine substituents and acceptable '
               'additional groups\n'
               ' * SMILES: Oc1ccc(cc1)-c1c(Cl)c(Cl)c(O)c(Cl)c1Cl NAME: '
               "2,3,5,6-tetrachloro-1,1'-biphenyl-4,4'-diol REASON: CORRECT "
               'Found benzene ring with exactly 4 chlorine substituents and '
               'acceptable additional groups\n'
               ' * SMILES: Clc1ccc(cc1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,4,4',5-Pentachlorobiphenyl REASON: CORRECT Found benzene "
               'ring with exactly 4 chlorine substituents and acceptable '
               'additional groups\n'
               ' * SMILES: Oc1c(O)c(Cl)c(Cl)c(Cl)c1Cl NAME: '
               'tetrachlorocatechol REASON: CORRECT Found benzene ring with '
               'exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Clc1cc(Cl)c(Cl)c(-c2ccccc2)c1Cl NAME: '
               '2,3,5,6-tetrachlorobiphenyl REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Oc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2',3',4',5'-tetrachlorobiphenyl-3-ol REASON: CORRECT Found "
               'benzene ring with exactly 4 chlorine substituents and '
               'acceptable additional groups\n'
               ' * SMILES: Clc1cc(-c2ccccc2)c(Cl)c(Cl)c1Cl NAME: '
               '2,3,4,5-tetrachlorobiphenyl REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Clc1cc(Cl)c(Cl)cc1Cl NAME: '
               '1,2,4,5-tetrachlorobenzene REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Oc1c(Cl)c(Cl)c(O)c(Cl)c1Cl NAME: '
               'tetrachlorohydroquinone REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               ' * SMILES: Oc1c(Cl)c(Cl)c(c(Cl)c1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',3,4',5,5',6-heptachlorobiphenyl REASON: CORRECT "
               'Found benzene ring with exactly 4 chlorine substituents and '
               'acceptable additional groups\n'
               ' * SMILES: C1(O)=C(C(=C(C=C1Cl)Cl)Cl)Cl NAME: '
               '2,3,4,6-tetrachlorophenol REASON: CORRECT Found benzene ring '
               'with exactly 4 chlorine substituents and acceptable additional '
               'groups\n'
               'False positives: SMILES: '
               'ClC=1C(C=2C(Cl)=CC(Cl)=C(Cl)C2)=CC(Cl)=C(Cl)C1Cl NAME: PCB180 '
               'REASON: WRONGLY CLASSIFIED Found benzene ring with exactly 4 '
               'chlorine substituents and acceptable additional groups\n'
               'False negatives: SMILES: '
               'OC1=C(Br)C2=C(C=C1Br)C1(OC(=O)C3=C1C(Cl)=C(Cl)C(Cl)=C3Cl)C1=CC(Br)=C(O)C(Br)=C1O2 '
               'NAME: phloxine O REASON: MISSED No benzene ring with exactly 4 '
               'chlorine substituents (and acceptable extra groups) found\n'
               ' * SMILES: '
               'OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1-c1c2cc(Br)c(O)c(Br)c2oc2c(Br)c(=O)c(Br)cc12 '
               "NAME: 2',4',5',7'-tetrabromo-2,3,4,5-tetrachlorofluorescein "
               'REASON: MISSED No benzene ring with exactly 4 chlorine '
               'substituents (and acceptable extra groups) found\n'
               ' * SMILES: '
               'OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1-c1c2cc(I)c(O)c(I)c2oc2c(I)c(=O)c(I)cc12 '
               'NAME: rose bengal free acid REASON: MISSED No benzene ring '
               'with exactly 4 chlorine substituents (and acceptable extra '
               'groups) found\n'
               ' * SMILES: Clc1c(Cl)c(Cl)c2C(=O)OC(=O)c2c1Cl NAME: '
               'tetrachlorophthalic anhydride REASON: MISSED No benzene ring '
               'with exactly 4 chlorine substituents (and acceptable extra '
               'groups) found\n'
               ' * SMILES: Clc1c(Cl)c(C#N)c(Cl)c(C#N)c1Cl NAME: chlorothalonil '
               'REASON: MISSED No benzene ring with exactly 4 chlorine '
               'substituents (and acceptable extra groups) found\n'
               ' * SMILES: Clc1c2COC(=O)c2c(Cl)c(Cl)c1Cl NAME: '
               '4,5,6,7-tetrachloro-2-benzofuran-1(3H)-one REASON: MISSED No '
               'benzene ring with exactly 4 chlorine substituents (and '
               'acceptable extra groups) found\n'
               ' * SMILES: [O-][N+](=O)c1c(Cl)c(Cl)cc(Cl)c1Cl NAME: tecnazene '
               'REASON: MISSED No benzene ring with exactly 4 chlorine '
               'substituents (and acceptable extra groups) found\n'
               ' * SMILES: OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1C(=O)Nc1cccc(Cl)c1Cl '
               'NAME: tecloftalam REASON: MISSED No benzene ring with exactly '
               '4 chlorine substituents (and acceptable extra groups) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No benzene ring with exactly 4 '
                                               'chlorine substituents (and '
                                               'acceptable extra groups) '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No benzene ring with exactly 4 '
                                               'chlorine substituents (and '
                                               'acceptable extra groups) '
                                               'found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No benzene ring with exactly 4 '
                                               'chlorine substituents (and '
                                               'acceptable extra groups) '
                                               'found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No benzene ring with exactly 4 '
                                               'chlorine substituents (and '
                                               'acceptable extra groups) '
                                               'found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No benzene ring with exactly 4 '
                                               'chlorine substituents (and '
                                               'acceptable extra groups) '
                                               'found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No benzene ring with exactly 4 '
                                               'chlorine substituents (and '
                                               'acceptable extra groups) '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No rings found in the '
                                               'molecule'}],
    'sample_false_negatives': [   {   'smiles': 'OC1=C(Br)C2=C(C=C1Br)C1(OC(=O)C3=C1C(Cl)=C(Cl)C(Cl)=C3Cl)C1=CC(Br)=C(O)C(Br)=C1O2',
                                      'name': 'phloxine O',
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'},
                                  {   'smiles': 'OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1-c1c2cc(Br)c(O)c(Br)c2oc2c(Br)c(=O)c(Br)cc12',
                                      'name': "2',4',5',7'-tetrabromo-2,3,4,5-tetrachlorofluorescein",
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'},
                                  {   'smiles': 'OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1-c1c2cc(I)c(O)c(I)c2oc2c(I)c(=O)c(I)cc12',
                                      'name': 'rose bengal free acid',
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'},
                                  {   'smiles': 'Clc1c(Cl)c(Cl)c2C(=O)OC(=O)c2c1Cl',
                                      'name': 'tetrachlorophthalic anhydride',
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'},
                                  {   'smiles': 'Clc1c2COC(=O)c2c(Cl)c(Cl)c1Cl',
                                      'name': '4,5,6,7-tetrachloro-2-benzofuran-1(3H)-one',
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'},
                                  {   'smiles': '[O-][N+](=O)c1c(Cl)c(Cl)cc(Cl)c1Cl',
                                      'name': 'tecnazene',
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'},
                                  {   'smiles': 'OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1C(=O)Nc1cccc(Cl)c1Cl',
                                      'name': 'tecloftalam',
                                      'reason': 'No benzene ring with exactly '
                                                '4 chlorine substituents (and '
                                                'acceptable extra groups) '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'Below is one way to improve on the previous heuristic. In '
                 'our reasoning we noticed that (a) checking for exactly four '
                 'Cl “neighbors” on a benzene‐ring must be performed on a '
                 '“clean” benzene candidate (a 6–membered aromatic ring) and '
                 '(b) extra substituents should be allowed only if they are '
                 '“very simple” (for example, –OH or –CN) or if the connection '
                 'comes from a direct benzene–benzene (biphenyl) linkage. In '
                 'our first attempt many valid tetrachlorobenzenes were missed '
                 '(false negatives) because the extra groups (for example, an '
                 'acyl or other “multi–atom” branch) were simply ruled out, '
                 'while a PCB (a biphenyl with extra substituents) was '
                 'mistakenly accepted. One improvement is to use a more '
                 'refined “allowed substituent” test. Here we do the following '
                 'for each candidate benzene ring (a 6–atom aromatic carbon '
                 'ring):\n'
                 '\n'
                 '1. For every ring atom we loop over the neighbors (those not '
                 'in the ring). If a neighbor is chlorine (atomic number 17) '
                 'we count that as a Cl substituent.\n'
                 '2. Otherwise, we require that the substituent be “simple.” '
                 'In our heuristic an allowed substituent is one that\n'
                 '   • is a single–atom substituent (for example oxygen whose '
                 'visible degree is 1, as in –OH), or\n'
                 '   • is a carbon atom that is directly attached via a triple '
                 'bond to a nitrogen (as in –CN), or\n'
                 '   • is itself an aromatic carbon that belongs to another '
                 'six–membered aromatic ring (so that a biphenyl linkage is '
                 'permitted).\n'
                 '3. If any substituent fails this test we flag the candidate '
                 'ring as “exotic” and do not qualify it.\n'
                 '4. Finally, if one (or more) benzene candidates has exactly '
                 'four directly attached chlorine atoms and all other '
                 'substituents are allowed, we classify the molecule as a '
                 'tetrachlorobenzene.\n'
                 '\n'
                 'The following Python code (using RDKit) implements this '
                 'strategy in a single code block. (Note that if the task '
                 'proves too challenging the function may return (None, '
                 'None).)\n'
                 '\n'
                 'Below is the complete program in one code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 1,
    'num_true_negatives': 142274,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.9473684210526315,
    'recall': 0.72,
    'f1': 0.8181818181818181,
    'accuracy': 0.9999437807449051,
    'negative_predictive_value': 0.9999508015827834}