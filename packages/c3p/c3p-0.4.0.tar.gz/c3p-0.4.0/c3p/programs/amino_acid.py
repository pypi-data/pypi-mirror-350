"""
Classifies: CHEBI:33709 amino acid
"""
from rdkit import Chem

def is_amino_acid(smiles: str):
    """
    Determines if a molecule is an amino acid based on its SMILES string.
    An amino acid is defined as having at least one carboxylic acid group
    and at least one amino group within the same molecule, excluding polymeric chains.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classifiable as an amino acid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Pattern for an amino group
    amino_pattern = Chem.MolFromSmarts("[NX3;H2,H1]")
    
    # Pattern for a carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts("C(=O)[OH]")
    
    # Check for both amino and carboxyl patterns within the molecule
    has_amino = mol.HasSubstructMatch(amino_pattern)
    has_carboxyl = mol.HasSubstructMatch(carboxyl_pattern)
    
    if has_amino and has_carboxyl:
        # Ensure it is not part of a known peptide or polymeric structure by looking for peptide linkages
        peptide_bond_pattern = Chem.MolFromSmarts("C(=O)N[C]")
        if not mol.HasSubstructMatch(peptide_bond_pattern):
            return True, "Contains both amino and carboxylic acid groups without peptide linkages"
        else:
            return False, "Contains peptide bond indicative of polymers or peptide sequences"
    
    return False, "Missing amino or carboxylic acid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33709',
                          'name': 'amino acid',
                          'definition': 'A carboxylic acid containing one or '
                                        'more amino groups.',
                          'parents': ['CHEBI:33575', 'CHEBI:50047'],
                          'xrefs': ['Wikipedia:Amino_acid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 29,
                           'log_lines_of_code': 3.367295829986474,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'C(=O)[OH]',
                                                 'C(=O)N[C]',
                                                 '[NX3;H2,H1]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_amino_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains both amino and '
                                          'carboxylic acid groups without '
                                          'peptide linkages"',
                                          'False, "Contains peptide bond '
                                          'indicative of polymers or peptide '
                                          'sequences"',
                                          'False, "Missing amino or carboxylic '
                                          'acid group"'],
                           'returns_count': 4,
                           'complexity': 2.873459165997295},
    'message': '\n'
               'Attempt failed: F1 score of 0.14175152749490832 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: NC(CC1(C=CC(O)C=C1)C(O)=O)C(O)=O NAME: '
               'arogenic acid REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: NC(CC1=CC=C(CC(O)=O)C=C1)C(O)=O NAME: '
               '4-(carboxymethyl)phenylalanine REASON: CORRECT Contains amino '
               'acid backbone structure\n'
               ' * SMILES: N[C@@H](CCC(=O)NC1(O)CC1)C(O)=O NAME: coprine '
               'REASON: CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: CC(CCNC(N)=N)C(N)C(O)=O NAME: 3-methylarginine '
               'REASON: CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: NC[C@H](N)C(O)=O NAME: 3-amino-L-alanine REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: N[C@@H](CCS)C(O)=O NAME: L-homocysteine REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: OC(=O)[C@H]([C@@H](N)C(O)=O)C NAME: '
               'DL-threo-beta-Methylaspartate REASON: CORRECT Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               '[H][C@@](O)(CO)[C@@]([H])(O)[C@]([H])(O)C(=O)CNCC(O)=O NAME: '
               'fructosylglycine REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: N[C@@H](CCC(=O)NNc1ccc(CO)cc1)C(O)=O NAME: '
               'agaritine REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: N[C@H]([C@@H](O)[C@@H](O)[C@H](O)CO)C(O)=O NAME: '
               'D-galactosaminic acid REASON: CORRECT Contains amino acid '
               'backbone structure\n'
               ' * SMILES: O=C(O)[C@@H](N)CC[N+]([O-])=NO NAME: Homoalanosine '
               'REASON: CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: C\\C(CO)=C/CNc1ncnc2n(C[C@H](N)C(O)=O)cnc12 NAME: '
               'L-lupinic acid REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: '
               'C(\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\CC)O)SC[C@H](N)C(O)=O)=C\\C/C=C\\CCC(O)=O '
               'NAME: '
               '16(S)-cystein-S-yl,17(R)-hydroxy-(4Z,7Z,10,12,14,19Z)-docosahexaenoic '
               'acid REASON: CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: '
               '[H][C@@]1(N\\C(N[C@]1([H])C(O)=O)=N/[C@@H]1O[C@H](CO)[C@H](OC(N)=O)[C@@H](O)[C@H]1NC(=O)C[C@@H](N)CCCN)[C@H](O)CN '
               'NAME: streptothricin F acid REASON: CORRECT Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'C(/C=C\\CCCCC)[C@H](C/C=C/C=C/[C@H]([C@@H](O)CCCC(=O)O)SC[C@H](N)C(=O)O)O '
               'NAME: (12R)-hydroxy-10,11-dihydroleukotriene E4 REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: '
               'NC(=O)CC[C@H](NC[C@@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: mannopine REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: N[C@@H](CC1=CC=C(OP(O)(O)=O)C(O)=C1)C(O)=O NAME: '
               'foslevodopa REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: COC1=CC=C(C[C@H](N)C(O)=O)C=C1O NAME: '
               '4-O-methyl-L-dopa REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: '
               'CC1(C)C[C@@H]1C(=O)N\\C(C(O)=O)=C/CCCCSC[C@H](N)C(O)=O NAME: '
               'cilastatin REASON: CORRECT Contains amino acid backbone '
               'structure\n'
               ' * SMILES: CC(C)(CCO)SC[C@H](N)C(O)=O NAME: felinine REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: NC(CCCNC(N)=O)C(O)=O NAME: citrulline REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: N[C@@H](CONC(N)=O)C(O)=O NAME: O-ureido-L-serine '
               'REASON: CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: Cn1cnc(S)c1C[C@H](N)C(O)=O NAME: ovothiol A REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: [H]C(=O)[C@H](N)C(O)=O NAME: L-3-oxoalanine REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               ' * SMILES: OC1CCNC1C(O)=O NAME: 3-hydroxyproline REASON: '
               'CORRECT Contains amino acid backbone structure\n'
               'False positives: SMILES: '
               'O=C(NCC(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CCCN=C(N)N NAME: '
               'Ser-Arg-Gly REASON: WRONGLY CLASSIFIED Contains amino acid '
               'backbone structure\n'
               ' * SMILES: '
               'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CC)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CCCN=C(N)N)C '
               'NAME: [D-Asp3]MC-RAba REASON: WRONGLY CLASSIFIED Contains '
               'amino acid backbone structure\n'
               ' * SMILES: OC(=O)CCC(NC(=O)Cc1ccc(O)cc1)C(O)=O NAME: '
               'N-4-hydroxyphenylacetylglutamic acid REASON: WRONGLY '
               'CLASSIFIED Contains amino acid backbone structure\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCCCN)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O '
               'NAME: Lys-Cys-His REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: SC[C@H](NC(=O)[C@@H](N)CCCCN)C(=O)N[C@@H](CS)C(O)=O '
               'NAME: Lys-Cys-Cys REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)C)CCC(=O)N)C(O)=O)C '
               'NAME: Ala-Gln-Thr REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@H]2NCCC2 '
               'NAME: Pro-Gln-Phe REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC=1NC=NC1)C(=O)N[C@@H](CC2=CC=CC=C2)C(O)=O)[C@@H](N)CC=3C=4C(NC3)=CC=CC4 '
               'NAME: Trp-His-Phe REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O[C@@H]([C@H](NC(=O)[C@@H](N)CCCCN)C(=O)N[C@@H]([C@H](O)C)C(O)=O)C '
               'NAME: Lys-Thr-Thr REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(C)C '
               'NAME: Asn-Leu-Asn REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)CC(C)C '
               'NAME: Leu-Glu-Gln REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](N)[C@H](O)C)[C@@H](O)C1=CC=CC=C1)CC(C)C)C(C)C)[C@H]2NC(=NCC2)N)[C@H](O)C '
               'NAME: Faulknamycin REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)C(=O)N[C@@H](CC2=CC=C(O)C=C2)C(O)=O)C '
               'NAME: Phe-Met-Tyr REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: C(C(=O)NP(O)(=O)O)C[C@@H](C(=O)O)N NAME: '
               'N(5)-phospho-L-glutamine REASON: WRONGLY CLASSIFIED Contains '
               'amino acid backbone structure\n'
               ' * SMILES: '
               'ClCCCCCCCC(N)C(O)C(=O)NC(C(=O)N1C(C(=O)NC(C(=O)O)CC2=CC=C(O)C=C2)CCC1)C(O)C '
               'NAME: Microginin 598 REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CC(=O)N)C(=O)N[C@@H](CCCCN)C(O)=O NAME: '
               'Asn-Cys-Lys REASON: WRONGLY CLASSIFIED Contains amino acid '
               'backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC=1C=2C(NC1)=CC=CC2 '
               'NAME: Arg-Trp-Arg REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)C '
               'NAME: His-Ala-Gln REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: OC(=O)C(NC(=O)CN)CCCC NAME: glycyl-DL-norleucine '
               'REASON: WRONGLY CLASSIFIED Contains amino acid backbone '
               'structure\n'
               ' * SMILES: '
               'OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CO)C)CC(C)C NAME: '
               'Ser-Ala-Leu REASON: WRONGLY CLASSIFIED Contains amino acid '
               'backbone structure\n'
               ' * SMILES: OC(=O)[C@@H](N)CCCC[N+](C)(C)C NAME: '
               'N(6),N(6),N(6)-trimethyl-L-lysine REASON: WRONGLY CLASSIFIED '
               'Contains amino acid backbone structure\n'
               ' * SMILES: O=C(N[C@@H](CO)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)C '
               'NAME: Ser-Ala-Ser REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CCCCN '
               'NAME: Ser-Lys-Ala REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC1=CC=C(O)C=C1 '
               'NAME: Asn-Tyr-Gln REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N[C@@H](CCCCN)C(O)=O)CC(O)=O)[C@@H](N)[C@H](CC)C '
               'NAME: Ile-Asp-Lys REASON: WRONGLY CLASSIFIED Contains amino '
               'acid backbone structure\n'
               'False negatives: SMILES: NCCC[C@H](N)CC(O)=O NAME: '
               '(3S)-3,6-diaminohexanoic acid REASON: MISSED No amino acid '
               'backbone structure found\n'
               ' * SMILES: NC(=C)C(O)=O NAME: 2-aminoacrylic acid REASON: '
               'MISSED No amino acid backbone structure found\n'
               ' * SMILES: N\\C(=C\\C=C/C(O)=O)C(O)=O NAME: '
               '(2E,4Z)-2-aminomuconic acid REASON: MISSED No amino acid '
               'backbone structure found\n'
               ' * SMILES: C(N(C(=[NH2+])NC)O)CC[C@@H](C(=O)[O-])[NH3+] NAME: '
               'N(delta)-hydroxy-N(omega)-methyl-L-argininium REASON: MISSED '
               'No amino acid backbone structure found\n'
               ' * SMILES: Nc1cccc(c1)C(O)=O NAME: 3-aminobenzoic acid REASON: '
               'MISSED No amino acid backbone structure found\n'
               ' * SMILES: OC(=O)COC(=O)Cc1ccccc1Nc1c(Cl)cccc1Cl NAME: '
               'aceclofenac REASON: MISSED No amino acid backbone structure '
               'found\n'
               ' * SMILES: CNC(=O)c1ccccc1N NAME: N-Methylanthranilamide '
               'REASON: MISSED Contains peptide bond indicative of polymers or '
               'peptide sequences\n'
               ' * SMILES: OCCN(CC(O)=O)CC(O)=O NAME: '
               'N-(2-hydroxyethyl)iminodiacetic acid REASON: MISSED No amino '
               'acid backbone structure found\n'
               ' * SMILES: OC(=O)C1=C(N)C=C(C=C1)C NAME: '
               '2-Amino-4-methylbenzoic acid REASON: MISSED No amino acid '
               'backbone structure found\n'
               ' * SMILES: NC1C(=O)C=CC=C1C(O)=O NAME: '
               '2,3-dihydro-3-oxoanthranilic acid REASON: MISSED No amino acid '
               'backbone structure found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Missing amino or carboxylic '
                                               'acid group'}],
    'sample_false_negatives': [   {   'smiles': 'N[C@@H](CCC(=O)NC1(O)CC1)C(O)=O',
                                      'name': 'coprine',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'},
                                  {   'smiles': 'C(N(C(=[NH2+])NC)O)CC[C@@H](C(=O)[O-])[NH3+]',
                                      'name': 'N(delta)-hydroxy-N(omega)-methyl-L-argininium',
                                      'reason': 'Missing amino or carboxylic '
                                                'acid group'},
                                  {   'smiles': '[H][C@@]1(N\\C(N[C@]1([H])C(O)=O)=N/[C@@H]1O[C@H](CO)[C@H](OC(N)=O)[C@@H](O)[C@H]1NC(=O)C[C@@H](N)CCCN)[C@H](O)CN',
                                      'name': 'streptothricin F acid',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'},
                                  {   'smiles': 'CC1(C)C[C@@H]1C(=O)N\\C(C(O)=O)=C/CCCCSC[C@H](N)C(O)=O',
                                      'name': 'cilastatin',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'},
                                  {   'smiles': 'NC(CCCNC(N)=O)C(O)=O',
                                      'name': 'citrulline',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'},
                                  {   'smiles': 'CNC(=O)c1ccccc1N',
                                      'name': 'N-Methylanthranilamide',
                                      'reason': 'Missing amino or carboxylic '
                                                'acid group'},
                                  {   'smiles': 'OCCN(CC(O)=O)CC(O)=O',
                                      'name': 'N-(2-hydroxyethyl)iminodiacetic '
                                              'acid',
                                      'reason': 'Missing amino or carboxylic '
                                                'acid group'},
                                  {   'smiles': '[H][C@@]1(C[C@]2(C)[C@]([H])(CC[C@@]3(C)[C@H](C[C@H](OC)[C@H](N)C(O)=O)C(C)=CC[C@]23[H])C(C)(C)[C@@H]1O)O[C@@H]1O[C@@H](C)[C@H](OC(=O)c2cccc(O)c2)[C@@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2NC(C)=O)[C@H]1O',
                                      'name': 'brasilicardin A',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'},
                                  {   'smiles': 'OC(CC(=O)NCCC[C@@H](N)C(O)=O)(CC(O)=O)C(O)=O',
                                      'name': 'delta-Citryl-d-ornithine',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'},
                                  {   'smiles': 'OC(C[C@H](N)C(O)=O)CNC(=O)N',
                                      'name': 'N5-Carbamoyl-4-hydroxy-L-ornithine',
                                      'reason': 'Contains peptide bond '
                                                'indicative of polymers or '
                                                'peptide sequences'}],
    'attempt': 5,
    'reasoning': 'The previous approach attempted to determine if a molecule '
                 'is an amino acid by checking for the presence of an amino '
                 'group and a carboxyl group attached to the same carbon atom, '
                 'generally known as the alpha carbon in amino acids. However, '
                 'the classification missed several cases and incorrectly '
                 'classified some peptide sequences as amino acids.\n'
                 '\n'
                 'To improve classification, I will expand the SMARTS pattern '
                 'to better capture the structure of amino acids, keeping in '
                 'mind that amino acids may not always follow the strict alpha '
                 'carbon structure (e.g., in the case of beta or gamma amino '
                 'acids). The goal is to identify at least one amino group and '
                 'one carboxylic acid group as part of the same substructure '
                 'or separated by non-polymeric chains.\n'
                 '\n'
                 'Here’s how I plan to improve the classification:\n'
                 '\n'
                 '1. **Separate Checks for Amino and Carboxylic Groups**: '
                 'Explicitly check for the presence of both amino and carboxyl '
                 "groups, but don't necessarily enforce their attachment to a "
                 'single carbon if they are within reasonable distance.\n'
                 '\n'
                 '2. **Exclude Peptide Linkages**: Ensure that the molecule is '
                 'not part of a polymeric chain (i.e., a peptide).\n'
                 '\n'
                 '3. **Pattern Flexibility**: Consider variants of amino acids '
                 'with additional functional groups, chain lengths, or '
                 'branching.\n'
                 '\n'
                 'Given these points, the following is an improved Python '
                 'function:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 921,
    'num_false_positives': 2207,
    'num_true_negatives': 138983,
    'num_false_negatives': 189,
    'num_negatives': None,
    'precision': 0.2944373401534527,
    'recall': 0.8297297297297297,
    'f1': 0.4346389806512506,
    'accuracy': 0.9831623330990864,
    'negative_predictive_value': 0.9986419682119967}