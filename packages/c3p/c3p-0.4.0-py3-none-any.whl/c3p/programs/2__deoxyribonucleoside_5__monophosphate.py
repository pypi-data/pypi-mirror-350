"""
Classifies: CHEBI:18241 2'-deoxyribonucleoside 5'-monophosphate
"""
#!/usr/bin/env python3
"""
Classifies chemical entities of the class 
2'-deoxyribonucleoside 5'-monophosphate.
Definition: A 2'-deoxyribonucleoside monophosphate compound with the phosphate group in the 5'-position.
The improved heuristic:
  (1) The molecule must have exactly one phosphorus (P) and a molecular weight below ~500 Da.
  (2) Identify a candidate furanose sugar ring (a 5-membered ring with exactly 4 C and 1 O).
  (3) Verify that at least one atom of the ring has a branch (directly or via a CH2 group) that leads to an oxygen
      which is attached to a phosphorus atom.
  (4) Confirm that one of the ring atoms is attached (outside the ring) to an aromatic nitrogen (nucleobase).
  (5) Count free –OH groups on ring carbons (excluding any oxygen involved in the phosphate branch);
      for 2'-deoxyribose the count should be exactly one (the 3'-OH).
If all conditions are met for at least one candidate furanose ring, we return True.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_2__deoxyribonucleoside_5__monophosphate(smiles: str):
    """
    Determines if a molecule is a 2'-deoxyribonucleoside 5'-monophosphate based on its SMILES string.
    
    The improved heuristic consists of:
      - Rejecting molecules that do not have exactly one phosphorus atom or have a molecular weight
        outside the expected range for simple nucleotides (< 500 Da).
      - Identifying a candidate furanose ring (5 atoms: 4 C, 1 O).
      - Checking that at least one ring atom has an exocyclic branch that (directly or via a CH2 group)
        leads to an oxygen attached to phosphorus (the phosphate branch).
      - Verifying that one of the ring atoms is attached to an aromatic nitrogen (nucleobase attachment).
      - Counting free hydroxyl (-OH) groups on ring carbons (ignoring oxygens that are part of the phosphate branch)
        and expecting exactly one free -OH (consistent with 2'-deoxyribose).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule fulfills the heuristic, False otherwise.
        str: Explanation of the result.
    """
    # Parse the molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Add explicit hydrogens so that -OH groups are explicit.
    mol = Chem.AddHs(mol)
    
    # Global check: exactly one phosphorus and a typical molecular weight.
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    if p_count != 1:
        return False, f"Molecule has {p_count} phosphorus atoms; expected exactly one for a monophosphate."
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 500:
        return False, f"Molecular weight too high ({mol_wt:.1f} Da) for a simple 2'-deoxyribonucleoside monophosphate."
    
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()  # list of tuples, each tuple is indices of atoms in one ring
    
    # Loop over candidate 5-membered rings.
    for ring in rings:
        if len(ring) != 5:
            continue
            
        # Check ring composition: should have exactly one oxygen and four carbons.
        count_O = 0
        count_C = 0
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            sym = atom.GetSymbol()
            if sym == "O":
                count_O += 1
            elif sym == "C":
                count_C += 1
        if count_O != 1 or count_C != 4:
            continue  # Not a proper candidate furanose ring
        
        candidate_ring = set(ring)
        
        # (1) Check for phosphate branch: Look for a neighbor (or neighbor via a CH2 group)
        # from any ring atom that leads to an oxygen attached to a phosphorus.
        phosphate_attached = False
        for idx in candidate_ring:
            atom = mol.GetAtomWithIdx(idx)
            for nb in atom.GetNeighbors():
                if nb.GetIdx() in candidate_ring:
                    continue
                # Case A: Direct oxygen attachment.
                if nb.GetSymbol() == "O":
                    # Check if this oxygen has a neighbor that is P.
                    for nb2 in nb.GetNeighbors():
                        if nb2.GetIdx() == atom.GetIdx():
                            continue
                        if nb2.GetSymbol() == "P":
                            phosphate_attached = True
                            break
                    if phosphate_attached:
                        break
                # Case B: Attachment via an exocyclic carbon (e.g. CH2 group).
                if nb.GetSymbol() == "C":
                    # Optionally, we might want the exocyclic carbon to have only 1 heavy atom neighbor (a CH2-like pattern).
                    for nb2 in nb.GetNeighbors():
                        if nb2.GetIdx() == atom.GetIdx():
                            continue
                        if nb2.GetSymbol() == "O":
                            for nb3 in nb2.GetNeighbors():
                                if nb3.GetIdx() in (nb.GetIdx(), nb2.GetIdx()):
                                    continue
                                if nb3.GetSymbol() == "P":
                                    phosphate_attached = True
                                    break
                        if phosphate_attached:
                            break
                    if phosphate_attached:
                        break
            if phosphate_attached:
                break
        if not phosphate_attached:
            continue  # This candidate ring does not carry a phosphate branch.
        
        # (2) Check for nucleobase attachment:
        nucleobase_found = False
        for idx in candidate_ring:
            atom = mol.GetAtomWithIdx(idx)
            for nb in atom.GetNeighbors():
                if nb.GetIdx() in candidate_ring:
                    continue
                # If neighbor is nitrogen and aromatic, consider it as part of a nucleobase.
                if nb.GetSymbol() == "N" and nb.GetIsAromatic():
                    nucleobase_found = True
                    break
                # Or if neighbor is a carbon that is part of an aromatic system containing nitrogen.
                if nb.GetSymbol() == "C" and nb.GetIsAromatic():
                    for sub_nb in nb.GetNeighbors():
                        if sub_nb.GetSymbol() == "N" and sub_nb.GetIsAromatic():
                            nucleobase_found = True
                            break
                if nucleobase_found:
                    break
            if nucleobase_found:
                break
        if not nucleobase_found:
            continue  # No clear nucleobase attachment from this ring.
        
        # (3) Count free hydroxyl (-OH) groups on the ring carbons.
        free_oh_count = 0
        for idx in candidate_ring:
            atom = mol.GetAtomWithIdx(idx)
            # Only consider carbons of the sugar ring.
            if atom.GetSymbol() != "C":
                continue
            for nb in atom.GetNeighbors():
                if nb.GetIdx() in candidate_ring:
                    continue
                if nb.GetSymbol() != "O":
                    continue
                # Exclude oxygens that are attached to phosphorus (i.e. part of the phosphate branch).
                if any(nbb.GetSymbol() == "P" for nbb in nb.GetNeighbors()):
                    continue
                # Require that this oxygen has at least one hydrogen (i.e. it is an -OH group).
                if any(nbb.GetSymbol() == "H" for nbb in nb.GetNeighbors()):
                    free_oh_count += 1
        # For a 2'-deoxyribose, we expect exactly one free hydroxyl (located at 3'-position).
        if free_oh_count != 1:
            continue
        
        # If all criteria are met, we have found a valid candidate.
        reason = ("Found candidate furanose ring (4 C, 1 O) with a phosphate branch (directly or via a CH2 group) "
                  "and a nucleobase attachment (aromatic N), and exactly one free -OH on the ring "
                  "(consistent with 2'-deoxyribose).")
        return True, reason

    # If no candidate ring meets our heuristic:
    return False, "Did not detect a valid 2'-deoxyribonucleoside 5'-monophosphate fragment based on the heuristic."

# For testing purposes, run this module to examine some example SMILES.
if __name__ == "__main__":
    test_smiles = [
        # True positives:
        "Nc1nc2n([C@H]3C[C@H](O)[C@@H](COP(O)(O)=O)O3)c(=O)[nH]c2c(=O)[nH]1",  # 8-oxo-dGMP
        "Nc1nc(=O)n(cc1CO)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1",  # 5-hydroxymethyldeoxycytidylic acid
        "Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)([O-])=O)O2)c(=O)[nH]c1=O",  # dTMP(-)
        "O[C@H]1C[C@@H](O[C@@H]1COP(O)(O)=O)n1cc(F)c(=O)[nH]c1=O",  # 5-fluorodeoxyuridine monophosphate
        "Nc1ccn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)n1",  # 2'-deoxycytosine 5'-monophosphate
        "Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(=O)Oc3ccc(cc3)[N+]([O-])=O)O2)c(=O)[nH]c1=O",  # p-nitrophenyl thymidine 5'-monophosphate
        "N1(C2=C(C(N)=NC(=N2)N)N=C1)[C@@H]3O[C@H](COP([O-])([O-])=O)[C@H](C3)O",  # 2-amino-2'-deoxyadenosine 5'-monophosphate(2-)
        "O[C@H]1C[C@@H](O[C@@H]1COP(O)(O)=O)n1ccc(=O)[nH]c1=O",  # dUMP
        "C1(=C(O)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O)O",  # 5,6-dihydroxy-2'-deoxyuridine 5'-monophosphate
        "Nc1ncnc2n(cnc12)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1",  # 2'-deoxyadenosine 5'-monophosphate
        # False positives (should be rejected):
        "S(C(=O)C(CCCC(CCCC(C)C)C)C)CCNC(=O)CCNC(=O)C(O)C(COP(OP(OCC1OC(N2C3=NC=NC(N)=C3N=C2)C(O)C1OP(O)(O)=O)(O)=O)(O)=O)(C)C",  # a long-chain CoA derivative
    ]
    
    for s in test_smiles:
        res, msg = is_2__deoxyribonucleoside_5__monophosphate(s)
        print(f"SMILES: {s}\nResult: {res}\nReason: {msg}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18241',
                          'name': "2'-deoxyribonucleoside 5'-monophosphate",
                          'definition': "A 2'-deoxyribonucleoside "
                                        'monophosphate compound with the '
                                        "phosphate group in the 5'-position.",
                          'parents': ['CHEBI:19257', 'CHEBI:37016'],
                          'xrefs': ['KEGG:C00676', 'KEGG:C03607'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 158,
                           'log_lines_of_code': 5.062595033026967,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
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
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 6,
                                                 7,
                                                 7,
                                                 5,
                                                 6,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 6,
                                                 7,
                                                 8,
                                                 9,
                                                 8,
                                                 9,
                                                 9,
                                                 6,
                                                 7,
                                                 5,
                                                 6,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
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
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
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
                                                 2,
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
                           'max_indent': 9,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetIsAromatic',
                                                 'AddHs',
                                                 'GetRingInfo',
                                                 'GetSymbol',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'AtomRings'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_2__deoxyribonucleoside_5__monophosphate(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecule has {p_count} '
                                          'phosphorus atoms; expected exactly '
                                          'one for a monophosphate."',
                                          'False, f"Molecular weight too high '
                                          '({mol_wt:.1f} Da) for a simple '
                                          "2'-deoxyribonucleoside "
                                          'monophosphate."',
                                          'True, reason',
                                          'False, "Did not detect a valid '
                                          "2'-deoxyribonucleoside "
                                          "5'-monophosphate fragment based on "
                                          'the heuristic."'],
                           'returns_count': 5,
                           'complexity': 6.412519006605393},
    'message': '\n'
               'Attempt failed: F1 score of 0.01866404715127701 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'Nc1nc2n([C@H]3C[C@H](O)[C@@H](COP(O)(O)=O)O3)c(=O)[nH]c2c(=O)[nH]1 '
               'NAME: 8-oxo-dGMP REASON: CORRECT Found candidate furanose ring '
               '(4 C, 1 O) that connects to a phosphate branch (directly or '
               'via a CH2 group) and a nucleobase (via an aromatic N), with '
               'exactly one free -OH on the ring (consistent with '
               "2'-deoxyribose).\n"
               ' * SMILES: '
               'Nc1nc(=O)n(cc1CO)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1 NAME: '
               '5-hydroxymethyldeoxycytidylic acid REASON: CORRECT Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)([O-])=O)O2)c(=O)[nH]c1=O '
               'NAME: dTMP(-) REASON: CORRECT Found candidate furanose ring (4 '
               'C, 1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'O[C@H]1C[C@@H](O[C@@H]1COP(O)(O)=O)n1cc(F)c(=O)[nH]c1=O NAME: '
               '5-fluorodeoxyuridine monophosphate REASON: CORRECT Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: Nc1ccn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)n1 '
               "NAME: 2'-deoxycytosine 5'-monophosphate REASON: CORRECT Found "
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(=O)Oc3ccc(cc3)[N+]([O-])=O)O2)c(=O)[nH]c1=O '
               "NAME: p-nitrophenyl thymidine 5'-monophosphate REASON: CORRECT "
               'Found candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'N1(C2=C(C(N)=NC(=N2)N)N=C1)[C@@H]3O[C@H](COP([O-])([O-])=O)[C@H](C3)O '
               "NAME: 2-amino-2'-deoxyadenosine 5'-monophosphate(2-) REASON: "
               'CORRECT Found candidate furanose ring (4 C, 1 O) that connects '
               'to a phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'O[C@H]1C[C@@H](O[C@@H]1COP(O)(O)=O)n1ccc(=O)[nH]c1=O NAME: '
               'dUMP REASON: CORRECT Found candidate furanose ring (4 C, 1 O) '
               'that connects to a phosphate branch (directly or via a CH2 '
               'group) and a nucleobase (via an aromatic N), with exactly one '
               "free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C1(=C(O)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O)O '
               "NAME: 5,6-dihydroxy-2'-deoxyuridine 5'-monophosphate REASON: "
               'CORRECT Found candidate furanose ring (4 C, 1 O) that connects '
               'to a phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               '[C@@H]1(N2C(NC(=O)C(=C2)C(=O)O)=O)O[C@H](COP(O)(=O)O)[C@H](C1)O '
               "NAME: 5-carboxy-2'-deoxyuridine 5'-monophosphate REASON: "
               'CORRECT Found candidate furanose ring (4 C, 1 O) that connects '
               'to a phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C1=C(CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)C(NC(N1[C@@H]3O[C@H](COP(=O)(O)O)[C@H](C3)O)=O)=O '
               'NAME: (beta-D-glucopyranosyloxymethyl)deoxyuridine '
               "5'-monophosphate REASON: CORRECT Found candidate furanose ring "
               '(4 C, 1 O) that connects to a phosphate branch (directly or '
               'via a CH2 group) and a nucleobase (via an aromatic N), with '
               'exactly one free -OH on the ring (consistent with '
               "2'-deoxyribose).\n"
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)nc1N NAME: '
               "2'-deoxy-5-methyl-5'-cytidylic acid REASON: CORRECT Found "
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Nc1nc(OCc2ccccc2)c2ncn([C@H]3C[C@H](O)[C@@H](COP(O)(O)=O)O3)c2n1 '
               "NAME: 6-O-benzyl-2'-deoxyguanosine 5'-monophosphate REASON: "
               'CORRECT Found candidate furanose ring (4 C, 1 O) that connects '
               'to a phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1 NAME: '
               "2'-deoxyadenosine 5'-monophosphate REASON: CORRECT Found "
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Nc1nc(=O)[nH]c2n(cnc12)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1 '
               'NAME: 2-hydroxy-dAMP REASON: CORRECT Found candidate furanose '
               'ring (4 C, 1 O) that connects to a phosphate branch (directly '
               'or via a CH2 group) and a nucleobase (via an aromatic N), with '
               'exactly one free -OH on the ring (consistent with '
               "2'-deoxyribose).\n"
               ' * SMILES: '
               'NC1=NC=NC2=C1N=NN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](O)C3 NAME: '
               "8-aza-2'-deoxyadenosine 5'-monophosphate REASON: CORRECT Found "
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'N1=C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O NAME: '
               "6-azathymidine 5'-monophosphate REASON: CORRECT Found "
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Cc1cn([C@@H]2C[C@@H](O)[C@H](COP(O)(O)=O)O2)c(=O)[nH]c1=O '
               'NAME: 1-(2-deoxy-5-O-phosphono-beta-L-ribofuranosyl)thymine '
               'REASON: CORRECT Found candidate furanose ring (4 C, 1 O) that '
               'connects to a phosphate branch (directly or via a CH2 group) '
               'and a nucleobase (via an aromatic N), with exactly one free '
               "-OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)[nH]c1=O NAME: '
               'dTMP REASON: CORRECT Found candidate furanose ring (4 C, 1 O) '
               'that connects to a phosphate branch (directly or via a CH2 '
               'group) and a nucleobase (via an aromatic N), with exactly one '
               "free -OH on the ring (consistent with 2'-deoxyribose).\n"
               'False positives: SMILES: '
               'S(C(=O)C(CCCC(CCCC(C)C)C)C)CCNC(=O)CCNC(=O)C(O)C(COP(OP(OCC1OC(N2C3=NC=NC(N)=C3N=C2)C(O)C1OP(O)(O)=O)(O)=O)(O)=O)(C)C '
               'NAME: (2S,6R,10R)-Trimethyl-hendecanoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Found candidate furanose ring (4 C, 1 O) that '
               'connects to a phosphate branch (directly or via a CH2 group) '
               'and a nucleobase (via an aromatic N), with exactly one free '
               "-OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'N(C1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](O)C3)CC(=O)N '
               "NAME: N(6)-carbamoylmethyl-2'-deoxyadenosine 5'-monophosphate "
               'REASON: WRONGLY CLASSIFIED Found candidate furanose ring (4 C, '
               '1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#36-CoA REASON: WRONGLY CLASSIFIED Found candidate '
               'furanose ring (4 C, 1 O) that connects to a phosphate branch '
               '(directly or via a CH2 group) and a nucleobase (via an '
               'aromatic N), with exactly one free -OH on the ring (consistent '
               "with 2'-deoxyribose).\n"
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(N)=NC=N3)N=C2)O[C@@H]([C@H]([C@H]1O)OP(=O)([O-])[O-])COP(O[C@@H]4[C@H](O[C@@H](N5C6=C(C(N)=NC=N6)N=C5)[C@@H]4O)COP(O[C@@H]7[C@H](O[C@@H](N8C9=C(C(=O)NC(=N9)N)N=C8)[C@@H]7O)CO)([O-])=O)(=O)[O-] '
               "NAME: G[3'-5']pA[3'-5']pAp[3'](4-) REASON: WRONGLY CLASSIFIED "
               'Found candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#36-CoA(4-) REASON: WRONGLY CLASSIFIED Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               '[C@H]12N3C=4N=C(NC(C4N=C3[C@H]([C@]([C@H](C1)O)(O2)[H])OP(O)(O)=O)=O)N '
               "NAME: 8,5'-cyclo-2'-deoxyguanosine monophosphate REASON: "
               'WRONGLY CLASSIFIED Found candidate furanose ring (4 C, 1 O) '
               'that connects to a phosphate branch (directly or via a CH2 '
               'group) and a nucleobase (via an aromatic N), with exactly one '
               "free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'NCCCCCCNc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: N(6)-(6-aminohexyl)-cAMP REASON: WRONGLY CLASSIFIED '
               'Found candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#34-CoA REASON: WRONGLY CLASSIFIED Found candidate '
               'furanose ring (4 C, 1 O) that connects to a phosphate branch '
               '(directly or via a CH2 group) and a nucleobase (via an '
               'aromatic N), with exactly one free -OH on the ring (consistent '
               "with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@@H](O)[C@H]1NC(C)=O '
               'NAME: dTDP-4-acetamido-4,6-dideoxy-alpha-D-galactose REASON: '
               'WRONGLY CLASSIFIED Found candidate furanose ring (4 C, 1 O) '
               'that connects to a phosphate branch (directly or via a CH2 '
               'group) and a nucleobase (via an aromatic N), with exactly one '
               "free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H]1OC(OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: dTDP-D-fucose(2-) REASON: WRONGLY CLASSIFIED Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H](CCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#22-CoA(4-) REASON: WRONGLY CLASSIFIED Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](C)[C@@H](CC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CC[C@H](C[C@]7(C[C@H]([C@]6([C@@]5(CC4)[H])[H])O)[H])O)C)[H])C)[H])(C)[H])O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: '
               '(24R,25R)-3alpha,7alpha,24-trihydroxy-5beta-cholestan-26-oyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Found candidate furanose ring (4 C, '
               '1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O '
               "NAME: adenosine 3',5'-bismonophosphate REASON: WRONGLY "
               'CLASSIFIED Found candidate furanose ring (4 C, 1 O) that '
               'connects to a phosphate branch (directly or via a CH2 group) '
               'and a nucleobase (via an aromatic N), with exactly one free '
               "-OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (7Z,10Z,13Z,16Z,19Z)-docosapentaenoyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Found candidate furanose ring (4 C, 1 O) '
               'that connects to a phosphate branch (directly or via a CH2 '
               'group) and a nucleobase (via an aromatic N), with exactly one '
               "free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-undecenoyl-CoA REASON: WRONGLY CLASSIFIED Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(=O)OP(O)(=O)OC3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)C(O)=O)O2)c(=O)[nH]c1=O '
               'NAME: dTDP-D-galacturonic acid REASON: WRONGLY CLASSIFIED '
               'Found candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (18Z,21Z,24Z,27Z,30Z,33Z)-hexatriacontahexaenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Found candidate furanose ring (4 C, '
               '1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC[C@H]1[C@@H]2CCC(=O)[C@@]2(C)CC[C@H]1O '
               'NAME: '
               '3-[(3aS,4S,5R,7aS)-5-hydroxy-7a-methyl-1-oxo-octahydroinden-4-yl]propanoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Found candidate furanose ring (4 C, '
               '1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CC(=O)NCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 4-acetamidobutanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Found candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H](CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#20-CoA REASON: WRONGLY CLASSIFIED Found candidate '
               'furanose ring (4 C, 1 O) that connects to a phosphate branch '
               '(directly or via a CH2 group) and a nucleobase (via an '
               'aromatic N), with exactly one free -OH on the ring (consistent '
               "with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CC(C)CCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxoisooctadecanoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Found candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'O([C@@H]1[C@H](O[C@@H](N2C=3N=CN=C(N)C3N=C2)[C@@H]1O)COP(=O)([O-])[O-])P(OC[C@H]4O[C@@H](N5C=6N=C(NC(=O)C6N=C5)N)[C@@H]([C@@H]4O)O)(=O)[O-] '
               "NAME: 5'-pApG-3'(3-) REASON: WRONGLY CLASSIFIED Found "
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O[C@@H]2O[C@H](COP([O-])([O-])=O)[C@@H](O)[C@H]2O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               "NAME: acetyl-2'-(5''-phosphoribosyl)-3'-dephospho-CoA(4-) "
               'REASON: WRONGLY CLASSIFIED Found candidate furanose ring (4 C, '
               '1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (19Z,22Z,25Z,28Z)-3-oxotetratriacontatetraenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Found candidate furanose ring (4 C, '
               '1 O) that connects to a phosphate branch (directly or via a '
               'CH2 group) and a nucleobase (via an aromatic N), with exactly '
               "one free -OH on the ring (consistent with 2'-deoxyribose).\n"
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#26-CoA(4-) REASON: WRONGLY CLASSIFIED Found '
               'candidate furanose ring (4 C, 1 O) that connects to a '
               'phosphate branch (directly or via a CH2 group) and a '
               'nucleobase (via an aromatic N), with exactly one free -OH on '
               "the ring (consistent with 2'-deoxyribose).\n"
               'False negatives: SMILES: '
               'C12N(C(NC(C1(C)C3(C2N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)=O)=O)[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O '
               "NAME: thymidine 5'-monophosphate dimer REASON: MISSED Did not "
               "detect a 2'-deoxyribonucleoside 5'-monophosphate fragment "
               'based on the heuristic\n'
               ' * SMILES: '
               'C1(C(C(=NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)N)O)O '
               "NAME: 2'-deoxy-5,6-dihydroxy-5,6-dihydrocytidine "
               "5'-monophosphate REASON: MISSED Did not detect a "
               "2'-deoxyribonucleoside 5'-monophosphate fragment based on the "
               'heuristic\n'
               ' * SMILES: '
               'C12C(C3(C1N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N '
               'NAME: dCMP-dTMP REASON: MISSED Did not detect a '
               "2'-deoxyribonucleoside 5'-monophosphate fragment based on the "
               'heuristic\n'
               ' * SMILES: '
               'C1C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O NAME: '
               "5,6-dihydrothymidine 5'-monophosphate REASON: MISSED Did not "
               "detect a 2'-deoxyribonucleoside 5'-monophosphate fragment "
               'based on the heuristic\n'
               ' * SMILES: '
               'C12C(C3C1N(C(N=C3N)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N '
               "NAME: 2'-deoxycytidine 5'-monophosphate dimer REASON: MISSED "
               "Did not detect a 2'-deoxyribonucleoside 5'-monophosphate "
               'fragment based on the heuristic\n'
               ' * SMILES: '
               '[C@@H]1(N2C=C(C(=N)C=C2)C(O)=O)O[C@H](COP(O)(O)=O)[C@H]([C@H]1O)O '
               "NAME: clitidine 5'-phosphate REASON: MISSED Did not detect a "
               "2'-deoxyribonucleoside 5'-monophosphate fragment based on the "
               'heuristic\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Molecule has 0 phosphorus '
                                               'atoms; expected exactly one '
                                               'for a monophosphate.'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Did not detect a valid '
                                               "2'-deoxyribonucleoside "
                                               "5'-monophosphate fragment "
                                               'based on the heuristic.'}],
    'sample_false_negatives': [   {   'smiles': 'C12N(C(NC(C1(C)C3(C2N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)=O)=O)[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O',
                                      'name': "thymidine 5'-monophosphate "
                                              'dimer',
                                      'reason': 'Molecule has 2 phosphorus '
                                                'atoms; expected exactly one '
                                                'for a monophosphate.'},
                                  {   'smiles': 'C1(C(C(=NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)N)O)O',
                                      'name': "2'-deoxy-5,6-dihydroxy-5,6-dihydrocytidine "
                                              "5'-monophosphate",
                                      'reason': 'Did not detect a valid '
                                                "2'-deoxyribonucleoside "
                                                "5'-monophosphate fragment "
                                                'based on the heuristic.'},
                                  {   'smiles': 'C12C(C3(C1N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N',
                                      'name': 'dCMP-dTMP',
                                      'reason': 'Molecule has 2 phosphorus '
                                                'atoms; expected exactly one '
                                                'for a monophosphate.'},
                                  {   'smiles': 'C1=C(CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)C(NC(N1[C@@H]3O[C@H](COP(=O)(O)O)[C@H](C3)O)=O)=O',
                                      'name': '(beta-D-glucopyranosyloxymethyl)deoxyuridine '
                                              "5'-monophosphate",
                                      'reason': 'Molecular weight too high '
                                                '(500.1 Da) for a simple '
                                                "2'-deoxyribonucleoside "
                                                'monophosphate.'},
                                  {   'smiles': 'C1C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O',
                                      'name': '5,6-dihydrothymidine '
                                              "5'-monophosphate",
                                      'reason': 'Did not detect a valid '
                                                "2'-deoxyribonucleoside "
                                                "5'-monophosphate fragment "
                                                'based on the heuristic.'},
                                  {   'smiles': 'C12C(C3C1N(C(N=C3N)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N',
                                      'name': "2'-deoxycytidine "
                                              "5'-monophosphate dimer",
                                      'reason': 'Molecule has 2 phosphorus '
                                                'atoms; expected exactly one '
                                                'for a monophosphate.'},
                                  {   'smiles': '[C@@H]1(N2C=C(C(=N)C=C2)C(O)=O)O[C@H](COP(O)(O)=O)[C@H]([C@H]1O)O',
                                      'name': "clitidine 5'-phosphate",
                                      'reason': 'Did not detect a valid '
                                                "2'-deoxyribonucleoside "
                                                "5'-monophosphate fragment "
                                                'based on the heuristic.'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before presenting the code. In our '
                 'previous attempt the heuristic looked for a five‐membered '
                 'ring with exactly one oxygen and four carbons, looked for an '
                 'exocyclic branch that eventually leads to a phosphate and an '
                 'aromatic nitrogen (to suggest a nucleobase) and then simply '
                 'counted free –OH groups on ring carbons expecting exactly '
                 'one. However, many false positives (for example, CoA '
                 'derivatives or larger molecules) were classified because '
                 'they happen to contain a fragment that meets that '
                 'rudimentary pattern while not being a simple '
                 'deoxyribonucleoside monophosphate. In addition, some true '
                 '2′‐deoxyribonucleotides in dimeric or modified forms were '
                 'being “missed” because the extra fragments caused extra “OH” '
                 'counts or P counts. \n'
                 '\n'
                 'Thus, to improve the heuristic we now add:\n'
                 '\u2002\u2002•\u2003A “global” check that the molecule is '
                 'small enough (molecular weight typically below 500\u2005Da) '
                 'and contains exactly one phosphorus atom (since a '
                 '2′‐deoxyribonucleoside 5′‐monophosphate should have one '
                 'phosphate group). \n'
                 '\u2002\u2002•\u2003Then, we loop over candidate 5‐membered '
                 'rings that contain exactly 4 carbons and 1 oxygen. For each '
                 'candidate ring we check:\n'
                 '\u2002\u2002\u2002\u2002– That one of its atoms (directly or '
                 'via an exocyclic CH2 group) bonds to an oxygen that in turn '
                 'is bonded to a phosphorus.\n'
                 '\u2002\u2002\u2002\u2002– That one of the ring atoms is '
                 'attached (outside the ring) to an aromatic nitrogen (i.e. '
                 'the nucleobase).\n'
                 '\u2002\u2002\u2002\u2002– That exactly one “free” hydroxyl '
                 '(–OH) remains on the ring carbons (i.e. not the oxygen that '
                 'is part of a phosphate branch). \n'
                 'Only if a candidate ring meets all these conditions will we '
                 'return True with a detailed reason. Otherwise, we reject the '
                 'input. \n'
                 '\n'
                 'Below is the complete Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 124,
    'num_true_negatives': 142151,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.1267605633802817,
    'recall': 0.72,
    'f1': 0.2155688622754491,
    'accuracy': 0.9990794096978215,
    'negative_predictive_value': 0.9999507590146175}