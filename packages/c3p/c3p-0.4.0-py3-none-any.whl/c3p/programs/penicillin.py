"""
Classifies: CHEBI:17334 penicillin
"""
#!/usr/bin/env python
"""
Classifies: Penicillins
Definition:
  “Any member of the group of substituted penams containing two methyl substituents at position 2,
   a carboxylate substituent at position 3 and a carboxamido group at position 6.”
   
This implementation first removes potential counterions by selecting the largest fragment,
detects the fused bicyclic penicillin core, and then restricts subgroup searches (for the dimethyl,
carboxylate, and carboxamido groups) to atoms that are part of (or directly attached to) the detected core.
"""

from rdkit import Chem

def is_penicillin(smiles: str):
    """
    Determines if a molecule is a penicillin based on its SMILES string.
    
    A molecule is considered a penicillin if:
      (a) Its largest organic fragment (after salt removal) is neutral.
      (b) It contains a fused bicyclic penicillin core – namely, a 4-membered β‐lactam (with a nitrogen
          and at least one carbonyl) fused to a 5-membered thiazolidine (containing at least one sulfur).
      (c) In that core the carbon adjancent to the sulfur (position 2) bears two methyl substituents.
      (d) A carboxylate substituent (C(=O)O or C(=O)[O-]) is attached to the core.
      (e) A carboxamido fragment (N–C(=O)) is attached to the core.
      
    Args:
        smiles (str): SMILES string of the molecule.
    Returns:
        bool: True if the molecule appears to be a penicillin; False otherwise.
        str: Explanation of the decision.
    """
    # Parse molecule from SMILES and isolate the largest fragment (to remove counterions/salts)
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    if not frags:
        return False, "No fragments found in molecule"
    frag = max(frags, key=lambda m: m.GetNumHeavyAtoms())
    if Chem.GetFormalCharge(frag) != 0:
        return False, "Major fragment is charged (likely a salt) and does not count as a penicillin core"

    # --- Step 1: Identify the fused penicillin core ---
    # We require:
    #   (i) A 4-membered ring (β-lactam) containing at least one N and one C that is double bonded to O.
    #   (ii) A 5-membered ring (thiazolidine) that shares exactly two atoms with the 4-membered ring and has at least one S.
    def get_penicillin_core(mol):
        ring_info = mol.GetRingInfo()
        rings = ring_info.AtomRings()  # each ring is a tuple of atom indices
        for ring4 in rings:
            if len(ring4) != 4:
                continue
            ring4_set = set(ring4)
            atoms4 = [mol.GetAtomWithIdx(i) for i in ring4_set]
            if not any(atom.GetSymbol() == "N" for atom in atoms4):
                continue
            has_carbonyl = False
            for atom in atoms4:
                if atom.GetSymbol() == "C":
                    for bond in atom.GetBonds():
                        if bond.GetBondType().name == "DOUBLE":
                            neigh = bond.GetOtherAtom(atom)
                            if neigh.GetSymbol() == "O":
                                has_carbonyl = True
                                break
                    if has_carbonyl:
                        break
            if not has_carbonyl:
                continue
            # Look for a 5-membered ring sharing exactly 2 atoms with the 4-membered ring and containing S
            for ring5 in rings:
                if len(ring5) != 5:
                    continue
                common = ring4_set.intersection(ring5)
                if len(common) == 2:
                    atoms5 = [mol.GetAtomWithIdx(i) for i in ring5]
                    if any(atom.GetSymbol() == "S" for atom in atoms5):
                        return ring4_set.union(ring5)
        return None

    core_atoms = get_penicillin_core(frag)
    if core_atoms is None:
        return False, "Molecule does not contain the required fused penicillin core (β-lactam fused with thiazolidine containing sulfur)"

    # --- Step 2: Check for two methyl substituents on the carbon adjacent to the core sulfur (position 2) ---
    # For any sulfur within the core, search its neighboring carbon in the core and count methyl groups (CH3) attached,
    # ensuring they lie outside of the core.
    found_dimethyl = False
    for atom in frag.GetAtoms():
        if atom.GetIdx() not in core_atoms:
            continue
        if atom.GetSymbol() != "S":
            continue
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() not in core_atoms or nbr.GetSymbol() != "C":
                continue
            methyl_count = 0
            for sub in nbr.GetNeighbors():
                if sub.GetIdx() in core_atoms:
                    continue
                if sub.GetAtomicNum() == 6 and sub.GetDegree() == 1:
                    methyl_count += 1
            if methyl_count == 2:
                found_dimethyl = True
                break
        if found_dimethyl:
            break
    if not found_dimethyl:
        return False, "Missing two methyl substituents on the core carbon adjacent to the sulfur (position 2)"
    
    # --- Step 3: Check for a carboxylate substituent attached to the core ---
    # Instead of forcing the carboxylate carbon to be a ring atom, we define a more flexible SMARTS:
    # "[CX3](=O)[O,OX1-]" which can match both cyclic and exocyclic carboxylate groups.
    carboxylate_smarts = Chem.MolFromSmarts("[CX3](=O)[O,OX1-]")
    if carboxylate_smarts is None:
        return False, "Error in carboxylate SMARTS"
    carboxylate_found = False
    for match in frag.GetSubstructMatches(carboxylate_smarts):
        # match[0] is the carboxylate carbon; check if it is directly attached to a core atom.
        c_idx = match[0]
        carboxylate_atom = frag.GetAtomWithIdx(c_idx)
        for nbr in carboxylate_atom.GetNeighbors():
            if nbr.GetIdx() in core_atoms:
                carboxylate_found = True
                break
        if carboxylate_found:
            break
    if not carboxylate_found:
        return False, "Missing a carboxylate substituent (C(=O)O or C(=O)[O-]) attached to the penicillin core"

    # --- Step 4: Check for a carboxamido fragment (N–C(=O)) attached to the core ---
    # We use a SMARTS for an amide moiety. The standard fragment "[N;R]-C(=O)" is used, and we require that one atom in the fragment is part of the core.
    carboxamido_smarts = Chem.MolFromSmarts("[N]-C(=O)")
    if carboxamido_smarts is None:
        return False, "Error in carboxamido SMARTS"
    carboxamido_found = False
    for match in frag.GetSubstructMatches(carboxamido_smarts):
        if any(idx in core_atoms for idx in match):
            carboxamido_found = True
            break
    if not carboxamido_found:
        return False, "Missing a carboxamido group (N-C(=O)) attached to the penicillin core"
    
    return True, "Molecule has a fused penicillin core with dimethyl at position 2, a carboxylate at position 3, and a carboxamido at position 6"

