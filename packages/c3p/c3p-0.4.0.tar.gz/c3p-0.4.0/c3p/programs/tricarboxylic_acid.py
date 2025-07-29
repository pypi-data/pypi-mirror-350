"""
Classifies: CHEBI:27093 tricarboxylic acid
"""
"""
Classifies: Tricarboxylic Acid 
Definition: An oxoacid containing three carboxy groups.
This version uses several heuristics:
  - The molecule must be neutral and contain only allowed (organic) elements.
  - The molecule must contain exactly three unique carboxyl groups (which may be protonated or deprotonated).
  - At most one amide bond is allowed.
  - The carboxyl–to–carbon ratio (number of carboxyl carbons divided by total carbon count) must be at least 0.18.
  - The molecular weight must be below 600 Da.
  - Molecules with any aromatic rings are rejected to ensure that only “simple” acids are accepted.
Note: This classification is heuristic.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_tricarboxylic_acid(smiles: str):
    """
    Determines whether a molecule is a tricarboxylic acid based on its SMILES string.
    
    A tricarboxylic acid is defined here as a neutral organic oxoacid that contains exactly three unique carboxyl groups.
    We further require that the molecule is “simple” by:
      - Allowing at most one amide bond,
      - Rejecting any molecule with aromatic rings,
      - Requiring that the carboxyl groups make up a significant fraction of the carbon skeleton (ratio >= 0.18),
      - And that the molecular weight is below 600 Da.
    
    Args:
        smiles (str): SMILES string for the molecule.
    
    Returns:
        bool: True if the molecule is classified as a tricarboxylic acid; False otherwise.
        str: Explanation for the classification decision.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check allowed elements (organic: H, C, N, O, S)
    allowed_atomic_nums = {1, 6, 7, 8, 16}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Contains non-organic atom: {atom.GetSymbol()} (atomic num: {atom.GetAtomicNum()})"
    
    # Check that the molecule is neutral (formal charge equals zero)
    if Chem.GetFormalCharge(mol) != 0:
        return False, "Molecule has nonzero formal charge; expected a neutral tricarboxylic acid"
    
    # Reject if any aromatic rings are present.
    # We check for any aromatic atom – if any are found, the molecule is considered too complex.
    if any(atom.GetIsAromatic() for atom in mol.GetAtoms()):
        return False, "Molecule contains aromatic rings; not a simple tricarboxylic acid"
    
    # Count amide bonds – allow at most one.
    # Using a SMARTS pattern for a simple amide: C(=O)N
    amide_pattern = Chem.MolFromSmarts("[C;X3](=O)[N;X3]")
    if amide_pattern is not None:
        amide_matches = mol.GetSubstructMatches(amide_pattern)
        if len(amide_matches) > 1:
            return False, f"Contains {len(amide_matches)} amide bonds; too many for a simple tricarboxylic acid"
    
    # Define SMARTS for carboxyl groups.
    # One for protonated acid: -C(=O)[OH]
    acid_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H]")
    # One for deprotonated carboxylate: -C(=O)[O-]
    carboxylate_pattern = Chem.MolFromSmarts("[CX3](=O)[O-]")
    if acid_pattern is None or carboxylate_pattern is None:
        return False, "Error creating SMARTS patterns for carboxyl groups"
    
    # Get all matches for the two carboxyl patterns.
    acid_matches = mol.GetSubstructMatches(acid_pattern)
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    
    # Count unique carboxyl-group carbons (take first atom index from each match).
    carboxyl_carbon_indices = set()
    for match in acid_matches:
        carboxyl_carbon_indices.add(match[0])
    for match in carboxylate_matches:
        carboxyl_carbon_indices.add(match[0])
    
    n_carboxyl = len(carboxyl_carbon_indices)
    if n_carboxyl != 3:
        return False, f"Found {n_carboxyl} carboxyl group(s); expected exactly 3"
    
    # Count total carbon atoms.
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if total_carbons == 0:
        return False, "No carbon atoms found"
    
    # Compute the carboxyl-to-carbon ratio.
    carboxyl_ratio = n_carboxyl / total_carbons
    # Lowered threshold (0.18) to allow borderline true positives.
    if carboxyl_ratio < 0.18:
        return False, f"Low carboxyl-to-carbon ratio ({carboxyl_ratio:.2f}); expected at least 0.18"
    
    # Calculate molecular weight.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 600:
        return False, f"Molecular weight too high ({mol_wt:.1f} Da); expected less than 600 Da for a tricarboxylic acid"
    
    return True, ("Contains exactly three carboxyl groups, has acceptable amide count, no aromatic rings, "
                  "sufficient carboxyl/carbon ratio, and is neutral and within weight range – consistent with a tricarboxylic acid")

