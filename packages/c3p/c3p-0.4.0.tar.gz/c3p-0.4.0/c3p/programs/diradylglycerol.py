"""
Classifies: CHEBI:76578 diradylglycerol
"""
#!/usr/bin/env python3
"""
Classifies: Diradylglycerol
Definition: Any lipid that is glycerol bearing two substituent groups – either acyl, alkyl,
or alk-1-enyl – at any two of the three possible positions. That is, a diacyl (or di-alkyl/alk-1-enyl)
glycerol should have a glycerol backbone in which exactly two of its oxygen groups are esterified (or etherified)
while the third remains a free hydroxyl.
Heuristic:
  1. Parse the molecule from the SMILES string.
  2. Loop over all atoms to find a candidate glycerol backbone.
     For a candidate central carbon:
       - It must be sp3 and have exactly two carbon neighbors.
       - Each of its two attached (terminal) carbons must have the central carbon as its only carbon neighbor.
  3. For each of the three glycerol backbone carbons (central + two terminals),
     look for exactly one oxygen substituent (via a single bond) that is not itself part of the backbone.
  4. For each oxygen in the backbone substituents, classify it as “free” (–OH) or “substituted” (acyl/alkyl)
     via the following improved logic:
         • If it has any attached hydrogen, call it free.
         • Otherwise, check the non-backbone neighbors.
             – If any neighbor is phosphorus, reject this candidate (phospholipid-like).
             – If a neighbor is carbon that bears a double bond to another oxygen (a carbonyl) then mark as substituted.
         • If no hydrogen is found and no convincing carbonyl is found, assume it is substituted.
  5. Finally, if exactly one oxygen is free and two are substituted, we classify the input as a diradylglycerol.
If no candidate passes, return False with a summary reason.
"""

from rdkit import Chem

