"""
Classifies: CHEBI:39362 mononitrophenol
"""
from rdkit import Chem

def is_mononitrophenol(smiles: str):
    """
    Determines if a molecule is a mononitrophenol based on its SMILES string.
    A mononitrophenol is a phenol carrying a single nitro substituent at an unspecified position.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a mononitrophenol, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get ring information
    ri = mol.GetRingInfo()
    atom_rings = ri.AtomRings()
    aromatic_rings = [ring for ring in atom_rings if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)]

    # Check that there is exactly one aromatic ring
    if len(aromatic_rings) != 1:
        return False, f"Molecule has {len(aromatic_rings)} aromatic rings, expected 1"

    ring_atoms = set(aromatic_rings[0])

    # Define nitro group pattern
    nitro_pattern = Chem.MolFromSmarts('[N+](=O)[O-]')
    nitro_matches = mol.GetSubstructMatches(nitro_pattern)

    # Check for exactly one nitro group
    if len(nitro_matches) != 1:
        return False, f"Found {len(nitro_matches)} nitro groups, expected 1"

    # Check that nitro group is attached to the aromatic ring
    nitro_nitrogen_idx = nitro_matches[0][0]
    nitro_nitrogen_atom = mol.GetAtomWithIdx(nitro_nitrogen_idx)
    nitro_connected = False
    for neighbor in nitro_nitrogen_atom.GetNeighbors():
        if neighbor.GetIdx() in ring_atoms:
            nitro_connected = True
            break
    if not nitro_connected:
        return False, "Nitro group is not attached to the aromatic ring"

    # Define phenolic hydroxyl group pattern
    phenol_pattern = Chem.MolFromSmarts('[c][O;H1]')
    phenol_matches = mol.GetSubstructMatches(phenol_pattern)

    # Check for exactly one phenolic hydroxyl group
    if len(phenol_matches) != 1:
        return False, f"Found {len(phenol_matches)} phenolic OH groups, expected 1"

    # Check that hydroxyl group is attached to the aromatic ring
    phenol_oxygen_idx = phenol_matches[0][1]
    phenol_oxygen_atom = mol.GetAtomWithIdx(phenol_oxygen_idx)
    hydroxyl_connected = False
    for neighbor in phenol_oxygen_atom.GetNeighbors():
        if neighbor.GetIdx() in ring_atoms:
            hydroxyl_connected = True
            break
    if not hydroxyl_connected:
        return False, "Phenolic OH group is not attached to the aromatic ring"

    # Check for other substituents on the aromatic ring
    allowed_substituents = {'C', 'H', 'O', 'N', 'F', 'Cl', 'Br', 'I'}
    for idx in ring_atoms:
        atom = mol.GetAtomWithIdx(idx)
        for neighbor in atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if neighbor_idx not in ring_atoms:
                element = neighbor.GetSymbol()
                if element not in allowed_substituents:
                    return False, f"Disallowed substituent '{element}' attached to aromatic ring"
                # Exclude large substituents (more than 3 atoms)
                substituent = Chem.PathToSubmol(mol, [idx, neighbor_idx])
                if substituent.GetNumHeavyAtoms() > 4:
                    return False, "Substituent attached to ring is too large"

    # Check that there are no other rings in the molecule
    if len(atom_rings) != 1:
        return False, f"Molecule has {len(atom_rings)} rings, expected 1"

    return True, "Molecule is a mononitrophenol with single aromatic ring and appropriate substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:39362',
                          'name': 'mononitrophenol',
                          'definition': 'A nitrophenol that is phenol carrying '
                                        'a single nitro substituent at '
                                        'unspecified position.',
                          'parents': ['CHEBI:25562'],
                          'xrefs': ['CAS:25154-55-6'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.4 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: COc1ccc(cc1O)[N+]([O-])=O NAME: '
               '2-Methoxy-5-nitrophenol REASON: CORRECT Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: Cc1cc(O)ccc1[N+]([O-])=O NAME: 4-nitro-m-cresol '
               'REASON: CORRECT Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: C=1C([As](O)O)=CC([N+](=O)[O-])=C(C1)[O-] NAME: '
               'roxarsone (III) REASON: CORRECT Contains phenol ring with one '
               'nitro group attached\n'
               ' * SMILES: OC(=O)CCCCCNC(=O)c1cc(I)c(O)c(c1)[N+]([O-])=O NAME: '
               '6-(4-hydroxy-5-iodo-3-nitrobenzamido)hexanoic acid REASON: '
               'CORRECT Contains phenol ring with one nitro group attached\n'
               ' * SMILES: OC(=O)CCCCCNC(=O)c1ccc(O)c(c1)[N+]([O-])=O NAME: '
               '6-(4-hydroxy-3-nitrobenzamido)hexanoic acid REASON: CORRECT '
               'Contains phenol ring with one nitro group attached\n'
               ' * SMILES: Nc1ccc(cc1O)[N+]([O-])=O NAME: '
               '2-Amino-5-nitrophenol REASON: CORRECT Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: CCOc1cc(cc(c1O)[N+]([O-])=O)\\C=C(/C#N)C(=O)N(CC)CC '
               'NAME: 3-O-ethylentacapone REASON: CORRECT Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: C(=O)(O)CC1=CC(=C(C(=C1)Br)O)[N+]([O-])=O NAME: '
               '(3-bromo-4-hydroxy-5-nitrophenyl)acetic acid REASON: CORRECT '
               'Contains phenol ring with one nitro group attached\n'
               ' * SMILES: Oc1cc(I)cc(c1)[N+]([O-])=O NAME: '
               '3-iodo-5-nitrophenol REASON: CORRECT Contains phenol ring with '
               'one nitro group attached\n'
               ' * SMILES: C1(=CC=C(C=C1OS(O)(=O)=O)[N+]([O-])=O)O NAME: '
               '2-hydroxy-5-nitrophenyl hydrogen sulfate REASON: CORRECT '
               'Contains phenol ring with one nitro group attached\n'
               ' * SMILES: OC(=O)Cc1cc(I)c(O)c(c1)[N+]([O-])=O NAME: '
               '(4-hydroxy-3-iodo-5-nitrophenyl)acetic acid REASON: CORRECT '
               'Contains phenol ring with one nitro group attached\n'
               ' * SMILES: Oc1ccc(CC(=O)ON2C(=O)CCC2=O)cc1[N+]([O-])=O NAME: '
               '1-((4-hydroxy-3-nitrophenyl)acetoxy)pyrrolidine-2,5-dione '
               'REASON: CORRECT Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: Oc1ccc(cc1[N+]([O-])=O)[As](O)(O)=O NAME: roxarsone '
               'REASON: CORRECT Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: Oc1ccccc1[N+]([O-])=O NAME: 2-nitrophenol REASON: '
               'CORRECT Contains phenol ring with one nitro group attached\n'
               ' * SMILES: N[C@@H](Cc1ccc(O)c(c1)[N+]([O-])=O)C(O)=O NAME: '
               '3-nitro-L-tyrosine REASON: CORRECT Contains phenol ring with '
               'one nitro group attached\n'
               ' * SMILES: Oc1c(I)cc(CC(=O)ON2C(=O)CCC2=O)cc1[N+]([O-])=O '
               'NAME: '
               '1-((4-hydroxy-5-iodo-3-nitrophenyl)acetoxy)pyrrolidine-2,5-dione '
               'REASON: CORRECT Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: Nc1cc(ccc1O)[N+]([O-])=O NAME: '
               '2-Amino-4-nitrophenol REASON: CORRECT Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: Cc1ccc(cc1)C(=O)c1cc(O)c(O)c(c1)[N+]([O-])=O NAME: '
               'tolcapone REASON: CORRECT Contains phenol ring with one nitro '
               'group attached\n'
               ' * SMILES: NC(Cc1ccc(O)c(c1)[N+]([O-])=O)C(O)=O NAME: '
               '3-nitrotyrosine REASON: CORRECT Contains phenol ring with one '
               'nitro group attached\n'
               ' * SMILES: Oc1ccc(cc1)[N+]([O-])=O NAME: 4-nitrophenol REASON: '
               'CORRECT Contains phenol ring with one nitro group attached\n'
               ' * SMILES: COc1cc(ccc1O)[N+]([O-])=O NAME: '
               '2-Methoxy-4-nitrophenol REASON: CORRECT Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: OC(=O)CCCCCNC(=O)Cc1cc(Br)c(O)c(c1)[N+]([O-])=O '
               'NAME: 6-[(3-bromo-4-hydroxy-5-nitrophenyl)acetamido]caproic '
               'acid REASON: CORRECT Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: [H]C(=O)c1cc(OC)c(O)c(c1)[N+]([O-])=O NAME: '
               '5-nitrovanillin REASON: CORRECT Contains phenol ring with one '
               'nitro group attached\n'
               ' * SMILES: Oc1cccc(c1)[N+]([O-])=O NAME: 3-nitrophenol REASON: '
               'CORRECT Contains phenol ring with one nitro group attached\n'
               ' * SMILES: '
               'CCN(CC)C(=O)C(\\C#N)=C\\c1cc(O)c(O)c(c1)[N+]([O-])=O NAME: '
               'entacapone REASON: CORRECT Contains phenol ring with one nitro '
               'group attached\n'
               'False positives: SMILES: '
               'OC1=C(C=C([N+]([O-])=O)C=C1)\\C=N\\C=2C=C(C=CC2)C#C NAME: '
               '2-{[(3-eth-1-ynylphenyl)imino]methyl}-4-nitrophenol REASON: '
               'WRONGLY CLASSIFIED Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: '
               'CCOC1=CC(=CC(=C1O)[N+](=O)[O-])C=C2C(=O)N(C(=O)S2)CC(=O)NC3=CC=CC=C3F '
               'NAME: '
               '2-[5-[(3-ethoxy-4-hydroxy-5-nitrophenyl)methylidene]-2,4-dioxo-3-thiazolidinyl]-N-(2-fluorophenyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Contains phenol ring with one nitro '
               'group attached\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCc4cc(O)c(cc34)[N+]([O-])=O)[C@@H]1CCC2=O '
               'NAME: 3-Hydroxy-2-nitroestra-1,3,5(10)-trien-17-one REASON: '
               'WRONGLY CLASSIFIED Contains phenol ring with one nitro group '
               'attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=CC(=C1)C2=C(O)NC(=C2C3=CC=CC=C3)N=O NAME: '
               'Aqabamycin E1 REASON: WRONGLY CLASSIFIED Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: '
               'CCOC(=O)C1=CN(C=C(C1C2=CC(=C(C(=C2)OC)O)[N+](=O)[O-])C(=O)OCC)C3=CC(=CC=C3)F '
               'NAME: '
               '1-(3-fluorophenyl)-4-(4-hydroxy-3-methoxy-5-nitrophenyl)-4H-pyridine-3,5-dicarboxylic '
               'acid diethyl ester REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: OC1=C([N+]([O-])=O)C=C(C=C(C(=O)C)C(=O)C)C=C1O '
               'NAME: Nitecapone REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: '
               'C1=C(C(=C(C=C1C2=NC(=NO2)C=3C(=[N+](C(=C(C3C)Cl)C)[O-])Cl)O)O)[N+](=O)[O-] '
               'NAME: opicapone REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=CC(=C1)C=2C(=O)NC(C2C3=CC=C(O)C=C3)=O '
               'NAME: Aqabamycin B REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: C1=C(C(=CC(=C1O)O)[N+](=O)[O-])CCN NAME: '
               '4-(2-aminoethyl)-5-nitrobenzene-1,2-diol REASON: WRONGLY '
               'CLASSIFIED Contains phenol ring with one nitro group attached\n'
               ' * SMILES: OC1=C(NC(=O)NC2=CC=CC=C2Br)C=CC(=C1)[N+]([O-])=O '
               'NAME: SB225002 REASON: WRONGLY CLASSIFIED Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C(OC2O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]2O)O)=CC(=C1)C(=O)C3=CC=C(C)C=C3 '
               'NAME: '
               '(2R,3R,4R,5S)-3,4,5-trihydroxy-6-[2-hydroxy-5-(4-methylbenzoyl)-3-nitrophenoxy]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains phenol ring with one '
               'nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=CC(=C1)C[C@@H]2NC(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](NC([C@@H](N3C([C@@H](N(C([C@@H](NC2=O)C)=O)C)C[C@@](O)(C)[C@H]3O)=O)CC(C)C)=O)C/C=C/C)CC=4C5=C(C=CC=C5)N(C4)C([C@@H]6OC6)(C)C)C)CC(C)C '
               'NAME: Rufomycin NBZ8 REASON: WRONGLY CLASSIFIED Contains '
               'phenol ring with one nitro group attached\n'
               ' * SMILES: [O-]C(=O)Cc1ccc([O-])c(c1)[N+]([O-])=O NAME: '
               '(3-nitro-4-oxidophenyl)acetate REASON: WRONGLY CLASSIFIED '
               'Contains phenol ring with one nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=CC(=C1)C2=C(N=O)NC(=C2C3=CC=CC=C3)O NAME: '
               'Aqabamycin E2 REASON: WRONGLY CLASSIFIED Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=2C3=C(O)C=CC(=C3)C(N(C(=O)CNC(=O)[C@H](NC(=O)[C@H](N(C(=O)CCCCCCCCC(CC)C)C)CO)C)C)C(=O)N[C@H](C(NC(CC(=C1)C2)C(=O)O)=O)C '
               'NAME: Arylomycin B4 REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: [O-]c1ccccc1[N+]([O-])=O NAME: 2-nitrophenolate '
               'REASON: WRONGLY CLASSIFIED Contains phenol ring with one nitro '
               'group attached\n'
               ' * SMILES: O=[N+]([O-])C1=CC(O)=CC(=C1)O NAME: '
               '5-nitroresorcinol REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=CC(=C1)C[C@@H]2NC(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](NC([C@@H](N3C([C@@H](N(C([C@@H](NC2=O)C)=O)C)C[C@H](C)[C@H]3O)=O)CC(C)C)=O)CC=CC)CC=4C5=C(C=CC=C5)N(C4)[C@](C=C)(CO)C)C)CC(C)C '
               'NAME: Ilamycin J REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: C1(=CC=C(C=C1O)[N+]([O-])=O)O NAME: 4-nitrocatechol '
               'REASON: WRONGLY CLASSIFIED Contains phenol ring with one nitro '
               'group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=CC(=C1)C[C@@H]2NC(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](NC([C@@H](NC([C@@H](N(C([C@@H](NC2=O)C)=O)C)C[C@@H](CO)C)=O)CC(C)C)=O)C/C=C/C)CC=3C4=C(C=CC=C4)N(C3)C([C@@H]5OC5)(C)C)C)CC(C)C '
               'NAME: Rufomycin NBZ1 REASON: WRONGLY CLASSIFIED Contains '
               'phenol ring with one nitro group attached\n'
               ' * SMILES: C1=CC(=C(C(=C1O)[O-])[N+]([O-])=O)C NAME: '
               '4-methyl-3-nitrocatechol(1-) REASON: WRONGLY CLASSIFIED '
               'Contains phenol ring with one nitro group attached\n'
               ' * SMILES: '
               'O=C(N(CC)CC)/C(=C\\C1=CC([N+]([O-])=O)=C(O)C(O)=C1)/C#N NAME: '
               'Cis-Entacapone REASON: WRONGLY CLASSIFIED Contains phenol ring '
               'with one nitro group attached\n'
               ' * SMILES: '
               'COC1=CC=C(C=C1)C(=O)COC(=O)C2=CC=CC=C2NS(=O)(=O)C3=CC(=C(C=C3)O)[N+](=O)[O-] '
               'NAME: 2-[(4-hydroxy-3-nitrophenyl)sulfonylamino]benzoic acid '
               '[2-(4-methoxyphenyl)-2-oxoethyl] ester REASON: WRONGLY '
               'CLASSIFIED Contains phenol ring with one nitro group attached\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=C(O)C=2C3=C(O)C=CC(=C3)C(N(C(=O)CNC(=O)[C@H](NC(=O)[C@H](N(C(=O)CCCCCCCCC(C)C)C)CO)C)C)C(=O)N[C@H](C(NC(CC(=C1)C2)C(=O)O)=O)C '
               'NAME: Arylomycin B2 REASON: WRONGLY CLASSIFIED Contains phenol '
               'ring with one nitro group attached\n'
               ' * SMILES: O=[N+]([O-])C1=C(O)C(OC)=CC(=C1)C(=O)C2=CC=C(C)C=C2 '
               'NAME: 3-O-methyltolcapone REASON: WRONGLY CLASSIFIED Contains '
               'phenol ring with one nitro group attached\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CNC(=O)CC[C@H](N)C(O)=O',
                                     'name': 'N(5)-methyl-L-glutamine',
                                     'reason': 'Molecule has 0 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': 'C[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)C(O)=O',
                                     'name': "L-lactyl-2-diphospho-5'-guanosine",
                                     'reason': 'Molecule has 2 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])CC[C@]1([H])[C@@]3(C)CCCC(C)(C)[C@]3([H])CC[C@@]21C)C(=C)CCC=C(C)C',
                                     'name': 'dammara-20,24-diene',
                                     'reason': 'Molecule has 0 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': 'O=C1C2=C(O)C3=C(O)C=CC=C3C(=C2C(C(=O)C)C(C1)(O)C)C=4C=5C(C(O)=C6C4C(C(=O)C)C(O)(C)CC6=O)=C(O)C=CC5',
                                     'name': 'A 39183A',
                                     'reason': 'Molecule has 4 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': 'C[C@H](O)[C@@H](O)C1=Nc2c(NC1)[nH]c(N)nc2=O',
                                     'name': 'L-threo-7,8-dihydrobiopterin',
                                     'reason': 'Found 0 nitro groups, expected '
                                               '1'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)CC3=CC=C(C=C3)F',
                                     'name': 'N-[(4S,7R,8S)-5-[(4-fluorophenyl)methyl]-8-methoxy-4,7,10-trimethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'Molecule has 2 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': 'C(CCN1CCCCC1)(CCN(C(C)C)C(C)=O)(C(N)=O)C2=C(Cl)C=CC=C2',
                                     'name': 'bidisomide',
                                     'reason': 'Found 0 nitro groups, expected '
                                               '1'},
                                 {   'smiles': 'OCCCCCCCCCCC#CC=C',
                                     'name': '13-Tetradece-11-yn-1-ol',
                                     'reason': 'Molecule has 0 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)CC3=CC=C(C=C3)OC',
                                     'name': '(3R,9S,10R)-16-(dimethylamino)-12-[(2S)-1-hydroxypropan-2-yl]-9-[[(4-methoxyphenyl)methyl-methylamino]methyl]-3,10-dimethyl-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-13-one',
                                     'reason': 'Molecule has 2 aromatic rings, '
                                               'expected 1'},
                                 {   'smiles': 'O(CCC12CC3CC(C1)CC(C2)C3)C(=O)CC4=CC=C(OCC(O)CNC(C)C)C=C4',
                                     'name': 'Adaprolol',
                                     'reason': 'Found 0 nitro groups, expected '
                                               '1'}],
    'sample_false_negatives': [   {   'smiles': 'C=1C([As](O)O)=CC([N+](=O)[O-])=C(C1)[O-]',
                                      'name': 'roxarsone (III)',
                                      'reason': 'Found 0 phenolic OH groups, '
                                                'expected 1'},
                                  {   'smiles': 'Oc1ccc(CC(=O)ON2C(=O)CCC2=O)cc1[N+]([O-])=O',
                                      'name': '1-((4-hydroxy-3-nitrophenyl)acetoxy)pyrrolidine-2,5-dione',
                                      'reason': 'Molecule has 2 rings, '
                                                'expected 1'},
                                  {   'smiles': 'Oc1ccc(cc1[N+]([O-])=O)[As](O)(O)=O',
                                      'name': 'roxarsone',
                                      'reason': "Disallowed substituent 'As' "
                                                'attached to aromatic ring'},
                                  {   'smiles': 'Oc1c(I)cc(CC(=O)ON2C(=O)CCC2=O)cc1[N+]([O-])=O',
                                      'name': '1-((4-hydroxy-5-iodo-3-nitrophenyl)acetoxy)pyrrolidine-2,5-dione',
                                      'reason': 'Molecule has 2 rings, '
                                                'expected 1'},
                                  {   'smiles': 'Cc1ccc(cc1)C(=O)c1cc(O)c(O)c(c1)[N+]([O-])=O',
                                      'name': 'tolcapone',
                                      'reason': 'Molecule has 2 aromatic '
                                                'rings, expected 1'},
                                  {   'smiles': 'CCN(CC)C(=O)C(\\C#N)=C\\c1cc(O)c(O)c(c1)[N+]([O-])=O',
                                      'name': 'entacapone',
                                      'reason': 'Found 2 phenolic OH groups, '
                                                'expected 1'}],
    'attempt': 3,
    'reasoning': 'Upon analyzing the previous program and the outcomes, it '
                 'appears that the main issue leading to the high number of '
                 'false positives is that the code classifies any molecule '
                 'containing a phenol ring with a single nitro group attached '
                 'as a mononitrophenol, regardless of additional structural '
                 'features.\n'
                 '\n'
                 'Many of the false positives are complex molecules where a '
                 'mononitrophenol moiety is part of a larger structure, such '
                 'as molecules with multiple aromatic rings, fused ring '
                 'systems, or extensive substituents. The current code does '
                 'not restrict the molecule to only being a mononitrophenol '
                 'but includes any molecule containing a mononitrophenol '
                 'substructure.\n'
                 '\n'
                 'To improve the classification and reduce false positives, we '
                 'can refine our criteria:\n'
                 '\n'
                 '- **Ensure the molecule contains only one aromatic ring** '
                 '(the phenol ring with the nitro group).\n'
                 '- **Exclude molecules with additional rings or fused ring '
                 'systems**.\n'
                 '- **Allow only small substituents on the phenol ring**, such '
                 'as alkyl groups or halogens, and exclude large substituents '
                 'or complex functional groups.\n'
                 '- **Verify that the nitro and hydroxyl groups are directly '
                 'attached to the aromatic ring**.\n'
                 '\n'
                 'By adding these constraints, we can more accurately classify '
                 'molecules that fit the definition of mononitrophenol: *"A '
                 'nitrophenol that is phenol carrying a single nitro '
                 'substituent at unspecified position."*\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 24,
    'num_false_positives': 11,
    'num_true_negatives': 142259,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.6857142857142857,
    'recall': 0.8,
    'f1': 0.7384615384615385,
    'accuracy': 0.9998805340829234,
    'negative_predictive_value': 0.9999578251853934}