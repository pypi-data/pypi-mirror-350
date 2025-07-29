"""
Classifies: CHEBI:33447 phospho sugar
"""
"""
Classifies: phospho sugar – any monosaccharide (or nucleoside) containing an alcoholic –OH 
esterified with phosphoric acid.

Definition: The molecule must contain at least one candidate sugar ring (a 5-membered ring 
with exactly 4 carbons and 1 oxygen, or a 6-membered ring with 5 carbons and 1 oxygen) 
and at least one phosphate group (a phosphorus atom having at least one double-bonded oxygen) 
that is linked via a single-bonded oxygen to a carbon directly in, or immediately adjacent 
to, such a ring.
"""

from rdkit import Chem

def is_phospho_sugar(smiles: str):
    """
    Determines if a molecule is a phospho sugar based on its SMILES string.
    
    The detection process is as follows:
      1. Identify candidate sugar rings from ring information. A candidate sugar ring is:
           - Either 5-membered (furanose: 4 carbons and 1 oxygen) or 6-membered (pyranose:
             5 carbons and 1 oxygen).
           - The ring should not contain phosphorus.
      2. Identify phosphate groups:
           - Look for phosphorus atoms (atomic number 15) with at least one double‐bonded oxygen.
      3. For each phosphate group, look at all oxygen substituents attached via a single bond.
         Then for each such oxygen, check its non–phosphorus neighbor carbons. If one of these
         carbons is either part of a candidate sugar ring or is directly attached (neighbor) to an 
         atom in a candidate sugar ring, the molecule is classified as a phospho sugar.
    
    Args:
        smiles (str): SMILES string representing the molecule.
    
    Returns:
        bool: True if the molecule is classified as a phospho sugar, False otherwise.
        str: Explanation for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # STEP 1: Identify candidate sugar rings based on ring size and atomic composition.
    candidate_sugar_rings = []  # list of sets, each set is the atom indices in a qualifying ring
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        size = len(ring)
        if size not in (5, 6):
            continue
        count_O = 0
        count_C = 0
        contains_P = False
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            num = atom.GetAtomicNum()
            if num == 8:
                count_O += 1
            elif num == 6:
                count_C += 1
            elif num == 15:
                contains_P = True
            # We ignore other atoms for simplicity.
        # For a furanose: expect size==5 with 1 oxygen and 4 carbons.
        # For a pyranose: expect size==6 with 1 oxygen and 5 carbons.
        if contains_P:
            continue
        if size == 5 and count_O == 1 and count_C == 4:
            candidate_sugar_rings.append(set(ring))
        elif size == 6 and count_O == 1 and count_C == 5:
            candidate_sugar_rings.append(set(ring))
            
    if not candidate_sugar_rings:
        return False, "No candidate sugar ring (5- or 6-membered with expected C/O count) found"
    
    # STEP 2: Identify phosphate groups: phosphorus with at least one double-bonded oxygen.
    phosphate_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 15:
            continue
        has_double_O = False
        for nb in atom.GetNeighbors():
            if nb.GetAtomicNum() == 8:
                bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nb.GetIdx())
                if bond is not None and bond.GetBondType() == Chem.BondType.DOUBLE:
                    has_double_O = True
                    break
        if has_double_O:
            phosphate_atoms.append(atom)
    
    if not phosphate_atoms:
        return False, "No phosphate group (P with at least one double-bonded O) found"
    
    # STEP 3: For each phosphate group, check its oxygen substituents (via a single bond)
    # to see if they attach to a carbon that is part of, or directly adjacent to, a candidate sugar ring.
    for p_atom in phosphate_atoms:
        for o_atom in p_atom.GetNeighbors():
            if o_atom.GetAtomicNum() != 8:
                continue  # Must be oxygen
            bond = mol.GetBondBetweenAtoms(p_atom.GetIdx(), o_atom.GetIdx())
            if bond is None or bond.GetBondType() != Chem.BondType.SINGLE:
                continue
            # For the oxygen attached via a single bond, inspect its other neighbors.
            for neighbor in o_atom.GetNeighbors():
                if neighbor.GetIdx() == p_atom.GetIdx():
                    continue
                # Look for a carbon neighbor
                if neighbor.GetAtomicNum() == 6:
                    carbon_idx = neighbor.GetIdx()
                    # Check if this carbon is directly in any candidate sugar ring
                    in_ring = any(carbon_idx in ring for ring in candidate_sugar_rings)
                    # OR check if any neighbor of this carbon is in a candidate sugar ring
                    adjacent_to_ring = any(any(nb.GetIdx() in ring for ring in candidate_sugar_rings)
                                            for nb in neighbor.GetNeighbors())
                    if in_ring or adjacent_to_ring:
                        return True, ("Found candidate sugar ring (or its immediate substituent) "
                                      "and a phosphate group attached via an alcoholic O to a sugar-derived C")
    
    return False, "No alcoholic –OH on a candidate sugar ring (or immediate substituent) found that is esterified to a phosphate"

# For testing the function (executed when the module is run as a script)
if __name__ == "__main__":
    test_examples = [
        # True positives:
        ("P(OCC1O[C@H](O)C(O)C(O)C1O)(O)(O)=O", "alpha-D-Hexose 6-phosphate"),
        ("Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)nc1N", "2'-deoxy-5-methyl-5'-cytidylic acid"),
        ("[C@@H]1O[C@H](OP(O)(O)=O)[C@H](O)[C@@H]1O", "alpha-L-fucose 1-phosphate"),
        ("C1[C@H]2[C@@H]([C@@H]([C@H](O2)N3C4=C(C(=NC=N4)N)N=C3SC5=CC=C(C=C5)Cl)O)OP(=O)(O1)O", 
         "False positive example (should not be classified)"),
    ]
    
    for smi, name in test_examples:
        classified, reason = is_phospho_sugar(smi)
        print(f"Name: {name}\nSMILES: {smi}\nClassified as phospho sugar? {classified}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33447',
                          'name': 'phospho sugar',
                          'definition': 'Any monosaccharide containing an '
                                        'alcoholic hydroxy group esterified '
                                        'with phosphoric acid.',
                          'parents': ['CHEBI:26816', 'CHEBI:63367'],
                          'xrefs': ['KEGG:C00934', 'PMID:18186488'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 104,
                           'log_lines_of_code': 4.6443908991413725,
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
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
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
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'GetAtoms',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetBondType',
                                                 'GetRingInfo'],
                           'methods_called_count': 11,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_phospho_sugar(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No candidate sugar ring (5- '
                                          'or 6-membered with expected C/O '
                                          'count) found"',
                                          'False, "No phosphate group (P with '
                                          'at least one double-bonded O) '
                                          'found"',
                                          'True, ("Found candidate sugar ring '
                                          '(or its immediate substituent) "',
                                          'False, "No alcoholic –OH on a '
                                          'candidate sugar ring (or immediate '
                                          'substituent) found that is '
                                          'esterified to a phosphate"'],
                           'returns_count': 5,
                           'complexity': 5.528878179828274},
    'message': '\n'
               'Attempt failed: F1 score of 0.07889546351084813 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@@H]1O[C@@H](OP(O)(O)=O)[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-L-fucose 1-phosphate REASON: CORRECT Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'Nc1nc2n(ccc2c(=O)[nH]1)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: 7-deaza-cGMP REASON: CORRECT Found candidate sugar ring '
               '(size 5 or 6 with expected C/O count) and a phosphate group '
               'attached via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](CO)[C@@H](OP(O)(O)=O)[C@H]1O '
               "NAME: guanosine 3'-monophosphate REASON: CORRECT Found "
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP(O)(=O)OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: D-mannosyl undecaprenyl phosphate REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: P(OC1OC(C(O)C1O)COP(O)(O)=O)(OP(O)(O)=O)(O)=O NAME: '
               '5-phospho-d-ribose 1-diphosphate REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'OCC1(OP(O)(O)=O)O[C@H](COP(O)(O)=O)[C@@H](O)[C@@H]1O NAME: '
               'D-fructofuranose 2,6-bisphosphate REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O[C@H]2O[C@H](COP(O)(=O)O[C@H]3OC[C@@H](O)[C@H](O)[C@H]3O)[C@@H](O)[C@H](O)[C@@H]2O)[C@@H]1O '
               'NAME: '
               '3-O-(6-O-alpha-D-xylosylphospho-alpha-D-mannopyranosyl)-alpha-D-mannopyranose '
               'REASON: CORRECT Found candidate sugar ring (size 5 or 6 with '
               'expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: C[C@H]1O[C@H](OP(O)(O)=O)[C@H](O)[C@@H]1O NAME: '
               '5-deoxy-alpha-D-ribose 1-phosphate REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'Nc1ncnc2n([C@@H]3O[C@@H]4COP(O)(=O)O[C@H]4[C@H]3O)c(Sc3ccc(Cl)cc3)nc12 '
               'NAME: 8-(4-chlorophenylthio)-cAMP REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: OC[C@H]1O[C@H](C[C@@H]1OP(O)(O)=O)N1C=CC(=O)NC1=O '
               "NAME: 2'-deoxyuridine 3'-monophosphate REASON: CORRECT Found "
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O)[C@H](O[C@@H]1COP(O)(O)=O)OP(O)(O)=O NAME: '
               'alpha-D-ribose 1,5-bisphosphate REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1OP(O)(O)=O '
               'NAME: N-acetyl-beta-D-glucosamine 1-phosphate REASON: CORRECT '
               'Found candidate sugar ring (size 5 or 6 with expected C/O '
               'count) and a phosphate group attached via an alcoholic O '
               'leading to a ring C\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O)C(O[C@@H]1COP(O)(O)=O)OP(O)(=O)OP(O)(O)=O '
               'NAME: 5-O-phosphono-D-ribofuranosyl diphosphate REASON: '
               'CORRECT Found candidate sugar ring (size 5 or 6 with expected '
               'C/O count) and a phosphate group attached via an alcoholic O '
               'leading to a ring C\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OS(O)(=O)=O)[C@@H](OP(O)(O)=O)[C@H]1O '
               "NAME: 3'-phospho-5'-adenylyl sulfate REASON: CORRECT Found "
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](O)C(O[C@@H]([C@H]1O)C(O)=O)OP(O)(O)=O NAME: '
               'D-glucuronic acid 1-phosphate REASON: CORRECT Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)O[Se](O)(=O)=O)[C@@H](OP(O)(O)=O)[C@H]1O '
               "NAME: 3'-phosphoadenylyl selenate REASON: CORRECT Found "
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CC(C)C[C@H](NP(O)(=O)O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O '
               'NAME: phosphoramidon REASON: CORRECT Found candidate sugar '
               'ring (size 5 or 6 with expected C/O count) and a phosphate '
               'group attached via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](O)[C@H](O[C@@H]([C@@H]1O)C(O)=O)OP(O)(O)=O '
               'NAME: 1-phospho-alpha-D-galacturonic acid REASON: CORRECT '
               'Found candidate sugar ring (size 5 or 6 with expected C/O '
               'count) and a phosphate group attached via an alcoholic O '
               'leading to a ring C\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OP(O)(O)=O '
               'NAME: N-acetyl-beta-D-galactosamine 1-phosphate REASON: '
               'CORRECT Found candidate sugar ring (size 5 or 6 with expected '
               'C/O count) and a phosphate group attached via an alcoholic O '
               'leading to a ring C\n'
               ' * SMILES: '
               'OC[C@@H]1O[C@@H](OP(O)(O)=O)[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-L-galactose 1-phosphate REASON: CORRECT Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(O)(=O)O[C@@H]3[C@@H](COP(O)(=O)O[C@H]2[C@H]1O)O[C@H]([C@@H]3O)n1cnc2c(N)ncnc12 '
               'NAME: cyclic di-AMP REASON: CORRECT Found candidate sugar ring '
               '(size 5 or 6 with expected C/O count) and a phosphate group '
               'attached via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'NCCCCCCNc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: N(6)-(6-aminohexyl)-cAMP REASON: CORRECT Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'NCCCCCCNc1nc(N)c2ncn([C@@H]3O[C@@H]4COP(O)(=O)O[C@H]4[C@H]3O)c2n1 '
               'NAME: 2-(6-aminohexylamino)-cAMP REASON: CORRECT Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC[C@H](C)CCCOP(O)(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: beta-D-mannosyl (4S)-4-methylheptacosyl phosphate '
               'REASON: CORRECT Found candidate sugar ring (size 5 or 6 with '
               'expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: O[C@H]1COC(OP(O)(O)=O)[C@H](O)[C@H]1O NAME: '
               'L-arabinose 1-phosphate REASON: CORRECT Found candidate sugar '
               'ring (size 5 or 6 with expected C/O count) and a phosphate '
               'group attached via an alcoholic O leading to a ring C\n'
               'False positives: SMILES: '
               'C1[C@H]2[C@@H]([C@@H]([C@H](O2)N3C4=C(C(=NC=N4)N)N=C3SC5=CC=C(C=C5)Cl)O)OP(=O)(O1)O '
               'NAME: '
               '(4aS,6S,7S,7aR)-6-[6-amino-8-[(4-chlorophenyl)thio]-9-purinyl]-2-hydroxy-2-oxo-4a,6,7,7a-tetrahydro-4H-furo[3,2-d][1,3,2]dioxaphosphorin-7-ol '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (9Z,12Z,15Z,18Z,21Z)-3-oxotetracosapentaenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'CCCC\\C=C/CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: cis-3-octenoyl-CoA REASON: WRONGLY CLASSIFIED Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@H](O[C@H](CO)[C@]2([H])O[C@@H](OC[C@@H](O)[C@]3([H])O[C@@H](O[C@H](CO)[C@]4([H])O[C@@H](OC[C@@H](O)[C@]5([H])O[C@@H](O[C@H](CO)[C@]6([H])O[C@@H](OC[C@@H](O)[C@]7([H])O[C@@H](O[C@H](CO)[C@]8([H])O[C@@H](OC[C@@H](O)[C@]9([H])O[C@@H](O[C@H](CO)[C@]%10([H])O[C@@H](OC[C@@H](O)[C@]%11([H])O[C@@H](O[C@H](CO)[C@]%12([H])O[C@@H](OC[C@@H](O)[C@]%13([H])O[C@@H](O[C@H](CO)[C@]%14([H])O[C@@H](OC[C@@H](O)[C@]%15([H])O[C@@H](O[C@H](CO)[C@]%16([H])O[C@@H](OC[C@@H](O)[C@]%17([H])O[C@@H](O[C@H](CO)[C@]%18([H])O[C@@H](OC[C@@H](O)[C@]%19([H])O[C@@H](O[C@H](CO)[C@]%20([H])O[C@@H](OC[C@@H](O)[C@]%21([H])O[C@@H](O[C@H](CO)[C@]%22([H])O[C@@H](OC[C@@H](O)[C@]%23([H])O[C@@H](O[C@H](CO)[C@]%24([H])O[C@@H](OC[C@@H](O)[C@]%25([H])O[C@@H](O[C@H](CO)[C@]%26([H])O[C@@H](OC[C@@H](O)[C@]%27([H])O[C@@H](O[C@H](CO)[C@]%28([H])O[C@@H](OC[C@@H](O)[C@]%29([H])O[C@@H](O[C@H](CO)[C@]%30([H])O[C@@H](O[C@H]%31[C@H](C)O[C@@H](O[C@H]%32[C@H](O)[C@@H](CO)O[C@H](OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CCC=C(C)C)[C@@H]%32NC(C)=O)[C@H](O)[C@@H]%31O)[C@H](O)[C@H]%30O)[C@H](O)[C@H]%29O)[C@H](O)[C@H]%28O)[C@H](O)[C@H]%27O)[C@H](O)[C@H]%26O)[C@H](O)[C@H]%25O)[C@H](O)[C@H]%24O)[C@H](O)[C@H]%23O)[C@H](O)[C@H]%22O)[C@H](O)[C@H]%21O)[C@H](O)[C@H]%20O)[C@H](O)[C@H]%19O)[C@H](O)[C@H]%18O)[C@H](O)[C@H]%17O)[C@H](O)[C@H]%16O)[C@H](O)[C@H]%15O)[C@H](O)[C@H]%14O)[C@H](O)[C@H]%13O)[C@H](O)[C@H]%12O)[C@H](O)[C@H]%11O)[C@H](O)[C@H]%10O)[C@H](O)[C@H]9O)[C@H](O)[C@H]8O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)CO '
               'NAME: '
               '[beta-D-Galf-(1->5)-beta-D-Galf-(1->6)]14-beta-D-Galf-(1->5)-beta-D-Galf-(1->4)-alpha-L-Rhap-(1->3)-alpha-D-GlcpNAc-1-diphospho-trans,octacis-decaprenol '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#34-CoA REASON: WRONGLY CLASSIFIED Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'C[C@@H]1[C@H](CC2(C([C@@H](C(O2)[C@@H](C[C@H]([C@@H](C)[C@H]([C@@H](C)C=C(C)C(=CC=CC(=CC#N)C)C)O)O)OC)OP(=O)(O)O)(C)C)O[C@@H]1CC=CC3=COC(=N3)[C@H](C)CCNC(=O)[C@@H]([C@@H]([C@@H](COC)N(C)C)O)O)O '
               'NAME: '
               '[(3S,7R,8R,9S)-2-[(1R,3R,4R,5S,6S)-14-cyano-3,5-dihydroxy-1-methoxy-4,6,8,9,13-pentamethyltetradeca-7,9,11,13-tetraenyl]-7-[3-[2-[(2R)-4-[[(2R,3R,4R)-4-(dimethylamino)-2,3-dihydroxy-5-methoxy-1-oxopentyl]amino]butan-2-yl]-4-oxazolyl]prop-2-enyl]-9-hydroxy-4,4,8-trimethyl-1,6-dioxaspiro[4.5]decan-3-yl] '
               'dihydrogen phosphate REASON: WRONGLY CLASSIFIED Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z)-eicosenoyl-CoA REASON: WRONGLY CLASSIFIED Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'C[C@@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@H](O)[C@H]1O '
               'NAME: dTDP-L-rhamnose REASON: WRONGLY CLASSIFIED Found '
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (3R,17Z,20Z,23Z,26Z)-3-hydroxydotriacontatetraenoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               '[C@@H]1(N2C(NC(=O)C(=C2)C)=O)O[C@H](COP(OP(O[C@H]3O[C@@H]([C@H](CC3)[NH2+]C)C)(=O)[O-])(=O)[O-])[C@H](C1)O '
               'NAME: '
               'dTDP-4-(methylammonio)-2,3,4,6-tetradeoxy-alpha-D-glucose(1-) '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP([O-])(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: trans,octacis-decaprenylphospho-beta-D-ribofuranose(1-) '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               '[C@@]1([C@@H]([C@@H](COC(C)=O)O)O)([C@H](NC(=O)C)[C@@H](O)C[C@](O1)(C([O-])=O)OP(=O)([O-])OC[C@H]2O[C@@H](N3C(N=C(C=C3)N)=O)[C@@H]([C@@H]2O)O)[H] '
               'NAME: CMP-N-beta-acetyl-9-O-acetylneuraminate(2-) REASON: '
               'WRONGLY CLASSIFIED Found candidate sugar ring (size 5 or 6 '
               'with expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@H](O[C@H]2[C@H](C)O[C@@H](O[C@H]3[C@H](O)[C@@H](CO)O[C@H](OP([O-])(=O)OP([O-])(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CCC=C(C)C)[C@@H]3NC(C)=O)[C@H](O)[C@@H]2O)[C@H](O)[C@H]1O)[C@H](O)CO '
               'NAME: '
               'beta-D-Galf-(1->4)-alpha-L-Rhap-(1->3)-alpha-D-GlcpNAc-1-diphospho-trans,octacis-decaprenol(2-) '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'OC[C@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: UDP-D-glucose REASON: WRONGLY CLASSIFIED Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'C=1N(C(NC(C1)=O)=O)[C@@H]2O[C@@H]([C@H]([C@H]2O)O)COP(OP(O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)COS(=O)(=O)O)OS(=O)(=O)O)O)NC(=O)C)(=O)O)(=O)O '
               'NAME: UDP-N-acetyl-alpha-D-galactosamine 4,6-bissulfate '
               'REASON: WRONGLY CLASSIFIED Found candidate sugar ring (size 5 '
               'or 6 with expected C/O count) and a phosphate group attached '
               'via an alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'C(\\CC)=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C/C(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O '
               'NAME: (2E,5Z,8Z,11Z,14Z,17Z)-icosahexaenoyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Found candidate sugar ring (size 5 or 6 '
               'with expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z,14Z,17Z,20Z)-hexacosatetraenoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Found candidate sugar ring (size 5 or 6 with '
               'expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bhos#20-CoA REASON: WRONGLY CLASSIFIED Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'C[C@@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](NC(C)=O)[C@H](O)[C@@H]1O '
               'NAME: UDP-2-acetamido-2,6-dideoxy-beta-L-talose REASON: '
               'WRONGLY CLASSIFIED Found candidate sugar ring (size 5 or 6 '
               'with expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bhos#24-CoA REASON: WRONGLY CLASSIFIED Found candidate '
               'sugar ring (size 5 or 6 with expected C/O count) and a '
               'phosphate group attached via an alcoholic O leading to a ring '
               'C\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (3R,13Z)-3-hydroxyicosenoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Found candidate sugar ring (size 5 or 6 with '
               'expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC([C@H](CC)C)=O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (S)-2-methylbutanoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Found candidate sugar ring (size 5 or 6 with expected C/O '
               'count) and a phosphate group attached via an alcoholic O '
               'leading to a ring C\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCSC(=O)C(\\S)=C\\CC(O)=O '
               'NAME: (2Z)-4-carboxy-2-sulfanylbut-2-enoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Found candidate sugar ring (size 5 or 6 with '
               'expected C/O count) and a phosphate group attached via an '
               'alcoholic O leading to a ring C\n'
               ' * SMILES: '
               'Nc1ccn([C@@H]2O[C@@H]3COP([O-])(=O)O[C@H]3[C@H]2O)c(=O)n1 '
               "NAME: 3',5'-cyclic CMP(1-) REASON: WRONGLY CLASSIFIED Found "
               'candidate sugar ring (size 5 or 6 with expected C/O count) and '
               'a phosphate group attached via an alcoholic O leading to a '
               'ring C\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z)-3-oxodocosenoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Found candidate sugar ring (size 5 or 6 with expected C/O '
               'count) and a phosphate group attached via an alcoholic O '
               'leading to a ring C\n'
               'False negatives: SMILES: P(OCC1O[C@H](O)C(O)C(O)C1O)(O)(O)=O '
               'NAME: alpha-D-Hexose 6-phosphate REASON: MISSED No alcoholic '
               '–OH on a candidate sugar ring found that is esterified to a '
               'phosphate\n'
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)nc1N NAME: '
               "2'-deoxy-5-methyl-5'-cytidylic acid REASON: MISSED No "
               'alcoholic –OH on a candidate sugar ring found that is '
               'esterified to a phosphate\n'
               ' * SMILES: '
               '[C@@H]1(N2C=C(C(=N)C=C2)C(O)=O)O[C@H](COP(O)(O)=O)[C@H]([C@H]1O)O '
               "NAME: clitidine 5'-phosphate REASON: MISSED No alcoholic –OH "
               'on a candidate sugar ring found that is esterified to a '
               'phosphate\n'
               ' * SMILES: '
               'Cc1nc2n(C)c3n(cnc3c(=O)n2c1CC(O)[C@H](N)C(O)=O)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: 7-(2-hydroxy-3-amino-3-carboxypropyl)wyosine '
               "5'-monophosphate REASON: MISSED No alcoholic –OH on a "
               'candidate sugar ring found that is esterified to a phosphate\n'
               ' * SMILES: '
               'Nc1nc(=O)[nH]c2n(cnc12)[C@H]1C[C@H](O)[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)O1 '
               'NAME: 2-hydroxy-dATP REASON: MISSED No alcoholic –OH on a '
               'candidate sugar ring found that is esterified to a phosphate\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]1O[C@H](COP(O)(O)=O)C(=O)[C@H]1O NAME: '
               "3'-dehydro-AMP REASON: MISSED No alcoholic –OH on a candidate "
               'sugar ring found that is esterified to a phosphate\n'
               ' * SMILES: '
               'O[C@H](COP(O)(O)=O)[C@H](O)[C@@H](O)C(=O)COP(O)(O)=O NAME: '
               'D-sorbose 1,6-bisphosphate REASON: MISSED No candidate sugar '
               'ring (5- or 6-membered with expected C/O count) found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               'NAME: tetradecanoyl-AMP REASON: MISSED No alcoholic –OH on a '
               'candidate sugar ring found that is esterified to a phosphate\n'
               ' * SMILES: '
               'P(OC[C@@H](O)[C@@H](O)[C@H](O)C(=O)CO)([O-])([O-])=O.[Na+].[Na+] '
               'NAME: D-Fructose 6-Phosphate-Disodium Salt REASON: MISSED No '
               'candidate sugar ring (5- or 6-membered with expected C/O '
               'count) found\n'
               ' * SMILES: '
               'Nc1ncnc2n([C@H]3C[C@H](O)[C@@H](COP(O)(O)=O)O3)c(=O)[nH]c12 '
               'NAME: 8-oxo-dAMP REASON: MISSED No alcoholic –OH on a '
               'candidate sugar ring found that is esterified to a phosphate\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No phosphate group (P with at '
                                               'least one double-bonded O) '
                                               'found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No phosphate group (P with at '
                                               'least one double-bonded O) '
                                               'found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No phosphate group (P with at '
                                               'least one double-bonded O) '
                                               'found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No candidate sugar ring (5- or '
                                               '6-membered with expected C/O '
                                               'count) found'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@H](COP(O)(O)=O)[C@H](O)[C@@H](O)C(=O)COP(O)(O)=O',
                                      'name': 'D-sorbose 1,6-bisphosphate',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': 'P(OC[C@@H](O)[C@@H](O)[C@H](O)C(=O)CO)([O-])([O-])=O.[Na+].[Na+]',
                                      'name': 'D-Fructose 6-Phosphate-Disodium '
                                              'Salt',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': 'OCC(=O)[C@@H](O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                      'name': 'keto-D-fructose 6-phosphate',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': 'P(OC[C@@H](O)[C@@H](O)[C@H](O)C(=O)COP([O-])([O-])=O)(O)([O-])=O.[Na+].[Na+].[Na+]',
                                      'name': 'D-Fructose 1,6-bisphosphate '
                                              'trisodium salt',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': 'C(C([C@H]([C@H]([C@@H](COP(=O)(O)O)O)O)O)=O)OP(=O)(O)O',
                                      'name': 'keto-D-tagatose '
                                              '1,6-bisphosphate',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCCOCC(=O)COP(O)(O)=O',
                                      'name': '1-(9Z,12Z,15Z)-octadecatrienylglycerone '
                                              '3-phosphate',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': 'OCC(=O)[C@H](O)[C@H](O)[C@@H](O)COP(O)(O)=O',
                                      'name': 'keto-L-tagatose 6-phosphate',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': '[H][C@@]1(O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)COP([O-])([O-])=O',
                                      'name': 'D-glycero-alpha-D-manno-heptose '
                                              '7-phosphate(2-)',
                                      'reason': 'No alcoholic –OH on a '
                                                'candidate sugar ring (or '
                                                'immediate substituent) found '
                                                'that is esterified to a '
                                                'phosphate'},
                                  {   'smiles': 'P(OCC(=O)COC(=O)CCCCCCCCC)(O)(O)=O',
                                      'name': 'DHAP(10:0)',
                                      'reason': 'No candidate sugar ring (5- '
                                                'or 6-membered with expected '
                                                'C/O count) found'},
                                  {   'smiles': '[H][C@@]1(O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)COP(O)(O)=O',
                                      'name': 'D-glycero-alpha-D-manno-heptose '
                                              '7-phosphate',
                                      'reason': 'No alcoholic –OH on a '
                                                'candidate sugar ring (or '
                                                'immediate substituent) found '
                                                'that is esterified to a '
                                                'phosphate'}],
    'attempt': 4,
    'reasoning': 'Below is our reasoning before presenting the code.\n'
                 '\n'
                 'We noted that the previous approach encountered many “false '
                 'negatives” because (a) it looked only for sugar rings '
                 'themselves (i.e. atoms formally in the ring) while in many '
                 'phospho sugars the phosphate is attached via an oxygen that '
                 'connects to a sugar‐derived carbon that may not be part of '
                 'the ring but directly linked to it (for example, at the '
                 '“6‑position” of a hexose) and (b) the alcoholic –OH that is '
                 'esterified by phosphoric acid might be on a carbon adjacent '
                 'to a candidate ring. In addition, there were some false '
                 'positives where a phosphate and a sugar ring existed in the '
                 'same molecule but were not connected appropriately. \n'
                 '\n'
                 'To improve this, we now (1) identify candidate sugar rings '
                 'as before (rings of size 5 with 4 carbons and 1 oxygen or '
                 'size 6 with 5 carbons and 1 oxygen, excluding rings that '
                 'contain phosphorus), and then (2) look for phosphate groups '
                 '(phosphorus with at least one double-bonded oxygen '
                 'neighbor). For each phosphate group we check its oxygen '
                 'substituents (those linked to P via a single bond). Then '
                 'rather than insisting that the oxygen’s carbon neighbor be '
                 'in the ring itself, we now check whether that carbon is '
                 'either directly in a candidate sugar ring or is connected '
                 '(by a single bond) to a carbon that is in such a ring. That '
                 'extra “adjacency” step helps correctly classify phospho '
                 'sugars (e.g. hexose 6-phosphates) while hopefully avoiding '
                 'the false positives.\n'
                 '\n'
                 'Below is the complete Python code implementation.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 376,
    'num_false_positives': 3246,
    'num_true_negatives': 138594,
    'num_false_negatives': 84,
    'num_negatives': None,
    'precision': 0.10381004969630038,
    'recall': 0.8173913043478261,
    'f1': 0.1842234198922097,
    'accuracy': 0.9765987350667603,
    'negative_predictive_value': 0.9993942802751699}