"""
Classifies: CHEBI:48927 N-acyl-L-alpha-amino acid
"""
"""
Classifies: N-acyl-L-alpha-amino acid
Definition: Any L-alpha-amino acid carrying an N-acyl substituent.
An L-alpha-amino acid has a chiral alpha‐carbon bonded to an amino group and a free carboxyl group.
The N-acyl substituent is defined as an acyl group (R–C(=O)–) attached directly to the nitrogen,
which must not be part of a peptide bond.
"""

from rdkit import Chem

def is_N_acyl_L_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-acyl L-alpha-amino acid based on its SMILES string.

    The function first attempts to detect an L-alpha-amino acid unit by matching a chiral
    carbon attached to an amino group and a carboxyl group. To avoid peptide chains we
    require that the carboxyl group is “free” (i.e. the carboxyl carbon is not bonded to any nitrogen
    other than that from the backbone). Then, for the amino group bonded to that chiral carbon,
    we search for a substituent that meets the criteria for an N-acyl group: a single-bonded carbon
    that itself is doubly bound to an oxygen, and that is not connected (besides the carbonyl oxygen)
    to another chiral center typical of a peptide bond.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if molecule is a valid N-acyl L-alpha-amino acid, False otherwise.
        str: Reason for classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # SMARTS to capture L-alpha-amino acid backbone:
    # It looks for a chiral carbon ([C@H] or [C@@H]) connected to an amino group (N)
    # and a carboxyl group (C(=O)[O;H,-]), which should be free (not connected to another N).
    aa_smarts = [
        "[C@H](N)(C(=O)[O;H,-])",
        "[C@@H](N)(C(=O)[O;H,-])"
    ]
    backbone_matches = []
    for sm in aa_smarts:
        patt = Chem.MolFromSmarts(sm)
        if patt is None:
            continue
        backbone_matches.extend(mol.GetSubstructMatches(patt))
        
    if not backbone_matches:
        return False, "No L-alpha-amino acid backbone found"

    # Helper function to check if a carbon atom is an acyl carbon
    # i.e. it has a carbonyl oxygen (double-bonded O).
    def has_carbonyl(carbon):
        for bond in carbon.GetBonds():
            # check for double bond to oxygen
            if bond.GetBondType() == Chem.BondType.DOUBLE:
                nbr = bond.GetOtherAtom(carbon)
                if nbr.GetAtomicNum() == 8:
                    return True
        return False

    # Helper: determine if the acyl carbon appears to be part of a peptide bond.
    # In a peptide bond, the acyl carbon is connected to a chiral (alpha) carbon from a neighboring residue.
    def seems_peptide_bond(acyl_carbon, attached_N):
        # Check all heavy neighbors except the one we came from (attached_N) and carbonyl oxygens.
        for nbr in acyl_carbon.GetNeighbors():
            if nbr.GetIdx() == attached_N.GetIdx():
                continue
            # Skip oxygen from carbonyl (double bond)
            if nbr.GetAtomicNum() == 8:
                continue
            # If any neighbor is a chiral carbon with specified chirality, suspect peptide bond.
            if nbr.GetAtomicNum() == 6 and nbr.GetChiralTag() != Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
                return True
        return False

    # When dealing with peptides, the carboxyl group is amide-bound.
    # We require the carboxyl carbon of the backbone to have NO nitrogen neighbor.
    def is_free_carboxyl(carboxyl_carbon):
        for nbr in carboxyl_carbon.GetNeighbors():
            # Skip oxygen neighbors (the carbonyl and hydroxyl oxygen)
            if nbr.GetAtomicNum() == 8:
                continue
            if nbr.GetAtomicNum() == 7:
                return False
        return True

    # For each identified amino acid backbone match, check:
    for match in backbone_matches:
        # Our SMARTS was defined as [C](N)(C(=O)[O;H,-]), so we expect three atoms;
        # assume the first atom in the match is the chiral alpha carbon.
        alpha_idx = match[0]
        alpha_atom = mol.GetAtomWithIdx(alpha_idx)
        # In the match, we expect a nitrogen and a carboxyl-carbon.
        # Distinguish the two by their atomic number and bond environment.
        neighbor_atoms = alpha_atom.GetNeighbors()
        candidate_N = None
        candidate_C_carboxyl = None
        for nbr in neighbor_atoms:
            if nbr.GetAtomicNum() == 7:
                candidate_N = nbr
            elif nbr.GetAtomicNum() == 6:
                # Check if this carbon atom has a carbonyl pattern (i.e., is part of COOH)
                if has_carbonyl(nbr):
                    candidate_C_carboxyl = nbr
        if candidate_N is None or candidate_C_carboxyl is None:
            continue  # not matching a complete AA unit

        # Check that the carboxyl group is free (not involved in peptide bond)
        if not is_free_carboxyl(candidate_C_carboxyl):
            continue  # likely a di-/oligo-peptide

        # Now, for the amine candidate (the N attached to alpha),
        # look at its substituents other than the alpha carbon.
        found_acyl = False
        for nbr in candidate_N.GetNeighbors():
            if nbr.GetIdx() == alpha_atom.GetIdx():
                continue
            # We are looking for a carbon that is connected via a single bond:
            if nbr.GetAtomicNum() != 6:
                continue
            bond = mol.GetBondBetweenAtoms(candidate_N.GetIdx(), nbr.GetIdx())
            if bond is None or bond.GetBondType() != Chem.BondType.SINGLE:
                continue
            acyl_carbon = nbr
            # Check that this carbon has a double-bonded oxygen (i.e. is carbonyl carbon)
            if not has_carbonyl(acyl_carbon):
                continue
            # To exclude peptide bonds (where the acyl carbon is part of the backbone), 
            # check that it is not additionally connected to a chiral carbon.
            if seems_peptide_bond(acyl_carbon, candidate_N):
                continue
            # It appears we found an N-acyl substituent.
            found_acyl = True
            break

        if found_acyl:
            return True, "Contains L-alpha-amino acid backbone with acylated amino group"

    return False, "Found L-alpha-amino acid backbone with free carboxyl group, but amino group is not acylated"

