"""
Classifies: CHEBI:16701 nucleoside 5'-phosphate
"""
"""
Classifies: Nucleoside 5'-phosphate

Definition: A ribosyl or deoxyribosyl derivative of a pyrimidine or purine base in which
            C-5 of the ribose ring is mono-, di-, tri- or tetra-phosphorylated.
            
Heuristic Approach:
  1. Parse the SMILES and get ring info.
  2. Search for a candidate “sugar” ring. In a nucleoside sugar (ribose or deoxyribose),
     the cyclic (furanose) ring is expected to have 5 atoms, exactly one of which
     is oxygen and the other four carbons.
  3. Verify that at least one atom of that sugar is attached outside the ring to:
       a. a substituent leading to a phosphate group (or a phosphate chain) that is “pure”
          (i.e. all non-connection atoms at the phosphate(s) are oxygen – no extra carbon appendage),
       b. and a nucleobase (i.e. an external aromatic ring that contains at least one nitrogen).
  4. Finally, as a safeguard to weed out large molecules (e.g. CoA derivatives) that merely contain
     a nucleoside 5'-phosphate substructure, we check that the molecular weight is not too high.
     
If all criteria are met then the structure is classified as a nucleoside 5'-phosphate.
If there is an issue with the substructure or the molecule is too large, the function returns False.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_nucleoside_5__phosphate(smiles: str):
    """
    Determines if a molecule is a nucleoside 5'-phosphate from its SMILES string.
    
    A nucleoside 5'-phosphate is defined as a ribosyl or deoxyribosyl derivative of a
    purine or pyrimidine base in which the 5'-position of the sugar is phosphorylated
    (mono-, di-, tri- or tetra-phosphorylated).
    
    We apply the following heuristic tests:
      1. Identify a 5-membered ring with exactly one oxygen and four carbons (a furanose ring).
      2. In that candidate sugar, check for an exocyclic substituent (expected to be the 5'-CH2)
         that is attached via an oxygen to a phosphate group (or chain of phosphate groups).
           • For the attached phosphate, require that every neighbor (other than the linking oxygen)
             is an oxygen or another phosphate (indicating an “unadorned” phosphate chain).
      3. Check that the sugar ring is connected to a nucleobase: at least one sugar atom must have 
         a neighbor (outside the ring) that belongs to an external ring (size>=5) that is aromatic
         and contains at least one nitrogen.
      4. Finally, if the overall molecular weight is unusually high (e.g. >600 Da) we assume this is
         part of a larger molecule rather than a pure nucleoside 5'-phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if molecule is classified as a nucleoside 5'-phosphate, False otherwise.
        str: Reason for classification.
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    ring_info = mol.GetRingInfo()
    
    # Check overall molecular weight: typical nucleoside mono/diphosphates are below ~600 Da.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 600:
        return False, f"Molecular weight too high ({mol_wt:.1f} Da) for a typical nucleoside 5'-phosphate"
    
    sugar_candidate_found = False
    phosphate_attached = False
    nucleobase_attached = False

    # Step 1: find candidate sugar ring (a 5-membered ring with exactly one oxygen and four carbons)
    sugar_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) != 5:
            continue
        oxy_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8)
        c_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
        if oxy_count == 1 and c_count == 4:
            sugar_rings.append(ring)

    if not sugar_rings:
        return False, "No 5-membered ring with 1 oxygen (expected for a ribofuranose) found"
    
    # For each candidate sugar ring, try to verify the required external connections.
    for ring in sugar_rings:
        # Step 2a: Look for a phosphate connection.
        # We expect that one of the sugar atoms is connected (exocyclically) to a CH2 group,
        # which in turn is linked via an oxygen to a phosphate.
        this_ring_has_phosphate = False
        for idx in ring:
            sugar_atom = mol.GetAtomWithIdx(idx)
            for nbr in sugar_atom.GetNeighbors():
                # Consider neighbors outside the ring
                if nbr.GetIdx() in ring:
                    continue
                # Expect a carbon (typically primary CH2) emanating from the sugar
                if nbr.GetAtomicNum() != 6 or nbr.GetHybridization() != Chem.rdchem.HybridizationType.SP3:
                    continue
                # Now check if this exocyclic carbon has a neighbor that is an oxygen attached to a phosphate
                for subnbr in nbr.GetNeighbors():
                    # We want an oxygen that is not the sugar carbon (nbr)
                    if subnbr.GetAtomicNum() != 8:
                        continue
                    # Search neighbors of that oxygen for a phosphorus atom
                    for p_neigh in subnbr.GetNeighbors():
                        if p_neigh.GetAtomicNum() == 15:
                            # Check that—aside from the linking oxygen—every other neighbor of the phosphorus (or chain)
                            # is oxygen or another phosphorus (i.e. no additional carbon, which would indicate an extra
                            # acyl or conjugated group).
                            valid_phosphate = True
                            for pn in p_neigh.GetNeighbors():
                                if pn.GetIdx() == subnbr.GetIdx():
                                    continue
                                if pn.GetAtomicNum() not in (8, 15):
                                    valid_phosphate = False
                                    break
                            if valid_phosphate:
                                this_ring_has_phosphate = True
                                break
                    if this_ring_has_phosphate:
                        break
                if this_ring_has_phosphate:
                    break
            if this_ring_has_phosphate:
                break
        
        # Step 2b: Look for attachment to a nucleobase.
        # We require that at least one atom of the sugar ring is directly connected to an external ring
        # (of size >= 5) that is aromatic and contains at least one nitrogen.
        this_ring_has_base = False
        for idx in ring:
            atom_in_ring = mol.GetAtomWithIdx(idx)
            for nbr in atom_in_ring.GetNeighbors():
                if nbr.GetIdx() in ring:
                    continue
                # For each neighbor outside the sugar, check if it appears in any sufficiently large aromatic ring.
                for other_ring in ring_info.AtomRings():
                    if nbr.GetIdx() in other_ring and len(other_ring) >= 5:
                        # Check all atoms in this ring are aromatic and at least one is a nitrogen.
                        if all(mol.GetAtomWithIdx(a).GetIsAromatic() for a in other_ring) and \
                           any(mol.GetAtomWithIdx(a).GetAtomicNum() == 7 for a in other_ring):
                            this_ring_has_base = True
                            break
                if this_ring_has_base:
                    break
            if this_ring_has_base:
                break
        
        if this_ring_has_phosphate and this_ring_has_base:
            sugar_candidate_found = True
            phosphate_attached = True
            nucleobase_attached = True
            break  # our candidate sugar meets everything

    if not sugar_candidate_found:
        msg = "Did not find a candidate sugar ring with both a terminal phosphate and attached nucleobase"
        if not phosphate_attached:
            msg = "No proper phosphate (or phosphate chain) attached to a sugar exocyclic group was found"
        elif not nucleobase_attached:
            msg = "No nucleobase (aromatic heterocycle with nitrogen) attached to the sugar was found"
        return False, msg

    return True, "Structure contains a nucleoside 5'-phosphate moiety with appropriate sugar, phosphate, and nucleobase"