# Example usage (for local testing):
if __name__ == "__main__":
    test_smiles = [
        # True examples:
        "C[C@H](\\C=C\\C=C(\\C)[C@H]1CN[C@@H]([C@H]1CC(O)=O)C(O)=O)C(O)=O",  # domoic acid
        "O[C@@H]([C@H](CC(O)=O)C(O)=O)C(O)=O",  # D-erythro-isocitric acid
        "OCCC(NCCC(NCCC(O)C(O)=O)C(O)=O)C(O)=O",  # avenic acid A
        "O=C(O)[C@@H](NC[C@@H](C(O)=O)N)CCC(=O)O",  # N-[(2S)-2-amino-2-carboxyethyl]-L-glutamic acid
        "C(C(C(C)(C(=O)O)O)C(=O)O)C(O)=O",  # 3-hydroxybutane-1,2,3-tricarboxylic acid
        # False examples:
        "O(CCCCCCC(C(C(O)=O)=C)C(O)=O)C(=O)C(O)=O",  # 2-Methylidene-3-(6-oxalooxyhexyl)butanedioic acid (should be rejected)
        "O[C@@H]1C[C@@H](C([O-])=O)\\[N+](C1)=C/C=C1C[C@H](NC(=C\\1)C(O)=O)C(O)=O",  # Portulacaxanthin I (should be rejected due to aromaticity/charge)
        "N[C@@H](CCC(O)=O)C(=O)N[C@@H](CC(O)=O)C(O)=O",  # Glu-Asp (multiple amide bonds)
        "OC(CC(=O)NCCC[C@@H](N)C(O)=O)(CC(O)=O)C(O)=O",  # delta-Citryl-d-ornithine (multiple amide bonds)
        "OC(=O)CCP(CCC(O)=O)CCC(O)=O",  # TCEP (contains a P atom)
    ]
    for s in test_smiles:
        result, reason = is_tricarboxylic_acid(s)
        print(f"SMILES: {s}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27093',
                          'name': 'tricarboxylic acid',
                          'definition': 'An oxoacid containing three carboxy '
                                        'groups.',
                          'parents': ['CHEBI:33575'],
                          'xrefs': ['Wikipedia:Tricarboxylic_acid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 88,
                           'log_lines_of_code': 4.477336814478207,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
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
                                                 2,
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
                                                 0,
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
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetSymbol',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'add',
                                                 'GetFormalCharge'],
                           'methods_called_count': 10,
                           'smarts_strings': [   '[CX3](=O)[O-]',
                                                 '[CX3](=O)[OX2H]',
                                                 '[C;X3](=O)[N;X3]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_tricarboxylic_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Contains non-organic atom: '
                                          '{atom.GetSymbol()} (atomic num: '
                                          '{atom.GetAtomicNum()})"',
                                          'False, "Molecule has nonzero formal '
                                          'charge; expected a neutral '
                                          'tricarboxylic acid"',
                                          'False, "Molecule contains aromatic '
                                          'rings; not a simple tricarboxylic '
                                          'acid"',
                                          'False, f"Contains '
                                          '{len(amide_matches)} amide bonds; '
                                          'too many for a simple tricarboxylic '
                                          'acid"',
                                          'False, "Error creating SMARTS '
                                          'patterns for carboxyl groups"',
                                          'False, f"Found {n_carboxyl} '
                                          'carboxyl group(s); expected exactly '
                                          '3"',
                                          'False, "No carbon atoms found"',
                                          'False, f"Low carboxyl-to-carbon '
                                          'ratio ({carboxyl_ratio:.2f}); '
                                          'expected at least 0.18"',
                                          'False, f"Molecular weight too high '
                                          '({mol_wt:.1f} Da); expected less '
                                          'than 600 Da for a tricarboxylic '
                                          'acid"',
                                          'True, ("Contains exactly three '
                                          'carboxyl groups, has acceptable '
                                          'amide count, no aromatic rings, "'],
                           'returns_count': 11,
                           'complexity': 5.8954673628956415},
    'message': '\n'
               'Attempt failed: F1 score of 0.6382978723404256 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@H](\\C=C\\C=C(\\C)[C@H]1CN[C@@H]([C@H]1CC(O)=O)C(O)=O)C(O)=O '
               'NAME: domoic acid REASON: CORRECT Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: O[C@@H]([C@H](CC(O)=O)C(O)=O)C(O)=O NAME: '
               'D-erythro-isocitric acid REASON: CORRECT Contains exactly '
               'three carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OCCC(NCCC(NCCC(O)C(O)=O)C(O)=O)C(O)=O NAME: avenic '
               'acid A REASON: CORRECT Contains exactly three carboxyl groups, '
               'has acceptable amide count, sufficient carboxyl/carbon ratio, '
               'and is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: O=C(O)[C@@H](NC[C@@H](C(O)=O)N)CCC(=O)O NAME: '
               'N-[(2S)-2-amino-2-carboxyethyl]-L-glutamic acid REASON: '
               'CORRECT Contains exactly three carboxyl groups, has acceptable '
               'amide count, sufficient carboxyl/carbon ratio, and is neutral '
               'and within weight range – consistent with a tricarboxylic '
               'acid\n'
               ' * SMILES: C(C(C(C)(C(=O)O)O)C(=O)O)C(O)=O NAME: '
               '3-hydroxybutane-1,2,3-tricarboxylic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(C(CCC(O)=O)C(O)=O)C(O)=O NAME: homoisocitric '
               'acid REASON: CORRECT Contains exactly three carboxyl groups, '
               'has acceptable amide count, sufficient carboxyl/carbon ratio, '
               'and is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: [H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O NAME: '
               '5-oxopent-3-ene-1,2,5-tricarboxylic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: NC(CC1=CC2=C(NC(CC2C(O)=O)C(O)=O)C(=O)C1=O)C(O)=O '
               'NAME: '
               '6-(2-amino-2-carboxyethyl)-7,8-dioxo-1,2,3,4,7,8-hexahydroquinoline-2,4-dicarboxylic '
               'acid REASON: CORRECT Contains exactly three carboxyl groups, '
               'has acceptable amide count, sufficient carboxyl/carbon ratio, '
               'and is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: '
               'N[C@@H](CSc1cc(C[C@H](N)C(O)=O)c(SC[C@H](N)C(O)=O)c(O)c1O)C(O)=O '
               "NAME: 2,5-S,S'-dicysteinyldopa REASON: CORRECT Contains "
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)\\C=C(/CC(=O)C(O)=O)C(O)=O NAME: '
               '(1E)-4-oxobut-1-ene-1,2,4-tricarboxylic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)CCCC[C@@](O)(CC(O)=O)C(O)=O NAME: '
               '(2R)-trihomocitric acid REASON: CORRECT Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: O[C@H]([C@H](CC(O)=O)C(O)=O)C(O)=O NAME: '
               'D-threo-isocitric acid REASON: CORRECT Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)CC(\\C=C\\C(=O)C(O)=O)C(O)=O NAME: '
               '(3E)-5-oxopent-3-ene-1,2,5-tricarboxylic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)CCC(=O)N[C@@H](CCCC(=O)C(O)=O)C(O)=O NAME: '
               'L-2-succinylamino-6-oxoheptanedioic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)C[C@H](\\C=C\\C(=O)C(O)=O)C(O)=O NAME: '
               '(2R,3E)-5-oxopent-3-ene-1,2,5-tricarboxylic acid REASON: '
               'CORRECT Contains exactly three carboxyl groups, has acceptable '
               'amide count, sufficient carboxyl/carbon ratio, and is neutral '
               'and within weight range – consistent with a tricarboxylic '
               'acid\n'
               ' * SMILES: OC(=O)CC(=CC(O)=O)C(O)=O NAME: aconitic acid '
               'REASON: CORRECT Contains exactly three carboxyl groups, has '
               'acceptable amide count, sufficient carboxyl/carbon ratio, and '
               'is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: CC(C(O)=O)C(O)(CC(O)=O)C(O)=O NAME: 2-methylcitric '
               'acid REASON: CORRECT Contains exactly three carboxyl groups, '
               'has acceptable amide count, sufficient carboxyl/carbon ratio, '
               'and is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: C([C@@H]([C@](C)(C(=O)O)O)C(=O)O)C(=O)O NAME: '
               '(2S,3R)-3-hydroxybutane-1,2,3-tricarboxylic acid REASON: '
               'CORRECT Contains exactly three carboxyl groups, has acceptable '
               'amide count, sufficient carboxyl/carbon ratio, and is neutral '
               'and within weight range – consistent with a tricarboxylic '
               'acid\n'
               ' * SMILES: OC(=O)\\C=C(\\C=C(/O)C(O)=O)C(O)=O NAME: '
               '4-carboxy-2-hydroxyhexa-2,4-dienedioic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)[C@H](CCN1CC[C@H]1C(O)=O)NCCC(=O)C(O)=O NAME: '
               "3''-deamino-3''-oxonicotianamine REASON: CORRECT Contains "
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)\\C=C(/C=C(/O)C(O)=O)C(O)=O NAME: '
               '4-carboxy-2-hydroxy-cis,cis-muconic acid REASON: CORRECT '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)CCC(C(O)=O)C(=O)C(O)=O NAME: 2-oxaloglutaric '
               'acid REASON: CORRECT Contains exactly three carboxyl groups, '
               'has acceptable amide count, sufficient carboxyl/carbon ratio, '
               'and is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: CCC(C(=O)O)(C(=O)O)C(=O)O NAME: '
               '1,1,1-propanetricarboxylic acid REASON: CORRECT Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: NC(=N)NCCC[C@H](N[C@H](CCC(O)=O)C(O)=O)C(O)=O NAME: '
               'D-nopaline REASON: CORRECT Contains exactly three carboxyl '
               'groups, has acceptable amide count, sufficient carboxyl/carbon '
               'ratio, and is neutral and within weight range – consistent '
               'with a tricarboxylic acid\n'
               ' * SMILES: '
               'O[C@@H](CN1C[C@@H](O)[C@H]1C(O)=O)[C@H](NCC[C@H](O)C(O)=O)C(O)=O '
               'NAME: 3-hydroxymugineic acid REASON: CORRECT Contains exactly '
               'three carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               'False positives: SMILES: '
               'O(CCCCCCC(C(C(O)=O)=C)C(O)=O)C(=O)C(O)=O NAME: '
               '2-Methylidene-3-(6-oxalooxyhexyl)butanedioic acid REASON: '
               'WRONGLY CLASSIFIED Contains exactly three carboxyl groups, has '
               'acceptable amide count, sufficient carboxyl/carbon ratio, and '
               'is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: '
               'O[C@@H]1C[C@@H](C([O-])=O)\\[N+](C1)=C/C=C1C[C@H](NC(=C\\1)C(O)=O)C(O)=O '
               'NAME: Portulacaxanthin I REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: N[C@@H](CCC(O)=O)C(=O)N[C@@H](CC(O)=O)C(O)=O NAME: '
               'Glu-Asp REASON: WRONGLY CLASSIFIED Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(CC(=O)NCCC[C@@H](N)C(O)=O)(CC(O)=O)C(O)=O NAME: '
               'delta-Citryl-d-ornithine REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: '
               'CC(O)=O.N[C@@H](CCCNC(N)=N)C(=O)N[C@@H](CCC(O)=O)C(O)=O NAME: '
               'L-arginyl-L-glutamic acid monoacetate REASON: WRONGLY '
               'CLASSIFIED Contains exactly three carboxyl groups, has '
               'acceptable amide count, sufficient carboxyl/carbon ratio, and '
               'is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: '
               'O=C(O)C1=C(O)C=C(OC)C=C1/C(/C(=C\\C(=O)O)/C)=C/C(=O)O NAME: '
               'Altenuic acid IV REASON: WRONGLY CLASSIFIED Contains exactly '
               'three carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: O[C@]([C@H](O)C(O)=O)(CC(O)=O)C(O)=O NAME: Garcinia '
               'acid REASON: WRONGLY CLASSIFIED Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: '
               '[NH4+].[NH4+].[NH4+].OC(CC([O-])=O)(CC([O-])=O)C([O-])=O NAME: '
               'triammonium citrate REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: '
               'COc1cc(cc(C(=O)\\C=C(/C=C(/O)C(O)=O)C(O)=O)c1O)C(O)=O NAME: '
               '4-[2-(5-Carboxy-2-hydroxy-3-methoxyphenyl)-2-oxoethylidene]-2-hydroxy-2-pentenedioate '
               'REASON: WRONGLY CLASSIFIED Contains exactly three carboxyl '
               'groups, has acceptable amide count, sufficient carboxyl/carbon '
               'ratio, and is neutral and within weight range – consistent '
               'with a tricarboxylic acid\n'
               ' * SMILES: OC(C(O)C(O)=O)(CC(O)=O)C(O)=O NAME: Hydroxycitric '
               'acid REASON: WRONGLY CLASSIFIED Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(NCC(O)=O)CC(NCCC(O)C(O)=O)C(O)=O NAME: '
               'Distichonic acid B REASON: WRONGLY CLASSIFIED Contains exactly '
               'three carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)CC[C@@]1(N[C@@H](Cc2nc[nH]c12)C(O)=O)C(O)=O '
               'NAME: Cucumopine REASON: WRONGLY CLASSIFIED Contains exactly '
               'three carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(CN1C(CC1)C(O)=O)C(NCCC(O)C(O)=O)C(O)=O NAME: '
               'Isomugineic acid REASON: WRONGLY CLASSIFIED Contains exactly '
               'three carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)C(CC[C@H](N)C(O)=O)C(N)C(O)=O NAME: Tabtoxin '
               'biosynthesis intermediate 3 REASON: WRONGLY CLASSIFIED '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: O1C(OC(C(O)C(O)=O)C(O)=O)C(O)C(O)C(O)C1C(O)=O NAME: '
               '2-[(6-carboxy-3,4,5-trihydroxyoxan-2-yl)oxy]-3-hydroxybutanedioic '
               'acid REASON: WRONGLY CLASSIFIED Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: '
               'N[C@@H](CC1=C/[N+](=C\\C=C2C[C@H](NC(=C/2)C(O)=O)C(O)=O)/C=N1)C([O-])=O '
               'NAME: Musca-aurin VII REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(O)=O NAME: '
               'Glu-Glu REASON: WRONGLY CLASSIFIED Contains exactly three '
               'carboxyl groups, has acceptable amide count, sufficient '
               'carboxyl/carbon ratio, and is neutral and within weight range '
               '– consistent with a tricarboxylic acid\n'
               ' * SMILES: '
               'OCCC[C@H](\\N=C/C=C1C[C@@H](NC(=C\\1)C(O)=O)C(O)=O)C(O)=O '
               'NAME: Humilixanthin REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1C(O)=O)C(C(O)=O)C(O)=O NAME: '
               '2-(6-carboxy-3,4,5-trihydroxyoxan-2-yl)propanedioic acid '
               'REASON: WRONGLY CLASSIFIED Contains exactly three carboxyl '
               'groups, has acceptable amide count, sufficient carboxyl/carbon '
               'ratio, and is neutral and within weight range – consistent '
               'with a tricarboxylic acid\n'
               ' * SMILES: [NH4+].[NH4+].OC(=O)C(O)(CC([O-])=O)CC([O-])=O '
               'NAME: diammonium citrate REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: C(SCC(O)=O)(SCC(O)=O)SCC(O)=O NAME: ritiometan '
               'REASON: WRONGLY CLASSIFIED Contains exactly three carboxyl '
               'groups, has acceptable amide count, sufficient carboxyl/carbon '
               'ratio, and is neutral and within weight range – consistent '
               'with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)[C@@H](NC(=O)CCC(O)=O)CCCC(N)C(O)=O NAME: '
               'N-Succinyl-L,L-2,6-diaminopimelate REASON: WRONGLY CLASSIFIED '
               'Contains exactly three carboxyl groups, has acceptable amide '
               'count, sufficient carboxyl/carbon ratio, and is neutral and '
               'within weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: OC(=O)C\\N=C/C=C1C[C@H](NC(=C\\1)C(O)=O)C(O)=O '
               'NAME: Portulacaxanthin III REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               ' * SMILES: [NH3+][C@@H](CC(C(O)=O)C(O)=O)C([O-])=O NAME: '
               'gamma-carboxy-L-glutamic acid zwitterion REASON: WRONGLY '
               'CLASSIFIED Contains exactly three carboxyl groups, has '
               'acceptable amide count, sufficient carboxyl/carbon ratio, and '
               'is neutral and within weight range – consistent with a '
               'tricarboxylic acid\n'
               ' * SMILES: '
               'OC(=O)[C@@H](\\N=C/C=C1C[C@H](NC(=C\\1)C(O)=O)C(O)=O)c1cc(O)no1 '
               'NAME: Musca-aurin-I REASON: WRONGLY CLASSIFIED Contains '
               'exactly three carboxyl groups, has acceptable amide count, '
               'sufficient carboxyl/carbon ratio, and is neutral and within '
               'weight range – consistent with a tricarboxylic acid\n'
               'False negatives: SMILES: '
               'CCCCCCCCCC[C@H](C(O)=O)[C@@](O)(CC(O)=O)C(O)=O NAME: '
               '(2S,3S)-2-hydroxytridecane-1,2,3-tricarboxylic acid REASON: '
               'MISSED Low carboxyl-to-carbon ratio (0.19); expected at least '
               '0.20\n'
               ' * SMILES: '
               'OC(=O)C1=CC(C=CC1=O)=C(c1ccc(O)c(c1)C(O)=O)c1ccc(O)c(c1)C(O)=O '
               'NAME: aurintricarboxylic acid REASON: MISSED Low '
               'carboxyl-to-carbon ratio (0.14); expected at least 0.20\n'
               ' * SMILES: '
               'C(/C=C\\CCCCC(=O)O)\\C=C/C=C/C=C/[C@H]([C@@H](O)CCCC(=O)O)SC[C@H](N)C(=O)O '
               'NAME: 20-carboxyleukotriene E4 REASON: MISSED Low '
               'carboxyl-to-carbon ratio (0.13); expected at least 0.20\n'
               ' * SMILES: '
               'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\C/C=C\\CCC(O)=O '
               'NAME: '
               '16(S)-glutathionyl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
               'acid REASON: MISSED Contains 2 amide bonds; too many for a '
               'simple tricarboxylic acid\n'
               ' * SMILES: '
               'C([C@H](NC(CC[C@@H](C(=O)O)N)=O)C(NCC(=O)O)=O)S[C@H](\\C=C\\C=C\\C[C@@H](C/C=C\\CCCCC)O)[C@@H](O)CCCC(=O)O '
               'NAME: 11,12-dihydro-(12R)-hydroxyleukotriene C4 REASON: MISSED '
               'Contains 2 amide bonds; too many for a simple tricarboxylic '
               'acid\n'
               ' * SMILES: '
               'C[C@H](N1C(=O)CCC1(O)C(O)=O)C(=O)NCCOC(=O)C[C@](O)(CC(O)=O)C(O)=O '
               'NAME: vibrioferrin REASON: MISSED Contains 2 amide bonds; too '
               'many for a simple tricarboxylic acid\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(O)C[C@]1(CC3=C)[C@@H](C(O)=O)[C@]1([H])[C@@](C)([C@@H](O)CC[C@@]21C(O)=O)C(O)=O '
               'NAME: gibberellin A28 REASON: MISSED Low carboxyl-to-carbon '
               'ratio (0.15); expected at least 0.20\n'
               ' * SMILES: OC(=O)CCP(CCC(O)=O)CCC(O)=O NAME: TCEP REASON: '
               'MISSED Contains non-organic atom: P (atomic num: 15)\n'
               ' * SMILES: '
               'O=C(NCCNC(CCC(C(O)=O)=O)=O)C[C@](CC(=O)NC[C@@H](C(O)=O)N)(C(O)=O)O '
               'NAME: staphyloferrin B REASON: MISSED Contains 3 amide bonds; '
               'too many for a simple tricarboxylic acid\n'
               ' * SMILES: '
               'N[C@@H](CS[C@H](\\C=C\\C=C\\C=C/CCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O '
               'NAME: 16-carboxy-17,18,19,20-tetranor-leukotriene E3 REASON: '
               'MISSED Low carboxyl-to-carbon ratio (0.16); expected at least '
               '0.20\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Found 0 carboxyl group(s); '
                                               'expected exactly 3'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule has nonzero formal '
                                               'charge; expected a neutral '
                                               'tricarboxylic acid'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Contains non-organic atom: F '
                                               '(atomic num: 9)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Found 0 carboxyl group(s); '
                                               'expected exactly 3'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Found 0 carboxyl group(s); '
                                               'expected exactly 3'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule contains aromatic '
                                               'rings; not a simple '
                                               'tricarboxylic acid'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Found 0 carboxyl group(s); '
                                               'expected exactly 3'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecule contains aromatic '
                                               'rings; not a simple '
                                               'tricarboxylic acid'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Found 0 carboxyl group(s); '
                                               'expected exactly 3'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Found 0 carboxyl group(s); '
                                               'expected exactly 3'}],
    'sample_false_negatives': [   {   'smiles': 'OC(=O)C1=CC(C=CC1=O)=C(c1ccc(O)c(c1)C(O)=O)c1ccc(O)c(c1)C(O)=O',
                                      'name': 'aurintricarboxylic acid',
                                      'reason': 'Molecule contains aromatic '
                                                'rings; not a simple '
                                                'tricarboxylic acid'},
                                  {   'smiles': 'N[C@@H](CSc1cc(C[C@H](N)C(O)=O)c(SC[C@H](N)C(O)=O)c(O)c1O)C(O)=O',
                                      'name': "2,5-S,S'-dicysteinyldopa",
                                      'reason': 'Molecule contains aromatic '
                                                'rings; not a simple '
                                                'tricarboxylic acid'},
                                  {   'smiles': 'C(/C=C\\CCCCC(=O)O)\\C=C/C=C/C=C/[C@H]([C@@H](O)CCCC(=O)O)SC[C@H](N)C(=O)O',
                                      'name': '20-carboxyleukotriene E4',
                                      'reason': 'Low carboxyl-to-carbon ratio '
                                                '(0.13); expected at least '
                                                '0.18'},
                                  {   'smiles': 'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\C/C=C\\CCC(O)=O',
                                      'name': '16(S)-glutathionyl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
                                              'acid',
                                      'reason': 'Contains 2 amide bonds; too '
                                                'many for a simple '
                                                'tricarboxylic acid'},
                                  {   'smiles': 'C([C@H](NC(CC[C@@H](C(=O)O)N)=O)C(NCC(=O)O)=O)S[C@H](\\C=C\\C=C\\C[C@@H](C/C=C\\CCCCC)O)[C@@H](O)CCCC(=O)O',
                                      'name': '11,12-dihydro-(12R)-hydroxyleukotriene '
                                              'C4',
                                      'reason': 'Contains 2 amide bonds; too '
                                                'many for a simple '
                                                'tricarboxylic acid'},
                                  {   'smiles': 'C[C@H](N1C(=O)CCC1(O)C(O)=O)C(=O)NCCOC(=O)C[C@](O)(CC(O)=O)C(O)=O',
                                      'name': 'vibrioferrin',
                                      'reason': 'Contains 2 amide bonds; too '
                                                'many for a simple '
                                                'tricarboxylic acid'},
                                  {   'smiles': '[H][C@@]12CC[C@]3(O)C[C@]1(CC3=C)[C@@H](C(O)=O)[C@]1([H])[C@@](C)([C@@H](O)CC[C@@]21C(O)=O)C(O)=O',
                                      'name': 'gibberellin A28',
                                      'reason': 'Low carboxyl-to-carbon ratio '
                                                '(0.15); expected at least '
                                                '0.18'},
                                  {   'smiles': 'OC(=O)CCP(CCC(O)=O)CCC(O)=O',
                                      'name': 'TCEP',
                                      'reason': 'Contains non-organic atom: P '
                                                '(atomic num: 15)'},
                                  {   'smiles': 'O=C(NCCNC(CCC(C(O)=O)=O)=O)C[C@](CC(=O)NC[C@@H](C(O)=O)N)(C(O)=O)O',
                                      'name': 'staphyloferrin B',
                                      'reason': 'Contains 3 amide bonds; too '
                                                'many for a simple '
                                                'tricarboxylic acid'},
                                  {   'smiles': 'N[C@@H](CS[C@H](\\C=C\\C=C\\C=C/CCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O',
                                      'name': '16-carboxy-17,18,19,20-tetranor-leukotriene '
                                              'E3',
                                      'reason': 'Low carboxyl-to-carbon ratio '
                                                '(0.16); expected at least '
                                                '0.18'}],
    'attempt': 4,
    'reasoning': 'Below is an improved version. In our reasoning we noted that '
                 'many errors seemed to come from a too‐strict '
                 'carboxyl–to–carbon ratio cutoff as well as allowing '
                 'molecules with aromatic rings (or other “complex” features) '
                 'that are not “simple” tricarboxylic acids. To address these '
                 'issues we (1) lower the ratio threshold slightly (from 0.20 '
                 'to 0.18) so that long‐chain acids having borderline values '
                 'are accepted, and (2) reject molecules that contain any '
                 'aromatic rings. (Other heuristics such as checking amide '
                 'bonds, rejecting non‐organic atoms, and keeping the MW below '
                 '600 Da are maintained.) \n'
                 '\n'
                 'Below is the complete code in one Python block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 72,
    'num_false_positives': 53,
    'num_true_negatives': 142147,
    'num_false_negatives': 28,
    'num_negatives': None,
    'precision': 0.576,
    'recall': 0.72,
    'f1': 0.64,
    'accuracy': 0.9994307800421645,
    'negative_predictive_value': 0.999803059609636}