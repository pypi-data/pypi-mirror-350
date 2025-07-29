"""
Classifies: CHEBI:51129 nitrohydrocarbon
"""
"""
Classifies: Nitrohydrocarbon
Definition: A C-nitro compound that is a hydrocarbon in which one or more hydrogens has been replaced by nitro groups.
Heuristic:
  1. The molecule must contain at least one nitro group ([N+](=O)[O-]) attached directly to a carbon atom.
  2. Remove all atoms belonging to nitro groups; the remaining heavy atoms must be almost exclusively (>=90%) carbon.
     However, a very limited number of oxygen atoms are allowed—for example, if the oxygen is part of a three‐membered ring (epoxide) that may occur in otherwise all‐carbon fused ring systems.
  3. For aromatic multi‐ring systems, if more than one ring exists, the rings should be fused.
"""

from rdkit import Chem
from rdkit.Chem import rdmolops

def is_nitrohydrocarbon(smiles: str):
    """
    Determines if a molecule is a nitrohydrocarbon based on its SMILES string.
    
    A nitrohydrocarbon is defined as a compound containing one or more nitro groups ([N+](=O)[O-])
    that are attached directly to a carbon, and whose (non-nitro) backbone is predominantly a hydrocarbon.
    
    The heuristic in this implementation is as follows:
    
      1. Check for the presence of at least one nitro group.
      2. Verify that at least one nitro group is attached to a carbon atom.
      3. Remove all atoms that are part of any nitro group.
      4. Examine the remaining (backbone) heavy atoms. They are allowed only if:
            - They are carbon atoms, or
            - They are oxygen atoms that look “epoxide-like” (i.e. in a ring and with exactly two neighbors).
      5. The backbone must contain at least 90% carbon atoms (by count of allowed heavy atoms).
      6. If the backbone is aromatic and contains multiple rings, require that the aromatic rings are fused (i.e. share at least one bond).
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule qualifies as a nitrohydrocarbon, False otherwise.
        str: A reason describing the outcome.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define the nitro group SMARTS pattern.
    nitro_smarts = Chem.MolFromSmarts("[N+](=O)[O-]")
    if not mol.HasSubstructMatch(nitro_smarts):
        return False, "No nitro group ([N+](=O)[O-]) found in the molecule"
    
    # Check that at least one nitro group is attached directly to a carbon atom.
    nitro_matches = mol.GetSubstructMatches(nitro_smarts)
    attached_to_carbon = False
    for match in nitro_matches:
        # Assume the first atom in the nitro match is the nitrogen.
        nitroN_idx = match[0]
        atomN = mol.GetAtomWithIdx(nitroN_idx)
        # Look at neighbors of the nitro nitrogen.
        for neighbor in atomN.GetNeighbors():
            # If a neighbor is carbon and is not part of this found nitro group, mark valid.
            if neighbor.GetAtomicNum() == 6 and neighbor.GetIdx() not in match:
                attached_to_carbon = True
                break
        if attached_to_carbon:
            break
    if not attached_to_carbon:
        return False, "Nitro group(s) not directly attached to a carbon atom"
    
    # Gather indices of all atoms that are part of any nitro group.
    nitro_atom_indices = set()
    for match in nitro_matches:
        nitro_atom_indices.update(match)
    
    # Create a copy of the molecule and remove nitro group atoms to obtain the backbone.
    backbone = Chem.RWMol(mol)
    # Remove atoms in descending order so indices do not shift.
    for idx in sorted(nitro_atom_indices, reverse=True):
        try:
            backbone.RemoveAtom(idx)
        except Exception:
            pass
    backbone = backbone.GetMol()
    
    # Examine the backbone heavy atoms (exclude hydrogens).
    backbone_atoms = [atom for atom in backbone.GetAtoms() if atom.GetAtomicNum() != 1]
    if not backbone_atoms:
        return False, "Backbone is empty after removing nitro groups"
    
    # Allowed atoms: carbon always; oxygen allowed only if it appears to be in an epoxide-like environment.
    allowed_atom_types = {6}  # carbon atomic number is 6
    non_carbon_atoms = 0
    carbon_count = 0
    for atom in backbone_atoms:
        atomic_num = atom.GetAtomicNum()
        if atomic_num == 6:
            carbon_count += 1
        elif atomic_num == 8:
            # Check if oxygen is allowed (for example, in an epoxide-like ring):
            # Typically, an oxygen in an epoxide is part of a ring and has exactly two heavy-atom neighbors.
            if atom.IsInRing() and len([nbr for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() != 1])==2:
                non_carbon_atoms += 1
            else:
                return False, "Backbone contains an oxygen atom not in an allowed (e.g. epoxide) environment"
        else:
            # Any other heteroatom (e.g. N, S, etc.) is not allowed
            return False, f"Backbone contains disallowed heteroatom with atomic number {atomic_num}"
    
    total_allowed = len(backbone_atoms)
    hydro_ratio = carbon_count / total_allowed
    if hydro_ratio < 0.9:
        return False, f"Backbone has only {hydro_ratio*100:.1f}% carbons (requires at least 90%); extra heteroatoms present"
    
    # For aromatic systems with multiple rings, verify that the rings are fused
    ri = backbone.GetRingInfo()
    rings = ri.AtomRings()
    if len(rings) > 1:
        # For each ring, get the set of bonds that form the ring.
        ring_bonds = []
        for ring in rings:
            bonds = set()
            ring = list(ring)
            n = len(ring)
            for i in range(n):
                a1 = ring[i]
                a2 = ring[(i + 1) % n]
                bond = frozenset((a1, a2))
                bonds.add(bond)
            ring_bonds.append(bonds)
        # Check that at least one pair of rings share at least one bond.
        fused = False
        for i in range(len(ring_bonds)):
            for j in range(i + 1, len(ring_bonds)):
                if ring_bonds[i].intersection(ring_bonds[j]):
                    fused = True
                    break
            if fused:
                break
        if not fused:
            return False, "Aromatic backbone rings are not fused (found separate isolated rings)"
    
    return True, "Molecule is a nitrohydrocarbon: nitro group(s) are attached directly to a carbon and the backbone is predominantly hydrocarbon"

# Uncomment and run the following block to perform quick tests:
# test_smiles = [
#     "[O-][N+](=O)c1cccc2C3OC3C=Cc12",  # 1-Nitronaphthalene-5,6-oxide (expected: True)
#     "[O-][N+](=O)c1ccc-2c(c1)-c1ccc([N+]([O-])=O)c3cccc-2c13",  # 3,9-Dinitrofluoranthene (expected: True)
#     "CC(C)[N+]([O-])=O",  # 2-nitropropane (expected: True)
#     "[O-][N+](=O)c1ccc(cc1)-c1ccccc1",  # 4-Nitrobiphenyl (expected: False, extra aromatic system not exclusively hydrocarbon)
# ]
#
# for s in test_smiles:
#     valid, reason = is_nitrohydrocarbon(s)
#     print(f"SMILES: {s}\nResult: {valid}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:51129',
                          'name': 'nitrohydrocarbon',
                          'definition': 'A C-nitro compound that is a '
                                        'hydrocarbon in which one or more of '
                                        'the hydrogens has been replaced by '
                                        'nitro groups.',
                          'parents': ['CHEBI:35716'],
                          'xrefs': ['PMCID:PMC3909368'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 111,
                           'log_lines_of_code': 4.709530201312334,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
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
                                                 2,
                                                 3,
                                                 2,
                                                 3,
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
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdmolops'],
                           'imports_count': 2,
                           'methods_called': [   'add',
                                                 'HasSubstructMatch',
                                                 'IsInRing',
                                                 'update',
                                                 'GetSubstructMatches',
                                                 'GetMol',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'intersection',
                                                 'append',
                                                 'GetNeighbors',
                                                 'RemoveAtom',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'RWMol',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'MolFromSmiles'],
                           'methods_called_count': 19,
                           'smarts_strings': ['[N+](=O)[O-]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_nitrohydrocarbon(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No nitro group '
                                          '([N+](=O)[O-]) found in the '
                                          'molecule"',
                                          'False, "Nitro group(s) not directly '
                                          'attached to a carbon atom"',
                                          'False, "Backbone is empty after '
                                          'removing nitro groups"',
                                          'False, "Backbone contains an oxygen '
                                          'atom not in an allowed (e.g. '
                                          'epoxide) environment"',
                                          'False, f"Backbone contains '
                                          'disallowed heteroatom with atomic '
                                          'number {atomic_num}"',
                                          'False, f"Backbone has only '
                                          '{hydro_ratio*100:.1f}% carbons '
                                          '(requires at least 90%); extra '
                                          'heteroatoms present"',
                                          'False, "Aromatic backbone rings are '
                                          'not fused (found separate isolated '
                                          'rings)"',
                                          'True, "Molecule is a '
                                          'nitrohydrocarbon: nitro group(s) '
                                          'are attached directly to a carbon '
                                          'and the backbone is predominantly '
                                          'hydrocarbon"'],
                           'returns_count': 9,
                           'complexity': 7.741906040262466},
    'message': '\n'
               'Attempt failed: F1 score of 0.3492063492063492 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: [O-][N+](=O)c1cccc2C3OC3C=Cc12 NAME: '
               '1-Nitronaphthalene-5,6-oxide REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: '
               '[O-][N+](=O)c1ccc-2c(c1)-c1ccc([N+]([O-])=O)c3cccc-2c13 NAME: '
               '3,9-Dinitrofluoranthene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)CCCCCCC NAME: 1-nitroheptane REASON: '
               'CORRECT Molecule is a nitrohydrocarbon: nitro group(s) are '
               'attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2cccc([N+]([O-])=O)c2c1 NAME: '
               '1,7-dinitronaphthalene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2ccc(cc2c1)[N+]([O-])=O NAME: '
               '2,7-dinitronaphthalene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc([N+]([O-])=O)c2ccccc12 NAME: '
               '1,4-dinitronaphthalene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: CC(C)[N+]([O-])=O NAME: 2-nitropropane REASON: '
               'CORRECT Molecule is a nitrohydrocarbon: nitro group(s) are '
               'attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1cccc2c(cccc12)[N+]([O-])=O NAME: '
               '1,5-dinitronaphthalene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)C=C NAME: nitroethene REASON: CORRECT '
               'Molecule is a nitrohydrocarbon: nitro group(s) are attached '
               'directly to a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1cccc2cccc([N+]([O-])=O)c12 NAME: '
               '1,8-dinitronaphthalene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: '
               '[O-][N+](=O)c1cccc-2c1-c1cccc3c(ccc-2c13)[N+]([O-])=O NAME: '
               '3,7-Dinitrofluoranthene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2ccc3cccc4ccc1c2c34 NAME: '
               '1-nitropyrene REASON: CORRECT Molecule is a nitrohydrocarbon: '
               'nitro group(s) are attached directly to a carbon and backbone '
               'is (mostly) hydrocarbon\n'
               ' * SMILES: CC(C)CC[N+]([O-])=O NAME: 3-methyl-1-nitrobutane '
               'REASON: CORRECT Molecule is a nitrohydrocarbon: nitro group(s) '
               'are attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2ccccc2c1 NAME: 2-nitronaphthalene '
               'REASON: CORRECT Molecule is a nitrohydrocarbon: nitro group(s) '
               'are attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1cccc2C=CC3OC3c12 NAME: '
               '1-Nitronaphthalene-7,8-oxide REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)C1=C(C(=C(C(=C1[2H])[2H])[2H])[2H])[2H] '
               'NAME: nitrobenzene-d5 REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: CCC[N+]([O-])=O NAME: 1-nitropropane REASON: '
               'CORRECT Molecule is a nitrohydrocarbon: nitro group(s) are '
               'attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2-c3ccccc3-c3cccc1c23 NAME: '
               '3-Nitrofluoranthene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccccc1 NAME: nitrobenzene REASON: '
               'CORRECT Molecule is a nitrohydrocarbon: nitro group(s) are '
               'attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1cc([N+]([O-])=O)c2ccccc2c1 NAME: '
               '1,3-dinitronaphthalene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc-2c(Cc3ccccc-23)c1 NAME: '
               '2-nitrofluorene REASON: CORRECT Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1cccc2ccccc12 NAME: 1-nitronaphthalene '
               'REASON: CORRECT Molecule is a nitrohydrocarbon: nitro group(s) '
               'are attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               'False positives: SMILES: '
               'C1CC(C2=CC=CC=C2C1)NCC3=CC=C(C=C3)[N+](=O)[O-] NAME: '
               'N-[(4-nitrophenyl)methyl]-1,2,3,4-tetrahydronaphthalen-1-amine '
               'REASON: WRONGLY CLASSIFIED Molecule is a nitrohydrocarbon: '
               'nitro group(s) are attached directly to a carbon and backbone '
               'is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc(cc1)-c1ccccc1 NAME: '
               '4-Nitrobiphenyl REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc(cc1)\\C=C\\c1ccccc1 NAME: '
               '(E)-4-nitrostilbene REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: Cc1ccc(cc1[N+]([O-])=O)[N+]([O-])=O NAME: '
               '2,4-dinitrotoluene REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1cc2c3ccccc3ccc2c2ccccc12 NAME: '
               '6-Nitrochrysene REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1c2ccccc2c2ccc3cccc4ccc1c2c34 NAME: '
               '6-Nitrobenzo[a]pyrene REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [H]C(=C([H])c1ccc(cc1)[N+]([O-])=O)c1ccc(cc1)N(C)C '
               "NAME: 4-dimethylamino-4'-nitrostilbene REASON: WRONGLY "
               'CLASSIFIED Molecule is a nitrohydrocarbon: nitro group(s) are '
               'attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: '
               'C=1(C)[C-]([N+](=O)[O-])CC(CC1[N+]([O-])=O)[N+](=O)[O-] NAME: '
               '2-methyl-1,3,5-trinitrocyclohex-2-en-1-ide REASON: WRONGLY '
               'CLASSIFIED Molecule is a nitrohydrocarbon: nitro group(s) are '
               'attached directly to a carbon and backbone is (mostly) '
               'hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2ccc3ccc([N+]([O-])=O)c4ccc1c2c34 '
               'NAME: 1,8-Dinitropyrene REASON: WRONGLY CLASSIFIED Molecule is '
               'a nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)CCCC NAME: 1-nitrobutane REASON: '
               'WRONGLY CLASSIFIED Molecule is a nitrohydrocarbon: nitro '
               'group(s) are attached directly to a carbon and backbone is '
               '(mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1c2ccccc2cc2c1ccc1ccccc21 NAME: '
               '7-Nitrobenz[a]anthracene REASON: WRONGLY CLASSIFIED Molecule '
               'is a nitrohydrocarbon: nitro group(s) are attached directly to '
               'a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)c1ccc2c3cccc4cccc(c5cccc1c25)c34 NAME: '
               '3-Nitroperylene REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: Cc1ccc(cc1)[N+]([O-])=O NAME: 4-nitrotoluene '
               'REASON: WRONGLY CLASSIFIED Molecule is a nitrohydrocarbon: '
               'nitro group(s) are attached directly to a carbon and backbone '
               'is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)C1CC(C(C)C)C=CC1=C NAME: '
               'cis-6-Nitro-p-mentha-1(7),2-diene REASON: WRONGLY CLASSIFIED '
               'Molecule is a nitrohydrocarbon: nitro group(s) are attached '
               'directly to a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: Cc1c(cc(cc1[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O '
               'NAME: 2,4,6-trinitrotoluene REASON: WRONGLY CLASSIFIED '
               'Molecule is a nitrohydrocarbon: nitro group(s) are attached '
               'directly to a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: O=[N+]([O-])/C=C/C=1C2=C(C=CC=C2)NC1C NAME: '
               'Labindole B REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: '
               'CCN1C=C(C2=CC=CC=C21)C(C3=CC=CC=C3)C(C(=O)C)[N+](=O)[O-] NAME: '
               '4-(1-ethyl-3-indolyl)-3-nitro-4-phenyl-2-butanone REASON: '
               'WRONGLY CLASSIFIED Molecule is a nitrohydrocarbon: nitro '
               'group(s) are attached directly to a carbon and backbone is '
               '(mostly) hydrocarbon\n'
               ' * SMILES: C=1C2=C(C=CC1[N+](=O)[O-])OC(C=C2)C=3C=CC=CC3 NAME: '
               '6-nitro-2-phenyl-2H-chromene REASON: WRONGLY CLASSIFIED '
               'Molecule is a nitrohydrocarbon: nitro group(s) are attached '
               'directly to a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: [O-][N+](=O)C1=CC=C(N2CCCCC2)C=C1 NAME: '
               '1-(4-nitrophenyl)piperidine REASON: WRONGLY CLASSIFIED '
               'Molecule is a nitrohydrocarbon: nitro group(s) are attached '
               'directly to a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)Oc1ccc(cc1)[N+]([O-])=O NAME: '
               'p-nitrophenyl palmitate REASON: WRONGLY CLASSIFIED Molecule is '
               'a nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC[C@@]1(C)O[C@@H]1Cc1c[nH]c(c1)[N+]([O-])=O '
               'NAME: Nitropyrrolin B REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: CC[C@@H](C)c1cc(cc(c1O)[N+]([O-])=O)[N+]([O-])=O '
               'NAME: (R)-dinoseb REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: OC1c2ccccc2-c2ccc(cc12)[N+]([O-])=O NAME: '
               '9-Hydroxy-2-nitrofluorene REASON: WRONGLY CLASSIFIED Molecule '
               'is a nitrohydrocarbon: nitro group(s) are attached directly to '
               'a carbon and backbone is (mostly) hydrocarbon\n'
               ' * SMILES: '
               'CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)C(C)(C)C)[N+](=O)[O-] NAME: '
               '4-tert-butyl-N-(4-methyl-3-nitrophenyl)benzamide REASON: '
               'WRONGLY CLASSIFIED Molecule is a nitrohydrocarbon: nitro '
               'group(s) are attached directly to a carbon and backbone is '
               '(mostly) hydrocarbon\n'
               ' * SMILES: C1=CC=C(C(=C1C)[N+]([O-])=O)[N+]([O-])=O NAME: '
               '2,3-dinitrotoluene REASON: WRONGLY CLASSIFIED Molecule is a '
               'nitrohydrocarbon: nitro group(s) are attached directly to a '
               'carbon and backbone is (mostly) hydrocarbon\n'
               'False negatives: SMILES: '
               'C1=CC=C2C(=C1)C=CC(=C2O)NN=C3C4=C(C=C(C=C4)[N+](=O)[O-])C(=CC3=O)S(=O)(=O)O '
               'NAME: '
               '4-[(1-hydroxy-2-naphthalenyl)hydrazinylidene]-7-nitro-3-oxo-1-naphthalenesulfonic '
               'acid REASON: MISSED Backbone has only 71.4% carbons (requires '
               'at least 90%); extra heteroatoms present\n'
               ' * SMILES: '
               'C1=CC2=C(C=CC3=C2C(=C1)C(=O)N(C3=O)CCC(=O)O)[N+](=O)[O-] NAME: '
               '3-(6-nitro-1,3-dioxo-2-benzo[de]isoquinolinyl)propanoic acid '
               'REASON: MISSED Backbone has only 75.0% carbons (requires at '
               'least 90%); extra heteroatoms present\n'
               ' * SMILES: O\\N=C1\\C(=O)Nc2c1cc(c1CCCCc21)N(=O)=O NAME: '
               'NS-102 REASON: MISSED Backbone has only 75.0% carbons '
               '(requires at least 90%); extra heteroatoms present\n'
               ' * SMILES: '
               'C1=CC(=CC(=C1)N2C(=O)C3=CC(=CC4=CC(=CC(=C43)C2=O)[N+](=O)[O-])[N+](=O)[O-])C(=O)O '
               'NAME: '
               '3-(5,8-dinitro-1,3-dioxo-2-benzo[de]isoquinolinyl)benzoic acid '
               'REASON: MISSED Backbone has only 79.2% carbons (requires at '
               'least 90%); extra heteroatoms present\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Nitro group(s) not directly '
                                               'attached to a carbon atom'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No nitro group ([N+](=O)[O-]) '
                                               'found in the molecule'}],
    'sample_false_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C=CC(=C2O)NN=C3C4=C(C=C(C=C4)[N+](=O)[O-])C(=CC3=O)S(=O)(=O)O',
                                      'name': '4-[(1-hydroxy-2-naphthalenyl)hydrazinylidene]-7-nitro-3-oxo-1-naphthalenesulfonic '
                                              'acid',
                                      'reason': 'Backbone contains an oxygen '
                                                'atom not in an allowed (e.g. '
                                                'epoxide) environment'},
                                  {   'smiles': 'C1=CC2=C(C=CC3=C2C(=C1)C(=O)N(C3=O)CCC(=O)O)[N+](=O)[O-]',
                                      'name': '3-(6-nitro-1,3-dioxo-2-benzo[de]isoquinolinyl)propanoic '
                                              'acid',
                                      'reason': 'Backbone contains an oxygen '
                                                'atom not in an allowed (e.g. '
                                                'epoxide) environment'},
                                  {   'smiles': 'O\\N=C1\\C(=O)Nc2c1cc(c1CCCCc21)N(=O)=O',
                                      'name': 'NS-102',
                                      'reason': 'Backbone contains an oxygen '
                                                'atom not in an allowed (e.g. '
                                                'epoxide) environment'},
                                  {   'smiles': 'C1=CC(=CC(=C1)N2C(=O)C3=CC(=CC4=CC(=CC(=C43)C2=O)[N+](=O)[O-])[N+](=O)[O-])C(=O)O',
                                      'name': '3-(5,8-dinitro-1,3-dioxo-2-benzo[de]isoquinolinyl)benzoic '
                                              'acid',
                                      'reason': 'Backbone contains disallowed '
                                                'heteroatom with atomic number '
                                                '7'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before the code. We noticed that the '
                 'previous approach was classifying many non‐nitrohydrocarbons '
                 'as true because it only “masked” the nitro groups and then '
                 'checked that the remaining heavy‐atom backbone was ≥90% '
                 'carbon. However, some false positives (e.g. molecules '
                 'bearing other heteroatoms such as extra nitrogen or '
                 'substituents attached to a nitrobenzene framework) showed up '
                 'because we did not “police” the backbone sufficiently. '
                 '(Likewise, some molecules that are functionally '
                 '“nitrohydrocarbons” but have extra groups (like an epoxide '
                 'in “1‑Nitronaphthalene‑7,8‑oxide”) were inconsistently '
                 'handled.) \n'
                 '\n'
                 'To fix this we now add an extra backbone check. After '
                 '“masking” nitro group atoms we iterate over every heavy atom '
                 'remaining. We allow the atom if it is a carbon or if it is '
                 'an oxygen that appears only in very “hydrocarbon‐like” '
                 'contexts (for example, in a small ring such as an epoxide) '
                 'because a hydrocarbon by strict definition should contain '
                 'only carbons and hydrogens. Any non‐allowed atoms (e.g. '
                 'extra nitrogen, sulfur, or oxygen in non‐epoxide '
                 'environments) cause rejection. We also keep the requirement '
                 'that at least one nitro group ([N+](=O)[O-]) is present and '
                 'attached directly to a carbon, and for fused aromatic ring '
                 'systems we insist that if there are multiple rings they '
                 'share at least one bond. \n'
                 '\n'
                 'Below is the complete updated Python program.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 22,
    'num_false_positives': 36,
    'num_true_negatives': 142238,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.3793103448275862,
    'recall': 0.8461538461538461,
    'f1': 0.5238095238095238,
    'accuracy': 0.9997189037245257,
    'negative_predictive_value': 0.999971878910589}