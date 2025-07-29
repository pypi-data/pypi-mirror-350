"""
Classifies: CHEBI:27096 trichlorobenzene
"""
"""
Classifies: trichlorobenzene
Definition: Any member of the class of chlorobenzenes carrying three chloro substituents at unspecified positions.
A candidate is identified by finding an isolated (non‐fused) benzene ring (six aromatic carbons) and then checking that
exactly 3 of the ring carbons bear a terminal chlorine substituent. In addition, any other substituent attached to the ring
(which is not an aromatic fragment) must be “small” (here, defined as having 2 or fewer heavy atoms).
"""

from rdkit import Chem

def is_trichlorobenzene(smiles: str):
    """
    Determines if a molecule qualifies as a trichlorobenzene based on its SMILES string.
    
    The algorithm:
      1. Parse and sanitize the molecule.
      2. Identify rings that are candidate benzene fragments:
         - a ring of exactly 6 atoms,
         - all atoms are aromatic carbons.
         - the ring is isolated (not fused with any other ring; i.e. it does not share 2 or more atoms with any other ring).
      3. For each candidate ring, examine each ring atom’s neighbors that are not in the ring:
         - If the neighbor is a chlorine (atomic number 17) and is terminal (degree==1) then count it.
         - Otherwise, perform a DFS starting from that neighbor – but only “count” heavy atoms if no aromatic atom is encountered.
           (If an aromatic atom is reached, we assume this bond is simply the linkage to an aromatic fragment and allow it.)
         - If any substituent (other than Cl) is found to span more than 2 heavy atoms [without quickly “hitting” an aromatic atom],
           then disqualify that candidate benzene ring.
      4. If a candidate ring has exactly 3 valid terminal Cl substituents (and no disqualifying larger non‐Cl substituents),
         return True plus an explanation.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if a candidate ring meeting the criteria is found, False otherwise.
        str: Explanation of the classification decision.
    """
    # Helper DFS that traverses a substituent fragment (avoiding the candidate ring atom that initiated the bond)
    # The DFS returns a tuple (count, aromatic_found) where count is the total number of heavy atoms (atomic number > 1)
    # encountered in the fragment (if no aromatic atom is encountered) and aromatic_found is True if an aromatic atom is reached.
    def dfs_substituent(atom, origin_idx, visited):
        # If we hit an aromatic atom, then we mark that branch as aromatic.
        if atom.GetIsAromatic():
            return (0, True)
        # Count this heavy atom (ignore hydrogens by atomic number <= 1)
        count = 1 if atom.GetAtomicNum() > 1 else 0
        aromatic_found = False
        visited.add(atom.GetIdx())
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() == origin_idx or nbr.GetIdx() in visited:
                continue
            sub_count, sub_arom = dfs_substituent(nbr, origin_idx, visited)
            if sub_arom:
                aromatic_found = True
            else:
                count += sub_count
            # If already aromatic found in one branch, we can stop further counting as this branch is allowed.
            if aromatic_found:
                # No need to accumulate further heavy atoms.
                break
        return (count, aromatic_found)
    
    # Parse the input SMILES.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    try:
        Chem.SanitizeMol(mol)
    except Exception as e:
        return False, f"Sanitization failed: {e}"
    
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()
    
    # Loop over all rings in the molecule to find a candidate benzene ring.
    for ring in atom_rings:
        if len(ring) != 6:
            continue
        
        # Check that every atom in the ring is a carbon and is aromatic.
        is_candidate = True
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6 or not atom.GetIsAromatic():
                is_candidate = False
                break
        if not is_candidate:
            continue
            
        # Exclude fused rings: if the candidate ring shares 2 or more atoms with any other ring in the molecule.
        fused = False
        for other_ring in atom_rings:
            if other_ring == ring:
                continue
            if len(set(ring).intersection(other_ring)) >= 2:
                fused = True
                break
        if fused:
            continue
        
        # For the candidate benzene ring, check the substituents.
        cl_count = 0  # count of terminal chlorine substituents on the ring.
        disqualified = False
        
        # Iterate over each atom in the candidate ring.
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                # Skip neighbors that are part of the ring.
                if nbr.GetIdx() in ring:
                    continue
                # If the neighbor is an aromatic atom, then we assume it is an attached aromatic fragment.
                if nbr.GetIsAromatic():
                    continue
                # If the neighbor is chlorine (atomic #17) and is terminal (degree == 1), count it.
                if nbr.GetAtomicNum() == 17 and nbr.GetDegree() == 1:
                    cl_count += 1
                else:
                    # For other substituents, assess its "size" using DFS.
                    # Create a new visited set for each substituent branch.
                    visited = set()
                    count, arom_found = dfs_substituent(nbr, atom.GetIdx(), visited)
                    # If an aromatic fragment is encountered in this substituent branch,
                    # then we treat it as not disqualifying (assumed to be a simple aromatic extension).
                    if not arom_found and count > 2:
                        disqualified = True
                        # We can break out if one substituent is too extensive.
                        break
            if disqualified:
                break
        
        # We accept this candidate ring only if there are exactly 3 terminal Cl substituents and no disqualifying substituents.
        if not disqualified and cl_count == 3:
            return True, ("Found an isolated benzene ring with exactly three terminal chlorine substituents "
                          "and only small (or aromatic) additional substituents")
    
    return False, ("No isolated benzene ring with exactly three terminal chlorine substituents "
                   "(with acceptable small or aromatic substituents) found")


