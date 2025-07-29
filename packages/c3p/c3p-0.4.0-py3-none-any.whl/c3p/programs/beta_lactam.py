"""
Classifies: CHEBI:35627 beta-lactam
"""
"""
Classifies: beta-lactam
A beta-lactam is defined as a lactam (cyclic amide) in which the amide bond is contained within a four-membered ring,
which includes the amide nitrogen and the carbonyl carbon.
This implementation selects the largest fragment from the SMILES (to minimize interference from salts)
and then iterates over all 4-membered rings. For each ring, it checks:
  - the ring has exactly 4 atoms (by definition),
  - the ring has exactly one nitrogen and three carbons,
  - at least one of the carbons has a double bond to oxygen (with the oxygen not being in the ring),
  - and that carbon (the carbonyl carbon) is directly bonded to the nitrogen.
If all these conditions are met, the molecule is classified as a beta-lactam.
"""

from rdkit import Chem

def is_beta_lactam(smiles: str):
    """
    Determines if a molecule is a beta-lactam based on its SMILES string.
    
    The function first sanitizes the molecule, selects the largest fragment, adds explicit hydrogens,
    and then inspects each 4-membered ring. A valid beta-lactam ring must have exactly one nitrogen
    and three carbons, one of which is carbonyl (i.e. double-bonded to an oxygen that is not part of the ring)
    and is directly bonded to that nitrogen.
    
    Args:
        smiles (str): SMILES string representing the molecule.
    
    Returns:
        bool: True if the molecule is classified as a beta-lactam, False otherwise.
        str: A reason supporting the classification decision.
    """
    # Parse the molecule from the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Remove salts/multiple fragments by selecting the largest fragment.
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    if not frags:
        return False, "No fragments could be parsed from the SMILES"
    
    # Choose the fragment with the most heavy atoms
    main_frag = max(frags, key=lambda m: m.GetNumHeavyAtoms())
    
    # Add explicit hydrogens to help with bond perceptions.
    main_frag = Chem.AddHs(main_frag)
    
    # Get ring information for the main fragment
    ring_info = main_frag.GetRingInfo()
    atom_rings = ring_info.AtomRings()  # a tuple of tuples, each inner tuple is a set of atom indices for that ring.
    
    # Loop over all rings in the main fragment.
    for ring in atom_rings:
        if len(ring) != 4:
            continue  # We only care about 4-membered rings.
        
        # Get the atoms of this ring.
        ring_atoms = [main_frag.GetAtomWithIdx(idx) for idx in ring]
        
        # Check composition: A true beta-lactam ring should have exactly 1 nitrogen and 3 carbons.
        num_nitrogen = sum(1 for atom in ring_atoms if atom.GetAtomicNum() == 7)
        num_carbon = sum(1 for atom in ring_atoms if atom.GetAtomicNum() == 6)
        if num_nitrogen != 1 or num_carbon != 3:
            continue  # This ring does not have the correct atom composition
        
        # Identify the nitrogen atom in the ring.
        nitrogen_atom = [atom for atom in ring_atoms if atom.GetAtomicNum() == 7][0]
        
        # Look among the carbons for a carbonyl carbon.
        # A carbonyl carbon is defined here as a carbon that is double-bonded to an oxygen atom,
        # where the oxygen is not part of the 4-membered ring.
        carbonyl_carbon = None
        for atom in ring_atoms:
            if atom.GetAtomicNum() != 6:
                continue  # We are only interested in carbons.
            # Examine each bond from this carbon.
            for nbr in atom.GetNeighbors():
                # Skip if the neighbor is within the ring.
                if nbr.GetIdx() in ring:
                    continue
                if nbr.GetAtomicNum() == 8:  # Oxygen candidate
                    bond = main_frag.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                    # Check if the bond is a double bond.
                    if bond and bond.GetBondType() == Chem.BondType.DOUBLE:
                        carbonyl_carbon = atom
                        break
            if carbonyl_carbon:
                break
        
        if not carbonyl_carbon:
            continue  # No carbonyl carbon found in this ring
        
        # Ensure the carbonyl carbon and the nitrogen are directly bonded (i.e. form the amide linkage within the ring).
        bond = main_frag.GetBondBetweenAtoms(nitrogen_atom.GetIdx(), carbonyl_carbon.GetIdx())
        if bond is not None:
            return True, ("Beta-lactam ring detected: found a 4-membered ring with one nitrogen, three carbons "
                          "(where one carbon is carbonyl via a double bond to oxygen outside the ring) and a direct "
                          "C-N bond representing the amide bond")
    
    # If no ring met our criteria, return False.
    return False, "No beta-lactam ring found (4-membered ring with the required amide bond was not detected)"

