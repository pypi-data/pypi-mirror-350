"""
Classifies: CHEBI:48024 3'-hydroxyflavanones
"""
#!/usr/bin/env python
"""
Classifies: 3'-hydroxyflavanones
Definition: Any hydroxyflavanone with a hydroxy substituent at position 3' (meta to the attachment on the B ring) of the phenyl ring.
"""

from rdkit import Chem

def is_3__hydroxyflavanones(smiles: str):
    """
    Determines if a molecule is a 3'-hydroxyflavanone based on its SMILES string.
    
    We require:
      1. A flavanone core (a 2-phenylchroman-4-one fragment).
         Here we use the simple SMARTS "C1CC(=O)c2ccccc2O1" which captures the chromanone ring.
      2. An extra aromatic ring (“B ring”) attached to the core at the substitution carbon.
      3. That aromatic ring must have a hydroxy (-OH) substituent at the meta position
         (i.e. two bonds away from the connecting carbon of the ring).
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule fits the class, False otherwise.
        str: Reason for the classification.
    """
    # Parse SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Define a SMARTS for a simplistic flavanone/chromanone core.
    # This pattern represents a 2-phenylchroman-4-one fragment.
    # The assumption is that the first atom in the match (index 0) is the chiral (or substitution) center 
    # that should be connected to the extra (B) aromatic ring.
    core_smarts = "C1CC(=O)c2ccccc2O1"
    core_query = Chem.MolFromSmarts(core_smarts)
    if core_query is None:
        return False, "Failed to create substructure query for flavanone core"
    
    core_matches = mol.GetSubstructMatches(core_query)
    if not core_matches:
        return False, "Molecule does not contain a flavanone (chromanone) core"
        
    # For this implementation, we assume that if the core is present, we can use the first match.
    core_match = core_matches[0]
    # The core SMARTS was written so that the first atom (core_match[0]) is expected to be the substitution center.
    substitution_center_idx = core_match[0]
    
    # Now, loop over neighbors of the substitution center.
    # In a flavanone, one of these neighbors (not part of the core) should be an aromatic carbon belonging to the B ring.
    atom_sub_center = mol.GetAtomWithIdx(substitution_center_idx)
    b_ring_attachment_idx = None
    for nb in atom_sub_center.GetNeighbors():
        # if this neighbor is not part of the core match then it is the attached phenyl (B) ring.
        if nb.GetIdx() not in core_match and nb.GetIsAromatic():
            b_ring_attachment_idx = nb.GetIdx()
            break
            
    if b_ring_attachment_idx is None:
        return False, "Could not find the attached aromatic (B) ring from the flavanone core"
        
    # Now we search for an aromatic ring that contains the B ring attachment atom.
    ring_info = mol.GetRingInfo()
    aromatic_rings = []
    for ring in ring_info.AtomRings():
        # We narrow to rings of size 6 (benzene rings) and all atoms aromatic.
        if len(ring) == 6:
            if b_ring_attachment_idx in ring:
                # Check that all atoms in the ring are aromatic.
                if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
                    aromatic_rings.append(ring)
                    
    if not aromatic_rings:
        return False, "No aromatic six‐membered ring (B ring) found attached to the flavanone core"
    
    # Assume that the first aromatic ring that contains the attachment atom is the B ring.
    b_ring = aromatic_rings[0]
    
    # Now, we search for a hydroxy (-OH) group on the B ring 
    # at a position meta to the attachment.
    # In benzene, "meta" means the topological distance along the ring (within the ring) is 2.
    # We use RDKit’s shortest path function to measure the distance.
    found_meta_OH = False
    for atom_idx in b_ring:
        # Skip the attachment atom itself.
        if atom_idx == b_ring_attachment_idx:
            continue
        # Compute the topological distance between the attachment atom and this atom.
        path = Chem.GetShortestPath(mol, b_ring_attachment_idx, atom_idx)
        # In a benzene ring, adjacent (ortho) means path length 1, meta means 2, para means 3.
        if len(path) - 1 == 2:  # exactly meta
            # For the candidate atom, check its neighbors for an -OH substituent.
            atom = mol.GetAtomWithIdx(atom_idx)
            for nbr in atom.GetNeighbors():
                # We want an oxygen (atomic number 8) that is attached by a single bond.
                if nbr.GetAtomicNum() == 8:
                    # Using GetTotalNumHs to check if it has an attached hydrogen (typical for an -OH group).
                    # (This excludes –O–C glycosidic linkages where the oxygen would have no hydrogen.)
                    if nbr.GetTotalNumHs() >= 1:
                        found_meta_OH = True
                        break
            if found_meta_OH:
                break
                
    if not found_meta_OH:
        return False, "No hydroxy (-OH) group found at the 3' (meta) position on the B ring"
        
    # If we passed all tests:
    return True, "Molecule contains flavanone core with a hydroxy group at the 3' position on the B ring"

