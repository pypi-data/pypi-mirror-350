"""
Classifies: CHEBI:25448 myo-inositol phosphate
"""
#!/usr/bin/env python
"""
Classifies: myo-inositol phosphate – an inositol phosphate in which the inositol component 
has myo-configuration.

This heuristic checks for:
  1. A valid molecule that is neutral (formal charge = 0).
  2. At least one six‐membered ring in which every ring atom:
       • Is carbon.
       • Has an explicitly assigned chiral configuration.
       • Carries at least one non‐ring substituent.
  3. For each ring atom, at least one substituent must be an oxygen branch whose atoms 
     (found via a short breadth‐first search) are limited to oxygen and phosphorus – and 
     importantly each such atom must be uncharged.
  4. At least one oxygen branch on the ring eventually contains a phosphorus atom.
  
These criteria are intended to capture a neutral myo–inositol phosphate core (as illustrated 
by the provided examples) while filtering out overly ionized (or extended lipid‐like) species.
"""

from rdkit import Chem

def is_myo_inositol_phosphate(smiles: str):
    """
    Determines whether a given molecule is a myo-inositol phosphate based on its SMILES string.
    
    The heuristic requires that:
      - The molecule parses correctly and carries zero net formal charge.
      - There is at least one six‐membered ring in which every atom is carbon with explicitly 
        assigned chirality.
      - Every ring carbon has at least one substituent (atom not in the ring) that is oxygen.
      - For each such oxygen substituent, a short breadth‐first search confirms that the branch 
        contains only oxygen and phosphorus atoms (each with formal charge 0) and that at least one branch 
        contains phosphorus.
    
    Args:
        smiles (str): SMILES representation of the molecule.
    
    Returns:
        (bool, str): Tuple where the boolean indicates correct classification and the string 
                     provides an explanation.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Enforce neutrality: reject molecules with non-zero overall formal charge.
    if Chem.GetFormalCharge(mol) != 0:
        return False, "Molecule carries non-zero formal charge; likely a deprotonated ionized form."
    
    # Ensure that stereochemistry is assigned.
    Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # Get ring information from the molecule.
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if not rings:
        return False, "No ring system found in the molecule"
    
    # In substituent branches we allow only oxygen (atomic number 8) and phosphorus (15),
    # but we require that these atoms be uncharged.
    allowed_atoms = {8, 15}
    
    # Loop over all rings; look for a six-membered ring meeting our criteria.
    for ring in rings:
        if len(ring) != 6:
            continue  # only consider six-membered rings
        
        valid_ring = True
        branch_has_phosphorus = False
        
        # Process each atom in the ring:
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # The ring atom must be carbon.
            if atom.GetAtomicNum() != 6:
                valid_ring = False
                break
            # The carbon must have its chiral tag explicitly assigned.
            if atom.GetChiralTag() == Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
                valid_ring = False
                break
            
            # Identify non‐ring neighbors as possible substituents.
            non_ring_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetIdx() not in ring]
            if not non_ring_neighbors:
                valid_ring = False
                break
            
            oxygen_found = False
            # Examine each substituent branch.
            for nbr in non_ring_neighbors:
                # We require that the immediate neighbor be an oxygen.
                if nbr.GetAtomicNum() != 8:
                    continue  # if not oxygen, skip it
                
                # Do a BFS on this branch (starting at the oxygen) to ensure that all atoms 
                # are either oxygen or phosphorus AND that they all carry formal charge 0.
                branch_valid = True
                queue = [nbr.GetIdx()]
                visited = set()
                branch_contains_P = False
                while queue:
                    current_idx = queue.pop(0)
                    if current_idx in visited:
                        continue
                    visited.add(current_idx)
                    current_atom = mol.GetAtomWithIdx(current_idx)
                    # Check that the atom type is allowed.
                    if current_atom.GetAtomicNum() not in allowed_atoms:
                        branch_valid = False
                        break
                    # Reject atoms that are not neutrally charged.
                    if current_atom.GetFormalCharge() != 0:
                        branch_valid = False
                        break
                    if current_atom.GetAtomicNum() == 15:
                        branch_contains_P = True
                    # Traverse neighbors that are not in the ring.
                    for nb in current_atom.GetNeighbors():
                        if nb.GetIdx() in ring:
                            continue
                        if nb.GetIdx() not in visited:
                            queue.append(nb.GetIdx())
                if not branch_valid:
                    continue  # try the next substituent branch
                # Accept this branch for the ring atom.
                oxygen_found = True
                if branch_contains_P:
                    branch_has_phosphorus = True
            if not oxygen_found:
                valid_ring = False
                break
        
        # We require at least one substituent branch on the ring to eventually contain phosphorus.
        if valid_ring and branch_has_phosphorus:
            return True, ("Found six‐membered ring of chiral carbons with substituents that are limited "
                          "to uncharged oxygen/phosphorus atoms and at least one branch bearing a phosphate, "
                          "consistent with myo-inositol phosphate.")
    
    # If no ring passes the criteria return false.
    return False, "No six‐membered inositol-like ring with appropriate chiral centers, oxygen branches, and a phosphate attachment was found."

# Example usage (for testing purposes):
if __name__ == "__main__":
    test_smiles = [
        # 1D-myo-inositol 1,2,3,4,5-pentakisphosphate (neutral)
        "O[C@H]1[C@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(O)=O",
        # 1D-myo-inositol 4-phosphate (neutral)
        "O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O",
        # A known false positive; note the deprotonated phosphate groups:
        "[O-]P([O-])(=O)O[C@@H]1[C@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)"
        " [C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@H]1OP([O-])([O-])=O"
    ]
    for smi in test_smiles:
        result, reason = is_myo_inositol_phosphate(smi)
        print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25448',
                          'name': 'myo-inositol phosphate',
                          'definition': 'An inositol phosphate in which the '
                                        'inositol component has '
                                        'myo-configuration.',
                          'parents': ['CHEBI:24846'],
                          'xrefs': ['PMID:1694860'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 117,
                           'log_lines_of_code': 4.762173934797756,
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
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 6,
                                                 7,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
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
                           'max_indent': 7,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'append',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'pop',
                                                 'GetChiralTag',
                                                 'GetNeighbors',
                                                 'add',
                                                 'GetRingInfo',
                                                 'AssignStereochemistry',
                                                 'GetFormalCharge'],
                           'methods_called_count': 13,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_myo_inositol_phosphate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule carries non-zero '
                                          'formal charge; likely a '
                                          'deprotonated ionized form."',
                                          'False, "No ring system found in the '
                                          'molecule"',
                                          'True, ("Found six‐membered ring of '
                                          'chiral carbons with substituents '
                                          'that are limited "',
                                          'False, "No six‐membered '
                                          'inositol-like ring with appropriate '
                                          'chiral centers, oxygen branches, '
                                          'and a phosphate attachment was '
                                          'found."'],
                           'returns_count': 5,
                           'complexity': 6.152434786959551},
    'message': '\n'
               'Attempt failed: F1 score of 0.7096774193548387 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O[C@H]1[C@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(O)=O '
               'NAME: 1D-myo-inositol 1,2,3,4,5-pentakisphosphate REASON: '
               'CORRECT Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O '
               'NAME: 1D-myo-inositol 4-phosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: 1-diphospho-1D-myo-inositol 3,4,5,6-tetrakisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'OP(O)(=O)O[C@@H]1[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(=O)OP(O)(=O)OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(O)=O '
               'NAME: 5-triphospho-1D-myo-inositol 1,2,3,4,6-pentakisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H](O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(O)=O '
               'NAME: myo-inositol 1,3,4,6-tetrakisphosphate REASON: CORRECT '
               'Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](OP(O)(=O)OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: 1,3-bis(diphospho)-myo-inositol 4,5,6-trisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O '
               'NAME: 1D-myo-inositol 3,5-bisphosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1OP(O)(O)=O '
               'NAME: 1D-myo-inositol 3,4,5,6-tetrakisphosphate REASON: '
               'CORRECT Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@@H](O)[C@@H](OP(O)(O)=O)[C@@H]1O '
               'NAME: myo-inositol 1,3-bisphosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(=O)OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: 1,5-bis(diphospho)-1D-myo-inositol 3,4,6-trisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O '
               'NAME: 1D-myo-inositol 4,5-bisphosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H](O)[C@@H]1O '
               'NAME: 1D-myo-inositol 1-phosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H]1OP(O)(O)=O '
               'NAME: 1D-myo-inositol 1,2,3,5,6-pentakisphosphate REASON: '
               'CORRECT Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@@H](O)[C@@H]1OP(O)(O)=O '
               'NAME: 1D-myo-inositol 1,4-bisphosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: 3-diphospho-1D-myo-inositol 1,4,5,6-tetrakisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'OP(O)(=O)O[C@@H]1[C@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(=O)OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1OP(O)(O)=O '
               'NAME: 4-diphospho-1D-myo-inositol pentakisphosphate REASON: '
               'CORRECT Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(OP(=O)(O)O)[C@@H](OP(=O)(O)OP(O)(O)=O)[C@H](OP(=O)(O)O)[C@@H](OP(=O)(O)OP(O)(O)=O)[C@@H](OP(=O)(O)O)[C@H]1OP(=O)(O)O '
               'NAME: 3,5-bis(diphospho)-1D-myo-inositol '
               '1,2,4,6-tetrakisphosphate REASON: CORRECT Found six-membered '
               'ring of chiral carbons with oxygen substituents (only O/P '
               'allowed) and at least one branch with a phosphate attachment, '
               'consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](O)[C@@H]1OP(O)(O)=O '
               'NAME: 1D-myo-inositol 1,4,5-trisphosphate REASON: CORRECT '
               'Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](OP(O)(O)=O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1OP(O)(O)=O '
               'NAME: 1D-myo-inositol 1,3,4,5-tetrakisphosphate REASON: '
               'CORRECT Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(=O)OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: 3,5-bis(diphospho)-1D-myo-inositol 1,4,6-trisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(=O)OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@@H]1OP(O)(O)=O '
               'NAME: 5-diphospho-myo-inositol 1,3,4,6-tetrakisphosphate '
               'REASON: CORRECT Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'OP(O)(=O)O[C@@H]1[C@@H](OP(O)(O)=O)[C@H](OP(O)(=O)OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(=O)OP(O)(O)=O)[C@@H]1OP(O)(O)=O '
               'NAME: 1,5-bis(diphospho)-1D-myo-inositol '
               '2,3,4,6-tetrakisphosphate REASON: CORRECT Found six-membered '
               'ring of chiral carbons with oxygen substituents (only O/P '
               'allowed) and at least one branch with a phosphate attachment, '
               'consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               '[C@H]1(OP(=O)(O)O)[C@H](OP(O)(=O)O)[C@@H](OP(O)(=O)O)[C@@H]([C@H]([C@H]1OP(O)(=O)O)O)O '
               'NAME: 1D-myo-inositol 1,2,5,6-tetrakisphosphate REASON: '
               'CORRECT Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](OP(O)(O)=O)[C@H](O)[C@H](OP(O)(O)=O)[C@@H](O)[C@@H]1OP(O)(O)=O '
               'NAME: myo-inositol 1,3,5-trisphosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@@H]1O '
               'NAME: 1D-myo-inositol 6-phosphate REASON: CORRECT Found '
               'six-membered ring of chiral carbons with oxygen substituents '
               '(only O/P allowed) and at least one branch with a phosphate '
               'attachment, consistent with myo-inositol phosphate.\n'
               'False positives: SMILES: '
               '[O-]P([O-])(=O)O[C@@H]1[C@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@H]1OP([O-])([O-])=O '
               'NAME: myo-inositol hexakisphosphate(12-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(OP(=O)([O-])[O-])[C@@H](OP(=O)([O-])OP([O-])([O-])=O)[C@H](OP(=O)([O-])[O-])[C@@H](OP(=O)([O-])OP([O-])(O)=O)[C@@H](OP(=O)([O-])[O-])[C@H]1OP(=O)([O-])[O-] '
               'NAME: 3,5-bis(diphospho)-1D-myo-inositol '
               '1,2,4,6-tetrakisphosphate(13-) REASON: WRONGLY CLASSIFIED '
               'Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@@H]1OP([O-])([O-])=O '
               'NAME: 1D-myo-inositol 1,2,4,5,6-pentakisphosphate(10-) REASON: '
               'WRONGLY CLASSIFIED Found six-membered ring of chiral carbons '
               'with oxygen substituents (only O/P allowed) and at least one '
               'branch with a phosphate attachment, consistent with '
               'myo-inositol phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(OP(=O)([O-])[O-])[C@@H](O)[C@@H]([C@H]([C@H]([C@H]1OP([O-])(=O)[O-])OP(=O)([O-])[O-])O)O '
               'NAME: 1D-myo-inositol 1,2,6-trisphosphate(6-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(O)[C@@H](OP(=O)([O-])[O-])[C@@H]([C@H]([C@H]([C@H]1O)O)O)OP(=O)([O-])[O-] '
               'NAME: 1D-myo-inositol 4,5-bisphosphate(4-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'P(O[C@@H]1[C@@H](OP(O)(O)=O)[C@H](O)[C@H](O)[C@H](OP(O)(O)=O)[C@H]1O)(O)(O)=O '
               'NAME: L-myo-inositol-1,4,5-triphosphate REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@H]1O '
               'NAME: 1D-myo-inositol 4-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@@H](O)[C@@H](OP([O-])([O-])=O)[C@@H]1OP([O-])([O-])=O '
               'NAME: myo-inositol 1,3,4,6-tetrakisphosphate(8-) REASON: '
               'WRONGLY CLASSIFIED Found six-membered ring of chiral carbons '
               'with oxygen substituents (only O/P allowed) and at least one '
               'branch with a phosphate attachment, consistent with '
               'myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@@H]1OP([O-])([O-])=O '
               'NAME: 1D-myo-inositol 1,2,3,5,6-pentakisphosphate(10-) REASON: '
               'WRONGLY CLASSIFIED Found six-membered ring of chiral carbons '
               'with oxygen substituents (only O/P allowed) and at least one '
               'branch with a phosphate attachment, consistent with '
               'myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@@H](O)[C@H]2OP(O)(=O)O[C@H]2[C@@H]1O NAME: '
               '1D-myo-inositol 1,2-cyclic phosphate REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H]1O '
               'NAME: 1D-myo-inositol 3,4-biphosphate(4-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(O)[C@@H](O)[C@@H]([C@H]([C@H]([C@H]1OP([O-])(=O)[O-])OP(=O)([O-])[O-])O)O '
               'NAME: 1D-myo-inositol 1,2-bisphosphate(4-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(O)[C@@H](O)[C@@H]([C@H]([C@H]([C@H]1O)OP(=O)([O-])[O-])OP(=O)([O-])[O-])O '
               'NAME: 1D-myo-inositol 2,3-bisphosphate(4-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@@H]1(O)[C@@H](O)[C@@H]([C@H]([C@H]([C@H]1OP([O-])(=O)[O-])OP(=O)([O-])[O-])OP(=O)([O-])[O-])O '
               'NAME: 1D-myo-inositol 1,2,3-trisphosphate(6-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@@H]1OP([O-])([O-])=O '
               'NAME: 1L-myo-inositol 1,2,3,4,6-pentakisphosphate(10-) REASON: '
               'WRONGLY CLASSIFIED Found six-membered ring of chiral carbons '
               'with oxygen substituents (only O/P allowed) and at least one '
               'branch with a phosphate attachment, consistent with '
               'myo-inositol phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@@H](O)[C@@H]1OP([O-])([O-])=O '
               'NAME: 1D-myo-inositol 1,4,5-trisphosphate(6-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@@H](O)[C@H]2OP([O-])(=O)O[C@H]2[C@@H]1O '
               'NAME: 1D-myo-inositol 1,2-cyclic phosphate(1-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@H]1OP([O-])([O-])=O '
               'NAME: 1D-myo-inositol 3,4,5,6-tetrakisphosphate(8-) REASON: '
               'WRONGLY CLASSIFIED Found six-membered ring of chiral carbons '
               'with oxygen substituents (only O/P allowed) and at least one '
               'branch with a phosphate attachment, consistent with '
               'myo-inositol phosphate.\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)OP([O-])(=O)[O-])OP(=O)([O-])[O-])O)O)OP(=O)([O-])[O-] '
               'NAME: 1D-myo-inositol 3,4,6-trisphosphate(6-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@@H]1O '
               'NAME: 1D-myo-inositol 6-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@H](O)[C@@H]1O '
               'NAME: 1D-myo-inositol 1-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@H]1([C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)OP(=O)([O-])[O-])OP(=O)([O-])[O-])OP([O-])(=O)[O-])OP(=O)([O-])[O-])O '
               'NAME: 1D-myo-inositol 2,3,4,5-tetrakisphosphate(8-) REASON: '
               'WRONGLY CLASSIFIED Found six-membered ring of chiral carbons '
               'with oxygen substituents (only O/P allowed) and at least one '
               'branch with a phosphate attachment, consistent with '
               'myo-inositol phosphate.\n'
               ' * SMILES: '
               '[C@H]1([C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)OP(=O)([O-])[O-])O)O)OP(=O)([O-])[O-])O '
               'NAME: 1D-myo-inositol 2,5-bisphosphate(4-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H]([C@@H]1O)OP(=O)([O-])[O-])O)O)O)O '
               'NAME: scyllo-inositol 1-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Found six-membered ring of chiral carbons with '
               'oxygen substituents (only O/P allowed) and at least one branch '
               'with a phosphate attachment, consistent with myo-inositol '
               'phosphate.\n'
               ' * SMILES: '
               '[C@H]1(OP([O-])(OP([O-])(=O)[O-])=O)[C@@H](OP([O-])(=O)[O-])[C@@H](OP([O-])(=O)[O-])[C@@H]([C@H]([C@@H]1OP([O-])(=O)[O-])OP(=O)([O-])[O-])O '
               'NAME: 3-diphospho-1D-myo-inositol '
               '1,2,4,5-tetrakisphosphate(11-) REASON: WRONGLY CLASSIFIED '
               'Found six-membered ring of chiral carbons with oxygen '
               'substituents (only O/P allowed) and at least one branch with a '
               'phosphate attachment, consistent with myo-inositol phosphate.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No six‐membered inositol-like '
                                               'ring with appropriate chiral '
                                               'centers, oxygen branches, and '
                                               'a phosphate attachment was '
                                               'found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule carries non-zero '
                                               'formal charge; likely a '
                                               'deprotonated ionized form.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No six‐membered inositol-like '
                                               'ring with appropriate chiral '
                                               'centers, oxygen branches, and '
                                               'a phosphate attachment was '
                                               'found.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No ring system found in the '
                                               'molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No six‐membered inositol-like '
                                               'ring with appropriate chiral '
                                               'centers, oxygen branches, and '
                                               'a phosphate attachment was '
                                               'found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No six‐membered inositol-like '
                                               'ring with appropriate chiral '
                                               'centers, oxygen branches, and '
                                               'a phosphate attachment was '
                                               'found.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No six‐membered inositol-like '
                                               'ring with appropriate chiral '
                                               'centers, oxygen branches, and '
                                               'a phosphate attachment was '
                                               'found.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No six‐membered inositol-like '
                                               'ring with appropriate chiral '
                                               'centers, oxygen branches, and '
                                               'a phosphate attachment was '
                                               'found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No ring system found in the '
                                               'molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No ring system found in the '
                                               'molecule'}],
    'sample_false_negatives': [   {   'smiles': '[C@@H]1(O)[C@H](OP([O-])(=O)[O-])[C@H]([C@H](OP(OP([O-])(=O)[O-])(=O)[O-])[C@H]([C@@H]1OP(=O)([O-])[O-])OP([O-])(=O)[O-])OP([O-])(=O)[O-]',
                                      'name': '5-diphospho-1D-myo-inositol '
                                              '1,3,4,6-tetrakisphosphate(11-)',
                                      'reason': 'Molecule carries non-zero '
                                                'formal charge; likely a '
                                                'deprotonated ionized form.'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'We observed that our previous heuristic was “too lenient” '
                 'because many deprotonated (ionized) variants ended up being '
                 'flagged as myo‐inositol phosphates. In many false‐positive '
                 'cases the molecule carries formal charges (typically on '
                 'oxygen atoms in phosphate groups) even though the neutral '
                 'form is what we want to capture. Also, some substituted '
                 'rings with extra carbon connectivity were mistakenly '
                 'accepted. To improve our approach we therefore make two key '
                 'changes:\n'
                 '  \n'
                 '1. We insist that the overall molecule has zero formal '
                 'charge so that ionized versions (for example, '
                 'multi‐deprotonated forms) get rejected.\n'
                 '  \n'
                 '2. In the branch search we tighten the allowed atom check. '
                 'In each oxygen branch our allowed atoms are oxygen and '
                 'phosphorus—but we now require that any oxygen (and '
                 'phosphorus) be uncharged. This restricts the search to '
                 '“neutral” substituents that follow the typical phosphate (or '
                 'hydroxyl) pattern.\n'
                 '\n'
                 'We then search for a six‐membered ring in which every ring '
                 'atom is a chiral carbon that bears at least one substituent '
                 'not in the ring. For these substituents we do a '
                 'breadth‐first search (limited to a small neighborhood) that '
                 'requires that every atom in the branch be either an oxygen '
                 '(with formal charge zero) or phosphorus (with formal charge '
                 'zero) and we mark the branch as “phosphorylated” if we find '
                 'phosphorus along the way. Finally, we require that at least '
                 'one of the substituent branches (from any ring carbon) '
                 'contains phosphorus.\n'
                 '\n'
                 'Below is the complete Python code implementing these '
                 'improvements.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 43,
    'num_false_positives': 3,
    'num_true_negatives': 142253,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.9347826086956522,
    'recall': 0.9772727272727273,
    'f1': 0.9555555555555557,
    'accuracy': 0.9999718903724526,
    'negative_predictive_value': 0.999992970320694}