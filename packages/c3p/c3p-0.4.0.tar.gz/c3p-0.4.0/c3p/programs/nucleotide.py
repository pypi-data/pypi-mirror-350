"""
Classifies: CHEBI:36976 nucleotide
"""
"""
Classifies: Nucleotide
A nucleotide is defined as a nucleoside phosphate resulting from the condensation 
of the 3 or 5 hydroxy group of a nucleoside with phosphoric acid.

This function checks that:
  - A furanose sugar ring (5-membered ring with exactly 1 oxygen and 4 carbons) is present.
  - The sugar region is expanded with its immediate carbon neighbors (e.g. the exocyclic 5'-CH2 group).
  - A glycosidic bond exists between a carbon atom of the sugar (typically the anomeric carbon) 
    and a nucleobase-like fragment (an aromatic heterocycle carrying at least one nitrogen).
  - A phosphate group is attached to the sugar through an oxygen (i.e. a P atom with an O that connects to the sugar region).
  
If these criteria are met, the molecule is classified as a nucleotide.
"""
from rdkit import Chem

def is_nucleotide(smiles: str):
    """
    Determines if a molecule is a nucleotide based on its SMILES string.
    
    A nucleotide is expected to have:
      • A nucleoside portion: a furanose sugar (and its immediate exocyclic carbons) 
        connected via a glycosidic bond to a nucleobase (an aromatic heterocycle with at least one nitrogen).
      • A phosphate group attached to the sugar via an oxygen bridge.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a nucleotide, False otherwise.
        str: Reason for the classification result.
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo()
    sugar_ring = None
    # Step 1: Identify a furanose ring – a 5-membered ring with exactly 1 oxygen and 4 carbons.
    for ring in ring_info.AtomRings():
        if len(ring) == 5:
            # Count atoms in the ring by element.
            symbols = [mol.GetAtomWithIdx(idx).GetSymbol() for idx in ring]
            if symbols.count("O") == 1 and symbols.count("C") == 4:
                sugar_ring = set(ring)
                break
    if sugar_ring is None:
        return False, "No furanose sugar ring (5-membered ring with 1 oxygen and 4 carbons) found"
    
    # Step 2: Expand sugar region: include immediate carbon neighbors of the sugar ring.
    sugar_region = set(sugar_ring)
    for idx in list(sugar_ring):
        atom = mol.GetAtomWithIdx(idx)
        for nbr in atom.GetNeighbors():
            # Consider adding carbons that lie immediately outside the ring.
            if nbr.GetSymbol() == "C":
                sugar_region.add(nbr.GetIdx())
    
    # Step 3: Identify the glycosidic bond.
    # Look for a bond from a carbon atom in the sugar ring to a nitrogen that belongs to an aromatic ring (nucleobase).
    glycosidic_found = False
    for idx in sugar_ring:
        sugar_atom = mol.GetAtomWithIdx(idx)
        # we expect the connecting atom (anomeric carbon) to be carbon
        if sugar_atom.GetSymbol() != "C":
            continue
        for nbr in sugar_atom.GetNeighbors():
            if nbr.GetIdx() in sugar_region:
                # Skip atoms that are also part of (or immediately attached to) the sugar
                continue
            # We favor a connection to a nitrogen.
            if nbr.GetAtomicNum() == 7 and nbr.GetIsAromatic():
                # Ensure that the neighbor is part of an aromatic ring that is not completely in the sugar region.
                for ring in ring_info.AtomRings():
                    if nbr.GetIdx() in ring and not set(ring).issubset(sugar_region):
                        glycosidic_found = True
                        break
            if glycosidic_found:
                break
        if glycosidic_found:
            break
    if not glycosidic_found:
        return False, ("No glycosidic bond found connecting a sugar carbon to an aromatic heterocycle "
                       "with nitrogen (nucleobase-like component)")
    
    # Step 4: Check for a phosphate group attached to the sugar.
    # We consider a phosphate as a phosphorus atom (atomic number 15) that is connected 
    # via an oxygen to any atom in the sugar region.
    phosphate_found = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 15:  # phosphorus
            for nbr in atom.GetNeighbors():
                if nbr.GetSymbol() == "O":
                    # Check if this oxygen is connected to any atom in the sugar region.
                    for nbr2 in nbr.GetNeighbors():
                        if nbr2.GetIdx() in sugar_region:
                            phosphate_found = True
                            break
                if phosphate_found:
                    break
        if phosphate_found:
            break
    if not phosphate_found:
        return False, "No phosphate group attached to the sugar region via an oxygen bridge"
    
    return True, ("Molecule contains a furanose sugar (with expanded sugar region), a glycosidic bond to a nucleobase-like "
                  "aromatic heterocycle, and a phosphate group attached via oxygen – consistent with a nucleotide")
    
# Example usage (for testing purposes)
if __name__ == "__main__":
    # List a few test examples; note that in practice the full test list is extensive.
    test_examples = [
        "Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)nc1N",  # 2'-deoxy-5-methyl-5'-cytidylic acid (should be True)
        "[C@@H]1(N2C=C(C(=N)C=C2)C(O)=O)O[C@H](COP(O)(O)=O)[C@H]([C@H]1O)O",  # clitidine 5'-phosphate (should be True)
    ]
    for smi in test_examples:
        res, reason = is_nucleotide(smi)
        print(f"SMILES: {smi}\nResult: {res}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36976',
                          'name': 'nucleotide',
                          'definition': 'A nucleotide is a nucleoside '
                                        'phosphate resulting from the '
                                        'condensation of the 3 or 5 hydroxy '
                                        'group of a nucleoside with phosphoric '
                                        'acid.',
                          'parents': ['CHEBI:25608'],
                          'xrefs': ['KEGG:C00215', 'Wikipedia:Nucleotide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 90,
                           'log_lines_of_code': 4.499809670330265,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 4,
                                                 5,
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
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 7,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSymbol',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'GetAtoms',
                                                 'issubset',
                                                 'GetNeighbors',
                                                 'add',
                                                 'GetRingInfo',
                                                 'GetIsAromatic',
                                                 'count'],
                           'methods_called_count': 13,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_nucleotide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No furanose sugar ring '
                                          '(5-membered ring with 1 oxygen and '
                                          '4 carbons) found"',
                                          'False, ("No glycosidic bond found '
                                          'connecting a sugar carbon to an '
                                          'aromatic heterocycle "',
                                          'False, "No phosphate group attached '
                                          'to the sugar region via an oxygen '
                                          'bridge"',
                                          'True, ("Molecule contains a '
                                          'furanose sugar (with expanded sugar '
                                          'region), a glycosidic bond to a '
                                          'nucleobase-like "'],
                           'returns_count': 5,
                           'complexity': 6.099961934066053},
    'message': '\n'
               'Attempt failed: F1 score of 0.18877551020408165 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(O)=O)O2)c(=O)nc1N NAME: '
               "2'-deoxy-5-methyl-5'-cytidylic acid REASON: CORRECT Molecule "
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Cc1nc2n(C)c3n(cnc3c(=O)n2c1CC(O)[C@H](N)C(O)=O)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: 7-(2-hydroxy-3-amino-3-carboxypropyl)wyosine '
               "5'-monophosphate REASON: CORRECT Molecule contains a "
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1nc(=O)[nH]c2n(cnc12)[C@H]1C[C@H](O)[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)O1 '
               'NAME: 2-hydroxy-dATP REASON: CORRECT Molecule contains a '
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CCCC(=O)NC1=NC(=O)C2=C(N1)N(C=N2)C3[C@H]([C@@H]4[C@@H](O3)COP(=O)(O4)O)OC(=O)CCC '
               'NAME: butanoic acid '
               '[(4aS,7S,7aS)-2-hydroxy-2-oxo-6-[6-oxo-2-(1-oxobutylamino)-3H-purin-9-yl]-4a,6,7,7a-tetrahydro-4H-furo[3,2-d][1,3,2]dioxaphosphorin-7-yl] '
               'ester REASON: CORRECT Molecule contains a nucleoside (sugar + '
               'nucleobase) with a phosphate group attached at a sugar hydroxy '
               'group\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]1O[C@H](COP(O)(O)=O)C(=O)[C@H]1O NAME: '
               "3'-dehydro-AMP REASON: CORRECT Molecule contains a nucleoside "
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'Cc1cc2nc3c(nc(=O)[nH]c3=O)n(C[C@H](O)[C@H](O)[C@H](O)COP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c(N)ncnc34)c2cc1C '
               'NAME: FAD REASON: CORRECT Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               'NAME: tetradecanoyl-AMP REASON: CORRECT Molecule contains a '
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1ncnc2n([C@H]3C[C@H](O)[C@@H](COP(O)(O)=O)O3)c(=O)[nH]c12 '
               'NAME: 8-oxo-dAMP REASON: CORRECT Molecule contains a '
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Cn1cnc2n(cnc2c1=N)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               "NAME: N(1)-methyladenosine 5'-monophosphate REASON: CORRECT "
               'Molecule contains a nucleoside (sugar + nucleobase) with a '
               'phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1[n+]2cnc3n(cnc13)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]3O[C@@H]2[C@H](O)[C@@H]3O)[C@@H](O)[C@H]1OP(O)(O)=O '
               "NAME: 2'-phospho-cyclic ADP-ribose REASON: CORRECT Molecule "
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](CO)[C@@H](OP(O)(O)=O)[C@H]1O '
               "NAME: guanosine 3'-monophosphate REASON: CORRECT Molecule "
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)NP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: AMP-PNP REASON: CORRECT Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'Cc1cn2c(nc3n(cnc3c2=O)[C@@H]2O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]2O)[nH]1 '
               "NAME: 4-demethylwyosine 5'-monophosphate REASON: CORRECT "
               'Molecule contains a nucleoside (sugar + nucleobase) with a '
               'phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: GTP REASON: CORRECT Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'C1=C(CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)C(NC(N1[C@@H]3O[C@H](COP(=O)(O)O)[C@H](C3)O)=O)=O '
               'NAME: (beta-D-glucopyranosyloxymethyl)deoxyuridine '
               "5'-monophosphate REASON: CORRECT Molecule contains a "
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Cc1nc2[nH]c3n(cnc3c(=O)n2c1CC[C@H](N)C(O)=O)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: 4-demethyl-7-(3-amino-3-carboxypropyl)wyosine '
               "5'-monophosphate REASON: CORRECT Molecule contains a "
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(O)=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O '
               "NAME: uridine 5'-monophosphate REASON: CORRECT Molecule "
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CC(=O)Nc1ccn([C@@H]2O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]2O)c(=O)n1 '
               "NAME: N(4)-acetylcytidine 5'-monophosphate REASON: CORRECT "
               'Molecule contains a nucleoside (sugar + nucleobase) with a '
               'phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(O)=O)O[C@H]([C@@H]1O)n1cnc2c1nc[nH]c2=O '
               'NAME: IMP REASON: CORRECT Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               "NAME: guanosine 5'-monophosphate REASON: CORRECT Molecule "
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1ncnc2n([C@@H]3O[C@@H]4COP(O)(=O)O[C@H]4[C@H]3O)c(Sc3ccc(Cl)cc3)nc12 '
               'NAME: 8-(4-chlorophenylthio)-cAMP REASON: CORRECT Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Cn1c(N)nc2n(cnc2c1=O)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: N(1)-methyl-cGMP REASON: CORRECT Molecule contains a '
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Cc1ncc(C[n+]2csc(CCOP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c(N)ncnc34)c2C)c(N)n1 '
               'NAME: adenosine thiamine triphosphate REASON: CORRECT Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Cc1cn([C@H]2C[C@@H]3OP(O)(=O)OC[C@H]3O2)c(=O)[nH]c1=O NAME: '
               "3',5'-cyclic dTMP REASON: CORRECT Molecule contains a "
               'nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c2[nH]c(=O)[nH]c3=O)O[C@H]([C@@H]1O)n1cnc2c1[nH]c(=O)[nH]c2=O '
               "NAME: P(1),P(4)-bis(5'-xanthosyl) tetraphosphate REASON: "
               'CORRECT Molecule contains a nucleoside (sugar + nucleobase) '
               'with a phosphate group attached at a sugar hydroxy group\n'
               'False positives: SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (9Z,12Z,15Z,18Z,21Z)-3-oxotetracosapentaenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'CCCC\\C=C/CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: cis-3-octenoyl-CoA REASON: WRONGLY CLASSIFIED Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#34-CoA REASON: WRONGLY CLASSIFIED Molecule contains '
               'a nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z)-eicosenoyl-CoA REASON: WRONGLY CLASSIFIED Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'C[C@@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@H](O)[C@H]1O '
               'NAME: dTDP-L-rhamnose REASON: WRONGLY CLASSIFIED Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (3R,17Z,20Z,23Z,26Z)-3-hydroxydotriacontatetraenoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               '[C@@H]1(N2C(NC(=O)C(=C2)C)=O)O[C@H](COP(OP(O[C@H]3O[C@@H]([C@H](CC3)[NH2+]C)C)(=O)[O-])(=O)[O-])[C@H](C1)O '
               'NAME: '
               'dTDP-4-(methylammonio)-2,3,4,6-tetradeoxy-alpha-D-glucose(1-) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@H](O1)COP([O-])(=O)OP([O-])(OC[C@H]2O[C@H]([C@@H]([C@@H]2O)O)N3C=NC=4C(=NC=NC34)N)=O)O)O)N5C=NC=6C(=NC=NC56)N '
               "NAME: P(1),P(2)-bis(5'-adenosyl) diphosphate(2-) REASON: "
               'WRONGLY CLASSIFIED Molecule contains a nucleoside (sugar + '
               'nucleobase) with a phosphate group attached at a sugar hydroxy '
               'group\n'
               ' * SMILES: '
               '[C@@]1([C@@H]([C@@H](COC(C)=O)O)O)([C@H](NC(=O)C)[C@@H](O)C[C@](O1)(C([O-])=O)OP(=O)([O-])OC[C@H]2O[C@@H](N3C(N=C(C=C3)N)=O)[C@@H]([C@@H]2O)O)[H] '
               'NAME: CMP-N-beta-acetyl-9-O-acetylneuraminate(2-) REASON: '
               'WRONGLY CLASSIFIED Molecule contains a nucleoside (sugar + '
               'nucleobase) with a phosphate group attached at a sugar hydroxy '
               'group\n'
               ' * SMILES: '
               'NC1=C2N=CN([C@@H]3O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]4O[C@@H](O)[C@H](O)[C@@H]4O)[C@@H](O)[C@H]3O)C2=NC=N1 '
               'NAME: ADP-beta-D-ribose REASON: WRONGLY CLASSIFIED Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP([O-])([O-])=O)OC([C@@H]1O)n1cnc(CC([O-])=O)c1 '
               'NAME: [1-(5-phosphonatoribosyl)imidazol-4-yl]acetate(3-) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)O[C@H]([C@@H]1O)n1cnc2c1ncn([C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O)c2=N '
               'NAME: 1-(5-phospho-beta-D-ribosyl)-ATP REASON: WRONGLY '
               'CLASSIFIED Molecule contains a nucleoside (sugar + nucleobase) '
               'with a phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'OC[C@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: UDP-D-glucose REASON: WRONGLY CLASSIFIED Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'C=1N(C(NC(C1)=O)=O)[C@@H]2O[C@@H]([C@H]([C@H]2O)O)COP(OP(O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)COS(=O)(=O)O)OS(=O)(=O)O)O)NC(=O)C)(=O)O)(=O)O '
               'NAME: UDP-N-acetyl-alpha-D-galactosamine 4,6-bissulfate '
               'REASON: WRONGLY CLASSIFIED Molecule contains a nucleoside '
               '(sugar + nucleobase) with a phosphate group attached at a '
               'sugar hydroxy group\n'
               ' * SMILES: '
               'C(\\CC)=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C/C(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O '
               'NAME: (2E,5Z,8Z,11Z,14Z,17Z)-icosahexaenoyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Molecule contains a nucleoside (sugar + '
               'nucleobase) with a phosphate group attached at a sugar hydroxy '
               'group\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z,14Z,17Z,20Z)-hexacosatetraenoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Molecule contains a nucleoside (sugar + nucleobase) '
               'with a phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bhos#20-CoA REASON: WRONGLY CLASSIFIED Molecule contains '
               'a nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'C[C@@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](NC(C)=O)[C@H](O)[C@@H]1O '
               'NAME: UDP-2-acetamido-2,6-dideoxy-beta-L-talose REASON: '
               'WRONGLY CLASSIFIED Molecule contains a nucleoside (sugar + '
               'nucleobase) with a phosphate group attached at a sugar hydroxy '
               'group\n'
               ' * SMILES: '
               'N1(C2=C(C(=NC=N2)N)N=C1)[C@@H]3O[C@H](COP(OP(OC[C@H]4O[C@@H](N5CC(=CC=C5)C(=O)N)[C@@H]([C@@H]4O)O)(=O)[O-])(=O)[O-])[C@H]([C@H]3O)O '
               'NAME: 2-hydro-beta-NAD(2-) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bhos#24-CoA REASON: WRONGLY CLASSIFIED Molecule contains '
               'a nucleoside (sugar + nucleobase) with a phosphate group '
               'attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (3R,13Z)-3-hydroxyicosenoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a nucleoside (sugar + nucleobase) '
               'with a phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC([C@H](CC)C)=O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (S)-2-methylbutanoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Molecule contains a nucleoside (sugar + nucleobase) with a '
               'phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCSC(=O)C(\\S)=C\\CC(O)=O '
               'NAME: (2Z)-4-carboxy-2-sulfanylbut-2-enoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Molecule contains a nucleoside (sugar + nucleobase) '
               'with a phosphate group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'Nc1ccn([C@@H]2O[C@@H]3COP([O-])(=O)O[C@H]3[C@H]2O)c(=O)n1 '
               "NAME: 3',5'-cyclic CMP(1-) REASON: WRONGLY CLASSIFIED Molecule "
               'contains a nucleoside (sugar + nucleobase) with a phosphate '
               'group attached at a sugar hydroxy group\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z)-3-oxodocosenoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a nucleoside (sugar + nucleobase) with a '
               'phosphate group attached at a sugar hydroxy group\n'
               'False negatives: SMILES: '
               '[C@@H]1(N2C=C(C(=N)C=C2)C(O)=O)O[C@H](COP(O)(O)=O)[C@H]([C@H]1O)O '
               "NAME: clitidine 5'-phosphate REASON: MISSED No nucleobase-like "
               'aromatic heterocycle (ring with ≥2 nitrogens attached to '
               'sugar) found\n'
               ' * SMILES: '
               'NC(=O)c1ccc[n+](c1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](OP(O)(O)=O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O '
               'NAME: NADP(+) REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'Nc1nc2n(ccc2c(=O)[nH]1)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: 7-deaza-cGMP REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'NC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O '
               'NAME: NADH REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'CCCc1cc(ccn1)C(=O)[C@H]1C=CN(C=C1C(N)=O)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O '
               'NAME: (4S)-4-(2-propylisonicotinoyl)nicotinamide adenine '
               'dinucleotide REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'NC(=O)C1=CN(C=CC1)[C@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O '
               'NAME: alpha-NADH REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'C1C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O NAME: '
               "5,6-dihydrothymidine 5'-monophosphate REASON: MISSED No "
               'nucleobase-like aromatic heterocycle (ring with ≥2 nitrogens '
               'attached to sugar) found\n'
               ' * SMILES: '
               'NC(=O)c1ccc[n+](c1)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: NMN(+) REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'NC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: NMNH REASON: MISSED No nucleobase-like aromatic '
               'heterocycle (ring with ≥2 nitrogens attached to sugar) found\n'
               ' * SMILES: '
               'CN1CN([C@@H]2O[C@H](COP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]2O)c2nc(N)[nH]c(=O)c12 '
               "NAME: 7-methyl-7,8-dihydroguanosine-5'-diphosphate REASON: "
               'MISSED No nucleobase-like aromatic heterocycle (ring with ≥2 '
               'nitrogens attached to sugar) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No furanose sugar ring '
                                               '(5-membered ring with 1 oxygen '
                                               'and 4 carbons) found'}],
    'sample_false_negatives': [   {   'smiles': 'NC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O',
                                      'name': 'NADH',
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'CCCc1cc(ccn1)C(=O)[C@H]1C=CN(C=C1C(N)=O)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O',
                                      'name': '(4S)-4-(2-propylisonicotinoyl)nicotinamide '
                                              'adenine dinucleotide',
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'NC(=O)C1=CN(C=CC1)[C@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O',
                                      'name': 'alpha-NADH',
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'C1C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O',
                                      'name': '5,6-dihydrothymidine '
                                              "5'-monophosphate",
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'NC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O',
                                      'name': 'NMNH',
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'CN1CN([C@@H]2O[C@H](COP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]2O)c2nc(N)[nH]c(=O)c12',
                                      'name': "7-methyl-7,8-dihydroguanosine-5'-diphosphate",
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'CC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OCC2OC([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O',
                                      'name': 'AcNADH',
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'P(=O)(OC[C@@H](O)[C@@H](O)[C@@H](O)CN1C=2NC(=O)NC(C2[N+]3=CCC(C=4C3=C1C=C(C)C4C)(C)C)=O)(O)O',
                                      'name': 'Prenylated flavin '
                                              'mononucleotide',
                                      'reason': 'No furanose sugar ring '
                                                '(5-membered ring with 1 '
                                                'oxygen and 4 carbons) found'},
                                  {   'smiles': 'C12C(C3(C1N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N',
                                      'name': 'dCMP-dTMP',
                                      'reason': 'No glycosidic bond found '
                                                'connecting a sugar carbon to '
                                                'an aromatic heterocycle with '
                                                'nitrogen (nucleobase-like '
                                                'component)'},
                                  {   'smiles': 'C=12N=C(NC(C1[N+]=3C=4C(N2C[C@@H]([C@@H]([C@@H](COP(O)(O)=O)O)O)O)=CC(=C(C4C(C)(CC3)C)C)C)=O)[O-]',
                                      'name': 'prenyl-FMN',
                                      'reason': 'No furanose sugar ring '
                                                '(5-membered ring with 1 '
                                                'oxygen and 4 carbons) found'}],
    'attempt': 5,
    'reasoning': 'Below is one possible improved approach. In our reasoning we '
                 'noted that the previous version may miss the nucleoside '
                 '“connection” (the glycosidic bond from the anomeric sugar '
                 'carbon to a nitrogen in an aromatic ring) and may be too '
                 'permissive about a general phosphate attached to any '
                 '“sugar‐like” region. In this version we first search for a '
                 'classic furanose ring (a 5‐membered ring with one oxygen and '
                 'four carbons). Then we “expand” the sugar by adding directly '
                 'attached carbons (since many nucleosides include an extra '
                 'CH₂ at the 5′ position). Next, we look specifically for at '
                 'least one bond from a sugar ring carbon (the presumptive '
                 'anomeric carbon) to a nitrogen atom that is aromatic and '
                 'belongs to a ring that is not entirely part of the sugar '
                 'region. Finally, we verify that a phosphate group (a '
                 'phosphorus atom attached via an oxygen) is connected to the '
                 'sugar region. The hope is that these criteria better exclude '
                 'molecules in which a phosphate is attached to a '
                 'non‐nucleoside fragment while recovering nucleotides such as '
                 'clitidine 5′-phosphate. (Of course nucleotides are very '
                 'complex and borderline cases remain.) \n'
                 '\n'
                 'Below is the complete Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 312,
    'num_false_positives': 2513,
    'num_true_negatives': 139447,
    'num_false_negatives': 28,
    'num_negatives': None,
    'precision': 0.1104424778761062,
    'recall': 0.9176470588235294,
    'f1': 0.1971563981042654,
    'accuracy': 0.9821433591004919,
    'negative_predictive_value': 0.9997992471769134}