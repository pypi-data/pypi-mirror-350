"""
Classifies: CHEBI:47923 tripeptide
"""
"""
Classifies: CHEBI:36357 tripeptide
Any oligopeptide that consists of three amino-acid residues connected by peptide linkages.
"""

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

def is_tripeptide(smiles: str):
    """
    Determines if a molecule is a tripeptide based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tripeptide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Look for 2 amide bonds (-C(=O)-N-)
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if len(amide_matches) != 2:
        return False, f"Found {len(amide_matches)} amide bonds, need exactly 2"
    
    # Look for 3 amino acid residues (N-C-C)
    aa_pattern = Chem.MolFromSmarts("NC(C)C")
    aa_matches = mol.GetSubstructMatches(aa_pattern)
    if len(aa_matches) != 3:
        return False, f"Found {len(aa_matches)} amino acid residues, need exactly 3"
    
    # Check for peptide bonds connecting residues
    peptide_bond_pattern = Chem.MolFromSmarts("N(C(=O))C")
    peptide_bond_matches = mol.GetSubstructMatches(peptide_bond_pattern)
    if len(peptide_bond_matches) != 2:
        return False, f"Found {len(peptide_bond_matches)} peptide bonds, need exactly 2"
    
    # Check hydrogen bond donors/acceptors
    n_hbond_donors = rdMolDescriptors.CalcNumHBD(mol)
    n_hbond_acceptors = rdMolDescriptors.CalcNumHBA(mol)
    if n_hbond_donors < 3 or n_hbond_donors > 6:
        return False, "Hydrogen bond donor count outside expected range"
    if n_hbond_acceptors < 4 or n_hbond_acceptors > 8:
        return False, "Hydrogen bond acceptor count outside expected range"
    
    # Check molecular weight
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200 or mol_wt > 800:
        return False, "Molecular weight outside expected range for tripeptide"
    
    # Additional checks for structural diversity
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[r]")):  # Ring system
        return True, "Contains 3 amino acid residues linked by peptide bonds (cyclic)"
    if any(atom.GetDegree() > 4 for atom in mol.GetAtoms()):  # Quaternary atoms
        return True, "Contains 3 amino acid residues linked by peptide bonds (quaternary atoms present)"
    
    return True, "Contains 3 amino acid residues linked by peptide bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47923',
                          'name': 'tripeptide',
                          'definition': 'Any oligopeptide that consists of '
                                        'three amino-acid residues connected '
                                        'by peptide linkages.',
                          'parents': ['CHEBI:25676'],
                          'xrefs': ['KEGG:C00316', 'Wikipedia:Tripeptide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 44,
                           'log_lines_of_code': 3.784189633918261,
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
                                                 1,
                                                 1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem, '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetAtoms',
                                                 'GetDegree',
                                                 'CalcExactMolWt',
                                                 'CalcNumHBA',
                                                 'MolFromSmarts',
                                                 'CalcNumHBD',
                                                 'GetSubstructMatches',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 9,
                           'smarts_strings': [   'C(=O)N',
                                                 '"[r]")',
                                                 'N(C(=O))C',
                                                 'NC(C)C'],
                           'smarts_strings_count': 4,
                           'defs': ['is_tripeptide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Found {len(amide_matches)} '
                                          'amide bonds, need exactly 2"',
                                          'False, f"Found {len(aa_matches)} '
                                          'amino acid residues, need exactly '
                                          '3"',
                                          'False, f"Found '
                                          '{len(peptide_bond_matches)} peptide '
                                          'bonds, need exactly 2"',
                                          'False, "Hydrogen bond donor count '
                                          'outside expected range"',
                                          'False, "Hydrogen bond acceptor '
                                          'count outside expected range"',
                                          'False, "Molecular weight outside '
                                          'expected range for tripeptide"',
                                          'True, "Contains 3 amino acid '
                                          'residues linked by peptide bonds '
                                          '(cyclic)"',
                                          'True, "Contains 3 amino acid '
                                          'residues linked by peptide bonds '
                                          '(quaternary atoms present)"',
                                          'True, "Contains 3 amino acid '
                                          'residues linked by peptide bonds"'],
                           'returns_count': 10,
                           'complexity': 5.156837926783652},
    'message': '\n'
               'Error: unterminated string literal (detected at line 3) '
               '(<string>, line 3)\n'
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
    'sample_true_negatives': [   {   'smiles': 'O1C2(C(CCC2C(C)=C)C)CC(C1=O)=C(C)C',
                                     'name': 'Curcumanolide A',
                                     'reason': 'Found 0 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)CC4=CC=C(C=C4)O)[C@H](C)CO',
                                     'name': 'LSM-30882',
                                     'reason': 'Found 1 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'O=C1N([C@H](C2=C(O)C(OC)=CC(=C2)C)C=3C1=C(OC)C=C(O)C3)CCCC(=O)O',
                                     'name': 'Daldinan C',
                                     'reason': 'Found 1 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=CC(=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)CC3CC3',
                                     'name': 'N-[(5S,6R,9S)-8-(cyclopropylmethyl)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'Found 1 amino acid residues, '
                                               'need exactly 3'},
                                 {   'smiles': 'O=C1C2=C(O)C=CC=C2C(=O)[C@]3([C@]1(O)C=C[C@@]45C[C@@](O)(C)[C@@H](C([C@]35O4)=O)O)O',
                                     'name': '(1S,2R,11R,14R,16S,17S)-2,8,11,16,17-pentahydroxy-16-methyl-19-oxapentacyclo[12.4.1.01,14.02,11.04,9]nonadeca-4(9),5,7,12-tetraene-3,10,18-trione',
                                     'reason': 'Found 0 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\C)=O)C)[Mg-2]735)[C@@H](C(C8=C6C)=O)C(=O)OC)C(=C4C)CC)=C(C2C)C=C',
                                     'name': "chlorophyll a'",
                                     'reason': 'Found 0 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'C1Oc2ccccc2C=C1',
                                     'name': '2H-chromene',
                                     'reason': 'Found 0 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'O1C([C@H]2[C@@H]3[C@]([C@H](C1(CC3)C)C)(C)CC2)(CO)C',
                                     'name': 'Seiricardine B',
                                     'reason': 'Found 0 amide bonds, need '
                                               'exactly 2'},
                                 {   'smiles': 'C[C@@H]1CN[C@@H](COC2=C(C=CC(=C2)NC(=O)C3=CC=C(C=C3)OC)C(=O)N(C[C@H]1OC)C)C',
                                     'name': '4-methoxy-N-[(5S,6R,9R)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]benzamide',
                                     'reason': 'Found 1 amino acid residues, '
                                               'need exactly 3'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(OCCN)(O)=O',
                                     'name': 'PE(17:2(9Z,12Z)/16:0)',
                                     'reason': 'Found 0 amide bonds, need '
                                               'exactly 2'}],
    'sample_false_negatives': [   {   'smiles': 'CC(=O)N[C@@H](Cc1ccc(O)c(c1)\\N=N\\c1ccc(cc1)C(O)=O)C(=O)NCC(=O)NCC(O)=O',
                                      'name': '3-[(4-carboxyphenyl)diazenyl]-N-AcTyrGlyGly',
                                      'reason': 'Found 3 amide bonds, need '
                                                'exactly 2'},
                                  {   'smiles': 'CC(C)C[C@@H](NC(=O)CNC(=O)CN)C(O)=O',
                                      'name': 'Gly-Gly-D-Leu',
                                      'reason': 'Found 1 amino acid residues, '
                                                'need exactly 3'},
                                  {   'smiles': 'N[C@@H](CCC(O)=O)C(=O)NCC(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O',
                                      'name': 'Glu-Gly-Trp',
                                      'reason': 'Found 2 amino acid residues, '
                                                'need exactly 3'},
                                  {   'smiles': 'NC(=O)C(CCCCNC(=O)c1ccc(o1)[N+]([O-])=O)NC(=O)CCOCCOCCNC(=O)C1CCN(CC1)C(=O)CNC(=O)C1CCN(CC1)C(=O)CCOCCOCCNC(=O)CCCc1c[nH]c2ccccc12',
                                      'name': 'N(2)-{3-[2-(2-{[(1-{N-[(1-{3-[2-(2-{[4-(indol-3-yl)butanoyl]amino}ethoxy)ethoxy]propanoyl}piperidin-4-yl)carbonyl]glycyl}piperidin-4-yl)carbonyl]amino}ethoxy)ethoxy]propanoyl}-N(6)-(5-nitro-2-furoyl)lysinamide',
                                      'reason': 'Found 8 amide bonds, need '
                                                'exactly 2'},
                                  {   'smiles': 'C[C@H](N)C(=O)N[C@H](CCC(=O)N[C@H](CCC[C@H](N)C(O)=O)C(O)=O)C(O)=O',
                                      'name': 'L-alanyl-gamma-D-glutamyl-meso-diaminopimelic '
                                              'acid',
                                      'reason': 'Found 4 amino acid residues, '
                                                'need exactly 3'},
                                  {   'smiles': 'CCCC[C@H](NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CC(C)C)NC(C)=O)C=O',
                                      'name': 'acetylleucyl-leucyl-norleucinal',
                                      'reason': 'Found 3 amide bonds, need '
                                                'exactly 2'},
                                  {   'smiles': 'C([C@H](CC(C)C)NC([C@@H](NC(=O)[C@@H](NC(=O)C1=NOC(=C1)C)C)C(C)C)=O)(=O)N[C@H](/C=C/C(OCC2=CC=CC=C2)=O)C[C@H]3C(NCC3)=O',
                                      'name': 'N-[(5-methyl-1,2-oxazol-3-yl)carbonyl]-L-alanyl-L-valyl-N-{(2S,3E)-5-(benzyloxy)-5-oxo-1-[(3S)-2-oxopyrrolidin-3-yl]pent-3-en-2-yl}-L-leucinamide',
                                      'reason': 'Found 5 amide bonds, need '
                                                'exactly 2'},
                                  {   'smiles': 'N[C@@H](Cc1ccccc1)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(O)=O',
                                      'name': 'Phe-Pro-Pro',
                                      'reason': 'Found 4 peptide bonds, need '
                                                'exactly 2'},
                                  {   'smiles': 'NCCCC[C@H](N)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](Cc1ccc(O)cc1)C(O)=O',
                                      'name': 'Lys-Asp-Tyr',
                                      'reason': 'Hydrogen bond donor count '
                                                'outside expected range'},
                                  {   'smiles': 'C(=O)([C@@H](N)CCCCN)N[C@H](C(=O)N[C@H](C(=O)O)CC=1C=2C=CC=CC2NC1)CO',
                                      'name': 'Lys-Ser-Trp',
                                      'reason': 'Hydrogen bond donor count '
                                                'outside expected range'}],
    'attempt': 3,
    'reasoning': 'Here is a program to classify chemical entities as '
                 'tripeptides using RDKit:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 55,
    'num_false_positives': 2404,
    'num_true_negatives': 139730,
    'num_false_negatives': 111,
    'num_negatives': None,
    'precision': 0.022366815778771858,
    'recall': 0.3313253012048193,
    'f1': 0.0419047619047619,
    'accuracy': 0.9823260716795502,
    'negative_predictive_value': 0.999206241374132}