"""
Classifies: CHEBI:46761 dipeptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_dipeptide(smiles: str):
    """
    Determines if a molecule is a dipeptide based on its SMILES string.
    A dipeptide is a molecule that contains two amino acid residues connected by peptide bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dipeptide, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define peptide bond pattern (amide bond between two amino acids)
    peptide_bond_smarts = '[NX3][CX3](=O)'
    peptide_bond = Chem.MolFromSmarts(peptide_bond_smarts)

    # Find all peptide bonds
    peptide_bond_matches = mol.GetSubstructMatches(peptide_bond)
    num_peptide_bonds = len(peptide_bond_matches)

    if num_peptide_bonds != 1:
        return False, f"Found {num_peptide_bonds} peptide bonds, need exactly 1 for dipeptide"

    # Define amino acid residue pattern (alpha amino acid backbone)
    # N-C(alpha)-C(=O)
    amino_acid_smarts = '[NX3][CX4H1][CX3](=O)'
    amino_acid = Chem.MolFromSmarts(amino_acid_smarts)

    # Find all amino acid residues
    amino_acid_matches = mol.GetSubstructMatches(amino_acid)
    num_amino_acids = len(amino_acid_matches)

    if num_amino_acids != 2:
        return False, f"Found {num_amino_acids} amino acid residues, need exactly 2"

    # Check if the amino acids are connected via the peptide bond
    # Map the atoms involved in peptide bond
    peptide_bond_atoms = [match for match in peptide_bond_matches[0]]
    amino_acid_atoms = [list(match) for match in amino_acid_matches]

    # Verify that the peptide bond connects the two amino acid residues
    connected = False
    for aa1 in amino_acid_atoms:
        for aa2 in amino_acid_atoms:
            if aa1 != aa2:
                # Check if peptide bond connects aa1 and aa2
                if (peptide_bond_atoms[0] in aa1 and peptide_bond_atoms[1] in aa2) or \
                   (peptide_bond_atoms[0] in aa2 and peptide_bond_atoms[1] in aa1):
                    connected = True
                    break
        if connected:
            break

    if not connected:
        return False, "Peptide bond does not connect the two amino acid residues"

    return True, "Contains two amino acid residues connected by a peptide bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:46761',
                          'name': 'dipeptide',
                          'definition': 'Any molecule that contains two '
                                        'amino-acid residues connected by '
                                        'peptide linkages.',
                          'parents': ['CHEBI:25676'],
                          'xrefs': ['KEGG:C00107'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 49,
                           'log_lines_of_code': 3.8918202981106265,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'peptide_bond_smarts',
                                                 'amino_acid_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_dipeptide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Found {num_peptide_bonds} '
                                          'peptide bonds, need exactly 1 for '
                                          'dipeptide"',
                                          'False, f"Found {num_amino_acids} '
                                          'amino acid residues, need exactly '
                                          '2"',
                                          'False, "Peptide bond does not '
                                          'connect the two amino acid '
                                          'residues"',
                                          'True, "Contains two amino acid '
                                          'residues connected by a peptide '
                                          'bond"'],
                           'returns_count': 5,
                           'complexity': 3.5783640596221256},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCOC(=O)CC(C1=CC=CC=C1Cl)NC2=NC(=NC(=N2)N3CCOCC3)N4CCOCC4',
                                     'name': '3-[[4,6-bis(4-morpholinyl)-1,3,5-triazin-2-yl]amino]-3-(2-chlorophenyl)propanoic '
                                             'acid ethyl ester',
                                     'reason': 'Found 0 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@]1(C=2C=3OC(=CC(=O)C3C(O)=CC2O)C4=CC(O)=C(O)C=C4)[H])CO)[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)CO',
                                     'name': "2''-O-beta-L-Galactopyranosylorientin",
                                     'reason': 'Found 0 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](NC(C)=O)[C@@H](O[C@H](CO)[C@H]2O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)O[C@@H]2[C@@H](O)[C@@H](O)O[C@H](CO)[C@@H]2O)[C@@H](O)[C@H](O)[C@@H]1O',
                                     'name': 'beta-D-GalpNAc-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->3)-alpha-D-Galp',
                                     'reason': 'Found 2 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CCC(F)(F)F)O[C@H]1CN(C)CC3=CC4=C(C=C3)OCO4)[C@@H](C)CO',
                                     'name': 'N-[(2R,3S)-2-[[1,3-benzodioxol-5-ylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-4,4,4-trifluorobutanamide',
                                     'reason': 'Found 2 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'C1CC(C1)C(=O)N[C@@H]2C=C[C@H](O[C@H]2CO)CC(=O)NCCCN3CCOCC3',
                                     'name': 'N-[(2R,3R,6R)-2-(hydroxymethyl)-6-[2-[3-(4-morpholinyl)propylamino]-2-oxoethyl]-3,6-dihydro-2H-pyran-3-yl]cyclobutanecarboxamide',
                                     'reason': 'Found 2 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'O=C1O[C@@H](CC[C@H](O)C=C[C@H](C1)O)C',
                                     'name': 'Decarestrictine C1',
                                     'reason': 'Found 0 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': '[H]P(O)(=O)OP([H])(O)=O',
                                     'name': 'diphosphonic acid',
                                     'reason': 'Found 0 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)C3=NOC(=C3)C4=CC=CC=C4)[C@H](C)CO',
                                     'name': 'N-[[(8S,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N-methyl-5-phenyl-3-isoxazolecarboxamide',
                                     'reason': 'Found 2 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'OCCCCCCC[C@@H](O)CC(O)=O',
                                     'name': '(3R)-3,10-dihydroxydecanoic acid',
                                     'reason': 'Found 0 peptide bonds, need '
                                               'exactly 1 for dipeptide'},
                                 {   'smiles': 'S(=O)(=O)(CC[C@@H]1NC(=O)[C@H](NC(=O)C(N(C(=O)CC[C@@H](NC([C@H]([C@@H](NC([C@@H](NC(C[C@@H](NC1=O)C(=O)O)=O)CCCN=C(N)N)=O)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)C)=O)C(=O)O)C)=C)C)C',
                                     'name': '[D-Asp3]MC-M(O2)R',
                                     'reason': 'Found 7 peptide bonds, need '
                                               'exactly 1 for dipeptide'}],
    'sample_false_negatives': [   {   'smiles': 'N[C@@H](Cc1ccccc1)C(=O)NCCC(O)=O',
                                      'name': 'Phe-beta-Ala',
                                      'reason': 'Found 1 amino acid residues, '
                                                'need exactly 2'},
                                  {   'smiles': '[H][C@@]12CCCN1C(=O)[C@H](Cc1c(CC=C(C)C)[nH]c3ccccc13)NC2=O',
                                      'name': 'tryprostatin B',
                                      'reason': 'Found 2 peptide bonds, need '
                                                'exactly 1 for dipeptide'},
                                  {   'smiles': 'OC(=O)c1ccc(NC(=O)[C@H](Cc2ccc(O)cc2)NC(=O)c2ccccc2)cc1',
                                      'name': 'bentiromide',
                                      'reason': 'Found 2 peptide bonds, need '
                                                'exactly 1 for dipeptide'},
                                  {   'smiles': 'O=C(N[C@@H](C(C)(C)C)C(=O)N[C@@H](C)C(=O)NCCN)C(CC(C)C)CC(=O)NO',
                                      'name': 'N-[2-[2-(Hydroxyamino)-2-oxoethyl]-4-methyl-1-oxopentyl]-3-methyl-L-valyl-N-(2-aminoethyl)-L-alaninamide '
                                              'Acetic Acid',
                                      'reason': 'Found 4 peptide bonds, need '
                                                'exactly 1 for dipeptide'},
                                  {   'smiles': 'O=C(NCC(O)=O)C[C@H](N)C(O)=O',
                                      'name': 'L-beta-aspartylglycine',
                                      'reason': 'Found 1 amino acid residues, '
                                                'need exactly 2'},
                                  {   'smiles': 'O=C1O[C@@H](C(=O)N[C@@H]2[C@@H](C[C@H](NC(=O)[C@@H](N)C)C(=O)O)C2)[C@@H]1[C@H](CC)C',
                                      'name': 'Belactosin A',
                                      'reason': 'Found 2 peptide bonds, need '
                                                'exactly 1 for dipeptide'},
                                  {   'smiles': 'NC(=O)CC[C@H](NC(=O)[C@@H]1CCCN1)C(O)=O',
                                      'name': 'Pro-Gln',
                                      'reason': 'Found 2 peptide bonds, need '
                                                'exactly 1 for dipeptide'},
                                  {   'smiles': 'O=C1NCC[C@H](O)C[C@H](NC(=O)[C@@H](NC(=O)/C=C/C=C/CC/C=C/CCCCC)[C@H](O)C)C(N[C@H](C=C1)C)=O',
                                      'name': 'Glidobactin B',
                                      'reason': 'Found 4 peptide bonds, need '
                                                'exactly 1 for dipeptide'},
                                  {   'smiles': 'C[C@H](NC(=O)CC[C@H](N)C(O)=O)C(O)=O',
                                      'name': 'gamma-Glu-Ala',
                                      'reason': 'Peptide bond does not connect '
                                                'the two amino acid residues'},
                                  {   'smiles': 'S1C(=NC(=C1)C(=O)N[C@@H](CC2=CC=CC=C2)C[C@@H](C(=O)O)C)[C@H](OC(=O)C)C[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H]3N(CCCC3)C)[C@H](CC)C)COC(=O)C)C(C)C',
                                      'name': 'Tubulysin H',
                                      'reason': 'Found 3 peptide bonds, need '
                                                'exactly 1 for dipeptide'}],
    'attempt': 0,
    'reasoning': 'To determine if a molecule is a dipeptide, we need to:\n'
                 '\n'
                 '1. Parse the SMILES string into an RDKit molecule object.\n'
                 '2. Identify peptide bonds (amide bonds connecting amino '
                 'acids).\n'
                 '3. Detect amino acid residues connected by these peptide '
                 'bonds.\n'
                 '4. Ensure that there are exactly two amino acid residues '
                 'connected via a peptide bond.\n'
                 '\n'
                 'An amino acid residue can be identified by the presence of '
                 'an alpha carbon connected to:\n'
                 '\n'
                 '- An amino group (`-NH2` or protonated versions)\n'
                 '- A carboxyl group (`-COOH` or deprotonated versions)\n'
                 '- A side chain (various R groups)\n'
                 '\n'
                 'A peptide bond is an amide linkage formed between the '
                 'carboxyl group of one amino acid and the amino group of '
                 'another.\n'
                 '\n'
                 "Here's the code implementing this logic:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 381,
    'num_false_positives': 67,
    'num_true_negatives': 141264,
    'num_false_negatives': 588,
    'num_negatives': None,
    'precision': 0.8504464285714286,
    'recall': 0.3931888544891641,
    'f1': 0.5377558221594919,
    'accuracy': 0.9953970484891075,
    'negative_predictive_value': 0.9958548346163607}