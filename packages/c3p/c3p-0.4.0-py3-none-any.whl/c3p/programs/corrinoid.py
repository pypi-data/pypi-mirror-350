"""
Classifies: CHEBI:33913 corrinoid
"""
from rdkit import Chem

def is_corrinoid(smiles: str):
    """
    Determines if a molecule is a corrinoid based on its SMILES string.
    A corrinoid typically contains a corrin macrocycle with cobalt.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a corrinoid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Corrin ring pattern is hard to capture in a singular SMARTS
    # We can check for cobalt and a large macrocycle as proxy
    cobalt_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'Co':
            cobalt_atom = atom
            break
    if not cobalt_atom:
        return False, "Cobalt atom not found"

    # Attempt to identify a macrocyclic ring structure (indicative of a corrin)
    # Corrin-specific patterns would make use of detailed SMARTS capturing the macrocycle
    # This is a simplified check to capture a large ring presence
    ri = mol.GetRingInfo()
    if not any(len(r) > 10 for r in ri.AtomRings()):
        return False, "No large macrocyclic ring found"

    return True, "Contains cobalt and large macrocyclic ring consistent with corrinoid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33913',
                          'name': 'corrinoid',
                          'definition': 'A derivative of the corrin nucleus, '
                                        'which contains four reduced or partly '
                                        'reduced pyrrole rings joined in a '
                                        'macrocycle by three =C- groups and '
                                        'one direct carbon-carbon bond linking '
                                        'alpha positions.',
                          'parents': ['CHEBI:36309'],
                          'xrefs': ['KEGG:C06021'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'P(OCC(OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCN(C)C)(O)=O',
                                     'name': 'Pe-nme2(20:3(5Z,8Z,11Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'O1[C@]2([C@@H](O)[C@H](O)[C@@H](O)[C@@]1(OCC[C@H](CCC=C(C(OC[C@]3(O)[C@@H](O)[C@@](OC3)(OC2)[H])=O)C)C)[H])[H]',
                                     'name': 'Urceolide',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'CC1=CC(=C(C=C1)C)C(=O)CSC2=NN=C(S2)C',
                                     'name': '1-(2,5-dimethylphenyl)-2-[(5-methyl-1,3,4-thiadiazol-2-yl)thio]ethanone',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'O=C1C=C([C@@]2(C(C[C@@H](C2)O)(C)C)C)CC[C@@]1(O)C',
                                     'name': 'Enokipodin H',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'CCCC[C@](Cn1cncn1)(C#N)c1ccc(Cl)cc1',
                                     'name': '(S)-myclobutanil',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)CCCCC)CC(=O)O)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1C(C)C)=O)CC3=CC=CC=C3)C)=O)CC(C)C)C2=O)O)CCCCN(C)C)C',
                                     'name': 'Cyanopeptolin D',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'O1[C@]2(O)N([C@H](C(=O)N3[C@]2(CCC3)[H])C(C)C)C(=O)[C@@]1(NC(=O)[C@H]4CN([C@]5(C(=C4)C6=C7C(C5)=CNC7=CC=C6)[H])C)C',
                                     'name': 'Ergovaline',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'OC(=O)CCCCCCC#CCCCC',
                                     'name': '8-tridecynoic acid',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'CC(=O)N([O-])CCC[C@H](N)C(=O)N[C@@H](CCCN([O-])C(C)=O)C(=O)N[C@@H](CCCN([O-])C(C)=O)C(=O)N[C@@H](CO)C(=O)N[C@H]([C@H](O)[C@H]1S[C@H]([C@H](O)[C@H]1O)n1ccc(=N)n(C)c1=O)C(O)=O',
                                     'name': 'desferrialbomycin epsilon(3-)',
                                     'reason': 'Cobalt atom not found'},
                                 {   'smiles': 'OC[C@H]1O[C@H](O[C@@H]2[C@@H](CO)O[C@H](O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O',
                                     'name': 'alpha-maltotetraose',
                                     'reason': 'Cobalt atom not found'}],
    'sample_false_negatives': [   {   'smiles': 'C=12C(=C3[N+]4=C(C=C5[N+]6=C(C(=C7N8[C@]([C@@H]([C@]7(CCC(NC[C@@H](C)O)=O)C)CC(N)=O)([C@]([N+]1[Co-3]846)([C@]([C@@H]2CCC(=O)N)(CC(=O)N)C)C)[H])C)[C@H](C5(C)C)CCC(=O)N)[C@H]([C@@]3(CC(=O)N)C)CCC(=O)N)C',
                                      'name': 'cobinamide',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': 'CC1OC(=O)C[C@@]2(C)[C@H](CCC(O)=O)C3=CC4=[N+]5C(=CC6=[N+]7C(=CC8=[N+]9C(=C(CC(O)=O)[C@@]8(C)CCC(O)=O)C12N3[Co--]579)C(CCC(O)=O)=C6CC(O)=O)[C@@H](CCC(O)=O)[C@]4(C)CC(O)=O',
                                      'name': 'cobalt(II)-factor IV',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': 'CC1=C2N3[C@H]([C@H](CC(N)=O)[C@@]2(C)CCC([O-])=O)[C@]2(C)[N+]4=C([C@@H](CCC(N)=O)[C@]2(C)CC(N)=O)C(C)=C2[N+]5=C(C=C6[N+](=C1[C@@H](CCC(N)=O)C6(C)C)[Co--]345C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc3c(N)ncnc13)[C@@H](CCC(N)=O)[C@]2(C)CC(N)=O',
                                      'name': 'adenosylcobyrate',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': '[H][C@@]12[C@H](CC(N)=O)[C@@](C)(CCC(=O)NC[C@@H](C)OP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c3nc(N)[nH]c4=O)C3=C(C)C4=[N+]5C(=CC6=[N+]7C(=C(C)C8=[N+]([C@]1(C)[C@@](C)(CC(N)=O)[C@@H]8CCC(N)=O)[Co--]57(C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc5c(N)ncnc15)N23)[C@@](C)(CC(N)=O)[C@@H]6CCC(N)=O)C(C)(C)[C@@H]4CCC(N)=O',
                                      'name': 'adenosylcobinamide guanosyl '
                                              'diphosphate',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': '[H][C@]12[C@H](CC(O)=O)[C@@](C)(CCC(O)=O)C3=[N+]1[Co--]14N5C(=CC6=[N+]1C(C[C@@]1(C)C(CC(O)=O)=C(CCC(O)=O)C(C3)=[N+]41)=C(CCC(O)=O)[C@]6(C)CC(O)=O)[C@@H](CCC(O)=O)[C@](C)(CC(O)=O)[C@]25C',
                                      'name': 'cobalt-precorrin-6B',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': '[H][C@@]12[C@H](CC(O)=O)[C@@](C)(CCC(O)=O)C3=C(C)C4=[N+]5C(=CC6=[N+]7C(=C(C)C8=[N+]([C@]1(C)[C@@](C)(CC(O)=O)[C@@H]8CCC(O)=O)[Co--]57N23)[C@@](C)(CC(N)=O)[C@@H]6CCC(O)=O)C(C)(C)[C@@H]4CCC(O)=O',
                                      'name': 'cob(II)yrinic acid c monoamide',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': 'CC(=O)C12N\\C(=C/C3=NC(Cc4[nH]c(CC5=NC1=C(CC(O)=O)[C@@]5(C)CCC(O)=O)c(CCC(O)=O)c4CC(O)=O)=C(CCC(O)=O)[C@]3(C)CC(O)=O)[C@@H](CCC(O)=O)[C@]2(C)CC(O)=O',
                                      'name': 'precorrin-4',
                                      'reason': 'Cobalt atom not found'},
                                  {   'smiles': '[H][C@]12N=C(C(C)C3=N[C@@](C)(CC4=C(CCC(O)=O)[C@](C)(CC(O)=O)C(/C=C5\\N[C@]1(C)[C@@](C)(CC(O)=O)[C@@H]5CCC(O)=O)=N4)C(C)=C3CCC(O)=O)[C@](C)(CCC(O)=O)[C@H]2CC(O)=O',
                                      'name': 'precorrin-7',
                                      'reason': 'Cobalt atom not found'},
                                  {   'smiles': 'C[C@@]1(CCC(O)=O)C(CC(O)=O)=C2[N+]3=C1CC1=[N+]4[C@@](C)(CC5=C(CCC(O)=O)[C@](C)(CC(O)=O)C6=[N+]5[Co--]34N3C(=C6)[C@@H](CCC(O)=O)[C@](C)(CC(O)=O)[C@]23C)C(CC(O)=O)=C1CCC(O)=O',
                                      'name': 'cobalt-precorrin-6A',
                                      'reason': 'No large macrocyclic ring '
                                                'found'},
                                  {   'smiles': '[H][C@]12[C@H](CC(O)=O)[C@@](C)(CCC(O)=O)C3=[N+]1[Co--]14N5C(=CC6=[N+]1C(C[C@@]1(C)C(C)=C(CCC(O)=O)C(C3C)=[N+]41)=C(CCC(O)=O)[C@]6(C)CC(O)=O)[C@@H](CCC(O)=O)[C@](C)(CC(O)=O)[C@]25C',
                                      'name': 'cobalt-precorrin-7',
                                      'reason': 'No large macrocyclic ring '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as corrinoids using their '
                 'SMILES strings, we will need to identify structural motifs '
                 'characteristic of corrinoids. Corrinoids are complex '
                 'compounds known for their unique corrin ring containing '
                 'cobalt.\n'
                 '\n'
                 'A defining feature of corrinoids is the presence of the '
                 'corrin macrocycle, which is similar to a porphyrin ring but '
                 'with fewer methine bridges, resulting in a more flexible '
                 'structure. Another key identifier is the presence of cobalt '
                 'in the corrin ring.\n'
                 '\n'
                 "Let's break down the steps needed to write the code:\n"
                 '\n'
                 "1. **Import Necessary Libraries:** We'll use RDKit, a "
                 'chemoinformatics toolkit, to parse the SMILES string and '
                 'search for substructures.\n'
                 '2. **Identify Key Functional Groups:**\n'
                 '   - Look for the presence of the corrin macrocycle. This is '
                 'a complex task, as the corrin macrocycle can vary slightly '
                 'in structure across different corrinoids.\n'
                 '   - Confirm the presence of cobalt within the macrocycle.\n'
                 "3. **Create a SMARTS pattern:** We'll attempt to define a "
                 "SMARTS pattern to identify the corrin structure and cobalt's "
                 'presence. This is a challenging task due to the variability '
                 'and complexity of the macrocycle.\n'
                 '\n'
                 'Due to the complex nature of corrinoids, we should be ready '
                 'to return `None` if the detection proves too difficult or if '
                 "the SMARTS pattern isn't sufficiently accurate across "
                 'different examples.\n'
                 '\n'
                 "Here's the Python program utilizing RDKit:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 19,
    'num_false_positives': 5,
    'num_true_negatives': 142255,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.7916666666666666,
    'recall': 0.475,
    'f1': 0.5937499999999999,
    'accuracy': 0.9998172874209417,
    'negative_predictive_value': 0.9998523995614158}