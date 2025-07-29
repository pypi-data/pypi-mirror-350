"""
Classifies: CHEBI:35381 monosaccharide
"""
"""
Classifies: Parent monosaccharide.
A parent monosaccharide is defined heuristically as either:
  (a) An open‐chain polyhydroxy aldehyde (or ketone) with a terminal aldehyde (or internal ketone)
      if sufficient –OH groups are present, or
  (b) A cyclic sugar (5‐ or 6‐membered ring containing oxygen) with several –OH groups.
Only molecules consisting solely of carbon and oxygen (with formal charge 0 on all atoms)
and having 3–9 carbon atoms and a single fragment are accepted.
If no typical sugar motifs are found, the compound is rejected.
Note: This is a heuristic; if the task is too difficult we may return (None, None).
"""
from rdkit import Chem

def is_monosaccharide(smiles: str):
    """
    Determines if a molecule is a parent monosaccharide based on its SMILES string.
    Improved heuristics:
      1. Only allow molecules with C and O atoms (H is implicit).
      2. Must be a single fragment and all atoms must have formal charge zero.
      3. Carbon atoms count must be between 3 and 9.
      4. Count hydroxyl groups using the SMARTS "[OX2H]".
      5. Check for a typical cyclic sugar ring: a 5- or 6-membered ring containing at least one oxygen.
         – If found, require at least 3 hydroxyl groups and an OH/C ratio ≥ 0.5.
      6. If no ring is found, seek an open‐chain carbonyl:
         – For an aldose: a terminal aldehyde pattern "[H]C(=O)" is required and expect roughly (C-1) –OH groups.
         – For a ketose: require an internal carbonyl pattern "C(=O)C" and expect roughly (C-2) –OH groups.
      7. Reject if any extraneous elements (other than C and O) are present.
      8. Reject molecules with any non‐zero formal charge.
      
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classified as a parent monosaccharide, False otherwise.
        str: Reason for the classification decision.
    """
    # Parse SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "SMILES parsing failed"

    # 1. Check connectivity: single fragment only.
    frags = Chem.GetMolFrags(mol, asMols=False)
    if len(frags) > 1:
        return False, "Multiple fragments detected; not a single monosaccharide unit"

    # 2. Check that every atom is either carbon (6) or oxygen (8)
    # and atom formal charge is zero.
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in (6, 8):
            return False, f"Extraneous atom found: {atom.GetSymbol()} (only C and O allowed)"
        if atom.GetFormalCharge() != 0:
            return False, f"Atom {atom.GetSymbol()} has non-zero formal charge"

    # 3. Count carbon atoms.
    atoms = mol.GetAtoms()
    c_count = sum(1 for atom in atoms if atom.GetAtomicNum() == 6)
    if c_count < 3:
        return False, f"Too few carbon atoms ({c_count}); monosaccharides require 3–9 carbons"
    if c_count > 9:
        return False, f"Too many carbon atoms ({c_count}); parent monosaccharides are expected to have 3–9 carbons"
    
    # 4. Count hydroxyl groups using SMARTS "[OX2H]"
    hydroxyl_smarts = Chem.MolFromSmarts("[OX2H]")
    oh_matches = mol.GetSubstructMatches(hydroxyl_smarts)
    num_oh = len(oh_matches)
    oh_ratio = num_oh / c_count

    # 5. Detect a cyclic sugar ring if present.
    ring_found = False
    ring_size = None
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) in (5, 6):
            # Check if there is at least one oxygen in the ring.
            if any(mol.GetAtomWithIdx(idx).GetAtomicNum() == 8 for idx in ring):
                ring_found = True
                ring_size = len(ring)
                break

    # 6. Check for open-chain carbonyl signatures.
    # For terminal aldehyde: pattern "[H]C(=O)"
    aldehyde_smarts = Chem.MolFromSmarts("[H]C(=O)")
    has_terminal_aldehyde = mol.HasSubstructMatch(aldehyde_smarts)
    # For internal ketone: pattern "C(=O)C"
    ketone_smarts = Chem.MolFromSmarts("C(=O)C")
    has_internal_ketone = mol.HasSubstructMatch(ketone_smarts)

    # Decision branch:
    details = f"Carbons: {c_count}, Hydroxyls: {num_oh} (OH/C ratio: {oh_ratio:.2f})"
    if ring_found:
        # With a cyclic structure, expect at least 3 -OH groups and ratio >=0.5.
        if num_oh < 3:
            return False, f"Cyclic {ring_size}-membered sugar ring found but too few –OH groups ({num_oh}); expected at least 3. {details}"
        if oh_ratio < 0.5:
            return False, f"Cyclic sugar ring found but OH/C ratio ({oh_ratio:.2f}) is below 0.5. {details}"
        return True, f"Matches cyclic monosaccharide criteria: {details}. Contains a {ring_size}-membered ring with oxygen."
    else:
        # Open-chain: must contain a carbonyl group.
        if has_terminal_aldehyde:
            # For an aldose, most carbons (except the carbonyl) should be hydroxylated.
            expected_oh = c_count - 1
            if num_oh < expected_oh:
                return False, f"Open-chain aldose (terminal aldehyde detected) but only {num_oh} –OH groups (expected ~{expected_oh}). {details}"
            if oh_ratio < 0.5:
                return False, f"Open-chain aldose detected but OH/C ratio ({oh_ratio:.2f}) is too low. {details}"
            return True, f"Matches open-chain aldose criteria: {details}. Contains a terminal aldehyde."
        elif has_internal_ketone:
            # For a ketose, expect somewhat fewer OH groups (rough heuristic: expected ~C-2).
            expected_oh = c_count - 2
            if num_oh < expected_oh:
                return False, f"Open-chain ketose (internal ketone detected) but only {num_oh} –OH groups (expected ~{expected_oh}). {details}"
            if oh_ratio < 0.5:
                return False, f"Open-chain ketose detected but OH/C ratio ({oh_ratio:.2f}) is too low. {details}"
            return True, f"Matches open-chain ketose criteria: {details}. Contains an internal ketone."
        else:
            return False, "No cyclic sugar ring or recognizable open-chain carbonyl (aldehyde/ketone) detected."

