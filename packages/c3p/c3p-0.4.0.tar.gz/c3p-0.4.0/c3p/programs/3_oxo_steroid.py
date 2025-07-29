"""
Classifies: CHEBI:47788 3-oxo steroid
"""
"""
Classifies: 3-oxo steroid
Definition: Any oxo steroid where an oxo substituent is located at position 3.
This algorithm first finds fused ring systems in the molecule and then looks for a
component that has four fused rings with sizes 5,6,6,6 and a core carbon count between 17 and 21.
Then, among the six membered rings in that fused core, it looks for a ketone group (C=O).
The function is_3_oxo_steroid takes a SMILES string as input and returns a tuple (bool, reason)
indicating whether the molecule is a 3-oxo steroid and why.
"""

from rdkit import Chem

def is_3_oxo_steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo steroid based on its SMILES string.
    A 3-oxo steroid is defined as a steroid (with a fused tetracyclic nucleus: one five-membered ring
    and three six-membered rings that together contain between roughly 17 and 21 carbons) possessing a ketone group (C=O)
    on one of the six-membered rings (i.e. in the A ring region).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if the molecule is a 3-oxo steroid, False otherwise
        str: Explanation for the classification decision
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get ring information from the molecule.
    ring_info = mol.GetRingInfo().AtomRings()
    if not ring_info:
        return False, "No rings found in molecule, so not a steroid"

    # Convert each ring (tuple of atom indices) to a set for easier processing.
    rings = [set(r) for r in ring_info]

    # Group rings into fused components: rings are fused if they share at least one atom.
    n = len(rings)
    visited = [False] * n
    components = []  # each component is a set of ring indices.
    for i in range(n):
        if visited[i]:
            continue
        comp = set([i])
        stack = [i]
        while stack:
            current = stack.pop()
            visited[current] = True
            for j in range(n):
                if not visited[j]:
                    if rings[current].intersection(rings[j]):
                        comp.add(j)
                        stack.append(j)
                        visited[j] = True
        components.append(comp)

    candidate_component = None
    # Look for a component with exactly 4 rings where the ring sizes (sorted) are [5,6,6,6].
    for comp in components:
        ring_sizes = sorted([len(rings[i]) for i in comp])
        if len(comp) == 4 and ring_sizes == [5, 6, 6, 6]:
            candidate_component = comp
            break
    if candidate_component is None:
        return False, "Steroid nucleus not found (expected four fused rings with sizes 5,6,6,6)"

    # Get the union of all atom indices in the candidate component.
    core_atom_indices = set()
    for i in candidate_component:
        core_atom_indices = core_atom_indices.union(rings[i])
    
    # Count carbon atoms in the steroid core.
    core_carbon_count = sum(1 for idx in core_atom_indices if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
    if core_carbon_count < 17 or core_carbon_count > 21:
        return False, f"Fused ring system found but with {core_carbon_count} core carbons (expected between 17 and 21)"

    # Among the rings in the candidate component, collect the six-membered rings.
    six_membered_rings = [rings[i] for i in candidate_component if len(rings[i]) == 6]
    if len(six_membered_rings) != 3:
        return False, "Fused ring system present but the number of six-membered rings is not equal to 3"

    # Now, for each six-membered ring in the core, check for a ketone.
    # A ketone group is defined as a carbon (atomic number 6) in the ring that has
    # at least one double bond to an oxygen atom (atomic number 8) and that oxygen should be terminal.
    ketone_found = False
    ketone_details = ""
    for ring in six_membered_rings:
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6:
                continue
            for bond in atom.GetBonds():
                # Check that the bond is a double bond.
                if bond.GetBondType() == Chem.BondType.DOUBLE:
                    neighbor = bond.GetOtherAtom(atom)
                    if neighbor.GetAtomicNum() == 8:
                        # Check that the oxygen is terminal (only one non-hydrogen neighbor)
                        nonH_neighbors = [nbr for nbr in neighbor.GetNeighbors() if nbr.GetAtomicNum() != 1]
                        if len(nonH_neighbors) == 1:
                            ketone_found = True
                            ketone_details = f"Ketone (C=O) found on atom index {idx} in a six-membered ring"
                            break
            if ketone_found:
                break
        if ketone_found:
            break

    if not ketone_found:
        return False, "Steroid nucleus core found but no ketone group detected on any six-membered ring (expected on position 3)"
    
    return True, f"Steroid nucleus with {core_carbon_count} core carbons and a ketone group detected: {ketone_details}"


# Optional main block for testing examples.
if __name__ == "__main__":
    test_smiles = [
        # Examples that should be classified as 3-oxo steroids:
        "[H][C@@]12CC(=O)CC[C@]1(C)[C@@]1([H])CC(=O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@H](C)CCC(O)=O",  # 3,7,12-trioxo-5beta-cholanic acid
        "[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)C=CC[C@@]34[H])[C@@]1(C)CCC(=O)C2"  # 5alpha-androst-16-en-3-one
    ]
    for s in test_smiles:
        result, reason = is_3_oxo_steroid(s)
        print("SMILES:", s)
        print("Classification:", result)
        print("Reason:", reason)
        print("-----")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47788',
                          'name': '3-oxo steroid',
                          'definition': 'Any oxo steroid where an oxo '
                                        'substituent is located at position 3.',
                          'parents': ['CHEBI:35789', 'CHEBI:3992'],
                          'xrefs': [   'KEGG:C01876',
                                       'MetaCyc:3-Oxosteroids',
                                       'PMID:9811880'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 99,
                           'log_lines_of_code': 4.59511985013459,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
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
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
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
                                                 2,
                                                 0,
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
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 7,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 7,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'GetOtherAtom',
                                                 'GetNeighbors',
                                                 'GetBonds',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'add',
                                                 'union',
                                                 'pop',
                                                 'intersection',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_3_oxo_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in molecule, '
                                          'so not a steroid"',
                                          'False, "Steroid nucleus not found '
                                          '(expected four fused rings with '
                                          'sizes 5,6,6,6)"',
                                          'False, f"Fused ring system found '
                                          'but with {core_carbon_count} core '
                                          'carbons (expected between 17 and '
                                          '21)"',
                                          'False, "Fused ring system present '
                                          'but the number of six-membered '
                                          'rings is not equal to 3"',
                                          'False, "Steroid nucleus core found '
                                          'but no ketone group detected on any '
                                          'six-membered ring (expected on '
                                          'position 3)"',
                                          'True, f"Steroid nucleus with '
                                          '{core_carbon_count} core carbons '
                                          'and a ketone group detected: '
                                          '{ketone_details}"'],
                           'returns_count': 7,
                           'complexity': 6.719023970026919},
    'message': '\n'
               'Attempt failed: F1 score of 0.10692375109553025 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]12CC(=O)CC[C@]1(C)[C@@]1([H])CC(=O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])C(=O)C2)[C@H](C)CCC(O)=O '
               'NAME: 3,7,12-trioxo-5beta-cholanic acid REASON: CORRECT '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@]([C@@]4(C(=CC(CC4)=O)[C@H](C3)C)C)(CC[C@@]2([C@@](C1)(O)C(=O)C)C)[H])[H])[H] '
               'NAME: medroxyprogesterone REASON: CORRECT Steroid nucleus with '
               'a ketone group at position 3 identified\n'
               ' * SMILES: '
               '[C@@H]1(CC(C=C2[C@]1([C@@]3([C@@](CC2)([C@]4([C@](CC3)(C(CC4)=O)C)[H])[H])[H])C)=O)O '
               'NAME: 1alpha-hydroxyandrost-4-ene-3,17-dione REASON: CORRECT '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(CC(C1)=O)[H])[H])(CC[C@@H]4O)[H])CO)[H])C '
               'NAME: 18-hydroxy-5alpha-dihydrotestosterone REASON: CORRECT '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               '[H][C@]12CCC(=O)C=C1CC[C@]1([H])[C@]2([H])CC[C@]2(C)[C@@H](O)CC[C@@]12[H] '
               'NAME: nandrolone REASON: CORRECT Steroid nucleus with a ketone '
               'group at position 3 identified\n'
               ' * SMILES: '
               'COC[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@](C)(O)[C@@]4(C)CC[C@H]23)CC1=O '
               'NAME: '
               '17beta-Hydroxy-2alpha-(methoxymethyl)-17-methyl-5alpha-androstan-3-one '
               'REASON: CORRECT Steroid nucleus with a ketone group at '
               'position 3 identified\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@]([C@@]4([C@](CC([C@@H](C4)C)=O)(CC3)[H])C)(CC[C@@]2([C@H](C1)OC(CC)=O)C)[H])[H])[H] '
               'NAME: dromostanolone propionate REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               '[C@]12([C@]([C@]3([C@](CC1)([C@@]4(C(=CC(CC4)=O)C[C@H]3O)C)[H])[H])(CC[C@@]2([C@@H](CCC[C@@H](C)CO)C)[H])[H])C '
               'NAME: (25R)-7alpha,26-dihydroxycholest-4-en-3-one REASON: '
               'CORRECT Steroid nucleus with a ketone group at position 3 '
               'identified\n'
               ' * SMILES: '
               'C1C(C=C2[C@](C1)([C@@]3([C@@](CC2)([C@]4([C@](C[C@@H]3O)([C@](CC4)(C(C)=O)O)C)[H])[H])[H])C)=O '
               'NAME: 21-deoxycortisol REASON: CORRECT Steroid nucleus with a '
               'ketone group at position 3 identified\n'
               ' * SMILES: '
               'C=1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C=CC2=CC(C1)=O)[H])(CCC4=O)[H])C)[H])C '
               'NAME: androsta-1,4,6-triene-3,17-dione REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CC(=O)[C@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O '
               'NAME: 17beta-Hydroxy-5alpha-androstan-3,6-dione REASON: '
               'CORRECT Steroid nucleus with a ketone group at position 3 '
               'identified\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2(C)C3=C(CC[C@]12C)[C@@]1(C)CCC(=O)C(C)(C)C1CC3=O)[C@H](C)C[C@H](O)\\C=C(/C)C(O)=O '
               'NAME: hainanic acid A REASON: CORRECT Steroid nucleus with a '
               'ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C=CC2=CC(C1)=O)[H])(CC[C@@]4([C@@H](CCC(=O)O)C)[H])[H])C)[H])C '
               'NAME: 3-oxochola-4,6-dien-24-oic acid REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@]([C@@]4([C@](CC([C@@H](C4)C)=O)(CC3)[H])C)(CC[C@@]2([C@H](C1)O)C)[H])[H])[H] '
               'NAME: metholone REASON: CORRECT Steroid nucleus with a ketone '
               'group at position 3 identified\n'
               ' * SMILES: '
               '[C@]12([C@]([C@]3([C@](CC1)([C@@]4(C(=CC(CC4)=O)C=C3)C)[H])[H])(CC[C@@]2([C@@H](CCCC(C)(C)O)C)[H])[H])C '
               'NAME: 25-hydroxycholest-4,6-dien-3-one REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               '[C@@]12([C@@]([C@@]3([C@]([C@@H](C(CC3)=O)C)(CC1)[H])C)(CC[C@@]4([C@H](CC[C@@]24[H])O)C)[H])[H] '
               'NAME: 17beta-hydroxy-4alpha-methyl-5alpha-androstan-3-one '
               'REASON: CORRECT Steroid nucleus with a ketone group at '
               'position 3 identified\n'
               ' * SMILES: '
               'C1=CC(C=C2[C@]1([C@@]3([C@@](CC2)([C@]4([C@](C[C@@H]3O)([C@]([C@@H](C4)C)(C(CO)=O)O)C)[H])[H])F)C)=O '
               'NAME: dexamethasone REASON: CORRECT Steroid nucleus with a '
               'ketone group at position 3 identified\n'
               ' * SMILES: '
               'C[C@]12CCC(=O)C[C@H]1CC[C@H]1[C@@H]3CC[C@H](C(=O)CO)[C@]3(C[C@H](O)[C@H]21)C=O '
               'NAME: 5beta-dihydroaldosterone REASON: CORRECT Steroid nucleus '
               'with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1C(C=C2[C@](C1)([C@@]3([C@@](CC2)([C@@]4([H])[C@@](CC3)(C)[C@H]([C@@H](C4)O)O)[H])[H])C)=O '
               'NAME: 16alpha-hydroxytestosterone REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CCC(=O)C[C@@H]1CC3 '
               'NAME: 5alpha-cholest-8-en-3-one REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               '[C@]12([C@]([C@]3([C@](CC1)([C@@]4(C(=CC(C=C4)=O)CC3)C)[H])[H])(CC[C@@]2([C@@H](CCCC(C)C)C)[H])[H])C '
               'NAME: cholest-1,4-dien-3-one REASON: CORRECT Steroid nucleus '
               'with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC([C@]4([C@]([C@@]3([C@H](C[C@@]2(CC(C1)=O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(O)=O)C)[H])C)=O)[H])C '
               'NAME: 7beta-hydroxy-3,12-dioxo-5beta-cholanic acid REASON: '
               'CORRECT Steroid nucleus with a ketone group at position 3 '
               'identified\n'
               ' * SMILES: '
               'CC1=C2CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@@H]3[C@H]2CCC1=O '
               'NAME: 17beta-Hydroxy-4-methylestr-4-en-3-one REASON: CORRECT '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(CC(C1)=O)[H])[H])(CC[C@@H]4O)[H])C)[H])C=O '
               'NAME: 19-oxo-5alpha-dihydrotestosterone REASON: CORRECT '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2CC(C1)=O)[H])(CC[C@@H]4O)[H])C)[H])C '
               'NAME: 17beta-hydroxy-5-androsten-3-one REASON: CORRECT Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               'False positives: SMILES: '
               '[H][C@@]12C[C@H](O)C(=O)C(C)(C)C1=CC[C@@]1([H])[C@]3(C)C[C@@H](O)[C@]([H])([C@@](C)(O)C(=O)\\C=C\\C(C)(C)O)[C@@]3(C)CC(=O)[C@@]21C '
               'NAME: cucurbitacin D REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C(C2[C@](C3[C@@](C4(C(=O)[C@](C(C3)(C)C4=C)(O)C(=O)C)C(=O)OC)(C)CC2)(C)CC1)(C)C '
               'NAME: Preaustinoid B REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C=C2[C@H](CC[C@]3([C@H]2C[C@H](O)[C@@H]3[C@@H](CC[C@@H](C(O)(C)C)C)C)C)[C@@]4([C@H]1C[C@H](O)CC4)C '
               'NAME: Psathergosterol C REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C=C2C=CC3=C4[C@]([C@@H](/C(=C/[C@H]5OC(=O)[C@@H]([C@@H]5C)C)/C)CC4)(C)CC[C@@H]3[C@@]2(C)CC1 '
               'NAME: Penijanthoid A REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O1C(C(C2=C1C=C(O)C3=C2N(C4=C(C3=O)C=CC=C4O)C)C=5C(O)=C6C(NC7=C(C6=O)C=CC(OC)=C7OC)=CC5OC)C(O)(C)C '
               'NAME: '
               '2-[5,10-Dihydroxy-2-(2-hydroxypropan-2-yl)-11-methyl-6-oxo-1H,2H,6H,11H-furo[2,3-c]acridin-1-yl]-1-hydroxy-3,5,6-trimethoxy-9,10-dihydroacridin-9-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus with a ketone group '
               'at position 3 identified\n'
               ' * SMILES: '
               'CC1C[C@@]2(C)C(CC[C@H]3[C@@H]4CC[C@](C)(O)[C@@]4(C)C[C@H](O)[C@]23F)=CC1=O '
               'NAME: '
               '9-Fluoro-11beta,17beta-dihydroxy-2,17-dimethylandrost-4-en-3-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus with a ketone group '
               'at position 3 identified\n'
               ' * SMILES: '
               'O=C1[C@@]2(C(C3C(C4C(C(CC4)C(CCCC(C)C)C)(CC3)C)C1)(CCC(O)C2)C)[H] '
               'NAME: 5-Cholestan-3-ol-6-one REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C(C2C(C=3C(C4(C(C(CC4)C(CCC=C(CO)C)C)(CC3)C)C)=CC2)(CC1)C)(C)C '
               'NAME: '
               '17-(7-hydroxy-6-methylhept-5-en-2-yl)-4,4,10,13,14-pentamethyl-1,2,5,6,12,15,16,17-octahydrocyclopenta[a]phenanthren-3-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus with a ketone group '
               'at position 3 identified\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@@H]([C@@H](OC(=O)C)CC=C(C(=O)O)C)C)CC4)(C)CC3)C)=CC2)(C)CC1)(C)C '
               'NAME: Ganorbiformin G REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C=C2[C@@](CC[C@H](C2(C)C)O)(C)C=3[C@@H]1[C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC3)C '
               'NAME: Irpeksolactin D REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H]([C@]3(CO)C)O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1OC(=O)C)C)C(CC(=O)CC(C(=O)O)C)C)C '
               'NAME: '
               '12beta-acetoxy-3beta,28-dihydroxy-7,11,15,23-tetraoxo-5alpha-lanosta-8-en-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Steroid nucleus with a ketone '
               'group at position 3 identified\n'
               ' * SMILES: '
               'O=C1[C@H]2[C@]3([C@@]([C@H](CC3)[C@@H](CC(=O)C)C)(CC[C@]2([C@H]4C(C([C@@H](O)CC4)(C)C)=C1)C)C)C '
               'NAME: Kuguacin C REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CC[C@H](C([C@@H]3C1)(C)C)OC(=O)CC(=O)OC)C)C[C@@H](O)[C@]4([C@]2(CC[C@@H]4[C@@H](CCC(=C)[C@@H](C(=O)O)C)C)C)C '
               'NAME: Officimalonic acid F REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/C(=O)O)\\C)C)C[C@@H]4OC(=O)C)(C)CC3)C)=CC2)(C)CC1)(C)C '
               'NAME: Ganoderic acid T-Q REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/C(=O)O)\\C)C)C[C@@H]4O)(C)CC3)C)[C@@H](C2)OC(=O)C)(C)CC1)(C)C '
               'NAME: '
               '(24E)-7alpha-acetoxy-15alpha-hydroxy-3-oxolanosta-8,24-dien-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Steroid nucleus with a ketone '
               'group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C2C(C3C(C4C(C(CC4)C(CCC(C(C)C)C)C)(CC3)C)C1)(CCC(=O)C2)C '
               'NAME: Ergostane-3,6-dione REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1[C@H]([C@H]2[C@](C=3C([C@H]4[C@]([C@@H]([C@@H](CCC(=C)C(C)C)C)CC4)(C)[C@H](C3)O)=CC2)(C)CC1)C '
               'NAME: Antcamphorol G REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1[C@H]([C@H]2[C@]([C@]34C([C@H](O)[C@H](C3)[C@@](CC4)(O)CO)=CC2)(C)CC1)C '
               'NAME: Aphidicolin A66 REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)CC3[C@@]2(CCC([C@H]3C)=O)C)C4CC[C@@H]([C@]4(C1)C)[C@@H](CCC(=C)C(C(=O)OC)C)C '
               'NAME: Zhankuic acid methyl ester A REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H](C3(C)C)OC(=O)C)C)[C@@]4([C@@H](O)C[C@@H]([C@]4(C1)C)[C@@H](CC(=O)CC(C(=O)O)C)C)C '
               'NAME: 3-O-acetylganoderic acid K REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'C[C@@H]1C[C@]2(C)[C@H]3[C@@H](O)C[C@@]4(C)[C@@H](CC[C@]4(O)C(=O)COC(C)=O)[C@@H]3CCC2=CC1=O '
               'NAME: '
               '11beta,17,21-Trihydroxy-2alpha-methylpregn-4-ene-3,20-dione '
               '21-acetate REASON: WRONGLY CLASSIFIED Steroid nucleus with a '
               'ketone group at position 3 identified\n'
               ' * SMILES: '
               '[H][C@@]1([C@H](C)[C@@]2(C)C[C@]3(OC2=C(C)C1=O)[C@@H](C)CC[C@@]1([H])C(C)(C)C(=O)CC[C@]31C)C(=O)OC '
               'NAME: asnovolin J REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)CC3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4([C@@H](O)CC([C@]4(C1)C)[C@@](O)(CC/C=C(/C(=O)O)\\C)C)C '
               'NAME: Resinacein E REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1OC=2C=3C(C(C)=CC2OC)=C4O[C@H](C(C4=C(C3C1=O)O)(C)C)C NAME: '
               '(-)-bipolaride A REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'with a ketone group at position 3 identified\n'
               ' * SMILES: '
               'O=C1C(C2[C@](C3=C([C@]4([C@]([C@@H](C(C(=O)O)C)CC4)(C)CC3)C)CC2)(C)CC1)(C)C '
               'NAME: Torulosic acid REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus with a ketone group at position 3 identified\n'
               'False negatives: SMILES: '
               '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)C=CC[C@@]34[H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 5alpha-androst-16-en-3-one REASON: MISSED Steroid '
               'nucleus found but no ketone group detected on the A ring '
               '(position 3)\n'
               ' * SMILES: '
               '[H][C@@]12CCC(=O)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])[C@H](O)CC2=CC(=O)CC[C@]12C '
               'NAME: 7alpha-hydroxyandrost-4-ene-3,17-dione REASON: MISSED '
               'Steroid nucleus found but no ketone group detected on the A '
               'ring (position 3)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: cholest-4-en-3-one REASON: MISSED Steroid nucleus found '
               'but no ketone group detected on the A ring (position 3)\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=C3C=CC(=O)C4=O)[C@@H]1CCC2=O NAME: '
               'estra-1,5(10)-diene-3,4,17-trione REASON: MISSED Steroid '
               'nucleus found but no ketone group detected on the A ring '
               '(position 3)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@](O)(C(=O)CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 17,21-dihydroxy-5beta-pregnane-3,11,20-trione REASON: '
               'MISSED Steroid nucleus found but no ketone group detected on '
               'the A ring (position 3)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)([C@@H](O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 20beta-dihydroprednisolone REASON: MISSED Steroid '
               'nucleus found but no ketone group detected on the A ring '
               '(position 3)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)CC[C@]12C '
               'NAME: fludrocortisone REASON: MISSED Steroid nucleus found but '
               'no ketone group detected on the A ring (position 3)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCC[C@@H](C)C(O)=O '
               'NAME: (25R)-Delta(4)-dafachronic acid REASON: MISSED Steroid '
               'nucleus found but no ketone group detected on the A ring '
               '(position 3)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)CC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCC(O)C(C)C '
               'NAME: 7alpha,24-dihydroxycholest-4-en-3-one REASON: MISSED '
               'Steroid nucleus found but no ketone group detected on the A '
               'ring (position 3)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])[C@@H](O)C[C@]12C=O)C(=O)CO '
               'NAME: aldosterone REASON: MISSED Steroid nucleus found but no '
               'ketone group detected on the A ring (position 3)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No rings found in molecule, so '
                                               'not a steroid'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No rings found in molecule, so '
                                               'not a steroid'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Steroid nucleus not found '
                                               '(expected four fused rings '
                                               'with sizes 5,6,6,6)'}],
    'sample_false_negatives': [   {   'smiles': '[C@]123[C@](C(=O)[C@]([C@@]1(CC[C@@]4([C@]5(C=CC(C([C@@]5(C[C@H]([C@@]24C)OC(=O)C6=CC=CC=C6)[H])(C)C)=O)C)[H])C)(C7=COC=C7)[H])([H])O3',
                                      'name': '7-deacetyl-7-benzoylepoxyazadiradione',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)OC(=O)CC[C@@]21[H]',
                                      'name': 'testololactone',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': 'C[C@H](CC(O)C(C)C(C)=C)[C@H]1CC[C@@]2(C)[C@@H]3[C@@H](O)C[C@@H]4[C@]5(C[C@@]35CC[C@]12C)CCC(=O)C4(C)C',
                                      'name': 'combretanone F',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@@]4(C)[C@@]3([H])CC[C@]4(C)O)[C@@]1(C)COC(=O)C2',
                                      'name': 'oxandrolone',
                                      'reason': 'Fused ring system found but '
                                                'with 16 core carbons '
                                                '(expected between 17 and 21)'},
                                  {   'smiles': '[H][C@]12CC[C@@]3(C)[C@@]([H])(CC[C@@]33CCC(=O)O3)[C@]1([H])[C@@H](CC1=CC(=O)CC[C@]21C)SC(C)=O',
                                      'name': 'spironolactone',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1(F)[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@H]2OC3(CCCC3)O[C@@]12C(=O)COC(C)=O',
                                      'name': 'amcinonide',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': 'C[C@H](C[C@@H](O)[C@H](O)C(C)(C)O)[C@H]1CC[C@@]2(C)[C@@H]3[C@@H](O)C[C@@H]4[C@]5(C[C@@]35CC[C@]12C)CCC(=O)[C@@]4(C)CO',
                                      'name': 'combretanone B',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': '[H][C@]12CC[C@@]3(C)[C@@]([H])([C@@H]4C[C@@H]4[C@@]33CCC(=O)O3)[C@]1([H])[C@H]1C[C@H]1C1=CC(=O)CC[C@]21C',
                                      'name': 'drospirenone',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': 'COC(=O)[C@@H]1CC2=CC(=O)CC[C@]2(C)[C@@]23O[C@@H]2C[C@@]2(C)[C@@H](CC[C@@]22CCC(=O)O2)[C@H]13',
                                      'name': 'eplerenone',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H]2O[C@](C)(O[C@@]12C(C)=O)c1ccccc1',
                                      'name': 'algestone acetophenide',
                                      'reason': 'Steroid nucleus not found '
                                                '(expected four fused rings '
                                                'with sizes 5,6,6,6)'}],
    'attempt': 1,
    'reasoning': 'We can see from the evaluation that our previous code was '
                 '“finding” a steroid‐nucleus by simply identifying any fused '
                 'four‐ring system with rings of sizes 5,6,6,6 and then '
                 '“checking” for any ketone (C=O) on one six‐membered ring. '
                 '(1) In many cases the identification of the tetracyclic '
                 '“steroid core” was too generous so that even a “non‐steroid” '
                 '(or a triterpenoid with extra rings or extra carbons) might '
                 'be counted as one and (2) the heuristic for picking the A '
                 'ring (the six‐membered ring not fused to the 5–membered '
                 'ring) mis‐assigned some cases, giving false negatives. \n'
                 '\n'
                 'To improve the classification we now propose the following '
                 'refinements:\n'
                 ' • First, identify fused ring systems from the molecule and '
                 'look for one that has exactly four rings with sizes '
                 '5,6,6,6.\n'
                 ' • Then (to reduce false positives) count the number of '
                 'carbon atoms that belong to the fused component. (By “core” '
                 'steroid structure we usually expect 17–21 carbons.)\n'
                 ' • Finally, instead of trying to “identify” the A ring by '
                 'disjointness from the 5–membered ring, we simply check all '
                 'six–membered rings in the candidate steroid core for the '
                 'presence of a ketone group (a carbon with an explicit double '
                 'bond to an oxygen atom that is not bonded elsewhere). If one '
                 'of these rings has such a group then we classify the '
                 'molecule as a 3–oxo steroid.\n'
                 '\n'
                 'Below is the complete Python program (using a single code '
                 'block) that implements this improved strategy. (Keep in mind '
                 'that our algorithm is heuristic and may not cover every edge '
                 'case.) \n'
                 '\n'
                 'Below is the code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 313,
    'num_false_positives': 1444,
    'num_true_negatives': 140520,
    'num_false_negatives': 23,
    'num_negatives': None,
    'precision': 0.17814456459874786,
    'recall': 0.9315476190476191,
    'f1': 0.2990922121356904,
    'accuracy': 0.9896907940969782,
    'negative_predictive_value': 0.9998363490177383}