"""
Classifies: CHEBI:46633 carbapenems
"""
"""
Classifies: Carbapenems (beta-lactam antibiotics that have a carbapenem skeleton,
which is a four-membered beta-lactam ring fused to a five-membered ring lacking sulfur
and containing a C=C bond in the 5-membered ring).

The approach:
1. Parse the SMILES.
2. Identify a candidate beta-lactam ring (a ring of size 4 that contains exactly one nitrogen
   and at least one carbon (C) that is double-bonded to an oxygen (C=O)).
3. Look for a fused five-membered ring (ring of size 5) sharing at least 2 atoms with the beta-lactam;
   the five-membered ring must not contain any sulfur and must contain at least one C=C double bond.
4. If both are found, return True and a reason; otherwise, return False.
"""

from rdkit import Chem

def is_carbapenems(smiles: str):
    """
    Determines if a molecule has the carbapenem bicyclic skeleton based on its SMILES string.
    It looks for a candidate beta-lactam ring (4-membered with one nitrogen and a carbonyl) fused
    to a 5-membered ring that (a) is free of sulfur and (b) contains at least one carbon-carbon double bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule appears to be a carbapenem, False otherwise.
        str: Reason for the classification.
    """
    # Parse SMILES string to molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()

    beta_lactam_candidate = None

    # Identify a candidate beta-lactam ring: 4-membered, exactly one nitrogen,
    # and at least one carbon (C) in the ring which is double-bonded to an oxygen.
    for ring in rings:
        if len(ring) != 4:
            continue
        # Check for exactly one nitrogen in the ring.
        n_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 7)
        if n_count != 1:
            continue

        carbonyl_found = False
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # Check only carbon atoms
            if atom.GetAtomicNum() == 6:
                # Look through bonds for a double bond to oxygen.
                for bond in atom.GetBonds():
                    if bond.GetBondType() == Chem.BondType.DOUBLE:
                        nbr = bond.GetOtherAtom(atom)
                        if nbr.GetAtomicNum() == 8:
                            carbonyl_found = True
                            break
                if carbonyl_found:
                    break
        if not carbonyl_found:
            continue

        # Candidate beta-lactam ring found.
        beta_lactam_candidate = set(ring)
        break

    if beta_lactam_candidate is None:
        return False, "No four-membered beta-lactam ring (with one nitrogen and carbonyl) found"

    # Look for a fused 5-membered ring that meets additional criteria.
    fused_ring_found = False
    for ring in rings:
        if len(ring) != 5:
            continue
        ring_set = set(ring)
        # Check that the ring and the beta-lactam candidate share at least 2 atoms (fused rings)
        if len(beta_lactam_candidate.intersection(ring_set)) < 2:
            continue
        # Exclude rings containing sulfur (atomic number 16).
        if any(mol.GetAtomWithIdx(idx).GetAtomicNum() == 16 for idx in ring):
            continue

        # Additionally, require that within this 5-membered ring there is a carbon-carbon double bond.
        # Iterate over bonds whose both atoms are in the ring.
        has_CC_double = False
        for bond in mol.GetBonds():
            a1 = bond.GetBeginAtom()
            a2 = bond.GetEndAtom()
            if a1.GetIdx() in ring_set and a2.GetIdx() in ring_set:
                # Check if both are carbons and bond is double.
                if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 6 and bond.GetBondType() == Chem.BondType.DOUBLE:
                    has_CC_double = True
                    break
        if not has_CC_double:
            continue

        # Found a fused 5-membered ring fulfilling all conditions.
        fused_ring_found = True
        break

    if not fused_ring_found:
        return False, "No fused five-membered ring (free of sulfur and containing a C=C bond) found with the beta-lactam ring; not a carbapenem skeleton"

    return True, "Found carbapenem bicyclic skeleton (4-membered beta-lactam fused to a sulfur-free 5-membered ring with C=C bond)"

