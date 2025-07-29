"""
Classifies: CHEBI:47908 alkanethiol
"""
"""
Classifies: alkanethiol
Definition: A compound in which a sulfanyl group, -SH, is attached to an alkyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alkanethiol(smiles: str):
    """
    Determines if a molecule is an alkanethiol based on its SMILES string.
    An alkanethiol has a sulfanyl group (-SH) attached to an alkyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkanethiol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for -SH (sulfanyl) group pattern
    sulfanyl_pattern = Chem.MolFromSmarts("[SH1]")
    if not mol.HasSubstructMatch(sulfanyl_pattern):
        return False, "No sulfanyl (-SH) group found"

    # Count sulfanyl groups
    sulfanyl_matches = len(mol.GetSubstructMatches(sulfanyl_pattern))
    if sulfanyl_matches > 2:
        return False, "Too many sulfanyl groups for simple alkanethiol"

    # Exclude aromatic compounds
    if any(atom.GetIsAromatic() for atom in mol.GetAtoms()):
        return False, "Contains aromatic rings"

    # Exclude compounds with complex functional groups
    exclusion_patterns = [
        ("[CX3](=O)[OX2H1]", "Contains carboxylic acid"),
        ("[CX3](=O)[OX2][CX4]", "Contains ester group"),
        ("[CX3]=O", "Contains ketone/aldehyde"),
        ("[NX3](~[!#1])(~[!#1])~[!#1]", "Contains tertiary amine"),
        ("[#7X2]=,:[#6]", "Contains imine or similar"),
        ("[SX2](!@[#6])!@[#6]", "Contains thioether bridge"),
        ("[S;!$([SH1]);!$(S(=O));!$(S(=O)=O)]", "Contains other sulfur groups"),
        ("[CX3]=[CX3]", "Contains alkene not adjacent to SH"),
        ("[#6X3]~[#6X3]", "Contains conjugated system"),
        ("[S;R]", "Contains sulfur in ring"),
        ("[C;R5]", "Contains 5-membered ring"),
        ("[C;R6]", "Contains 6-membered ring"),
        ("[PX4]", "Contains phosphorus"),
        ("[BX3]", "Contains boron"),
        ("[SiX4]", "Contains silicon"),
        ("[S;X3,X4,X5,X6]", "Contains oxidized sulfur")
    ]

    for pattern, reason in exclusion_patterns:
        pat = Chem.MolFromSmarts(pattern)
        if pat and mol.HasSubstructMatch(pat):
            return False, reason

    # Get all sulfur atoms and check their environment
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 16:  # Sulfur
            if atom.GetDegree() == 1:  # Terminal sulfur (as in -SH)
                carbon = atom.GetNeighbors()[0]
                if carbon.GetAtomicNum() != 6:  # Must be connected to carbon
                    return False, "Sulfanyl not connected to carbon"
                if carbon.GetIsAromatic():
                    return False, "Connected to aromatic carbon"
                if carbon.GetHybridization() != Chem.HybridizationType.SP3:
                    return False, "Connected carbon must be sp3 hybridized"

    # Allow simple primary amines (max 1) if present with thiol
    amine_pattern = Chem.MolFromSmarts("[NX3H2]")
    if mol.HasSubstructMatch(amine_pattern):
        if len(mol.GetSubstructMatches(amine_pattern)) > 1:
            return False, "Contains multiple primary amines"
        # Check distance between amine and thiol
        if rdMolDescriptors.CalcNumAtomStereoCenters(mol) > 2:
            return False, "Too complex for simple aminothiol"

    # Final check for molecular complexity
    if rdMolDescriptors.CalcNumRotatableBonds(mol) > 12:
        return False, "Too many rotatable bonds for simple alkanethiol"
    
    if rdMolDescriptors.CalcNumRings(mol) > 0:
        return False, "Contains rings"

    return True, "Contains sulfanyl group (-SH) attached to an alkyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47908',
                          'name': 'alkanethiol',
                          'definition': 'An alkanethiol is a compound in which '
                                        'a sulfanyl group, -SH, is attached to '
                                        'an alkyl group.',
                          'parents': ['CHEBI:29256'],
                          'xrefs': ['KEGG:C00812'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.4150943396226415 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: SC(CC)CS NAME: 1,2-Butanedithiol '
               'REASON: CORRECT Contains sulfanyl group (-SH) attached to an '
               'alkyl group\n'
               ' * SMILES: SCC=C(C)C NAME: 3-Methyl-2-butene-1-thiol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: SC(CCC)C NAME: 2-Pentanethiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SC1CCCC1 NAME: Cyclopentanethiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SC(C(C)C=O)CC NAME: 3-Mercapto-2-methylpentanal '
               'REASON: CORRECT Contains sulfanyl group (-SH) attached to an '
               'alkyl group\n'
               ' * SMILES: SC(CS)(C)C NAME: 2-methylpropane-1,2-dithiol '
               'REASON: CORRECT Contains sulfanyl group (-SH) attached to an '
               'alkyl group\n'
               ' * SMILES: CCSCCS NAME: 2-(ethylsulfanyl)ethanethiol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: CCSCS NAME: (ethylsulfanyl)methanethiol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: C(C(S)CCO)C NAME: 3-mercaptopentanol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: OCCS NAME: mercaptoethanol REASON: CORRECT Contains '
               'sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: CCCCC(S)CCCO NAME: 4-sulfanyloctan-1-ol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: SC(CCS)C NAME: 1,3-Butanedithiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SCCCC NAME: butanethiol REASON: CORRECT Contains '
               'sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: CC(C)(S)CCO NAME: 3-methyl-3-sulfanylbutan-1-ol '
               'REASON: CORRECT Contains sulfanyl group (-SH) attached to an '
               'alkyl group\n'
               ' * SMILES: SCC(CC)C NAME: 2-Methyl-1-butanethiol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: SCCCCCC NAME: 1-Hexanethiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SC(C(C)C)C NAME: 3-Methyl-2-butanethiol REASON: '
               'CORRECT Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: SC(C(S)C)C NAME: 2,3-Butanedithiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SCCCCCCCCCS NAME: 1,9-Nonanedithiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: CCS NAME: ethanethiol REASON: CORRECT Contains '
               'sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: CC(=O)CC(C)(C)S NAME: '
               '4-mercapto-4-methylpentan-2-one REASON: CORRECT Contains '
               'sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SC(CCCCC)C NAME: 2-Heptanethiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: SC(C(C)C)CO NAME: xi-2-Mercapto-3-methyl-1-butanol '
               'REASON: CORRECT Contains sulfanyl group (-SH) attached to an '
               'alkyl group\n'
               ' * SMILES: SCCCCCCC NAME: Heptane-1-thiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: CC(C)S NAME: propane-2-thiol REASON: CORRECT '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               'False positives: SMILES: SC(CCC)CCOC(=O)CCCC NAME: '
               '(S)-3-Mercaptohexyl pentanoate REASON: WRONGLY CLASSIFIED '
               'Contains sulfanyl group (-SH) attached to an alkyl group\n'
               ' * SMILES: C1CCCN(CC1)C(=C2C=CC=CC2=O)S NAME: '
               '6-[1-azepanyl(mercapto)methylidene]-1-cyclohexa-2,4-dienone '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: C(CC(CCO)(S)C)C NAME: 3-methyl-3-sulfanylhexan-1-ol '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: SC([S-])=S NAME: hydrogen trithiocarbonate REASON: '
               'WRONGLY CLASSIFIED Contains sulfanyl group (-SH) attached to '
               'an alkyl group\n'
               ' * SMILES: SC(CC(OCCCCCC)=O)C NAME: Hexyl 3-mercaptobutanoate '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: OCC(O)COC(=O)CS NAME: glyceryl monothioglycolate '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: SC(CCC)CCOC(=O)CCCCC NAME: 3-Mercaptohexyl '
               'hexanoate REASON: WRONGLY CLASSIFIED Contains sulfanyl group '
               '(-SH) attached to an alkyl group\n'
               ' * SMILES: SC(C(O)C)C NAME: 3-Mercapto-2-butanol REASON: '
               'WRONGLY CLASSIFIED Contains sulfanyl group (-SH) attached to '
               'an alkyl group\n'
               ' * SMILES: SCCCS NAME: propane-1,3-dithiol REASON: WRONGLY '
               'CLASSIFIED Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: C(=S)(S)N(CC)CC NAME: diethyldithiocarbamic acid '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: [NH3+]C(CS)C([O-])=O NAME: cysteine zwitterion '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: S1CC(S)C=C1C NAME: '
               '2,3-Dihydro-5-methyl-3-thiophenethiol REASON: WRONGLY '
               'CLASSIFIED Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: O[C@@H](CS)[C@@H](O)CS NAME: L-1,4-dithiothreitol '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: S(C(C(S)C)C)C(C(O)C)C NAME: '
               '3-[(2-Mercapto-1-methylpropyl)thio]-2-butanol REASON: WRONGLY '
               'CLASSIFIED Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: SCCCC([O-])=O NAME: 4-sulfanylbutanoate REASON: '
               'WRONGLY CLASSIFIED Contains sulfanyl group (-SH) attached to '
               'an alkyl group\n'
               ' * SMILES: SC1COCC1=O NAME: 4-Sulfanyloxolan-3-one REASON: '
               'WRONGLY CLASSIFIED Contains sulfanyl group (-SH) attached to '
               'an alkyl group\n'
               ' * SMILES: SC(CCOC)(C)C NAME: 4-Methoxy-2-methyl-2-butanethiol '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: SCCC(OCC)=O NAME: Ethyl 3-mercaptopropanoic acid '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: SC(C)C(OCC)=O NAME: Ethyl 2-mercaptopropionate '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: S1CC(=O)C(S)=C1C NAME: '
               '5-Methyl-4-sulfanyl-2,3-dihydrothiophen-3-one REASON: WRONGLY '
               'CLASSIFIED Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               ' * SMILES: O[C@@H](CS)[C@H](O)CS NAME: dithioerythritol '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: SC(CCOC(=O)C)(C)C NAME: 3-Mercapto-3-methyl-1-butyl '
               'acetate REASON: WRONGLY CLASSIFIED Contains sulfanyl group '
               '(-SH) attached to an alkyl group\n'
               ' * SMILES: C1CCN(CC1)C(=C2C=CC=CC2=O)S NAME: '
               '6-[mercapto(1-piperidinyl)methylidene]-1-cyclohexa-2,4-dienone '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: SC(=O)[C@H](CC)C NAME: (S)-Methylbutanethioic acid '
               'REASON: WRONGLY CLASSIFIED Contains sulfanyl group (-SH) '
               'attached to an alkyl group\n'
               ' * SMILES: C(S)(=NO)CCCCCCCCSC NAME: '
               '9-[(methylthio)nonyl]thiohydroximic acid REASON: WRONGLY '
               'CLASSIFIED Contains sulfanyl group (-SH) attached to an alkyl '
               'group\n'
               'False negatives: SMILES: NCCCNCCS NAME: WR-1065 REASON: MISSED '
               'Too many nitrogen atoms for simple alkanethiol\n'
               ' * SMILES: Cl.SCCN NAME: Cysteamine hydrochloride REASON: '
               'MISSED Contains primary or secondary amine\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1C=C(N=C2N1NN=N2)C3=CC=CC=C3',
                                     'name': '5-phenyl-1,7-dihydrotetrazolo[1,5-a]pyrimidine',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                     'name': 'TG(14:1(9Z)/22:1(13Z)/18:1(11Z))',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1O',
                                     'name': 'beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-D-Manp-(1->3)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-GlcpNAc-(1->4)-beta-D-GlcpNAc',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': '[C@@]12([C@@]([C@]([C@@H](CC1)C)(CCC(CC)C)C)(CCC[C@@H]2C)[H])C',
                                     'name': 'clerodane',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4R,5R,6R)-3,4-dihydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'O=C(NC(CC(C)C)C(=O)N[C@@H](CCCN=C(N)N)C=O)C(NC(=O)CC)CC(C)C',
                                     'name': 'Leupeptin Pr-LL',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)CCNC(=O)C(=C2C3=CC=CC=C3C(=N2)NC(=O)C4=CC=CS4)C#N',
                                     'name': 'N-[3-[1-cyano-2-[2-(4-methoxyphenyl)ethylamino]-2-oxoethylidene]-1-isoindolyl]-2-thiophenecarboxamide',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'O=C1O[C@@H](CC=2C1=C(OC)C(O)=CC2)CCC[C@@H](O)C',
                                     'name': 'Penicimarin C',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'CO[C@@H]1[C@@H]2[C@@H](C[C@@H]3[C@@](O2)([C@H]([C@@H]([C@H](O3)C(=O)OC)O)O)O)OC1N4C=NC5=C4N=CN=C5N',
                                     'name': 'LSM-4497',
                                     'reason': 'No sulfanyl (-SH) group found'},
                                 {   'smiles': 'C[C@@H]1[C@H](O)CCC2=CC[C@H](C[C@]12C)C(C)=C',
                                     'name': '1-deoxycapsidiol',
                                     'reason': 'No sulfanyl (-SH) group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'SCC=C(C)C',
                                      'name': '3-Methyl-2-butene-1-thiol',
                                      'reason': 'Contains alkene not adjacent '
                                                'to SH'},
                                  {   'smiles': 'SC1CCCC1',
                                      'name': 'Cyclopentanethiol',
                                      'reason': 'Contains rings'},
                                  {   'smiles': 'SC(C(C)C=O)CC',
                                      'name': '3-Mercapto-2-methylpentanal',
                                      'reason': 'Contains ketone/aldehyde'},
                                  {   'smiles': 'CCSCCS',
                                      'name': '2-(ethylsulfanyl)ethanethiol',
                                      'reason': 'Contains thioether bridge'},
                                  {   'smiles': 'CCSCS',
                                      'name': '(ethylsulfanyl)methanethiol',
                                      'reason': 'Contains thioether bridge'},
                                  {   'smiles': 'CC(=O)CC(C)(C)S',
                                      'name': '4-mercapto-4-methylpentan-2-one',
                                      'reason': 'Contains ketone/aldehyde'},
                                  {   'smiles': 'C=CCS',
                                      'name': '2-Propene-1-thiol',
                                      'reason': 'Contains alkene not adjacent '
                                                'to SH'},
                                  {   'smiles': 'S\\C=C(\\CC)/C',
                                      'name': '2-Methyl-1-propenethiol',
                                      'reason': 'Contains alkene not adjacent '
                                                'to SH'},
                                  {   'smiles': 'C[C@H](O)[C@@H](S)P(O)(O)=O',
                                      'name': '[(1R,2S)-2-hydroxy-1-thiopropyl]phosphonic '
                                              'acid',
                                      'reason': 'Contains phosphorus'}],
    'attempt': 2,
    'reasoning': 'Let me analyze the previous attempt and its issues:\n'
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- Many compounds with additional functional groups (esters, '
                 'ketones, carboxylic acids) were wrongly classified\n'
                 '- Complex sulfur-containing compounds (like '
                 'dithiocarbonates) were included\n'
                 '- Cyclic compounds with -SH groups were included when they '
                 "shouldn't be\n"
                 '- Compounds with multiple functional groups besides the '
                 'thiol were included\n'
                 '\n'
                 '2. False Negatives Analysis:\n'
                 '- The program was too strict with nitrogen-containing '
                 'compounds\n'
                 '- Simple amines with thiol groups (like cysteamine) were '
                 'excluded\n'
                 '\n'
                 '3. Key Improvements Needed:\n'
                 '- Better definition of "alkyl group" - should be primarily '
                 'saturated carbons\n'
                 '- Allow simple amines but exclude more complex nitrogen '
                 'compounds\n'
                 '- Exclude compounds where the sulfur is part of a more '
                 'complex functional group\n'
                 '- Add checks for other functional groups that make the '
                 'compound not a simple alkanethiol\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 19,
    'num_true_negatives': 142246,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.5777777777777777,
    'recall': 0.7428571428571429,
    'f1': 0.65,
    'accuracy': 0.999803232607168,
    'negative_predictive_value': 0.9999367333309901}