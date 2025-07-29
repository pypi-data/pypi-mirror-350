"""
Classifies: CHEBI:84948 11,12-saturated fatty acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_11_12_saturated_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule belongs to the class 11,12-saturated fatty acyl-CoA(4-) based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is 11,12-saturated fatty acyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES to obtain an RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Pattern to find a long chain fatty acid, flexible based on saturation and chain length
    # This should match long hydrophobic carbon chains
    fatty_acid_pattern = Chem.MolFromSmarts("C[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]")
    if not mol.HasSubstructMatch(fatty_acid_pattern):
        return False, "No or incomplete long chain fatty acid detected"

    # Recognize the coenzyme A moiety, allowing flexibility with bonds and charges
    coa_pattern = Chem.MolFromSmarts("SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(=O)([O-])OP(=O)([O-])OCC1OCC(O)C1OP(=O)([O-])[O-]")
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "No CoA moiety found"

    # Inclusion of chiral centers and specific 3-hydroxyl group identification
    hydroxyl_pattern = Chem.MolFromSmarts("[C@@H](O)CC(=O)S")
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "Chiral hydroxyl group not in expected position"

    return True, "Molecule matches the structural patterns for 11,12-saturated fatty acyl-CoA(4-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:84948',
                          'name': '11,12-saturated fatty acyl-CoA(4-)',
                          'definition': 'Any fatty acyl-CoA(4-) in which the '
                                        '11-12 bond of the fatty acyl group is '
                                        'saturated. This is needed for a '
                                        'reaction together with CHEBI:84947',
                          'parents': ['CHEBI:77636'],
                          'xrefs': ['PMID:10563812', 'PMID:2295634'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: '
               '(3R,17Z,20Z,23Z,26Z,29Z)-3-hydroxydotriacontapentaenoyl-CoA(4-) '
               'REASON: MISSED No CoA moiety found\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (3R,13Z)-3-hydroxydocosenoyl-CoA(4-) REASON: MISSED No '
               'long chain fatty acid detected\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: '
               '(19Z,22Z,25Z,28Z,31Z)-3-oxotetratriacontapentaenoyl-CoA(4-) '
               'REASON: MISSED No CoA moiety found\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCC(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-hydroxyisopentadecanoyl-CoA(4-) REASON: MISSED No long '
               'chain fatty acid detected\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (R)-3-hydroxytriacontanoyl-CoA(4-) REASON: MISSED No CoA '
               'moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (R)-3-hydroxytetradecanoyl-CoA(4-) REASON: MISSED No '
               'long chain fatty acid detected\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxopalmitoyl-CoA(4-) REASON: MISSED No long chain '
               'fatty acid detected\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (R)-3-hydroxydocosanoyl-CoA(4-) REASON: MISSED No CoA '
               'moiety found\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z,16Z,19Z)-3-oxodocosatrienoyl-CoA(4-) REASON: MISSED '
               'No long chain fatty acid detected\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxodocosanoyl-CoA(4-) REASON: MISSED No CoA moiety '
               'found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'P(OCC(OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCN(C)C)(O)=O',
                                     'name': 'Pe-nme2(20:3(5Z,8Z,11Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'O1[C@]2([C@@H](O)[C@H](O)[C@@H](O)[C@@]1(OCC[C@H](CCC=C(C(OC[C@]3(O)[C@@H](O)[C@@](OC3)(OC2)[H])=O)C)C)[H])[H]',
                                     'name': 'Urceolide',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CC1=CC(=C(C=C1)C)C(=O)CSC2=NN=C(S2)C',
                                     'name': '1-(2,5-dimethylphenyl)-2-[(5-methyl-1,3,4-thiadiazol-2-yl)thio]ethanone',
                                     'reason': 'No or incomplete long chain '
                                               'fatty acid detected'},
                                 {   'smiles': 'O=C1C=C([C@@]2(C(C[C@@H](C2)O)(C)C)C)CC[C@@]1(O)C',
                                     'name': 'Enokipodin H',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CCCC[C@](Cn1cncn1)(C#N)c1ccc(Cl)cc1',
                                     'name': '(S)-myclobutanil',
                                     'reason': 'No or incomplete long chain '
                                               'fatty acid detected'},
                                 {   'smiles': 'O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)CCCCC)CC(=O)O)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1C(C)C)=O)CC3=CC=CC=C3)C)=O)CC(C)C)C2=O)O)CCCCN(C)C)C',
                                     'name': 'Cyanopeptolin D',
                                     'reason': 'No or incomplete long chain '
                                               'fatty acid detected'},
                                 {   'smiles': 'O1[C@]2(O)N([C@H](C(=O)N3[C@]2(CCC3)[H])C(C)C)C(=O)[C@@]1(NC(=O)[C@H]4CN([C@]5(C(=C4)C6=C7C(C5)=CNC7=CC=C6)[H])C)C',
                                     'name': 'Ergovaline',
                                     'reason': 'No or incomplete long chain '
                                               'fatty acid detected'},
                                 {   'smiles': 'OC(=O)CCCCCCC#CCCCC',
                                     'name': '8-tridecynoic acid',
                                     'reason': 'No CoA moiety found'},
                                 {   'smiles': 'CC(=O)N([O-])CCC[C@H](N)C(=O)N[C@@H](CCCN([O-])C(C)=O)C(=O)N[C@@H](CCCN([O-])C(C)=O)C(=O)N[C@@H](CO)C(=O)N[C@H]([C@H](O)[C@H]1S[C@H]([C@H](O)[C@H]1O)n1ccc(=N)n(C)c1=O)C(O)=O',
                                     'name': 'desferrialbomycin epsilon(3-)',
                                     'reason': 'No or incomplete long chain '
                                               'fatty acid detected'},
                                 {   'smiles': 'OC[C@H]1O[C@H](O[C@@H]2[C@@H](CO)O[C@H](O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O',
                                     'name': 'alpha-maltotetraose',
                                     'reason': 'No or incomplete long chain '
                                               'fatty acid detected'}],
    'sample_false_negatives': [   {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '(19Z,22Z,25Z,28Z,31Z)-3-oxotetratriacontapentaenoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '3-oxopalmitoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '(13Z,16Z,19Z)-3-oxodocosatrienoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '3-oxodocosanoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '(14Z,17Z,20Z,23Z,26Z,29Z)-3-oxodotriacontahexaenoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)C[C@@H](O)CCCCCCCCCCCCCCCCCCCCC)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '(3S)-3-hydroxytetracosanoyl-CoA',
                                      'reason': 'No CoA moiety found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '3-oxotetracosanoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '2-hydroxytetracosanoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': '(13Z,16Z,19Z,22Z)-3-oxooctacosatetraenoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'},
                                  {   'smiles': 'CC(C)CCCC(C)CCCC(C)CCCC(C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                      'name': 'phytanoyl-CoA(4-)',
                                      'reason': 'Chiral hydroxyl group not in '
                                                'expected position'}],
    'attempt': 2,
    'reasoning': 'To properly classify the chemical class 11,12-saturated '
                 "fatty acyl-CoA(4-) based on the SMILES strings, it's "
                 'important to understand the core structural features of this '
                 'class. Analyzing the outcomes from the previous program '
                 'indicates that the failure was due to not detecting key '
                 'structural elements: the long chain fatty acid component '
                 'with specific unsaturations and the CoA moiety. '
                 'Additionally, there were no true positives indicating the '
                 'patterns used may not have been accurate or specific '
                 'enough.\n'
                 '\n'
                 'Key structural features to check:\n'
                 '1. **Long Chain Fatty Acid**: This should allow flexibility '
                 'for variations in chain lengths and positions of double '
                 'bonds.\n'
                 '2. **CoA Moiety**: The presence of the coenzyme A component '
                 'needs to be accurately identified.\n'
                 '3. **Stereochemistry and Hydroxyl Position**: Certain '
                 'hydroxyl groups and chiral centers play a crucial role in '
                 'identification.\n'
                 '\n'
                 'Steps to improve:\n'
                 '- Adjust the SMILES patterns to be more flexible and '
                 'descriptive of the variety seen in the examples.\n'
                 '- Ensure the recognition of varied lengths and '
                 'functionalities in the CoA moiety.\n'
                 '- Consider the presence of unsaturation sites allowing more '
                 'general patterns with possibly varied positions or count.\n'
                 '\n'
                 'Here is the updated program:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 31,
    'num_false_positives': 56,
    'num_true_negatives': 142175,
    'num_false_negatives': 38,
    'num_negatives': None,
    'precision': 0.3563218390804598,
    'recall': 0.4492753623188406,
    'f1': 0.39743589743589747,
    'accuracy': 0.9993394237526353,
    'negative_predictive_value': 0.999732795173437}