# Example usage for testing
if __name__ == "__main__":
    test_examples = {
        # True positives (monosaccharides)
        "beta-ascarylopyranose": "C[C@@H]1O[C@H](O)[C@H](O)C[C@H]1O",
        "aldehydo-D-fucose": "[H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@@H](C)O",
        "alpha-D-idopyranose": "O1[C@@H]([C@H](O)[C@@H](O)[C@H](O)[C@@H]1O)CO",
        "aldehydo-L-glucose": "[H]C(=O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO",
        "beta-D-gulose": "OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@H]1O",
        "beta-L-sorbofuranose": "OC[C@@H]1O[C@@](O)(CO)[C@@H](O)[C@@H]1O",
        "D-fucopyranose": "C[C@H]1OC(O)[C@H](O)[C@@H](O)[C@H]1O",
        "L-altrofuranose": "O1[C@H]([C@H](O)[C@@H](O)C1O)[C@@H](O)CO",
        "alpha-L-galactose": "OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O",
        "2-dehydro-D-glucopyranose": "OC[C@H]1OC(O)C(=O)[C@@H](O)[C@@H]1O",
        "6-deoxy-beta-L-talopyranose": "O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O)C",
        "L-lyxofuranose": "O1[C@H]([C@@H](O)[C@@H](O)C1O)CO",
        "L-allofuranose": "[H][C@]1(OC(O)[C@@H](O)[C@H]1O)[C@@H](O)CO",
        "beta-D-fructuronic acid": "OC[C@@]1(O)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O",
        "2,3,4,5-tetrahydroxypentanal": "OCC(O)C(O)C(O)C=O",
        "D-galacto-hexodialdose": "O[C@@H](C=O)[C@@H](O)[C@@H](O)[C@H](O)C=O",
        "D-fructofuranuronic acid": "OCC1(O)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O",
        "aldehydo-L-xylose": "[H]C(=O)[C@@H](O)[C@H](O)[C@@H](O)CO",
        "aldehydo-L-iduronic acid": "O[C@@H](C=O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O",
        "D-altro-D-manno-Heptose": "O1C(C(O)C(O)C(O)C1O)C(O)CO",
        "alpha-D-talofuranose": "O1[C@H]([C@H](O)[C@H](O)[C@H]1O)[C@H](O)CO",
        "D-xylulose": "C(O)C(=O)[C@@H](O)[C@H](O)CO",
        "beta-D-glucofuranose": "O1[C@@]([C@H](O)[C@@H](O)[C@@H]1O)([C@H](O)CO)[H]",
        "alpha-D-mannose": "OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O",
        "beta-D-fructopyranose": "OC[C@@]1(O)OC[C@@H](O)[C@@H](O)[C@@H]1O",
        # False positives (should be rejected)
        "Diglycolic acid": "O(CC(O)=O)CC(O)=O",
        "alpha-(hydroxymethyl)serine zwitterion": "C(C([O-])=O)(CO)(CO)[NH3+]"
    }
    for name, smi in test_examples.items():
        result, msg = is_monosaccharide(smi)
        print(f"{name}: {result} | {msg}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35381',
                          'name': 'monosaccharide',
                          'definition': 'Parent monosaccharides are '
                                        'polyhydroxy aldehydes '
                                        'H[CH(OH)]nC(=O)H or polyhydroxy '
                                        'ketones H-[CHOH]n-C(=O)[CHOH]m-H with '
                                        'three or more carbon atoms. The '
                                        "generic term 'monosaccharide' (as "
                                        'opposed to oligosaccharide or '
                                        'polysaccharide) denotes a single '
                                        'unit, without glycosidic connection '
                                        'to other such units. It includes '
                                        'aldoses, dialdoses, aldoketoses, '
                                        'ketoses and diketoses, as well as '
                                        'deoxy sugars, provided that the '
                                        'parent compound has a (potential) '
                                        'carbonyl group.',
                          'parents': ['CHEBI:16646'],
                          'xrefs': ['KEGG:C06698'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 128,
                           'log_lines_of_code': 4.852030263919617,
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
                                                 0,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 2,
                                                 3,
                                                 0,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetMolFrags',
                                                 'GetSymbol',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetSubstructMatches',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'items',
                                                 'GetRingInfo',
                                                 'GetFormalCharge'],
                           'methods_called_count': 13,
                           'smarts_strings': ['C(=O)C', '[OX2H]', '[H]C(=O)'],
                           'smarts_strings_count': 3,
                           'defs': ['is_monosaccharide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "SMILES parsing failed"',
                                          'False, "Multiple fragments '
                                          'detected; not a single '
                                          'monosaccharide unit"',
                                          'False, f"Extraneous atom found: '
                                          '{atom.GetSymbol()} (only C and O '
                                          'allowed)"',
                                          'False, f"Atom {atom.GetSymbol()} '
                                          'has non-zero formal charge"',
                                          'False, f"Too few carbon atoms '
                                          '({c_count}); monosaccharides '
                                          'require 3–9 carbons"',
                                          'False, f"Too many carbon atoms '
                                          '({c_count}); parent monosaccharides '
                                          'are expected to have 3–9 carbons"',
                                          'False, f"Cyclic '
                                          '{ring_size}-membered sugar ring '
                                          'found but too few –OH groups '
                                          '({num_oh}); expected at least 3. '
                                          '{details}"',
                                          'False, f"Cyclic sugar ring found '
                                          'but OH/C ratio ({oh_ratio:.2f}) is '
                                          'below 0.5. {details}"',
                                          'True, f"Matches cyclic '
                                          'monosaccharide criteria: {details}. '
                                          'Contains a {ring_size}-membered '
                                          'ring with oxygen."',
                                          'False, f"Open-chain aldose '
                                          '(terminal aldehyde detected) but '
                                          'only {num_oh} –OH groups (expected '
                                          '~{expected_oh}). {details}"',
                                          'False, f"Open-chain aldose detected '
                                          'but OH/C ratio ({oh_ratio:.2f}) is '
                                          'too low. {details}"',
                                          'True, f"Matches open-chain aldose '
                                          'criteria: {details}. Contains a '
                                          'terminal aldehyde."',
                                          'False, f"Open-chain ketose '
                                          '(internal ketone detected) but only '
                                          '{num_oh} –OH groups (expected '
                                          '~{expected_oh}). {details}"',
                                          'False, f"Open-chain ketose detected '
                                          'but OH/C ratio ({oh_ratio:.2f}) is '
                                          'too low. {details}"',
                                          'True, f"Matches open-chain ketose '
                                          'criteria: {details}. Contains an '
                                          'internal ketone."',
                                          'False, "No cyclic sugar ring or '
                                          'recognizable open-chain carbonyl '
                                          '(aldehyde/ketone) detected."'],
                           'returns_count': 16,
                           'complexity': 7.770406052783923},
    'message': '\n'
               'Attempt failed: F1 score of 0.48868071818891484 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C[C@@H]1O[C@H](O)[C@H](O)C[C@H]1O '
               'NAME: beta-ascarylopyranose REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 3 (ratio '
               '0.50). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@@H](C)O NAME: '
               'aldehydo-D-fucose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 4 (ratio 0.67). Contains an '
               'internal carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@H](O)[C@H]1O)CO NAME: '
               'alpha-D-idopyranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO NAME: '
               'aldehydo-L-glucose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains an '
               'internal carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-D-gulose REASON: CORRECT Matches monosaccharide criteria: '
               'Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a typical '
               'cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1O)COC(=O)CC(O)=O NAME: '
               '3-oxo-3-[(3,4,5,6-tetrahydroxyoxan-2-yl)methoxy]propanoic acid '
               'REASON: CORRECT Matches monosaccharide criteria: Carbons: 9, '
               'Hydroxyls: 5 (ratio 0.56). Contains a typical cyclic sugar '
               'ring (6-membered).\n'
               ' * SMILES: OC[C@@H]1O[C@@](O)(CO)[C@@H](O)[C@@H]1O NAME: '
               'beta-L-sorbofuranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: C[C@H]1OC(O)[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'D-fucopyranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 4 (ratio 0.67). Contains a '
               'typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@@H](O)C1O)[C@@H](O)CO NAME: '
               'L-altrofuranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-L-galactose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: OC[C@H]1OC(O)C(=O)[C@@H](O)[C@@H]1O NAME: '
               '2-dehydro-D-glucopyranose REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 4 (ratio '
               '0.67). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O)C NAME: '
               '6-deoxy-beta-L-talopyranose REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 4 (ratio '
               '0.67). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)C1O)CO NAME: '
               'L-lyxofuranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 5, Hydroxyls: 4 (ratio 0.80). Contains a '
               'typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: [H][C@]1(OC(O)[C@@H](O)[C@H]1O)[C@@H](O)CO NAME: '
               'L-allofuranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: OC[C@@]1(O)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O NAME: '
               'beta-D-fructuronic acid REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: OCC(O)C(O)C(O)C=O NAME: '
               '2,3,4,5-tetrahydroxypentanal REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 5, Hydroxyls: 4 (ratio '
               '0.80). Contains an internal carbonyl indicating an open-chain '
               'ketose.\n'
               ' * SMILES: O[C@@H](C=O)[C@@H](O)[C@@H](O)[C@H](O)C=O NAME: '
               'D-galacto-hexodialdose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 4 (ratio 0.67). Contains an '
               'internal carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: OCC1(O)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O NAME: '
               'D-fructofuranuronic acid REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 5 (ratio '
               '0.83). Contains a typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@H](O)[C@@H](O)CO NAME: '
               'aldehydo-L-xylose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 5, Hydroxyls: 4 (ratio 0.80). Contains an '
               'internal carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: O[C@@H](C=O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O NAME: '
               'aldehydo-L-iduronic acid REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 5 (ratio '
               '0.83). Contains an internal carbonyl indicating an open-chain '
               'ketose.\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1O)C(O)CO NAME: '
               'D-altro-D-manno-Heptose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 7, Hydroxyls: 6 (ratio 0.86). Contains a '
               'typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@H](O)[C@H]1O)[C@H](O)CO NAME: '
               'alpha-D-talofuranose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: C(O)C(=O)[C@@H](O)[C@H](O)CO NAME: D-xylulose '
               'REASON: CORRECT Matches monosaccharide criteria: Carbons: 5, '
               'Hydroxyls: 4 (ratio 0.80). Contains an internal carbonyl '
               'indicating an open-chain ketose.\n'
               ' * SMILES: O1[C@@]([C@H](O)[C@@H](O)[C@@H]1O)([C@H](O)CO)[H] '
               'NAME: beta-D-glucofuranose REASON: CORRECT Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 5 (ratio '
               '0.83). Contains a typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-mannose REASON: CORRECT Matches monosaccharide '
               'criteria: Carbons: 6, Hydroxyls: 5 (ratio 0.83). Contains a '
               'typical cyclic sugar ring (6-membered).\n'
               'False positives: SMILES: O(CC(O)=O)CC(O)=O NAME: Diglycolic '
               'acid REASON: WRONGLY CLASSIFIED Matches monosaccharide '
               'criteria: Carbons: 4, Hydroxyls: 2 (ratio 0.50). Contains an '
               'internal carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: C(C([O-])=O)(CO)(CO)[NH3+] NAME: '
               'alpha-(hydroxymethyl)serine zwitterion REASON: WRONGLY '
               'CLASSIFIED Matches monosaccharide criteria: Carbons: 4, '
               'Hydroxyls: 2 (ratio 0.50). Contains an internal carbonyl '
               'indicating an open-chain ketose.\n'
               ' * SMILES: O[C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O '
               'NAME: beta-D-galacturonate REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 4 (ratio '
               '0.67). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: OC(CC(N)C(O)=O)C(O)=O NAME: '
               '(4R)-4-Hydroxy-L-glutamic acid REASON: WRONGLY CLASSIFIED '
               'Matches monosaccharide criteria: Carbons: 5, Hydroxyls: 3 '
               '(ratio 0.60). Contains an internal carbonyl indicating an '
               'open-chain ketose.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OCC(O)CO)CO NAME: '
               '1-O-(beta-D-glucosyl)glycerol REASON: WRONGLY CLASSIFIED '
               'Matches monosaccharide criteria: Carbons: 9, Hydroxyls: 6 '
               '(ratio 0.67). Contains a typical cyclic sugar ring '
               '(6-membered).\n'
               ' * SMILES: CC(=O)[C@@H](O)[C@H](O)CO NAME: 1-deoxy-D-xylulose '
               'REASON: WRONGLY CLASSIFIED Matches monosaccharide criteria: '
               'Carbons: 5, Hydroxyls: 3 (ratio 0.60). Contains an internal '
               'carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: OC(C(O)CC([H])=O)CO NAME: 2-deoxypentose REASON: '
               'WRONGLY CLASSIFIED Matches monosaccharide criteria: Carbons: '
               '5, Hydroxyls: 3 (ratio 0.60). Contains an internal carbonyl '
               'indicating an open-chain ketose.\n'
               ' * SMILES: [H][C@@]1(OC(=O)[C@@H](O)C1=O)[C@@H](O)CO NAME: '
               'L-xylo-hex-3-ulonolactone REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 3 (ratio '
               '0.50). Contains a typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: '
               'OC[C@@H](O)CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O NAME: '
               '3-O-beta-D-galactopyranosyl-sn-glycerol REASON: WRONGLY '
               'CLASSIFIED Matches monosaccharide criteria: Carbons: 9, '
               'Hydroxyls: 6 (ratio 0.67). Contains a typical cyclic sugar '
               'ring (6-membered).\n'
               ' * SMILES: OC[C@@H](O)[C@H](O)[C@H](O)C(=O)C([O-])=O NAME: '
               '2-dehydro-D-galactonate REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 4 (ratio '
               '0.67). Contains an internal carbonyl indicating an open-chain '
               'ketose.\n'
               ' * SMILES: OC[C@@H]([C@H](C(C([O-])=O)(O)C(=O)[O-])O)O NAME: '
               '2-carboxy-L-lyxonate REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 4 (ratio '
               '0.67). Contains an internal carbonyl indicating an open-chain '
               'ketose.\n'
               ' * SMILES: N[C@H]1O[C@@H](CO)[C@@H](O)[C@H]1O NAME: '
               'beta-L-lyxofuranosylamine REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 5, Hydroxyls: 3 (ratio '
               '0.60). Contains a typical cyclic sugar ring (5-membered).\n'
               ' * SMILES: O[C@@H]1C=C(O)C(=O)[C@H](O)[C@H]1O NAME: '
               '(4R,5S,6R)-2,4,5,6-tetrahydroxycyclohex-2-en-1-one REASON: '
               'WRONGLY CLASSIFIED Matches monosaccharide criteria: Carbons: '
               '6, Hydroxyls: 4 (ratio 0.67). Contains an internal carbonyl '
               'indicating an open-chain ketose.\n'
               ' * SMILES: C(C(C(C(=O)O)([2H])[2H])([2H])[2H])(O)=O NAME: '
               'succinic acid-d4 REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 4, Hydroxyls: 2 (ratio '
               '0.50). Contains an internal carbonyl indicating an open-chain '
               'ketose.\n'
               ' * SMILES: O[C@H](CC(=O)C(O)=O)C(O)=O NAME: '
               'D-4-hydroxy-2-oxoglutaric acid REASON: WRONGLY CLASSIFIED '
               'Matches monosaccharide criteria: Carbons: 5, Hydroxyls: 3 '
               '(ratio 0.60). Contains an internal carbonyl indicating an '
               'open-chain ketose.\n'
               ' * SMILES: CC(=O)N[C@H]1[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O '
               'NAME: N-acetyl-alpha-D-glucosamine REASON: WRONGLY CLASSIFIED '
               'Matches monosaccharide criteria: Carbons: 8, Hydroxyls: 4 '
               '(ratio 0.50). Contains a typical cyclic sugar ring '
               '(6-membered).\n'
               ' * SMILES: OC1O[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)C(O)=O NAME: '
               'D-mannopyranuronic acid REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 5 (ratio '
               '0.83). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](NC(=O)CO)[C@@H](O)[C@@H]1O NAME: '
               'N-glycoloyl-D-glucosamine REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 8, Hydroxyls: 5 (ratio '
               '0.62). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1OC(=O)CC(O)=O)C(O)=O NAME: '
               '6-[(2-carboxyacetyl)oxy]-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Matches monosaccharide '
               'criteria: Carbons: 9, Hydroxyls: 5 (ratio 0.56). Contains a '
               'typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O[C@H]1COC(=O)[C@H](O)[C@H]1O NAME: '
               'L-Arabino-1,5-lactone REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 5, Hydroxyls: 3 (ratio '
               '0.60). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@H]1OCC(O)CO)CO '
               'NAME: isofloridoside REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 9, Hydroxyls: 6 (ratio '
               '0.67). Contains a typical cyclic sugar ring (6-membered).\n'
               ' * SMILES: O/C(/C(O)=O)=C\\O NAME: (2Z)-2,3-dihydroxyacrylic '
               'acid REASON: WRONGLY CLASSIFIED Matches monosaccharide '
               'criteria: Carbons: 3, Hydroxyls: 3 (ratio 1.00). Contains an '
               'internal carbonyl indicating an open-chain ketose.\n'
               ' * SMILES: OC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)C(O)=O NAME: '
               'L-gulonic acid REASON: WRONGLY CLASSIFIED Matches '
               'monosaccharide criteria: Carbons: 6, Hydroxyls: 6 (ratio '
               '1.00). Contains an internal carbonyl indicating an open-chain '
               'ketose.\n'
               ' * SMILES: [NH3+][C@@H]([C@H](O)CO)C([O-])=O NAME: '
               '4-hydroxy-L-threonine zwitterion REASON: WRONGLY CLASSIFIED '
               'Matches monosaccharide criteria: Carbons: 4, Hydroxyls: 2 '
               '(ratio 0.50). Contains an internal carbonyl indicating an '
               'open-chain ketose.\n'
               ' * SMILES: '
               '[C@H]1(O)[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1O[C@@H](C(O)=O)CO '
               'NAME: 2-(beta-D-mannosyl)-D-glyceric acid REASON: WRONGLY '
               'CLASSIFIED Matches monosaccharide criteria: Carbons: 9, '
               'Hydroxyls: 6 (ratio 0.67). Contains a typical cyclic sugar '
               'ring (6-membered).\n'
               'False negatives: SMILES: OC(C(CC([C@H](C)O)=O)=O)=O NAME: '
               '2,4-didehydro-3-deoxy-L-rhamnonic acid REASON: MISSED '
               'Open-chain ketose detected (internal carbonyl) but '
               'insufficient hydroxyl groups (2 vs expected at least 4). '
               'Carbons: 6, Hydroxyls: 2 (ratio 0.33)\n'
               ' * SMILES: '
               'O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)CC1=C(C(=CC=C1C)C)CCC=C(C)C '
               'NAME: Seco-sporulositol REASON: MISSED Too many carbon atoms '
               '(21); parent monosaccharides are expected to have 3–9 carbons\n'
               ' * SMILES: CSCC(=O)[C@H](O)[C@H](O)COP([O-])([O-])=O NAME: '
               '1-(methylthio)ribulose 5-phosphate(2-) REASON: MISSED Contains '
               'extraneous heteroatom S; likely not a parent monosaccharide\n'
               ' * SMILES: '
               'CC1=C(C=CC=C1NC2=C(C=CC=N2)C(=O)O)C(F)(F)F.CNCC(C(C(C(CO)O)O)O)O '
               'NAME: 6-(methylamino)hexane-1,2,3,4,5-pentol '
               '2-[2-methyl-3-(trifluoromethyl)anilino]-3-pyridinecarboxylic '
               'acid REASON: MISSED Multiple fragments detected; likely not a '
               'single monosaccharide unit\n'
               ' * SMILES: '
               'O=C(N[C@H]1C(O)C(O)[C@@H](O[C@@H]([C@H](N)[C@H](O)CO)[C@@H](O)CN)OC1CO)C '
               'NAME: Sorbistin B REASON: MISSED Too many carbon atoms (14); '
               'parent monosaccharides are expected to have 3–9 carbons\n'
               ' * SMILES: '
               'CC1=C(C=C)\\C(NC1=O)=C/c1[nH]c(Cc2[nH]c(\\C=C3NC(=O)C(C=C)=C\\3C)c(C)c2CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)c(CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)c1C '
               'NAME: bis(beta-glucosyluronic acid)bilirubin REASON: MISSED '
               'Too many carbon atoms (45); parent monosaccharides are '
               'expected to have 3–9 carbons\n'
               ' * SMILES: O([C@H]([C@@H](O)CO)[C@H](O)C=O)C NAME: '
               '3-o-methyl-l-xylose REASON: MISSED Open-chain ketose detected '
               '(internal carbonyl) but insufficient hydroxyl groups (3 vs '
               'expected at least 4). Carbons: 6, Hydroxyls: 3 (ratio 0.50)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC\\C=C(/Cl)CC\\C=C/CCCC[C@@H]1OC[C@H](N)[C@@H]1O '
               'NAME: Penasin B REASON: MISSED Too many carbon atoms (30); '
               'parent monosaccharides are expected to have 3–9 carbons\n'
               ' * SMILES: '
               'O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)CC1=C(C[C@H](O)[C@@H]2[C@@]1(CCCC2(C)C)C)C '
               'NAME: Sporulositol B REASON: MISSED Too many carbon atoms '
               '(21); parent monosaccharides are expected to have 3–9 carbons\n'
               ' * SMILES: O=C(N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)OC1)C NAME: '
               '1-deoxy-N-acetylglucosamine REASON: MISSED Ring found but the '
               'hydroxyl/carbon ratio (0.38) is too low; expected ≥ 0.5. '
               'Carbons: 8, Hydroxyls: 3 (ratio 0.38)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Extraneous atom found: N (only '
                                               'C and O allowed)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Atom O has non-zero formal '
                                               'charge'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Extraneous atom found: N (only '
                                               'C and O allowed)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Too many carbon atoms (13); '
                                               'parent monosaccharides are '
                                               'expected to have 3–9 carbons'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Too many carbon atoms (24); '
                                               'parent monosaccharides are '
                                               'expected to have 3–9 carbons'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Too many carbon atoms (28); '
                                               'parent monosaccharides are '
                                               'expected to have 3–9 carbons'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Extraneous atom found: N (only '
                                               'C and O allowed)'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Extraneous atom found: N (only '
                                               'C and O allowed)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Too many carbon atoms (22); '
                                               'parent monosaccharides are '
                                               'expected to have 3–9 carbons'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Too many carbon atoms (67); '
                                               'parent monosaccharides are '
                                               'expected to have 3–9 carbons'}],
    'sample_false_negatives': [   {   'smiles': 'OC(C(CC([C@H](C)O)=O)=O)=O',
                                      'name': '2,4-didehydro-3-deoxy-L-rhamnonic '
                                              'acid',
                                      'reason': 'Open-chain ketose (internal '
                                                'ketone detected) but only 2 '
                                                '–OH groups (expected ~4). '
                                                'Carbons: 6, Hydroxyls: 2 '
                                                '(OH/C ratio: 0.33)'},
                                  {   'smiles': 'O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)CC1=C(C(=CC=C1C)C)CCC=C(C)C',
                                      'name': 'Seco-sporulositol',
                                      'reason': 'Too many carbon atoms (21); '
                                                'parent monosaccharides are '
                                                'expected to have 3–9 carbons'},
                                  {   'smiles': 'CSCC(=O)[C@H](O)[C@H](O)COP([O-])([O-])=O',
                                      'name': '1-(methylthio)ribulose '
                                              '5-phosphate(2-)',
                                      'reason': 'Extraneous atom found: S '
                                                '(only C and O allowed)'},
                                  {   'smiles': 'CC1=C(C=CC=C1NC2=C(C=CC=N2)C(=O)O)C(F)(F)F.CNCC(C(C(C(CO)O)O)O)O',
                                      'name': '6-(methylamino)hexane-1,2,3,4,5-pentol '
                                              '2-[2-methyl-3-(trifluoromethyl)anilino]-3-pyridinecarboxylic '
                                              'acid',
                                      'reason': 'Multiple fragments detected; '
                                                'not a single monosaccharide '
                                                'unit'},
                                  {   'smiles': 'O=C(N[C@H]1C(O)C(O)[C@@H](O[C@@H]([C@H](N)[C@H](O)CO)[C@@H](O)CN)OC1CO)C',
                                      'name': 'Sorbistin B',
                                      'reason': 'Extraneous atom found: N '
                                                '(only C and O allowed)'},
                                  {   'smiles': 'CC1=C(C=C)\\C(NC1=O)=C/c1[nH]c(Cc2[nH]c(\\C=C3NC(=O)C(C=C)=C\\3C)c(C)c2CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)c(CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)c1C',
                                      'name': 'bis(beta-glucosyluronic '
                                              'acid)bilirubin',
                                      'reason': 'Extraneous atom found: N '
                                                '(only C and O allowed)'},
                                  {   'smiles': 'O([C@H]([C@@H](O)CO)[C@H](O)C=O)C',
                                      'name': '3-o-methyl-l-xylose',
                                      'reason': 'Open-chain ketose (internal '
                                                'ketone detected) but only 3 '
                                                '–OH groups (expected ~4). '
                                                'Carbons: 6, Hydroxyls: 3 '
                                                '(OH/C ratio: 0.50)'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC\\C=C(/Cl)CC\\C=C/CCCC[C@@H]1OC[C@H](N)[C@@H]1O',
                                      'name': 'Penasin B',
                                      'reason': 'Extraneous atom found: Cl '
                                                '(only C and O allowed)'},
                                  {   'smiles': 'O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)CC1=C(C[C@H](O)[C@@H]2[C@@]1(CCCC2(C)C)C)C',
                                      'name': 'Sporulositol B',
                                      'reason': 'Too many carbon atoms (21); '
                                                'parent monosaccharides are '
                                                'expected to have 3–9 carbons'},
                                  {   'smiles': 'O=C(N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)OC1)C',
                                      'name': '1-deoxy-N-acetylglucosamine',
                                      'reason': 'Extraneous atom found: N '
                                                '(only C and O allowed)'}],
    'attempt': 3,
    'reasoning': 'Below is our proposed solution. In our reasoning we decided '
                 'to do the following improvements over the previous '
                 'heuristic:\n'
                 '\n'
                 '• Before doing any further work we now insist that the '
                 'molecule consists only of carbon and oxygen atoms (H is '
                 'implicit in SMILES), thereby immediately rejecting cases '
                 'such as amino acids, phosphorylated sugars, or '
                 'sulfur‐containing compounds. (This “allowed elements” check '
                 'correctly removes many false positives.) \n'
                 '\n'
                 '• We also require that all atoms have a formal charge of '
                 'zero (so that deprotonated acids or other charged species '
                 'are rejected).\n'
                 '\n'
                 '• We retain the carbon‐count rule (3–9 carbons) and '
                 '“single‐fragment” rule.\n'
                 '\n'
                 '• For “sugar‐like” molecules we now “branch” into two '
                 'cases:\n'
                 '\n'
                 '\u2003\u2003– If a cyclic sugar ring (5‐ or 6‐membered ring '
                 'containing at least one oxygen) is found we require that '
                 'there be at least three hydroxyl groups and that the ratio '
                 '(number of –OH groups per carbon) is at least 0.5.\n'
                 '\n'
                 '\u2003\u2003– Otherwise (an open‐chain structure) we look '
                 'for a characteristic carbonyl group: either a terminal '
                 'aldehyde ([H]C(=O)) or an internal ketone (using a SMARTS '
                 'such as “C(=O)C”). In the open‐chain case we require that '
                 'the hydroxyl count roughly matches the expected pattern '
                 '(most aldehydes are polyhydroxy “all‐but one” and ketoses '
                 'are “all‐but two”) and that the OH to C ratio (typically ≥ '
                 '0.5) holds.\n'
                 '\n'
                 '• Since many false positives turned out to be molecules that '
                 'met the “OH ratio” even though they were not sugars (or were '
                 'sugar acids with extra –COOH groups), we now also note that '
                 'any deviation (including extra substituents or extra '
                 'heteroatoms) is cause for rejection. \n'
                 '\n'
                 'The code below implements these rules. (If the task is “too '
                 'difficult” one may choose to return (None, None); however, '
                 'we attempt here a best‐effort heuristic.) \n'
                 '\n'
                 'Below is the complete Python code in one code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 306,
    'num_false_positives': 271,
    'num_true_negatives': 141581,
    'num_false_negatives': 142,
    'num_negatives': None,
    'precision': 0.5303292894280762,
    'recall': 0.6830357142857143,
    'f1': 0.5970731707317073,
    'accuracy': 0.9970976809557274,
    'negative_predictive_value': 0.9989980454830902}