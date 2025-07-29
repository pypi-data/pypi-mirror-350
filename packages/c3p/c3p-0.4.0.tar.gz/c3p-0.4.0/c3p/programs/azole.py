"""
Classifies: CHEBI:68452 azole
"""
"""
Classifies: azole
Defined as: any monocyclic heteroarene consisting of a five‐membered aromatic ring 
that contains at least one nitrogen. (The ring may include O or S but no other elements.)
To reduce false positives from large multicyclic molecules or peptides,
this version requires that the candidate five‐membered ring is “non‐fused”
(i.e. not sharing ≥2 atoms with another ring) and that it makes up at least 10% of the molecule’s heavy atoms.
Additionally, if the molecule contains ≥4 amide bonds it is assumed to be a peptide,
and the candidate azole is rejected.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_azole(smiles: str):
    """
    Determines if a molecule is (essentially) an azole based on its SMILES string.
    
    Our algorithm checks for a five‐membered aromatic heterocycle (with C, N, O, S only),
    containing at least one nitrogen. In order to filter out false positives that are large molecules
    (in which an azole fragment would be only a small substituent) or peptides (with many amide bonds),
    we require that:
      1. The candidate ring is non‐fused (not sharing ≥2 atoms with any other ring)
      2. The five‐membered ring accounts for at least 10% of the heavy atoms.
      3. The molecule does not contain 4 or more amide bonds.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if the molecule is classified as an azole, False otherwise.
        str: Explanation of the classification decision.
    """
    # Parse SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    try:
        Chem.SanitizeMol(mol)
    except Exception as e:
        return False, f"Sanitization failed: {str(e)}"

    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    if not all_rings:
        return False, "No rings found in the molecule"
    
    # Allowed atomic numbers: C=6, N=7, O=8, S=16
    allowed_atoms = {6, 7, 8, 16}
    candidate_rings = []
    # First, find rings that are exactly five atoms, aromatic,
    # contain only allowed elements, and have at least one nitrogen.
    for ring in all_rings:
        if len(ring) != 5:
            continue
        ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if not all(atom.GetIsAromatic() for atom in ring_atoms):
            continue
        if not all(atom.GetAtomicNum() in allowed_atoms for atom in ring_atoms):
            continue
        if not any(atom.GetAtomicNum() == 7 for atom in ring_atoms):
            continue
        candidate_rings.append(ring)
    
    if not candidate_rings:
        return False, "No five‐membered aromatic heterocycle with nitrogen found"
    
    # Now discard rings that are fused – i.e. that share at least 2 atoms with any other ring.
    non_fused_candidates = []
    for cand in candidate_rings:
        cand_set = set(cand)
        fused = False
        for other in all_rings:
            # Skip if same ring
            if set(other) == cand_set:
                continue
            # If the candidate shares 2 or more atoms with any other ring, we treat it as fused.
            if len(cand_set.intersection(other)) >= 2:
                fused = True
                break
        if not fused:
            non_fused_candidates.append(cand)
    
    if not non_fused_candidates:
        return False, "No non‐fused five‐membered aromatic heterocycle with nitrogen found"
    
    # Check that the candidate ring is not a very minor substructure.
    num_heavy = mol.GetNumHeavyAtoms()
    # Since every candidate here is 5 atoms, compute the fraction.
    max_fraction = 5 / num_heavy
    if max_fraction < 0.10:
        return False, f"Candidate azole ring accounts for only {max_fraction*100:.1f}% of the molecule's heavy atoms"
    
    # Heuristic to reduce peptides: count amide bonds.
    # Use a SMARTS pattern for an amide: [CX3](=O)N
    amide_smarts = Chem.MolFromSmarts("[CX3](=O)N")
    amide_matches = mol.GetSubstructMatches(amide_smarts)
    if len(amide_matches) >= 4:
        return False, f"Molecule contains {len(amide_matches)} amide bonds, likely a peptide"
    
    return True, "Found a non‐fused five‐membered aromatic heterocycle with nitrogen (azole ring)"

# Example usage (for testing; remove or comment out in production):
if __name__ == "__main__":
    examples = [
        ("CC(C)OCCCNC1=NC=NC2=C1C=NN2C3=CC=CC=C3", "1-phenyl-N-(3-propan-2-yloxypropyl)-4-pyrazolo[3,4-d]pyrimidinamine"),
        ("CC1CCCCC1N2C(=NNC2=S)C3=CN=CC=C3", "4-(2-methylcyclohexyl)-3-(3-pyridinyl)-1H-1,2,4-triazole-5-thione"),
        ("Cn1cnc(CCN)c1", "N(tele)-methylhistamine"),
        ("OC1=CC=CC=C1C=NNC(=O)C2=C(N(N=N2)C3=NON=C3N)C4=CC=CC=C4", "1-(4-amino-1,2,5-oxadiazol-3-yl)-..."),
        # A couple of examples from the false negatives:
        ("CC(C)C1=C(C(=O)NC2=CC=CC=C2)C(=C(N1CC[C@@H](O)C[C@@H](O)CC(O)=O)C1=CC=C(F)C=C1)C1=CC=CC=C1", "atorvastatin"),
        ("O=C1NC(=O)C(c2c[nH]c3ccccc23)=C1c1c[nH]cn1", "didemnimide A"),
    ]
    for smi, name in examples:
        res, reason = is_azole(smi)
        print(f"Test: {name}\n  SMILES: {smi}\n  Result: {res}\n  Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:68452',
                          'name': 'azole',
                          'definition': 'Any monocyclic heteroarene consisting '
                                        'of a five-membered ring containing '
                                        'nitrogen. Azoles can also contain one '
                                        'or more other non-carbon atoms, such '
                                        'as nitrogen, sulfur or oxygen.',
                          'parents': ['CHEBI:38101', 'CHEBI:38179'],
                          'xrefs': ['Wikipedia:Azole'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 87,
                           'log_lines_of_code': 4.465908118654584,
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
                                                 2,
                                                 1,
                                                 2,
                                                 0,
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
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
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
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
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
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'GetIsAromatic',
                                                 'intersection',
                                                 'AtomRings',
                                                 'GetNumHeavyAtoms',
                                                 'MolFromSmarts',
                                                 'SanitizeMol',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetRingInfo'],
                           'methods_called_count': 12,
                           'smarts_strings': ['[CX3](=O)N'],
                           'smarts_strings_count': 1,
                           'defs': ['is_azole(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Sanitization failed: '
                                          '{str(e)}"',
                                          'False, "No rings found in the '
                                          'molecule"',
                                          'False, "No five‐membered aromatic '
                                          'heterocycle with nitrogen found"',
                                          'False, "No non‐fused five‐membered '
                                          'aromatic heterocycle with nitrogen '
                                          'found"',
                                          'False, f"Candidate azole ring '
                                          'accounts for only '
                                          '{max_fraction*100:.1f}% of the '
                                          'molecule\'s heavy atoms"',
                                          'False, f"Molecule contains '
                                          '{len(amide_matches)} amide bonds, '
                                          'likely a peptide"',
                                          'True, "Found a non‐fused '
                                          'five‐membered aromatic heterocycle '
                                          'with nitrogen (azole ring)"'],
                           'returns_count': 8,
                           'complexity': 5.893181623730916},
    'message': '\n'
               'Attempt failed: F1 score of 0.29857697283311774 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CC(C)OCCCNC1=NC=NC2=C1C=NN2C3=CC=CC=C3 '
               'NAME: '
               '1-phenyl-N-(3-propan-2-yloxypropyl)-4-pyrazolo[3,4-d]pyrimidinamine '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: CC1CCCCC1N2C(=NNC2=S)C3=CN=CC=C3 NAME: '
               '4-(2-methylcyclohexyl)-3-(3-pyridinyl)-1H-1,2,4-triazole-5-thione '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: Cn1cnc(CCN)c1 NAME: N(tele)-methylhistamine REASON: '
               'CORRECT Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: CC(C)(C)C(O)C(=C/C1CCCCC1)\\n1cncn1 NAME: '
               'Triapenthenol REASON: CORRECT Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'COC1=CC=CC=C1C=NNC(=O)C2=C(N(N=N2)C3=NON=C3N)C4=CC=CC=C4 NAME: '
               '1-(4-amino-1,2,5-oxadiazol-3-yl)-N-[(2-methoxyphenyl)methylideneamino]-5-phenyl-4-triazolecarboxamide '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: '
               'Cc1ncc(C[n+]2c(C)c(CCOP(O)(=O)OP(O)(O)=O)sc2C(O)CCC(O)=O)c(N)n1 '
               'NAME: 3-carboxy-1-hydroxypropylthiamine diphosphate REASON: '
               'CORRECT Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: '
               'CCC(CC)(CC(=O)Nc1cccc(\\C=C\\c2nc(cs2)C2CCC2)c1)C(O)=O NAME: '
               'cinalukast REASON: CORRECT Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: O1C(=NC=C1)CCCCC NAME: 2-Pentyloxazole REASON: '
               'CORRECT Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: CC(C)CCn1c2ccccc2c(O)c(C(=O)Nc2ncc(C)s2)c1=O NAME: '
               '4-hydroxy-1-isopentyl-N-(5-methyl-1,3-thiazol-2-yl)-2-oxoquinoline-3-carboxamide '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CC1=C(C(=O)N(N1)C2=NC=C(S2)C3=CC=C(C=C3)Cl)C(C4=CC=C(C=C4)Cl)C(C#N)C#N '
               'NAME: '
               '2-[(4-chlorophenyl)-[2-[5-(4-chlorophenyl)-2-thiazolyl]-5-methyl-3-oxo-1H-pyrazol-4-yl]methyl]propanedinitrile '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: '
               'C1=CC=C(C=C1)NC2=NC(=NC(=N2)N)CSC3=NN=NN3C4=CC=CC=C4 NAME: '
               'N2-phenyl-6-[[(1-phenyl-5-tetrazolyl)thio]methyl]-1,3,5-triazine-2,4-diamine '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: '
               'C1(=NOC(=C1)COC=2C(=CC=CC2C)C)C(=O)N3CCC(CC3)C4=CC=NC=C4 NAME: '
               'dafadine A REASON: CORRECT Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: FC(F)(F)C=1NC(=C(C1)C(O)=O)C NAME: PQH REASON: '
               'CORRECT Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: Cc1cccc(C)c1N(Cn1cccn1)C(=O)CS(O)(=O)=O NAME: '
               'metazachlor ESA REASON: CORRECT Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'C1=C(C=CC(=C1)[C@@H](C(CC)CC)N2C=NC=N2)NC=3SC4=C(N3)C=CC=C4 '
               'NAME: (R)-talarozole REASON: CORRECT Found a five‐membered '
               'aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'C1=CC=NC(=C1)C2=NN=C(N2CC3=CC=CO3)SCC4=C(C=C(C=C4)Cl)Cl NAME: '
               '2-[5-[(2,4-dichlorophenyl)methylthio]-4-(2-furanylmethyl)-1,2,4-triazol-3-yl]pyridine '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: CC1=CC=C(C=C1)OCC2=NNC(=S)N2C3=CC=CC=C3 NAME: '
               '3-[(4-methylphenoxy)methyl]-4-phenyl-1H-1,2,4-triazole-5-thione '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: ON1C=2CCCC(=O)C2N=C1C3=CC=CC=C3 NAME: '
               '1-hydroxy-2-phenyl-1,5,6,7-tetrahydro-4H-benzimidazol-4-one '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: CC(C)CN1C(=O)C(=CC2=C(NN=C2)C3=CC=CC=C3)SC1=S NAME: '
               '3-(2-methylpropyl)-5-[(5-phenyl-1H-pyrazol-4-yl)methylidene]-2-sulfanylidene-4-thiazolidinone '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: C1CCN(CC1)C2=C(N=C(O2)C3=CC=C(C=C3)Cl)C#N NAME: '
               '2-(4-chlorophenyl)-5-(1-piperidinyl)-4-oxazolecarbonitrile '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: C1=CC=C(C=C1)C2=C(N3C=CSC3=N2)NC(=O)C4=CC=CC=C4 '
               'NAME: N-(6-phenyl-5-imidazo[2,1-b]thiazolyl)benzamide REASON: '
               'CORRECT Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: N[C@H](Cc1c[nH]cn1)C(O)=O NAME: D-histidine REASON: '
               'CORRECT Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: Cc1nc(C)c(C)s1 NAME: 2,4,5-trimethylthiazole '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: COC1=CC=C(C=C1)CNC(=O)C2=CSC(=N2)CC3=CC=CC=C3 NAME: '
               'N-[(4-methoxyphenyl)methyl]-2-(phenylmethyl)-4-thiazolecarboxamide '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)C2=NC(=C(O2)C)CS(=O)(=O)CC(=O)N3CCC4=CC=CC=C4C3 '
               'NAME: '
               '1-(3,4-dihydro-1H-isoquinolin-2-yl)-2-[[5-methyl-2-(4-methylphenyl)-4-oxazolyl]methylsulfonyl]ethanone '
               'REASON: CORRECT Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               'False positives: SMILES: '
               'CCN1C2=CC=CC=C2C(=C(C1=O)C(=O)NC3=NC4=CC=CC=C4N3)O NAME: '
               'N-(1H-benzimidazol-2-yl)-1-ethyl-4-hydroxy-2-oxo-3-quinolinecarboxamide '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               '[NH3+][C@H](C([O-])=O)CCC(=O)N[C@H](C(=O)[O-])CC1=CNC2=C1C=CC=C2 '
               'NAME: gamma-Glu-Trp(1-) REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: Oc1ccc2c3ccnc4ccc(=O)n(c2c1)c34 NAME: '
               '9-hydroxycanthin-6-one REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: COC(=O)Nc1nc2cc(ccc2[nH]1)C(=O)c1ccccc1 NAME: '
               'mebendazole REASON: WRONGLY CLASSIFIED Found a five‐membered '
               'aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: CSc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: 6-methylthioinosine REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CN1C=C(N=C1)S(=O)(=O)N2CC[C@H]3[C@@H]2C4=C(C=CC(=C4)C5=CC(=CC=C5)OC)N[C@H]3CO '
               'NAME: '
               '[(3aR,4R,9bR)-8-(3-methoxyphenyl)-1-[(1-methyl-4-imidazolyl)sulfonyl]-2,3,3a,4,5,9b-hexahydropyrrolo[3,2-c]quinolin-4-yl]methanol '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: CCC[NH2+][C@H]1CCc2[nH+]c(N)sc2C1 NAME: '
               'pramipexole(2+) REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CN1CC2(CCN(CC2)C(=O)CN3CCOCC3)C4=C([C@H]1CO)N(C5=C4C=CC(=C5)OC)C '
               'NAME: '
               "1-[(1S)-1-(hydroxymethyl)-7-methoxy-2,9-dimethyl-1'-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]-2-(4-morpholinyl)ethanone "
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CC1=CC(=CC=C1)S(=O)(=O)N2CC3(C2)CN[C@@H](C4=C3C5=C(N4C)C=C(C=C5)OC)CO '
               'NAME: '
               "[(1S)-7-methoxy-9-methyl-1'-(3-methylphenyl)sulfonyl-1-spiro[2,3-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]methanol "
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: O=C1N=C2N(C(=O)N(C2=NN1C)C)C NAME: '
               '2-methyl-fervenulone REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: CN(CC#C)c1c(cnn1-c1nn2CCCCc2c1Cl)C#N NAME: '
               'Pyraclonil REASON: WRONGLY CLASSIFIED Found a five‐membered '
               'aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: CC(C)C[C@@H]1COCC2=CN(CCCC(=O)N1)N=N2 NAME: '
               '(7R)-7-(2-methylpropyl)-9-oxa-1,6,12,13-tetrazabicyclo[9.2.1]tetradeca-11(14),12-dien-5-one '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CC(C)C1=CN(N=N1)CC[C@H]2CC[C@@H]([C@H](O2)CO)NC(=O)C3CC3 NAME: '
               'N-[(2S,3S,6R)-2-(hydroxymethyl)-6-[2-(4-propan-2-yl-1-triazolyl)ethyl]-3-oxanyl]cyclopropanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: Cc1nc2CCCCn2c(=O)c1CCN1CCC(CC1)c1noc2cc(F)ccc12 '
               'NAME: risperidone REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'OC[C@H]1OC(OC(=O)c2c[nH]c3cc(O)ccc23)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: D-glucosyl 6-hydroxyindole-3-carboxylate REASON: WRONGLY '
               'CLASSIFIED Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               ' * SMILES: '
               'CC1=C(ON=C1C)NS(=O)(=O)C2=CC=C(C=C2)NC=CC(=O)C3=CC=C(C=C3)F '
               'NAME: '
               'N-(3,4-dimethyl-5-isoxazolyl)-4-[[3-(4-fluorophenyl)-3-oxoprop-1-enyl]amino]benzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: CC1=CC2=NC(=C(N2C=C1)C(=O)CSC3=CC=CC=C3)C NAME: '
               '1-(2,7-dimethyl-3-imidazo[1,2-a]pyridinyl)-2-(phenylthio)ethanone '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'C1C[C@H]([C@@H](O[C@H]1CCN2C=C(N=N2)C3=CN=CC=C3)CO)NC(=O)C4=CC=CC=C4F '
               'NAME: '
               '2-fluoro-N-[(2R,3R,6R)-2-(hydroxymethyl)-6-[2-[4-(3-pyridinyl)-1-triazolyl]ethyl]-3-oxanyl]benzamide '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: O=c1[nH]c2nc[nH]c2c(=O)[nH]1 NAME: 7H-xanthine '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CN(C4)CC5=NC=CS5)C(=O)CN(C)C)CO '
               'NAME: '
               "2-(dimethylamino)-1-[(1S)-1-(hydroxymethyl)-7-methoxy-9-methyl-1'-(2-thiazolylmethyl)-2-spiro[1,3-dihydropyrido[3,4-b]indole-4,3'-azetidine]yl]ethanone "
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)C2=NC(=C(C=C2)C3=NOC(=N3)C4=CN=CC=C4)OC NAME: '
               '3-[2-methoxy-6-(4-methylphenyl)-3-pyridinyl]-5-(3-pyridinyl)-1,2,4-oxadiazole '
               'REASON: WRONGLY CLASSIFIED Found a five‐membered aromatic '
               'heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: CCCCCCCCn1cc[n+](C)c1 NAME: '
               '3-methyl-1-octylimidazolium REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: '
               'C\\C=C1\\CN2[C@H]3Cc4c([nH]c5ccccc45)[C@@H]2C[C@@H]1[C@H]3C=O '
               'NAME: vellosimine REASON: WRONGLY CLASSIFIED Found a '
               'five‐membered aromatic heterocycle with nitrogen (azole ring)\n'
               ' * SMILES: C1=CC=C(C=C1)OC2=CC=CC=C2NC(=O)CN3C=CSC3=N NAME: '
               '2-(2-imino-3-thiazolyl)-N-(2-phenoxyphenyl)acetamide REASON: '
               'WRONGLY CLASSIFIED Found a five‐membered aromatic heterocycle '
               'with nitrogen (azole ring)\n'
               ' * SMILES: Nc1ccc2nc3ccccn3c2n1 NAME: Glu-P-2 REASON: WRONGLY '
               'CLASSIFIED Found a five‐membered aromatic heterocycle with '
               'nitrogen (azole ring)\n'
               'False negatives: SMILES: '
               'CC(C)C1=C(C(=O)NC2=CC=CC=C2)C(=C(N1CC[C@@H](O)C[C@@H](O)CC(O)=O)C1=CC=C(F)C=C1)C1=CC=CC=C1 '
               'NAME: atorvastatin REASON: MISSED Candidate azole ring '
               "accounts for only 12.2% of the molecule's heavy atoms\n"
               ' * SMILES: O=C1NC(=O)C(c2c[nH]c3ccccc23)=C1c1c[nH]cn1 NAME: '
               'didemnimide A REASON: MISSED Molecule contains 2 amide bonds, '
               'likely a peptide\n'
               ' * SMILES: '
               'CC1=C(C(=O)N(N1C)C2=CC=CC=C2)N3C(=O)C(=C4C5=CC=CC=C5N(C4=O)C(=O)C)SC3=S '
               'NAME: '
               '5-(1-acetyl-2-oxo-3-indolylidene)-3-(1,5-dimethyl-3-oxo-2-phenyl-4-pyrazolyl)-2-sulfanylidene-4-thiazolidinone '
               'REASON: MISSED Molecule contains 3 amide bonds, likely a '
               'peptide\n'
               ' * SMILES: C(OC)(C1=C(C=CC(=C1)C)C2=NC(C(N2)=O)(C(C)C)C)=O '
               'NAME: methyl '
               '2-(4-isopropyl-4-methyl-5-oxo-4,5-dihydro-1H-imidazol-2-yl)-5-methylbenzoate '
               'REASON: MISSED No five-membered aromatic heterocycle with '
               'nitrogen found\n'
               ' * SMILES: [O-][N+](=O)c1cnc(s1)N1CCNC1=O NAME: Niridazole '
               'REASON: MISSED Molecule contains 2 amide bonds, likely a '
               'peptide\n'
               ' * SMILES: CCCCNC(=O)[C@H](CS)NC(=O)C(=N/OC)\\c1csc(N)n1 NAME: '
               'N(2)-[(2Z)-2-(2-amino-1,3-thiazol-4-yl)-2-(methoxyimino)acetyl]-N-butyl-L-cysteinamide '
               'REASON: MISSED Molecule contains 2 amide bonds, likely a '
               'peptide\n'
               ' * SMILES: '
               'CC1=CC=CC=C1N2C(=NN=C2SCC(=O)NC3=NOC(=C3)C)CN4C5=CC=CC=C5SC4=O '
               'NAME: '
               'N-(5-methyl-3-isoxazolyl)-2-[[4-(2-methylphenyl)-5-[(2-oxo-1,3-benzothiazol-3-yl)methyl]-1,2,4-triazol-3-yl]thio]acetamide '
               'REASON: MISSED Candidate azole ring accounts for only 14.7% of '
               "the molecule's heavy atoms\n"
               ' * SMILES: C1(NC(=O)CN1N=CC=2OC(C=3C=CC(=CC3)Br)=CN2)=O NAME: '
               'azumolene REASON: MISSED Molecule contains 3 amide bonds, '
               'likely a peptide\n'
               ' * SMILES: '
               'CC1=C(C(=NC2=CC(=NN12)C3=CC=C(C=C3)Cl)C)CCC(=O)NC(C)C4=CC5=C(C=C4)OCCO5 '
               'NAME: '
               '3-[2-(4-chlorophenyl)-5,7-dimethyl-6-pyrazolo[1,5-a]pyrimidinyl]-N-[1-(2,3-dihydro-1,4-benzodioxin-6-yl)ethyl]propanamide '
               'REASON: MISSED Candidate azole ring accounts for only 14.3% of '
               "the molecule's heavy atoms\n"
               ' * SMILES: '
               'CC(C)[C@H]1OC(=O)C2=CCCN2C(=O)c2coc(CC(=O)C[C@H](O)\\C=C(/C)\\C=C\\CNC(=O)\\C=C\\[C@H]1C)n2 '
               'NAME: pristinamycin IIA REASON: MISSED Molecule contains 2 '
               'amide bonds, likely a peptide\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No five‐membered aromatic '
                                               'heterocycle with nitrogen '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)OCCCNC1=NC=NC2=C1C=NN2C3=CC=CC=C3',
                                      'name': '1-phenyl-N-(3-propan-2-yloxypropyl)-4-pyrazolo[3,4-d]pyrimidinamine',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'C(OC)(C1=C(C=CC(=C1)C)C2=NC(C(N2)=O)(C(C)C)C)=O',
                                      'name': 'methyl '
                                              '2-(4-isopropyl-4-methyl-5-oxo-4,5-dihydro-1H-imidazol-2-yl)-5-methylbenzoate',
                                      'reason': 'No five‐membered aromatic '
                                                'heterocycle with nitrogen '
                                                'found'},
                                  {   'smiles': 'ON1C=2CCCC(=O)C2N=C1C3=CC=CC=C3',
                                      'name': '1-hydroxy-2-phenyl-1,5,6,7-tetrahydro-4H-benzimidazol-4-one',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'CC1=C(C(=NC2=CC(=NN12)C3=CC=C(C=C3)Cl)C)CCC(=O)NC(C)C4=CC5=C(C=C4)OCCO5',
                                      'name': '3-[2-(4-chlorophenyl)-5,7-dimethyl-6-pyrazolo[1,5-a]pyrimidinyl]-N-[1-(2,3-dihydro-1,4-benzodioxin-6-yl)ethyl]propanamide',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'C1=CC=C(C=C1)C2=C(N3C=CSC3=N2)NC(=O)C4=CC=CC=C4',
                                      'name': 'N-(6-phenyl-5-imidazo[2,1-b]thiazolyl)benzamide',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'CC(C)[C@H]1OC(=O)C2=CCCN2C(=O)c2coc(CC(=O)C[C@H](O)\\C=C(/C)\\C=C\\CNC(=O)\\C=C\\[C@H]1C)n2',
                                      'name': 'pristinamycin IIA',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'C1CSC2=NC(=CN21)C3=CC=C(C=C3)Cl',
                                      'name': '6-(4-chlorophenyl)-2,3-dihydroimidazo[2,1-b]thiazole',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'O1N2[C@@H](C[C@@H]([C@H]([C@H]1C3=CC=CC=C3)C2)O)CCCCCCCCC',
                                      'name': 'Asperidine C',
                                      'reason': 'No five‐membered aromatic '
                                                'heterocycle with nitrogen '
                                                'found'},
                                  {   'smiles': 'CC1=CC2=C(C=C1)C3=C(C2)C(=NN3C4=C(C=C(C=C4)Cl)Cl)C(=O)NN5CCCCC5',
                                      'name': '1-(2,4-dichlorophenyl)-6-methyl-N-(1-piperidinyl)-4H-indeno[1,2-c]pyrazole-3-carboxamide',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'},
                                  {   'smiles': 'C1=CC=C(C=C1)C2=NNC3=C2N=CC(=C3)C(F)(F)F',
                                      'name': '3-phenyl-6-(trifluoromethyl)-1H-pyrazolo[4,3-b]pyridine',
                                      'reason': 'No non‐fused five‐membered '
                                                'aromatic heterocycle with '
                                                'nitrogen found'}],
    'attempt': 3,
    'reasoning': 'Below is one possible solution. In my reasoning I took '
                 'another look at what went wrong with the previous code. (1) '
                 'The previous method accepted any five‐membered aromatic ring '
                 'with at least one nitrogen even when it was “just” a small '
                 'substituent in a very large molecule. In many '
                 '“false‐negative” cases the candidate azole ring was indeed '
                 'found but its size relative to the whole molecule was very '
                 'small. (2) Also, many false positives came from molecules '
                 'where the five‐membered ring was part of a fused '
                 '(multi‐ring) system (for example benzimidazoles) or where '
                 'multiple amide bonds (which appear in peptides) made up the '
                 'majority of the molecule. \n'
                 '\n'
                 'To address these issues I made two major changes. First, I '
                 'now consider only candidate rings that (a) are exactly five '
                 'atoms, (b) are aromatic, (c) contain only the allowed '
                 'elements (C, N, O, or S) with at least one nitrogen, and (d) '
                 'are not “fused” (i.e. the five‐membered ring is not sharing '
                 'two or more atoms with another ring). Second, rather than '
                 'use a strict 15% threshold on the candidate ring’s fraction '
                 'of heavy atoms, I lowered it (to 10%) so that valid (but '
                 'larger) molecules such as atorvastatin can be detected as '
                 'azoles while still helping to disallow tiny azole '
                 'substituents. Finally, instead of rejecting molecules having '
                 'more than one amide bond (which ended up “missing” some '
                 'peptide‐like azoles), the algorithm now only rejects those '
                 'that have many amide links (i.e. four or more) as a hint '
                 'that the candidate azole might only be a very minor part of '
                 'a peptide. (Of course, any single heuristic has its '
                 'limitations.) \n'
                 '\n'
                 'Below is the complete Python code implementing these '
                 'ideas. \n'
                 '\n'
                 'Below is the code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1702,
    'num_false_positives': 5274,
    'num_true_negatives': 134870,
    'num_false_negatives': 454,
    'num_negatives': None,
    'precision': 0.24397935779816513,
    'recall': 0.7894248608534323,
    'f1': 0.37275514673674986,
    'accuracy': 0.9597470133520731,
    'negative_predictive_value': 0.9966450888238598}