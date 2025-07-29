"""
Classifies: CHEBI:38958 indole alkaloid
"""
"""
Classifies: Indole alkaloid

Definition: An alkaloid containing an indole skeleton.
This implementation uses a SMARTS pattern to detect the indole core 
(c1ccc2[nH]ccc2c1) and then requires that at least one match corresponds
to a classical indole fragment (with 9 or 10 atoms in the match). 
It also includes a simple amide bond check to help filter out peptide‐like 
molecules (which sometimes contain a Trp residue but are not indole alkaloids).
"""

from rdkit import Chem

def is_indole_alkaloid(smiles: str):
    """
    Determines if a given molecule is an indole alkaloid based on its SMILES string.
    For our purposes, the molecule qualifies if it:
      (1) Can be parsed as a molecule,
      (2) Contains at least one nitrogen atom (as a rough check for alkaloid nature),
      (3) Contains an indole skeleton as defined by the SMARTS pattern "c1ccc2[nH]ccc2c1"
          with at least one match whose atom count is 9 (or at most one extra atom to allow slight extension),
      (4) Does NOT contain multiple amide bonds (which would suggest a peptide rather than an alkaloid).
      
    Args:
        smiles (str): The SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as an indole alkaloid, False otherwise.
        str: Explanation string for the decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check that the molecule has at least one nitrogen atom.
    num_nitrogen = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    if num_nitrogen == 0:
        return False, "Molecule does not contain any nitrogen atoms; unlikely to be an alkaloid"
    
    # (Optional) Filter out obvious peptides: count amide bonds via a simple SMARTS. 
    # Most indole alkaloids have at most one amide bond. (Peptides will contain two or more.)
    amide_smarts = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_smarts)
    if len(amide_matches) >= 2:
        return False, "Molecule contains multiple amide bonds; likely a peptide rather than an indole alkaloid"
    
    # Define the indole SMARTS pattern.
    indole_smarts = "c1ccc2[nH]ccc2c1"  # canonical indole substructure
    indole_query = Chem.MolFromSmarts(indole_smarts)
    if indole_query is None:
        return False, "Error in indole SMARTS pattern"
    
    # Look for indole substructure matches.
    matches = mol.GetSubstructMatches(indole_query)
    if not matches:
        return False, "No indole skeleton found"
    
    # Check that at least one match is of the expected size (9 atoms, possibly 10 to allow slight extensions).
    valid_match = False
    for match in matches:
        # For a classical indole, the match should yield 9 atoms.
        # However, sometimes one extra atom may be included due to fused extensions.
        if len(match) == 9 or len(match) == 10:
            valid_match = True
            break
    if not valid_match:
        return False, "Indole-like substructure found but does not match the expected indole fragment size"
    
    # Passed all tests: assume the molecule contains an indole skeleton and is of alkaloid type.
    return True, "Molecule contains an indole skeleton and minimal amide bonds, consistent with an indole alkaloid"

# For testing (if this code is run as a script), you can include a main section.
if __name__ == "__main__":
    # Test with one example (Ochropposinine)
    test_smiles = "CC[C@]1(CN2CCC=3C4=CC(=C(C=C4NC3[C@@]2(C[C@@]1(CCO)[H])[H])OC)OC)[H]"
    result, reason = is_indole_alkaloid(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:38958',
                          'name': 'indole alkaloid',
                          'definition': 'An alkaloid containing an indole '
                                        'skeleton.',
                          'parents': ['CHEBI:22315'],
                          'xrefs': ['KEGG:C06073', 'Wikipedia:Indole_alkaloid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 54,
                           'log_lines_of_code': 3.9889840465642745,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum'],
                           'methods_called_count': 5,
                           'smarts_strings': ['indole_smarts', 'C(=O)N'],
                           'smarts_strings_count': 2,
                           'defs': ['is_indole_alkaloid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule does not contain '
                                          'any nitrogen atoms; unlikely to be '
                                          'an alkaloid"',
                                          'False, "Molecule contains multiple '
                                          'amide bonds; likely a peptide '
                                          'rather than an indole alkaloid"',
                                          'False, "Error in indole SMARTS '
                                          'pattern"',
                                          'False, "No indole skeleton found"',
                                          'False, "Indole-like substructure '
                                          'found but does not match the '
                                          'expected indole fragment size"',
                                          'True, "Molecule contains an indole '
                                          'skeleton and minimal amide bonds, '
                                          'consistent with an indole '
                                          'alkaloid"'],
                           'returns_count': 7,
                           'complexity': 3.997796809312855},
    'message': '\n'
               'Attempt failed: F1 score of 0.0985884907709012 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC[C@]1(CN2CCC=3C4=CC(=C(C=C4NC3[C@@]2(C[C@@]1(CCO)[H])[H])OC)OC)[H] '
               'NAME: Ochropposinine REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: [H][C@@]12Cc3c[nH]c4cccc(c34)[C@@]1([H])C=C(C)CN2C '
               'NAME: agroclavine REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'O=C1N2[C@H]([C@@]3(O[C@](C(N3[C@H]1CCC)=O)(NC(=O)[C@@H]4C=C5C6=C7C(NC=C7C[C@H]5N(C4)C)=CC=C6)CCC)O)CCC2 '
               'NAME: Ergonornorine REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: CC(=O)c1nc(cc2c3cccc(O)c3[nH]c12)C(N)=O NAME: '
               'dichotomide VI REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'CNC(=O)[C@]1(O)C(=O)c2c([nH]c3ccc(Cl)cc23)-c2c(OC)c3cc(Cl)ccc3n12 '
               'NAME: cladoniamide E REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: O1C2C3N4C(CC(C3C1)C(C4)=CC)C=5NC6=C(C25)C=CC(OC)=C6 '
               'NAME: '
               '5-Ethylidene-17-methoxy-11-oxa-7,20-diazahexacyclo[11.7.0.02,7.04,9.08,12.014,19]icosa-1(13),14(19),15,17-tetraene '
               'REASON: CORRECT Molecule contains an indole skeleton '
               '(5-membered aromatic ring fused with 6-membered aromatic ring) '
               'and nitrogen, consistent with an indole alkaloid\n'
               ' * SMILES: '
               'O[C@]12N(C([C@@](NC(=O)[C@@H]3C[C@@]4(C5=C6C(=CNC6=CC=C5)C[C@@]4([H])N(C)C3)[H])(C(C)C)O1)=O)[C@@]([C@@H](CC)C)(C(=O)N7CCC[C@@]27[H])[H] '
               'NAME: epicriptine REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'CCC1=C(CC(=O)OC)C(C=2C3=C(C=CN2)C4=CC=CC=C4N3)(OC)OC1=O NAME: '
               'O-methylgeissolaevine REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'C[C@@H]([C@@]1(C[C@]2(C[C@]3(C4=C(CCN(C2)[C@@]13[H])C=5C=C(C=CC5N4)OC)[H])[H])[H])O '
               'NAME: Iboxygaine REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               '[H][C@@]1(C[C@]2([H])C(=CO[C@@H](O)[C@]2([H])C=C)C(=O)OC)NCCC2=C1NC1=C2C=CC=C1 '
               'NAME: strictosidine aglycone REASON: CORRECT Molecule contains '
               'an indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'C1=CC=C2C(=C1)C=3CCN4C(=C5C=CC=6C=NC=C(C65)C4=O)C3N2 NAME: '
               'Naulafine REASON: CORRECT Molecule contains an indole skeleton '
               '(5-membered aromatic ring fused with 6-membered aromatic ring) '
               'and nitrogen, consistent with an indole alkaloid\n'
               ' * SMILES: '
               'CC[C@@]1(C[C@@]2(C[C@@]3(C4=C(CCN(C2)[C@]13[H])C5=CC(=C(C=C5N4)OC)[C@]6(C[C@]7([C@H](CC)CN(C)[C@@](CC=8C9=CC=CC=C9NC86)(C7C(=O)OC)[H])[H])O)C(=O)OC)[H])[H] '
               'NAME: 3-R,S-hydroxytabernaelegantine A REASON: CORRECT '
               'Molecule contains an indole skeleton (5-membered aromatic ring '
               'fused with 6-membered aromatic ring) and nitrogen, consistent '
               'with an indole alkaloid\n'
               ' * SMILES: '
               'C=C[C@]1(CN2CCC=3C=4C=CC(=CC4NC3[C@@]2(C[C@@]1(C[C@@]5(C6=C(CCN5C)C7=CC=CC=C7N6)[H])[H])[H])O)[H] '
               'NAME: 11-hydroxyusambarine REASON: CORRECT Molecule contains '
               'an indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'C=1C=CC=2NC=3[C@]4(N(CCC3C2C1)C[C@@]5([C@@](C(=CO[C@H]5C)C(OC)=O)(C4)[H])[H])[H] '
               'NAME: tetrahydroalstonine REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               '[H][C@@]12Cc3c[nH]c4cccc(C1=C[C@H](CN2C)C(=O)N[C@@]1(O[C@]2(O)N([C@@H](C(C)CC)C(=O)N5CCC[C@@]25[H])C1=O)C(C)C)c34 '
               'NAME: beta-ergocryptine REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](C[C@@H]2CN3CCc4c([nH]c5ccccc45)[C@H]3C[C@@H]2[C@@H]1C(=O)OC)OC(=O)c1cc(OC)c(OC)c(OC)c1 '
               'NAME: deserpidine REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: [H][C@@]12Cc3c[nH]c4cccc(c34)[C@@]1([H])CCCN2 NAME: '
               'ergoline REASON: CORRECT Molecule contains an indole skeleton '
               '(5-membered aromatic ring fused with 6-membered aromatic ring) '
               'and nitrogen, consistent with an indole alkaloid\n'
               ' * SMILES: CN[C@@H]1Cc2c[nH]c3cccc([C@H]1\\C=C(/C)C=O)c23 '
               'NAME: chanoclavine-I aldehyde REASON: CORRECT Molecule '
               'contains an indole skeleton (5-membered aromatic ring fused '
               'with 6-membered aromatic ring) and nitrogen, consistent with '
               'an indole alkaloid\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](C[C@@H]2CN3CCC4=C([C@@H]3C[C@@H]2[C@@H]1C(=O)OC)NC5=C4C=CC(=C5)OC)OC(=O)C6=CC(=C(C(=C6)OC)OC)OC '
               'NAME: '
               '(1S,15S,17R,18R,19S,20S)-6,18-dimethoxy-17-[oxo-(3,4,5-trimethoxyphenyl)methoxy]-1,3,11,12,14,15,16,17,18,19,20,21-dodecahydroyohimban-19-carboxylic '
               'acid methyl ester REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'N12C([C@@H](NC([C@@]1(CCC2)[H])=O)CC3=C(NC4=C3C=CC5=C4C=CC(O5)(C)C)C(C=C)(C)C)=O '
               'NAME: notoamide E REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'COc1c2-c3[nH]c4ccc(Cl)cc4c3[C@@]3(O)C(=O)N(C)C(=O)[C@@]3(O)n2c2ccc(Cl)cc12 '
               'NAME: cladoniamide B REASON: CORRECT Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               '[H][C@@]12C[C@]3(O)C4=CC=CC=C4N([C@]3([H])N1C(=O)[C@H](CC1=C(NC3=C1C=CC=C3)C(C)(C)C=C)NC2=O)C(C)(C)C=C '
               'NAME: okaramine C REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               '[H][C@]12CC[C@H](O)[C@@H](C(=O)OC)[C@@]1([H])C[C@]1([H])N(CCc3c1[nH]c1ccccc31)C2 '
               'NAME: rauwolscine REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               '[C@@]12([C@@]3([C@H](C[C@](C1)(CN3CCC=4C5=C(C=CC(=C5)O)NC42)[H])CC)[H])[H] '
               'NAME: noribogaine REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'C[C@@H]1NC(=O)[C@@H](Cc2c[nH]c3ccccc23)n2c1nc1ccccc1c2=O NAME: '
               'fumiquinazoline F REASON: CORRECT Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               'False positives: SMILES: Brc1ccc2[nH]c3cnccc3c2c1 NAME: '
               'Eudistomin N REASON: WRONGLY CLASSIFIED Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'ClC1=C(OP(=O)(O)O)C=CC(=C1)C2NC(=O)[C@H](N(C(=O)[C@@H](NC(=O)[C@@H](C)CC(=C[C@@H]([C@H](OC([C@H]2OC)=O)C)C)C)C)C)CC3=C(Cl)NC4=C3C=CC=C4 '
               'NAME: Chrondramide 10 REASON: WRONGLY CLASSIFIED Molecule '
               'contains an indole skeleton (5-membered aromatic ring fused '
               'with 6-membered aromatic ring) and nitrogen, consistent with '
               'an indole alkaloid\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)S(=O)(=O)N2CC3(C2)CN([C@@H](C4=C3C5=C(N4)C=C(C=C5)OC)CO)CC6=CC=CC=C6 '
               'NAME: '
               "[(1S)-7-methoxy-1'-(4-methylphenyl)sulfonyl-2-(phenylmethyl)-1-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]methanol "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'CC(=O)N1CC2(CN(C2)CC3=CC=CC=C3Cl)C4=C([C@H]1CO)NC5=C4C=CC(=C5)OC '
               'NAME: '
               "1-[(1S)-1'-[(2-chlorophenyl)methyl]-1-(hydroxymethyl)-7-methoxy-2-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]ethanone "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'C1(=C(C=C2C(=C1)C3=C(N2)[C@]4(C[C@@]5(C(=CO[C@H]([C@@]5(CN4CC3)[H])C)C(OCCN(C)C)=O)[H])[H])OC)OC.Cl.Cl '
               'NAME: Dimethylaminoethyl reserpilinate dihydrochloride REASON: '
               'WRONGLY CLASSIFIED Molecule contains an indole skeleton '
               '(5-membered aromatic ring fused with 6-membered aromatic ring) '
               'and nitrogen, consistent with an indole alkaloid\n'
               ' * SMILES: '
               'CCCC(=O)N1CC2(C1)CN([C@@H](C3=C2C4=C(N3)C=C(C=C4)OC)CO)S(=O)(=O)C5=CC=C(C=C5)C '
               'NAME: '
               "1-[(1S)-1-(hydroxymethyl)-7-methoxy-2-(4-methylphenyl)sulfonyl-1'-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]-1-butanone "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CS)CC=1C=2C(NC1)=CC=CC2)C(O)=O '
               'NAME: Cys-Trp-Cys REASON: WRONGLY CLASSIFIED Molecule contains '
               'an indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CCCCN)C(O)=O)[C@H]3NCCC3 '
               'NAME: Pro-Trp-Lys REASON: WRONGLY CLASSIFIED Molecule contains '
               'an indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'O=C1C=C2C(=CC[C@]3([C@@]2(O)CC[C@@H]4[C@@]3(C=5NC=6C=C7C8=CC(OC([C@H]8[C@@H](C7=CC6C5C4)O)(C)C)(C)C)C)C)O[C@@H]1C(O)(C)C '
               'NAME: Shearinine M REASON: WRONGLY CLASSIFIED Molecule '
               'contains an indole skeleton (5-membered aromatic ring fused '
               'with 6-membered aromatic ring) and nitrogen, consistent with '
               'an indole alkaloid\n'
               ' * SMILES: BrC1=CC=2NC=3C=C(Br)C=CC3C2C=C1 NAME: '
               '2,7-Dibromocarbazole REASON: WRONGLY CLASSIFIED Molecule '
               'contains an indole skeleton (5-membered aromatic ring fused '
               'with 6-membered aromatic ring) and nitrogen, consistent with '
               'an indole alkaloid\n'
               ' * SMILES: '
               'O=C1N2[C@H](C(=O)N3[C@@]1(O)[C@H](OC)C=4C5=C(C=C(OC)C=C5)NC4[C@H]3C=C(C)C)CCC2 '
               'NAME: Rel-(8R)-9-hydroxy-8-methoxy-18-epi-fumitremorgin C '
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC=1C=2C(NC1)=CC=CC2 '
               'NAME: Arg-Trp-Ala REASON: WRONGLY CLASSIFIED Molecule contains '
               'an indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'O=C1C(=C[C@H](CC=C[C@@H]2[C@]3(C(CC[C@@H]1O)=O)C(=O)N[C@]4([C@@H]3[C@H](C)[C@]([C@H]2O)(C)O4)CC=5C6=C(C=CC=C6)NC5)C)C '
               'NAME: Chaetoglobosin W REASON: WRONGLY CLASSIFIED Molecule '
               'contains an indole skeleton (5-membered aromatic ring fused '
               'with 6-membered aromatic ring) and nitrogen, consistent with '
               'an indole alkaloid\n'
               ' * SMILES: O(CC1=C2C(NC(=C2)C)=CC=C1)C NAME: '
               '4-Methoxymethyl-2-methylindole REASON: WRONGLY CLASSIFIED '
               'Molecule contains an indole skeleton (5-membered aromatic ring '
               'fused with 6-membered aromatic ring) and nitrogen, consistent '
               'with an indole alkaloid\n'
               ' * SMILES: '
               'CC1=C(C=C(C=C1)F)S(=O)(=O)N[C@@H]2CCN(C2)CC3=CC4=C(C=C3)NC=C4 '
               'NAME: '
               '5-fluoro-N-[(3R)-1-(1H-indol-5-ylmethyl)-3-pyrrolidinyl]-2-methylbenzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'CC(C)OC1=CC=CC(=C1)N2C(=NC3=CC=CC=C3C2=O)CCC4=CNC5=C4C=C(C=C5)Br '
               'NAME: '
               '2-[2-(5-bromo-1H-indol-3-yl)ethyl]-3-(3-propan-2-yloxyphenyl)-4-quinazolinone '
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'CCCNC(=O)N1CC2(CN(C2)C(=O)C3=NC=CN=C3)C4=C([C@H]1CO)NC5=C4C=CC(=C5)OC '
               'NAME: '
               "(1S)-1-(hydroxymethyl)-7-methoxy-1'-[oxo(2-pyrazinyl)methyl]-N-propyl-2-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]carboxamide "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'CC(=O)N1CC2(CN(C2)C(=O)NC3=CC=C(C=C3)OC)C4=C([C@H]1CO)NC5=C4C=CC(=C5)OC '
               'NAME: '
               "(1S)-2-acetyl-1-(hydroxymethyl)-7-methoxy-N-(4-methoxyphenyl)-1'-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]carboxamide "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'O=C1[C@H](NC([C@@H](NC([C@@H](CC(C)C)NC(=O)[C@@H](NC([C@@H](C(C)C)NC(=O)[C@@H]2CSC(N2)[C@H](C(C)C)N1)=O)CC=3C=4C=CC=CC4NC3)=O)C(C)C)=O)C(C)C '
               'NAME: lugdunin REASON: WRONGLY CLASSIFIED Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'O=C1N([C@@H](C(=O)N[C@H]1CC=2C3=C(C=CC=C3)NC2)CC(C)C)C NAME: '
               'Cyclo(D-N-methyl-Leu-L-Trp) REASON: WRONGLY CLASSIFIED '
               'Molecule contains an indole skeleton (5-membered aromatic ring '
               'fused with 6-membered aromatic ring) and nitrogen, consistent '
               'with an indole alkaloid\n'
               ' * SMILES: '
               'O1[C@]2(O)N([C@H](C(=O)N3[C@H]2CCC3)CC(C)C)C(=O)[C@@]1(NC(=O)[C@@H]4C[C@H]5[C@H](N(C4)C)CC=6C7=C5C=CC=C7NC6)C '
               'NAME: Dhesn REASON: WRONGLY CLASSIFIED Molecule contains an '
               'indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CCN(CC4)C(=O)C5=CC=CC=C5)C(=O)C6=CC(=CC=C6)F)CO '
               'NAME: '
               "[(1R)-2-[(3-fluorophenyl)-oxomethyl]-1-(hydroxymethyl)-7-methoxy-1'-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,4'-piperidine]yl]-phenylmethanone "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC=1C=2C(NC1)=CC=CC2 '
               'NAME: Gln-Trp-Lys REASON: WRONGLY CLASSIFIED Molecule contains '
               'an indole skeleton (5-membered aromatic ring fused with '
               '6-membered aromatic ring) and nitrogen, consistent with an '
               'indole alkaloid\n'
               ' * SMILES: '
               'CN(C)CC(=O)N1CCC2(CC1)CN([C@H](C3=C2C4=C(N3)C=C(C=C4)OC)CO)CC5=CN=CC=C5 '
               'NAME: '
               "2-(dimethylamino)-1-[(1R)-1-(hydroxymethyl)-7-methoxy-2-(3-pyridinylmethyl)-1'-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,4'-piperidine]yl]ethanone "
               'REASON: WRONGLY CLASSIFIED Molecule contains an indole '
               'skeleton (5-membered aromatic ring fused with 6-membered '
               'aromatic ring) and nitrogen, consistent with an indole '
               'alkaloid\n'
               ' * SMILES: O=C1C(=O)C2=C(NC3=C2C=CC=C3)C(=C1C)CCCCCCC(C)C '
               'NAME: Carbazoquinocin F REASON: WRONGLY CLASSIFIED Molecule '
               'contains an indole skeleton (5-membered aromatic ring fused '
               'with 6-membered aromatic ring) and nitrogen, consistent with '
               'an indole alkaloid\n'
               'False negatives: SMILES: '
               '[H][C@@]12COC=C[C@@]1([H])C[C@]1([H])N(CC[C@]11CNc3ccccc13)C2 '
               'NAME: formosanan REASON: MISSED No indole skeleton found\n'
               ' * SMILES: '
               'COC([C@@H]1C[C@@]23CCCN4CCC5(C6=CC=CC=C6N(C(=O)OC)[C@]15CC2)[C@]34[H])=O '
               'NAME: Pleiocarpine REASON: MISSED No indole skeleton found\n'
               ' * SMILES: '
               'O=C1N2[C@@]3([C@@]4([C@]5(N(CC4)C\\C(\\[C@](C5)(C3=CC1)[H])=C\\CO)[H])C=6C2=CC=CC6)[H] '
               'NAME: isostrychnine REASON: MISSED No indole skeleton found\n'
               ' * SMILES: '
               '[H][C@@]12N3CC[C@]11C(Nc4ccccc14)=C(C[C@]2(CC)C=CC3)C(=O)OC '
               'NAME: tabersonine REASON: MISSED No indole skeleton found\n'
               ' * SMILES: '
               'C/C=C\\1/CN2CC[C@]34C5=CC(C=6C=C7C(=CC6OC)[C@]89CCN%10C/C(=C\\C)/[C@](CCC8%10N7C)([C@]9(C(=O)OC)[H])[H])=C(C=C5N(C)[C@]4(C2C[C@@]1([C@@]3(C(=O)OC)[H])[H])[H])OC '
               'NAME: Desoxycabufiline REASON: MISSED No indole skeleton '
               'found\n'
               ' * SMILES: '
               'CON1c2ccccc2[C@]2(C=C(O)C(=O)N3\\C(=C\\c4c[nH]cn4)C(=O)N[C@]123)C(C)(C)C=C '
               'NAME: meleagrine REASON: MISSED No indole skeleton found\n'
               ' * SMILES: [H][C@@]12N3CCC[C@]1(CC)C=Cn1c2c(CC3)c2ccccc12 '
               'NAME: eburnamenine REASON: MISSED No indole skeleton found\n'
               ' * SMILES: '
               'C/C=C\\1/CN2CCC=3C4=CC=CC=C4[NH2+]C3[C@@]2(C[C@@]1([C@](CC5=CN6C[C@]7([C@H](C)OC=C([C@]7(CC6=C8C5=C9C=CC=CC9=N8)[H])C(=O)OC)[H])(C(=O)OC)[H])[H])[H] '
               "NAME: 20'-episerpentinine REASON: MISSED No indole skeleton "
               'found\n'
               ' * SMILES: '
               '[H][C@]12N(C)CC[C@]1(c1ccccc1N2C)[C@@]12CCN(C)[C@]1([H])N(C)c1ccccc21 '
               'NAME: (-)-folicanthine REASON: MISSED No indole skeleton '
               'found\n'
               ' * SMILES: '
               'O(C(=O)[C@H]1[C@@]23C(=NC=4C2=CC=CC4)[C@]5(N(CC3)C\\C(\\[C@@]1(C5)[H])=C\\C)[H])C '
               'NAME: methyl '
               '(1R,10S,12R,13E,18R)-13-ethylidene-8,15-diazapentacyclo[10.5.1.01,9.02,7.010,15]octadeca-2,4,6,8-tetraene-18-carboxylate '
               'REASON: MISSED No indole skeleton found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Molecule contains multiple '
                                               'amide bonds; likely a peptide '
                                               'rather than an indole '
                                               'alkaloid'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Molecule does not contain any '
                                               'nitrogen atoms; unlikely to be '
                                               'an alkaloid'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Molecule does not contain any '
                                               'nitrogen atoms; unlikely to be '
                                               'an alkaloid'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No indole skeleton found'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No indole skeleton found'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Molecule does not contain any '
                                               'nitrogen atoms; unlikely to be '
                                               'an alkaloid'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Molecule does not contain any '
                                               'nitrogen atoms; unlikely to be '
                                               'an alkaloid'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No indole skeleton found'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Molecule contains multiple '
                                               'amide bonds; likely a peptide '
                                               'rather than an indole '
                                               'alkaloid'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Molecule does not contain any '
                                               'nitrogen atoms; unlikely to be '
                                               'an alkaloid'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1N2[C@H]([C@@]3(O[C@](C(N3[C@H]1CCC)=O)(NC(=O)[C@@H]4C=C5C6=C7C(NC=C7C[C@H]5N(C4)C)=CC=C6)CCC)O)CCC2',
                                      'name': 'Ergonornorine',
                                      'reason': 'Molecule contains multiple '
                                                'amide bonds; likely a peptide '
                                                'rather than an indole '
                                                'alkaloid'},
                                  {   'smiles': '[H][C@@]12COC=C[C@@]1([H])C[C@]1([H])N(CC[C@]11CNc3ccccc13)C2',
                                      'name': 'formosanan',
                                      'reason': 'No indole skeleton found'},
                                  {   'smiles': 'O[C@]12N(C([C@@](NC(=O)[C@@H]3C[C@@]4(C5=C6C(=CNC6=CC=C5)C[C@@]4([H])N(C)C3)[H])(C(C)C)O1)=O)[C@@]([C@@H](CC)C)(C(=O)N7CCC[C@@]27[H])[H]',
                                      'name': 'epicriptine',
                                      'reason': 'Molecule contains multiple '
                                                'amide bonds; likely a peptide '
                                                'rather than an indole '
                                                'alkaloid'},
                                  {   'smiles': 'COC([C@@H]1C[C@@]23CCCN4CCC5(C6=CC=CC=C6N(C(=O)OC)[C@]15CC2)[C@]34[H])=O',
                                      'name': 'Pleiocarpine',
                                      'reason': 'No indole skeleton found'},
                                  {   'smiles': 'O=C1N2[C@@]3([C@@]4([C@]5(N(CC4)C\\C(\\[C@](C5)(C3=CC1)[H])=C\\CO)[H])C=6C2=CC=CC6)[H]',
                                      'name': 'isostrychnine',
                                      'reason': 'No indole skeleton found'},
                                  {   'smiles': '[H][C@@]12N3CC[C@]11C(Nc4ccccc14)=C(C[C@]2(CC)C=CC3)C(=O)OC',
                                      'name': 'tabersonine',
                                      'reason': 'No indole skeleton found'},
                                  {   'smiles': 'C/C=C\\1/CN2CC[C@]34C5=CC(C=6C=C7C(=CC6OC)[C@]89CCN%10C/C(=C\\C)/[C@](CCC8%10N7C)([C@]9(C(=O)OC)[H])[H])=C(C=C5N(C)[C@]4(C2C[C@@]1([C@@]3(C(=O)OC)[H])[H])[H])OC',
                                      'name': 'Desoxycabufiline',
                                      'reason': 'No indole skeleton found'},
                                  {   'smiles': 'CON1c2ccccc2[C@]2(C=C(O)C(=O)N3\\C(=C\\c4c[nH]cn4)C(=O)N[C@]123)C(C)(C)C=C',
                                      'name': 'meleagrine',
                                      'reason': 'Molecule contains multiple '
                                                'amide bonds; likely a peptide '
                                                'rather than an indole '
                                                'alkaloid'},
                                  {   'smiles': '[H][C@@]12N3CCC[C@]1(CC)C=Cn1c2c(CC3)c2ccccc12',
                                      'name': 'eburnamenine',
                                      'reason': 'No indole skeleton found'},
                                  {   'smiles': '[H][C@@]12Cc3c[nH]c4cccc(C1=C[C@H](CN2C)C(=O)N[C@@]1(O[C@]2(O)N([C@@H](C(C)CC)C(=O)N5CCC[C@@]25[H])C1=O)C(C)C)c34',
                                      'name': 'beta-ergocryptine',
                                      'reason': 'Molecule contains multiple '
                                                'amide bonds; likely a peptide '
                                                'rather than an indole '
                                                'alkaloid'}],
    'attempt': 3,
    'reasoning': 'Below is one possible improved solution. One idea was to '
                 '“trust” the indole SMARTS match rather than re‐assembling '
                 'the fused rings from the full ring info (which proved too '
                 'strict in several cases). At the same time we want to avoid '
                 'catching peptides (or other non‐alkaloids with a tryptophan '
                 'fragment) that contain an indole “look‐alike”. In this '
                 'version the indole SMARTS pattern is defined as the '
                 'canonical pattern\n'
                 '\u2003\u2003c1ccc2[nH]ccc2c1\n'
                 'and after matching we insist that at least one match has '
                 'either exactly nine atoms (the classical indole fragment) or '
                 'one “extra” atom (to tolerate some fused extension). In '
                 'addition, we count the number of amide bonds (using a simple '
                 'C(=O)N SMARTS) and, if two or more are present, we assume '
                 'the molecule is peptide‐like and reject it. (There are many '
                 'ways to improve and tune the classifier; this is just one '
                 'attempt.) \n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 186,
    'num_false_positives': 1997,
    'num_true_negatives': 139881,
    'num_false_negatives': 236,
    'num_negatives': None,
    'precision': 0.08520384791571232,
    'recall': 0.44075829383886256,
    'f1': 0.14280230326295587,
    'accuracy': 0.9843078004216445,
    'negative_predictive_value': 0.9983156933134452}