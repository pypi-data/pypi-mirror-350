"""
Classifies: CHEBI:73080 hemiaminal
"""
from rdkit import Chem

def is_hemiaminal(smiles: str):
    """
    Determines if a molecule is a hemiaminal based on its SMILES string.
    A hemiaminal has an amino group and a hydroxy group attached to the same carbon atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hemiaminal, False otherwise
        str: Reason for classification
    """
    
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return False, "Invalid SMILES string"
    
    # Define SMARTS pattern for hemiaminal (C bonded to OH and NH2)
    hemiaminal_pattern = Chem.MolFromSmarts("[CX4]([OH])([NH2])")
    
    # Check if the molecule matches the hemiaminal pattern
    if mol.HasSubstructMatch(hemiaminal_pattern):
        return True, "Contains a hemiaminal motif: C with OH and NH2 attached"
    else:
        return False, "No hemiaminal motif found"

# Example usage:
# result, reason = is_hemiaminal("OC(N)CC")
# print(f"Is hemiaminal: {result}, Reason: {reason}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:73080',
                          'name': 'hemiaminal',
                          'definition': 'Any organic amino compound that has '
                                        'an amino group and a hydroxy group '
                                        'attached to the same carbon atom. '
                                        'Hemiaminals are intermediates in the '
                                        'formation of imines by addition of an '
                                        'amine to an aldehyde or ketone; those '
                                        'derived from primary amines are '
                                        'particularly unstable.',
                          'parents': ['CHEBI:33822', 'CHEBI:50047'],
                          'xrefs': ['Wikipedia:Hemiaminal'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C1C2=C(OC(=C1)C)C3=C(OC)C=C(OC)C=C3C(=C2O)C4=C5OC(=CC(C5=C(O)C=6C4=CC(OC)=CC6OC)=O)C',
                                     'name': 'Isonigerone',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                     'name': '1-myristoyl-2-oleoyl-sn-glycero-3-phosphatidylglycerol(1-)',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'C(=C\\C/C=C\\CCCC(NC)=O)\\C/C=C\\C/C=C\\CCCCC',
                                     'name': 'N-methyl arachidonoyl amine',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'OC1(O)[C@]23N(CC1)C(N(O)[C@H]([C@@]3(N=C(N2)N)[H])CO)=N',
                                     'name': 'Decarbamoylneosaxitoxin',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'S([C@H]1N(C(=O)/C(=C\\C2=CC=C(OCC=C(C)C)C=C2)/N(C1=O)C)C)C',
                                     'name': 'Fusaperazine F',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'Oc1ccccc1I',
                                     'name': '2-iodophenol',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'O=C1N(CC(=O)N[C@H](C(=O)O[C@H]([C@@H](C(NC(C=C1)=C)=O)C)C(CCCCCCCCCCCCCC)C)C(O)C(=O)N)C',
                                     'name': 'Rakicidin H',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C',
                                     'name': 'Prenylterphenyllin F',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                     'reason': 'No hemiaminal motif found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'Gal2GlcNAc2Man3GlcNAcFucGlcNAc',
                                     'reason': 'No hemiaminal motif found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCOc1ccc2n3[C@H]4C[C@](O)(C(=O)OC)[C@](C)(O4)n4c5ccccc5c5c6CNC(=O)c6c(c2c1)c3c45',
                                      'name': 'KT 5926',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'C1[C@@]2(N3CC[C@@]42[C@]5(N(C=6C4=CC=CC6)C(C[C@]7([C@@]5([C@@]1(C(=CCO7)C3)[H])[H])[H])=O)[H])O',
                                      'name': 'pseudostrychnine',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'O=C1NC(=O)N(C1(C)C)CO',
                                      'name': '1-(hydroxymethyl)-5,5-dimethylhydantoin',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'NC(=O)C1=CN([C@H](O)CC1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](OP(O)(O)=O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O',
                                      'name': '(R)-NADPHX',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'N1[C@@]2([C@@]3(C4=C1C=CC=C4)[C@@H](C5[C@@H]([N+]6([C@]2(C[C@H]5[C@@H]([C@H]6O)CC)[H])C)C3)O)[H]',
                                      'name': '4-methylnorajmaline',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': '[H][C@@]12C[C@]3([H])N([C@H]4C[C@@]5([C@H](OC(C)=O)C14)c1ccccc1N=C35)[C@H](O)\\C2=C\\C',
                                      'name': 'vomilenine',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': '[H][C@@]12C[C@]3([H])N([C@H]4C[C@@]5([C@H](OC(C)=O)C14)c1ccccc1N[C@@]35[H])[C@H](O)\\C2=C\\C',
                                      'name': '1,2-dihydrovomilenine',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'C(CCCCCCCCCCC)(=O)N[C@H](C(O)=O)O',
                                      'name': 'N-dodecanoyl-(2S)-hydroxyglycine',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'COC(=O)[C@]1(C[C@H]2O[C@]1(C)n1c3ccccc3c3c4CN(C)C(=O)c4c4c5ccccc5n2c4c13)OC',
                                      'name': 'KT 5823',
                                      'reason': 'No hemiaminal motif found'},
                                  {   'smiles': 'O=C1N2[C@@]3([C@@]4([C@]5(N(CC4)C\\C(\\[C@](C5)([C@]3(CC1)[H])[H])=C\\CO)O)C=6C2=CC=CC6)[H]',
                                      'name': 'isopseudostrychnine',
                                      'reason': 'No hemiaminal motif found'}],
    'attempt': 0,
    'reasoning': 'To develop a program that classifies chemical entities as '
                 'hemiaminals based on their SMILES string, we need to create '
                 'a function `is_hemiaminal`. A hemiaminal is defined as a '
                 'compound with an amino group (NH2) and a hydroxy group (OH) '
                 'attached to the same carbon atom. Our task is to check for '
                 'this pattern in the provided SMILES structure using RDKit.\n'
                 '\n'
                 "Here's a step-by-step reasoning for implementing this:\n"
                 '\n'
                 '1. **Parse the SMILES string**: Convert the SMILES string '
                 'into an RDKit molecule object.\n'
                 '\n'
                 '2. **Define the SMARTS pattern for a hemiaminal**:\n'
                 '    - To identify a hemiaminal, look for a carbon atom (C) '
                 'that connects both an amino group (`[NH2]`) and a hydroxy '
                 'group (`[OH]`).\n'
                 '\n'
                 '3. **Search for the substructure match** using the SMARTS '
                 'pattern in the molecule created from the SMILES.\n'
                 '\n'
                 '4. **Output the result**: If any such carbon with both amino '
                 'and hydroxy groups is found, classify the molecule as a '
                 'hemiaminal.\n'
                 '\n'
                 "Let's write the program now:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 4,
    'num_true_negatives': 142270,
    'num_false_negatives': 23,
    'num_negatives': None,
    'precision': 0.42857142857142855,
    'recall': 0.11538461538461539,
    'f1': 0.18181818181818182,
    'accuracy': 0.9998102600140548,
    'negative_predictive_value': 0.999838361690315}