"""
Classifies: CHEBI:23437 cyanohydrin
"""
from rdkit import Chem

def is_cyanohydrin(smiles: str):
    """
    Determines if a molecule is a cyanohydrin based on its SMILES string.
    A cyanohydrin is an alpha-hydroxynitrile resulting from the formal addition of hydrogen cyanide to the C=O bond of an aldehyde or ketone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyanohydrin, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES to create a molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a SMARTS pattern for a carbon with attached hydroxyl group (OH) and nitrile group (C#N)
    # Exclude patterns that might encompass ring structures
    cyanohydrin_pattern = Chem.MolFromSmarts("[C;!R]([OH])([C]#[N])")

    # Check if molecule matches the cyanohydrin pattern
    if mol.HasSubstructMatch(cyanohydrin_pattern):
        return True, "Molecule contains the defining substructure of a cyanohydrin"
    else:
        return False, "No cyanohydrin substructure found in the molecule"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23437',
                          'name': 'cyanohydrin',
                          'definition': 'An alpha-hydroxynitrile resulting '
                                        'from the formal addition of hydrogen '
                                        'cyanide to the C=O bond of an '
                                        'aldehyde or ketone.',
                          'parents': ['CHEBI:22455'],
                          'xrefs': ['KEGG:C05712'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.45312500000000006 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C([C@@](O)(C)C#N)(C)(C)C NAME: '
               '(2S)-2-hydroxy-2-methyl-3,3-dimethylbutanenitrile REASON: '
               'CORRECT Molecule contains the defining substructure of a '
               'cyanohydrin\n'
               ' * SMILES: C1(=CC=CC=C1)C[C@H](O)C#N NAME: '
               '(2S)-2-hydroxy-3-phenylpropanenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C(C[C@@H](C#N)O)CCC NAME: '
               '(2S)-2-hydroxyheptanenitrile REASON: CORRECT Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: C=1C=C([C@@H](C#N)O)C=CC1OC NAME: '
               '(2S)-2-hydroxy-2-(4-methoxyphenyl)acetonitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: O[C@@H](C#N)c1ccccc1 NAME: (R)-mandelonitrile '
               'REASON: CORRECT Molecule contains the defining substructure of '
               'a cyanohydrin\n'
               ' * SMILES: CCC(C)(O)C#N NAME: 2-hydroxy-2-methylbutanenitrile '
               'REASON: CORRECT Molecule contains the defining substructure of '
               'a cyanohydrin\n'
               ' * SMILES: C1=C2OCOC2=CC(=C1)[C@H](O)C#N NAME: '
               '(2S)-2-(2H-1,3-benzodioxol-5-yl)-2-hydroxyacetonitrile REASON: '
               'CORRECT Molecule contains the defining substructure of a '
               'cyanohydrin\n'
               ' * SMILES: C(=C/[C@@H](C#N)O)\\CCC NAME: '
               '(2S,3E)-2-hydroxyhept-3-enenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: CC[C@@](C)(O)C#N NAME: '
               '(2R)-2-hydroxy-2-methylbutanenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C1([C@@H](C#N)O)CCCCC1 NAME: '
               '(2S)-2-cyclohexyl-2-hydroxyacetonitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: CC(C)(O)C#N NAME: 2-hydroxy-2-methylpropanenitrile '
               'REASON: CORRECT Molecule contains the defining substructure of '
               'a cyanohydrin\n'
               ' * SMILES: C=1(C=C([C@@H](C#N)O)C=CC1)OC NAME: '
               '(2S)-2-hydroxy-2-(3-methoxyphenyl)acetonitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C([C@@](O)(C)C#N)C(C)C NAME: '
               '(2S)-2-hydroxy-2,4-dimethylpentanenitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: CC[C@@H](C#N)O NAME: (2S)-2-hydroxybutanenitrile '
               'REASON: CORRECT Molecule contains the defining substructure of '
               'a cyanohydrin\n'
               ' * SMILES: C1=CC=CC=C1/C=C/[C@@H](C#N)O NAME: '
               '(2S,3E)-2-hydroxy-4-phenylbut-3-enenitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C(C[C@@H](C#N)O)CC NAME: '
               '(2S)-2-hydroxyhexanenitrile REASON: CORRECT Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: C=1([C@@](O)(C)C#N)C=CC=CC1 NAME: '
               '(2S)-2-hydroxy-2-phenylpropanenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: CC([C@@H](C#N)O)(C)C NAME: '
               '(2S)-2-hydroxy-3,3-dimethylbutanenitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C(C[C@@H](C#N)O)C NAME: '
               '(2S)-2-hydroxypentanenitrile REASON: CORRECT Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: C=1C=CSC1[C@H](O)C#N NAME: '
               '(2R)-2-hydroxy-2-(thiophen-2-yl)acetonitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C([C@@](O)(C)C#N)CC NAME: '
               '(2S)-2-hydroxy-2-methylpentanenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C(C[C@@H](C#N)O)CCCCCC NAME: '
               '(2S)-2-hydroxydecanenitrile REASON: CORRECT Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: C=1C(=C([C@@H](C#N)O)C=CC1)OC NAME: '
               '(2S)-2-hydroxy-2-(2-methoxyphenyl)acetonitrile REASON: CORRECT '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C([C@@](O)(C)C#N)CCCC NAME: '
               '(2S)-2-hydroxy-2-methylheptanenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: C1=CC=CC=C1CC[C@@H](C#N)O NAME: '
               '(2S)-2-hydroxy-4-phenylbutanenitrile REASON: CORRECT Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               'False positives: SMILES: '
               'OC[C@H]1O[C@@H](O[C@@H](C#N)c2ccccc2)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: (R)-prunasin REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: ClC1=CC(OCC#N)=CC(Cl)=C1 NAME: '
               '2-(3,5-Dichlorophenoxy)acetonitrile REASON: WRONGLY CLASSIFIED '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O[C@H](C2=CC=CC=C2)C#N)CO[C@@H]3OC[C@H](O)[C@H](O)[C@H]3O '
               'NAME: Vicianin REASON: WRONGLY CLASSIFIED Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'O(C(C(OC(=O)C)C(OC(=O)C)C#N)C(OC(=O)C)COC(=O)C)C(=O)C NAME: '
               '2,3-di(acetyloxy)-3-cyano-1-[1,2-di(acetyloxy)ethyl]propyl '
               'acetate REASON: WRONGLY CLASSIFIED Molecule contains the '
               'defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](O[C@H](C#N)C(=C)CO)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: Cardiospermin REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'ClC1(Cl)CC1(C(=O)OC(C#N)c1cccc(Oc2ccccc2)c1)c1ccccc1 NAME: '
               'cycloprothrin REASON: WRONGLY CLASSIFIED Molecule contains the '
               'defining substructure of a cyanohydrin\n'
               ' * SMILES: CC1(C)C(C=C(Cl)Cl)C1C(=O)OC(C#N)c1cccc(Oc2ccccc2)c1 '
               'NAME: cypermethrin REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](O[C@H](C#N)c2ccccc2)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: (S)-prunasin REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'O(C1C(O)C(O)C(OC1OC(C2=CC=CC=C2)C#N)CO)C3OCC(O)(C3O)CO NAME: '
               '(S)-2-Hydroxy-2-phenylacetonitrile '
               'O-[b-D-apiosyl-(1->2)-b-D-glucoside] REASON: WRONGLY '
               'CLASSIFIED Molecule contains the defining substructure of a '
               'cyanohydrin\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\CCCCCCCC)C(C(C)=C)C#N NAME: '
               'type iv cyanolipid 20:1(11z) ester REASON: WRONGLY CLASSIFIED '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'CC1(C)[C@@H](C=C(Br)Br)[C@H]1C(=O)O[C@H](C#N)c1cccc(Oc2ccccc2)c1 '
               'NAME: deltamethrin REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'CC1(C)[C@@H](C=C(Cl)Cl)[C@@H]1C(=O)O[C@@H](C#N)c1cccc(Oc2ccccc2)c1 '
               'NAME: (1S)-trans-(alphaR)-cypermethrin REASON: WRONGLY '
               'CLASSIFIED Molecule contains the defining substructure of a '
               'cyanohydrin\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1OC(CC)(C)C#N)COC2OC(C(O)C2O)CO '
               "NAME: 6'-Apiosyllotaustralin REASON: WRONGLY CLASSIFIED "
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: FC(F)(F)C=1C=CC(OCC#N)=NC1 NAME: '
               '2-{[5-(Trifluoromethyl)-2-pyridyl]oxy}acetonitrile REASON: '
               'WRONGLY CLASSIFIED Molecule contains the defining substructure '
               'of a cyanohydrin\n'
               ' * SMILES: '
               'CC1(C)[C@@H](\\C=C/C(=O)OC(C(F)(F)F)C(F)(F)F)[C@H]1C(=O)O[C@H](C#N)c1cccc(Oc2ccccc2)c1 '
               'NAME: acrinathrin REASON: WRONGLY CLASSIFIED Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: O=C(O)[C@@H](N)CCO[C@H](C#N)C1=CC(OC)=C(O)C(=C1)O '
               'NAME: Aleurodisconitrile REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'O1C(C1C2=CC=CC=C2)CC(OC(C3=CC4=C(C=C3)C=C(OC)C=C4)C#N)=O NAME: '
               'PHOME REASON: WRONGLY CLASSIFIED Molecule contains the '
               'defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC(C2=CC=C(O)C=C2)C#N)COC3OC(C(O)C(O)C3O)CO '
               "NAME: Dhurrin 6'-glucoside REASON: WRONGLY CLASSIFIED Molecule "
               'contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'CC(C)C(C(=O)OC(C#N)c1cccc(Oc2ccc(Br)cc2)c1)c1ccc(OC(F)F)cc1 '
               'NAME: ZXI 8901 REASON: WRONGLY CLASSIFIED Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'CC1(C)[C@H](C=C(Cl)Cl)[C@@H]1C(=O)O[C@@H](C#N)c1ccc(F)c(Oc2ccccc2)c1 '
               'NAME: (1S)-cis-(alphaR)-cyfluthrin REASON: WRONGLY CLASSIFIED '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'O(C1C(O)C(O)C(OC1OC(C2=CC=CC=C2)C#N)CO)C3OC(C(O)C(O)C3O)CO '
               'NAME: Mandelonitrile sophoroside REASON: WRONGLY CLASSIFIED '
               'Molecule contains the defining substructure of a cyanohydrin\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1OC(C2=CC=CC=C2)C#N)CO NAME: '
               '(S)-2-Hydroxy-2-phenylacetonitrile O-b-D-allopyranoside '
               'REASON: WRONGLY CLASSIFIED Molecule contains the defining '
               'substructure of a cyanohydrin\n'
               ' * SMILES: '
               'CC1(C)[C@@H](C=C(Cl)Cl)[C@@H]1C(=O)O[C@@H](C#N)c1ccc(F)c(Oc2ccccc2)c1 '
               'NAME: (1S)-trans-(alphaR)-cyfluthrin REASON: WRONGLY '
               'CLASSIFIED Molecule contains the defining substructure of a '
               'cyanohydrin\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC(C#N)c3ccccc3)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: amygdalin REASON: WRONGLY CLASSIFIED Molecule contains '
               'the defining substructure of a cyanohydrin\n'
               ' * SMILES: '
               'CC[C@@](C)(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)C#N '
               'NAME: Lotaustralin REASON: WRONGLY CLASSIFIED Molecule '
               'contains the defining substructure of a cyanohydrin\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1C2=C(OC(=C1)C)C3=C(OC)C=C(OC)C=C3C(=C2O)C4=C5OC(=CC(C5=C(O)C=6C4=CC(OC)=CC6OC)=O)C',
                                     'name': 'Isonigerone',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                     'name': '1-myristoyl-2-oleoyl-sn-glycero-3-phosphatidylglycerol(1-)',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'C(=C\\C/C=C\\CCCC(NC)=O)\\C/C=C\\C/C=C\\CCCCC',
                                     'name': 'N-methyl arachidonoyl amine',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'OC1(O)[C@]23N(CC1)C(N(O)[C@H]([C@@]3(N=C(N2)N)[H])CO)=N',
                                     'name': 'Decarbamoylneosaxitoxin',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'S([C@H]1N(C(=O)/C(=C\\C2=CC=C(OCC=C(C)C)C=C2)/N(C1=O)C)C)C',
                                     'name': 'Fusaperazine F',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'Oc1ccccc1I',
                                     'name': '2-iodophenol',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'O=C1N(CC(=O)N[C@H](C(=O)O[C@H]([C@@H](C(NC(C=C1)=C)=O)C)C(CCCCCCCCCCCCCC)C)C(O)C(=O)N)C',
                                     'name': 'Rakicidin H',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C',
                                     'name': 'Prenylterphenyllin F',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'Gal2GlcNAc2Man3GlcNAcFucGlcNAc',
                                     'reason': 'No cyanohydrin substructure '
                                               'found in the molecule'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'To improve the classification of cyanohydrins based on the '
                 'previous results, we need to address why certain structures '
                 'are being wrongly classified as cyanohydrins. The '
                 'cyanohydrin classification relies on recognizing a specific '
                 'substructure: a carbon atom attached to both a hydroxyl '
                 'group (OH) and a nitrile group (C≡N), typically forming as '
                 'an addition product with an aldehyde or ketone.\n'
                 '\n'
                 'In the previous implementation, the SMARTS pattern used to '
                 'identify cyanohydrins might have been too general, '
                 'potentially matching other substructures inadvertently. '
                 "Let's refine our approach to more accurately identify "
                 'cyanohydrins by considering:\n'
                 '\n'
                 '1. **Improving the SMARTS pattern**: Ensure it requires that '
                 'the hydroxyl and nitrile groups are bonded to the same '
                 'carbon atom. The stereo variations, while initially '
                 'considered, may have led to overmatching other irrelevant '
                 "structures. We'll also account more precisely for non-ring "
                 'structures as cyanohydrins generally form outside of ring '
                 'systems.\n'
                 '\n'
                 '2. **Considerations for common incorrect matches**: Examine '
                 'the underlying structural elements within molecules that '
                 'were mistakenly considered cyanohydrins. This adjustment '
                 'should prevent classifications in molecules with additional '
                 'large functional groups or complex steric profiles not '
                 'typical for simple cyanohydrins.\n'
                 '\n'
                 "Let's adjust the SMARTS pattern accordingly and check if it "
                 'aids in our classification task:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 29,
    'num_false_positives': 3,
    'num_true_negatives': 142268,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.90625,
    'recall': 1.0,
    'f1': 0.9508196721311475,
    'accuracy': 0.9999789177793394,
    'negative_predictive_value': 1.0}