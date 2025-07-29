"""
Classifies: CHEBI:46874 alpha-amino acid ester
"""
"""
Classifies: alpha-amino acid ester
Definition: The amino acid ester derivative obtained by the formal condensation 
of an alpha-amino acid with an alcohol.
An α‐amino acid typically has the structure H2N–CHR–COOH. Upon esterification, 
the –COOH is converted to –COOR. Here we search for a substructure corresponding to:
   N–αC–C(=O)O[*] 
with the refinements that (a) the nitrogen is not acylated (i.e. not an amide) and 
(b) the α‐carbon is either CH (one hydrogen) or CH2 (two hydrogens) so that glycine and 
substituted amino acids are both covered.
"""

from rdkit import Chem

def is_alpha_amino_acid_ester(smiles: str):
    """
    Determines if a molecule is an alpha-amino acid ester based on its SMILES string.
    This function looks for the motif:
        [NX3;!$(N-C(=O))]-[C;H1,H2]-[C](=O)O[*]
    which represents a (free) amino group attached to an alpha carbon (with one or two H's)
    that is further bound to a carbonyl carbon in an ester (C(=O)O-).
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule contains an alpha-amino acid ester motif, False otherwise.
        str: Reason for the classification.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define an improved SMARTS pattern:
    # - [NX3;!$(N-C(=O))] ensures the amino nitrogen is not immediately acylated.
    # - [C;H1,H2] requires the alpha carbon be either CH or CH2.
    # - [C](=O)O[*] looks for a carbonyl group that is esterified.
    aa_ester_smarts = "[NX3;!$(N-C(=O))]-[C;H1,H2]-[C](=O)O[*]"
    aa_ester_pattern = Chem.MolFromSmarts(aa_ester_smarts)
    if aa_ester_pattern is None:
        return False, "Error in SMARTS pattern"

    # Check if the molecule has at least one match to the defined alpha-amino acid ester motif.
    if not mol.HasSubstructMatch(aa_ester_pattern):
        return False, "No alpha-amino acid ester motif found"

    return True, "Contains an alpha-amino acid ester moiety"

# Example use (uncomment for testing):
# smiles_examples = [
#     "O(C(=O)C(N)C(OCC)=O)CC",      # Diethyl aminomalonate
#     "OC(=O)CN",                   # methyl glycinate
#     "CCCC",                       # negative test
# ]
# for smi in smiles_examples:
#     result, reason = is_alpha_amino_acid_ester(smi)
#     print(f"SMILES: {smi}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:46874',
                          'name': 'alpha-amino acid ester',
                          'definition': 'The amino acid ester derivative '
                                        'obtained the formal condensation of '
                                        'an alpha-amino acid with an alcohol.',
                          'parents': ['CHEBI:46668'],
                          'xrefs': ['KEGG:C03317'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 0],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': ['aa_ester_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_alpha_amino_acid_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error in SMARTS pattern"',
                                          'False, "No alpha-amino acid ester '
                                          'motif found"',
                                          'True, "Contains an alpha-amino acid '
                                          'ester moiety"'],
                           'returns_count': 4,
                           'complexity': 2.666440902035041},
    'message': '\n'
               'Attempt failed: F1 score of 0.1446700507614213 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: O(C(=O)C(N)C(OCC)=O)CC NAME: Diethyl '
               'aminomalonate REASON: CORRECT Contains an alpha-amino acid '
               'ester moiety\n'
               ' * SMILES: O(CC1=CC=CC=C1)C(=O)CN NAME: Benzyl glycinate '
               'REASON: CORRECT Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CCCNC(=N)N)[C@H]3O '
               "NAME: 3'-L-arginyl-AMP REASON: CORRECT Contains an alpha-amino "
               'acid ester moiety\n'
               ' * SMILES: COC(=O)C(N)Cc1ccc2nc(ccc2c1)-c1c(Cl)cccc1Cl NAME: '
               'methyl 3-[2-(2,6-dichlorophenyl)quinolin-6-yl]alaninate '
               'REASON: CORRECT Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1O[C@@H](C[C@@H](OC(=O)[C@@H](NC=O)C)CCCCCCC)[C@@H]1CCCCCCCC(C)C '
               'NAME: Panclicin A REASON: CORRECT Contains an alpha-amino acid '
               'ester moiety\n'
               ' * SMILES: '
               'COC1=CC=CC=C1C2=CC=C3[C@H]4[C@@H](CN3C2=O)[C@@H]([C@H](N4CC5CCCC5)C(=O)OC)CO '
               'NAME: '
               '(2S,3S,3aR,9bR)-1-(cyclopentylmethyl)-3-(hydroxymethyl)-7-(2-methoxyphenyl)-6-oxo-3,3a,4,9b-tetrahydro-2H-pyrrolo[2,3-a]indolizine-2-carboxylic '
               'acid methyl ester REASON: CORRECT Contains an alpha-amino acid '
               'ester moiety\n'
               ' * SMILES: '
               'O=C1N(C2(C(=O)OC2)C(C1(C)C)(O)C(CC(O)C3OC3C(O)CNC(=O)C(C(O)/C(=C\\C/C=C/C=C/C=C/C=4OC=NC4)/C)(C)C)C)C '
               'NAME: Oxazolepoxidomycin A REASON: CORRECT Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: COC(=O)C(N)Cc1ccc(cc1)[N+]([O-])=O NAME: methyl '
               '4-nitrophenylalaninate REASON: CORRECT Contains an alpha-amino '
               'acid ester moiety\n'
               ' * SMILES: O(C(C)(C)C)C(=O)N1CC(NCCC1)C(OCC)=O NAME: '
               '1-tert-Butyl 3-ethyl 1,4-diazepane-1,3-dicarboxylate REASON: '
               'CORRECT Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: CC1(OC(=O)C(C(=O)O1)NN=C2C=CC(=O)C=C2)C NAME: '
               'LSM-19443 REASON: CORRECT Contains an alpha-amino acid ester '
               'moiety\n'
               ' * SMILES: CCN(CC)CCNC(C1=CC=CC=C1)C(=O)OCCC(C)C NAME: '
               '2-[2-(diethylamino)ethylamino]-2-phenylacetic acid '
               '3-methylbutyl ester REASON: CORRECT Contains an alpha-amino '
               'acid ester moiety\n'
               ' * SMILES: [C@@H](C(OCC)=O)(CS)N.Cl NAME: Ethyl L-cysteine '
               'hydrochloride REASON: CORRECT Contains an alpha-amino acid '
               'ester moiety\n'
               ' * SMILES: '
               'O=C1C=2NC(C(=O)OC)(C)C(C2C34C(C3)CN(C4=C1)C(=O)C=5NC=6C(OC)=C(OC)C(=CC6C5)OC)=O '
               'NAME: Duocarmycin A REASON: CORRECT Contains an alpha-amino '
               'acid ester moiety\n'
               ' * SMILES: COC(=O)C(Cc1ccc(N)cc1)NC(=O)OC(C)(C)C NAME: methyl '
               '4-amino-N-(tert-butoxycarbonyl)phenylalaninate REASON: CORRECT '
               'Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: O=C1N[C@H](C(=O)OC(C(O)C)C)CC1 NAME: '
               "(3'-hydroxybutan-20-yl)5-oxopyrrolidine-2-carboxylate REASON: "
               'CORRECT Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CC=4C=CC(=CC4)O)[C@H]3O '
               "NAME: 3'-L-tyrosyl-AMP REASON: CORRECT Contains an alpha-amino "
               'acid ester moiety\n'
               ' * SMILES: '
               'C1C[C@H](N(C1)S(=O)(=O)C2=CC=CC=C2F)C(=O)OCC3=NC4=CC=CC=C4S3 '
               'NAME: (2S)-1-(2-fluorophenyl)sulfonyl-2-pyrrolidinecarboxylic '
               'acid 1,3-benzothiazol-2-ylmethyl ester REASON: CORRECT '
               'Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'CCOC(=O)NC1=CC2=C(C=C1)C(=CC(=O)O2)COC(=O)CNS(=O)(=O)C3=CC=C(C=C3)NC(=O)C '
               'NAME: 2-[(4-acetamidophenyl)sulfonylamino]acetic acid '
               '[7-(ethoxycarbonylamino)-2-oxo-1-benzopyran-4-yl]methyl ester '
               'REASON: CORRECT Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: COC(=O)CN NAME: methyl glycinate REASON: CORRECT '
               'Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: O=C1O[C@@H](C(=O)N([C@H]1CC2=CC=C(O)C=C2)C)C(C)C '
               'NAME: Cordycepamide E REASON: CORRECT Contains an alpha-amino '
               'acid ester moiety\n'
               ' * SMILES: '
               'COC1=C(C=C(C=C1)C(=O)COC(=O)CN2CC(=O)OC3=CC=CC=C32)Br NAME: '
               '2-(2-oxo-3H-1,4-benzoxazin-4-yl)acetic acid '
               '[2-(3-bromo-4-methoxyphenyl)-2-oxoethyl] ester REASON: CORRECT '
               'Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC([C@H](CC=4C=CC=CC4)N)=O)[C@H]3O '
               "NAME: 3'-L-phenylalanyl-AMP REASON: CORRECT Contains an "
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C(OC)[C@H]1N(N=CC=2OC(C=NN3[C@H](C(=O)OC)CCC3)=CC2)CCC1 '
               'NAME: Prolinimine B REASON: CORRECT Contains an alpha-amino '
               'acid ester moiety\n'
               ' * SMILES: '
               'C[C@@H](C(=O)OCN1C(=O)C2=CC=CC=C2N=N1)N3C(=O)C4CCCCC4C3=O '
               'NAME: '
               '(2S)-2-(1,3-dioxo-3a,4,5,6,7,7a-hexahydroisoindol-2-yl)propanoic '
               'acid (4-oxo-1,2,3-benzotriazin-3-yl)methyl ester REASON: '
               'CORRECT Contains an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CS)[C@H]3O '
               "NAME: 3'-L-cysteinyl-AMP REASON: CORRECT Contains an "
               'alpha-amino acid ester moiety\n'
               'False positives: SMILES: '
               'O=C1N(O)CCCCC1NC(=O)C(C(OC(=O)C(NC(=O)C2N=C(C3=C(O)C=CC=C3)OC2C)CCCCN(O)C(=O)/C=C\\CCCCCCCCCC(=O)O)CC)C '
               'NAME: Carboxymycobactin-7 REASON: WRONGLY CLASSIFIED Contains '
               'an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](NC(=O)[C@H](O)CO)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1[C@H](CC)C)=O)CC3=CC=CC=C3)C)=O)[C@H](CC)C)C2=O)OC)CCCN=C(N)N)C '
               'NAME: Micropeptin MZ859 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1OC(C(NC(=O)/C=C/C2=C(C=CC=C2)/C=C\\C)C(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)N3CCCC3C(NC(C(NC(C(NC(C(NC(C(NC1C(O)C(C)C)=O)CC(C)C)=O)O)=O)CC=4C5=C(C=CC=C5)NC4)=O)C(O)C6=CC=C(OC)C=C6)=O)C(O)C7=CC=CC=C7)C(C(=O)O)C)C)C '
               'NAME: RP-1776 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C(OC)[C@@H](NC(=O)C[C@@](O)(CC(=O)O[C@H]1[C@H](O)C([C@@H]2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4[C@@H](CC[C@@H](O)C(O)(C)C)C)C)C)(C)C)C)[C@@H](O)C5=CC=CC=C5 '
               'NAME: Pardinol C REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@H](NC(=O)[C@H](NC(=O)C(O)CC2=CC=C(O)C=C2)CCC(=O)N)C(=O)N[C@H](C(=O)N[C@H]3CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1[C@H](CC)C)=O)CC4=CC=CC=C4)C)=O)C(C)C)C3=O)O)CC5C=CC(O)CC5)C '
               'NAME: Micropeptin KB1046 REASON: WRONGLY CLASSIFIED Contains '
               'an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'S1SC[C@@H]2NC(=O)[C@H](NC(CC(OC([C@H](C1)NC2=O)=O)CCCCCCC)=O)CC3=CC=CC=C3 '
               'NAME: Sunshinamide REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C/1N[C@@H](C(=O)N[C@H](C(=O)O[C@H](C)[C@@H](C(N[C@H](C(N\\C1=C/C)=O)C)=O)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C=C(C)C)C(C)C)CC2=CC=C(O)C=C2)CC(C)C)CCC(=O)O '
               'NAME: Largamide A REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'CCCCCCCC(C)C\\C=C(C)\\C=C\\C(=O)C(C)CCC1OC(=O)[C@H](CC(OS(O)(=O)=O)C(N)=O)NC(=O)C(C)CNC(=O)C(=C)NCC1C '
               'NAME: Topostatin REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: CCOC(=O)[C@H](Cc1ccc(O)cc1)NC(C)=O NAME: ethyl '
               'N-acetyl-L-tyrosinate REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1N2C(OC(C2(CO)C)=O)(CC=3C1=C(O)C4=C5C(=O)C6=C(OC=7C=C(OC)C(=CC7C6=O)OC)C(C5=CC=C4C3)=O)C '
               'NAME: Citreamicin n REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1N[C@H](C(=O)N([C@H](C(=O)N[C@H](C(=O)N([C@@H]([C@H](OC)C)C(O[C@@H]([C@@H](C(O[C@@H](C(N(C1=C)C)=O)CC2=CC=CC=C2)=O)NC(=O)C)C)=O)C)[C@H](O)C(C)C)C)C)C '
               'NAME: '
               'N-[(2R,8S,11S,14S,17S,20R,21S)-2-benzyl-14-[(1R)-1-hydroxy-2-methylpropyl]-17-[(1R)-1-methoxyethyl]-4,8,10,11,16,20-hexamethyl-5-methylidene-3,6,9,12,15,18,22-heptaoxo-1,19-dioxa-4,7,10,13,16-pentazacyclodocos-21-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains an alpha-amino acid ester '
               'moiety\n'
               ' * SMILES: '
               'O=C1OC(CC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NCC(=O)N(C(C(=O)NC(C(NC(C(NC(C(NC(C(NC(C(NC(C(N(C1C(C)C)C)=O)CCCN)=O)CC=2C3=C(C=CC=C3)NC2)=O)CC(=O)N)=O)CCC(=O)O)=O)CCCN)=O)CC(C)C)CC4=CC=CC=C4)C)CO)C(O)C(=O)N)CO)CCCC(C)C '
               'NAME: WAP-8294A2 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O1C(=O)C2N(CCC2)C(=O)CCNC(=O)C(NC(=O)C(N(C(=O)C(N(C(=O)C1CC(C)C)C)C(C)C)C)C(C)C)CC3=CC=CC=C3 '
               'NAME: '
               '7-benzyl-11,14-dimethyl-16-(2-methylpropyl)-10,13-di(propan-2-yl)-17-oxa-1,5,8,11,14-pentazabicyclo[17.3.0]docosane-2,6,9,12,15,18-hexone '
               'REASON: WRONGLY CLASSIFIED Contains an alpha-amino acid ester '
               'moiety\n'
               ' * SMILES: '
               'O=[N+]([O-])/C(=C(/C=C/C=C\\C=C(/C(O)C(C(=O)NC/C=C/C=C/C(O)C(CC(OC)C1(O)C2(N(C)C(C1C)=O)C(=O)OC2C)C)(C)C)\\C)\\C)/C '
               'NAME: Lajollamycin REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCCCCCCCCCCC)CCCN)C(C)C)C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N2[C@H](C(N[C@H](C(N[C@H](C(N[C@H]1[C@H](CC)C)=O)CCCCN)=O)C(C)C)=O)CCC2)=O)[C@H](CC)C)=O)CO)CCCCN)C(C)C)CO)CCCN)C '
               'NAME: Paenibacterin REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1N(C(=O)[C@@H]2N(C(=O)[C@@H](N(C(=O)[C@@H](OC(=O)[C@@H](N(C(=O)C)C)CC(C)C)[C@H](CC)C)C)C(C)C)CCC2)[C@H](C(C)C)C(=C1)OC '
               'NAME: Mirabimide D REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               '[C@@]1(OC([C@]1(CCCCCC)[H])=O)(C[C@H](CCCCCCCCCCC)OC([C@@H](NC(=O)[H])CC(C)C)=O)[H] '
               'NAME: orlistat REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1OC(C(NC(=O)C(NC(=O)C2N(C(=O)CC)CCC2)CCC(=O)N)C(=O)NC(C(=O)NC3CCC(N(C(C(N(C(C(NC1CC(C)C)=O)CC4=CC=C(OC)C=C4)C)=O)CC(C)C)C3=O)O)CC(C)C)C '
               'NAME: Cyanopeptolin 1025 REASON: WRONGLY CLASSIFIED Contains '
               'an alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](NC(=O)CC)C(=O)N[C@H](C(=O)N2[C@@H](CCC2)C(N[C@H](C(N([C@H](C(N[C@H]1CC3=CC=C(O)C=C3)=O)CC4=CC=C(O)C=C4)C)=O)C(C)C)=O)C(C)C)C '
               'NAME: Petrosamide B REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1OC(CC(=O)N[C@H](CC(C)C)C(N[C@H](C(N[C@H]1CC(C)C)=O)CC(C)C)=O)CCCCCCCC '
               'NAME: Xefoampeptide E REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1OC(C(=O)N([C@H](C(=O)OC(C(=O)N([C@@H](C(=O)OC(C(N([C@H](C(OC(C(N([C@@H]1C)C)=O)CCCCC)=O)C)C)=O)CCCCC)C)C)CCCCC)C)C)CCCCCCC '
               'NAME: Verticilide A3 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1N(CC(=O)N([C@@H](C(=O)N2[C@H](C(=O)O[C@@H](CCC(=CCC(N[C@H]1CC3=CC=CC=C3)=O)C)CCC[C@H](OC)C)CCC2)CC(C)C)C)C '
               'NAME: Haprolid REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CC(C)C)C(N[C@H](C(N[C@H](C(N[C@@H](C(N[C@H]1C(CC)C)=O)CC(C)C)=O)CC(=O)O)=O)CC(C)C)=O)CC(C)C)CCC(=O)O)CCCCCCCCCC(C)C '
               'NAME: Pumilacidin A REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'O=C1N2C(OC(C2(CO)C)=O)(CC=3C1=C(O)C4=C5C(=O)C6=C(OC=7C=CC(=C(C7C6=O)O)OC)C(C5=CC=C4C3)=O)C '
               'NAME: Citreamicin delta REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               ' * SMILES: '
               'COC(=O)[C@@H](C1=CC=CC=C1)NC(=O)C2=CC(=NC3=CC=CC=C32)C4=CC=CC=C4 '
               'NAME: '
               '(2R)-2-[[oxo-(2-phenyl-4-quinolinyl)methyl]amino]-2-phenylacetic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Contains an '
               'alpha-amino acid ester moiety\n'
               'False negatives: SMILES: '
               'O=C1N(C(=NC2=C1C=CC=C2)[C@H](O)C(C)C)[C@@H]3C(=O)O[C@@]4(C3)C5=C(C=CC=C5)N6[C@H]4N(O)C(C)(C)C6=O '
               'NAME: Aspertoryadin C REASON: MISSED No alpha-amino acid ester '
               'motif found\n'
               ' * SMILES: '
               'O=C1N(C(=CC(=C1)OC)C)[C@H](C(=O)OC)CC=2C3=C(C=CC=C3)NC2 NAME: '
               'Calipyridone A REASON: MISSED No alpha-amino acid ester motif '
               'found\n'
               ' * SMILES: COC(=O)CN1C2=C(C=C(C=C2)F)SC1=NC(=O)C3=CC=C(S3)Cl '
               'NAME: '
               '2-[2-[(5-chloro-2-thiophenyl)-oxomethyl]imino-6-fluoro-1,3-benzothiazol-3-yl]acetic '
               'acid methyl ester REASON: MISSED No alpha-amino acid ester '
               'motif found\n'
               ' * SMILES: O=C(OC)[C@@H](N=[N+]([O-])/C=C\\CCCCCCCCCC(CC)C)C '
               'NAME: Azodyrecin B REASON: MISSED No alpha-amino acid ester '
               'motif found\n'
               ' * SMILES: '
               'O=C1N(C(=NC2=C1C=CC=C2)C(OC(=O)C)C(C)C)[C@@H]3C(=O)O[C@]4(C3)C(=O)NC5=C4C=CC=C5 '
               'NAME: Aspertoryadin F REASON: MISSED No alpha-amino acid ester '
               'motif found\n'
               ' * SMILES: CCOC(=O)CN1C=C(C2=CC=CC=C21)C=C[N+](=O)[O-] NAME: '
               '2-[3-(2-nitroethenyl)-1-indolyl]acetic acid ethyl ester '
               'REASON: MISSED No alpha-amino acid ester motif found\n'
               ' * SMILES: CC1=CC2=C(O1)C=C3N2C=NN(C3=O)CC(=O)OC NAME: '
               '2-(7-methyl-4-oxo-3-furo[3,4]pyrrolo[3,5-c][1,2,4]triazinyl)acetic '
               'acid methyl ester REASON: MISSED No alpha-amino acid ester '
               'motif found\n'
               ' * SMILES: '
               'CCOC(=O)CN1C2=C(C=C(C=C2)S(=O)(=O)NC3=C(C=CC(=C3)Cl)OC)OC1=O '
               'NAME: '
               '2-[6-[(5-chloro-2-methoxyphenyl)sulfamoyl]-2-oxo-1,3-benzoxazol-3-yl]acetic '
               'acid ethyl ester REASON: MISSED No alpha-amino acid ester '
               'motif found\n'
               ' * SMILES: '
               'O=C1N(C=NC2=C1C=CC=C2)[C@H]3C(=O)O[C@@]4(C3)C5=C(C=CC=C5)N6[C@H]4N(O)[C@@H](C)C6=O '
               'NAME: Tryptoquivaline H REASON: MISSED No alpha-amino acid '
               'ester motif found\n'
               ' * SMILES: C1=CC=C(C=C1)C2=NN(C3=CC=CC=C32)CC(=O)OC4=CC=CC=C4 '
               'NAME: 2-(3-phenyl-1-indazolyl)acetic acid phenyl ester REASON: '
               'MISSED No alpha-amino acid ester motif found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No alpha-amino acid ester '
                                               'motif found'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1N(C(=NC2=C1C=CC=C2)[C@H](O)C(C)C)[C@@H]3C(=O)O[C@@]4(C3)C5=C(C=CC=C5)N6[C@H]4N(O)C(C)(C)C6=O',
                                      'name': 'Aspertoryadin C',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C1O[C@@H](C[C@@H](OC(=O)[C@@H](NC=O)C)CCCCCCC)[C@@H]1CCCCCCCC(C)C',
                                      'name': 'Panclicin A',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C1N(C(=CC(=C1)OC)C)[C@H](C(=O)OC)CC=2C3=C(C=CC=C3)NC2',
                                      'name': 'Calipyridone A',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'COC(=O)CN1C2=C(C=C(C=C2)F)SC1=NC(=O)C3=CC=C(S3)Cl',
                                      'name': '2-[2-[(5-chloro-2-thiophenyl)-oxomethyl]imino-6-fluoro-1,3-benzothiazol-3-yl]acetic '
                                              'acid methyl ester',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C1N(C2(C(=O)OC2)C(C1(C)C)(O)C(CC(O)C3OC3C(O)CNC(=O)C(C(O)/C(=C\\C/C=C/C=C/C=C/C=4OC=NC4)/C)(C)C)C)C',
                                      'name': 'Oxazolepoxidomycin A',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C1C=2NC(C(=O)OC)(C)C(C2C34C(C3)CN(C4=C1)C(=O)C=5NC=6C(OC)=C(OC)C(=CC6C5)OC)=O',
                                      'name': 'Duocarmycin A',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'COC(=O)C(Cc1ccc(N)cc1)NC(=O)OC(C)(C)C',
                                      'name': 'methyl '
                                              '4-amino-N-(tert-butoxycarbonyl)phenylalaninate',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C1N[C@H](C(=O)OC(C(O)C)C)CC1',
                                      'name': "(3'-hydroxybutan-20-yl)5-oxopyrrolidine-2-carboxylate",
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C(OC)[C@@H](N=[N+]([O-])/C=C\\CCCCCCCCCC(CC)C)C',
                                      'name': 'Azodyrecin B',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'},
                                  {   'smiles': 'O=C1N(C(=NC2=C1C=CC=C2)C(OC(=O)C)C(C)C)[C@@H]3C(=O)O[C@]4(C3)C(=O)NC5=C4C=CC=C5',
                                      'name': 'Aspertoryadin F',
                                      'reason': 'No alpha-amino acid ester '
                                                'motif found'}],
    'attempt': 1,
    'reasoning': 'Below is our reasoning and then the code. We noticed that '
                 'the original SMARTS “[NX3]-[CX4]-[C](=O)O[*]” was too '
                 'narrow. Many valid α‐amino acid ester derivatives (including '
                 'glycine derivatives as well as substituted, stereo‐defined '
                 'examples) may present subtle differences in the α‐carbon '
                 'atom (it is sometimes CH2 as in glycine, or CH for '
                 'substituted amino acids) and the amino group should not be '
                 'in an amide bond (as occurs in peptides). Also, in many '
                 'false positives the pattern was “hit” in a more complex '
                 'peptide or macrocyclic framework. Therefore, we refined our '
                 'SMARTS to require a free (or non‐acylated) amino group '
                 'connected to an α‐carbon that has one or two hydrogens – '
                 'that is, it is either CH or CH2 – and then that same '
                 'α‐carbon is bound to a carboxyl group that is esterified. '
                 'Our revised SMARTS is:\n'
                 '\n'
                 '\u2003\u2003"[NX3;!$(N-C(=O))]-[C;H1,H2]-[C](=O)O[*]"\n'
                 '\n'
                 'This pattern now looks for an N atom (with three bonds) not '
                 'directly connected to a carbonyl (avoiding amides) followed '
                 'by a carbon with one or two hydrogens (covering both CH and '
                 'CH2, as in substituted amino acids or glycine) and finally a '
                 'carbonyl carbon bound to an oxygen that, in turn, is bound '
                 'to any atom (the ester function). We hope this increases '
                 'true positives while filtering out most of the false '
                 'positives observed. \n'
                 '\n'
                 'Below is the complete Python program using RDKit. \n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 109,
    'num_false_positives': 202,
    'num_true_negatives': 141862,
    'num_false_negatives': 127,
    'num_negatives': None,
    'precision': 0.3504823151125402,
    'recall': 0.461864406779661,
    'f1': 0.39853747714808047,
    'accuracy': 0.9976879831342235,
    'negative_predictive_value': 0.9991055645155611}