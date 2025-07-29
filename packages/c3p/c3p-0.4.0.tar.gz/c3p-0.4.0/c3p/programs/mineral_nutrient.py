"""
Classifies: CHEBI:167164 mineral nutrient
"""
from rdkit import Chem

def is_mineral_nutrient(smiles: str):
    """
    Determines if a molecule is a mineral nutrient based on its SMILES string.
    A mineral nutrient is an inorganic compound essential for the human body,
    typically consisting of an inorganic anion and a metal cation.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool, str: True and reason if classified as a mineral nutrient;
                   False and reason otherwise
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define valid SMARTS patterns for metal cations
    metal_cations_patterns = [
        Chem.MolFromSmarts("[K+]"),
        Chem.MolFromSmarts("[Na+]"),
        Chem.MolFromSmarts("[Ca+2]"),
        Chem.MolFromSmarts("[Mg+2]"),
        Chem.MolFromSmarts("[Fe+3]"),
        Chem.MolFromSmarts("[Zn+2]"),
        Chem.MolFromSmarts("[Al+3]"),
        Chem.MolFromSmarts("[Ba+2]"),
        Chem.MolFromSmarts("[Cs+]"),
        Chem.MolFromSmarts("[La+3]"),
        Chem.MolFromSmarts("[Sb+5]")
    ]
    
    # Define valid SMARTS patterns for common anionic groups
    anions_patterns = [
        Chem.MolFromSmarts("[Cl-]"),
        Chem.MolFromSmarts("[F-]"),
        Chem.MolFromSmarts("[O-]S(=O)(=O)[O-]"),  # sulfate
        Chem.MolFromSmarts("[O-]P(=O)([O-])[O-]"),  # phosphate
        Chem.MolFromSmarts("[O-]C(=O)[O-]"),  # carbonate
        Chem.MolFromSmarts("[O-]N(=O)[O-]"),  # nitrate
        Chem.MolFromSmarts("[Si]([O-])([O-])([O-])[O-]")  # silicate
    ]
    
    # Check for presence of at least one metal cation
    cation_found = any(mol.HasSubstructMatch(pattern) for pattern in metal_cations_patterns)
    if not cation_found:
        return False, "No essential metal cations found"
    
    # Check for presence of at least one anion or inorganic group
    anion_found = any(mol.HasSubstructMatch(pattern) for pattern in anions_patterns)
    if not anion_found:
        return False, "No recognizable anionic groups found"
    
    # If both components are present, classify as a potential mineral nutrient
    return True, "Contains essential metal cation and anionic counterpart typical of mineral nutrients"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167164',
                          'name': 'mineral nutrient',
                          'definition': 'A mineral that is an inorganic '
                                        'nutrient which must be ingested and '
                                        'absorbed in adequate amounts to '
                                        'satisfy a wide range of essential '
                                        'metabolic and/or structural functions '
                                        'in the human body.',
                          'parents': ['CHEBI:46662'],
                          'xrefs': ['Wikipedia:Mineral_(nutrient)'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Error: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)\n'
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
    'sample_true_negatives': [   {   'smiles': 'O=C1O[C@@H](C(=O)[C@@]2([C@]1(C(=C)C[C@H]3[C@]4([C@@H](C(C(=O)CC4)(C)C)[C@H](C[C@]23C)O)C)C)C(=O)OC)C',
                                     'name': 'Terreustoxin L',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': '[H][C@]12CCC[C@H](C)[C@@]1(C)C[C@@H](CC2)C(C)C',
                                     'name': 'eremophilane',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'N.C[C@]12CC[C@@](C)(C[C@H]1C1=CC(=O)[C@@H]3[C@@]4(C)CC[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O)C(O)=O)C(C)(C)[C@@H]4CC[C@@]3(C)[C@]1(C)CC2)C(O)=O',
                                     'name': 'Monoammonium glycyrrhizinate',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC2=CC=CC=C2)CCC(=O)N',
                                     'name': 'Phe-Gln-His',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'S(=O)(=O)(O[C@@H](C(=O)N[C@@H]1C(=O)N[C@H](C(=O)N[C@@H]2C(=O)N([C@@H]([C@H](CC)C)C(N([C@H](C(N[C@H](C(O[C@@H]1C)=O)[C@H](CC)C)=O)CC3=CC=CC=C3)C)=O)[C@H](OC)CC2)CCCN=C(N)N)COS(=O)(=O)O)O',
                                     'name': 'Micropeptin MZ1019',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'CN(C)CC(=O)N[C@H]1CC[C@@H](O[C@H]1CO)CCN2C=C(N=N2)C3=CC(=CC=C3)OC',
                                     'name': '2-(dimethylamino)-N-[(2R,3S,6R)-2-(hydroxymethyl)-6-[2-[4-(3-methoxyphenyl)-1-triazolyl]ethyl]-3-oxanyl]acetamide',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'CC1=CC=C(C=C1)CS(=O)(=O)C2=NC=C(C(=N2)C(=O)NC3=NN=C(S3)C(C)C)Cl',
                                     'name': '5-chloro-2-[(4-methylphenyl)methylsulfonyl]-N-(5-propan-2-yl-1,3,4-thiadiazol-2-yl)-4-pyrimidinecarboxamide',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCC)([O-])=O',
                                     'name': 'PC(15:1(9Z)/15:1(9Z))',
                                     'reason': 'No essential metal cations '
                                               'found'},
                                 {   'smiles': 'OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)C)[C@H](CC)C',
                                     'name': 'Asp-Ala-Ile',
                                     'reason': 'No essential metal cations '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': '[Mg++].CCC([O-])=O.CCC([O-])=O',
                                      'name': 'magnesium dipropionate',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': '[Mg++].CCCCCCCCCCCCCCCCCC([O-])=O.CCCCCCCCCCCCCCCCCC([O-])=O',
                                      'name': 'magnesium distearate',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': '[Na+].[Na+].OP([O-])([O-])=O',
                                      'name': 'disodium hydrogenphosphate',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': '[Ca++].[H]OP([O-])([O-])=O',
                                      'name': 'calcium hydrogenphosphate',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': '[Cs+].[H]C([O-])=O',
                                      'name': 'caesium formate',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': '[Pd-2](Cl)(Cl)(Cl)(Cl)(Cl)Cl.[K+].[K+]',
                                      'name': 'Potassium '
                                              'hexachloropalladate(IV)',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': 'Cl[O-].[Ca+2].Cl[O-]',
                                      'name': 'Calcium hypochlorite',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': '[Ba++].CC([O-])=O.CC([O-])=O',
                                      'name': 'barium acetate',
                                      'reason': 'No recognizable anionic '
                                                'groups found'},
                                  {   'smiles': 'Cl[La](Cl)Cl',
                                      'name': 'lanthanum trichloride',
                                      'reason': 'No essential metal cations '
                                                'found'},
                                  {   'smiles': 'O[Ca]',
                                      'name': 'calcium monohydroxide',
                                      'reason': 'No essential metal cations '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'The error indicates that there was an issue with the SMARTS '
                 'patterns used to identify metal cations and anions. '
                 'Specifically, the patterns are strings rather than valid '
                 'SMARTS expressions, leading to `NoneType` when trying to '
                 'create a pattern with `Chem.MolFromSmarts`. Therefore, the '
                 'attempt to match substructures failed.\n'
                 '\n'
                 'To address this, properly define SMARTS patterns and ensure '
                 'a correct logical structure for identifying common features '
                 'of mineral nutrients. Mineral nutrients typically consist of '
                 'one or more metal cations paired with anions such as '
                 'chlorides, sulfates, nitrates, carbonates, and phosphates.\n'
                 '\n'
                 '### Steps to correct the implementation:\n'
                 '\n'
                 '1. **Ensure Valid SMARTS Patterns:**\n'
                 '   - Each ion or ion group should be a valid SMARTS pattern '
                 'string.\n'
                 '   - Use separate patterns for each component and parse them '
                 'individually.\n'
                 '\n'
                 '2. **Modify Matching Logic:**\n'
                 '   - Check if the molecule contains any of the recognized '
                 'metal cations.\n'
                 '   - Check if the molecule contains any of the recognized '
                 'anionic groups.\n'
                 '\n'
                 '3. **Review Essential Cation and Anion Types:**\n'
                 '   - Consider all provided examples to refine which ions are '
                 'central to the classification.\n'
                 '\n'
                 'Below is the adjusted code to better classify mineral '
                 'nutrients.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 20,
    'num_false_positives': 38,
    'num_true_negatives': 142230,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.3448275862068966,
    'recall': 0.625,
    'f1': 0.4444444444444445,
    'accuracy': 0.999648629655657,
    'negative_predictive_value': 0.999915636731767}