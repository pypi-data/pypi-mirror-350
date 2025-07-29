"""
Classifies: CHEBI:52639 N-acylsphingosine
"""
#!/usr/bin/env python
"""
Classifies: N‐acylsphingosine (parent compounds of the ceramide family)

Definition: An N‐acylsphingosine is a molecule that contains a sphingosine backbone –
an acyclic chain featuring a secondary amine attached to two hydroxyl‐bearing carbons
(where one of these carbons is linked to a C=C bond) – and where the nitrogen is acylated
(via an amide bond to a fatty acyl group that itself has a long aliphatic chain).

Improvements over previous version:
  • The entire molecule is required to be free of rings (to exclude glycosyl/phosphorylated derivatives).
  • We enforce that the N atom’s degree equals 2 so that it is only bound to the backbone and the acyl group.
  • The acyl substituent must be a carbonyl carbon (connected via a double bond to oxygen)
    and carry a long aliphatic chain (minimum 6 carbons) defined by a DFS search limited to non‐aromatic carbons.
"""

from rdkit import Chem

def is_N_acylsphingosine(smiles: str):
    """
    Determines if a molecule is an N-acylsphingosine based on its SMILES string.
    
    Our approach is to:
      1. Reject the molecule if any ring is present (thus excluding glycosphingolipids,
         gangliosides, and phosphorylated derivatives).
      2. Find a sphingosine backbone pattern defined as:
           N - C(CO) - C(O)C=C
         where the first atom is a secondary amine, the next two carbons carry hydroxyl groups,
         and the last carbon is part of an alkene.
      3. Ensure that the N atom is acylated (i.e. its only non-backbone neighbor is a carbonyl carbon
         that is directly double-bonded to an oxygen).
      4. Use a DFS search to ensure that the acyl carbonyl is attached to a long, unbranched aliphatic chain
         (at least 6 connected carbons, none in rings or aromatic).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule matches the N-acylsphingosine criteria, False otherwise.
        str: A message indicating the reason for the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject molecules with any rings (this removes sugar headgroups, phosphates, etc.)
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains ring systems not found in a parent N-acylsphingosine structure"
    
    # Define a sphingosine backbone SMARTS: we require –N–C(CO)–C(O)C=C.
    # This pattern ignores chirality and is simplified.
    backbone_smarts = "N-C(CO)-C(O)C=C"
    backbone_pattern = Chem.MolFromSmarts(backbone_smarts)
    if backbone_pattern is None:
        return False, "Error in backbone SMARTS definition"
    
    backbone_matches = mol.GetSubstructMatches(backbone_pattern, useChirality=False)
    if not backbone_matches:
        return False, "Sphingosine backbone not found"
    
    # Helper function: DFS to count maximum chain length (number of connected, non-aromatic carbon atoms).
    def dfs_chain_length(atom, coming_from, visited):
        max_length = 0
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() == coming_from:
                continue
            # Only count if the neighbor is a non-aromatic carbon and not part of a ring.
            if nbr.GetAtomicNum() == 6 and (not nbr.GetIsAromatic()):
                if nbr.GetIdx() in visited:
                    continue
                visited.add(nbr.GetIdx())
                length = 1 + dfs_chain_length(nbr, atom.GetIdx(), visited)
                if length > max_length:
                    max_length = length
                visited.remove(nbr.GetIdx())
        return max_length

    # Set minimum chain length for the fatty acyl group (in number of carbon atoms)
    min_chain_length = 6

    # Iterate over each sphingosine backbone match.
    for match in backbone_matches:
        # Ensure that the backbone atoms (by the match) are acyclic.
        if any(mol.GetAtomWithIdx(idx).IsInRing() for idx in match):
            continue  # if any backbone atom is in a ring, skip this match

        # Our backbone pattern is defined with the first atom as nitrogen.
        n_idx = match[0]
        n_atom = mol.GetAtomWithIdx(n_idx)
        
        # Ensure the N atom is a secondary amine: it should have exactly two neighbors.
        # One neighbor should be from the backbone, and one must be the acyl substituent.
        n_neighbors = [nbr for nbr in n_atom.GetNeighbors()]
        if len(n_neighbors) != 2:
            continue
        
        # Identify the non-backbone neighbor of the nitrogen.
        acyl_candidate = None
        for nbr in n_neighbors:
            if nbr.GetIdx() not in match:
                acyl_candidate = nbr
                break
        if acyl_candidate is None:
            continue

        # Check that the acyl candidate is a carbon that is acyl (i.e. part of a carbonyl group).
        if acyl_candidate.GetAtomicNum() != 6:
            continue
        # It must be connected to at least one oxygen via a double bond.
        carbonyl_found = False
        for bond in acyl_candidate.GetBonds():
            if bond.GetBondType() == Chem.BondType.DOUBLE:
                other = bond.GetOtherAtom(acyl_candidate)
                if other.GetAtomicNum() == 8:
                    carbonyl_found = True
                    break
        if not carbonyl_found:
            continue
        
        # Now, search from the acyl candidate (excluding the bond back to N) for a long aliphatic chain.
        visited = set([acyl_candidate.GetIdx()])
        chain_length = dfs_chain_length(acyl_candidate, n_idx, visited)
        # Include the carbonyl carbon itself in the chain count.
        total_chain = 1 + chain_length
        if total_chain < min_chain_length:
            continue
        
        # If reached here, we have:
        # – a sphingosine backbone with no rings,
        # – an N atom with exactly one extra substituent that is a carbonyl-containing carbon,
        # – and that carbonyl is attached to a sufficiently long, unbranched carbon chain.
        return True, "Molecule contains a sphingosine backbone with an N-linked acyl (fatty acid) group and a long aliphatic chain"

    return False, "No valid N-acylsphingosine backbone with proper acylation and long acyl chain found"


# Example usage:
if __name__ == "__main__":
    # Test a few provided examples.
    test_smiles = [
        # True positive:
        "CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC",  # N-2-hydroxylignoceroylsphingosine
        "CCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCC\\C=C/CCCCCCCC",  # N-(11Z)-icosenoylsphingosine
        # False negative (should be accepted):
        "CCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(C)=O"  # N-acetylsphingosine
    ]
    
    for s in test_smiles:
        res, reason = is_N_acylsphingosine(s)
        print(res, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:52639',
                          'name': 'N-acylsphingosine',
                          'definition': 'The parent compounds of the ceramide '
                                        'family, composed of sphingosine '
                                        'having an unspecified fatty acyl '
                                        'group attached to the nitrogen.',
                          'parents': ['CHEBI:82830', 'CHEBI:83273'],
                          'xrefs': [   'KEGG:C00195',
                                       'LIPID_MAPS_class:LMSP0201',
                                       'PMID:1378088',
                                       'PMID:7542630'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 69,
                           'log_lines_of_code': 4.23410650459726,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 'GetSubstructMatches',
                                                 'remove',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'GetIdx',
                                                 'GetNeighbors',
                                                 'GetIsAromatic',
                                                 'GetRingInfo',
                                                 'add',
                                                 'IsInRing'],
                           'methods_called_count': 13,
                           'smarts_strings': ['backbone_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_N_acylsphingosine(smiles: str):',
                                       'dfs_chain_length(atom, coming_from, '
                                       'visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains ring '
                                          'systems not found in a parent '
                                          'N-acylsphingosine structure"',
                                          'False, "Error in backbone SMARTS '
                                          'definition"',
                                          'False, "Sphingosine backbone not '
                                          'found"',
                                          'max_length',
                                          'False, "No valid N-acylsphingosine '
                                          'backbone with proper acylation and '
                                          'long acyl chain found"'],
                           'returns_count': 6,
                           'complexity': 6.0468213009194525},
    'message': '\n'
               'Attempt failed: F1 score of 0.09923664122137406 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-2-hydroxylignoceroylsphingosine REASON: CORRECT '
               'Molecule contains a sphingosine backbone with an N-linked acyl '
               '(fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-(11Z)-icosenoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               '[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCOC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)CO '
               'NAME: N-(omega-linoleoyloxydotricontanoyl)sphingosine REASON: '
               'CORRECT Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-tetracosanoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'C(CCCCCCCCCC)CC\\C=C\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCO)CO '
               'NAME: N-(omega-hydroxytriacontanoyl)sphingosine REASON: '
               'CORRECT Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCCC '
               'NAME: N-octanoylsphingosine REASON: CORRECT Molecule contains '
               'a sphingosine backbone with an N-linked acyl (fatty acid) '
               'group and a long aliphatic chain\n'
               ' * SMILES: '
               'C(CCCCCCCCCC)CC\\C=C\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCO)CO '
               'NAME: N-(omega-hydroxyoctacosanoyl)sphingosine REASON: CORRECT '
               'Molecule contains a sphingosine backbone with an N-linked acyl '
               '(fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)C(O)CCCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-[(15Z)-2-hydroxytetracosenoyl]sphingosine REASON: '
               'CORRECT Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-icosanoylsphingosine REASON: CORRECT Molecule contains '
               'a sphingosine backbone with an N-linked acyl (fatty acid) '
               'group and a long aliphatic chain\n'
               ' * SMILES: CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCC '
               'NAME: N-(hexanoyl)sphing-4-enine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               '[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCOC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)CO '
               'NAME: N-(omega-linoleoyloxy-octacosanoyl)sphingosine REASON: '
               'CORRECT Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-octacosanoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: N-arachidonoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               '[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCOC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)CO '
               'NAME: '
               'N-(30-(9Z,12Z-octadecadienoyloxy)-tricontanoyl)-sphing-4-enine '
               'REASON: CORRECT Molecule contains a sphingosine backbone with '
               'an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)C(O)CCCC NAME: '
               'N-(2-hydroxyhexanoyl)sphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               '[C@]([C@@](/C=C/C=C/CCCCCCCCC)(O)[H])(NC(=O)C(CCCCCCCCCCCCCCCCCCCC)O)([H])CO '
               'NAME: Cer(d16:2(4E,6E)/22:0(2OH)) REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCNc1ccc([N+]([O-])=O)c2nonc12 '
               'NAME: '
               'N-{6-[(7-nitro-2,1,3-benzoxadiazol-4-yl)amino]hexanoyl}sphingosine '
               'REASON: CORRECT Molecule contains a sphingosine backbone with '
               'an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-2-hydroxystearoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-heptadecanoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCC NAME: '
               'N-dodecanoylsphingosine REASON: CORRECT Molecule contains a '
               'sphingosine backbone with an N-linked acyl (fatty acid) group '
               'and a long aliphatic chain\n'
               ' * SMILES: '
               'C(=C/CCCCCCCCCCCCC)\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCC)=O)CO '
               'NAME: N-pentacosanoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCC NAME: '
               'N-decanoylsphingosine REASON: CORRECT Molecule contains a '
               'sphingosine backbone with an N-linked acyl (fatty acid) group '
               'and a long aliphatic chain\n'
               ' * SMILES: '
               'C(CCCCCCCCCC)CC\\C=C\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCO)CO '
               'NAME: N-(omega-hydroxydotriacontanoyl)sphingosine REASON: '
               'CORRECT Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-docosanoylsphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-[(13Z)-docosenoyl]sphingosine REASON: CORRECT Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               'False positives: SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)C(O)=O)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               "beta-GalNAc-(1->4)-[alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->3)]-beta-Gal-(1->4)-beta-Glc-(1->1')-Cer(d18:1/18:0) "
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: '
               'beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-[(15Z)-tetracosenoyl]sphingosine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'C(CCCCCCCCCCCCCCC)(=O)N[C@H]([C@@H](/C=C/CCCCCCCCC(CC)C)O)CO '
               'NAME: N-hexadecanoyl-14-methylhexadecasphingosine REASON: '
               'WRONGLY CLASSIFIED Molecule contains a sphingosine backbone '
               'with an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]4[C@H](O)[C@@H](O)[C@@H](O[C@@H]4CO)OC[C@@H](NC(=O)CCCCCCC/C=C\\CCCCCCCC)[C@@H](O)/C=C\\CCCCCCCCCCCCC)[C@@H]1O)CO)[C@]5(O[C@@]([C@H](NC(=O)C)[C@@H](O)C5)([C@@H](O)[C@@H](O)CO)[H])C(O)=O '
               'NAME: Ganglioside GM1 (18:1/9Z-18:1) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-heptadecanoylsphingosine-1-phosphocholine REASON: '
               'WRONGLY CLASSIFIED Molecule contains a sphingosine backbone '
               'with an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](OS([O-])(=O)=O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-docosanoyl-(3-O-sulfo-D-galactosyl)sphingosine(1-) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)C(=O)N[C@@H](CO)[C@H](O)/C=C/CCCCCCCCCC(C)C '
               'NAME: Cer(d16:1(4E)(1OH,3OH)(15Me)/30:0(2OH[R])) REASON: '
               'WRONGLY CLASSIFIED Molecule contains a sphingosine backbone '
               'with an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCCCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](O)\\C=C\\CCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: CerP(d18:1/26:1(17Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a sphingosine backbone with an N-linked acyl '
               '(fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'O=C(NC([C@H](O)/C=C/CC/C=C(/CCCCCCCCCCCCC)\\C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)/C=C/CCCCCCCCCCCC '
               'NAME: Asperiamide C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'C(CCCCCCC(C)C)CC\\C=C\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCC)=O)COP(OCC[N+](C)(C)C)(=O)[O-] '
               'NAME: '
               'N-octadecanoyl-15-methylhexadecasphingosine-1-phosphocholine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: 1-(3-O-sulfo-beta-D-galactosyl)-N-palmitoylsphingosine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](COP(O)(=O)OCCN)NC(=O)CCCCC '
               'NAME: N-hexanoylsphingosine-1-phosphoethanolamine REASON: '
               'WRONGLY CLASSIFIED Molecule contains a sphingosine backbone '
               'with an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: beta-D-galactosyl-N-eicosanoylsphingosine REASON: '
               'WRONGLY CLASSIFIED Molecule contains a sphingosine backbone '
               'with an N-linked acyl (fatty acid) group and a long aliphatic '
               'chain\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OCC(NC(=O)C(O)C/C=C\\C/C=C\\CCCCCCCC)C(O)/C=C/CC/C=C/CC/C=C/CCC)CO '
               'NAME: HexCer 16:3;2O/16:2;O REASON: WRONGLY CLASSIFIED '
               'Molecule contains a sphingosine backbone with an N-linked acyl '
               '(fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)OCCN)[C@H](O)\\C=C\\CCCCCCCCC '
               'NAME: '
               'N-(heneicosanoyl)-tetradecasphing-4-enine-1-phosphoethanolamine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'O(P(O)(=O)OCC[N+](C)(C)C)C[C@]([C@](\\C=C\\CCCCCCCCCCC)([H])O)([H])NC(CCCCCCCCCCCCC/C=C\\CCCCCCCC)=O '
               'NAME: SM(d16:1/24:1(15Z)) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sphingosine backbone with an N-linked acyl (fatty '
               'acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCC)[C@H](O)/C=C/CC/C=C\\CCCCCCCCC)CO '
               'NAME: GlcCer(d18:2(4E,8Z)/17:0(2OH[R])) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1OC(CO)C(O)C(O)C1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-tetracosanoyl hexosylceramide REASON: WRONGLY '
               'CLASSIFIED Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-icosanoyl-15-methylhexadecasphing-4-enine-1-phosphocholine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'OC(CCCCCCCCCCCCCCCCCC)C(=O)N[C@H]([C@H](O)\\C=C\\CCCCCCCCCCC)CO '
               'NAME: Cer(d16:1(4E)/20:0(2OH)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a sphingosine backbone with an N-linked acyl '
               '(fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](COP(O)(O)=O)NC(=O)CCCCCCCCC '
               'NAME: N-decanoylsphingosine 1-phosphate REASON: WRONGLY '
               'CLASSIFIED Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(O)=O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-docosanoylsphingosine-1-phosphate REASON: WRONGLY '
               'CLASSIFIED Molecule contains a sphingosine backbone with an '
               'N-linked acyl (fatty acid) group and a long aliphatic chain\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-hexadecanoyl-15-methylhexadecasphing-4-enine-1-phosphocholine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               'C(=C/CCCCCCCCCCCCC)\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)O)O '
               'NAME: '
               'beta-D-galactosyl-(1->4)-beta-D-galactosyl-N-(pentacosanoyl)sphingosine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               ' * SMILES: '
               '[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(CO[C@@H]1O[C@@H]([C@@H]([C@@H]([C@H]1O)OS(=O)(=O)O)O)CO)NC([C@H](O)CCCCCCCCCCCCCCCCCCCCCC)=O '
               'NAME: '
               '1-(3-O-sulfo-beta-D-galactosyl)-N-[(2R)-2-hydroxylignoceroyl]sphingosine '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sphingosine '
               'backbone with an N-linked acyl (fatty acid) group and a long '
               'aliphatic chain\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(C)=O NAME: '
               'N-acetylsphingosine REASON: MISSED No valid N-acylsphingosine '
               'backbone with proper acylation and long aliphatic chain found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'Sphingosine backbone not '
                                               'found'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'Sphingosine backbone not '
                                               'found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'Molecule contains ring systems '
                                               'not found in a parent '
                                               'N-acylsphingosine structure'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(C)=O',
                                      'name': 'N-acetylsphingosine',
                                      'reason': 'No valid N-acylsphingosine '
                                                'backbone with proper '
                                                'acylation and long acyl chain '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)NC(=O)CCCCCNc1ccc([N+]([O-])=O)c2nonc12',
                                      'name': 'N-{6-[(7-nitro-2,1,3-benzoxadiazol-4-yl)amino]hexanoyl}sphingosine',
                                      'reason': 'Molecule contains ring '
                                                'systems not found in a parent '
                                                'N-acylsphingosine structure'}],
    'attempt': 4,
    'reasoning': 'Below is our reasoning and the improved code. In our '
                 'analysis of the previous attempt we noted several issues:\n'
                 '\u2003• The original SMARTS for the sphingosine backbone was '
                 'broad so that even molecules having extra rings (e.g. '
                 'glycosyl or phosphorylated groups) might produce a '
                 'substructure match.\n'
                 '\u2003• The algorithm did not strictly enforce that the '
                 'nitrogen be “clean” (i.e. only linked to the sphingosine '
                 'chain on one side and a proper acyl carbonyl on the other) '
                 'so that molecules with additional substituents or branching '
                 '(like sugars) may be falsely accepted.\n'
                 '\u2003• Many false‐positives showed ring systems (common in '
                 'glycosphingolipids) even though the definition of an '
                 'N‑acylsphingosine is a parent compound with an acyclic '
                 'sphingosine backbone.\n'
                 '\u2003\n'
                 'Our approach is to first ensure that the entire molecule is '
                 'acyclic (i.e. no sugar or ring substituents), which excludes '
                 'many of the wrong hits without losing valid examples. Then '
                 'we define a slightly stricter SMARTS for a sphingosine '
                 'backbone: namely a secondary amine (–NH–) bound to a carbon '
                 'that bears a –CH2OH group and to a second carbon carrying an '
                 '–OH and attached to a C=C fragment. We then require that the '
                 'nitrogen have exactly two connections (one in the backbone '
                 'and one acyl substituent) and that the acyl substituent is a '
                 'carbonyl carbon (i.e. with a double bond to oxygen) that is '
                 'connected to a long unbroken aliphatic (non‐ring, '
                 'non‐aromatic) chain (we require at least six carbons). This '
                 'should help minimize false‐positives while still catching '
                 'the true positives.\n'
                 '\n'
                 'Below is the complete Python code implementing these '
                 'improvements.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 192,
    'num_true_negatives': 142081,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.1152073732718894,
    'recall': 0.9259259259259259,
    'f1': 0.20491803278688525,
    'accuracy': 0.9986366830639494,
    'negative_predictive_value': 0.9999859237206422}