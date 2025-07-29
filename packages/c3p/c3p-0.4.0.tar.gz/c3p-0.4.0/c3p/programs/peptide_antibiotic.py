"""
Classifies: CHEBI:25903 peptide antibiotic
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Lipinski

def is_peptide_antibiotic(smiles: str):
    """
    Determines if a molecule is a peptide antibiotic based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a peptide antibiotic, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check if molecule is organic
    if not mol.GetAtomWithIdx(0).GetSymbol() == "C":
        return False, "Not an organic molecule"
        
    # Calculate molecular properties
    mw = Descriptors.MolWt(mol)
    n_rotatable = Descriptors.NumRotatableBonds(mol)
    h_bond_donor = Lipinski.NumHDonors(mol)
    h_bond_acceptor = Lipinski.NumHAcceptors(mol)
    
    # Check if molecule meets basic peptide criteria
    if mw < 500 or mw > 5000:
        return False, f"Molecular weight ({mw:.2f} Da) out of typical peptide range"
    if n_rotatable < 5:
        return False, "Too few rotatable bonds for a peptide"
    if h_bond_donor < 2 or h_bond_acceptor < 4:
        return False, "Insufficient hydrogen bond donors/acceptors for a peptide"
        
    # Look for peptide bonds
    peptide_pattern = Chem.MolFromSmarts("C(=O)NCC")
    if not mol.HasSubstructMatch(peptide_pattern):
        return False, "No peptide bonds found"
    
    # Look for amino acid residues
    amino_acid_patterns = [Chem.MolFromSmarts(s) for s in [
        "[NH2]CCC(=O)O", # Basic
        "N[C@H](C)C(=O)O", # Ala
        "NC(C(=O)O)CC", # Asp/Asn
        # Add patterns for other amino acids here
    ]]
    
    amino_acid_matches = []
    for pattern in amino_acid_patterns:
        amino_acid_matches.extend(mol.GetSubstructMatches(pattern))
    
    if not amino_acid_matches:
        return False, "No amino acid residues found"
    
    # Look for non-ribosomal signature (ring systems)
    ring_info = mol.GetRingInfo()
    if not ring_info.AtomRings():
        return False, "No ring systems found (likely ribosomal peptide)"
    
    # Passed all checks, classify as peptide antibiotic
    return True, "Molecule meets criteria for peptide antibiotic"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25903',
                          'name': 'peptide antibiotic',
                          'definition': 'A chemically diverse class of '
                                        'peptides that exhibit antimicrobial '
                                        'properties.',
                          'parents': ['CHEBI:16670'],
                          'xrefs': [   'MetaCyc:Peptide-Antibiotics',
                                       'PMID:33398258'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 49,
                           'log_lines_of_code': 3.8918202981106265,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem, '
                                          'Descriptors, Lipinski'],
                           'imports_count': 2,
                           'methods_called': [   'NumHDonors',
                                                 'GetSymbol',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'NumRotatableBonds',
                                                 'MolFromSmarts',
                                                 'NumHAcceptors',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'extend',
                                                 'MolWt'],
                           'methods_called_count': 13,
                           'smarts_strings': ['s', 'C(=O)NCC'],
                           'smarts_strings_count': 2,
                           'defs': ['is_peptide_antibiotic(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Not an organic molecule"',
                                          'False, f"Molecular weight ({mw:.2f} '
                                          'Da) out of typical peptide range"',
                                          'False, "Too few rotatable bonds for '
                                          'a peptide"',
                                          'False, "Insufficient hydrogen bond '
                                          'donors/acceptors for a peptide"',
                                          'False, "No peptide bonds found"',
                                          'False, "No amino acid residues '
                                          'found"',
                                          'False, "No ring systems found '
                                          '(likely ribosomal peptide)"',
                                          'True, "Molecule meets criteria for '
                                          'peptide antibiotic"'],
                           'returns_count': 9,
                           'complexity': 5.778364059622126},
    'message': '\n'
               'Error: invalid syntax (<string>, line 1)\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O[C@H]1[C@H](O[C@H]2[C@@H](O[C@@H]([C@@H](O)[C@@H]2O)C([O-])=O)Oc2cc(O)c3c(c2)oc(cc3=O)-c2ccc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)c(O)c2)O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O',
                                     'name': 'luteolin '
                                             '7-O-[(beta-D-glucosyluronate)-(1->2)-(beta-D-glucosiduronate)] '
                                             "4'-O-beta-D-glucosiduronate",
                                     'reason': 'Not an organic molecule'},
                                 {   'smiles': 'C1(=CNC2=C1C=CC=C2)CC(C(=O)O)=N',
                                     'name': '2-imino-3-(indol-3-yl)propanoic '
                                             'acid',
                                     'reason': 'Molecular weight (202.21 Da) '
                                               'out of typical peptide range'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3CCCCC3)[C@H](C)CO)C)CN(C)C(=O)C4=CC=NC=C4',
                                     'name': 'N-[[(3R,9S,10R)-16-[[cyclohexyl(oxo)methyl]amino]-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methyl-4-pyridinecarboxamide',
                                     'reason': 'No amino acid residues found'},
                                 {   'smiles': 'CC(C)C[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](C)C(O)=O',
                                     'name': 'Glu-Leu-Phe-Ala',
                                     'reason': 'Molecular weight (478.55 Da) '
                                               'out of typical peptide range'},
                                 {   'smiles': 'O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC=2NC=NC2',
                                     'name': 'Tyr-His-Lys',
                                     'reason': 'Not an organic molecule'},
                                 {   'smiles': 'CC(=O)NCCNc1cccc2c(cccc12)S(O)(=O)=O',
                                     'name': '5-[(2-acetamidoethyl)amino]naphthalene-1-sulfonic '
                                             'acid',
                                     'reason': 'Molecular weight (308.36 Da) '
                                               'out of typical peptide range'},
                                 {   'smiles': 'FC(F)(F)C1=NC(=C(C=C1)C(=O)NC=2C(F)=CC=CC2)C',
                                     'name': 'N-(2-fluorophenyl)-2-methyl-6-(trifluoromethyl)nicotinamide',
                                     'reason': 'Not an organic molecule'},
                                 {   'smiles': 'O(C(COP(=O)(O)O)COC(=O)CCCCCCCC=CCCCCCCCC)C(=O)CCCCCCCC=CCCCCCCCC',
                                     'name': '1,2-bis(octadec-9-enoyl)phosphatidic '
                                             'acid',
                                     'reason': 'Not an organic molecule'},
                                 {   'smiles': 'OC(=O)C(N)(CCCN)C',
                                     'name': '2,5-Diamino-2-methylpentanoic '
                                             'acid',
                                     'reason': 'Not an organic molecule'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(18:1(11Z)/14:0/18:3(9Z,12Z,15Z))',
                                     'reason': 'Not an organic molecule'}],
    'sample_false_negatives': [   {   'smiles': 'CC[C@@H](C)CCCCC(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CCNCS(O)(=O)=O)NC1=O)[C@@H](C)O',
                                      'name': 'colistimethate A',
                                      'reason': 'No amino acid residues found'},
                                  {   'smiles': '[H][C@@]1(Cc2ccc(O)cc2)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CC(N)=O)NC(=O)[C@@H](Cc2ccccc2)NC(=O)[C@H](Cc2c[nH]c3ccccc23)NC(=O)[C@]2([H])CCCN2C(=O)[C@@H](Cc2ccccc2)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCN)NC(=O)[C@@H](NC1=O)C(C)C',
                                      'name': 'tyrocidine B',
                                      'reason': 'No amino acid residues found'},
                                  {   'smiles': 'CC(C)CCCCC(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CCNCS(O)(=O)=O)NC1=O)[C@@H](C)O',
                                      'name': 'colistimethate B',
                                      'reason': 'No amino acid residues found'},
                                  {   'smiles': 'COC1=CC(=O)N(C1)C(=O)[C@H]1CSC(=N1)C(CO)NC(=O)C1=CSC(\\C=N\\O)=N1',
                                      'name': 'althiomycin',
                                      'reason': 'Molecular weight (439.48 Da) '
                                                'out of typical peptide range'},
                                  {   'smiles': 'C(CCCCCCCC)CCCCC(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(=O)O)CCCCN)CCCCN)=O)CCCCN)=O)CCCCN)=O)CO)CSCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)=O',
                                      'name': 'N-palmitoyl-S-[2,3-bis(palmitoyloxy)propyl]-Cys-Ser-Lys-Lys-Lys-Lys',
                                      'reason': 'No ring systems found (likely '
                                                'ribosomal peptide)'},
                                  {   'smiles': '[H][C@@]1(Cc2c[nH]c3ccccc23)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CC(N)=O)NC(=O)[C@@H](Cc2c[nH]c3ccccc23)NC(=O)[C@H](Cc2c[nH]c3ccccc23)NC(=O)[C@]2([H])CCCN2C(=O)[C@@H](Cc2ccccc2)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCN)NC(=O)[C@@H](NC1=O)C(C)C',
                                      'name': 'tyrocidine D',
                                      'reason': 'No amino acid residues found'},
                                  {   'smiles': 'N[C@@H]1c2ccc(O)c(Oc3cc(O)cc(c3)[C@@H]3NC(=O)[C@H](Cc4ccc(Oc5cc6cc(Oc7ccc(cc7Cl)[C@@H](O)[C@@H]7NC(=O)[C@H](NC(=O)[C@@H]6NC3=O)c3cc(Cl)c(O)c(c3)-c3c(O)cc(O)cc3[C@@H](NC7=O)C(O)=O)c5O)c(Cl)c4)NC1=O)c2',
                                      'name': 'A41030A',
                                      'reason': 'Not an organic molecule'},
                                  {   'smiles': '[H][C@@]1(C)SC[C@@H]2NC(=O)[C@H](CCC(O)=O)NC(=O)C(=C)NC(=O)C(NC(=O)[C@H](CC(C)C)NC(=O)[C@@H]1NC(=O)[C@@H]1CS[C@@H](C)[C@@]([H])(NC(=O)[C@H](Cc3ccccc3)NC(=O)[C@]3([H])NC(=O)[C@@H](N)CS[C@H]3C)C(=O)N[C@@]([H])(CC(C)C)C(=O)N3CCC[C@@]3([H])C(=O)NCC(=O)NCC(=O)NCC(=O)NCC(=O)N[C@@H](C(C)C)C(=O)N1)[C@H](C)S\\C=C\\NC(=O)[C@@]([H])(NC2=O)[C@H](C)CC',
                                      'name': 'mersacidin',
                                      'reason': 'No amino acid residues found'},
                                  {   'smiles': 'N[C@H](CO)[C@@H](O)C[C@H](O)[C@H](N)[C@H](O)[C@@H](O)C(=O)N[C@@H](CNC(N)=O)C(N)=O',
                                      'name': '(+)-zwittermicin A',
                                      'reason': 'Not an organic molecule'},
                                  {   'smiles': '[H][C@]1(CS[C@@H](C)[C@@H](NC(=O)[C@@H]2CSC[C@@H](NC(=O)[C@H](C)NC(=O)[C@@H](N)[C@@H](C)CC)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](Cc3ccccc3)C(=O)N[C@@H]([C@@H](C)CC)C(=O)N2)C(=O)N2CCC[C@@]2([H])C(=O)NCC(=O)N1)C(=O)N[C@@H](C)C(=O)N[C@@H](CCCCN)C(=O)N\\C(=C/C)C(=O)NCC(=O)N[C@@H]1CSC[C@@H]2NC(=O)[C@]([H])(Cc3ccc(O)cc3)NC(=O)[C@@H](CS\\C=C/NC2=O)NC(=O)[C@H](CC(N)=O)NC(=O)[C@H](Cc2ccccc2)NC1=O',
                                      'name': 'epidermin',
                                      'reason': 'No amino acid residues '
                                                'found'}],
    'attempt': 2,
    'reasoning': "I apologize for the confusion earlier. Here's a new attempt "
                 'at the `is_peptide_antibiotic` function:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 556,
    'num_true_negatives': 141706,
    'num_false_negatives': 20,
    'num_negatives': None,
    'precision': 0.0313588850174216,
    'recall': 0.47368421052631576,
    'f1': 0.058823529411764705,
    'accuracy': 0.9959522136331693,
    'negative_predictive_value': 0.9998588826326856}