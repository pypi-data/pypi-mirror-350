"""
Classifies: CHEBI:64985 bioconjugate
"""
from rdkit import Chem

def is_bioconjugate(smiles: str):
    """
    Determines if a molecule is a bioconjugate based on its SMILES string.
    A bioconjugate consists of at least 2 biological molecules covalently linked together.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a bioconjugate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    try:
        # Define more comprehensive biological patterns (including more biologically relevant structures)
        amino_acid_pattern = Chem.MolFromSmarts("[NX3;H2,H1;!$(NC=O)][CX4][CX3](=O)[O,N,R]")
        peptide_linkage_pattern = Chem.MolFromSmarts("[NX3][CX3](=O)[NX3]")
        sugar_pattern = Chem.MolFromSmarts("OC[C@H]1O[C@@H](O)[C@H]([O,N])[C@H]1O")
        nucleotide_pattern = Chem.MolFromSmarts("n1cnc2c(ncnc12)")
        
        cofactor_patterns = [
            Chem.MolFromSmarts("CSCCC(=O)O"),  # General cofactor motif
            Chem.MolFromSmarts("COP(O)(=O)O")   # Phosphate-containing motif e.g., CoA
        ]
        
        # Covalent linkage patterns (e.g., amide, disulfide, thioester)
        amide_linkage_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[NX3][CX4]")
        disulfide_linkage_pattern = Chem.MolFromSmarts("[S][S]")
        thioester_linkage_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[SX2]")

        # Patterns for biological components
        bio_patterns = {
            "amino acid": amino_acid_pattern,
            "sugar": sugar_pattern,
            "nucleotide": nucleotide_pattern,
            "cofactor": cofactor_patterns
        }

        # Patterns for linkage types
        linkage_patterns = {
            "amide linkage": amide_linkage_pattern,
            "disulfide linkage": disulfide_linkage_pattern,
            "thioester linkage": thioester_linkage_pattern,
            "peptide linkage": peptide_linkage_pattern
        }

        # Checking detected biological components
        detected_bio_patterns = set()
        for name, pattern in bio_patterns.items():
            if isinstance(pattern, list):
                for p in pattern:
                    if p and mol.HasSubstructMatch(p):
                        detected_bio_patterns.add(name)
                        break
            elif pattern and mol.HasSubstructMatch(pattern):
                detected_bio_patterns.add(name)

        # Checking detected linkage types
        detected_link_patterns = set()
        for name, pattern in linkage_patterns.items():
            if pattern and mol.HasSubstructMatch(pattern):
                detected_link_patterns.add(name)

        # Decision: must have at least 2 biological components and 1 linkage type
        if len(detected_bio_patterns) >= 2 and len(detected_link_patterns) > 0:
            return True, f"Contains {len(detected_bio_patterns)} biological structures and {len(detected_link_patterns)} covalent link types"
        else:
            return False, f"Contains {len(detected_bio_patterns)} biological structures and {len(detected_link_patterns)} covalent link types. Requires at least 2 biological substructures with 1 linkage."

    except Exception as e:
        return None, f"Error in pattern matching: {e}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:64985',
                          'name': 'bioconjugate',
                          'definition': 'A molecular entity consisting of at '
                                        'least 2 biological molecules '
                                        'covalently linked together.',
                          'parents': ['CHEBI:50860'],
                          'xrefs': ['Wikipedia:Bioconjugate'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
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
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 2],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': ['MolFromSmarts', 'MolFromSmiles'],
                           'methods_called_count': 2,
                           'smarts_strings': [   '[CX3](=[OX1])[SX2]',
                                                 '[NX3][CX3](=O)[NX3]',
                                                 '[CX3](=[OX1])[NX3][CX4]',
                                                 'CSCCC(=O)O',
                                                 'COP(O)(=O)O',
                                                 '[NX3;H2,H1;!$(NC=O)][CX4][CX3](=O)[O,N,R]',
                                                 'OC[C@H]1O[C@@H](O)[C@H]([O,N])[C@H]1O',
                                                 '[S][S]',
                                                 'n1cnc2c(ncnc12)'],
                           'smarts_strings_count': 9,
                           'defs': ['is_bioconjugate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'None, "Invalid SMILES string"',
                                          'None, f"Error in pattern matching: '
                                          '{e}"'],
                           'returns_count': 2,
                           'complexity': 2.2664409020350407},
    'message': '\n'
               'Attempt failed: F1 score of 0.008403361344537815 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'N[C@@H](CCC(=O)N[C@@H](CSC(C#N)c1c[nH]c2ccccc12)C(O)=O)C(O)=O '
               'NAME: gammaGluCys(IAN) REASON: CORRECT Contains 2 biological '
               'structures and 1 covalent link types\n'
               'False positives: SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CS)[C@H]3O '
               "NAME: 3'-L-cysteinyl-AMP REASON: WRONGLY CLASSIFIED Contains 2 "
               'biological structures and 1 covalent link types\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=CC=C1)C(=O)OCC1=C(C)OC(=O)O1 '
               'NAME: lenampicillin REASON: WRONGLY CLASSIFIED Contains 2 '
               'biological structures and 2 covalent link types\n'
               ' * SMILES: '
               'S(C[C@H](N)C(=O)N(C(=O)CC[C@H](N)C(O)=O)CC(O)=O)C(CC(O)=O)C(O)=O '
               'NAME: S-(1,2-dicarboxyethyl)glutathione REASON: WRONGLY '
               'CLASSIFIED Contains 2 biological structures and 1 covalent '
               'link types\n'
               ' * SMILES: '
               '[H+].Cc1ccc(cc1)S([O-])(=O)=O.[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C(=O)OCOC(=O)[C@@H]1N2C(=O)C[C@@]2([H])S(=O)(=O)C1(C)C '
               'NAME: sultamicillin tosylate REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 2 covalent link types\n'
               ' * SMILES: S(CC(NC(=O)CCC(N)C(O)=O)C(O)=O)CC=C NAME: '
               'N-gamma-Glutamyl-S-allylcysteine REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC)C[C@H](N)C(O[C@@H](COP(OCC[N+](C)(C)C)([O-])=O)CO\\C=C\\CCCCCCCCCCCCCCCC)=O '
               'NAME: PC(P-18:0/LTE4) REASON: WRONGLY CLASSIFIED Contains 2 '
               'biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC([C@H](CC(C)C)N)=O)[C@H]3O '
               "NAME: 3'-L-leucyl-AMP REASON: WRONGLY CLASSIFIED Contains 2 "
               'biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'S(C[C@H](N)C(O[C@@H]1CC=2[C@@]([C@@H]3[C@H]([C@H]4[C@@]([C@H](CC4)[C@@H](CCCC(C)C)C)(CC3)C)CC2)(CC1)C)=O)[C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC '
               'NAME: CE(LTE4) REASON: WRONGLY CLASSIFIED Contains 2 '
               'biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'NC[C@H]1O[C@H](O[C@@H]2[C@@H](N)C[C@@H](NC(=O)[C@@H](O)CCNC(=O)CC[C@H](N)C(O)=O)[C@H](O)[C@H]2O[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)[C@H](N)[C@@H](O)[C@@H]1O '
               'NAME: gamma-L-glutamylbutirosin B REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: '
               '[H][C@]1(N[C@@H](C(O)=O)C(C)(C)S1)[C@H](NC(=O)[C@H](N)c1ccccc1)C(=O)NCCCC '
               'NAME: ampicilloyl-butylamine REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: S1C(NC(C1)C(=O)O)CCSCC(OCC)=O NAME: letosteine '
               'REASON: WRONGLY CLASSIFIED Contains 2 biological structures '
               'and 1 covalent link types\n'
               ' * SMILES: '
               'O1C(OC(C)=O)[C@H](O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-] '
               "NAME: 1''-O-acetyl-ADP-D-ribose(2-) REASON: WRONGLY CLASSIFIED "
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'CN(C)C1=NC=NC2=C1N=CN2C3[C@@H]([C@@H]([C@H](O3)CO)NC(=O)[C@H](CC4=CC=C(C=C4)OC)N)O '
               'NAME: '
               '(2S)-2-amino-N-[(2S,3S,4R)-5-[6-(dimethylamino)-9-purinyl]-4-hydroxy-2-(hydroxymethyl)-3-oxolanyl]-3-(4-methoxyphenyl)propanamide '
               'REASON: WRONGLY CLASSIFIED Contains 2 biological structures '
               'and 1 covalent link types\n'
               ' * SMILES: '
               'COc1cc2c(CCN[C@]22CS[C@H]3[C@H]4[C@@H]5N(C)[C@@H](Cc6cc(C)c(OC)c(O)c56)[C@H](O)N4[C@@H](COC2=O)c2c4OCOc4c(C)c(OC(C)=O)c32)cc1O '
               'NAME: trabectedin REASON: WRONGLY CLASSIFIED Contains 2 '
               'biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'O1C(O)[C@H](OC(CCC(=O)O)=O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)O)(=O)O '
               "NAME: 2''-O-succinyl-ADP-D-ribose REASON: WRONGLY CLASSIFIED "
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: '
               'S(C(CSCC(NC(=O)CCC(N)C(O)=O)C(O)=O)C)CC(NC(=O)CCC(N)C(O)=O)C(O)=O '
               "NAME: N,N'-Bis(g-glutamyl)-3,3'-(1,2-propylenedithio)dialanine "
               'REASON: WRONGLY CLASSIFIED Contains 2 biological structures '
               'and 1 covalent link types\n'
               ' * SMILES: S(CC(NC(=O)CCC(N)C(O)=O)C(O)=O)/C=C/C NAME: '
               'N-gamma-Glutamyl-S-(1-propenyl)cysteine REASON: WRONGLY '
               'CLASSIFIED Contains 2 biological structures and 1 covalent '
               'link types\n'
               ' * SMILES: '
               'CC[C@@H](C([O-])=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (S)-ethylmalonyl-CoA(5-) REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 2 covalent link types\n'
               ' * SMILES: '
               'N1=CN=C2C(=C1N)N=CN2C[C@H](OC[P@](N[C@H](C(OC(C)C)=O)C)(=O)OC3=CC=CC=C3)C '
               'NAME: tenofovir alafenamide REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: NCC(=O)SC[C@H](N)C(O)=O NAME: S-glycyl-L-cysteine '
               'REASON: WRONGLY CLASSIFIED Contains 2 biological structures '
               'and 1 covalent link types\n'
               ' * SMILES: '
               'O1C(O)[C@H](OC([C@H](C)O)=O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-] '
               "NAME: 2''-O-(S)-lactoyl-ADP-D-ribose(2-) REASON: WRONGLY "
               'CLASSIFIED Contains 2 biological structures and 1 covalent '
               'link types\n'
               ' * SMILES: '
               'S(C[C@H](N)C(O[C@@H](COP(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(O)=O)COC(=O)CCCCCCC/C=C\\C/C=C\\CCC)=O)[C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC '
               'NAME: PI(16:2(9Z,12Z)/LTE4) REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 1 covalent link types\n'
               ' * SMILES: S(=O)(CC(NC(=O)CCC(N)C(O)=O)C(O)=O)C NAME: '
               'gamma-Glutamyl-S-methylcysteine sulfoxide REASON: WRONGLY '
               'CLASSIFIED Contains 2 biological structures and 1 covalent '
               'link types\n'
               ' * SMILES: '
               'C([C@H](NC(CC[C@H](N)C(=O)O)=O)C(O)=O)S[C@H](\\C=C\\C=C\\C=C/C/C=C\\CCCCC)[C@@H](O)CCCC(=O)O '
               'NAME: leukotriene F4 REASON: WRONGLY CLASSIFIED Contains 2 '
               'biological structures and 1 covalent link types\n'
               ' * SMILES: S(CC(NC(=O)CCC(N)C(O)=O)C(O)=O)C NAME: '
               'gamma-Glutamyl-S-methylcysteine REASON: WRONGLY CLASSIFIED '
               'Contains 2 biological structures and 1 covalent link types\n'
               'False negatives: SMILES: S(SS(O)(=O)=O)C[C@H](N)C(O)=O NAME: '
               '3-(Sulfodisulfanyl)-L-alanine REASON: MISSED Contains 1 '
               'biological structures and 1 covalent link types. Requires at '
               'least 2 biological substructures with 1 linkage.\n'
               ' * SMILES: '
               'COc1cccc2[nH]cc(CSC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)c12 '
               'NAME: gammaGluCys(4MeOI3M)Gly REASON: MISSED Contains 1 '
               'biological structures and 1 covalent link types. Requires at '
               'least 2 biological substructures with 1 linkage.\n'
               ' * SMILES: S(=O)(CCCCNC(SC[C@H](N)C(O)=O)=S)C NAME: '
               'sulforaphane-cysteine REASON: MISSED Contains 2 biological '
               'structures and 0 covalent link types. Requires at least 2 '
               'biological substructures with 1 linkage.\n'
               ' * SMILES: N[C@@H](CSC(C#N)c1c[nH]c2ccccc12)C(O)=O NAME: '
               'L-Cys(IAN) REASON: MISSED Contains 2 biological structures and '
               '0 covalent link types. Requires at least 2 biological '
               'substructures with 1 linkage.\n'
               ' * SMILES: S(C[C@H](N)C(O)=O)C=1C=C(NC(=O)C)C=CC1O NAME: '
               '3-Cysteinylacetaminophen REASON: MISSED Contains 1 biological '
               'structures and 0 covalent link types. Requires at least 2 '
               'biological substructures with 1 linkage.\n'
               ' * SMILES: '
               'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\C/C=C\\CCC(O)=O '
               'NAME: '
               '16(S)-glutathionyl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
               'acid REASON: MISSED Contains 1 biological structures and 1 '
               'covalent link types. Requires at least 2 biological '
               'substructures with 1 linkage.\n'
               ' * SMILES: '
               'N[C@@H](CCC(=O)N[C@@H](CSC(C#N)c1c[nH]c2ccccc12)C(=O)NCC(O)=O)C(O)=O '
               'NAME: gammaGluCys(IAN)Gly REASON: MISSED Contains 1 biological '
               'structures and 1 covalent link types. Requires at least 2 '
               'biological substructures with 1 linkage.\n'
               ' * SMILES: S(C[C@H](N)C(O)=O)C=C NAME: S-vinylcysteine REASON: '
               'MISSED Contains 2 biological structures and 0 covalent link '
               'types. Requires at least 2 biological substructures with 1 '
               'linkage.\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: alpha-linolenoyl-CoA REASON: MISSED Contains 1 '
               'biological structures and 2 covalent link types. Requires at '
               'least 2 biological substructures with 1 linkage.\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CCCCCCCCCCCCCCC)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: palmitoyl-CoA REASON: MISSED Contains 1 biological '
               'structures and 2 covalent link types. Requires at least 2 '
               'biological substructures with 1 linkage.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C=2C(=C(O)C(CC=C(C)C)=C(OC)C2)C(=O)C(C3=CC=C(O)C=C3)=C1',
                                     'name': 'Gancaonin G',
                                     'reason': 'Contains 0 biological '
                                               'structures and 0 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'S(CC[C@H](N)C(=O)N[C@@H](CCC(=O)N)C(=O)N[C@@H](C(C)C)C(O)=O)C',
                                     'name': 'Met-Gln-Val',
                                     'reason': 'Contains 1 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@@H](O)O[C@H](CO)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O',
                                     'name': 'beta-D-Galp3S-(1->3-)-alpha-D-GalpNAc',
                                     'reason': 'Contains 0 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'CN(C)C(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@@H](CN2C(=O)NC3=CC(=CC=C3)OC)O',
                                     'name': '(3R,6aR,8R,10aR)-8-[2-(dimethylamino)-2-oxoethyl]-3-hydroxy-N-(3-methoxyphenyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Contains 0 biological '
                                               'structures and 2 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CC=CC=C4C#N)C5=CC=CC=C5N2C)[C@@H](C)CO',
                                     'name': 'LSM-9464',
                                     'reason': 'Contains 0 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'CC1=CC=CC=C1S(=O)(=O)N2C[C@@H](COC[C@H]3[C@H]2CC[C@@H](O3)CC(=O)NCC4=CC=CC=C4Cl)O',
                                     'name': '2-[(3S,6aR,8R,10aR)-3-hydroxy-1-(2-methylphenyl)sulfonyl-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[(2-chlorophenyl)methyl]acetamide',
                                     'reason': 'Contains 0 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)C(=O)C3=NC=CN=C3',
                                     'name': 'N-[(4S,7S,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-[oxo(2-pyrazinyl)methyl]-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'Contains 0 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'C1CCN(CC1)CCNC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@H](CN3S(=O)(=O)C4=CC=CC=C4)O',
                                     'name': '2-[(3S,6aS,8S,10aS)-1-(benzenesulfonyl)-3-hydroxy-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[2-(1-piperidinyl)ethyl]acetamide',
                                     'reason': 'Contains 0 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'OC1CC(N(C1)C(=O)C(N)CC2=CC=CC=C2)C(O)=O',
                                     'name': 'Phenylalanyl-Hydroxyproline',
                                     'reason': 'Contains 1 biological '
                                               'structures and 1 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'},
                                 {   'smiles': 'O([C@H]1O[C@@H]([C@H]([C@@H]([C@@H]1O)O)O)CO)CCC(CCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C)=O',
                                     'name': '1-(alpha-D-mannosyl)-3-keto-(1,27R)-octacosanediol',
                                     'reason': 'Contains 0 biological '
                                               'structures and 0 covalent link '
                                               'types. Requires at least 2 '
                                               'biological substructures with '
                                               '1 linkage.'}],
    'sample_false_negatives': [   {   'smiles': 'S(SS(O)(=O)=O)C[C@H](N)C(O)=O',
                                      'name': '3-(Sulfodisulfanyl)-L-alanine',
                                      'reason': 'Contains 1 biological '
                                                'structures and 1 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'COc1cccc2[nH]cc(CSC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)c12',
                                      'name': 'gammaGluCys(4MeOI3M)Gly',
                                      'reason': 'Contains 1 biological '
                                                'structures and 1 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'S(=O)(CCCCNC(SC[C@H](N)C(O)=O)=S)C',
                                      'name': 'sulforaphane-cysteine',
                                      'reason': 'Contains 2 biological '
                                                'structures and 0 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'N[C@@H](CSC(C#N)c1c[nH]c2ccccc12)C(O)=O',
                                      'name': 'L-Cys(IAN)',
                                      'reason': 'Contains 2 biological '
                                                'structures and 0 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'S(C[C@H](N)C(O)=O)C=1C=C(NC(=O)C)C=CC1O',
                                      'name': '3-Cysteinylacetaminophen',
                                      'reason': 'Contains 1 biological '
                                                'structures and 0 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\C/C=C\\CCC(O)=O',
                                      'name': '16(S)-glutathionyl-17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
                                              'acid',
                                      'reason': 'Contains 1 biological '
                                                'structures and 1 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'N[C@@H](CCC(=O)N[C@@H](CSC(C#N)c1c[nH]c2ccccc12)C(=O)NCC(O)=O)C(O)=O',
                                      'name': 'gammaGluCys(IAN)Gly',
                                      'reason': 'Contains 1 biological '
                                                'structures and 1 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'S(C[C@H](N)C(O)=O)C=C',
                                      'name': 'S-vinylcysteine',
                                      'reason': 'Contains 2 biological '
                                                'structures and 0 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': 'C(CCCC)[C@@H]([C@@H](\\C=C\\[C@H](C/C=C\\C/C=C\\CCCC(O)=O)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)O',
                                      'name': '11(S),15(S)-dihydroxy-14(R)-(S-glutathionyl)-5(Z),8(Z),12(E)-icosatrienoic '
                                              'acid',
                                      'reason': 'Contains 1 biological '
                                                'structures and 1 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'},
                                  {   'smiles': '[C@H]1([C@H]([C@H](CC1=O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)/C=C/[C@H](CCCCC)O)C/C=C\\CCCC(=O)O',
                                      'name': '(S)-PGA2-S-glutathione '
                                              'conjugate',
                                      'reason': 'Contains 1 biological '
                                                'structures and 1 covalent '
                                                'link types. Requires at least '
                                                '2 biological substructures '
                                                'with 1 linkage.'}],
    'attempt': 5,
    'reasoning': 'In the previous program, the main challenge was to correctly '
                 'identify bioconjugates based on their SMILES strings by '
                 'detecting biological substructures and linkage types. The F1 '
                 'score and specific outcomes indicated issues with false '
                 'positives and false negatives. Here are some hypotheses '
                 'about what might have gone wrong and how improvements can be '
                 'made:\n'
                 '\n'
                 '1. **SMILES Parsing and Pattern Matching:**\n'
                 '   - Ensure all provided SMILES are correctly parsed to '
                 'molecules.\n'
                 '   - Improve SMARTS patterns for specific biological '
                 'components.\n'
                 '   - Expand SMARTS patterns to cover more diverse biological '
                 'motifs.\n'
                 '\n'
                 '2. **Detection Logic for Biological Units:**\n'
                 '   - Refine the definition and detection of biological '
                 'entities.\n'
                 '   - Consider proteins/peptides, nucleic acids, and '
                 'cofactors as separate classes.\n'
                 '   - Include other biological substructures like lipids and '
                 'complex carbohydrates.\n'
                 '\n'
                 '3. **Covalent Linkage Types:**\n'
                 '   - Expand the types of covalent linkages recognized by the '
                 'program.\n'
                 '   - Adjust criteria such that multiple linkages match more '
                 'realistic bioconjugates.\n'
                 '\n'
                 '4. **Feedback from False Positives/Negatives:**\n'
                 '   - Analyze specific cases of false positives/negatives to '
                 'refine SMARTS patterns.\n'
                 '   - Create new patterns or refine existing ones to reduce '
                 'mismatches.\n'
                 '\n'
                 'Given this understanding, here is an improved attempt at the '
                 'program:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 9,
    'num_false_positives': 1663,
    'num_true_negatives': 140603,
    'num_false_negatives': 25,
    'num_negatives': None,
    'precision': 0.005382775119617225,
    'recall': 0.2647058823529412,
    'f1': 0.010550996483001172,
    'accuracy': 0.9881377371749824,
    'negative_predictive_value': 0.9998222260147339}