# Example usage:
if __name__ == "__main__":
    # A few example SMILES (including azetidin-2-one as the simplest beta-lactam)
    test_smiles = [
        "O=C1CCN1",   # azetidin-2-one
        "[H][C@]12SCC(C)=C(N1C(=O)[C@H]2N)C(O)=O",  # 7beta-aminodeacetoxycephalosporanic acid
        "C[C@H]1[C@@H](C(=O)N1S(=O)(=O)O)NC(=O)C(=NOC(C)(C)C(=O)O)C2=CSC(=N2)N"  # complex beta-lactam derivative
    ]
    
    for smi in test_smiles:
        result, reason = is_beta_lactam(smi)
        print("SMILES:", smi)
        print("Result:", result)
        print("Reason:", reason)
        print("------")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35627',
                          'name': 'beta-lactam',
                          'definition': 'A lactam in which the amide bond is '
                                        'contained within a four-membered '
                                        'ring, which includes the amide '
                                        'nitrogen and the carbonyl carbon.',
                          'parents': ['CHEBI:24995'],
                          'xrefs': ['KEGG:C01866', 'Wikipedia:Beta-lactam'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 82,
                           'log_lines_of_code': 4.406719247264253,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 3,
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
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
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
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetMolFrags',
                                                 'GetNumHeavyAtoms',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'AddHs',
                                                 'GetBondType',
                                                 'GetRingInfo'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_beta_lactam(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No fragments could be '
                                          'parsed from the SMILES"',
                                          'True, ("Beta-lactam ring detected: '
                                          'found a 4-membered ring with one '
                                          'nitrogen, three carbons "',
                                          'False, "No beta-lactam ring found '
                                          '(4-membered ring with the required '
                                          'amide bond was not detected)"'],
                           'returns_count': 4,
                           'complexity': 5.48134384945285},
    'message': '\n'
               'Attempt failed: F1 score of 0.7364016736401674 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@]12SCC(C)=C(N1C(=O)[C@H]2N)C(O)=O NAME: '
               '7beta-aminodeacetoxycephalosporanic acid REASON: CORRECT '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               'C[C@H]1[C@@H](C(=O)N1S(=O)(=O)O)NC(=O)C(=NOC(C)(C)C(=O)O)C2=CSC(=N2)N '
               'NAME: '
               '2-[[1-(2-amino-4-thiazolyl)-2-[[(2S,3S)-2-methyl-4-oxo-1-sulfo-3-azetidinyl]amino]-2-oxoethylidene]amino]oxy-2-methylpropanoic '
               'acid REASON: CORRECT Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@@]1(CCCO1)C1=C(N2C(=O)[C@@]([H])([C@H](C)O)[C@@]2([H])S1)C([O-])=O '
               'NAME: '
               '6beta-[(S)-1-hydroxyethyl]-2-[(R)-tetrahydrofuran-2-yl]pen-2-em-3-carboxylate '
               'REASON: CORRECT Beta-lactam ring detected: found 4-membered '
               'ring with a carbonyl carbon and an adjacent nitrogen '
               'representing an amide bond\n'
               ' * SMILES: '
               'N[C@H](CCOc1ccc(cc1)C(=N\\O)\\C(=O)N[C@H]1CN([C@@H](C(O)=O)c2ccc(O)cc2)C1=O)C(O)=O '
               'NAME: nocardicin A REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: [H][C@@]12CC(=O)N1[C@@H](C(O)=O)C(C)(C)S2(=O)=O '
               'NAME: sulbactam REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: S1C2N(C(=O)C2NC(=O)CSC3=CC=NC=C3)C(=C(C1)CO)C(O)=O '
               'NAME: '
               '7-{[1-hydroxy-2-(pyridin-4-ylsulfanyl)ethylidene]amino}-3-(hydroxymethyl)-8-oxo-5-thia-1-azabicyclo[4.2.0]oct-2-ene-2-carboxylic '
               'acid REASON: CORRECT Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'C[C@@H]1[C@H]([C@@H](O[C@]12C3=CC=CC=C3N(C2=O)CC4=CC(=CC=C4)N5CCC5=O)CCN6C=C(N=N6)CCO)[Si](C)(C)C7=CC=C(C=C7)OC '
               'NAME: '
               "(3S,3'S,4'R,5'S)-5'-[2-[4-(2-hydroxyethyl)-1-triazolyl]ethyl]-4'-[(4-methoxyphenyl)-dimethylsilyl]-3'-methyl-1-[[3-(2-oxo-1-azetidinyl)phenyl]methyl]-2-spiro[indole-3,2'-oxolane]one "
               'REASON: CORRECT Beta-lactam ring detected: found 4-membered '
               'ring with a carbonyl carbon and an adjacent nitrogen '
               'representing an amide bond\n'
               ' * SMILES: '
               '[C@]12(N(C(=C(CS1)COC)C(=O)O)C([C@H]2NC(=O)/C(=N\\O)/C3=CSC(=N3)N)=O)[H] '
               'NAME: cefdaloxime REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: O=C1CCN1 NAME: azetidin-2-one REASON: CORRECT '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               'O\\N=C(/C(=O)N[C@H]1CN([C@@H](C(O)=O)c2ccc(O)cc2)C1=O)c1ccc(O)cc1 '
               'NAME: nocardicin E REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: [H][C@@]12CC(=O)N1C=C[C@@H]2C NAME: '
               '1beta-methylcarbapenem REASON: CORRECT Beta-lactam ring '
               'detected: found 4-membered ring with a carbonyl carbon and an '
               'adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(Sc3nc(cs3)-c3cc[n+](C)cc3)=C(N1C(=O)[C@H]2NC(=O)C(=N/OCC)\\c1nsc(NP(O)(O)=O)n1)C([O-])=O '
               'NAME: ceftaroline fosamil REASON: CORRECT Beta-lactam ring '
               'detected: found 4-membered ring with a carbonyl carbon and an '
               'adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(Sc3nc(cs3)-c3cc[n+](C)cc3)=C(N1C(=O)[C@H]2NC(=O)C(=N/OCC)\\c1nsc(N)n1)C([O-])=O '
               'NAME: ceftaroline REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[C@]12(N(C(=C(CS1)/C=C/C[N+](CC(N)=O)(CC)C)C(=O)[O-])C([C@H]2NC(=O)/C(/C3=NSC(=N3)N)=N\\OCF)=O)[H] '
               'NAME: cefluprenam REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'S(CC1=C(N2[C@](SC1)([C@@](C2=O)(NC(CN3C=C(C(C(=C3)Cl)=O)Cl)=O)[H])[H])C(=O)O)C=4SC(=NN4)C '
               'NAME: cefazedone REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[C@H]1(C(N(C1)[C@H](C=2C=CC(=CC2)O)C(=O)O)=O)NC([C@@H](C3=CC=C(C=C3)OCC[C@H](C(O)=O)N)N)=O '
               'NAME: nocardicin C REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'S(=O)(=O)(OC([C@@H]1C(=O)N2C(C(=O)O)=C(C[C@H]12)S(=O)CCNC(=O)C)(C)C)O '
               'NAME: Carpetimycin D REASON: CORRECT Beta-lactam ring '
               'detected: found 4-membered ring with a carbonyl carbon and an '
               'adjacent nitrogen representing an amide bond\n'
               ' * SMILES: S(C1C(N2C(C1)/C(/C2=O)=C/C)C(O)=O)CCN NAME: '
               'Carbapenem biosynthesis intermediate 4 REASON: CORRECT '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[C@]12(N(C(=C(CS1)CSC3=NN=C(S3)C)C(=O)O)C([C@H]2NC(=O)CN4C=NN=N4)=O)[H] '
               'NAME: cefazolin REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)COc1ccccc1)C([O-])=O '
               'NAME: phenoxymethylpenicillin(1-) REASON: CORRECT Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(CSc3nnnn3C)=C(N1C(=O)[C@H]2NC(=O)[C@H](O)c1ccccc1)C(O)=O '
               'NAME: cefamandole REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)CCC[C@@H](N)C(O)=O)C(O)=O '
               'NAME: penicillin N REASON: CORRECT Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H]C(CCCC([H])=Nc1ccc(N)cc1)=N[C@@H]1C(=O)N2[C@@H](C(O)=O)C(C)(C)S[C@]12[H] '
               'NAME: '
               '6beta-({5-[(p-aminophenyl)imino]pentylidene}amino)penicillanic '
               'acid REASON: CORRECT Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'CC(=O)OCC1=C(N2[C@@H]([C@@H](C2=O)NC(=O)C(=NOC)C3=CSC(=N3)N)SC1)C(=O)O '
               'NAME: '
               '(6R,7R)-3-(acetyloxymethyl)-7-[[2-(2-amino-4-thiazolyl)-2-methoxyimino-1-oxoethyl]amino]-8-oxo-5-thia-1-azabicyclo[4.2.0]oct-2-ene-2-carboxylic '
               'acid REASON: CORRECT Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'CC1(C(N2[C@H](S1)[C@@H](C2=O)NC(=O)COC3=CC=CC=C3)C(=O)O)C.CC1(C(N2[C@H](S1)[C@@H](C2=O)NC(=O)COC3=CC=CC=C3)C(=O)O)C.C1=CC=C(C=C1)CNCCNCC2=CC=CC=C2 '
               "NAME: N,N'-bis(phenylmethyl)ethane-1,2-diamine "
               '(5R,6R)-3,3-dimethyl-7-oxo-6-[(1-oxo-2-phenoxyethyl)amino]-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: CORRECT Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               'False positives: SMILES: '
               'N12[C@](CC1=O)(C[C@H]([C@H]2C(=O)[O-])SCCNC(CCNC(=O)[C@@H](C(CO)(C)C)O)=O)[H] '
               'NAME: (2R,3R,5S)-2-(S-pantetheinyl)-carbapenam-3-carboxylate '
               'REASON: WRONGLY CLASSIFIED Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'O.[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccc(O)cc1)C(O)=O '
               'NAME: cefadroxil monohydrate REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@]2(NC(=O)C([H])(C([O-])=O)c1ccsc1)OC)C([O-])=O '
               'NAME: temocillin(2-) REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[Na+].[Na+].[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)C(C([O-])=O)c1ccccc1)C([O-])=O '
               'NAME: carbenicillin disodium REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccc(O)cc1)C([O-])=O '
               'NAME: cefadroxil(1-) REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[Na+].[H][C@]12SCC=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\c1csc(N)n1)C([O-])=O '
               'NAME: ceftizoxime sodium REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[Na+].[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(C)onc1-c1c(Cl)cccc1Cl)C([O-])=O '
               'NAME: dicloxacillin sodium REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               'O.CC(O)=O.[H][C@]12SCC(Sc3nc(cs3)-c3cc[n+](C)cc3)=C(N1C(=O)[C@H]2NC(=O)C(=N/OCC)\\c1nsc(NP(O)(O)=O)n1)C([O-])=O '
               'NAME: ceftaroline fosamil acetate monohydrate REASON: WRONGLY '
               'CLASSIFIED Beta-lactam ring detected: found 4-membered ring '
               'with a carbonyl carbon and an adjacent nitrogen representing '
               'an amide bond\n'
               ' * SMILES: '
               'Cl.Cl.[H][C@]12SCC(CSc3nnnn3CCN(C)C)=C(N1C(=O)[C@@]2([H])NC(=O)Cc1csc(N)n1)C(O)=O '
               'NAME: cefotiam dihydrochloride REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[H][C@]12CC(=O)N1[C@@H]([C@@H](CC[NH3+])O2)C([O-])=O NAME: '
               'dihydroclavaminic acid zwitterion REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[H][N+]([H])(CCc1ccccc1)Cc1ccccc1.[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)Cc1ccccc1)C([O-])=O '
               'NAME: benzylpenicillin benethamine REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[H]O[H].[H]O[H].[H]O[H].[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C(O)=O '
               'NAME: ampicillin trihydrate REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(CSc3nnnn3C)=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\c1csc(N)n1)C([O-])=O '
               'NAME: cefmenoxime(1-) REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               'CCN1CCN(C(=O)C1=O)C(=O)N[C@H](C2=CC=CC=C2)C(=O)N[C@H]3[C@H]4N(C3=O)[C@H](C(S4)(C)C)C(=O)O '
               'NAME: '
               '(2S,5S,6R)-6-[[(2R)-2-[[(4-ethyl-2,3-dioxo-1-piperazinyl)-oxomethyl]amino]-1-oxo-2-phenylethyl]amino]-3,3-dimethyl-7-oxo-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Beta-lactam ring detected: '
               'found 4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'S1[C@H]2N(C(C(=O)O)=C(C1)COC(=O)C[C@@H](O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC)C)C)CCCN=C(N)N)C(=O)[C@]2(NC(=O)CCC[C@@H](N)C(=O)O)NC=O '
               'NAME: Chitinovorin B REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: CC(C)[C@@]1(C(=O)N(N1C(=O)OC)C(=O)OC)C2=CSC=C2 '
               'NAME: '
               '(3S)-4-oxo-3-propan-2-yl-3-(3-thiophenyl)diazetidine-1,2-dicarboxylic '
               'acid dimethyl ester REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               'CC(=O)NCCC[C@H](N)C(=O)N[C@@H](C(O)[C@H]1CN2[C@H](CC2=O)O1)C(O)=O '
               'NAME: Clavamycin F REASON: WRONGLY CLASSIFIED Beta-lactam ring '
               'detected: found 4-membered ring with a carbonyl carbon and an '
               'adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               'C[C@H]([C@H](NC([C@H](CC[C@H]1C(NC1)=O)N)=O)C(=O)O)O NAME: '
               'Tabtoxin biosynthesis intermediate 6 REASON: WRONGLY '
               'CLASSIFIED Beta-lactam ring detected: found 4-membered ring '
               'with a carbonyl carbon and an adjacent nitrogen representing '
               'an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(COC(C)=O)=C(N1C(=O)[C@H]2NC(=O)CCCC(=O)C([O-])=O)C([O-])=O '
               'NAME: (7R)-7-(5-carboxy-5-oxopentanamido)cephalosporanate(2-) '
               'REASON: WRONGLY CLASSIFIED Beta-lactam ring detected: found '
               '4-membered ring with a carbonyl carbon and an adjacent '
               'nitrogen representing an amide bond\n'
               ' * SMILES: '
               'S(=O)(=O)(O)N1C(=O)[C@@](OC)(NC(=O)[C@@H](NC(=O)CC[C@@H](N)C(=O)O)C)C1 '
               'NAME: Isosulfazecin REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H][C@]12SCC(COC(C)=O)=C(N1C(=O)[C@H]2[NH3+])C([O-])=O NAME: '
               '7beta-aminocephalosporanic acid zwitterion REASON: WRONGLY '
               'CLASSIFIED Beta-lactam ring detected: found 4-membered ring '
               'with a carbonyl carbon and an adjacent nitrogen representing '
               'an amide bond\n'
               ' * SMILES: '
               '[Na+].[H][C@]12SCC(CSC3=NN=NN3C)=C(N1C(=O)[C@]2(NC(=O)CSC[C@@H](N)C(O)=O)OC)C([O-])=O '
               'NAME: cefminox sodium REASON: WRONGLY CLASSIFIED Beta-lactam '
               'ring detected: found 4-membered ring with a carbonyl carbon '
               'and an adjacent nitrogen representing an amide bond\n'
               ' * SMILES: '
               '[H+].[Cl-].[H]C(=N[C@@H]1C(=O)N2[C@@H](C(=O)OCOC(=O)C(C)(C)C)C(C)(C)S[C@]12[H])N1CCCCCC1 '
               'NAME: pivmecillinam hydrochloride REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[Na+].OC(=O)c1nc(c[nH]1)C(=O)N[C@@H](C(=O)N[C@H]1[C@H]2SCC(C[n+]3ccc(CCS([O-])(=O)=O)cc3)=C(N2C1=O)C([O-])=O)c1ccccc1 '
               'NAME: Cefpimizole sodium REASON: WRONGLY CLASSIFIED '
               'Beta-lactam ring detected: found 4-membered ring with a '
               'carbonyl carbon and an adjacent nitrogen representing an amide '
               'bond\n'
               ' * SMILES: '
               '[Na+].[H]O[H].[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(OC)cccc1OC)C([O-])=O '
               'NAME: methicillin sodium monohydrate REASON: WRONGLY '
               'CLASSIFIED Beta-lactam ring detected: found 4-membered ring '
               'with a carbonyl carbon and an adjacent nitrogen representing '
               'an amide bond\n'
               'False negatives: SMILES: '
               '[H][C@]1(N[C@@H](C([O-])=O)C(C)(C)S1)[C@H](NC(=O)CC1=CC=CC=C1)C(=O)NCCCC '
               'NAME: benzylpenicilloyl-butylamine(1-) REASON: MISSED No '
               'beta-lactam ring found (4-membered ring with the required '
               'amide bond was not detected)\n'
               ' * SMILES: '
               '[H]C(N[C@@H](C([O-])=O)C(C)(C)S)=C1N=C(Cc2ccccc2)OC1=O NAME: '
               'benzylpenicillenate REASON: MISSED No beta-lactam ring found '
               '(4-membered ring with the required amide bond was not '
               'detected)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No beta-lactam ring found '
                                               '(4-membered ring with the '
                                               'required amide bond was not '
                                               'detected)'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]1(N[C@@H](C([O-])=O)C(C)(C)S1)[C@H](NC(=O)CC1=CC=CC=C1)C(=O)NCCCC',
                                      'name': 'benzylpenicilloyl-butylamine(1-)',
                                      'reason': 'No beta-lactam ring found '
                                                '(4-membered ring with the '
                                                'required amide bond was not '
                                                'detected)'},
                                  {   'smiles': '[H]C(N[C@@H](C([O-])=O)C(C)(C)S)=C1N=C(Cc2ccccc2)OC1=O',
                                      'name': 'benzylpenicillenate',
                                      'reason': 'No beta-lactam ring found '
                                                '(4-membered ring with the '
                                                'required amide bond was not '
                                                'detected)'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'We noticed that the previous beta‐lactam classifier simply '
                 'looked for any 4‐membered ring that had a nitrogen and a '
                 'carbon (with a double bond to oxygen) that were directly '
                 'bonded. Unfortunately the pattern was too loose. Many false '
                 'positives were found because some 4‐membered rings (or '
                 'fragments thereof) in larger molecules may contain a '
                 'nitrogen and a carbonyl group but are not “true” beta‐lactam '
                 'cores. Also, some beta‐lactams (for example in fused ring '
                 'systems) were missed because the criteria did not insist on '
                 'the correct composition of the beta‐lactam ring. \n'
                 '\n'
                 'We thus improved our approach:\n'
                 '1. First, we select the largest fragment (to remove salts '
                 'and extraneous fragments) and add explicit hydrogens to help '
                 'with perceiving bonds.\n'
                 '2. Then, we examine every ring with exactly 4 atoms.\n'
                 '3. For each candidate 4‑membered ring we enforce that it '
                 'must have exactly one nitrogen and exactly three carbons. '
                 '(This is the composition of a classic beta‐lactam ring.)\n'
                 '4. For the carbons in the ring, we check if at least one is '
                 '“carbonyl”: that is, it must have at least one double bond '
                 'to an oxygen that is not part of the same ring.\n'
                 '5. Finally, we verify that the carbonyl carbon and the '
                 'nitrogen are directly connected by a bond (representing the '
                 'amide bond in the lactam).\n'
                 '\n'
                 'If these conditions are met, we classify the molecule as a '
                 'beta‑lactam and provide an explanatory reason. Otherwise we '
                 'return False with a reason.\n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 264,
    'num_false_positives': 174,
    'num_true_negatives': 141860,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.6027397260273972,
    'recall': 0.9924812030075187,
    'f1': 0.75,
    'accuracy': 0.9987631763879129,
    'negative_predictive_value': 0.9999859017918823}