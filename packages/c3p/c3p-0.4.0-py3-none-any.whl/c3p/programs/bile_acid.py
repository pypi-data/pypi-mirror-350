"""
Classifies: CHEBI:3098 bile acid
"""
"""
Classifies: Hydroxy-5β-cholanic acids (bile acids)
Definition: Bile acids are members of the hydroxy-5β-cholanic acid family (or their glycine/taurine conjugates). 
They typically show a fused steroid nucleus built from one 5-membered ring and three 6-membered rings (roughly 17 carbon atoms total in the core), 
a carboxyl (or conjugated amide) group on a side chain (the acid carbon is not part of the core and is 3–7 bonds away), and at least three hydroxyl groups on the scaffold.
Note: This heuristic approach may need further refinement (for example, stereochemical tests to rule out 5α-configuration).
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_bile_acid(smiles: str):
    """
    Determines if a molecule is a (hydroxy-5β-cholanic) bile acid or its glycine/taurine conjugate.

    Heuristic tests:
      1. The SMILES string must parse properly.
      2. Contains exactly one acid-like moiety – either a free carboxylic acid or a glycine/taurine-conjugated acyl group
         (using SMARTS patterns, ensuring the acid group is not part of any ring).
      3. Must have at least three hydroxyl groups ([OX2H] groups).
      4. The molecular weight should be within the bile acid range (roughly 350–700 Da).
      5. Contains a fused steroid nucleus. Typically, this means one 5-membered ring and three 6-membered rings. 
         When only considering carbon atoms from these rings, a total count of roughly 16–18 is expected.
      6. The acid (or conjugate) group must be on a side chain – that is, its nearest distance (in number of bonds) to any nucleus carbon should be 3–7.
         
    Args:
       smiles (str): SMILES string for the molecule.
       
    Returns:
       (bool, str): Tuple with True and a positive reason if the molecule is classified as a bile acid,
                    or False and a reason for rejection.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # --- Acid / Conjugate Group Checks ---
    # Free carboxylic acid group (not in a ring)
    acid_pattern = Chem.MolFromSmarts("[$([CX3](=O)[O;H,-]);!R]")
    # Glycine conjugate: acyl carbon bonded to -NCC(=O)[O;H,-]
    glycine_pattern = Chem.MolFromSmarts("[$([CX3](=O)NCC(=O)[O;H,-]);!R]")
    # Taurine conjugate: acyl carbon bonded to -NCCS(=O)(=O)[O;H,-]
    taurine_pattern = Chem.MolFromSmarts("[$([CX3](=O)NCCS(=O)(=O)[O;H,-]);!R]")
    
    acid_matches = mol.GetSubstructMatches(acid_pattern)
    glycine_matches = mol.GetSubstructMatches(glycine_pattern)
    taurine_matches = mol.GetSubstructMatches(taurine_pattern)
    total_acid_matches = len(acid_matches) + len(glycine_matches) + len(taurine_matches)
    
    if total_acid_matches == 0:
        return False, "Missing a free acid or recognized conjugated acid group essential for cholanic acids"
    if total_acid_matches > 1:
        return False, f"Found {total_acid_matches} acid-like groups; expected exactly one."
    
    # --- Hydroxyl Group Count ---
    hydroxyl_pattern = Chem.MolFromSmarts("[OX2H]")
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    if len(hydroxyl_matches) < 3:
        return False, f"Too few hydroxyl substituents (found {len(hydroxyl_matches)}; expected at least 3)"
    
    # --- Molecular Weight Check ---
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if not (350 <= mol_wt <= 700):
        return False, f"Molecular weight {mol_wt:.1f} is out of the expected bile acid range (350–700 Da)"
    
    # --- Fused Steroid Nucleus Detection ---
    # Gather ring information.
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if not rings:
        return False, "No rings found; a steroid nucleus is expected"

    # Filter rings for common steroid sizes (5- and 6-membered rings)
    rings_5 = [ring for ring in rings if len(ring) == 5]
    rings_6 = [ring for ring in rings if len(ring) == 6]
    if len(rings_5) != 1 or len(rings_6) < 3:
        return False, f"Ring system does not meet steroid criteria (found {len(rings_5)} 5-membered and {len(rings_6)} 6-membered rings)"
    
    # Construct the set of atoms in our steroid nucleus (5- and 6-membered rings)
    steroid_core_atoms = set()
    for ring in rings:
        if len(ring) in (5, 6):
            steroid_core_atoms.update(ring)
    # Count only carbon atoms from the steroid core
    core_carbons = [atom for idx, atom in enumerate(mol.GetAtoms()) if idx in steroid_core_atoms and atom.GetAtomicNum() == 6]
    if not (16 <= len(core_carbons) <= 18):
        return False, f"Fused steroid core carbon count ({len(core_carbons)}) is not in the expected range (16–18)"
    
    # --- Side Chain Check for the Acid Group ---
    # Verify that the acid (or conjugate) group is on a side chain.
    # We take the acyl carbon (the first atom in any match) and verify that:
    #   (a) It is not part of the steroid nucleus.
    #   (b) Its shortest path (in bonds) to any nucleus carbon is between 3 and 7.
    acid_on_side_chain = False
    all_matches = list(acid_matches) + list(glycine_matches) + list(taurine_matches)
    for match in all_matches:
        acid_carbon_idx = match[0]
        if acid_carbon_idx in steroid_core_atoms:
            continue  # Acid carbon is part of the core, which is not acceptable.
        min_dist = float("inf")
        for core_idx in steroid_core_atoms:
            sp = Chem.GetShortestPath(mol, acid_carbon_idx, core_idx)
            if sp:
                dist = len(sp) - 1  # number of bonds in the path
                if dist < min_dist:
                    min_dist = dist
        if 3 <= min_dist <= 7:
            acid_on_side_chain = True
            break
    if not acid_on_side_chain:
        return False, "Acid/conjugate group is not situated on a side chain (expected separation of 3–7 bonds from the steroid core)"
    
    # If all tests pass, classify the molecule as a bile acid.
    return True, "Molecule displays a fused steroid nucleus (1 five-membered and at least 3 six-membered rings with ~17 carbons), " \
                  "a single, properly placed acid/conjugate group, and sufficient hydroxyl substituents typical for bile acids"