# (Optional) Example testing
if __name__ == '__main__':
    test_smiles = [
        # Expected True examples:
        "Oc1c(Cl)cc(c(Cl)c1Cl)-c1ccc(Cl)c(Cl)c1Cl",  # 2,2',3,3',4',5-Hexachloro-4-biphenylol
        "Clc1cccc(Cl)c1Cl",  # 1,2,3-trichlorobenzene
        # Some examples that should be False:
        "C=1(C(=C(C=C(C1Cl)O)Cl)[O-])Cl",  # 2,3,6-trichloro-4-hydroxyphenolate (false positive in previous attempt)
        "CON([C@@H](C)Cc1c(Cl)cc(Cl)cc1Cl)C(=O)c1cn(C)nc1C(F)F"  # (S)-pydiflumetofen (false negative in previous attempt)
    ]
    for smi in test_smiles:
        result, reason = is_trichlorobenzene(smi)
        print(f"SMILES: {smi}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27096',
                          'name': 'trichlorobenzene',
                          'definition': 'Any member of the class of '
                                        'chlorobenzenes carrying three chloro '
                                        'substituents at unspecified '
                                        'positions.',
                          'parents': ['CHEBI:23132'],
                          'xrefs': ['Wikipedia:Trichlorobenzene'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 125,
                           'log_lines_of_code': 4.8283137373023015,
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
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
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
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
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
                                                 2],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetNeighbors',
                                                 'GetDegree',
                                                 'GetIdx',
                                                 'AtomRings',
                                                 'GetRingInfo',
                                                 'SanitizeMol',
                                                 'GetAtomWithIdx',
                                                 'add',
                                                 'intersection',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_trichlorobenzene(smiles: str):',
                                       'dfs_substituent(atom, origin_idx, '
                                       'visited):'],
                           'defs_count': 2,
                           'returns': [   'True plus an explanation.',
                                          '(0, True)',
                                          '(count, aromatic_found)',
                                          'False, "Invalid SMILES string"',
                                          'False, f"Sanitization failed: {e}"',
                                          'True, ("Found an isolated benzene '
                                          'ring with exactly three terminal '
                                          'chlorine substituents "',
                                          'False, ("No isolated benzene ring '
                                          'with exactly three terminal '
                                          'chlorine substituents "'],
                           'returns_count': 7,
                           'complexity': 6.36566274746046},
    'message': '\n'
               'Attempt failed: F1 score of 0.6835443037974683 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'Oc1c(Cl)cc(c(Cl)c1Cl)-c1ccc(Cl)c(Cl)c1Cl NAME: '
               "2,2',3,3',4',5-Hexachloro-4-biphenylol REASON: CORRECT Found "
               'an isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccccc1-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',4,5-tetrachlorobiphenyl REASON: CORRECT Found an isolated "
               'benzene ring with exactly three terminal chloro substituents '
               'and only small additional substituents\n'
               ' * SMILES: Oc1cc(Cl)c(Cl)c(Cl)c1-n1cc(Cl)c(Cl)c1Cl NAME: '
               'neopyrrolomycin B REASON: CORRECT Found an isolated benzene '
               'ring with exactly three terminal chloro substituents and only '
               'small additional substituents\n'
               ' * SMILES: NCc1c(O)c(Cl)cc(Cl)c1Cl NAME: '
               '2-(aminomethyl)-3,4,6-trichlorophenol REASON: CORRECT Found an '
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1cccc(Cl)c1Cl NAME: 1,2,3-trichlorobenzene '
               'REASON: CORRECT Found an isolated benzene ring with exactly '
               'three terminal chloro substituents and only small additional '
               'substituents\n'
               ' * SMILES: Clc1cc(Cl)c(Cl)c(c1)-c1cc(Cl)cc(Cl)c1Cl NAME: '
               "2,2',3,3',5,5'-hexachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(cc1)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "2,4,4',6-tetrachlorobiphenyl REASON: CORRECT Found an isolated "
               'benzene ring with exactly three terminal chloro substituents '
               'and only small additional substituents\n'
               ' * SMILES: Oc1ccc(c(Cl)c1)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',4',6'-tetrachlorobiphenyl REASON: CORRECT Found "
               'an isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,3',4,4',5-Pentachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(Cl)c(Cl)c1 NAME: 1,2,4-trichlorobenzene '
               'REASON: CORRECT Found an isolated benzene ring with exactly '
               'three terminal chloro substituents and only small additional '
               'substituents\n'
               ' * SMILES: Clc1cc(Cl)cc(Cl)c1 NAME: 1,3,5-trichlorobenzene '
               'REASON: CORRECT Found an isolated benzene ring with exactly '
               'three terminal chloro substituents and only small additional '
               'substituents\n'
               ' * SMILES: Oc1c(Cl)cc(-c2ccc(Cl)c(Cl)c2)c(Cl)c1Cl NAME: '
               "4-Hydroxy-2,3,3',4',5-pentachlorobiphenyl REASON: CORRECT "
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: Oc1c(Cl)c(Cl)c(c(Cl)c1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',3,4',5,5',6-heptachlorobiphenyl REASON: CORRECT "
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "3,3',4,4',5-pentachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: COc1c(Cl)cc(Cl)cc1Cl NAME: 2,4,6-trichloroanisole '
               'REASON: CORRECT Found an isolated benzene ring with exactly '
               'three terminal chloro substituents and only small additional '
               'substituents\n'
               ' * SMILES: Oc1c(Cl)cc(Cl)c(Cl)c1-c1cc(Cl)cc(Cl)c1Cl NAME: '
               "2,2',3,3',5,5'-Hexachloro-6-biphenylol REASON: CORRECT Found "
               'an isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Oc1cc(Cl)c(Cl)cc1Cl NAME: 2,4,5-trichlorophenol '
               'REASON: CORRECT Found an isolated benzene ring with exactly '
               'three terminal chloro substituents and only small additional '
               'substituents\n'
               ' * SMILES: Clc1ccc(Cl)c(-c2ccccc2)c1Cl NAME: '
               '2,3,6-trichlorobiphenyl REASON: CORRECT Found an isolated '
               'benzene ring with exactly three terminal chloro substituents '
               'and only small additional substituents\n'
               ' * SMILES: Clc1ccc(c(Cl)c1)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "2,3',4,4',5'-Pentachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1cc(cc(Cl)c1Cl)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "3,4,5,3',4',5'-Hexachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Oc1cc(Cl)c(c(Cl)c1Cl)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "2,2'3,4',6,6'-Hexachloro-4-biphenylol REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1ccc(Cl)c(Cl)c1Cl NAME: '
               "2,3,4,3',4'-Pentachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(-c2cc(Cl)c(Cl)c(Cl)c2)c(Cl)c1Cl NAME: '
               "2,3,3',4,4',5'-Hexachlorobiphenyl REASON: CORRECT Found an "
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: Oc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',4',5,5'-pentachlorobiphenyl REASON: CORRECT "
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(cc1)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "3,4,4',5-Tetrachlorobiphenyl REASON: CORRECT Found an isolated "
               'benzene ring with exactly three terminal chloro substituents '
               'and only small additional substituents\n'
               'False positives: SMILES: C=1(C(=C(C=C(C1Cl)O)Cl)[O-])Cl NAME: '
               '2,3,6-trichloro-4-hydroxyphenolate REASON: WRONGLY CLASSIFIED '
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: ClC=1C(C=2C(Cl)=CC(Cl)=C(Cl)C2)=CC(Cl)=C(Cl)C1Cl '
               'NAME: PCB180 REASON: WRONGLY CLASSIFIED Found an isolated '
               'benzene ring with exactly three terminal chloro substituents '
               'and only small additional substituents\n'
               ' * SMILES: ClC1=C(OC)C(Cl)=CC(=C1O)Cl NAME: '
               '2,4,6-trichloro-3-methoxyphenol REASON: WRONGLY CLASSIFIED '
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: Clc1ccc(Cl)c(c1Cl)-c1c(Cl)ccc(Cl)c1Cl NAME: '
               "2,2',3,3',6,6'-hexachlorobiphenyl REASON: WRONGLY CLASSIFIED "
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: ClC1=C(Cl)C(OC)=C(O)C(=C1OC)Cl NAME: '
               '2,4,5-Trichlor-3,6-dimethoxy-phenol REASON: WRONGLY CLASSIFIED '
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: Clc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',4,4',5,5'-hexachlorobiphenyl REASON: WRONGLY CLASSIFIED "
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: CN1CCN(CC1)c1ncc(c(N)n1)-c1cc(Cl)cc(Cl)c1Cl NAME: '
               'Sipatrigine REASON: WRONGLY CLASSIFIED Found an isolated '
               'benzene ring with exactly three terminal chloro substituents '
               'and only small additional substituents\n'
               ' * SMILES: ClC1=C(C=2C(Cl)=CC(Cl)=C(Cl)C2)C=CC(Cl)=C1Cl NAME: '
               'PCB138 REASON: WRONGLY CLASSIFIED Found an isolated benzene '
               'ring with exactly three terminal chloro substituents and only '
               'small additional substituents\n'
               ' * SMILES: C1=CC(=C(C(=C1C2=NNC(=C2)C(=O)NCCO)Cl)Cl)Cl NAME: '
               'N-(2-hydroxyethyl)-3-(2,3,4-trichlorophenyl)-1H-pyrazole-5-carboxamide '
               'REASON: WRONGLY CLASSIFIED Found an isolated benzene ring with '
               'exactly three terminal chloro substituents and only small '
               'additional substituents\n'
               ' * SMILES: C=1(C(=C(C=C(C1Cl)O)Cl)O)Cl NAME: '
               '2,3,5-trichlorobenzene-1,4-diol REASON: WRONGLY CLASSIFIED '
               'Found an isolated benzene ring with exactly three terminal '
               'chloro substituents and only small additional substituents\n'
               ' * SMILES: C=1C(=C(C(=CC1Cl)Cl)[O-])Cl NAME: '
               '2,4,6-trichlorophenolate REASON: WRONGLY CLASSIFIED Found an '
               'isolated benzene ring with exactly three terminal chloro '
               'substituents and only small additional substituents\n'
               ' * SMILES: ClC1=C(Cl)C(O)=C(OC)C(=C1OC)Cl NAME: '
               '2,3,5-trichloro-4,6-dimethoxy-phenol REASON: WRONGLY '
               'CLASSIFIED Found an isolated benzene ring with exactly three '
               'terminal chloro substituents and only small additional '
               'substituents\n'
               'False negatives: SMILES: '
               'CON([C@@H](C)Cc1c(Cl)cc(Cl)cc1Cl)C(=O)c1cn(C)nc1C(F)F NAME: '
               '(S)-pydiflumetofen REASON: MISSED No isolated benzene ring '
               'with exactly three terminal chloro substituents (with '
               'acceptable small substituents) found\n'
               ' * SMILES: CCCN(CCOc1c(Cl)cc(Cl)cc1Cl)C(=O)n1ccnc1 NAME: '
               'prochloraz REASON: MISSED No isolated benzene ring with '
               'exactly three terminal chloro substituents (with acceptable '
               'small substituents) found\n'
               ' * SMILES: C1=C(C(=C(C(=C1Cl)OC)C(O)=O)Cl)Cl NAME: tricamba '
               'REASON: MISSED No isolated benzene ring with exactly three '
               'terminal chloro substituents (with acceptable small '
               'substituents) found\n'
               ' * SMILES: C1(=CC=C(C(=C1Cl)CC(O)=O)Cl)Cl NAME: chlorfenac '
               'REASON: MISSED No isolated benzene ring with exactly three '
               'terminal chloro substituents (with acceptable small '
               'substituents) found\n'
               ' * SMILES: Clc1ccc(S\\N=N\\c2cc(Cl)c(Cl)cc2Cl)cc1 NAME: '
               'Chlorfensulphide REASON: MISSED No isolated benzene ring with '
               'exactly three terminal chloro substituents (with acceptable '
               'small substituents) found\n'
               ' * SMILES: OC(=O)C1=C(Cl)C(Cl)=CC(Cl)=C1 NAME: '
               '2,3,5-trichlorobenzoic acid REASON: MISSED No isolated benzene '
               'ring with exactly three terminal chloro substituents (with '
               'acceptable small substituents) found\n'
               ' * SMILES: OC(=O)C1=CC(Cl)=C(Cl)C(Cl)=C1 NAME: '
               '3,4,5-trichlorobenzoic acid REASON: MISSED No isolated benzene '
               'ring with exactly three terminal chloro substituents (with '
               'acceptable small substituents) found\n'
               ' * SMILES: OC(=O)COc1cc(Cl)c(Cl)cc1Cl NAME: '
               '(2,4,5-trichlorophenoxy)acetic acid REASON: MISSED No isolated '
               'benzene ring with exactly three terminal chloro substituents '
               '(with acceptable small substituents) found\n'
               ' * SMILES: COP(=O)(OC)O\\C(c1cc(Cl)c(Cl)cc1Cl)=C/Cl NAME: '
               'tetrachlorvinphos REASON: MISSED No isolated benzene ring with '
               'exactly three terminal chloro substituents (with acceptable '
               'small substituents) found\n'
               ' * SMILES: Oc1c(Cl)cc(Cl)c(Cl)c1Cc1c(O)c(Cl)cc(Cl)c1Cl NAME: '
               'hexachlorophene REASON: MISSED No isolated benzene ring with '
               'exactly three terminal chloro substituents (with acceptable '
               'small substituents) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'No isolated benzene ring with '
                                               'exactly three terminal '
                                               'chlorine substituents (with '
                                               'acceptable small or aromatic '
                                               'substituents) found'}],
    'sample_false_negatives': [   {   'smiles': 'C1=C(C(=C(C(=C1Cl)OC)C(O)=O)Cl)Cl',
                                      'name': 'tricamba',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'},
                                  {   'smiles': 'C1(=CC=C(C(=C1Cl)CC(O)=O)Cl)Cl',
                                      'name': 'chlorfenac',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'},
                                  {   'smiles': 'OC(=O)C1=C(Cl)C(Cl)=CC(Cl)=C1',
                                      'name': '2,3,5-trichlorobenzoic acid',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'},
                                  {   'smiles': 'OC(=O)C1=CC(Cl)=C(Cl)C(Cl)=C1',
                                      'name': '3,4,5-trichlorobenzoic acid',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'},
                                  {   'smiles': 'OC(=O)COc1cc(Cl)c(Cl)cc1Cl',
                                      'name': '(2,4,5-trichlorophenoxy)acetic '
                                              'acid',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'},
                                  {   'smiles': 'COP(=O)(OC)O\\C(c1cc(Cl)c(Cl)cc1Cl)=C/Cl',
                                      'name': 'tetrachlorvinphos',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'},
                                  {   'smiles': 'C1=CC(=C(C(=C1Cl)C(O)=O)Cl)Cl',
                                      'name': '2,3,6-TBA',
                                      'reason': 'No isolated benzene ring with '
                                                'exactly three terminal '
                                                'chlorine substituents (with '
                                                'acceptable small or aromatic '
                                                'substituents) found'}],
    'attempt': 3,
    'reasoning': 'Below is one solution along with inline commentary on our '
                 'thought‐process improvements. In the previous attempt the '
                 'method for “measuring” a substituent’s extent was too '
                 'blunt—simply performing a DFS from the neighbor led to '
                 'disqualification when a connecting “small” fragment (that '
                 'just happens to start with an sp³ carbon) later led into an '
                 'aromatic ring. But in our definition only non‐aromatic '
                 'fragments should be “counted” and if a substituent rapidly '
                 '“hits” an aromatic group then that branch should be allowed. '
                 'Also, we want to be sure to count only terminal chlorine '
                 'substituents (the Cl must have degree=1) directly attached '
                 'to a benzene ring. Hence, the following code first finds '
                 'isolated (non‐fused) benzene rings (six-membered rings of '
                 'aromatic carbons) and then examines each substituent. For '
                 'each neighbor not in the ring, if it is a Cl with degree 1 '
                 'we count it. Otherwise we run a DFS that sums “heavy atoms” '
                 'only if no aromatic atom is reached; if an aromatic atom is '
                 'reached then we consider that substituent “small” (i.e. it '
                 'is simply a link to an extended aromatic fragment). Any '
                 'non‐chlorine substituent that is non‐aromatic but “large” '
                 '(more than 2 heavy atoms) yields disqualification of that '
                 'benzene ring. Finally, if a candidate benzene ring shows '
                 'exactly three valid terminal Cl substituents (with only '
                 '“small” additional substituents) we return True along with '
                 'an explanation; otherwise, we return False. (If necessary '
                 'for your work the threshold may be tuned.) \n'
                 '\n'
                 'Below is the complete Python solution:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 21,
    'num_true_negatives': 142239,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.6111111111111112,
    'recall': 0.825,
    'f1': 0.7021276595744681,
    'accuracy': 0.999803232607168,
    'negative_predictive_value': 0.9999507894773842}