# Example usage (for quick ad-hoc testing)
if __name__ == "__main__":
    # 1beta-methylcarbapenem example
    test_smiles = "[H][C@@]12CC(=O)N1C=C[C@@H]2C"
    result, reason = is_carbapenems(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:46633',
                          'name': 'carbapenems',
                          'definition': 'The class of beta-lactam antibiotics '
                                        'that whose members have a carbapenem '
                                        'skeleton which is variously '
                                        'substituted at positions 3, 4, and 6.',
                          'parents': [   'CHEBI:27171',
                                         'CHEBI:27933',
                                         'CHEBI:38101'],
                          'xrefs': [   'PMID:18076336',
                                       'PMID:19199922',
                                       'PMID:19610642',
                                       'PMID:19617229',
                                       'PMID:19929840',
                                       'PMID:21859938',
                                       'Wikipedia:Carbapenem'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 47,
                           'log_lines_of_code': 3.8501476017100584,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
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
                                                 0,
                                                 0,
                                                 1,
                                                 2,
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
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'intersection',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'GetRingInfo'],
                           'methods_called_count': 6,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_carbapenems(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No four-membered '
                                          'beta-lactam ring (with one nitrogen '
                                          'and carbonyl) found"',
                                          'False, "No fused five-membered ring '
                                          '(free of sulfur and containing a '
                                          'C=C bond) found with the '
                                          'beta-lactam ring; not a carbapenem '
                                          'skeleton"',
                                          'True, "Found carbapenem bicyclic '
                                          'skeleton (4-membered beta-lactam '
                                          'fused to a sulfur-free 5-membered '
                                          'ring with C=C bond)"'],
                           'returns_count': 4,
                           'complexity': 3.570029520342012},
    'message': '\n'
               'Attempt failed: F1 score of 0.7131782945736435 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'S(C1=C(N2C(=O)[C@@H]([C@H]2C1)CC)C(=O)O)CCNC(=O)CCNC(=O)[C@H](O)C(CO)(C)C '
               'NAME: OA-6129 A REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: C[C@H](O)[C@H]1[C@H]2CC(SCCNC(C)=O)=C(N2C1=O)C(O)=O '
               'NAME: Epithienamycin A REASON: CORRECT Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'N12[C@@]([C@](C(C)O)(C1=O)[H])(C[C@@H]([C@@H]2C(O)=O)SCCNC(CCNC([C@@H](C(CO)(C)C)O)=O)=O)[H] '
               'NAME: OA-6129 D REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'P(=O)(OC12N(C(C(=O)OCC3=CC=C([N+](=O)[O-])C=C3)=C(C1(OC4=CC=CC=C4)C)OC5=CC=CC=C5)C(=O)C2C(O)C)(O)O '
               'NAME: Proteinase K REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: [H][C@@]12CC(=O)N1C=C[C@@H]2C NAME: '
               '1beta-methylcarbapenem REASON: CORRECT Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'C[C@H](O)[C@H]1[C@H]2CC(S\\C=C\\NC(C)=O)=C(N2C1=O)C(O)=O NAME: '
               'Epithienamycin B REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'S(=O)(=O)(OC([C@@H]1C(=O)N2C(C(=O)O)=C(C[C@H]12)S(=O)CCNC(=O)C)(C)C)O '
               'NAME: Carpetimycin D REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'CC(O)C1C2C(C)C(SC3NC(CS3)C(=O)Nc3cccc(c3)C(O)=O)=C(N2C1=O)C(O)=O '
               'NAME: MK826 REASON: CORRECT Found carbapenem bicyclic skeleton '
               '(4-membered beta-lactam fused to a sulfur-free 5-membered '
               'ring)\n'
               ' * SMILES: '
               'S(=O)(=O)(OC([C@@H]1C(=O)N2C(C(=O)O)=C(C[C@H]12)S(=O)/C=C/NC(=O)C)(C)C)O '
               'NAME: Carpetimycin B REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'S(=O)(=O)(OC(C1C(=O)N2C(C(=O)O)=C(CC12)S(=O)/C=C/NC(=O)C)C)O '
               'NAME: MM 4550 REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: [H][C@]12CC=C(N1C(=O)C2)C(O)=O NAME: '
               '1-carbapenem-3-carboxylic acid REASON: CORRECT Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'S(C1=C(N2C(=O)C(C2C1C)C(O)C)C(=O)[O-])C3CNC(C3)C(=O)NC4=CC(C(=O)[O-])=CC=C4.[Na+].[Na+] '
               'NAME: Ertapenem Disodium REASON: CORRECT Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'C[C@@H](O)[C@@H]1[C@H]2[C@@H](C)C(S[C@@H]3CN[C@@H](C3)CNS(N)(=O)=O)=C(N2C1=O)C(O)=O '
               'NAME: doripenem REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'S(C1[C@@H](N2C(=O)C(C2C1)[C@@H](O)C)C(=O)O)CCNC(=O)C NAME: '
               '17927 D REASON: CORRECT Found carbapenem bicyclic skeleton '
               '(4-membered beta-lactam fused to a sulfur-free 5-membered '
               'ring)\n'
               ' * SMILES: '
               'S(=O)(C1=C(N2C(=O)[C@@H]([C@H]2C1)C(O)(C)C)C(=O)O)CCNC(=O)C '
               'NAME: Carpetimycin C REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'N12[C@@]([C@]([C@@H](OS(O)(=O)=O)C)(C1=O)[H])(CC(=C2C(O)=O)SCCN)[H] '
               'NAME: Deacetylepithienamycin F REASON: CORRECT Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'N12[C@@]([C@@H](CC)C1=O)(CC(=C2C(O)=O)SCCNC(C)=O)[H] NAME: '
               'PS-5 REASON: CORRECT Found carbapenem bicyclic skeleton '
               '(4-membered beta-lactam fused to a sulfur-free 5-membered '
               'ring)\n'
               ' * SMILES: CC[C@@H]1[C@H]2CC(SCCN)=C(N2C1=O)C(O)=O NAME: NS-5 '
               'REASON: CORRECT Found carbapenem bicyclic skeleton (4-membered '
               'beta-lactam fused to a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               '[C@@H]1(SC2=C(N3C([C@]([C@]3([C@H]2C)[H])([H])[C@@H](C)O)=O)C(O)=O)CNC(C1)[C@H](O)CCNC.Cl.O '
               'NAME: BO 2727 REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: NCCSC1=C(N2[C@H](C1)[C@@H](CO)C2=O)C(O)=O NAME: '
               'Northienamycin REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'S(C1=C(N2C(=O)C(C2C1C)C(O)C)C(=O)O)C3CNC(C3)C(=O)N(C)C.[Na+].[Na+].O=C([O-])[O-] '
               'NAME: Meropenem sodium carbonate REASON: CORRECT Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'S(=O)(C1=C(N2C(=O)\\C(\\C2C1)=C(\\CO)/C)C(=O)O)CCNC(=O)C NAME: '
               'Asparenomycin B REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'C[C@@H](O)[C@@H]1[C@H]2[C@@H](C)C(Sc3nc(cs3)-c3cc[n+](CC(N)=O)cc3)=C(N2C1=O)C(O)=O '
               'NAME: SM-17466 REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'C[C@@H](O)[C@@H]1[C@H]2CC(SCCNC(C)=O)=C(N2C1=O)C(O)=O NAME: '
               'N-Acetylthienamycin REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'C[C@H](O)[C@@H]1[C@H]2CC(SCCNC(C)=O)=C(N2C1=O)C(O)=O NAME: '
               'Epithienamycin C REASON: CORRECT Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               'False positives: SMILES: '
               'N12[C@](CC1=O)(C[C@H]([C@H]2C(=O)[O-])SCCNC(CCNC(=O)[C@@H](C(CO)(C)C)O)=O)[H] '
               'NAME: (2R,3R,5S)-2-(S-pantetheinyl)-carbapenam-3-carboxylate '
               'REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic skeleton '
               '(4-membered beta-lactam fused to a sulfur-free 5-membered '
               'ring)\n'
               ' * SMILES: OCC[C@H]1CN2[C@H](CC2=O)O1 NAME: '
               '2-Hydroxyethylclavam REASON: WRONGLY CLASSIFIED Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               '[H][C@]12CC(=O)N1[C@@H]([C@@H](CC[NH3+])O2)C([O-])=O NAME: '
               'dihydroclavaminic acid zwitterion REASON: WRONGLY CLASSIFIED '
               'Found carbapenem bicyclic skeleton (4-membered beta-lactam '
               'fused to a sulfur-free 5-membered ring)\n'
               ' * SMILES: C1(C(N2C1CC(C2C(O)=O)SCCN)=O)CC NAME: '
               '3-[(2-aminoethyl)sulfanyl]-6-ethyl-7-oxo-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: S(C1C(N2C(C1)C(C2=O)=C)C(O)=O)CCN NAME: Carbapenem '
               'biosynthesis intermediate 3 REASON: WRONGLY CLASSIFIED Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'CC(=O)NCCC[C@H](N)C(=O)N[C@@H](C(O)[C@H]1CN2[C@H](CC2=O)O1)C(O)=O '
               'NAME: Clavamycin F REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: CC1C2CC(CN2C1=O)SCCN NAME: '
               '3-[(2-aminoethyl)thio]-6-methyl-1-azabicyclo[3.2.0]heptan-7-one '
               'REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic skeleton '
               '(4-membered beta-lactam fused to a sulfur-free 5-membered '
               'ring)\n'
               ' * SMILES: '
               'NCC(O)C(O)[C@H](N)C(=O)N[C@@H](C(O)[C@H]1CN2[C@H](CC2=O)O1)C(O)=O '
               'NAME: Clavamycin C REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'CC(C)[C@H](N)C(=O)NC(C(O)C[C@H]1CN2[C@H](CC2=O)O1)C(O)=O NAME: '
               'Valclavam REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: [H][C@]12CC=C(N1C(=O)C2)C([O-])=O NAME: '
               '(5R)-carbapenem-3-carboxylate REASON: WRONGLY CLASSIFIED Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: C1[C@@H]2N(C1=O)[C@H](C(=CCO)O2)C(=O)O NAME: '
               '(2R,5R)-3-(2-hydroxyethylidene)-7-oxo-4-oxa-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'C[C@H](N)C(=O)N[C@@H](C(O)[C@H]1CN2[C@H](CC2=O)O1)C(O)=O NAME: '
               'Clavamycin E REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: OC[C@H]1CN2[C@H](CC2=O)O1 NAME: '
               '2-Hydroxymethylclavam REASON: WRONGLY CLASSIFIED Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: [O-]C(=O)[C@@H]1N2[C@@H](CC2=O)O\\C1=C/C=O NAME: '
               'clavaldehyde(1-) REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               '[H][C@]1(C[NH2+][C@@]([H])(C1)C(=O)Nc1cccc(c1)C([O-])=O)SC1=C(N2C(=O)[C@]([H])([C@@H](C)O)[C@@]2([H])[C@H]1C)C([O-])=O '
               'NAME: ertapenem(1-) REASON: WRONGLY CLASSIFIED Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'CC(C)[C@H](N)C(=O)N[C@@H](C(O)[C@H]1CN2[C@H](CC2=O)O1)C(O)=O '
               'NAME: Clavamycin D REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: S(C1C[C@]2(N(C1C(O)=O)C(=O)C2)[H])CCN NAME: '
               '(5S)-3-(2-Aminoethylsulfanyl)-7-oxo-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: C1(C(N2C1CC(C2C(O)=O)SCCN)=O)C NAME: '
               '3-[(2-aminoethyl)sulfanyl]-6-methyl-7-oxo-1-azabicyclo[3.2.0]heptane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: '
               'O1[C@@]2(N(C[C@@H]1CC(O)C(NC(=O)C(N)C(C)C)C(O)=O)C(=O)C2)[H] '
               'NAME: '
               '2-[(2-Amino-3-methylbutanoyl)amino]-3-hydroxy-4-[(3S,5S)-7-oxo-4-oxa-1-azabicyclo[3.2.0]heptan-3-yl]butanoic '
               'acid REASON: WRONGLY CLASSIFIED Found carbapenem bicyclic '
               'skeleton (4-membered beta-lactam fused to a sulfur-free '
               '5-membered ring)\n'
               ' * SMILES: S(C1C(N2C(C1)/C(/C2=O)=C/C)C(O)=O)CCN NAME: '
               'Carbapenem biosynthesis intermediate 4 REASON: WRONGLY '
               'CLASSIFIED Found carbapenem bicyclic skeleton (4-membered '
               'beta-lactam fused to a sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               '[Na+].[H][C@]1(C[NH2+][C@@]([H])(C1)C(=O)Nc1cccc(c1)C([O-])=O)SC1=C(N2C(=O)[C@]([H])([C@@H](C)O)[C@@]2([H])[C@H]1C)C([O-])=O '
               'NAME: ertapenem sodium REASON: WRONGLY CLASSIFIED Found '
               'carbapenem bicyclic skeleton (4-membered beta-lactam fused to '
               'a sulfur-free 5-membered ring)\n'
               ' * SMILES: [H][C@]12CC(=O)N1[C@H](C(O)=O)\\C(O2)=C\\CN NAME: '
               'clavaminic acid REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: '
               'NC[C@@H](O)C(O)[C@@H](NC(=O)[C@H](N)C(O)[C@H]1CN2[C@H](CC2=O)O1)C(O)=O '
               'NAME: Clavamycin B REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: [H][C@@]12CC(=O)N1[C@@H](C([O-])=O)\\C(O2)=C\\CO '
               'NAME: clavulanate REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               ' * SMILES: OC(=O)[C@@H]1N2[C@@H](CC2=O)O\\C1=C/C=O NAME: '
               'clavaldehyde REASON: WRONGLY CLASSIFIED Found carbapenem '
               'bicyclic skeleton (4-membered beta-lactam fused to a '
               'sulfur-free 5-membered ring)\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No four-membered beta-lactam '
                                               'ring (with one nitrogen and '
                                               'carbonyl) found'}],
    'sample_false_negatives': [   {   'smiles': 'N12[C@@]([C@](C(C)O)(C1=O)[H])(C[C@@H]([C@@H]2C(O)=O)SCCNC(CCNC([C@@H](C(CO)(C)C)O)=O)=O)[H]',
                                      'name': 'OA-6129 D',
                                      'reason': 'No fused five-membered ring '
                                                '(free of sulfur and '
                                                'containing a C=C bond) found '
                                                'with the beta-lactam ring; '
                                                'not a carbapenem skeleton'},
                                  {   'smiles': 'S(C1[C@@H](N2C(=O)C(C2C1)[C@@H](O)C)C(=O)O)CCNC(=O)C',
                                      'name': '17927 D',
                                      'reason': 'No fused five-membered ring '
                                                '(free of sulfur and '
                                                'containing a C=C bond) found '
                                                'with the beta-lactam ring; '
                                                'not a carbapenem skeleton'},
                                  {   'smiles': 'N12C(C(C(C)O)C1=O)CC(C2C(O)=O)SCCN',
                                      'name': '2,3-Dihydrothienamycin',
                                      'reason': 'No fused five-membered ring '
                                                '(free of sulfur and '
                                                'containing a C=C bond) found '
                                                'with the beta-lactam ring; '
                                                'not a carbapenem skeleton'}],
    'attempt': 1,
    'reasoning': 'We can try to improve the prior approach by adding extra '
                 'structural constraints. One key difference between true '
                 'carbapenems and the false‐positive clavams is that '
                 'carbapenems (for example, 1β‑methylcarbapenem or '
                 '1‑carbapenem‑3‑carboxylic acid) have a distinct unsaturation '
                 'in the five‐membered ring—that is, a carbon–carbon double '
                 'bond—whereas many of the clavams are fully saturated. In the '
                 'improved code below, after we identify a candidate β‑lactam '
                 '(a four‐membered ring containing one nitrogen and a carbonyl '
                 'group), we look for a fused five‐membered ring that (1) '
                 'shares at least two atoms with the β‑lactam ring, (2) does '
                 'not contain any sulfur atoms, and (3) contains at least one '
                 'carbon–carbon double bond. (Other unusual ring systems will '
                 'be rejected.) This extra requirement should help lower the '
                 'rate of false positives.\n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 43,
    'num_false_positives': 6,
    'num_true_negatives': 142248,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.8775510204081632,
    'recall': 0.9347826086956522,
    'f1': 0.9052631578947369,
    'accuracy': 0.9999367533380182,
    'negative_predictive_value': 0.999978910517325}