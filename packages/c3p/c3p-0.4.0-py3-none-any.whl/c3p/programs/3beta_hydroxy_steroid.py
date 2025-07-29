"""
Classifies: CHEBI:36836 3beta-hydroxy steroid
"""
"""
Classifies: 3β-hydroxy steroid
Definition: A 3-hydroxy steroid in which the 3-hydroxy substituent is in the β‐position.
The program first looks for a steroid nucleus – defined as a fused tetracyclic ring system 
composed of one 5-membered and three 6-membered rings (with the rings being predominantly carbon) 
– and then it confirms that at least one beta‐oriented hydroxyl group ([C@@H](O)) is attached 
to an atom within that nucleus. Additionally, to avoid picking up large conjugated steroids 
(which are not our target simple 3β-hydroxy steroids), the code verifies that the nucleus constitutes 
at least 50% of the atoms in the molecule.
"""

from rdkit import Chem

def is_3beta_hydroxy_steroid(smiles: str):
    """
    Determines if a molecule is a 3β-hydroxy steroid based on its SMILES string.
    The classifier checks:
      1. Whether a steroid nucleus is present (a fused tetracyclic system with one 5-membered and three 6-membered rings).
         (Rings are filtered to have either 5 or 6 atoms and at least 67% carbons.)
      2. That the nucleus is not “diluted” by many extra substituents (the atoms in the nucleus must represent at least 50% of the molecule).
      3. That there is at least one beta-oriented hydroxyl group ([C@@H](O)) attached to an atom of the nucleus.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a 3β-hydroxy steroid, False otherwise.
        str: Explanation for the classification decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get all rings (as tuples of atom indices) from the molecule.
    ring_info = mol.GetRingInfo().AtomRings()
    
    # Filter rings: allow only rings of size 5 or 6 with at least ~67% carbons.
    filtered_rings = []
    for ring in ring_info:
        if len(ring) not in (5, 6):
            continue
        n_carbon = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
        if n_carbon / len(ring) >= 0.67:
            filtered_rings.append(ring)
    
    if not filtered_rings:
        return False, "No appropriate rings found for steroid nucleus"
    
    # Build a graph of rings. Two rings are “fused” if they share at least 2 atoms.
    ring_graph = {i: set() for i in range(len(filtered_rings))}
    for i in range(len(filtered_rings)):
        set_i = set(filtered_rings[i])
        for j in range(i+1, len(filtered_rings)):
            set_j = set(filtered_rings[j])
            if len(set_i & set_j) >= 2:
                ring_graph[i].add(j)
                ring_graph[j].add(i)
    
    # Find connected components (fused ring clusters) in the ring graph.
    seen = set()
    fused_components = []
    for i in ring_graph:
        if i in seen:
            continue
        stack = [i]
        component = set()
        while stack:
            cur = stack.pop()
            if cur in component:
                continue
            component.add(cur)
            for neighbor in ring_graph[cur]:
                if neighbor not in component:
                    stack.append(neighbor)
        seen |= component
        fused_components.append(component)
    
    # Look for a fused component that has at least 4 rings.
    steroid_component = None
    for comp in fused_components:
        if len(comp) >= 4:
            # Count how many 5-membered and 6-membered rings are in this component.
            n5 = sum(1 for idx in comp if len(filtered_rings[idx]) == 5)
            n6 = sum(1 for idx in comp if len(filtered_rings[idx]) == 6)
            if n5 >= 1 and n6 >= 3:
                steroid_component = comp
                break
    if steroid_component is None:
        return False, "Steroid nucleus not found (no fused tetracyclic system with expected ring sizes)"
    
    # Collect all atom indices that belong to the steroid nucleus.
    steroid_atoms = set()
    for idx in steroid_component:
        steroid_atoms.update(filtered_rings[idx])
    
    # As an extra precaution, check that the nucleus makes up at least 50% of the heavy atoms.
    if len(steroid_atoms) / mol.GetNumAtoms() < 0.5:
        return False, "Steroid nucleus constitutes less than 50% of the molecule's atoms"
    
    # Define SMARTS for a beta-oriented hydroxyl group.
    # In SMILES, a β OH group is typically expressed as [C@@H](O).
    beta_hydroxy_query = Chem.MolFromSmarts("[C@@H](O)")
    beta_matches = mol.GetSubstructMatches(beta_hydroxy_query)
    if not beta_matches:
        return False, "Beta-oriented hydroxyl group not found"
    
    # Check whether at least one beta–hydroxy carbon is part of the steroid nucleus.
    found_beta_in_nucleus = any(match[0] in steroid_atoms for match in beta_matches)
    if not found_beta_in_nucleus:
        return False, "Beta-oriented hydroxyl group not attached to the steroid nucleus"
    
    return True, "Molecule contains a steroid nucleus with a beta-oriented (3β) hydroxyl group"

# Example usage (uncomment to test):
# test_smiles = "[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@@H](O)C(C)C"  # (24R)-24-hydroxycholesterol
# result, reason = is_3beta_hydroxy_steroid(test_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36836',
                          'name': '3beta-hydroxy steroid',
                          'definition': 'A 3-hydroxy steroid in which the '
                                        '3-hydroxy substituent is in the  '
                                        'beta-position.',
                          'parents': ['CHEBI:35681', 'CHEBI:36834'],
                          'xrefs': [   'KEGG:C02945',
                                       'MetaCyc:3-Beta-Hydroxysterols',
                                       'PMID:10535978',
                                       'PMID:12829805'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 86,
                           'log_lines_of_code': 4.454347296253507,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
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
                                                 4,
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
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 2,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetNumAtoms',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'pop',
                                                 'MolFromSmarts',
                                                 'append',
                                                 'update',
                                                 'GetRingInfo',
                                                 'add',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['[C@@H](O)'],
                           'smarts_strings_count': 1,
                           'defs': ['is_3beta_hydroxy_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No appropriate rings found '
                                          'for steroid nucleus"',
                                          'False, "Steroid nucleus not found '
                                          '(no fused tetracyclic system with '
                                          'expected ring sizes)"',
                                          'False, "Steroid nucleus constitutes '
                                          "less than 50% of the molecule's "
                                          'atoms"',
                                          'False, "Beta-oriented hydroxyl '
                                          'group not found"',
                                          'False, "Beta-oriented hydroxyl '
                                          'group not attached to the steroid '
                                          'nucleus"',
                                          'True, "Molecule contains a steroid '
                                          'nucleus with a beta-oriented (3β) '
                                          'hydroxyl group"'],
                           'returns_count': 7,
                           'complexity': 5.890869459250702},
    'message': '\n'
               'Attempt failed: F1 score of 0.09220985691573927 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@@H](O)C(C)C '
               'NAME: (24R)-24-hydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'C1[C@]2([C@]3(C[C@H](C1)O)[C@H]([C@H](C4=C2CC[C@]5([C@@]4(C(C[C@@H]5[C@@H](/C=C/[C@@H](C(C)C)C)C)=O)O)C)O)O3)C '
               'NAME: '
               '(22E,24R)-5alpha,6alpha-epoxy3beta,7alpha,14beta-trihydroxy-ergosta-8,22,dien-15-one '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@H](C)C(C)C '
               'NAME: ergosta-5,7-dien-3beta-ol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'C12=C([C@]3([C@]([C@](CC3)([C@@H](CCC=C(C)C)C)[H])(C)CC1)[H])CC[C@@]4([C@@]2(CC[C@@H]([C@@]4(CO)C)O)C)[H] '
               'NAME: '
               '4beta-hydroxymethyl-4alpha-methyl-5alpha-cholesta-8,24-dien-3beta-ol '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=CC[C@]4([H])[C@](C)(CC[C@H](O)[C@@]4(C)C(O)=O)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: '
               '3beta-hydroxy-4beta-methyl-5alpha-cholest-7-ene-4alpha-carboxylic '
               'acid REASON: CORRECT Molecule contains a steroid nucleus with '
               'a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@H](O)CCC(C)C '
               'NAME: (22R)-22-hydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC=C(C)C)[C@@]1(C)CC[C@H](O)C2C '
               'NAME: 4-methylzymosterol REASON: CORRECT Molecule contains a '
               'steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)CCC(C)C '
               'NAME: (22S)-22-hydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C(C=C2C[C@H](C1)O)=O)[H])(CC[C@@]4([C@H](C)CCC[C@@H](C)CO)[H])[H])C)[H])C '
               'NAME: (25R)-3beta,26-dihydroxycholest-5-en-7-one REASON: '
               'CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C(C=C2C[C@H](C1)O)=O)[H])(CC[C@@]4([C@H](C)CCCC(C)(C)O)[H])[H])C)[H])C '
               'NAME: 7-keto-25-hydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'C1[C@H](O)C[C@@]2([C@@](C1)(C)[C@]3(CC[C@@]4(C)[C@@]([C@]35[C@H](C2)O5)(CC[C@@H]4C6=CC(=O)OC6)O)[H])[H] '
               'NAME: tanghinigenin REASON: CORRECT Molecule contains a '
               'steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H]([C@H](O)C[C@@]21[H])C(C)=O '
               'NAME: 16alpha-hydroxypregnenolone REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'CC(C)[C@@H](C)\\C=C\\[C@@H](C)[C@H]1CC[C@H]2C3=C[C@@H](O)[C@@]4(O)C[C@@H](O)CC[C@]4(C)[C@@]3(O)CC[C@]12C '
               'NAME: '
               '(22E,24R)-ergosta-7,22-diene-3beta,5alpha,6beta,9alpha-tetrol '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@]2(C)[C@]1([H])[C@H](O)C[C@]1([H])[C@@]3(C)CC[C@H](O)C(C)(C)[C@]3([H])[C@H](C[C@@]21C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@](C)(CCC=C(C)C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: ginsenoside Rg1 REASON: CORRECT Molecule contains a '
               'steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'CC(C)C(=C)CC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@@H]1CC3 '
               'NAME: 4,4-dimethyl-5alpha-ergosta-8,24(28)-dien-3beta-ol '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1 '
               'NAME: dihydrodigitoxin REASON: CORRECT Molecule contains a '
               'steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@@]2(CO)C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@@H]1CC3 '
               'NAME: lanost-8-ene-3beta,30-diol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'C12=C([C@]3([C@]([C@](CC3)([C@@H](CCC=C(C)C)C)[H])(C)CC1)[H])CC[C@@]4([C@@]2(CC[C@@H](C4(C)C)O)C)[H] '
               'NAME: 14-demethyllanosterol REASON: CORRECT Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4(C)[C@@]5(C(C)=O)[C@@H](C[C@]4([C@@]3(CC=C2C[C@H](C1)O)[H])[H])O5)[H])C '
               'NAME: 3beta-hydroxy-16alpha,17alpha-epoxypregnenolone REASON: '
               'CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=CC[C@]4([H])[C@](C)(CC[C@H](O)[C@]4(C)C(O)=O)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: '
               '3beta-hydroxy-4alpha-methyl-5alpha-cholest-7-ene-4beta-carboxylic '
               'acid REASON: CORRECT Molecule contains a steroid nucleus with '
               'a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC=C2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@]1([H])CC3)[C@H](C)CCC=C(C)C '
               'NAME: 4,4-dimethyl-5alpha-cholesta-8,14,24-trien-3beta-ol '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)[C@H]([C@@H]1CC3)C(O)=O '
               'NAME: 3beta-hydroxy-5alpha-cholest-8-ene-4alpha-carboxylic '
               'acid REASON: CORRECT Molecule contains a steroid nucleus with '
               'a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'CC(C)C(=C)CC[C@@H](C)[C@H]1CC[C@H]2C3=C([C@H](O)C[C@]12C)[C@@]1(C)CC[C@H](O)C[C@@H]1CC3=O '
               'NAME: 3beta,11alpha-dihydroxyergosta-8,24(28)-dien-7-one '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C4[C@H](O)C[C@]([H])([C@H](C)CCCC(C)C)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@H](O)C2 '
               'NAME: 5alpha-cholest-8(14)-en-3beta,15beta-diol REASON: '
               'CORRECT Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[C@]12([C@]3([C@]([H])([C@@H](C[C@]2([H])[C@@]4([C@@]([H])([C@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)CO)C([C@H](CC4)O)(C)C)C)O)[C@]([H])(CC3)[C@](CCC=C(C)C)(O)C)C)C '
               'NAME: (20S)-ginsenoside Rh1 REASON: CORRECT Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               'False positives: SMILES: '
               'CO[C@H]1C[C@H](O[C@H]2CC[C@@]3(C)[C@H](CC[C@@H]4[C@@H]3[C@H](O)C[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)O[C@@H](C)[C@@H]1O '
               'NAME: Divaricoside REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               '[C@]1([C@@H](CCC(C(C)C)CC)C)([C@]2(CC[C@@]3([C@]4(CC[C@@H](C[C@]4(CC[C@]3([C@@]2(CC1)[H])[H])[H])O)C)[H])C)[H] '
               'NAME: 24-ethylcoprostanol REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               '[H][C@@]12CC(=O)[C@](O)(c3ccc4ccncc4c3)[C@@]1(C)CC=C1C=C3[C@@H](O)[C@H](O)[C@H](C[C@]33CC[C@]21O3)N(C)C '
               'NAME: cortistatin D REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'C[C@H](CCC(=O)NCCCC(O)=O)[C@H]1CC[C@H]2[C@H]3[C@H](CC[C@]12C)[C@@]4(C)CC[C@@H](O)C[C@H]4CC3=O '
               'NAME: 7-oxo-gamma-aminoisobutyrolithocholic acid REASON: '
               'WRONGLY CLASSIFIED Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'O=C1[C@@]2(C=C3C(=O)OC[C@@]43[C@]1([C@H]5O[C@H]6CC(=O)C([C@H]7[C@]6([C@@]5(O)[C@@]4(C2)CC7)C)(C)C)C)C '
               'NAME: Emeridone D REASON: WRONGLY CLASSIFIED Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@H]23)C[C@@H]1O '
               'NAME: 2alpha-Methyl-5alpha-androstane-3alpha,17beta-diol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a steroid nucleus '
               'with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]1([H])[C@]1(C)[C@@H](O)C(=O)\\C(=C(\\C)C(=O)OC)[C@@]3([H])C1=C2C[C@@]1([H])[C@@]2(C)[C@]4([H])C[C@]4([H])[C@](O)(C\\C(C)=C\\C(=O)OC)[C@@]2([H])CC2=C(CO)C(=O)O[C@]312 '
               'NAME: shizukaol C REASON: WRONGLY CLASSIFIED Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC(=C)C(C)C)[C@@]1(C)CC[C@@H](C2)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: fecosteryl oleate REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               '[C@@]123[C@@]4([C@]5([C@@](CC1=O)(C(CN([C@H](C2)O)C)=CCO[C@]5(CC(N4C6=C3C=CC=C6)=O)[H])[H])[H])[H] '
               'NAME: 5-hydroxyvomicine REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'O=C(OC)[C@@H](NC(=O)C[C@@](O)(CC(=O)O[C@H]1[C@H](O)C([C@@H]2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4[C@@H](CC[C@@H](O)C(O)(C)C)C)C)C)(C)C)C)[C@@H](O)C5=CC=CC=C5 '
               'NAME: Pardinol C REASON: WRONGLY CLASSIFIED Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'OC12C3(C(O)(C(O)C=C1C4C(C(CC4)C(C)/C=C(/C(C(C)C)C)\\C)(CC2)C)CC(O)CC3)C '
               'NAME: '
               '(3beta,5alpha,6beta,9alpha,22E,24R)-23-Methylergosta-7,22-diene-3,5,6,9-tetrol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a steroid nucleus '
               'with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'O1[C@]23[C@@]([C@@]4([C@@](OC5=C(C4)C(OC)=C6C(=C5C)COC6=O)(C[C@H]2O)C)[H])([C@H](OC(=O)C)C[C@@]1(OC3(C)C)OC)C '
               'NAME: Austalide D REASON: WRONGLY CLASSIFIED Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@]12CCCC[C@]1(C)[C@@]1([H])CC[C@@]3(C)[C@@]([H])(C[C@]4([H])O[C@]5(CC[C@@H](C)CO5)[C@@H](C)[C@]34[H])[C@]1([H])CC2 '
               'NAME: (25R)-5alpha-spirostan REASON: WRONGLY CLASSIFIED '
               'Molecule contains a steroid nucleus with a beta-oriented (3β) '
               'hydroxyl group\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](OC(=O)\\C=C\\c3cc(OC)c(OC)c(OC)c3)[C@H](OC)[C@@H](C(=O)OC)[C@@]1([H])C[C@@]1([H])N(CCc3c1[nH]c1cc(OC)ccc31)C2 '
               'NAME: rescinnamine REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'OC1C2C(C3(C(C4(C(CC3)C(C(OC5OC(C(O)C(O)C5OC6OC(C(O)C(O)C6O)CO)COC(=O)C)CC4)(C)C)C)C1)C)(CCC2C(OC7OC(C(O)C(O)C7O)CO)(CCC=C(C)C)C)C '
               'NAME: Quinquenoside III REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCO)C)[H])[H])C '
               'NAME: 24-Nor-5beta-cholane-3alpha,12alpha,23-triol REASON: '
               'WRONGLY CLASSIFIED Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'CC(=O)OCC(=O)[C@H]1CC[C@H]2C3=CC=C4C[C@H](CC[C@]4(C)C3=CC[C@]12C)OC(C)=O '
               'NAME: 3beta,21-Dihydroxy-pregna-5,7,9(11)-trien-20-one '
               'diacetate REASON: WRONGLY CLASSIFIED Molecule contains a '
               'steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'O=C1[C@@]2([C@@]3([C@H](/C(=C(/C(=O)O)\\CCC=C(C)C)/[C@H](C3)OC(=O)C)CC[C@H]2[C@]4(CCC([C@H]([C@@H]4[C@@H]1OC(=O)C)C)=O)C)C)C '
               'NAME: 1,2-Dihydrohelvolic acid REASON: WRONGLY CLASSIFIED '
               'Molecule contains a steroid nucleus with a beta-oriented (3β) '
               'hydroxyl group\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3C[C@H]4OC[C@@]5(CCC(=O)C=C45)[C@H]3CC[C@]12C '
               'NAME: 6beta,19-Epoxypregn-4-ene-3,20-dione REASON: WRONGLY '
               'CLASSIFIED Molecule contains a steroid nucleus with a '
               'beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C3[C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC=C3[C@@]2(C)CC1)C)(C)C '
               'NAME: '
               '16alpha-hydroxy-3-oxo-24-methyllanosta-5,7,9(11),24(31)-tetraen-21-oic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a steroid '
               'nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'C1C[C@@H](C([C@@]2([C@@]1([C@]3([C@](CC2)([C@]4([C@@](C(=C3)C)(C(C(=C4O)C)=O)C)C(OC)=O)C)[H])CO)[H])(C)C)OC(C)=O '
               'NAME: andrastin B REASON: WRONGLY CLASSIFIED Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(C)[C@]([H])(CC[C@]45OC[C@@]6(CC[C@](C)(CO)C[C@@]46[H])[C@H](O)C[C@@]35C)[C@@]1(C)CC[C@H](O)C2(C)C '
               'NAME: (3beta,16alpha)-13,28-epoxyoleanane-3,16,30-triol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a steroid nucleus '
               'with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'O1[C@@]23[C@@]([C@@H]4C([C@H]5[C@]([C@@H]([C@@H](/C=C/[C@@H](C(C)C)C)C)CC5)(C)CC4)=C[C@@H]2O)(CC[C@@H]([C@H]13)O)C '
               'NAME: Gargalol A REASON: WRONGLY CLASSIFIED Molecule contains '
               'a steroid nucleus with a beta-oriented (3β) hydroxyl group\n'
               ' * SMILES: '
               'O(C1C2C(C3C(C4(C(C(CC4)C5(OC(CC5)C(O)(C)C)C)C(O)C3)C)(C1)C)(CCC(O)C2(C)C)C)C6OC(C(O)C(O)C6OC7OCC(O)C(O)C7O)COC8OC(C(O)C(O)C8O)CO '
               'NAME: Vinaginsenoside R6 REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a beta-oriented (3β) hydroxyl '
               'group\n'
               ' * SMILES: '
               'O=C(O[C@@H]1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/CO)\\C)C)CC4)(C)CC3)C)=CC2)(C)CC1)(C)C)C '
               'NAME: 3-acetyl-ganodermadiol REASON: WRONGLY CLASSIFIED '
               'Molecule contains a steroid nucleus with a beta-oriented (3β) '
               'hydroxyl group\n'
               'False negatives: SMILES: '
               'C1[C@]2([C@]3([H])COC([C@@]4([C@@]([C@]3(CC[C@@]2([C@](C1)([C@@H]([C@H]([C@@H]([C@H](C(C)C)C)O)O)C)[H])C)[H])(CC[C@@H](C4)O)C)[H])=O)[H] '
               'NAME: 7-oxoteasterone REASON: MISSED Steroid nucleus not found '
               '(no fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: '
               'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(CC)C NAME: '
               'Kobutimycin B REASON: MISSED Steroid nucleus not found (no '
               'fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: CN1[C@H]2CC3CC1C(C2O3)O NAME: LSM-1903 REASON: '
               'MISSED Steroid nucleus not found (no fused tetracyclic system '
               'with expected ring sizes)\n'
               ' * SMILES: '
               'O1[C@]2([C@H]([C@](O)(C(=O)N[C@@H]2C)C1=O)/C=C/C(O)CCCCCCC)[H] '
               'NAME: Awajanomycin REASON: MISSED Steroid nucleus not found '
               '(no fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])C=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: B-norcholesterol REASON: MISSED Steroid nucleus not '
               'found (no fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: O1C2/3C(=NCCC12)C=C\\C3=C/C NAME: Latumcidin '
               'REASON: MISSED Steroid nucleus not found (no fused tetracyclic '
               'system with expected ring sizes)\n'
               ' * SMILES: '
               '[H]C(=O)C1C2CC(O)CCC2(C)C2CCC3(C)C(CCC3([H])C(C)CCCC(C)C)C12O '
               'NAME: astropectenol A REASON: MISSED Steroid nucleus not found '
               '(no fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: '
               'O[C@@]12C3C([C@@]4(C(=CC3)C[C@@H](O)CC4)C)CC[C@@]1([C@@H](CO[C@H]2O)C(=O)C)C '
               'NAME: Insignin A REASON: MISSED Steroid nucleus not found (no '
               'fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: '
               'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(C)C NAME: '
               'Kobutimycin A REASON: MISSED Steroid nucleus not found (no '
               'fused tetracyclic system with expected ring sizes)\n'
               ' * SMILES: O1[C@]2/3C(=NCC[C@H]12)C=C\\C3=C/C NAME: '
               'Abikoviromycin REASON: MISSED Steroid nucleus not found (no '
               'fused tetracyclic system with expected ring sizes)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Steroid nucleus not found (no '
                                               'fused tetracyclic system with '
                                               'expected ring sizes)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No appropriate rings found for '
                                               'steroid nucleus'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Steroid nucleus not found (no '
                                               'fused tetracyclic system with '
                                               'expected ring sizes)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No appropriate rings found for '
                                               'steroid nucleus'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Steroid nucleus not found (no '
                                               'fused tetracyclic system with '
                                               'expected ring sizes)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Steroid nucleus not found (no '
                                               'fused tetracyclic system with '
                                               'expected ring sizes)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Steroid nucleus not found (no '
                                               'fused tetracyclic system with '
                                               'expected ring sizes)'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Steroid nucleus not found (no '
                                               'fused tetracyclic system with '
                                               'expected ring sizes)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No appropriate rings found for '
                                               'steroid nucleus'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No appropriate rings found for '
                                               'steroid nucleus'}],
    'sample_false_negatives': [   {   'smiles': 'C1[C@]2([C@]3([H])COC([C@@]4([C@@]([C@]3(CC[C@@]2([C@](C1)([C@@H]([C@H]([C@@H]([C@H](C(C)C)C)O)O)C)[H])C)[H])(CC[C@@H](C4)O)C)[H])=O)[H]',
                                      'name': '7-oxoteasterone',
                                      'reason': 'Steroid nucleus not found (no '
                                                'fused tetracyclic system with '
                                                'expected ring sizes)'},
                                  {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])[C@H](O)C[C@]1([H])[C@@]3(C)CC[C@H](O)C(C)(C)[C@]3([H])[C@H](C[C@@]21C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@](C)(CCC=C(C)C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': 'ginsenoside Rg1',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': '[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1',
                                      'name': 'dihydrodigitoxin',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': 'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(CC)C',
                                      'name': 'Kobutimycin B',
                                      'reason': 'Steroid nucleus not found (no '
                                                'fused tetracyclic system with '
                                                'expected ring sizes)'},
                                  {   'smiles': '[C@]12([C@]3([C@]([H])([C@@H](C[C@]2([H])[C@@]4([C@@]([H])([C@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)CO)C([C@H](CC4)O)(C)C)C)O)[C@]([H])(CC3)[C@](CCC=C(C)C)(O)C)C)C',
                                      'name': '(20S)-ginsenoside Rh1',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': 'CC(C)=CCC[C@](C)(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H]1CC[C@]2(C)[C@@H]1[C@H](O)C[C@@H]1[C@@]3(C)CC[C@H](O)C(C)(C)[C@@H]3CC[C@@]21C',
                                      'name': 'ginsenoside C-K',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': 'CC(C)=CCC[C@](C)(O[C@@H]1O[C@H](CO[C@@H]2O[C@@H](CO)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@H]1O)[C@H]1CC[C@]2(C)[C@@H]1[C@H](O)C[C@@H]1[C@@]3(C)CC[C@H](O)C(C)(C)[C@@H]3CC[C@@]21C',
                                      'name': 'ginsenoside Mc',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2O[C@H]2C[C@]3(C)[C@H](C[C@@H](O)[C@@H]4[C@H](CC[C@@]34C)[C@](C)(CCC=C(C)C)O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@]3(C)CC[C@H](O)C(C)(C)[C@H]23)[C@H](O)[C@H](O)[C@H]1O',
                                      'name': 'ginsenoside Re',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@@H](O)CC(=O)[C@]4(C)[C@H]3CC[C@]12C)[C@H]1CC(C)=C(CO)C(=O)O1',
                                      'name': 'viscosalactone B',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"},
                                  {   'smiles': '[H][C@]1([C@H](C)CCC[C@H](C)CO)[C@@H](O)[C@H](O)C2[C@]1(C)CCC1[C@@]3(C)CC[C@H](O)[C@H](O)C3[C@H](O)[C@@H](O)[C@@]21O',
                                      'name': '(9xi,14xi,25S)-cholestane-3beta,4beta,6beta,7alpha,8,15alpha,16beta,26-octol',
                                      'reason': 'Steroid nucleus constitutes '
                                                'less than 50% of the '
                                                "molecule's atoms"}],
    'attempt': 2,
    'reasoning': 'Below is one possible solution. In my approach I kept much '
                 'of the original logic but made two major improvements. '
                 'First, I relaxed the “mostly carbon” rule (from 80% to about '
                 '67%) so that rings bearing one or more heteroatoms (as '
                 'sometimes happens in natural steroids) are not excluded. '
                 'Second, once a fused tetracyclic (steroid‐like) component is '
                 'found, I compute the fraction of atoms in the molecule that '
                 'belong to the nucleus and require that it constitutes at '
                 'least 50% of the heavy atoms. This “nucleus fraction” filter '
                 'is intended to weed out steroid conjugates (many of which '
                 'are false positives) that have large extra‐nuclear '
                 'substituents. Finally, as before the β–hydroxy group is '
                 'detected by matching the SMARTS pattern "[C@@H](O)" and we '
                 'require that at least one such match lies within the fused '
                 'nucleus. (It is understood that there is no one “perfect” '
                 'answer; this is one example of how one might improve the '
                 'classifier.)\n'
                 '\n'
                 'Below is the complete program in a single code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 268,
    'num_false_positives': 3622,
    'num_true_negatives': 138378,
    'num_false_negatives': 32,
    'num_negatives': None,
    'precision': 0.06889460154241646,
    'recall': 0.8933333333333333,
    'f1': 0.1279236276849642,
    'accuracy': 0.9743218552354181,
    'negative_predictive_value': 0.9997688028321653}