# Example usage (for testing):
if __name__ == "__main__":
    # A known nucleoside 5'-monophosphate (e.g., adenosine 5'-monophosphate)
    test_smiles = "Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O"
    res, reason = is_nucleoside_5__phosphate(test_smiles)
    print(f"Test AMP: {res} // {reason}")
    
    # A false positive candidate (a CoA derivative fragment - note: simplified SMILES)
    false_smiles = "C[C@H](CCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H](O)[C@@H]1OP(O)(O)=O)"
    res, reason = is_nucleoside_5__phosphate(false_smiles)
    print(f"Test false candidate: {res} // {reason}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16701',
                          'name': "nucleoside 5'-phosphate",
                          'definition': 'A ribosyl or deoxyribosyl derivative '
                                        'of a pyrimidine or purine base in '
                                        'which C-5 of the ribose ring is '
                                        'mono-, di-, tri- or '
                                        'tetra-phosphorylated.',
                          'parents': ['CHEBI:29075'],
                          'xrefs': ['KEGG:C01117'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 129,
                           'log_lines_of_code': 4.859812404361672,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
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
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 7,
                                                 7,
                                                 7,
                                                 8,
                                                 9,
                                                 8,
                                                 9,
                                                 9,
                                                 7,
                                                 8,
                                                 8,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
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
                                                 6,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 0,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 9,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetIsAromatic',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'append',
                                                 'GetRingInfo',
                                                 'GetNeighbors',
                                                 'CalcExactMolWt',
                                                 'AtomRings',
                                                 'GetHybridization'],
                           'methods_called_count': 11,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_nucleoside_5__phosphate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight too high '
                                          '({mol_wt:.1f} Da) for a typical '
                                          'nucleoside 5\'-phosphate"',
                                          'False, "No 5-membered ring with 1 '
                                          'oxygen (expected for a '
                                          'ribofuranose) found"',
                                          'False, msg',
                                          'True, "Structure contains a '
                                          "nucleoside 5'-phosphate moiety with "
                                          'appropriate sugar, phosphate, and '
                                          'nucleobase"'],
                           'returns_count': 5,
                           'complexity': 6.171962480872335},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'C[C@H](CCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#30-CoA(4-) REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CCCCC/C=C\\CCCCCCCC)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (7Z)-hexadecenoyl-CoA REASON: WRONGLY CLASSIFIED '
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               '[C@@H]1(N2C(NC(C=C2)=O)=O)O[C@H]3[C@H]([C@H]1OP([O-])(OC[C@H]4O[C@@H](N5C=CC(NC5=O)=O)[C@@H]([C@@H]4OP([O-])(=O)OC3)O)=O)O '
               "NAME: 2'3'-cyclic di-UMP(2-) REASON: WRONGLY CLASSIFIED "
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CN(C)c1nc(N)c2ncn([C@@H]3O[C@@H]4COP(O)(=O)O[C@H]4[C@H]3O)c2n1 '
               'NAME: 2-(dimethylamino)-cAMP REASON: WRONGLY CLASSIFIED '
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)C/C=C/CCCCCCCCCC)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: (3E)-tetradecenoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bhos#26-CoA REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxo-23,24-bisnorchol-4-en-22-oyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Structure contains a nucleoside '
               "5'-phosphate moiety (sugar-phosphate linkage and nucleobase "
               'detected)\n'
               ' * SMILES: '
               'CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCCCCCCCCC([O-])=O '
               'NAME: tetradecanedioyl-CoA(5-) REASON: WRONGLY CLASSIFIED '
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'C[C@H](CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#10-CoA(4-) REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               'NCCCCCCOP(O)(=O)O[C@@H]1[C@@H](COP(O)(=O)Oc2ccc(C[C@H](N)C(O)=O)cc2)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O '
               "NAME: AcTyr(5'P->O)UpO(CH2)6NH2 REASON: WRONGLY CLASSIFIED "
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: isomyristoyl-CoA REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C/C=C\\C/C=C\\CC1C(CCCC(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O)=O)O1 '
               'NAME: 5,6-epoxy-(8Z,11Z,14Z)-icosatrienoyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Structure contains a nucleoside '
               "5'-phosphate moiety (sugar-phosphate linkage and nucleobase "
               'detected)\n'
               ' * SMILES: '
               '[H]C(CCCC(O)=O)=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 2,3-didehydropimeloyl-CoA REASON: WRONGLY CLASSIFIED '
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bhos#38-CoA(4-) REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: nonadecanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               "Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H]2OP(O)(=O)OC[C@H]2O[C@H]1n1ccc(=O)[nH]c1=O NAME: '
               "3',5'-cyclic UMP REASON: WRONGLY CLASSIFIED Structure contains "
               "a nucleoside 5'-phosphate moiety (sugar-phosphate linkage and "
               'nucleobase detected)\n'
               ' * SMILES: OC[C@H]1O[C@H](C[C@@H]1OP(O)(O)=O)N1C=CC(=O)NC1=O '
               "NAME: 2'-deoxyuridine 3'-monophosphate REASON: WRONGLY "
               "CLASSIFIED Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CC(C)CCCC(C)CCCC(C)CCCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: pristanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(CCCCCCCCCCCCCCC)O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 2-hydroxyheptadecanoyl-CoA(4-) REASON: WRONGLY '
               "CLASSIFIED Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1=CCCCC1O '
               'NAME: 6-hydroxycyclohex-1-ene-1-carbonyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Structure contains a nucleoside '
               "5'-phosphate moiety (sugar-phosphate linkage and nucleobase "
               'detected)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,6Z,9Z,12Z,15Z,18Z,21Z)-tetracosaheptaenoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Structure contains a nucleoside '
               "5'-phosphate moiety (sugar-phosphate linkage and nucleobase "
               'detected)\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#30-CoA REASON: WRONGLY CLASSIFIED Structure '
               "contains a nucleoside 5'-phosphate moiety (sugar-phosphate "
               'linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1C(O)CCCC1O '
               'NAME: 2,6-dihydroxycyclohexane-1-carbonyl-CoA REASON: WRONGLY '
               "CLASSIFIED Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](C)CCC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CCC(C=C7CC[C@]6([C@@]5(CC4)[H])[H])=O)C)[H])C)[H])(C)[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: (25R)-3-oxocholest-4-en-26-oyl-CoA(4-) REASON: WRONGLY '
               "CLASSIFIED Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               ' * SMILES: '
               'CCCCC\\C=C/CC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2-trans,6-cis)-dodeca-2,6-dienoyl-CoA REASON: WRONGLY '
               "CLASSIFIED Structure contains a nucleoside 5'-phosphate moiety "
               '(sugar-phosphate linkage and nucleobase detected)\n'
               'False negatives: SMILES: '
               'N1=C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O NAME: '
               "6-azathymidine 5'-monophosphate REASON: MISSED Molecule does "
               "not contain the expected nucleoside 5'-phosphate substructure\n"
               ' * SMILES: '
               'CN1CN([C@@H]2O[C@H](COP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]2O)c2nc(N)[nH]c(=O)c12 '
               "NAME: 7-methyl-7,8-dihydroguanosine-5'-diphosphate REASON: "
               'MISSED Molecule does not contain the expected nucleoside '
               "5'-phosphate substructure\n"
               ' * SMILES: '
               'O[C@H]1C[C@@H](O[C@@H]1COP(O)(=O)OP(O)(=O)OP(O)(O)=O)N1C=CC(=O)NC1=O '
               'NAME: dUTP REASON: MISSED Molecule does not contain the '
               "expected nucleoside 5'-phosphate substructure\n"
               ' * SMILES: '
               '[C@@H]1(N2C(NC(=O)C(=C2)C(=O)O)=O)O[C@H](COP(O)(=O)O)[C@H](C1)O '
               "NAME: 5-carboxy-2'-deoxyuridine 5'-monophosphate REASON: "
               'MISSED Molecule does not contain the expected nucleoside '
               "5'-phosphate substructure\n"
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)O[C@H]([C@@H]1O)n1cnc2c1nc[nH]c2=O '
               'NAME: ITP REASON: MISSED Molecule does not contain the '
               "expected nucleoside 5'-phosphate substructure\n"
               ' * SMILES: '
               'O[C@H]1C[C@@H](O[C@@H]1COP(O)(=O)OP(O)(=O)OP(O)(O)=O)n1cnc2c1nc[nH]c2=O '
               'NAME: dITP REASON: MISSED Molecule does not contain the '
               "expected nucleoside 5'-phosphate substructure\n"
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC([C@H](CC=4N=CNC4)N)=O)[C@H]3O '
               "NAME: 3'-L-histidyl-AMP REASON: MISSED Molecule does not "
               "contain the expected nucleoside 5'-phosphate substructure\n"
               ' * SMILES: '
               'CNc1ccn([C@@H]2O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]2O)c(=O)n1 '
               "NAME: N(4)-methylcytidine 5'-monophosphate REASON: MISSED "
               "Molecule does not contain the expected nucleoside 5'-phosphate "
               'substructure\n'
               ' * SMILES: '
               'Cc1nc2n(C)c3n(cnc3c(=O)n2c1CC[C@H](N)C(O)=O)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               "NAME: 7-(3-amino-3-carboxypropyl)wyosine 5'-monophosphate "
               'REASON: MISSED Molecule does not contain the expected '
               "nucleoside 5'-phosphate substructure\n"
               ' * SMILES: '
               'CNc1ccccc1C(=O)O[C@@H]1[C@@H](COP(O)(=O)OP(O)(O)=O)O[C@H]([C@@H]1O)n1cnc2c(N)ncnc12 '
               "NAME: 3'-O-(N-methylanthraniloyl)adenosine 5'-diphosphate "
               'REASON: MISSED Molecule does not contain the expected '
               "nucleoside 5'-phosphate substructure\n"
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]12CCC3=C(C(=O)C[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC(=C)C(C)C)[C@@]1(C)CCC(=O)[C@H]2C',
                                     'name': 'Camphoratin H',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'OC1CC=2C(C3C(C4C(C(CC4)C(C)/C=C\\C(C)C)(CC3)C)CC2)(CC1)C',
                                     'name': '(3beta,22E)-26,27-Dinorergosta-5,22-dien-3-ol',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'COc1ccc(cc1)[C@@H]1CC(=O)c2c(O)c(C)c(O)c(C)c2O1',
                                     'name': 'matteucinol',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](C)C(O)=O)[C@@H](N)C(C)C',
                                     'name': 'Val-Trp-Ala',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCC[C@@H](O)CC(O)=O)[C@H](O)C[C@H]1OC(=O)c1c[nH]c2ccccc12',
                                     'name': 'ibho#18',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecular weight too high '
                                               '(1113.4 Da) for a typical '
                                               "nucleoside 5'-phosphate"},
                                 {   'smiles': 'OC=1C=2N=C(C=CC2C=CC1)C',
                                     'name': '2-Methylquinolin-8-ol',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'O([C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)CO)[C@@H]3C[C@@H](NC(=O)C)C(O[C@@H]3CO)O',
                                     'name': 'N-[(3R,5R,6R)-5-[(2R,3R,4S,5R,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-2-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'},
                                 {   'smiles': 'O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@@H]2[C@@H](NC(=O)C)C(O[C@@H]([C@@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)O)[C@@H]1O)CO[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)CO)[C@H](O)[C@H]7NC(=O)C)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R)-5-Acetamido-4-[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-3,6-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecular weight too high '
                                               '(1665.6 Da) for a typical '
                                               "nucleoside 5'-phosphate"},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCSC)CC=1C=2C(NC1)=CC=CC2)C(O)=O)C',
                                     'name': 'Met-Trp-Met',
                                     'reason': 'No 5-membered ring with 1 '
                                               'oxygen (expected for a '
                                               'ribofuranose) found'}],
    'sample_false_negatives': [   {   'smiles': 'CN1CN([C@@H]2O[C@H](COP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]2O)c2nc(N)[nH]c(=O)c12',
                                      'name': "7-methyl-7,8-dihydroguanosine-5'-diphosphate",
                                      'reason': 'No proper phosphate (or '
                                                'phosphate chain) attached to '
                                                'a sugar exocyclic group was '
                                                'found'},
                                  {   'smiles': 'C[N+]1=CN([C@@H]2O[C@H](COP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)N3C=NC4=C3N=CN=C4N)[C@@H](O)[C@H]2O)C2=C1C(=O)NC(N)=N2',
                                      'name': 'N(7)-methyl-GpppA',
                                      'reason': 'Molecular weight too high '
                                                '(787.1 Da) for a typical '
                                                "nucleoside 5'-phosphate"},
                                  {   'smiles': 'C(CCCCCCCCCCCCCCCCC1=CC=C(C=C1)O)(=O)OP(OC[C@H]2O[C@@H](N3C=4N=CN=C(N)C4N=C3)[C@@H]([C@@H]2O)O)(=O)O',
                                      'name': '17-(4-hydroxyphenyl)heptadecanoyl-AMP',
                                      'reason': 'Molecular weight too high '
                                                '(691.3 Da) for a typical '
                                                "nucleoside 5'-phosphate"},
                                  {   'smiles': 'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)O[Al-](F)(F)(F)F)[C@@H](O)[C@H]1O',
                                      'name': 'GDP-tetrafluoroaluminate',
                                      'reason': 'Invalid SMILES string'},
                                  {   'smiles': 'O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c2[nH]c(=O)[nH]c3=O)O[C@H]([C@@H]1O)n1cnc2c1[nH]c(=O)[nH]c2=O',
                                      'name': "P(1),P(4)-bis(5'-xanthosyl) "
                                              'tetraphosphate',
                                      'reason': 'Molecular weight too high '
                                                '(870.0 Da) for a typical '
                                                "nucleoside 5'-phosphate"},
                                  {   'smiles': 'C12=NC(NC(C1=NC=3C(N2C[C@@H]([C@@H]([C@@H](COP(=O)(O)O)O)O)O)=CC(=C(C3)C)C)=O)=O',
                                      'name': 'FMN',
                                      'reason': 'No 5-membered ring with 1 '
                                                'oxygen (expected for a '
                                                'ribofuranose) found'},
                                  {   'smiles': 'C12C(C3(C1N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N',
                                      'name': 'dCMP-dTMP',
                                      'reason': 'Molecular weight too high '
                                                '(629.1 Da) for a typical '
                                                "nucleoside 5'-phosphate"},
                                  {   'smiles': 'C(N1C=2C(=NC3=C1C=C(C(=C3)C)N)C(NC(N2)=O)=O)[C@H](O)[C@H](O)[C@H](O)COP(O)(=O)O',
                                      'name': '8-amino-8-demethylriboflavin '
                                              "5'-phosphate",
                                      'reason': 'No 5-membered ring with 1 '
                                                'oxygen (expected for a '
                                                'ribofuranose) found'},
                                  {   'smiles': 'C1(NC(=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(OP(=O)(OP(=O)(O)O)O)O)[C@@H](O)[C@H]3OC(C=4C=CC=CC4NC)=O)N)=O',
                                      'name': "2'-MANT-GTP",
                                      'reason': 'Molecular weight too high '
                                                '(656.0 Da) for a typical '
                                                "nucleoside 5'-phosphate"},
                                  {   'smiles': 'C12N(C(NC(C1(C)C3(C2N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)=O)=O)[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O',
                                      'name': "thymidine 5'-monophosphate "
                                              'dimer',
                                      'reason': 'Molecular weight too high '
                                                '(644.1 Da) for a typical '
                                                "nucleoside 5'-phosphate"}],
    'attempt': 1,
    'reasoning': 'We can think of the problem as “finding the needle in a '
                 'haystack”: many large molecules (for example, coenzyme A '
                 'derivatives) contain a nucleoside‐5′‐phosphate '
                 '“substructure” even though they are not themselves '
                 'nucleosides. In our previous attempt the code looked at any '
                 'phosphate attached to a sugar ring and any nearby aromatic '
                 'heterocycle. This (1) flagged many CoA‐like compounds that '
                 'have extra “appendages” attached and (2) sometimes missed a '
                 'nucleoside\u20055′‐phosphate because the sugar ring isn’t '
                 'identified in the expected way.\n'
                 '\n'
                 'One idea to improve the code is first to focus on the sugar '
                 'ring, looking for a 5‐membered “furanose” ring. In a '
                 'nucleoside the furanose ring should have exactly one oxygen '
                 '(in the ring) and four carbons. (In ribose the five “ring” '
                 'atoms are O4′, C1′, C2′, C3′ and C4′—with the 5′‐CH2OH '
                 'outside the ring.) Then we can check two things:\n'
                 ' \n'
                 ' • One of the “sugar” atoms should have an exocyclic '
                 'substituent that leads to a phosphate (or chain of '
                 'phosphates) and that phosphate “branch” must not have any '
                 'additional carbon attachments (which would suggest a fatty '
                 'acyl or other non‐nucleoside moiety). \n'
                 ' • At least one sugar atom should be connected (outside the '
                 'sugar ring) to an aromatic heterocycle that contains at '
                 'least one nitrogen (the nucleobase).\n'
                 '\n'
                 'Finally, if the molecule is much larger than “typical” '
                 'nucleosides (for example, if the molecular weight exceeds '
                 'about 600\u2005Da) we assume that the nucleoside '
                 '5′‐phosphate is only a substructure in a much larger '
                 'molecule and thus we do not classify it as the entity in '
                 'question.\n'
                 '\n'
                 'The code below uses these heuristics. (Keep in mind that '
                 'these tests are “soft” and work by heuristic patterns; small '
                 'variations in structure may still be missed or falsely '
                 'flagged.) \n'
                 '\n'
                 'Below is the full code in one Python code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 141,
    'num_false_positives': 690,
    'num_true_negatives': 141444,
    'num_false_negatives': 25,
    'num_negatives': None,
    'precision': 0.16967509025270758,
    'recall': 0.8493975903614458,
    'f1': 0.2828485456369107,
    'accuracy': 0.994975404075896,
    'negative_predictive_value': 0.99982328283935}