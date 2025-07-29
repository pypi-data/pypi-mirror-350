"""
Classifies: CHEBI:35910 2-oxo monocarboxylic acid
"""
"""
Classifies: CHEBI:35755 2-oxo monocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_oxo_monocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a 2-oxo monocarboxylic acid based on its SMILES string.
    A 2-oxo monocarboxylic acid has a single carboxylic acid group with a ketone group
    at the alpha position (2-oxo).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-oxo monocarboxylic acid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[OX2H1]")
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_pattern)
    
    if len(carboxylic_matches) == 0:
        return False, "No carboxylic acid group found"
    elif len(carboxylic_matches) > 1:
        return False, "Multiple carboxylic acid groups found"

    # Find the carboxylic acid carbon atom
    acid_carbon = carboxylic_matches[0][0]
    
    # Pattern for 2-oxo monocarboxylic acid - more specific than before
    alpha_keto_pattern = Chem.MolFromSmarts("[#6]-[CX3](=O)-[CX3](=O)[OX2H1]")
    matches = mol.GetSubstructMatches(alpha_keto_pattern)
    
    if not matches:
        return False, "No 2-oxo monocarboxylic acid pattern found"

    # Check that we found the same carboxylic acid carbon
    for match in matches:
        if match[3] == acid_carbon:
            # Get neighboring atoms of the alpha carbon (ketone carbon)
            alpha_carbon = match[1]
            alpha_neighbors = mol.GetAtomWithIdx(alpha_carbon).GetNeighbors()
            
            # Count number of ketone groups attached to alpha carbon
            ketone_count = 0
            for neighbor in alpha_neighbors:
                if neighbor.GetAtomicNum() == 8 and neighbor.GetTotalNumHs() == 0:
                    ketone_count += 1
            
            if ketone_count > 1:
                return False, "Multiple ketone groups on alpha carbon"

            # Check that the ketone is not part of a larger conjugated system
            conjugated_pattern = Chem.MolFromSmarts("[CX3](=O)-[CX3](=O)-[CX3]=O")
            if mol.HasSubstructMatch(conjugated_pattern):
                return False, "Ketone is part of a conjugated system"

            # Check that the ketone carbon is not part of a ring containing the acid
            ring_info = mol.GetRingInfo()
            if ring_info.NumAtomRings(alpha_carbon) > 0 and ring_info.NumAtomRings(acid_carbon) > 0:
                # Check if both atoms are in the same ring
                for ring in ring_info.AtomRings():
                    if alpha_carbon in ring and acid_carbon in ring:
                        return False, "Ketone and acid are part of the same ring"

            return True, "Contains a valid 2-oxo monocarboxylic acid pattern"

    return False, "No valid 2-oxo monocarboxylic acid pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35910',
                          'name': '2-oxo monocarboxylic acid',
                          'definition': 'Any monocarboxylic acid having a '
                                        '2-oxo substituent.',
                          'parents': ['CHEBI:35871'],
                          'xrefs': ['KEGG:C00161'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.610909090909091 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: O[C@H](COP(O)(O)=O)C(=O)C(O)=O NAME: '
               '(R)-3-hydroxy-2-oxo-4-phosphonooxybutanoic acid REASON: '
               'CORRECT Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: CC(C(=O)C(O)=O)c1c[nH]c2ccccc12 NAME: '
               '3-(indol-3-yl)-2-oxobutyric acid REASON: CORRECT Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)Cc1cc(c(O)c(c1)[N+]([O-])=O)[N+]([O-])=O '
               'NAME: 3,5-dinitro-4-hydroxyphenylpyruvic acid REASON: CORRECT '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: C(CCCCCCCC(C(=O)O)=O)CC NAME: 2-oxododecanoic acid '
               'REASON: CORRECT Contains a valid 2-oxo monocarboxylic acid '
               'pattern\n'
               ' * SMILES: '
               'CC(=O)N[C@H]([C@@H](O)CC(=O)C(O)=O)[C@@H](O)[C@H](O)[C@H](O)CO '
               'NAME: aceneuramic acid REASON: CORRECT Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: CC(O)CC(=O)C(O)=O NAME: 4-hydroxy-2-oxopentanoic '
               'acid REASON: CORRECT Contains a valid 2-oxo monocarboxylic '
               'acid pattern\n'
               ' * SMILES: CC[C@H](C)C(=O)C(O)=O NAME: '
               '(S)-3-methyl-2-oxovaleric acid REASON: CORRECT Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(CCCCN)=O NAME: 6-amino-2-oxohexanoic acid '
               'REASON: CORRECT Contains a valid 2-oxo monocarboxylic acid '
               'pattern\n'
               ' * SMILES: O[C@@H]1CC=C(CC(=O)C(O)=O)C=C1 NAME: '
               '(4R)-3,4-dihydro-4-hydroxyphenylpyruvic acid REASON: CORRECT '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: NCCCC(=O)C(O)=O NAME: 5-amino-2-oxopentanoic acid '
               'REASON: CORRECT Contains a valid 2-oxo monocarboxylic acid '
               'pattern\n'
               ' * SMILES: OC1=CC(CC(=O)C(O)=O)=CC(O)=C1O NAME: '
               '2-oxo-3-(3,4,5-trihydroxyphenyl)propanoic acid REASON: CORRECT '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: [C@@H]1(C=C[C@@H](CC1)CC(=O)C(=O)O)O NAME: '
               '3-[(1S,4R)-4-hydroxycyclohex-2-en-1-yl]pyruvic acid REASON: '
               'CORRECT Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(CCCNC(=N)N)=O NAME: '
               '5-guanidino-2-oxopentanoic acid REASON: CORRECT Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: CCC(=O)C(O)=O NAME: 2-oxobutanoic acid REASON: '
               'CORRECT Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: Nc1ccccc1C(=O)CC(=O)C(O)=O NAME: '
               '4-(2-aminophenyl)-2,4-dioxobutanoic acid REASON: CORRECT '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: [H]C(=CC(=O)C(O)=O)c1sc2ccccc2c1O NAME: '
               '4-(3-hydroxy-1-benzothiophen-2-yl)-2-oxobut-3-enoic acid '
               'REASON: CORRECT Contains a valid 2-oxo monocarboxylic acid '
               'pattern\n'
               ' * SMILES: C1C(C1CC(=O)C(O)=O)=C NAME: '
               'beta-(methylenecyclopropyl)pyruvic acid REASON: CORRECT '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)CC1=CNC2=CC=C(O)C=C12 NAME: '
               '3-(5-hydroxyindol-3-yl)pyruvic acid REASON: CORRECT Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)CS NAME: 3-mercaptopyruvic acid REASON: '
               'CORRECT Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)c1cc(O)cc(O)c1 NAME: '
               '3,5-dihydroxyphenylglyoxylic acid REASON: CORRECT Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC[C@@H](O)CC(=O)C(O)=O NAME: '
               '2-dehydro-3-deoxy-D-arabinonic acid REASON: CORRECT Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: NC(=O)NC(=O)C(O)=O NAME: oxaluric acid REASON: '
               'CORRECT Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: [C@@H]1(C=C[C@H](CC1)CC(=O)C(=O)O)O NAME: '
               '3-[(1R,4R)-4-hydroxycyclohex-2-en-1-yl]pyruvic acid REASON: '
               'CORRECT Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: C1=CC(=CC=C1CC(C(O)=O)=O)N NAME: '
               '3-(4-aminophenyl)pyruvic acid REASON: CORRECT Contains a valid '
               '2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: S(OC1=CC=C(CC(=O)C(O)=O)C=C1)(O)(=O)=O NAME: '
               '2-oxo-3-[4-(sulfooxy)phenyl]propanoic acid REASON: CORRECT '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               'False positives: SMILES: '
               'O[C@@H]1C=Cc2ccccc2[C@H]1SCC(=O)C(O)=O NAME: '
               '(1R,2R)-3-[(1,2-Dihydro-2-hydroxy-1-naphthalenyl)thio]-2-oxopropanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)CCP(O)(O)=O NAME: '
               '2-Oxo-4-phosphonobutanoate REASON: WRONGLY CLASSIFIED Contains '
               'a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: O[13C](=O)[13C](=O)[13CH3] NAME: Pyruvic-13C3 acid '
               'REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: OC[C@@H](O)[C@@H](O)[C@H](O)C(=O)C(O)=O NAME: '
               '2-dehydro-D-gluconic acid REASON: WRONGLY CLASSIFIED Contains '
               'a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)Cc1c[nH]c2ccc(OCc3ccccc3)cc12 NAME: '
               '3-(5-benzyloxyindol-3-yl)pyruvic acid REASON: WRONGLY '
               'CLASSIFIED Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: '
               'S1C(C(=O)C(=O)O)C2C(CC=CCC(O)CC=CC=CCC3C4(C(=C(C(C2C1)=O)C(=O)O4)O)CC(C)C(=C3)C)C '
               'NAME: Tetronothiodin REASON: WRONGLY CLASSIFIED Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: CC(=O)CC(=O)CC(=O)C(O)=O NAME: '
               '2,4,6-trioxoheptanoic acid REASON: WRONGLY CLASSIFIED Contains '
               'a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: '
               'N[C@H]([C@@H](O)CC(=O)C(O)=O)[C@@H](O)[C@H](O)[C@H](O)CO NAME: '
               'keto-neuraminic acid REASON: WRONGLY CLASSIFIED Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: CCCCCCCCCCCCCCC(=O)C(O)=O NAME: 2-oxohexadecanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: CCc1cccc(C)c1N([C@H](C)COC)C(=O)C(O)=O NAME: '
               '(R)-metolachlor OXA REASON: WRONGLY CLASSIFIED Contains a '
               'valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: O(C1=CC(O)=C(C=C1)C(=O)C(O)=O)C NAME: '
               '2-(2-hydroxy-4-methoxyphenyl)-2-oxoacetic acid REASON: WRONGLY '
               'CLASSIFIED Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: C(CCC(C(O)=O)=O)CCCCCCCC NAME: 2-oxo-tridecanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: OC[C@H](O)[C@H](O)[C@@H](O)C(=O)C(O)=O NAME: '
               '2-dehydro-L-gluconic acid REASON: WRONGLY CLASSIFIED Contains '
               'a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: O[C@H](COP(O)(O)=O)[C@@H](O)CC(=O)C(O)=O NAME: '
               '2-dehydro-3-deoxy-6-phospho-D-gluconic acid REASON: WRONGLY '
               'CLASSIFIED Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(C(CC([C@H](C)O)=O)=O)=O NAME: '
               '2,4-didehydro-3-deoxy-L-rhamnonic acid REASON: WRONGLY '
               'CLASSIFIED Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: '
               'C1=CC=C2C(=C1)C=CC(=N2)C(=CC3=CC(=CC=C3)Cl)C(=O)C(=O)O NAME: '
               '4-(3-chlorophenyl)-2-oxo-3-(2-quinolinyl)-3-butenoic acid '
               'REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: OCCC(=O)C(O)=O NAME: 4-Hydroxy-2-oxobutanoic acid '
               'REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: OCC(=O)CC(=O)C(O)=O NAME: '
               '5-hydroxy-2,4-dioxopentanoic acid REASON: WRONGLY CLASSIFIED '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: '
               'FC(F)(F)OC1=CC=C(C2=CC3=C(N(CC4=CC=CC=C4)C=C3C(=O)C(O)=O)C=C2)C=C1 '
               'NAME: Tiplasinin REASON: WRONGLY CLASSIFIED Contains a valid '
               '2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC(=O)C(=O)c1ccc(O)cc1 NAME: '
               '4-hydroxyphenylglyoxylic acid REASON: WRONGLY CLASSIFIED '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: CSCCCCC(=O)C(O)=O NAME: 2-Oxo-6-methylthiohexanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: CC(C)(CO)C(=O)C(O)=O NAME: 2-dehydropantoic acid '
               'REASON: WRONGLY CLASSIFIED Contains a valid 2-oxo '
               'monocarboxylic acid pattern\n'
               ' * SMILES: NC[C@H](O)CC(=O)C(O)=O NAME: '
               '2-Oxo-4-hydroxy-5-aminovalerate REASON: WRONGLY CLASSIFIED '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: C[C@H](O)[C@H](O)CC(=O)C(O)=O NAME: '
               '2-dehydro-3-deoxy-L-rhamnonic acid REASON: WRONGLY CLASSIFIED '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               ' * SMILES: OC[C@@H](O)[C@H](O)CC(=O)C(O)=O NAME: '
               '2-dehydro-3-deoxy-D-galactonic acid REASON: WRONGLY CLASSIFIED '
               'Contains a valid 2-oxo monocarboxylic acid pattern\n'
               'False negatives: SMILES: O(C(C1=CC=CC=C1)=C(OC)C(O)=O)C NAME: '
               'Dimethoxycinnamic acid REASON: MISSED No alpha-keto acid '
               'pattern found\n'
               ' * SMILES: O(C1=CC=C(CC(=O)C(OC)=O)C=C1)C NAME: Methyl '
               '3-(4-methoxyphenyl)-2-oxopropanoate REASON: MISSED No '
               'carboxylic acid group found\n'
               ' * SMILES: '
               '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1OC=C2C(=O)O[C@@H](C[C@]2([H])[C@H]1C=C)C(\\c1ccccc1)=C(\\O)C(O)=O '
               'NAME: Loniphenyruviridoside C REASON: MISSED No alpha-keto '
               'acid pattern found\n'
               ' * SMILES: O(C1=CC=C(C=C1)/C=C(\\O)/C(O)=O)C NAME: '
               '(2Z)-2-hydroxy-3-(4-methoxyphenyl)prop-2-enoic acid REASON: '
               'MISSED No alpha-keto acid pattern found\n'
               ' * SMILES: '
               'O(C(CC1=CC(O)=C(O)C=C1)C(O)=O)C(=O)/C=C/C2=CC(O)=C(O/C(=C\\C3=CC(O)=C(O)C=C3)/C(OC)=O)C=C2 '
               'NAME: Schizotenuin F REASON: MISSED No alpha-keto acid pattern '
               'found\n'
               ' * SMILES: '
               '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1OC=C2C(=O)O[C@H](C[C@@]2([H])[C@H]1C=C)C(\\c1ccccc1)=C(\\O)C(O)=O '
               'NAME: Loniphenyruviridoside B, (rel)- REASON: MISSED No '
               'alpha-keto acid pattern found\n'
               ' * SMILES: O(C=1C=C(C=CC1)/C=C(\\O)/C(O)=O)C NAME: '
               '(2Z)-2-hydroxy-3-(3-methoxyphenyl)prop-2-enoic acid REASON: '
               'MISSED No alpha-keto acid pattern found\n'
               ' * SMILES: C(C(O)CC=1C=C(C(=CC1)O)OC)(=O)O NAME: Vanillactic '
               'acid REASON: MISSED No alpha-keto acid pattern found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C(C1CC#CC#CC(OC(=O)C)C=C)CCCCCC=C',
                                     'name': 'Ginsenoyne F',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'OC(=O)C1=CC=C(N1)C(=O)NC1=C(O)C2=CC=C(O)C=C2OC1=O',
                                     'name': 'cacibiocin A',
                                     'reason': 'No 2-oxo monocarboxylic acid '
                                               'pattern found'},
                                 {   'smiles': 'S(OC)C(=O)C1=NC(C(SC)=O)=CC=C1',
                                     'name': '6-[(methoxythio)carbonyl]pyridine-2-monothiocarboxylic '
                                             'acid S-methyl ester',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'S1(=O)(=O)C(C(C(=O)[O-])C2C1CC2=O)(C)C.S1C(C(C(=O)[O-])N2C1C(NC(=O)C(N)C3=CC=CC=C3)C2=O)(C)C.[Na+].[Na+]',
                                     'name': 'Ampicillin Sodium Mixture With '
                                             'Sulbactam Sodium',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CN(C)C1=CC2=C(C=C1)O[C@H]3[C@@H]2C[C@@H](O[C@H]3CO)CC(=O)NCC4=CC=C(C=C4)OC',
                                     'name': '2-[(1S,3R,4aR,9aS)-6-(dimethylamino)-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(4-methoxyphenyl)methyl]acetamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC=3C=4C(NC3)=CC=CC4',
                                     'name': 'Trp-Trp-Ile',
                                     'reason': 'No 2-oxo monocarboxylic acid '
                                               'pattern found'},
                                 {   'smiles': '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)Oc1c[nH]c2ccc(Br)c(Cl)c12',
                                     'name': '5-bromo-4-chloro-3-indolyl '
                                             'beta-D-glucoside',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C[N+]1=CC=C(C=C1)C2=CC(=C(C=C2)O)OC',
                                     'name': '2-methoxy-4-(1-methyl-4-pyridin-1-iumyl)phenol',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CC(C)CN(C1CCS(=O)(=O)C1)C(=O)COC(=O)C2=CC3=C(S2)CCC3',
                                     'name': '5,6-dihydro-4H-cyclopenta[b]thiophene-2-carboxylic '
                                             'acid '
                                             '[2-[(1,1-dioxo-3-thiolanyl)-(2-methylpropyl)amino]-2-oxoethyl] '
                                             'ester',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)C)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Ala-Thr-Leu',
                                     'reason': 'No 2-oxo monocarboxylic acid '
                                               'pattern found'}],
    'sample_false_negatives': [   {   'smiles': 'O(C(C1=CC=CC=C1)=C(OC)C(O)=O)C',
                                      'name': 'Dimethoxycinnamic acid',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': 'O(C1=CC=C(CC(=O)C(OC)=O)C=C1)C',
                                      'name': 'Methyl '
                                              '3-(4-methoxyphenyl)-2-oxopropanoate',
                                      'reason': 'No carboxylic acid group '
                                                'found'},
                                  {   'smiles': '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1OC=C2C(=O)O[C@@H](C[C@]2([H])[C@H]1C=C)C(\\c1ccccc1)=C(\\O)C(O)=O',
                                      'name': 'Loniphenyruviridoside C',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': 'NC(=O)NC(=O)C(O)=O',
                                      'name': 'oxaluric acid',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': 'O(C1=CC=C(C=C1)/C=C(\\O)/C(O)=O)C',
                                      'name': '(2Z)-2-hydroxy-3-(4-methoxyphenyl)prop-2-enoic '
                                              'acid',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': 'O(C(CC1=CC(O)=C(O)C=C1)C(O)=O)C(=O)/C=C/C2=CC(O)=C(O/C(=C\\C3=CC(O)=C(O)C=C3)/C(OC)=O)C=C2',
                                      'name': 'Schizotenuin F',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1OC=C2C(=O)O[C@H](C[C@@]2([H])[C@H]1C=C)C(\\c1ccccc1)=C(\\O)C(O)=O',
                                      'name': 'Loniphenyruviridoside B, (rel)-',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': 'O(C=1C=C(C=CC1)/C=C(\\O)/C(O)=O)C',
                                      'name': '(2Z)-2-hydroxy-3-(3-methoxyphenyl)prop-2-enoic '
                                              'acid',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'},
                                  {   'smiles': 'C(C(O)CC=1C=C(C(=CC1)O)OC)(=O)O',
                                      'name': 'Vanillactic acid',
                                      'reason': 'No 2-oxo monocarboxylic acid '
                                                'pattern found'}],
    'attempt': 3,
    'reasoning': 'Let me analyze the issues with the previous code based on '
                 'the outcomes:\n'
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- The code is incorrectly classifying many compounds that '
                 "have similar patterns but aren't true 2-oxo monocarboxylic "
                 'acids\n'
                 '- Many of the false positives contain the alpha-keto acid '
                 'pattern but have additional ketone groups or other features '
                 'that should exclude them\n'
                 '- Some compounds like "2,4,6-trioxoheptanoic acid" have '
                 'multiple ketone groups but are still being classified as '
                 'positive\n'
                 '\n'
                 '2. False Negatives Analysis:\n'
                 '- The code is missing some valid 2-oxo monocarboxylic acids\n'
                 '- Some compounds with different resonance forms or tautomers '
                 'are being missed\n'
                 '- The SMARTS patterns may be too strict and not accounting '
                 'for all valid structural variations\n'
                 '\n'
                 "Here's my proposed solution approach:\n"
                 '\n'
                 '1. Improve the core pattern matching:\n'
                 '- Make the alpha-keto acid pattern more specific\n'
                 "- Ensure we're only matching the exact 2-oxo pattern we "
                 'want\n'
                 '- Add additional checks for the carbon connectivity\n'
                 '\n'
                 '2. Better exclusion rules:\n'
                 '- Add more specific checks for multiple ketone groups\n'
                 "- Improve detection of compounds that shouldn't be "
                 'classified as 2-oxo monocarboxylic acids\n'
                 '- Add checks for the relative position of the ketone group\n'
                 '\n'
                 '3. Handle special cases:\n'
                 '- Account for different resonance forms\n'
                 '- Better handle tautomers\n'
                 '- Consider stereochemistry where relevant\n'
                 '\n'
                 "Here's my improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 83,
    'num_false_positives': 84,
    'num_true_negatives': 142124,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.49700598802395207,
    'recall': 0.9021739130434783,
    'f1': 0.6409266409266409,
    'accuracy': 0.9993464511595221,
    'negative_predictive_value': 0.9999366790259827}