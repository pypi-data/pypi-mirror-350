"""
Classifies: CHEBI:36498 galactosylceramide
"""
"""
Classifies: Galactosylceramide – any cerebroside in which the monosaccharide head group is galactose.
A galactosylceramide is a glycosphingolipid consisting of a ceramide (sphingoid base plus fatty acid,
attached via an amide bond) linked by an O‐glycosidic bond to a galactose sugar.
  
The algorithm applies several filters:
  1. Molecule size is within a typical range (30–150 heavy atoms).
  2. Exactly one amide bond (the ceramide motif).
  3. Presence of at least one long aliphatic chain (8+ consecutive carbons).
  4. Existence of exactly one candidate six‐membered sugar (pyranose) ring:
       a. The ring must have exactly 6 atoms,
       b. exactly one ring oxygen,
       c. and at least 3 exocyclic oxygen substituents.
  5. The candidate sugar ring must match the galactose fingerprint (either alpha or beta).
  
Note: In this version the candidate ring is first extracted from the molecule.
Then, instead of expecting the SMARTS match to correspond exactly to the ring,
we require that the candidate ring’s indices are contained in (a subset of) the SMARTS match.
This avoids missing positive cases when the SMARTS query returns extra atoms (for example, the linking O–CH2 group). 
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_galactosylceramide(smiles: str):
    """
    Determines if a molecule is a galactosylceramide based on its SMILES string.
    The decision is based on a sequence of filters on size, presence of a single ceramide amide bond,
    a long alkyl chain, exactly one candidate pyranose ring with the appropriate exocyclic oxygens,
    and confirmation that the candidate sugar ring displays a fingerprint akin to galactose.
    
    Args:
      smiles (str): SMILES string of the molecule.
        
    Returns:
      bool: True if the molecule is classified as a galactosylceramide, False otherwise.
      str: Explanation for the classification decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # --- Filter 1. Molecule size (heavy atom count) ---
    heavy_atoms = mol.GetNumHeavyAtoms()
    if heavy_atoms < 30:
        return False, "Molecule appears too small to be a galactosylceramide."
    if heavy_atoms > 150:
        return False, "Molecule appears too large to be a typical galactosylceramide."

    # --- Filter 2. Exactly one amide bond (C(=O)N) for the ceramide motif ---
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if len(amide_matches) != 1:
        return False, f"Expected exactly 1 amide bond, found {len(amide_matches)} (not typical of a ceramide)."
    
    # --- Filter 3. At least one long aliphatic chain (≥8 consecutive carbons) ---
    chain_pattern = Chem.MolFromSmarts("CCCCCCCC")
    if not mol.HasSubstructMatch(chain_pattern):
        return False, "Missing a long alkyl chain (expected from a fatty acyl or sphingoid base)."
    
    # --- Filter 4. Locate candidate sugar rings ---
    # Candidate sugar rings are 6-membered rings with exactly one ring oxygen and at least 3 exocyclic oxygen substituents.
    ring_info = mol.GetRingInfo()
    candidate_ring_indices = []  # each candidate is a tuple of atom indices (of the ring)
    for ring in ring_info.AtomRings():
        if len(ring) != 6:
            continue  # not a pyranose ring
        # Count number of ring oxygens.
        n_ring_oxygens = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8)
        if n_ring_oxygens != 1:
            continue
        # Count exocyclic oxygen substituents from atoms in the ring.
        ext_oxygen_count = 0
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                # Skip atoms that are in the ring.
                if nbr.GetIdx() in ring:
                    continue
                if nbr.GetAtomicNum() == 8:
                    ext_oxygen_count += 1
        if ext_oxygen_count >= 3:
            candidate_ring_indices.append(ring)
    
    if len(candidate_ring_indices) == 0:
        return False, "No candidate pyranose sugar ring with sufficient exocyclic oxygens detected."
    if len(candidate_ring_indices) > 1:
        return False, f"Found {len(candidate_ring_indices)} candidate sugar rings; expected exactly 1 for a galactosylceramide."
    
    # --- Filter 5. Verify that the candidate sugar ring displays galactose stereochemistry ---
    # We define two SMARTS queries (one for alpha and one for beta galactopyranose)
    # These SMARTS include the linking oxygen (the exocyclic O) as found in many glycosidic bonds.
    alpha_gal_smarts = "OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O"
    beta_gal_smarts  = "OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O"
    alpha_gal = Chem.MolFromSmarts(alpha_gal_smarts)
    beta_gal  = Chem.MolFromSmarts(beta_gal_smarts)
    
    # Instead of expecting an exact 1-to-1 match of atom indices,
    # we now accept a match if the candidate ring indices are a subset of the SMARTS match.
    candidate_ring_set = set(candidate_ring_indices[0])
    found_gal = False
    for query in (alpha_gal, beta_gal):
        if query is None:
            continue
        # Get substructure matches with chirality considerations.
        matches = mol.GetSubstructMatches(query, useChirality=True)
        for match in matches:
            # If the candidate ring (the 6 ring atoms) is contained in the SMARTS match, accept it.
            if candidate_ring_set.issubset(set(match)):
                found_gal = True
                break
        if found_gal:
            break
    if not found_gal:
        return False, "Candidate sugar ring does not display the expected galactose stereochemistry."
    
    return True, ("Contains one ceramide amide bond, exactly one candidate pyranose sugar ring with galactose stereochemical fingerprint, "
                  "and a long alkyl chain – consistent with a galactosylceramide.")