# --- Optional Testing Block ---
if __name__ == "__main__":
    # Testing with sample SMILES (true positives from provided examples)
    examples = [
        # (2S,3S,6R)-3-Hydroxy-2-methyl-6-((...)-heptanoic acid:
        "O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CC[C@H](O)[C@H](C)C(O)=O)C)[H])[H])C",
        # 3alpha,11beta,12alpha-Trihydroxy-5beta-cholan-24-oic Acid:
        "O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)([C@H]1O)[H])[H])(CC[C@@]2([C@@H](CCC(O)=O)C)[H])[H])C"
    ]
    for smi in examples:
        res, reason = is_bile_acid(smi)
        print(res, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:3098',
                          'name': 'bile acid',
                          'definition': 'Any member of a group of '
                                        'hydroxy-5beta-cholanic acids occuring '
                                        'in bile, where they are present as '
                                        'the sodium salts of their amides with '
                                        'glycine or taurine. In mammals bile '
                                        'acids almost invariably have '
                                        '5beta-configuration.',
                          'parents': ['CHEBI:138366', 'CHEBI:24663'],
                          'xrefs': ['KEGG:C01558'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 100,
                           'log_lines_of_code': 4.605170185988092,
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
                                                 1,
                                                 1,
                                                 2,
                                                 0,
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
                                                 3,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetShortestPath',
                                                 'update',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 10,
                           'smarts_strings': [   '[$([CX3](=O)NCC(=O)[O;H,-]);!R]',
                                                 '[OX2H]',
                                                 '[$([CX3](=O)[O;H,-]);!R]',
                                                 '[$([CX3](=O)NCCS(=O)(=O)[O;H,-]);!R]'],
                           'smarts_strings_count': 4,
                           'defs': ['is_bile_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Missing a free acid or '
                                          'recognized conjugated acid group '
                                          'essential for cholanic acids"',
                                          'False, f"Found {total_acid_matches} '
                                          'acid-like groups; expected exactly '
                                          'one."',
                                          'False, f"Too few hydroxyl '
                                          'substituents (found '
                                          '{len(hydroxyl_matches)}; expected '
                                          'at least 3)"',
                                          'False, f"Molecular weight '
                                          '{mol_wt:.1f} is out of the expected '
                                          'bile acid range (350–700 Da)"',
                                          'False, "No rings found; a steroid '
                                          'nucleus is expected"',
                                          'False, f"Ring system does not meet '
                                          'steroid criteria (found '
                                          '{len(rings_5)} 5-membered and '
                                          '{len(rings_6)} 6-membered rings)"',
                                          'False, f"Fused steroid core carbon '
                                          'count ({len(core_carbons)}) is not '
                                          'in the expected range (16–18)"',
                                          'False, "Acid/conjugate group is not '
                                          'situated on a side chain (expected '
                                          'separation of 3–7 bonds from the '
                                          'steroid core)"',
                                          'True, "Molecule displays a fused '
                                          'steroid nucleus (1 five-membered '
                                          'and at least 3 six-membered rings '
                                          'with ~17 carbons), " \\'],
                           'returns_count': 10,
                           'complexity': 6.121034037197619},
    'message': '\n'
               'Error: Error executing '
               "is_bile_acid('O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CC[C@H](O)[C@H](C)C(O)=O)C)[H])[H])C'):\n"
               " 'RingInfo' object has no attribute 'IsInitialized'\n"
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
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
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Too few hydroxyl substituents '
                                               '(found 1; expected at least '
                                               '3)'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Ring system does not meet '
                                               'steroid criteria (found 0 '
                                               '5-membered and 3 6-membered '
                                               'rings)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Missing a free acid or '
                                               'recognized conjugated acid '
                                               'group essential for cholanic '
                                               'acids'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCCC(CO)C)C)[H])[H])C',
                                      'name': '5alpha-Cholestane-3alpha,7alpha,12alpha,26-tetrol',
                                      'reason': 'Missing a free acid or '
                                                'recognized conjugated acid '
                                                'group essential for cholanic '
                                                'acids'},
                                  {   'smiles': 'O[C@H]([C@H]([C@@]1([C@@]2(C([C@]3([C@@]([C@@]4([C@@](CC3)(CC(=O)CC4)[H])C)(CC2)[H])[H])CC1)C)[H])C)C[C@H](C(C)C)C',
                                      'name': '(5S,8R,9S,10S,13S,17R)-17-[(2S,3S,5R)-3-Hydroxy-5,6-dimethylheptan-2-yl]-10,13-dimethyl-1,2,4,5,6,7,8,9,11,12,14,15,16,17-tetradecahydrocyclopenta[a]phenanthren-3-one',
                                      'reason': 'Missing a free acid or '
                                                'recognized conjugated acid '
                                                'group essential for cholanic '
                                                'acids'},
                                  {   'smiles': 'O=C1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCC(O)=O)C)[H])[H])C',
                                      'name': '3beta-Hydroxy-12-oxo-5beta-cholan-24-oic '
                                              'Acid',
                                      'reason': 'Too few hydroxyl substituents '
                                                '(found 2; expected at least '
                                                '3)'},
                                  {   'smiles': 'O[C@H]1C[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H](CC/C=C(\\C)/C(O)=O)C)[H])(CC3)C)[H])(CC2)[H])[H])(CC1)C)[H]',
                                      'name': '3alpha-Hydroxy-5beta-cholest-24-en-26-oic '
                                              'acid',
                                      'reason': 'Too few hydroxyl substituents '
                                                '(found 2; expected at least '
                                                '3)'},
                                  {   'smiles': 'O=C1C2C(C3C(C4C(C(CC4)C(C(O)C(O)C(C(C)(C)C)=C)C)(CC3)C)C1)(CC(O)C(O)C2)C',
                                      'name': '(2alpha,3alpha,5alpha,22R,23R)-2,3,22,23-Tetrahydroxy-25-methylergost-24(28)en-6-one',
                                      'reason': 'Missing a free acid or '
                                                'recognized conjugated acid '
                                                'group essential for cholanic '
                                                'acids'},
                                  {   'smiles': 'O=C(O)[C@@H]([C@@H]1[C@@]2([C@@](C=3C([C@@]4(C([C@](OC(=O)C)([C@@H](O)CC4)C)CC3)C)=CC2)(C)[C@H](C1)OC(=O)C)C)CCC(=C)C(C)C',
                                      'name': '15alpha-Acetyl-dehydrosulphurenic '
                                              'acid',
                                      'reason': 'Too few hydroxyl substituents '
                                                '(found 2; expected at least '
                                                '3)'},
                                  {   'smiles': 'O=C1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)(C1=O)[H])[H])(CC[C@@]2([C@@H](CCC(O)=O)C)[H])[H])C',
                                      'name': '3alpha-Hydroxy-11,12-dioxo-5beta-cholan-24-oic '
                                              'Acid',
                                      'reason': 'Too few hydroxyl substituents '
                                                '(found 2; expected at least '
                                                '3)'},
                                  {   'smiles': 'O[C@H]1CC2[C@@]([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H](CCC(O)=O)C)[H])(CC3)C)[H])(CC2)[H])[H])(CC1)C',
                                      'name': '3a-Hydroxycholanoic acid',
                                      'reason': 'Too few hydroxyl substituents '
                                                '(found 2; expected at least '
                                                '3)'},
                                  {   'smiles': 'O=C1C[C@@]2([C@@](C=3C([C@]4([C@@]([C@](CC4)([C@@H](CCC(O)=O)C)[H])(CC3)C)[H])=CC2)(CC1)C)[H]',
                                      'name': '3-Oxo-5beta-chola-7,9(11)-dien-24-oic '
                                              'Acid',
                                      'reason': 'Too few hydroxyl substituents '
                                                '(found 1; expected at least '
                                                '3)'},
                                  {   'smiles': 'O=C(O[C@@H]1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/CO)\\C)C)C[C@@H]4O)(C)CC3)C)[C@@H](C2)O)(C)CC1)(C)C)C',
                                      'name': '(24E)-3beta-acetoxy-7alpha,15alpha,26-trihydroxylanosta-8,24-diene',
                                      'reason': 'Missing a free acid or '
                                                'recognized conjugated acid '
                                                'group essential for cholanic '
                                                'acids'}],
    'attempt': 5,
    'reasoning': 'Below is one way to fix our approach. In our previous '
                 'attempt we called the method IsInitialized() on the RingInfo '
                 'object. However, in current versions of RDKit the RingInfo '
                 'object does not support IsInitialized(). We can instead '
                 'check whether any rings were detected (i.e. whether '
                 'AtomRings() returns any rings) to determine if ring '
                 'information is available. In addition, we may slightly '
                 'refine the SMARTS queries and comments. The following Python '
                 'code is a single code block implementing our heuristic '
                 'classification for a hydroxy-5β-cholanic bile acid (or its '
                 'glycine/taurine conjugates):\n'
                 '\n'
                 '------------------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 109,
    'num_false_positives': 296,
    'num_true_negatives': 141669,
    'num_false_negatives': 226,
    'num_negatives': None,
    'precision': 0.2691358024691358,
    'recall': 0.3253731343283582,
    'f1': 0.2945945945945946,
    'accuracy': 0.9963316936050597,
    'negative_predictive_value': 0.9984072729835441}