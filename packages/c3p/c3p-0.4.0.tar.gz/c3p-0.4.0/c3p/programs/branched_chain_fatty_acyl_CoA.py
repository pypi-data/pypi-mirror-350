"""
Classifies: CHEBI:61912 branched-chain fatty acyl-CoA
"""
"""
Classifies: branched-chain fatty acyl-CoA

A branched-chain fatty acyl-CoA is defined as a fatty acyl-CoA where the fatty acyl moiety
contains at least one branch (i.e. a substituent off the "main" chain). We look for:
  (i) a thioester linkage – indicated by a carbonyl bonded to sulfur ([#6](=O)S),
  (ii) a CoA substructure (using an approximate SMARTS match), and
  (iii) branching in the fatty acyl fragment.
  
It is important that we only traverse carbon atoms to extract the acyl fragment and that we
reject molecules in non‐standard protonation states (as indicated by "[O-]" tokens in the SMILES).
Branching is determined by looking at the induced subgraph of the acyl chain – in a linear chain,
each carbon (except terminals) has exactly two carbon neighbors. An atom with more than two neighbors
(in the subgraph) is evidence of branching.
"""

from rdkit import Chem

def is_branched_chain_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a branched-chain fatty acyl-CoA based on its SMILES string.
    
    Steps:
      1. Reject SMILES that show deprotonated groups (e.g. “[O-]”),
         to avoid misclassification due to non-standard protonation.
      2. Check for a CoA substructure (using an approximate SMARTS).
      3. Identify a thioester group via the SMARTS "[#6](=O)S".
      4. For each thioester, extract the fatty acyl fragment:
            a. Identify the acyl root: the carbon (atomic number 6) bonded to the carbonyl
               (while ignoring bonds to the oxygen and sulfur in the thioester).
            b. Traverse only to carbon neighbors (via a DFS) to collect the candidate acyl fragment.
            c. Reject the candidate if any part of the fragment is in a ring.
      5. In the induced subgraph (only carbons) of the acyl fragment, check every atom’s degree.
         In a linear chain, internal carbons have degree 2 and terminal carbons degree 1.
         If any atom has a degree >2, a branch is present.
      6. If any thioester candidate yields a branched fatty acyl fragment, return True with details;
         otherwise, return False.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is a branched-chain fatty acyl-CoA, False otherwise.
        str: Reason for classification.
    """
    # Reject molecules with explicit deprotonation markers to avoid non-standard forms.
    if "[O-]" in smiles:
        return False, "Molecule appears deprotonated ([O-] present); expected neutral CoA form."
    
    # Parse the molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for a CoA motif. This SMARTS is an approximate match to a fragment of Coenzyme A.
    # (This pattern may be refined further if needed.)
    coa_pattern = Chem.MolFromSmarts("SCCNC(=O)CCNC(=O)")
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "CoA moiety not found"
    
    # Identify a thioester group: a carbonyl carbon connected to a sulfur.
    thioester_pattern = Chem.MolFromSmarts("[#6](=O)S")
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if not thioester_matches:
        return False, "No thioester group (acyl-CoA linkage) found."
    
    # Helper to extract the acyl fragment (set of carbon atom indices) from a starting acyl root.
    # We do a DFS that only follows bonds to carbons.
    def get_acyl_fragment(root_idx, carbonyl_idx):
        visited = set()
        frontier = [root_idx]
        while frontier:
            curr = frontier.pop()
            if curr in visited:
                continue
            visited.add(curr)
            atom = mol.GetAtomWithIdx(curr)
            for nbr in atom.GetNeighbors():
                nbr_idx = nbr.GetIdx()
                # Do not go back to the carbonyl carbon
                if nbr_idx == carbonyl_idx:
                    continue
                # Only traverse carbon atoms
                if nbr.GetAtomicNum() == 6 and nbr_idx not in visited:
                    frontier.append(nbr_idx)
        return visited

    # Helper to check for branching in the acyl fragment.
    # In the induced subgraph, count the number of neighbors (within the fragment) for each atom.
    def is_fragment_branched(fragment_indices):
        for idx in fragment_indices:
            atom = mol.GetAtomWithIdx(idx)
            # Count neighbors that are also in the fragment.
            nbrs_in_fragment = [nbr.GetIdx() for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() == 6 and nbr.GetIdx() in fragment_indices]
            # In a linear chain, an internal carbon has exactly 2 carbon neighbors whereas a terminal has 1.
            # Any count >2 indicates branching.
            if len(nbrs_in_fragment) > 2:
                return True
        return False
    
    # For each thioester match, check if its acyl fragment is branched.
    for match in thioester_matches:
        # In the SMARTS "[#6](=O)S", match[0] is the carbonyl carbon,
        # match[1] is the oxygen, and match[2] is the sulfur.
        carbonyl_idx = match[0]
        sulfur_idx = match[2]
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
        
        # Find the acyl root from the carbonyl: choose a carbon neighbor that is not the oxygen or sulfur.
        acyl_root = None
        for nbr in carbonyl_atom.GetNeighbors():
            nbr_idx = nbr.GetIdx()
            if nbr_idx in (match[1], sulfur_idx):
                continue
            if nbr.GetAtomicNum() == 6:
                acyl_root = nbr_idx
                break
        if acyl_root is None:
            continue  # try next thioester match
        
        # Extract the acyl fragment from the acyl root (excluding the carbonyl carbon)
        fragment = get_acyl_fragment(acyl_root, carbonyl_idx)
        if len(fragment) < 2:
            continue  # too short to judge
        
        # Ensure that every atom in the fragment is acyclic (i.e. not in any ring)
        if any(mol.GetAtomWithIdx(idx).IsInRing() for idx in fragment):
            continue  # fragment not suitable
        
        # Check for branching in the fragment:
        # Using the induced subgraph method: if any atom’s number of carbon neighbors (within fragment) >2,
        # then we classify as branched.
        if is_fragment_branched(fragment):
            explanation = "Contains a thioester-linked fatty acyl chain with a branch and a CoA moiety. " \
                          "Branching detected in the acyl fragment."
            return True, explanation
        
        # If no branching was found within the fragment, we do not count this thioester candidate.
    return False, "No branched acyl chain detected in any thioester candidate"


# Example usage:
if __name__ == "__main__":
    # Example: 2-methylbutanoyl-CoA should be classified as branched.
    example_smiles = "CCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12"
    result, reason = is_branched_chain_fatty_acyl_CoA(example_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61912',
                          'name': 'branched-chain fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA that results from '
                                        'the formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any branched-chain fatty '
                                        'acid.',
                          'parents': ['CHEBI:37554'],
                          'xrefs': [   'PMID:16768463',
                                       'PMID:1761563',
                                       'PMID:9553048'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 110,
                           'log_lines_of_code': 4.700480365792417,
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
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetNeighbors',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'IsInRing',
                                                 'add',
                                                 'GetIdx',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'pop',
                                                 'append',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles'],
                           'methods_called_count': 12,
                           'smarts_strings': ['[#6](=O)S', 'SCCNC(=O)CCNC(=O)'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_branched_chain_fatty_acyl_CoA(smiles: '
                                       'str):',
                                       'get_acyl_fragment(root_idx, '
                                       'carbonyl_idx):',
                                       'is_fragment_branched(fragment_indices):'],
                           'defs_count': 3,
                           'returns': [   'False, "Molecule appears '
                                          'deprotonated ([O-] present); '
                                          'expected neutral CoA form."',
                                          'False, "Invalid SMILES string"',
                                          'False, "CoA moiety not found"',
                                          'False, "No thioester group '
                                          '(acyl-CoA linkage) found."',
                                          'visited',
                                          'True',
                                          'False',
                                          'True, explanation',
                                          'False, "No branched acyl chain '
                                          'detected in any thioester '
                                          'candidate"'],
                           'returns_count': 9,
                           'complexity': 6.740096073158483},
    'message': '\n'
               'Attempt failed: F1 score of 0.4072398190045249 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-methylbutanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               'CCCCCCCCCCCC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-2-methylpentadec-2-enoyl-CoA REASON: CORRECT '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(C)(C)C)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: pivaloyl-CoA REASON: CORRECT Contains a thioester-linked '
               'fatty acyl chain with a branch and a CoA moiety. Contains a '
               'branched acyl chain (extra carbon neighbor at acyl root).\n'
               ' * SMILES: '
               'CC(C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N '
               'NAME: isovaleryl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCC(C)C)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: 4-methylpentanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(=O)CC[C@H](CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(C)=C '
               'NAME: (3R)-3-isopropenyl-6-oxoheptanoyl-CoA REASON: CORRECT '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'C(C(CCCCCC)C)(C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O)O '
               'NAME: 2-hydroxy-3-methylnonanoyl-CoA REASON: CORRECT Contains '
               'a thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(=C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-methylbut-3-enoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CCCCCCCCCCCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2S)-2-methyltetradecanoyl-CoA REASON: CORRECT Contains '
               'a thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               'CC(C)CCCC(C)CCCC(C)CCCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: pristanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: isotridecanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxoisooctadecanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC([C@H](CC)C)=O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (S)-2-methylbutanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               'CCCCCCCCC(C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-methylundecanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'C(C(CCCCCCCCC)C)C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O '
               'NAME: 3-methyldodecanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCC(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-hydroxyisopentadecanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxoisoheptadecanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-isopentadec-2-enoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-isoheptadec-2-enoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2S)-2,6-dimethylheptanoyl-CoA REASON: CORRECT Contains '
               'a thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               'CC(C)C[C@@H](O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (R)-2-hydroxy-4-methylpentanoyl-CoA REASON: CORRECT '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: isobutyryl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               'C[C@H](O)[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2S,3S)-3-hydroxy-2-methylbutanoyl-CoA REASON: CORRECT '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'CC(C)C=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 4-methylpent-2-enoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxopristanoyl-CoA REASON: CORRECT Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               'False positives: SMILES: '
               'CC(C)CCCC(C)CCCC(C)CCCC(C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: phytanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CCCCCC(C)C)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 7-methyloctanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCC(C)CCCC(C)CCC[C@@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (2R)-pristanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'CC=C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-methylbut-2-enoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'C[C@@H]([C@@H](O)C([O-])=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: L-erythro-3-methylmalyl-CoA(5-) REASON: WRONGLY '
               'CLASSIFIED Contains a thioester-linked fatty acyl chain with a '
               'branch and a CoA moiety. Contains a branched acyl chain (extra '
               'carbon neighbor at acyl root).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(C(CCCCCCCCCCCCCCCC)C)=O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 2-methylstearoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'C\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N '
               'NAME: trans-3-methylglutaconyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: isoheptadecanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC([C@@H](CC)C)=O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: (R)-2-methylbutanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'CCCCCCCCCCCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (2S)-2-methyltetradecanoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Contains a thioester-linked fatty acyl chain with a '
               'branch and a CoA moiety. Contains a branched acyl chain (extra '
               'carbon neighbor at acyl root).\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-isopentadec-2-enoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Contains a thioester-linked fatty acyl chain with a '
               'branch and a CoA moiety. Contains a branched acyl chain (total '
               'carbons exceed longest chain length).\n'
               ' * SMILES: '
               'C[C@@H]([C@@H](O)C(O)=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: L-erythro-3-methylmalyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'C\\C(=C/C([O-])=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: mesaconyl-CoA(5-) REASON: WRONGLY CLASSIFIED Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(C(C)C)O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 2-hydroxyisovaleryl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-methylpalmitoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CC(C)=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-methylbut-2-enoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'S(C(=O)CC(/C=C/CC(/C=C/C(C(O)CC(O)CC(=C)CC)C)=C)=C)CCNC(=O)CCNC(=O)C(O)C(CO)(C)C '
               'NAME: Cuniculene 6B REASON: WRONGLY CLASSIFIED Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'C(C(CCCCCC)C)(C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O)=O)O '
               'NAME: 2-hydroxy-3-methylnonanoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Contains a thioester-linked fatty acyl chain with a '
               'branch and a CoA moiety. Contains a branched acyl chain (total '
               'carbons exceed longest chain length).\n'
               ' * SMILES: '
               'CC(C(C)=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-methylacetoacetyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (extra carbon '
               'neighbor at acyl root).\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(C)C(O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-hydroxy-3-methylhexadecanoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Contains a thioester-linked fatty acyl chain with a '
               'branch and a CoA moiety. Contains a branched acyl chain (total '
               'carbons exceed longest chain length).\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-methyl-3-oxopalmitoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Contains a thioester-linked fatty acyl chain with a '
               'branch and a CoA moiety. Contains a branched acyl chain (extra '
               'carbon neighbor at acyl root).\n'
               ' * SMILES: '
               'CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(C)(O)C([O-])=O '
               'NAME: citramalyl-CoA(5-) REASON: WRONGLY CLASSIFIED Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (total carbons exceed '
               'longest chain length).\n'
               ' * SMILES: '
               'CCCCCCCCC(C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-methylundecanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CC(=C)C(CCCC(O)=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-isopropenylpimeloyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a thioester-linked fatty acyl chain with a branch and '
               'a CoA moiety. Contains a branched acyl chain (total carbons '
               'exceed longest chain length).\n'
               ' * SMILES: '
               'CC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: isobutyryl-CoA(4-) REASON: WRONGLY CLASSIFIED Contains a '
               'thioester-linked fatty acyl chain with a branch and a CoA '
               'moiety. Contains a branched acyl chain (extra carbon neighbor '
               'at acyl root).\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1CCCC1)CCCCCC/C=C\\C2=CC=3OCOC3C=C2',
                                     'name': '(8E)-Piperamide-C9:1',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': '[H][C@@]12OC(=O)[C@H](C)[C@@]1(O)[C@@H](OC(C)=O)[C@]1([H])[C@@](C)([C@H](OC(C)=O)\\C=C/C(=C)[C@H]2OC)[C@@H](OC(=O)CC(C)C)[C@@H](OC(C)=O)[C@@H](OC(C)=O)[C@]11CO1',
                                     'name': 'Gemmacolide M, (rel)-',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](NC(OCC1=CC=CC=C1)=O)CC=2C=3C(NC2)=CC=CC3)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](CC4=CC=CC=C4)C(=O)N)C',
                                     'name': 'Gatratet',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': 'O=C(NCCC(=O)O)[C@@H]1N(NCCC1)C(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H]2N=C(C3=C(O)C=CC=C3)OC2)CO)CCCN(O)C=O',
                                     'name': 'Cahuitamycin A',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': 'C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@H](C)CO)C)CN(C)C(=O)CC3=CC=CC=C3',
                                     'name': 'N-[[(3S,9S,10R)-16-(dimethylamino)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methyl-2-phenylacetamide',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': 'OC[C@H]1O[C@H](OC[C@H]2O[C@H](OC[C@H]3O[C@H](OC[C@H]4O[C@H](OC[C@H]5O[C@H](O[C@]6(CO)O[C@H](CO)[C@@H](O)[C@@H]6O)[C@H](O)[C@@H](O)[C@@H]5O)[C@H](O)[C@@H](O)[C@H]4O)[C@H](O)[C@@H](O)[C@H]3O)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'ajugose',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': 'NC(=O)C[C@H]([NH3+])C([O-])=O',
                                     'name': 'L-asparagine zwitterion',
                                     'reason': 'Molecule appears deprotonated '
                                               '([O-] present); expected '
                                               'neutral CoA form.'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=CC=C1)C([O-])=O)[C@@H]([NH3+])CC([O-])=O',
                                     'name': '(3S)-3-Azaniumyl-4-[[(1S)-1-carboxylato-2-phenylethyl]amino]-4-oxobutanoate',
                                     'reason': 'Molecule appears deprotonated '
                                               '([O-] present); expected '
                                               'neutral CoA form.'},
                                 {   'smiles': 'CC1=CC(O)OC1=O',
                                     'name': '5-hydroxy-3-methylfuran-2(5H)-one',
                                     'reason': 'CoA moiety not found'},
                                 {   'smiles': '[Co++].CC([O-])=O.CC([O-])=O',
                                     'name': 'cobalt(II) acetate',
                                     'reason': 'Molecule appears deprotonated '
                                               '([O-] present); expected '
                                               'neutral CoA form.'}],
    'sample_false_negatives': [   {   'smiles': 'CCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '2-methylbutanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'CCCCCCCCCCCC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(E)-2-methylpentadec-2-enoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'CCCCCCCCCCCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(2S)-2-methyltetradecanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC([C@H](CC)C)=O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '(S)-2-methylbutanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'CC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': 'isobutyryl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'C[C@H](O)[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(2S,3S)-3-hydroxy-2-methylbutanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'CCCCCCCCCCCC[C@@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(2R)-2-methyltetradecanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '2-methylhexadecanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(CCCC)C)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '2-methylhexanoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'},
                                  {   'smiles': 'CCCCCCCCCCCCC=C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '2-methylpentadec-2-enoyl-CoA',
                                      'reason': 'No branched acyl chain '
                                                'detected in any thioester '
                                                'candidate'}],
    'attempt': 3,
    'reasoning': 'Below is my reasoning. In our first try the algorithm for '
                 'finding a branched‐chain fatty acyl–CoA used two tests on '
                 'the acyl fragment: one that looked at the “extra” neighbors '
                 'at the acyl root and one comparing the total number of '
                 'carbons to the length of its longest chain. However, many '
                 'false positives were obtained because (a) the DFS used to '
                 '“extract” the acyl fragment was too permissive (sometimes '
                 'picking up additional CoA atoms or extra substituents that '
                 'are not part of the linear fatty chain), and (b) the test at '
                 'the acyl root did not reliably distinguish a terminal '
                 '“extra” neighbor (which can, for example, include an extra '
                 'bond that is inherent to a deprotonated CoA portion) from a '
                 '“true” branch. In addition, most of the false‐positive '
                 'examples showed negatively charged oxygens (written '
                 'explicitly as “[O-]” in the SMILES) that indicate a '
                 'deprotonated form. To improve the classification we now do '
                 'the following:\n'
                 '\n'
                 '1. First check that the input has no “[O-]” so that we work '
                 'with a standard protonation state.\n'
                 '2. Confirm the presence of an approximate CoA substructure.\n'
                 '3. Identify the thioester group using a SMARTS.\n'
                 '4. Extract the fatty acyl fragment by starting at the carbon '
                 'attached to the carbonyl (ignoring oxygen and sulfur) and '
                 'traversing only to carbon neighbors.\n'
                 '5. Restrict to acyclic (“simple”) fragments.\n'
                 '6. Instead of only looking at the acyl‐root, compute in the '
                 'induced subgraph for the acyl fragment the degree (number of '
                 'neighboring carbons inside the fragment) of each carbon. In '
                 'a linear chain every “internal” atom should have exactly 2 '
                 'neighbors (terminal ones have 1). If any atom has a degree '
                 'greater than 2 then that suggests a branch.\n'
                 '7. Return True if any thioester candidate gives a branched '
                 'acyl fragment.\n'
                 '\n'
                 'Below is the complete program in a single Python code '
                 'block.\n'
                 '\n'
                 '-------------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 28,
    'num_true_negatives': 142227,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.5409836065573771,
    'recall': 0.7333333333333333,
    'f1': 0.6226415094339622,
    'accuracy': 0.9997189037245257,
    'negative_predictive_value': 0.9999156349524392}