# Example usage:
# Uncomment one or more lines below to test one of the provided SMILES examples.
# example_smiles = "C(=C/CCCCCCCCCCCCC)\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCC)=O)CO[C@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O)OS(O)(=O)=O)O"
# result, reason = is_galactosylceramide(example_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36498',
                          'name': 'galactosylceramide',
                          'definition': 'Any of the cerebrosides in which the '
                                        'monosaccharide head group is '
                                        'galactose.',
                          'parents': [   'CHEBI:23079',
                                         'CHEBI:5254',
                                         'CHEBI:62941'],
                          'xrefs': [   'KEGG:C02686',
                                       'KEGG:G11121',
                                       'PMID:16758576',
                                       'PMID:17855742',
                                       'PMID:2088646',
                                       'PMID:23065187',
                                       'PMID:23446636',
                                       'PMID:23650721',
                                       'PMID:25947378',
                                       'PMID:26058499',
                                       'PMID:26907993',
                                       'PMID:27786470'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 84,
                           'log_lines_of_code': 4.430816798843313,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 2,
                                                 3,
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
                                                 0],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetNumHeavyAtoms',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'issubset',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 13,
                           'smarts_strings': [   'beta_gal_smarts',
                                                 'CCCCCCCC',
                                                 'C(=O)N',
                                                 'alpha_gal_smarts'],
                           'smarts_strings_count': 4,
                           'defs': ['is_galactosylceramide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "Molecule appears too small '
                                          'to be a galactosylceramide."',
                                          'False, "Molecule appears too large '
                                          'to be a typical '
                                          'galactosylceramide."',
                                          'False, f"Expected exactly 1 amide '
                                          'bond, found {len(amide_matches)} '
                                          '(not typical of a ceramide)."',
                                          'False, "Missing a long alkyl chain '
                                          '(expected from a fatty acyl or '
                                          'sphingoid base)."',
                                          'False, "No candidate pyranose sugar '
                                          'ring with sufficient exocyclic '
                                          'oxygens detected."',
                                          'False, f"Found '
                                          '{len(candidate_ring_indices)} '
                                          'candidate sugar rings; expected '
                                          'exactly 1 for a '
                                          'galactosylceramide."',
                                          'False, "Candidate sugar ring does '
                                          'not display the expected galactose '
                                          'stereochemistry."',
                                          'True, ("Contains one ceramide amide '
                                          'bond, exactly one candidate '
                                          'pyranose sugar ring with galactose '
                                          'stereochemical fingerprint, "'],
                           'returns_count': 9,
                           'complexity': 6.486163359768662},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C(=C/CCCCCCCCCCCCC)\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCC)=O)CO[C@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O)OS(O)(=O)=O)O '
               'NAME: 1-(3-O-sulfo-beta-D-galactosyl)-N-stearoylsphingosine '
               'REASON: MISSED Candidate sugar ring does not display the '
               'expected galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC[C@@H](O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               '1-(3-O-sulfo-beta-D-galactosyl)-N-[(2R)-2-hydroxystearoyl]sphingosine '
               'REASON: MISSED Candidate sugar ring does not display the '
               'expected galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@H]1O[C@H](COS(O)(=O)=O)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)NC(=O)CCCCCCCCCCC '
               'NAME: '
               '1-(3,6-di-O-sulfo-beta-D-galactosyl)-N-lauroylsphingosine '
               'REASON: MISSED Candidate sugar ring does not display the '
               'expected galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: beta-D-galactosyl-N-(tricosanoyl)sphingosine REASON: '
               'MISSED Candidate sugar ring does not display the expected '
               'galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: 1-(beta-D-galactosyl)-N-behenoylsphingosine REASON: '
               'MISSED Candidate sugar ring does not display the expected '
               'galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: beta-D-galactosyl-N-(tetracosanoyl)sphingosine REASON: '
               'MISSED Candidate sugar ring does not display the expected '
               'galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC[C@@H](O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               '1-(3-O-sulfo-beta-D-galactosyl)-N-[(2R)-2-hydroxybehenoyl]sphingosine '
               'REASON: MISSED Candidate sugar ring does not display the '
               'expected galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-tricosanoyl-D-galactosylsphingosine REASON: MISSED '
               'Candidate sugar ring does not display the expected galactose '
               'stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC[C@@H](O)[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CC\\C=C/CCCCC1CC1CCCCCCCCCC '
               'NAME: '
               'alpha-D-galactosyl-N-[(4Z)-9-(2-decylcyclopropyl)non-4-enoyl]phytosphingosine '
               'REASON: MISSED Candidate sugar ring does not display the '
               'expected galactose stereochemistry.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC '
               'NAME: 1-O-(alpha-D-galactosyl)-N-hexacosanoylphytosphingosine '
               'REASON: MISSED Candidate sugar ring does not display the '
               'expected galactose stereochemistry.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No candidate pyranose sugar '
                                               'ring with sufficient exocyclic '
                                               'oxygens detected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule appears too small to '
                                               'be a galactosylceramide.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Expected exactly 1 amide bond, '
                                               'found 3 (not typical of a '
                                               'ceramide).'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Molecule appears too small to '
                                               'be a galactosylceramide.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Expected exactly 1 amide bond, '
                                               'found 0 (not typical of a '
                                               'ceramide).'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Expected exactly 1 amide bond, '
                                               'found 0 (not typical of a '
                                               'ceramide).'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Molecule appears too small to '
                                               'be a galactosylceramide.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Expected exactly 1 amide bond, '
                                               'found 3 (not typical of a '
                                               'ceramide).'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Molecule appears too small to '
                                               'be a galactosylceramide.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Expected exactly 1 amide bond, '
                                               'found 0 (not typical of a '
                                               'ceramide).'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@H]1O[C@H](COS(O)(=O)=O)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)NC(=O)CCCCCCCCCCC',
                                      'name': '1-(3,6-di-O-sulfo-beta-D-galactosyl)-N-lauroylsphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': 'N-tricosanoyl-D-galactosylsphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': 'CCCCCCCCCCCCCC[C@@H](O)[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CC\\C=C/CCCCC1CC1CCCCCCCCCC',
                                      'name': 'alpha-D-galactosyl-N-[(4Z)-9-(2-decylcyclopropyl)non-4-enoyl]phytosphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC',
                                      'name': '1-O-(alpha-D-galactosyl)-N-hexacosanoylphytosphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': 'N-(2-hydroxylignoceroyl)-D-galactosylsphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': '[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)OC[C@@H]([C@@H]([C@@H](CCCCC=2C=CC=CC2)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O',
                                      'name': 'N-[(2S,3S,4R)-1-(alpha-D-galactosyloxy)-3,4-dihydroxy-8-phenyloctan-2-yl]hexacosanamide',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': 'N-(2-hydroxytricosanoyl)-D-galactosylsphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': 'N-stearoyl-D-galactosylsphingosine',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': '[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)OC[C@@H]([C@@H]([C@@H](CCCCCCCC=2C=CC=CC2)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O',
                                      'name': 'N-[(2S,3S,4R)-1-(alpha-D-galactosyloxy)-3,4-dihydroxy-11-phenylundecan-2-yl]hexacosanamide',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'},
                                  {   'smiles': '[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCC=2C=CC=CC2)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O',
                                      'name': 'N-[(2S,3S,4R)-1-(alpha-D-galactosyloxy)-3,4-dihydroxy-13-phenyltridecan-2-yl]hexacosanamide',
                                      'reason': 'Candidate sugar ring does not '
                                                'display the expected '
                                                'galactose stereochemistry.'}],
    'attempt': 5,
    'reasoning': 'Below is one possible improved solution. In our reasoning we '
                 'noticed that the previous approach insisted on an exact '
                 'match between the candidate ring atom indices and the atoms '
                 'returned from the galactose SMARTS query. In many real '
                 'examples the SMARTS query returns extra atoms from the '
                 'linking group, so the exact‐equality check failed even when '
                 'the candidate ring really was galactose. In this revision we '
                 'relax that check by accepting the match if the candidate '
                 'ring indices are a subset of the atoms returned in the '
                 'SMARTS match. (We still use chirality in the SMARTS search.) '
                 'Hopefully this “subset” condition fixes the issue while '
                 'still ensuring that the ring displays the galactose '
                 'fingerprint. \n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 23,
    'num_true_negatives': 142240,
    'num_false_negatives': 14,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 0.6216216216216216,
    'f1': 0.5542168674698795,
    'accuracy': 0.9997399859451862,
    'negative_predictive_value': 0.9999015844897156}