"""
Classifies: CHEBI:22798 beta-D-glucoside
"""
"""
Classifies: CHEBI:59826 beta-D-glucoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_beta_D_glucoside(smiles: str):
    """
    Determines if a molecule is a beta-D-glucoside based on its SMILES string.
    A beta-D-glucoside is a molecule where a beta-D-glucose moiety is attached to another molecule via a glycosidic bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-D-glucoside, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the beta-D-glucose pattern
    # The pattern should match the beta-D-glucose moiety with the glycosidic bond at C1
    beta_D_glucose_pattern = Chem.MolFromSmarts("[C@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O")
    
    # Check if the molecule contains the beta-D-glucose pattern
    if not mol.HasSubstructMatch(beta_D_glucose_pattern):
        return False, "No beta-D-glucose moiety found"

    # Check the configuration of the glycosidic bond
    # The glycosidic bond should be in the beta-configuration (axial position)
    # We can check this by ensuring that the anomeric carbon (C1) is connected to the rest of the molecule in the correct orientation
    # This is a simplified check and may not cover all cases
    anomeric_carbon = mol.GetSubstructMatch(beta_D_glucose_pattern)[0]
    for neighbor in mol.GetAtomWithIdx(anomeric_carbon).GetNeighbors():
        if neighbor.GetAtomicNum() != 8:  # Not an oxygen (glycosidic bond)
            continue
        # Check if the glycosidic bond is in the beta-configuration
        # This is a heuristic and may not be accurate for all cases
        if neighbor.GetIdx() in mol.GetSubstructMatch(beta_D_glucose_pattern):
            return True, "Contains beta-D-glucose moiety with beta-configuration glycosidic bond"

    return False, "No beta-configuration glycosidic bond found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22798',
                          'name': 'beta-D-glucoside',
                          'definition': 'Any D-glucoside in which the anomeric '
                                        'centre has beta-configuration.',
                          'parents': ['CHEBI:35436', 'CHEBI:60980'],
                          'xrefs': ['KEGG:C00963'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 32,
                           'log_lines_of_code': 3.4657359027997265,
                           'indent_by_line': [   1,
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
                                                 0,
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
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'HasSubstructMatch',
                                                 'GetIdx',
                                                 'GetAtomWithIdx',
                                                 'GetNeighbors',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetSubstructMatch'],
                           'methods_called_count': 8,
                           'smarts_strings': [   '[C@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O'],
                           'smarts_strings_count': 1,
                           'defs': ['is_beta_D_glucoside(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No beta-D-glucose moiety '
                                          'found"',
                                          'True, "Contains beta-D-glucose '
                                          'moiety with beta-configuration '
                                          'glycosidic bond"',
                                          'False, "No beta-configuration '
                                          'glycosidic bond found"'],
                           'returns_count': 4,
                           'complexity': 3.893147180559945},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CC(C)CN=C1C=C(OC2=C1C=C(C=C2)Cl)C3=CC=CC=C3',
                                     'name': '6-chloro-N-(2-methylpropyl)-2-phenyl-1-benzopyran-4-imine',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'O1C2=C(C(O)=C(C(O)=C2)C)C(=O)C(O)=C1C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Pinomyricetin',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'CC1=C(C(=O)OC2=CC(=C(C=C12)Cl)O)CC(=O)N3CCN(CC3)C(=O)C4COC5=CC=CC=C5O4',
                                     'name': '6-chloro-3-[2-[4-[2,3-dihydro-1,4-benzodioxin-3-yl(oxo)methyl]-1-piperazinyl]-2-oxoethyl]-7-hydroxy-4-methyl-1-benzopyran-2-one',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'O=C1OC2=C(C3=C(C(=O)O[C@@H]3O)C(=C2COC(=O)/C=C/C(=O)O)O)OC4=C1C(=CC(=C4C=O)O)C',
                                     'name': 'Quaesitic acid',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCCCN)C(O)=O)[C@@H](N)CC=2C=3C(NC2)=CC=CC3',
                                     'name': 'Trp-Pro-Lys',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'C1CCC(CC1)NC(=O)C[C@@H]2C[C@H]3[C@@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)NC5=CC=CC=C5F',
                                     'name': '2-[(1R,3S,4aR,9aS)-6-[(2-fluorophenyl)carbamoylamino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b][1]benzofuran-3-yl]-N-cyclohexylacetamide',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'O(CCC/C=C/C/C=C\\CCCCC)C(=O)C',
                                     'name': '4E,7Z-Tridecadienyl acetate',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'O=C1N([C@H](C(=O)N[C@H](C(=O)N([C@H](C(N[C@H]1CC2=C(O)C=C(OC/C=C/C)C=C2)=O)CC(C)C)C)CC3=CC=C(OCC=C=C)C=C3)CC(C)C)C',
                                     'name': '(E)-pseudoxylallemycin F',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'N[C@@H]1[C@@H](O)C(O)O[C@H](CO)[C@H]1O',
                                     'name': '3-amino-3-deoxy-D-glucopyranose',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'},
                                 {   'smiles': 'OC(CN(CC(O)C)CC(O)C)C',
                                     'name': 'Triisopropanolamine',
                                     'reason': 'No beta-D-glucose moiety '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]1(O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)c(O)c2)[C@H](O)[C@H]1O)[C@H](O)CO',
                                      'name': 'quercetin '
                                              '3-O-beta-D-glucofuranoside',
                                      'reason': 'No beta-D-glucose moiety '
                                                'found'},
                                  {   'smiles': 'CC[C@H]1O[C@@H](OCC\\C=C/C[C@@H]2[C@H](CCC2=O)CC(O)=O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '12-hydroxyjasmonic acid '
                                              '12-O-beta-D-glucoside',
                                      'reason': 'No beta-D-glucose moiety '
                                                'found'},
                                  {   'smiles': 'O1[C@@H](OC[C@@H](O)[C@H](O)[C@H](O)[C@@H](NC(=O)C)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O)[C@H]1CO',
                                      'name': 'beta-D-GlcpNAc-(1->6)-GalNAc-ol',
                                      'reason': 'No beta-D-glucose moiety '
                                                'found'},
                                  {   'smiles': 'C[C@@H]1O[C@@H](Oc2cc(OC(C)=O)c3c(c2)oc(-c2ccc(OC(C)=O)c(OC(C)=O)c2)c(O[C@@H]2O[C@H](CC(C)=O)[C@@H](OC(C)=O)[C@H](OC(C)=O)[C@H]2OC(C)=O)c3=O)[C@H](OC(C)=O)[C@H](OC(C)=O)[C@H]1OC(C)=O',
                                      'name': 'petiolaroside decaacetate',
                                      'reason': 'No beta-D-glucose moiety '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'To classify a molecule as a beta-D-glucoside, we need to '
                 'identify the presence of a beta-D-glucose moiety attached to '
                 'another molecule via a glycosidic bond. The '
                 'beta-configuration means that the glycosidic bond is formed '
                 'with the hydroxyl group on the anomeric carbon (C1) in the '
                 'axial position (downwards) relative to the glucose ring.\n'
                 '\n'
                 'Here’s the step-by-step reasoning for the classification:\n'
                 '\n'
                 '1. **Identify the glucose moiety**: The glucose moiety '
                 'should have the typical structure of beta-D-glucose, which '
                 'includes a six-membered ring with hydroxyl groups in '
                 'specific positions.\n'
                 '2. **Check the glycosidic bond**: The glycosidic bond should '
                 'be formed at the anomeric carbon (C1) of the glucose '
                 'moiety.\n'
                 '3. **Verify the beta-configuration**: The glycosidic bond '
                 'should be in the beta-configuration, meaning the hydroxyl '
                 'group on C1 is in the axial position.\n'
                 '\n'
                 'The program will use RDKit to parse the SMILES string, '
                 'identify the glucose moiety, and check the configuration of '
                 'the glycosidic bond.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 540,
    'num_false_positives': 14268,
    'num_true_negatives': 127488,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.03646677471636953,
    'recall': 0.9926470588235294,
    'f1': 0.07034914017717561,
    'accuracy': 0.899704848910752,
    'negative_predictive_value': 0.9999686254823832}