# For testing purposes – you could run:
if __name__ == "__main__":
    # Example: (2S)-3'-hydroxyflavanone
    smiles_example = "Oc1cccc(c1)[C@@H]1CC(=O)c2ccccc2O1"
    result, reason = is_3__hydroxyflavanones(smiles_example)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:48024',
                          'name': "3'-hydroxyflavanones",
                          'definition': 'Any hydroxyflavanone with a hydroxy '
                                        "substituent at position 3' of the "
                                        'phenyl ring.',
                          'parents': ['CHEBI:24697'],
                          'xrefs': ['MetaCyc:3-Hydroxy-Flavanones'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 91,
                           'log_lines_of_code': 4.51085950651685,
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
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
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
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 2,
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
                           'methods_called': [   'GetTotalNumHs',
                                                 'GetIdx',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'MolFromSmarts',
                                                 'GetShortestPath',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 13,
                           'smarts_strings': ['core_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_3__hydroxyflavanones(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Failed to create '
                                          'substructure query for flavanone '
                                          'core"',
                                          'False, "Molecule does not contain a '
                                          'flavanone (chromanone) core"',
                                          'False, "Could not find the attached '
                                          'aromatic (B) ring from the '
                                          'flavanone core"',
                                          'False, "No aromatic six‐membered '
                                          'ring (B ring) found attached to the '
                                          'flavanone core"',
                                          'False, "No hydroxy (-OH) group '
                                          "found at the 3' (meta) position on "
                                          'the B ring"',
                                          'True, "Molecule contains flavanone '
                                          "core with a hydroxy group at the 3' "
                                          'position on the B ring"'],
                           'returns_count': 7,
                           'complexity': 6.30217190130337},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Molecule does not contain a '
                                               'flavanone (chromanone) core'}],
    'sample_false_negatives': [],
    'attempt': 0,
    'reasoning': 'We can solve this problem in two major steps. First, we '
                 '“recognize” a flavanone – that is, a molecule having the '
                 '2‐phenylchroman-4‐one (or chromanone) core. In our '
                 'implementation we use a simple SMARTS (without '
                 'stereochemistry) to “flag” a flavanone. Next (for '
                 'flavanones) we identify the phenyl (B) ring attached to the '
                 'carbon that “connects” the chromanone core with the extra '
                 'aromatic ring. Then we search that aromatic ring for a –OH '
                 'group (an oxygen bound to a hydrogen) located at a “meta” '
                 'position relative to the linking atom (i.e. a topological '
                 'distance of 2 in the benzene ring). (Recall that in a '
                 'benzene ring the positions relative to the substituent are '
                 'defined as ortho: distance 1, meta: distance 2, para: '
                 'distance 3.) \n'
                 '\n'
                 'Below is the complete Python code (all in one code block) '
                 'that implements this logic. (Note that due to the inherent '
                 'complexity of substructure detection and possible structural '
                 'variation, some molecules may be borderline according to our '
                 '“simple” SMARTS filter or our ring‐analysis. In such cases '
                 'the function will return (False, “…”) as a reason if our '
                 'criteria are not met.)\n'
                 '\n'
                 'Below is the complete code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 32,
    'num_false_positives': 102,
    'num_true_negatives': 142166,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.23880597014925373,
    'recall': 1.0,
    'f1': 0.38554216867469876,
    'accuracy': 0.9992832044975404,
    'negative_predictive_value': 1.0}