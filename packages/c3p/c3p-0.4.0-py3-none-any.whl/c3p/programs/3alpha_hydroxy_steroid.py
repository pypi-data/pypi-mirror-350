"""
Classifies: CHEBI:36835 3alpha-hydroxy steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3alpha_hydroxy_steroid(smiles: str):
    """
    Determines if a molecule is a 3alpha-hydroxy steroid based on its SMILES string.
    A 3alpha-hydroxy steroid is a 3-hydroxy steroid where the 3-hydroxy substituent is in the alpha-position.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 3alpha-hydroxy steroid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a pattern for the steroid backbone (adjust as needed for specificity)
    steroid_backbone_pattern = Chem.MolFromSmarts("C1CCC2C3CCC4CC[C@H](O)C[C@]4(C)C3CC[C@]12C")
    if not mol.HasSubstructMatch(steroid_backbone_pattern):
        return False, "No steroid backbone found"
        
    # Define a SMARTS pattern for 3alpha-hydroxy group
    # Note: This simplification assumes specific positions and stereochemistry, may need adjustment
    hydroxy_pattern = Chem.MolFromSmarts("C[C@H](O)C")  # Hydroxyl at position 3 in alpha
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No 3alpha-hydroxy group found"

    return True, "Contains steroid backbone with 3alpha-hydroxy group"

# Example usage
smiles_example = "C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(C[C@@H]([C@@H]1O)O)[H])[H])(CC[C@@]4([C@@H]([C@H]([C@@H](CC(C)C)O)O)C)[H])[H])C)[H])C"
print(is_3alpha_hydroxy_steroid(smiles_example))  # Output should be True with reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36835',
                          'name': '3alpha-hydroxy steroid',
                          'definition': 'A 3-hydroxy steroid in which the '
                                        '3-hydroxy substituent is in the '
                                        'alpha-position.',
                          'parents': ['CHEBI:35681', 'CHEBI:36834'],
                          'xrefs': [   'MetaCyc:3-alpha-Hydroxysteroids',
                                       'PMID:11514561'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C1C2=C(OC(=C1)C)C3=C(OC)C=C(OC)C=C3C(=C2O)C4=C5OC(=CC(C5=C(O)C=6C4=CC(OC)=CC6OC)=O)C',
                                     'name': 'Isonigerone',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                     'name': '1-myristoyl-2-oleoyl-sn-glycero-3-phosphatidylglycerol(1-)',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'C(=C\\C/C=C\\CCCC(NC)=O)\\C/C=C\\C/C=C\\CCCCC',
                                     'name': 'N-methyl arachidonoyl amine',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'OC1(O)[C@]23N(CC1)C(N(O)[C@H]([C@@]3(N=C(N2)N)[H])CO)=N',
                                     'name': 'Decarbamoylneosaxitoxin',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'S([C@H]1N(C(=O)/C(=C\\C2=CC=C(OCC=C(C)C)C=C2)/N(C1=O)C)C)C',
                                     'name': 'Fusaperazine F',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'Oc1ccccc1I',
                                     'name': '2-iodophenol',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'O=C1N(CC(=O)N[C@H](C(=O)O[C@H]([C@@H](C(NC(C=C1)=C)=O)C)C(CCCCCCCCCCCCCC)C)C(O)C(=O)N)C',
                                     'name': 'Rakicidin H',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C',
                                     'name': 'Prenylterphenyllin F',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                     'reason': 'No steroid backbone found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'Gal2GlcNAc2Man3GlcNAcFucGlcNAc',
                                     'reason': 'No steroid backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'C1[C@@]2([C@@]([C@@]3([C@](C[C@H](O)CC3)(C1)[H])C)(CC[C@@]4([C@H](CC[C@@]24[H])OS(O)(=O)=O)C)[H])[H]',
                                      'name': '(3alpha,5alpha,17beta)-3-hydroxyandrostan-17-yl '
                                              'sulfate',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': 'CC(C)[C@H](C)[C@@H](O)[C@H](O)[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC(=O)[C@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C',
                                      'name': 'typhasterol',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCC[C@H](C)C(O)=O',
                                      'name': '(25S)-3alpha,7alpha,12alpha-trihydroxy-5beta-cholestan-26-oic '
                                              'acid',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])C[C@@H](O)[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCC(O)=O',
                                      'name': 'murideoxycholic acid',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@]1([C@H](C)CCCC(O)=O)[C@H](O)C[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C',
                                      'name': 'homoavicholic acid',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@@]1(CCC2C3=CC(=O)[C@@]4([H])C[C@H](O)CC[C@]4(C)C3CC[C@]12C)[C@H](C)CCCC(C)COS(O)(=O)=O',
                                      'name': 'asterasterol B',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCCC(CO)COS(O)(=O)=O',
                                      'name': '5beta-cyprinol sulfate',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[C@]12([C@]([C@]3([C@](CC1)([C@@]4([C@@](C[C@@H](CC4)O)(C[C@H]3O)[H])C)[H])[H])(CC[C@@]2([C@@H](CCCC(C)(C)O)C)[H])[H])C',
                                      'name': '5beta-cholestane-3alpha,7alpha,25-triol',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])CC[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCCC(C)C(O)=O',
                                      'name': '3alpha,7alpha-dihydroxy-5beta-cholestan-26-oic '
                                              'acid',
                                      'reason': 'No steroid backbone found'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CC[C@H](O)C(C)CO',
                                      'name': '(24S)-5beta-cholestane-3alpha,7alpha,12alpha,24,26-pentol',
                                      'reason': 'No steroid backbone found'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as 3alpha-hydroxy steroids '
                 'based on their SMILES string, we can take the following '
                 'approach:\n'
                 '\n'
                 '1. **Understand the Structure Key Features**:\n'
                 '   - A 3alpha-hydroxy steroid is characterized by having a '
                 'hydroxyl group (-OH) at the 3rd position in the '
                 'alpha-configuration on a steroid backbone.\n'
                 '   - Steroids typically have a structure composed of four '
                 'fused carbon rings.\n'
                 '\n'
                 '2. **Identify Relevant Substructures**:\n'
                 '   - We need to identify a hydroxyl group in the alpha '
                 'position on the steroid framework, which consists of a '
                 'cyclopentanoperhydrophenanthrene ring system.\n'
                 '   - For alpha configurations, this often means the hydroxyl '
                 'group is facing downward in 3D space, often represented by '
                 '[C@ or C@@ in SMILES depending on the orientation.\n'
                 '\n'
                 '3. **SMILES and SMARTS Pattern**:\n'
                 '   - SMILES encode 3D stereochemistry information which is '
                 'essential in distinguishing alpha vs. beta configurations.\n'
                 '   - We should create a SMARTS pattern to identify the '
                 'steroid backbone and then verify the presence of the '
                 '3alpha-hydroxy group.\n'
                 '\n'
                 '4. **Programming with RDKit**:\n'
                 '   - We will use RDKit, a cheminformatics library, to parse '
                 'and analyze the SMILES structure.\n'
                 '\n'
                 "Here's the implementation of such a classifier:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 60,
    'num_true_negatives': 142149,
    'num_false_negatives': 85,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.06593406593406594,
    'f1': 0.07643312101910828,
    'accuracy': 0.9989810260014055,
    'negative_predictive_value': 0.9994023932393099}