# Example usage:
if __name__ == "__main__":
    # Test with Penicillin K SMILES (as one example)
    test_smiles = "CCCCCCCC(=O)N[C@H]1[C@H]2SC(C)(C)[C@@H](N2C1=O)C(O)=O"
    result, reason = is_penicillin(test_smiles)
    print("Is penicillin?", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17334',
                          'name': 'penicillin',
                          'definition': 'Any member of the group of '
                                        'substituted penams containing two '
                                        'methyl substituents at position 2, a '
                                        'carboxylate substituent at position 3 '
                                        'and a carboxamido group at position '
                                        '6.',
                          'parents': ['CHEBI:25865'],
                          'xrefs': [   'KEGG:C00395',
                                       'PMID:11851248',
                                       'PMID:12833570',
                                       'PMID:1502708',
                                       'PMID:16033609',
                                       'PMID:7061385',
                                       'PMID:7798534',
                                       'Wikipedia:Penicillin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 127,
                           'log_lines_of_code': 4.844187086458591,
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
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 8,
                                                 8,
                                                 5,
                                                 6,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 8,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'GetSubstructMatches',
                                                 'GetFormalCharge',
                                                 'intersection',
                                                 'union',
                                                 'GetAtoms',
                                                 'GetSymbol',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'GetBonds',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'GetMolFrags',
                                                 'AtomRings',
                                                 'GetNumHeavyAtoms',
                                                 'GetDegree',
                                                 'GetNeighbors',
                                                 'GetOtherAtom',
                                                 'GetAtomicNum'],
                           'methods_called_count': 20,
                           'smarts_strings': ['[N]-C(=O)', '[CX3](=O)[O,OX1-]'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_penicillin(smiles: str):',
                                       'get_penicillin_core(mol):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No fragments found in '
                                          'molecule"',
                                          'False, "Major fragment is charged '
                                          '(likely a salt) and does not count '
                                          'as a penicillin core"',
                                          'ring4_set.union(ring5)',
                                          'None',
                                          'False, "Molecule does not contain '
                                          'the required fused penicillin core '
                                          '(β-lactam fused with thiazolidine '
                                          'containing sulfur)"',
                                          'False, "Missing two methyl '
                                          'substituents on the core carbon '
                                          'adjacent to the sulfur (position '
                                          '2)"',
                                          'False, "Error in carboxylate '
                                          'SMARTS"',
                                          'False, "Missing a carboxylate '
                                          'substituent (C(=O)O or C(=O)[O-]) '
                                          'attached to the penicillin core"',
                                          'False, "Error in carboxamido '
                                          'SMARTS"',
                                          'False, "Missing a carboxamido group '
                                          '(N-C(=O)) attached to the '
                                          'penicillin core"',
                                          'True, "Molecule has a fused '
                                          'penicillin core with dimethyl at '
                                          'position 2, a carboxylate at '
                                          'position 3, and a carboxamido at '
                                          'position 6"'],
                           'returns_count': 12,
                           'complexity': 9.368837417291719},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCCCCCC(=O)N[C@H]1[C@H]2SC(C)(C)[C@@H](N2C1=O)C(O)=O NAME: '
               'Penicillin K REASON: MISSED Missing a carboxylate substituent '
               '(C(=O)O or C(=O)[O-]) attached to the penicillin core\n'
               ' * SMILES: '
               'CC1(C(N2[C@@H](S1)[C@@H](C2=O)NC(=O)COC3=CC=CC=C3)C(=O)O)C.CC1(C(N2[C@@H](S1)[C@@H](C2=O)NC(=O)COC3=CC=CC=C3)C(=O)O)C.C1=CC=C(C=C1)CNCCNCC2=CC=CC=C2 '
               'NAME: LSM-6045 REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: '
               '[H]C(=N[C@@H]1C(=O)N2[C@@H](C(O)=O)C(C)(C)S[C@]12[H])N1CCCCCC1 '
               'NAME: mecillinam REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: '
               'CC1(C)S[C@@H]2[C@H](NC(=O)Cc3ccc(N)cc3)C(=O)N2[C@H]1C(O)=O '
               'NAME: Penicillin T REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: CC1(C(N2C(S1)C(C2=O)NC(=O)COC3=CC=CC=C3)C(=O)O)C '
               'NAME: '
               '3,3-dimethyl-7-oxo-6-[(1-oxo-2-phenoxyethyl)amino]-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: MISSED Missing a carboxylate substituent (C(=O)O '
               'or C(=O)[O-]) attached to the penicillin core\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(C)onc1-c1ccccc1)C(O)=O '
               'NAME: oxacillin REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)C(c1ccccc1)S(O)(=O)=O)C(O)=O '
               'NAME: sulbenicillin REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(OCC)ccc2ccccc12)C(O)=O '
               'NAME: nafcillin REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C(O)=O '
               'NAME: ampicillin REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N=[N+]=[N-])c1ccccc1)C(O)=O '
               'NAME: azidocillin REASON: MISSED Missing a carboxylate '
               'substituent (C(=O)O or C(=O)[O-]) attached to the penicillin '
               'core\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Molecule does not contain the '
                                               'required fused penicillin core '
                                               '(β-lactam fused with '
                                               'thiazolidine containing '
                                               'sulfur)'}],
    'sample_false_negatives': [   {   'smiles': 'S1(=O)(=O)C(C(C(=O)[O-])C2C1CC2=O)(C)C.S1C(C(C(=O)[O-])N2C1C(NC(=O)C(N)C3=CC=CC=C3)C2=O)(C)C.[Na+].[Na+]',
                                      'name': 'Ampicillin Sodium Mixture With '
                                              'Sulbactam Sodium',
                                      'reason': 'Major fragment is charged '
                                                '(likely a salt) and does not '
                                                'count as a penicillin core'}],
    'attempt': 4,
    'reasoning': 'Below is my reasoning before the code.\n'
                 '\n'
                 'Almost all failures reported were due to our inability to '
                 '“see” a carboxylate substituent on the penicillin core. In '
                 'our previous code the carboxylate group was defined using a '
                 'SMARTS pattern that forced the carbon to be a ring atom '
                 '(i.e. "[#6;R](=O)[O,OX1-]"). However, in many penicillin '
                 'structures the carboxylate (C(=O)O or C(=O)[O‑]) is attached '
                 'exocyclically (i.e. is not in a ring but directly attached '
                 'to a core atom). To fix this we remove the ring restriction '
                 'from the SMARTS and then, for every match we find for the '
                 'carboxylate pattern, we verify if the carboxylate carbon '
                 '(the C of C(=O)[O,OX1-]) is directly attached to an atom '
                 'that belongs to the already‐detected fused penicillin core. '
                 '(We keep the rest of the logic as before.)\n'
                 '\n'
                 'Below is the single Python code block that implements the '
                 'improved version for the penicillin class.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 49,
    'num_false_positives': 22,
    'num_true_negatives': 142228,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.6901408450704225,
    'recall': 0.98,
    'f1': 0.8099173553719008,
    'accuracy': 0.9998383696416022,
    'negative_predictive_value': 0.9999929690850671}