def is_diradylglycerol(smiles: str):
    """
    Determines if a molecule is a diradylglycerol (a diacyl/di-alkyl/di-alk-1-enyl glycerol)
    based on its SMILES string using a heuristic for a glycerol backbone and analysis of oxygen substituents.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if the molecule is classified as a diradylglycerol; False otherwise.
        str: Explanation of the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Improved function to decide if an oxygen atom (attached to a backbone carbon) is free (OH) or substituted.
    def oxygen_is_free(oxy, backbone_idx):
        """
        Determine if the oxygen 'oxy' is a free hydroxyl (returns True) or is substituted (returns False).
        Additionally, if the oxygen is attached to a phosphorus atom, we mark this candidate as not a DG.
        """
        # Use explicit and implicit hydrogen count.
        num_H = oxy.GetNumExplicitHs() + oxy.GetNumImplicitHs()
        if num_H > 0:
            # Likely a free hydroxyl.
            return True
        
        # Examine non-backbone neighbors.
        for nbr in oxy.GetNeighbors():
            if nbr.GetIdx() == backbone_idx:
                continue
            # If the oxygen is attached to phosphorus, then it belongs to e.g. a phosphate headgroup.
            if nbr.GetAtomicNum() == 15:
                # Signal an ambiguous situation by returning None.
                return None
            if nbr.GetSymbol() == 'C':
                # Look at bonds from the neighbor to see if it bears a carbonyl.
                for bond in nbr.GetBonds():
                    # Identify a double bond to another oxygen from this neighbor.
                    if bond.GetBondType() == Chem.BondType.DOUBLE:
                        other = bond.GetOtherAtom(nbr)
                        if other.GetSymbol() == 'O' and other.GetIdx() != oxy.GetIdx():
                            return False  # This oxygen is part of an ester linkage.
        # No hydrogen and no clear carbonyl detected: assume substituted (e.g. an ether or vinyl linkage).
        return False
    
    last_reason = "No candidate glycerol backbone was found."
    # Loop over all atoms to search for a candidate central carbon of a glycerol backbone.
    for atom in mol.GetAtoms():
        # We require the candidate central atom to be carbon.
        if atom.GetSymbol() != "C":
            continue
        # The candidate must be sp3 hybridized.
        if atom.GetHybridization() != Chem.HybridizationType.SP3:
            continue
        # The candidate central carbon should have exactly two carbon neighbors.
        carbon_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetSymbol() == "C"]
        if len(carbon_neighbors) != 2:
            continue
        central = atom
        term1, term2 = carbon_neighbors

        # For each terminal carbon, its only carbon neighbor should be the central carbon.
        valid_terminals = True
        for term in (term1, term2):
            others = [nbr for nbr in term.GetNeighbors() if nbr.GetSymbol() == "C" and nbr.GetIdx() != central.GetIdx()]
            if others:
                valid_terminals = False
                break
        if not valid_terminals:
            continue

        # We have a candidate glycerol backbone (central, term1, term2).
        backbone_idxs = {central.GetIdx(), term1.GetIdx(), term2.GetIdx()}
        oxy_info = []  # Each entry: (backbone_atom_idx, oxygen_atom_idx, is_free)
        valid_backbone = True

        # For each backbone carbon we expect exactly one oxygen connected by a single (non-backbone) bond.
        for b_idx in backbone_idxs:
            carbon_atom = mol.GetAtomWithIdx(b_idx)
            oxygen_subs = []
            for bond in carbon_atom.GetBonds():
                # Only consider single bonds.
                if bond.GetBondType() != Chem.BondType.SINGLE:
                    continue
                nbr = bond.GetOtherAtom(carbon_atom)
                # Exclude atoms that belong to the backbone.
                if nbr.GetSymbol() == "O" and nbr.GetIdx() not in backbone_idxs:
                    oxygen_subs.append(nbr)
            if len(oxygen_subs) != 1:
                valid_backbone = False
                last_reason = ("Backbone carbon (idx {}) does not have exactly one oxygen substituent (found {})."
                               .format(b_idx, len(oxygen_subs)))
                break
            oxy = oxygen_subs[0]
            free = oxygen_is_free(oxy, b_idx)
            # If our oxygen assessment returns None, then the candidate backbone is part of a phospholipid.
            if free is None:
                valid_backbone = False
                last_reason = ("Backbone oxygen (idx {}) attached to carbon (idx {}) is connected to phosphorus."
                               .format(oxy.GetIdx(), b_idx))
                break
            oxy_info.append((b_idx, oxy.GetIdx(), free))
        if not valid_backbone:
            continue

        # In a diradylglycerol we expect exactly one free hydroxyl and two substituted oxygens.
        free_count = sum(1 for (_, _, is_free) in oxy_info if is_free)
        sub_count  = sum(1 for (_, _, is_free) in oxy_info if not is_free)
        if free_count == 1 and sub_count == 2:
            msg = ("Found glycerol backbone (central carbon idx {}) with two substituted positions and one free hydroxyl. "
                   "Backbone oxygen details: {}").format(central.GetIdx(), oxy_info)
            return True, msg
        else:
            last_reason = ("Candidate glycerol backbone (central carbon idx {}) found, "
                           "but oxygens show freeOH: {} and substituted: {}."
                           ).format(central.GetIdx(), free_count, sub_count)
    return False, ("No glycerol backbone with exactly two substituted oxygen groups and one free hydroxyl "
                   "was identified. " + last_reason)

# Example usage:
if __name__ == "__main__":
    # Test with one sample SMILES (a DG structure expected to be a diradylglycerol)
    test_smiles = "C([C@@](COC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])O"
    classification, reason = is_diradylglycerol(test_smiles)
    print("Classification:", classification)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:76578',
                          'name': 'diradylglycerol',
                          'definition': 'Any lipid that is glycerol bearing '
                                        'two substituent groups - either acyl, '
                                        'alkyl, or alk-1-enyl - at any two of '
                                        'the three possible positions.',
                          'parents': ['CHEBI:35741'],
                          'xrefs': ['LIPID_MAPS_class:LMGL0201'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 63,
                           'log_lines_of_code': 4.143134726391533,
                           'indent_by_line': [   1,
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
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 7,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'GetSymbol',
                                                 'GetOtherAtom',
                                                 'GetNeighbors',
                                                 'GetNumImplicitHs',
                                                 'GetNumExplicitHs',
                                                 'GetBonds',
                                                 'GetAtoms',
                                                 'GetIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetHybridization'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_diradylglycerol(smiles: str):',
                                       'oxygen_is_free(oxy, backbone_idx):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True',
                                          'None',
                                          'False  # This oxygen is part of an '
                                          'ester linkage.',
                                          'False',
                                          'False, ("No glycerol backbone with '
                                          'exactly two substituted oxygen '
                                          'groups and one free hydroxyl "'],
                           'returns_count': 6,
                           'complexity': 6.2286269452783065},
    'message': '\n'
               'Attempt failed: F1 score of 0.27338435374149656 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C([C@@](COC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])O '
               'NAME: DG(20:4(5Z,8Z,11Z,14Z)/18:2(9Z,12Z)/0:0) REASON: CORRECT '
               'Found glycerol backbone (central carbon idx 1) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(0, 45, True), (1, 25, False), (2, 3, False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCC)[C@H](COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)CO '
               'NAME: DG(22:6(4Z,7Z,10Z,13Z,16Z,19Z)/15:0/0:0) REASON: CORRECT '
               'Found glycerol backbone (central carbon idx 17) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(17, 0, False), (18, 19, False), (43, 44, True)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)C[C@@H](OC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)CO '
               'NAME: DG(22:2(13Z,16Z)/20:4(8Z,11Z,14Z,17Z)/0:0) REASON: '
               'CORRECT Found glycerol backbone (central carbon idx 25) with '
               'two substituted positions and one free hydroxyl. Backbone '
               'oxygen details: [(24, 0, False), (25, 26, False), (48, 49, '
               'True)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)C[C@@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)CO '
               'NAME: DG(22:2(13Z,16Z)/20:4(5Z,8Z,11Z,14Z)/0:0) REASON: '
               'CORRECT Found glycerol backbone (central carbon idx 25) with '
               'two substituted positions and one free hydroxyl. Backbone '
               'oxygen details: [(24, 0, False), (25, 26, False), (48, 49, '
               'True)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCC)C[C@@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)CO '
               'NAME: DG(13:0/20:5(5Z,8Z,11Z,14Z,17Z)/0:0)[iso2] REASON: '
               'CORRECT Found glycerol backbone (central carbon idx 16) with '
               'two substituted positions and one free hydroxyl. Backbone '
               'oxygen details: [(16, 17, False), (39, 40, True), (15, 0, '
               'False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCC/C=C\\CCCCCCCC)CC(O)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: DG(18:1n9/0:0/18:4n3) REASON: CORRECT Found glycerol '
               'backbone (central carbon idx 21) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(20, 0, False), (21, 22, True), (23, 24, False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCC/C=C\\C/C=C\\CCCCCC)C[C@@H](O)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: DG(18:2n6/0:0/20:4n6) REASON: CORRECT Found glycerol '
               'backbone (central carbon idx 22) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(24, 25, False), (21, 0, False), (22, 23, True)]\n'
               ' * SMILES: '
               'O(CCCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC '
               'NAME: (2S)-3-(Icosanoyloxy)-2-(octadecyloxy)propyl '
               '(11Z)-icos-11-enoate REASON: CORRECT Found glycerol backbone '
               '(central carbon idx 19) with two substituted positions and one '
               'free hydroxyl. Backbone oxygen details: [(43, 44, False), (19, '
               '0, True), (20, 21, False)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])O '
               'NAME: DG(14:0/22:4(7Z,10Z,13Z,16Z)/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 1) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(0, '
               '43, True), (1, 19, False), (2, 3, False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCC)CO NAME: '
               'DG(20:0/12:0/0:0) REASON: CORRECT Found glycerol backbone '
               '(central carbon idx 23) with two substituted positions and one '
               'free hydroxyl. Backbone oxygen details: [(38, 39, True), (22, '
               '0, False), (23, 24, False)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\CCCC)=O)(OC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])O '
               'NAME: DG(14:1(9Z)/22:4(7Z,10Z,13Z,16Z)/0:0) REASON: CORRECT '
               'Found glycerol backbone (central carbon idx 1) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(0, 43, True), (1, 19, False), (2, 3, False)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)(OC(CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)=O)[H])O '
               'NAME: DG(18:2(9Z,12Z)/20:3(5Z,8Z,11Z)/0:0) REASON: CORRECT '
               'Found glycerol backbone (central carbon idx 1) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(0, 45, True), (1, 23, False), (2, 3, False)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCCCC)=O)[H])O '
               'NAME: DG(16:1(9Z)/20:1(11Z)/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 1) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(0, '
               '43, True), (1, 21, False), (2, 3, False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCC)[C@H](COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)CO '
               'NAME: DG(18:4(6Z,9Z,12Z,15Z)/15:0/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 17) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(17, 0, False), (18, 19, False), (39, 40, True)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)CO '
               'NAME: DG(22:4(7Z,10Z,13Z,16Z)/24:0/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 26) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(26, 0, False), (27, 28, False), (52, 53, True)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)=O)(OC(CCCCCCC/C=C\\CCCCCC)=O)[H])O '
               'NAME: DG(18:3(9Z,12Z,15Z)/16:1(9Z)/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 1) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(0, '
               '41, True), (1, 23, False), (2, 3, False)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])O '
               'NAME: DG(18:0/20:2(11Z,14Z)/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 1) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(0, '
               '45, True), (1, 23, False), (2, 3, False)]\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)OC[C@H](CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-icosanoyl-2-oleoyl-sn-glycerol REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 23) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(24, 25, True), (22, 21, False), (23, 26, False)]\n'
               ' * SMILES: '
               'O(C[C@@H](O)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: DG(20:4n6/0:0/22:6n3) REASON: CORRECT Found glycerol '
               'backbone (central carbon idx 2) with two substituted positions '
               'and one free hydroxyl. Backbone oxygen details: [(1, 0, '
               'False), (2, 3, True), (4, 5, False)]\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](CO)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1,2-dilinoleoyl-sn-glycerol REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 21) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(20, 19, False), (21, 24, False), (22, 23, True)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCC/C=C\\CCCC)=O)[H])O '
               'NAME: DG(22:0/14:1(9Z)/0:0) REASON: CORRECT Found glycerol '
               'backbone (central carbon idx 1) with two substituted positions '
               'and one free hydroxyl. Backbone oxygen details: [(0, 43, '
               'True), (1, 27, False), (2, 3, False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCC(C)C)[C@H](COC(=O)CCCCCCCCCCCCCCCCCCC)CO NAME: '
               'DG(20:0/i-12:0/0:0) REASON: CORRECT Found glycerol backbone '
               '(central carbon idx 14) with two substituted positions and one '
               'free hydroxyl. Backbone oxygen details: [(38, 39, True), (14, '
               '0, False), (15, 16, False)]\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCCCCCCCC)CO '
               'NAME: DG(16:0/24:1(15Z)/0:0) REASON: CORRECT Found glycerol '
               'backbone (central carbon idx 26) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(26, 0, False), (27, 28, False), (46, 47, True)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\CCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])O '
               'NAME: DG(14:1(9Z)/18:1(11Z)/0:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 1) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(0, '
               '39, True), (1, 19, False), (2, 3, False)]\n'
               ' * SMILES: '
               'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCC/C=C\\CCCCCCCC '
               'NAME: TG(24:1(15Z)/22:2(13Z,16Z)/o-18:0) REASON: CORRECT Found '
               'glycerol backbone (central carbon idx 20) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(19, 0, True), (20, 21, False), (45, 46, False)]\n'
               'False positives: SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PI(22:0/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 15) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(35, 36, False), (14, 13, True), (15, 16, False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC(O)/C=C/C=C/C\\C=C\\CCCCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(18:3(6Z,9Z,12Z)/20:3(6,8,11)-OH(5)) REASON: WRONGLY '
               'CLASSIFIED Found glycerol backbone (central carbon idx 3) with '
               'two substituted positions and one free hydroxyl. Backbone '
               'oxygen details: [(27, 28, False), (2, 1, True), (3, 4, '
               'False)]\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:1(11Z)/16:0) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 15) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(16, 17, False), (14, 13, True), (15, 37, False)]\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(17:0/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 10) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(9, '
               '8, True), (10, 11, False), (30, 31, False)]\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[NH3+])OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-myristoyl-2-oleoyl-sn-glycero-3-phosphoethanolamine '
               'zwitterion REASON: WRONGLY CLASSIFIED Found glycerol backbone '
               '(central carbon idx 17) with two substituted positions and one '
               'free hydroxyl. Backbone oxygen details: [(16, 15, False), (17, '
               '27, False), (18, 19, True)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(20:1(11Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (central carbon idx '
               '3) with two substituted positions and one free hydroxyl. '
               'Backbone oxygen details: [(2, 1, True), (3, 4, False), (28, '
               '29, False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(18:0/19:1(9Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 3) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(25, 26, False), (2, 1, True), (3, 4, False)]\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCC(O)/C=C/C(O)=O)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)=O '
               'NAME: OHDdiA-PI REASON: WRONGLY CLASSIFIED Found glycerol '
               'backbone (central carbon idx 15) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(33, 34, False), (14, 13, True), (15, 16, False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)(O)=O '
               'NAME: PA(16:1(9Z)/14:1(9Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 3) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(2, '
               '1, True), (3, 4, False), (20, 21, False)]\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCC)([O-])=O '
               'NAME: PC(12:0/18:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 10) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(9, '
               '8, True), (10, 11, False), (31, 32, False)]\n'
               ' * SMILES: '
               'P(OCC(OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN(C)C)(O)=O '
               'NAME: Pe-nme2(15:0/22:0) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 3) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(2, '
               '1, True), (3, 4, False), (28, 29, False)]\n'
               ' * SMILES: '
               'P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@@H](CC=CCCCC(OC[C@@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COP(O1)(O)=O)=O)C=CC(=O)[C@@H]([C@H](O)[C@@H]2O)/C=C/[C@@H](O)CCCCC)(O)=O '
               'NAME: CDP-DG(PGJ2/18:1(11Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 24) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: '
               '[(24, 25, False), (45, 46, True), (23, 22, False)]\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(18:1(11Z)/20:4(5Z,8Z,11Z,14Z)) REASON: WRONGLY '
               'CLASSIFIED Found glycerol backbone (central carbon idx 1) with '
               'two substituted positions and one free hydroxyl. Backbone '
               'oxygen details: [(0, 45, True), (1, 23, False), (2, 3, '
               'False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: PA(18:3(6Z,9Z,12Z)/20:1(11Z)) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (central carbon idx 3) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(26, 27, False), (2, 1, True), (3, 4, False)]\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)([O-])=O '
               'NAME: PC(22:1(11Z)/12:0) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 10) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(9, '
               '8, True), (10, 11, False), (25, 26, False)]\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCC)(O)=O '
               'NAME: PI(13:0/18:3(9Z,12Z,15Z)) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (central carbon idx 15) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(36, 37, False), (14, 13, True), (15, 16, False)]\n'
               ' * SMILES: '
               'P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: 3-(Phosphonooxy)-1,2-propanediyl dioctadecanoate REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (central carbon idx '
               '3) with two substituted positions and one free hydroxyl. '
               'Backbone oxygen details: [(24, 25, False), (2, 1, True), (3, '
               '4, False)]\n'
               ' * SMILES: '
               'CC(CCCC(CCCC(CCCC(CC(=O)OC(COP(=O)(O)OCC[N+](C)(C)C)COC(CC(CCCC(CCCC(CCCC(C)C)C)C)C)=O)C)C)C)C '
               'NAME: 1,2-diphytanoyl-sn-glycero-3-phosphocholine REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (central carbon idx '
               '18) with two substituted positions and one free hydroxyl. '
               'Backbone oxygen details: [(18, 17, False), (19, 20, True), '
               '(31, 32, False)]\n'
               ' * SMILES: '
               'P(O[C@H]1C(C(O)C(O)[C@@H](O)C1O)C)(OC[C@H](OC(=O)CCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PS-PI REASON: WRONGLY CLASSIFIED Found glycerol backbone '
               '(central carbon idx 15) with two substituted positions and one '
               'free hydroxyl. Backbone oxygen details: [(24, 25, False), (14, '
               '13, True), (15, 16, False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(22:1(13Z)/18:3(9Z,12Z,15Z)) REASON: WRONGLY '
               'CLASSIFIED Found glycerol backbone (central carbon idx 3) with '
               'two substituted positions and one free hydroxyl. Backbone '
               'oxygen details: [(24, 25, False), (2, 1, True), (3, 4, '
               'False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(15:0/20:3(8Z,11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (central carbon idx 3) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(26, 27, False), (2, 1, True), (3, 4, False)]\n'
               ' * SMILES: '
               'O1C(C1C/C=C\\CCCCC)CCCCCCCC(O[C@H](COC(=O)CCCCCCC)CO)=O NAME: '
               'DG(8:0/18:1(12Z)-O(9S,10R)/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (central carbon idx 20) with two '
               'substituted positions and one free hydroxyl. Backbone oxygen '
               'details: [(32, 33, True), (20, 19, False), (21, 22, False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(20:0/16:1(9Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 3) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(2, '
               '1, True), (3, 4, False), (22, 23, False)]\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(17:0/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 3) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(2, '
               '1, True), (3, 4, False), (23, 24, False)]\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(15:0/17:1(9Z)) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (central carbon idx 10) with two substituted '
               'positions and one free hydroxyl. Backbone oxygen details: [(9, '
               '8, True), (10, 11, False), (30, 31, False)]\n'
               'False negatives: SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCC)CC(O)COCC(O)CO NAME: 253MC0P0YV '
               'REASON: MISSED No glycerol backbone with exactly two '
               'substituted oxygen groups and one free hydroxyl was '
               'identified. Candidate glycerol backbone (central carbon idx '
               '26) found, but oxygens show freeOH: 3 and substituted: 0.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](CO)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: 1-palmityl-2-arachidonoyl-sn-glycerol REASON: MISSED No '
               'glycerol backbone with exactly two substituted oxygen groups '
               'and one free hydroxyl was identified. Candidate glycerol '
               'backbone (central carbon idx 18) found, but oxygens show '
               'freeOH: 2 and substituted: 1.\n'
               ' * SMILES: '
               '[C@H](OCC[C@@H](CCC[C@H](C)CCC[C@@H](CCCC(C)C)C)C)(COCC[C@@H](CCC[C@H](C)CCC[C@@H](CCCC(C)C)C)C)CO '
               'NAME: 2,3-di-O-phytanyl-sn-glycerol REASON: MISSED No glycerol '
               'backbone with exactly two substituted oxygen groups and one '
               'free hydroxyl was identified. Candidate glycerol backbone '
               '(central carbon idx 0) found, but oxygens show freeOH: 3 and '
               'substituted: 0.\n'
               ' * SMILES: O(C(=O)CCCCCCC/C=C\\CCCCCCCC)CC(O)COCC(O)CO NAME: '
               'Diglyceryl monooleate REASON: MISSED No glycerol backbone with '
               'exactly two substituted oxygen groups and one free hydroxyl '
               'was identified. Candidate glycerol backbone (central carbon '
               'idx 26) found, but oxygens show freeOH: 3 and substituted: 0.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: 1-palmityl-2-arachidonoyl-sn-glycero-3-phosphate(2-) '
               'REASON: MISSED No glycerol backbone with exactly two '
               'substituted oxygen groups and one free hydroxyl was '
               'identified. Candidate glycerol backbone (central carbon idx '
               '18) found, but oxygens show freeOH: 2 and substituted: 1.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCOCC(O)COC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-O-palmityl-3-oleoylglycerol REASON: MISSED No glycerol '
               'backbone with exactly two substituted oxygen groups and one '
               'free hydroxyl was identified. Candidate glycerol backbone '
               '(central carbon idx 18) found, but oxygens show freeOH: 2 and '
               'substituted: 1.\n'
               ' * SMILES: '
               'O(CCC([N+](C)(C)C)C([O-])=O)CC(O)COC(=O)CCCCCCC/C=C\\CCCCCCCC '
               'NAME: '
               '4-[2-hydroxy-3-[(Z)-octadec-9-enoyl]oxypropoxy]-2-(trimethylazaniumyl)butanoate '
               'REASON: MISSED No glycerol backbone with exactly two '
               'substituted oxygen groups and one free hydroxyl was '
               'identified. Candidate glycerol backbone (central carbon idx '
               '12) found, but oxygens show freeOH: 2 and substituted: 1.\n'
               ' * SMILES: '
               'C[C@H]1CCC[C@@H](C)CCC[C@@H](C)CC[C@H](C)CCC[C@H](C)CCC[C@H](C)CCC[C@H](C)CCOC(CO)COCC[C@@H](C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@@H](C)CC[C@H](C)CCC[C@H](C)CCC[C@H](C)CCC[C@H](C)CCOC(CO)COCC[C@@H](C)CCC1 '
               'NAME: caldarchaeol REASON: MISSED No glycerol backbone with '
               'exactly two substituted oxygen groups and one free hydroxyl '
               'was identified. Candidate glycerol backbone (central carbon '
               'idx 80) found, but oxygens show freeOH: 3 and substituted: 0.\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(O/C=C\\CCCCCCCCCCCCCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([O-])=O '
               'NAME: PC(22:6(4Z,7Z,10Z,13Z,16Z,19Z)/P-18:0) REASON: MISSED No '
               'glycerol backbone with exactly two substituted oxygen groups '
               'and one free hydroxyl was identified. Candidate glycerol '
               'backbone (central carbon idx 10) found, but oxygens show '
               'freeOH: 2 and substituted: 1.\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(O/C=C\\CCCCCC/C=C\\CCCCCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)([O-])=O '
               'NAME: PC(22:5(4Z,7Z,10Z,13Z,16Z)/P-18:1(9Z)) REASON: MISSED No '
               'glycerol backbone with exactly two substituted oxygen groups '
               'and one free hydroxyl was identified. Candidate glycerol '
               'backbone (central carbon idx 10) found, but oxygens show '
               'freeOH: 2 and substituted: 1.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. Backbone '
                                               'carbon (idx 0) does not have '
                                               'exactly one oxygen substituent '
                                               '(found 0).'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. Backbone '
                                               'carbon (idx 13) does not have '
                                               'exactly one oxygen substituent '
                                               '(found 0).'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No glycerol backbone with '
                                               'exactly two substituted oxygen '
                                               'groups and one free hydroxyl '
                                               'was identified. No candidate '
                                               'glycerol backbone was found.'}],
    'sample_false_negatives': [   {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC',
                                      'name': '(2S)-3-(Icosanoyloxy)-2-(octadecyloxy)propyl '
                                              '(11Z)-icos-11-enoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 19) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCC/C=C\\CCCCCCCC',
                                      'name': 'TG(24:1(15Z)/22:2(13Z,16Z)/o-18:0)',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 20) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC',
                                      'name': '(2R)-3-(Octadecyloxy)-2-(pentadecanoyloxy)propyl '
                                              '(11Z,14Z)-icosa-11,14-dienoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 20) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                      'name': '(2R)-1-(Octadecyloxy)-3-[(9Z)-tetradec-9-enoyloxy]propan-2-yl '
                                              'pentadecanoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 20) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCC',
                                      'name': 'TG(14:0/o-18:0/24:1(15Z))',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 19) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                      'name': '1-palmityl-2-arachidonoyl-sn-glycero-3-phosphate(2-)',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Backbone oxygen (idx 20) '
                                                'attached to carbon (idx 19) '
                                                'is connected to phosphorus.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCC',
                                      'name': '(2R)-1-[(11Z)-Octadec-11-enoyloxy]-3-(octadecyloxy)propan-2-yl '
                                              '(4Z,7Z,10Z,13Z,16Z)-docosa-4,7,10,13,16-pentaenoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 20) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC',
                                      'name': '(2S)-3-[(9Z)-Hexadec-9-enoyloxy]-2-(octadecyloxy)propyl '
                                              'octadecanoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 19) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                      'name': '(2S)-2-(Octadecyloxy)-3-[(9Z)-tetradec-9-enoyloxy]propyl '
                                              '(9Z)-hexadec-9-enoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 19) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\CCCCCCCC',
                                      'name': '(2R)-3-(Octadecyloxy)-2-(pentadecanoyloxy)propyl '
                                              '(13Z)-docos-13-enoate',
                                      'reason': 'No glycerol backbone with '
                                                'exactly two substituted '
                                                'oxygen groups and one free '
                                                'hydroxyl was identified. '
                                                'Candidate glycerol backbone '
                                                '(central carbon idx 20) '
                                                'found, but oxygens show '
                                                'freeOH: 0 and substituted: '
                                                '3.'}],
    'attempt': 3,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 '• The previous approach tried to “find” a glycerol backbone '
                 'candidate by scanning for an sp³ carbon with exactly two '
                 'carbon neighbors and then requiring that each of that carbon '
                 'plus its two “terminal” carbons bear exactly one oxygen '
                 'substituent. Then, for each substituent oxygen the code '
                 'checked (using its hydrogen count and neighboring atoms) '
                 'whether it was “free” (–OH) or “substituted” (ester/ether). '
                 'However, many false positives came from cases where a '
                 'phospholipid (or another lipid class) presented a similar '
                 'backbone – for example, an oxygen that is connected to a '
                 'phosphorus atom, or a backbone where an extra oxygen is '
                 'present. In addition, some diradyl glycerols were missed '
                 '(false negatives) because the oxygen in an ester linkage was '
                 'mis‐classified as free (or vice‐versa).\n'
                 '\n'
                 '• To improve this we add two modifications:\n'
                 '\u2002 – First, when examining an oxygen substituent we not '
                 'only check for attached hydrogens but also look for '
                 'convincing “ester/ether” connectivity (for example, if that '
                 'oxygen is bonded to a carbon that itself is double‐bonded to '
                 'another oxygen, we call it substituted). Also, if the oxygen '
                 'sees neighbors such as phosphorus then we immediately know '
                 'that this glycerol candidate is likely part of a '
                 'phospholipid (and not a diradylglycerol), so we reject it.\n'
                 '\u2002 – Second, we keep the backbone search (by looking for '
                 'a sp³ candidate with two and only two carbon neighbors whose '
                 'only carbon neighbor is that candidate) but now we use the '
                 'refined oxygen‐classification routine.\n'
                 '\n'
                 '• Finally, if exactly one oxygen in the candidate backbone '
                 'is “free” and the other two are “substituted” (by our new '
                 'routine), we report the molecule as a diradylglycerol. If no '
                 'candidate passes these filters, we return False along with a '
                 'reason.\n'
                 '\n'
                 'Below is the complete Python code block with comments:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 625,
    'num_false_positives': 144,
    'num_true_negatives': 141479,
    'num_false_negatives': 52,
    'num_negatives': None,
    'precision': 0.812743823146944,
    'recall': 0.9231905465288035,
    'f1': 0.8644536652835407,
    'accuracy': 0.9986226282501757,
    'negative_predictive_value': 0.99963258932672}