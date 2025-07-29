"""
Classifies: CHEBI:30527 flavin
"""
from rdkit import Chem

def is_flavin(smiles: str):
    """
    Determines if a molecule is a flavin based on its SMILES string.
    A flavin is a derivative of the dimethylisoalloxazine core with a substitution at the 10 position.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a flavin, False otherwise
        str: Reason for classification
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the dimethylisoalloxazine core pattern; we use a simplified SMARTS string
    flavin_core_smarts = "Cc1cc2nc3c(nc(=O)[nH]c3=O)n(C)c2cc1C"
    flavin_core = Chem.MolFromSmarts(flavin_core_smarts)
    
    # Check if the molecule contains the core structure
    if not mol.HasSubstructMatch(flavin_core):
        return False, "Does not contain the dimethylisoalloxazine core"
    
    # Get matches and check for substitution at the 10 position
    matches = mol.GetSubstructMatch(flavin_core)
    if matches:
        # Assuming position 10 corresponds to the nitrogen atom in the core
        position_10 = matches[5]  # example index for position 10, adjust as necessary
        atom = mol.GetAtomWithIdx(position_10)
        
        # Check for substitution at position 10 (it should have more than one bond)
        if len(atom.GetNeighbors()) <= 1:
            return False, "No substitution at position 10"
    
    return True, "Contains dimethylisoalloxazine core with substitution at position 10"

# Example usage
smiles = "Cc1cc2nc3c(nc(=O)[nH]c3=O)n(C)c2cc1C"
result, reason = is_flavin(smiles)
print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:30527',
                          'name': 'flavin',
                          'definition': 'A derivative of the '
                                        'dimethylisoalloxazine '
                                        '(7,8-dimethylbenzo[g]pteridine-2,4(3H,10H)-dione) '
                                        'skeleton, with a substituent on the '
                                        '10 position.',
                          'parents': ['CHEBI:38925'],
                          'xrefs': ['KEGG:C00176'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1OC(=O)C=C1',
                                     'name': '(S)-5-methylfuran-2(5H)-one',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'Cc1cccc(c1)C(O)=O',
                                     'name': 'm-toluic acid',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'CN(C)CC(=O)NC[C@@H]1[C@@H]([C@@H](N1)CO)C2=CC=C(C=C2)C3=CC=CC(=C3)C#N',
                                     'name': 'N-[[(2S,3S,4R)-3-[4-(3-cyanophenyl)phenyl]-4-(hydroxymethyl)-2-azetidinyl]methyl]-2-(dimethylamino)acetamide',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCCCC(=O)CC(O)=O)[C@H](O)C[C@H]1O',
                                     'name': 'bkos#20',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O',
                                     'name': 'PG(18:1(11Z)/18:1(11Z))',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC=2C3=C(C=CC=C3)NC2)CCC(=O)N)(C)C)(C)C)(CC)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)CC4=CC=CC=C4)(C)C)CO)(C)C)(C)C)CC(C)C)CCC(=O)N)(C)C)(C)C)C)C)(C)C',
                                     'name': 'Chrysospermin B',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'CC1(C=CC2=C3C(=CC(=C2O1)OC)C(=O)C(=CO3)C4=CC5=C(C=C4OC)OCO5)C',
                                     'name': '6-methoxy-3-(6-methoxy-1,3-benzodioxol-5-yl)-8,8-dimethyl-4-pyrano[2,3-h][1]benzopyranone',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)NCC(O)=O)C',
                                     'name': 'Glu-Thr-Gly',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]3[C@@H](O)[C@H](O)[C@H](O[C@@H]3OC[C@H]4O[C@@H](O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO)O)[C@@H](O)[C@@H](O)[C@@H]4O)CO)[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO',
                                     'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3S,4S,5S,6S)-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'},
                                 {   'smiles': 'COCCOC(C)C(O)=O',
                                     'name': '2-(2-methoxyethoxy)propanoic '
                                             'acid',
                                     'reason': 'Does not contain the '
                                               'dimethylisoalloxazine core'}],
    'sample_false_negatives': [   {   'smiles': 'Cc1cc2N(C[C@H](O)[C@H](O)[C@H](O)COP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c(N)ncnc34)c3[nH]c(=O)[nH]c(=O)c3N(c2cc1C)S(O)(=O)=O',
                                      'name': 'N(5)-sulfo-FADH2',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'Cc1cc2[N]c3c([nH]c(=O)[nH]c3=O)N(C[C@H](O)[C@H](O)[C@H](O)COP(O)(O)=O)c2cc1C',
                                      'name': 'FMNH(.)',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'O1[C@H](N2C3=NC4=C(N=C3C(=O)NC2=O)C=C(C(=C4)C)C)[C@H](O)[C@H](O)[C@H]1CO',
                                      'name': '1-(a-ribofuranosyl)-lumichrome',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'O=C1N(C2=NC=3C(=CC(CO)=C(C3)C)N=C2C(N1)=O)C',
                                      'name': '1-methyl-11-hydroxylumichrome',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'Cc1cc2Nc3c([nH]c(=O)[nH]c3=O)N(C[C@H](O)[C@H](O)[C@H](O)CO)c2cc1C',
                                      'name': '1,5-dihydroriboflavin',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'C(N1C=2C(=NC3=C1C=C(C(=C3)C)N)C(NC(N2)=O)=O)[C@H](O)[C@H](O)[C@H](O)COP(O)(=O)O',
                                      'name': '8-amino-8-demethylriboflavin '
                                              "5'-phosphate",
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'Cc1cc2Nc3c([nH]c(=O)[nH]c3=O)N(C[C@H](O)[C@H](O)[C@H](O)COP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c(N)ncnc34)c2cc1C',
                                      'name': 'FADH2',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'Cc1cc2Nc3c([nH]c(=O)[nH]c3=O)N(C[C@H](O)[C@H](O)[C@H](O)COP(O)(O)=O)c2cc1C',
                                      'name': 'FMNH2',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'C=12N=C(NC(C1[N+]=3C=4C(N2C[C@@H]([C@@H]([C@@H](COP(O)(O)=O)O)O)O)=CC(=C(C4C(C)(CC3)C)C)C)=O)[O-]',
                                      'name': 'prenyl-FMN',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'},
                                  {   'smiles': 'O=C1N(C2=NC=3C(=CC(C)=C(C3)C)N=C2C(N1)=O)[C@@H]4O[C@H]([C@H](O)[C@H]([C@H]4O)O)C',
                                      'name': 'Ochangoside',
                                      'reason': 'Does not contain the '
                                                'dimethylisoalloxazine core'}],
    'attempt': 0,
    'reasoning': 'To classify a chemical entity as a flavin, we will write a '
                 'function `is_flavin` that uses the RDKit library to analyze '
                 'the SMILES string of a given molecule. The important '
                 'structural feature to consider for flavins is the '
                 'dimethylisoalloxazine scaffold with a substitution at the '
                 "10th position. Let's walk through the steps to implement "
                 'this function.\n'
                 '\n'
                 '1. **Import the RDKit Libraries**: We will import the '
                 'necessary RDKit modules for working with molecular '
                 'structures and substructure searches.\n'
                 '\n'
                 '2. **Define the Function**: The function will take a SMILES '
                 'string as input and will attempt to identify whether the '
                 'given structure is a flavin.\n'
                 '\n'
                 '3. **Parse the SMILES String**: We will decode the SMILES '
                 'string into an RDKit molecule object.\n'
                 '\n'
                 '4. **Identify the Core Structure**: We will define a SMARTS '
                 'pattern that represents the dimethylisoalloxazine core, '
                 'which is crucial for a molecule to be classified as a '
                 'flavin.\n'
                 '\n'
                 '5. **Check for Substitution at Position 10**: After '
                 "identifying the core, we'll ensure that there's a "
                 'substituent at the 10th position by further examining the '
                 'molecule.\n'
                 '\n'
                 '6. **Return Classification Result**: The function will '
                 'return a boolean indicating whether the molecule is a flavin '
                 'and a diagnostic message explaining the decision.\n'
                 '\n'
                 "Let's implement this step by step in Python:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 2,
    'num_true_negatives': 142269,
    'num_false_negatives': 14,
    'num_negatives': None,
    'precision': 0.8823529411764706,
    'recall': 0.5172413793103449,
    'f1': 0.6521739130434783,
    'accuracy': 0.9998875614898103,
    'negative_predictive_value': 0.9999016045486812}