# When run as a script you can test with an example.
if __name__ == "__main__":
    # Example test: N-acetyl-L-aspartic acid
    example_smiles = "CC(=O)N[C@@H](CC(O)=O)C(O)=O"
    result, reason = is_N_acyl_L_alpha_amino_acid(example_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:48927',
                          'name': 'N-acyl-L-alpha-amino acid',
                          'definition': 'Any L-alpha-amino acid carrying an '
                                        'N-acyl substituent.',
                          'parents': ['CHEBI:21644'],
                          'xrefs': ['KEGG:C02850'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 93,
                           'log_lines_of_code': 4.532599493153256,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
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
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
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
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetOtherAtom',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'GetBonds',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetChiralTag',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'extend',
                                                 'GetBondType',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['sm'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_N_acyl_L_alpha_amino_acid(smiles: '
                                       'str):',
                                       'has_carbonyl(carbon):',
                                       'seems_peptide_bond(acyl_carbon, '
                                       'attached_N):',
                                       'is_free_carboxyl(carboxyl_carbon):'],
                           'defs_count': 4,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No L-alpha-amino acid '
                                          'backbone found"',
                                          'True',
                                          'False',
                                          'True',
                                          'False',
                                          'False',
                                          'True',
                                          'False, "Found L-alpha-amino acid '
                                          'backbone with free carboxyl group, '
                                          'but amino group is not acylated"'],
                           'returns_count': 9,
                           'complexity': 6.906519898630651},
    'message': '\n'
               'Attempt failed: F1 score of 0.029668411867364748 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC(=O)N[13C@@H]([13CH2][13C](O)=O)[13C](O)=O NAME: '
               'N-acetyl-L-aspartic acid-1,2,3,4-(13)C4 REASON: CORRECT '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: OC(=O)CC[C@H](NC(=O)C(O)(CC(O)=O)CC(O)=O)C(O)=O '
               'NAME: beta-citrylglutamic acid REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'Nc1nc2ccc(CN(CC#C)c3ccc(cc3)C(=O)N[C@@H](CCC(O)=O)C(O)=O)cc2c(=O)[nH]1 '
               'NAME: CB3717 REASON: CORRECT Contains L-alpha-amino acid '
               'backbone with acylated amino group\n'
               ' * SMILES: '
               '[C@@H]1([C@H](CCC1=O)CC(N[C@H](C(O)=O)[C@H](CC)C)=O)C/C=C\\CCO '
               'NAME: N-[(+)-12-hydroxy-7-isojasmonyl]isoleucine REASON: '
               'CORRECT Contains L-alpha-amino acid backbone with acylated '
               'amino group\n'
               ' * SMILES: '
               'C12=C(C=C(C=C1)C(N3CC=4C(CC3)=C(C(=C(C4)Cl)C(N[C@@H](CC5=CC=CC(=C5)S(C)(=O)=O)C(=O)O)=O)Cl)=O)OC=C2 '
               'NAME: lifitegrast REASON: CORRECT Contains L-alpha-amino acid '
               'backbone with acylated amino group\n'
               ' * SMILES: '
               'C(C(N[C@H](C(O)=O)CCC(=O)O)=O)C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: N-[(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl]-L-glutamic '
               'acid REASON: CORRECT Contains L-alpha-amino acid backbone with '
               'acylated amino group\n'
               ' * SMILES: C(=O)([C@@H](NC(C)=O)CCS(C)(=O)=O)O NAME: '
               'N-acetylmethionine sulfone REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'C1([C@H](CCC1=O)CC(N[C@H](C(O)=O)[C@H](CC)C)=O)C/C=C\\CCO '
               'NAME: N-[(3R)-12-hydroxyjasmonyl]-L-isoleucine REASON: CORRECT '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: [H]C(=O)N[C@@H](CC(O)=O)C(O)=O NAME: '
               'N-formyl-L-aspartic acid REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'C=C(C(N[C@@H](CCC([O-])=O)C(=O)[O-])=O)O[C@H]1C=CC=C([C@@H]1O)C([O-])=O '
               'NAME: isochorismoyl-L-glutamate(3-) REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: C(\\CCCCCCCC(=O)N[C@H](C(O)=O)CC(C)C)=C\\CCCCCCCC '
               'NAME: N-oleoyl-L-leucine REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'C(\\CCCCCCCC(=O)N[C@H](C(O)=O)[C@H](CC)C)=C\\CCCCCCCC NAME: '
               'N-oleoyl-L-isoleucine REASON: CORRECT Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: C(\\CCCCCCCC(=O)N[C@H](C(O)=O)CO)=C\\CCCCCCCC NAME: '
               'N-oleoyl-L-serine REASON: CORRECT Contains L-alpha-amino acid '
               'backbone with acylated amino group\n'
               ' * SMILES: '
               'C1([C@H](CCC1=O)CC(N[C@H](C(O)=O)[C@H](CC)C)=O)C/C=C\\CC NAME: '
               'N-[(3R)-jasmonyl]-L-isoleucine REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: C(=O)([C@@H](NC(=O)CC)CCSC)O NAME: '
               'N-propanoyl-L-methionine REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(N[C@H](C(=O)O)CO)=O '
               'NAME: N-arachidonoyl-L-serine REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: C([C@@H](NC(=O)CC(C)C)C)(=O)O NAME: '
               'N-isovaleryl-L-alanine REASON: CORRECT Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: CC(=O)C(N[C@@H](CCC([O-])=O)C(=O)[O-])=O NAME: '
               'N-pyruvoyl-L-glutamate REASON: CORRECT Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: OC(=O)[C@H](CCS(=N)(=O)C)NC(C)=O NAME: '
               'N-acetyl-L-methionine sulfoximine REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'Nc1nc(=O)c2c(CCc3ccc(cc3)C(=O)N[C@@H](CCC(O)=O)C(O)=O)c[nH]c2[nH]1 '
               'NAME: pemetrexed REASON: CORRECT Contains L-alpha-amino acid '
               'backbone with acylated amino group\n'
               ' * SMILES: '
               'C(C(O)=O)C[C@@H](C(=O)O)NC(C1=CC=C(C=C1)S(N2CCC[C@@H]2C(=O)O)(=O)=O)=O '
               'NAME: N-[4-(D-prolinosulfonyl)benzoyl]-L-glutamic acid REASON: '
               'CORRECT Contains L-alpha-amino acid backbone with acylated '
               'amino group\n'
               ' * SMILES: C[C@H](NC(=O)Cc1c[nH]c2ccccc12)C(O)=O NAME: '
               'N-(indole-3-acetyl)-L-alanine REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: NCCCC(=O)N[C@@H](Cc1c[nH]cn1)C(O)=O NAME: '
               'L-homocarnosine REASON: CORRECT Contains L-alpha-amino acid '
               'backbone with acylated amino group\n'
               ' * SMILES: C(N[C@H](C(O)=O)CC(=O)O)(=O)CC1C(=O)NC2=C1C=CC=C2 '
               'NAME: N-(2-oxindole-3-acetyl)-L-aspartic acid REASON: CORRECT '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: CC(=O)N[C@@H](CC(O)=O)C(O)=O NAME: '
               'N-acetyl-L-aspartic acid REASON: CORRECT Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               'False positives: SMILES: '
               'O=C(NCC(=O)N[C@@H](CO)C(O)=O)[C@@H](N)CC=1NC=NC1 NAME: '
               'His-Gly-Ser REASON: WRONGLY CLASSIFIED Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: '
               'C1=CC(=CC=C1C(=O)NC(CCC(=O)NC(CCC(=O)NC(CCC(=O)O)C(=O)O)C(=O)O)C(=O)O)NCC2=CN=C3C(=N2)C(=O)NC(=N3)N '
               'NAME: Pteropterin REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'O=C(NC(C(=O)O)CC(=O)N)/C(=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/[C@H]1N=C(/C=C/C=2NC=CC2)O[C@@H]1C)/C '
               'NAME: DKxanthene 556 REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'O=C(NC(C(=O)O)CCC(=O)N)/C=C/C=C/C1=CC=C([N+]([O-])=NC2=CC=C(/C=C/C=C/C(=O)NC(C(=O)O)CCC(=O)N)C=C2)C=C1 '
               'NAME: Azoxymycin A REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'O=C(NC(CCCN=C(N)N)C(O)=O)C(NC(=O)C(NC(=O)C1=CC=CC=C1)CC2=CC=CC=C2)CC(C)C '
               'NAME: Phe(benzoyl)-leu-arg REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'O=C(NCC(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](N)CCCCN '
               'NAME: Lys-Gly-Trp REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: O=C(NC(CCC(=O)N)C(O)=O)CCCCCCC/C=C/C\\C=C\\CCCCC '
               'NAME: N-Linoleoyl Glutamine REASON: WRONGLY CLASSIFIED '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: '
               'O=C(NCC(=O)NC(C(=O)NC(CC1=CC=C(O)C=C1)C(O)=O)CO)C(N)CC=2C=3C(NC2)=CC=CC3 '
               'NAME: Trp Gly Ser Tyr REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: CC(=O)N[C@@H](CCP([O-])=O)C([O-])=O NAME: '
               'N-Acetyldemethylphosphinothricinate (2-) REASON: WRONGLY '
               'CLASSIFIED Contains L-alpha-amino acid backbone with acylated '
               'amino group\n'
               ' * SMILES: '
               'CC(=O)NC(CS[C@H](\\C=C\\C=C\\C=C/C\\C=C/CCCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O '
               'NAME: omega-Carboxy-N-acetyl-LTE4 REASON: WRONGLY CLASSIFIED '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: C(O)([C@@H](NC(C)=O)CSC(C(O)=O)CC(=O)O)=O NAME: '
               'N-acetyl-S-(2-succino)-L-cysteine REASON: WRONGLY CLASSIFIED '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: '
               'O=C1N(C(C(=O)N(C(C(=O)NC(C(=O)NCCCCC(C(NC1C(CC)C)=O)NC(=O)NC(C(=O)O)CCCCN)CC2=CC=CC=C2)CC(=O)N)C)CCC3=CC=CC=C3)C '
               'NAME: Anabaenopeptin 864 REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'ClC1=C(O)C=CC(=C1)CC[C@@H]2NC(=O)C(NC(=O)[C@H](NC(=O)N[C@H](C(=O)O)CC3=CC=CC=C3)CCCCNC([C@@H](NC(CN(C2=O)C)=O)CCC4=CC=CC=C4)=O)[C@@H](CC)C '
               'NAME: Anabaenopeptin SA9 REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: SC[C@H](N)C(=O)NCC(=O)N[C@@H](CCC(=O)N)C(O)=O NAME: '
               'Cys-Gly-Gln REASON: WRONGLY CLASSIFIED Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: '
               'OC(=O)C(NC(=O)C1=CC=C(N(CC2=NC=3C(NC2=O)=NC(=NC3N)N)C)C=C1)CCC(O)=O '
               'NAME: 7-Hydroxymethotrexate REASON: WRONGLY CLASSIFIED '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: O=C(O)[C@@H](NC(=O)CCCCCCCCCC(C)C)CC(=O)N NAME: '
               'Lipoamide C REASON: WRONGLY CLASSIFIED Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: S(CCC(NC(=O)CCCCCCCCCCCCCCCCC)C(O)=O)C NAME: '
               'N-Stearoyl Methionine REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'OC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](N)CC(=O)N)CCCN=C(N)N NAME: '
               'Asn-Gly-Arg REASON: WRONGLY CLASSIFIED Contains L-alpha-amino '
               'acid backbone with acylated amino group\n'
               ' * SMILES: S(C[C@H](NC(=O)C)C(O)=O)CC(O)C NAME: '
               'N-Acetyl-S-(2-hydroxypropyl)-cysteine REASON: WRONGLY '
               'CLASSIFIED Contains L-alpha-amino acid backbone with acylated '
               'amino group\n'
               ' * SMILES: '
               'O=C(NC(CC(O)=O)C(=O)NC(CC=1NC=NC1)C(O)=O)C(NC(=O)C(N)CC(=O)N)CC=2C=3C(NC2)=CC=CC3 '
               'NAME: Asn-Trp-Asp-His REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'COc1cc(O)c2C(=O)c3cc4[C@H](O)[C@@H](O)c5cc(C)c(C(=O)NC(C)C(O)=O)c(O)c5-c4c(O)c3C(=O)c2c1 '
               'NAME: Pradimicinone I REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(N[C@H](C(=O)O)CC1=CC=CC=C1)=O '
               'NAME: N-arachidonoyl-L-phenylalanine REASON: WRONGLY '
               'CLASSIFIED Contains L-alpha-amino acid backbone with acylated '
               'amino group\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)N[C@H](C(=O)NCCCC[C@H](C(N[C@H](C(N[C@H]1CCC2=CC=CC=C2)=O)[C@H](CC)C)=O)NC(=O)N[C@H](C(=O)O)CC3=CC=C(O)C=C3)[C@H](CC)C)CCC4=CC=C(O)C=C4)C '
               'NAME: Anabaenopeptin MM913 REASON: WRONGLY CLASSIFIED Contains '
               'L-alpha-amino acid backbone with acylated amino group\n'
               ' * SMILES: '
               'Cc1c(CC(=O)NCCCC[C@H](NC(=O)CCN)C(O)=O)c(=O)oc2cc(N)ccc12 '
               'NAME: beta-Ala-Lys-N(epsilon)-AMCA REASON: WRONGLY CLASSIFIED '
               'Contains L-alpha-amino acid backbone with acylated amino '
               'group\n'
               ' * SMILES: '
               'C[C@H](CCC(=O)N[C@@H](CC(O)=O)C(O)=O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: aspartylochenodeoxycholic acid REASON: WRONGLY '
               'CLASSIFIED Contains L-alpha-amino acid backbone with acylated '
               'amino group\n'
               'False negatives: SMILES: '
               'C(=O)([C@@H](N)CCCCNC([C@H]1[C@@H](CC=N1)C)=O)O NAME: '
               'L-pyrrolysine REASON: MISSED Found L-alpha-amino acid '
               'backbone, but amino group is not acylated\n'
               ' * SMILES: C(O)([C@@H](N)CCCCNC(C(O)(C)C)=O)=O NAME: '
               'N(6)-(2-hydroxyisobutanoyl)-L-lysine REASON: MISSED Found '
               'L-alpha-amino acid backbone, but amino group is not acylated\n'
               ' * SMILES: N[C@@H](CCCCNC(=O)[C@@H](N)CCS)C(O)=O NAME: '
               'N(6)-L-homocysteinyl-L-lysine REASON: MISSED Found '
               'L-alpha-amino acid backbone, but amino group is not acylated\n'
               ' * SMILES: N[C@@H](CCCCNC(=O)CCCCC1CCSS1)C(O)=O NAME: '
               'N(6)-lipoyl-L-lysine REASON: MISSED Found L-alpha-amino acid '
               'backbone, but amino group is not acylated\n'
               ' * SMILES: C(C(NCCCC[C@@H](C(O)=O)N)=O)(C)O NAME: '
               'N(6)-lactoyl-L-lysine REASON: MISSED Found L-alpha-amino acid '
               'backbone, but amino group is not acylated\n'
               ' * SMILES: CC(=O)NCCCC[C@H](NCc1c(COP(O)(O)=O)cnc(C)c1O)C(O)=O '
               "NAME: N(6)-acetyl-N(2)-(5'-phosphopyridoxyl)-L-lysine REASON: "
               'MISSED Found L-alpha-amino acid backbone, but amino group is '
               'not acylated\n'
               ' * SMILES: CC(=O)NCCCC[C@H](N)C(O)=O NAME: '
               'N(6)-acetyl-L-lysine REASON: MISSED Found L-alpha-amino acid '
               'backbone, but amino group is not acylated\n'
               ' * SMILES: N[C@@H](CCCCNC(=O)Cc1c[nH]c2ccccc12)C(O)=O NAME: '
               'N(6)-[(indol-3-yl)acetyl]-L-lysine REASON: MISSED Found '
               'L-alpha-amino acid backbone, but amino group is not acylated\n'
               ' * SMILES: N[C@@H](CCCCNC(=O)C(F)(F)F)C(O)=O NAME: '
               'N(6)-trifluoroacetyl-L-lysine REASON: MISSED Found '
               'L-alpha-amino acid backbone, but amino group is not acylated\n'
               ' * SMILES: O=C(CC[C@H](N)C(O)=O)NCCCC[C@H](N)C(O)=O NAME: '
               'epsilon-(gamma-glutamyl)lysine REASON: MISSED Found '
               'L-alpha-amino acid backbone, but amino group is not acylated\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No L-alpha-amino acid backbone '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C(=O)([C@@H](N)CCCCNC([C@H]1[C@@H](CC=N1)C)=O)O',
                                      'name': 'L-pyrrolysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'C(O)([C@@H](N)CCCCNC(C(O)(C)C)=O)=O',
                                      'name': 'N(6)-(2-hydroxyisobutanoyl)-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'N[C@@H](CCCCNC(=O)[C@@H](N)CCS)C(O)=O',
                                      'name': 'N(6)-L-homocysteinyl-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'N[C@@H](CCCCNC(=O)CCCCC1CCSS1)C(O)=O',
                                      'name': 'N(6)-lipoyl-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'C(C(NCCCC[C@@H](C(O)=O)N)=O)(C)O',
                                      'name': 'N(6)-lactoyl-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'CC(=O)NCCCC[C@H](NCc1c(COP(O)(O)=O)cnc(C)c1O)C(O)=O',
                                      'name': "N(6)-acetyl-N(2)-(5'-phosphopyridoxyl)-L-lysine",
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'CC(=O)NCCCC[C@H](N)C(O)=O',
                                      'name': 'N(6)-acetyl-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'N[C@@H](CCCCNC(=O)Cc1c[nH]c2ccccc12)C(O)=O',
                                      'name': 'N(6)-[(indol-3-yl)acetyl]-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'N[C@@H](CCCCNC(=O)C(F)(F)F)C(O)=O',
                                      'name': 'N(6)-trifluoroacetyl-L-lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'},
                                  {   'smiles': 'O=C(CC[C@H](N)C(O)=O)NCCCC[C@H](N)C(O)=O',
                                      'name': 'epsilon-(gamma-glutamyl)lysine',
                                      'reason': 'Found L-alpha-amino acid '
                                                'backbone with free carboxyl '
                                                'group, but amino group is not '
                                                'acylated'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before the code block. In our '
                 'previous attempt the algorithm simply looked for any amino '
                 'acid‐like backbone and then checked for a substituent on any '
                 'nearby N that looked “acyl”. That approach gave many false '
                 'positives because many peptide bonds (and even other '
                 'backbone fragments) satisfy a very loose pattern. Also, some '
                 'naturally “N‐acyl” amino acid derivatives (true positives) '
                 'may have only one nitrogen on the backbone while many '
                 'peptides (false positives) contain many amide bonds that '
                 'mimic an N‐acyl bond. To improve the performance we now do '
                 'the following:\n'
                 '\n'
                 '1. We use a SMARTS pattern to capture an L‑α‑amino acid '
                 '“unit” but we further require that the carboxyl group is '
                 'free (i.e. not involved in a peptide bond). (A peptide will '
                 'have an extra amide bond at the C‑terminal side.)\n'
                 '2. We then focus on the amino nitrogen that is attached to '
                 'the chiral α‑carbon. For each such N, we require that (a) '
                 'besides the connection to the α‑carbon the N is bound via a '
                 'single bond to a carbon and that that carbon bears a '
                 'double‐bonded oxygen (an acyl carbon) and (b) that this acyl '
                 'carbon is not further connected (besides the carbonyl O and '
                 'the “R” group) to another chiral center (which would '
                 'indicate participation in a peptide bond).\n'
                 '3. Only if an L‑α‑amino acid unit with a free acid and an '
                 'N‐acyl substituent is found do we accept the molecule.\n'
                 '\n'
                 'This should reduce both false positives (peptide chains and '
                 'multifunctional amides) and false negatives (cases where the '
                 'acyl group is a simple acyl, like acetyl or oleoyl, as long '
                 'as the carboxyl group remains “free”). \n'
                 '\n'
                 'Below is the complete Python code implementing these ideas.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 34,
    'num_false_positives': 2208,
    'num_true_negatives': 140047,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.015165031222123104,
    'recall': 0.7555555555555555,
    'f1': 0.029733275032794052,
    'accuracy': 0.9844061841180605,
    'negative_predictive_value': 0.9999214611089692}