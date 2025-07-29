"""
Classifies: CHEBI:16389 ubiquinones
"""
"""
Classifies: CHEBI:27102 ubiquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ubiquinones(smiles: str):
    """
    Determines if a molecule is a ubiquinone based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a ubiquinone, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for benzoquinone core (cyclohexa-2,5-diene-1,4-dione)
    benzoquinone_pattern = Chem.MolFromSmarts("O=C1C=CC(=O)C=C1")
    if not mol.HasSubstructMatch(benzoquinone_pattern):
        return False, "No benzoquinone core found"

    # Look for two methoxy groups (-OC) adjacent to quinone
    dimethoxy_pattern = Chem.MolFromSmarts("O=C1C(OC)=C(OC)C(=O)C=C1")
    if not mol.HasSubstructMatch(dimethoxy_pattern):
        return False, "Missing required 2,3-dimethoxy pattern"

    # Count methoxy groups (-OC) to ensure exactly 2
    methoxy_pattern = Chem.MolFromSmarts("OC")
    methoxy_matches = len(mol.GetSubstructMatches(methoxy_pattern))
    if methoxy_matches < 2:
        return False, "Insufficient methoxy groups"

    # Look for at least one methyl group on the quinone ring
    methyl_quinone_pattern = Chem.MolFromSmarts("O=C1C(OC)=C(OC)C(=O)C(C)=C1")
    if not mol.HasSubstructMatch(methyl_quinone_pattern):
        return False, "Missing methyl group on quinone ring"

    # Optional: Check for isoprenoid/polyprenoid side chain
    # Pattern for isoprenoid unit CC=C(C)C or CC=C(C)CC
    isoprenoid_pattern = Chem.MolFromSmarts("CC=C(C)[C,CC]")
    has_isoprenoid = mol.HasSubstructMatch(isoprenoid_pattern)

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if o_count < 4:
        return False, "Insufficient oxygen atoms for ubiquinone"
    
    # Basic structure confirmed
    if has_isoprenoid:
        return True, "Contains benzoquinone core with 2,3-dimethoxy groups, methyl group, and isoprenoid side chain"
    else:
        return True, "Contains benzoquinone core with 2,3-dimethoxy groups and methyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16389',
                          'name': 'ubiquinones',
                          'definition': 'Any benzoquinone derived from '
                                        '2,3-dimethoxy-5-methylbenzoquinone; '
                                        'one of a group of naturally occurring '
                                        'homologues. The redox-active quinoid '
                                        'moiety usually carries a polyprenoid '
                                        'side chain at position 6, the number '
                                        'of isoprenoid units in which is '
                                        'species-specific. Ubiquinones are '
                                        'involved in the control of '
                                        'mitochondrial electron transport, and '
                                        'are also potent anti-oxidants.',
                          'parents': ['CHEBI:132124', 'CHEBI:26255'],
                          'xrefs': [   'CAS:1339-63-5',
                                       'KEGG:C00399',
                                       'PMID:15788391',
                                       'PMID:7599208'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](O[C@@H]2[C@H](O)[C@@H](O[C@@H]3[C@@H](C[C@@](O)(O[C@]3([H])[C@H](O)CO)C(O)=O)O[C@@]3(C[C@@H](O)[C@@H](O)[C@]([H])(O3)[C@H](O)CO)C(O)=O)O[C@]([H])([C@@H](O)CO)[C@H]2O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@@H]1O)[C@@H](O)CO',
                                     'name': 'beta-D-Galp-(1->3)-L-alpha-D-Hepp-(1->3)-[beta-D-Glcp-(1->4)]-L-alpha-D-Hepp-(1->5)-[alpha-Kdo-(2->4)]-alpha-Kdo',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'C1CCC(CC1)N2C(=NNC2=S)C3=CN=CC=C3',
                                     'name': '4-cyclohexyl-3-(3-pyridinyl)-1H-1,2,4-triazole-5-thione',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'O=C1NCC[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CCCN(O)C(=O)C)CO)CCCN(O)C(=O)C)CO)NC([C@@H]([C@H]1O)NC(=O)CCCCCCCCCCCCCCCCC)=O',
                                     'name': 'Marinobactin F',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'C1(=C2C(=CC(=C1)O[C@H]3[C@H](C([C@@H](C(O3)CO[C@H]4[C@H](C([C@@H](C(O4)CO)O)O)O)O)O)O[C@H]5C([C@H]([C@H](C(O5)C)O)OC(C)=O)O)OC(=CC2=O)C6=CC=C(C=C6)OC)O',
                                     'name': 'acacetin '
                                             "7-O-[6''-O-glucosyl]-2''-O-(3'''-acetylrhamnosyl)glucoside",
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'CC1=CC2=C(N1C)C=CC(=C2)CNC(=O)C3=C(C(=CC=C3)[N+](=O)[O-])C',
                                     'name': 'N-[(1,2-dimethyl-5-indolyl)methyl]-2-methyl-3-nitrobenzamide',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'C[C@H](C1=CC=CC=C1)NC(=O)C[C@H]2C=C[C@@H]([C@@H](O2)CO)NC(=O)CC3=CC=CC=N3',
                                     'name': '2-[(2R,3S,6S)-2-(hydroxymethyl)-3-[[1-oxo-2-(2-pyridinyl)ethyl]amino]-3,6-dihydro-2H-pyran-6-yl]-N-[(1R)-1-phenylethyl]acetamide',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'CCOC(=O)CSC1=NC2=C(C=C(C=C2)N3CCOCC3)C(=O)N1CC4=CC=CC=C4',
                                     'name': '2-[[6-(4-morpholinyl)-4-oxo-3-(phenylmethyl)-2-quinazolinyl]thio]acetic '
                                             'acid ethyl ester',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'OC(=O)\\C=C\\C1=CC=CC(=C1)[Sb](O)(O)=O',
                                     'name': 'stibavirin',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(16:1(9Z)/22:0/22:6(4Z,7Z,10Z,13Z,16Z,19Z))',
                                     'reason': 'No benzoquinone core found'},
                                 {   'smiles': 'CN1C(=O)C(=CN2CCC3=CC=CC=C32)C(=O)NC1=S',
                                     'name': '5-(2,3-dihydroindol-1-ylmethylidene)-1-methyl-2-sulfanylidene-1,3-diazinane-4,6-dione',
                                     'reason': 'No benzoquinone core found'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C(OC)=C(O)C(=O)C(=C1CCOC(=O)C)C',
                                      'name': 'Fumiquinone A',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'},
                                  {   'smiles': 'COC1=C(O)C(=O)C(C)=C(C\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)C1=O',
                                      'name': '3-demethylubiquinone-9',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'},
                                  {   'smiles': 'O(C=1C(=O)C(=C(CC=C(C)C)C(=O)C1OC)CC=C(C)C)C=2C(=C(O)C=C(O)C2)C(OC)=O',
                                      'name': 'Atrovirinone',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'},
                                  {   'smiles': 'O=C1C(CCCCCCCCCCC)=CC(=O)C(O)=C1O',
                                      'name': 'Myrsinone',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'},
                                  {   'smiles': 'C1(=C(C(C(=C(C1=O)OC)[O-])=O)C)C/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)\\C)\\C)\\C)\\C',
                                      'name': '3-demethylubiquinone-8(1-)',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'},
                                  {   'smiles': 'C1(=C(C(C(=C(C1=O)OC)[O-])=O)C)C/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)\\C)\\C)\\C',
                                      'name': '3-demethyl-ubiquinone-7(1-)',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'},
                                  {   'smiles': 'C(C\\C(=C\\CC\\C(=C\\CC\\C(=C\\CC\\C(=C\\CC=1C(C(=C([O-])C(C1C)=O)OC)=O)\\C)\\C)\\C)\\C)/C=C(/CCC=C(C)C)\\C',
                                      'name': '3-demethylubiquinone-6(1-)',
                                      'reason': 'Missing required '
                                                '2,3-dimethoxy pattern'}],
    'attempt': 0,
    'reasoning': 'Let me break down the key characteristics of ubiquinones:\n'
                 '\n'
                 '1. Core structure: 2,3-dimethoxy-5-methylbenzoquinone\n'
                 '   - Has a benzoquinone core '
                 '(cyclohexa-2,5-diene-1,4-dione)\n'
                 '   - Two methoxy groups (OC) at positions 2,3\n'
                 '   - Methyl group at position 5\n'
                 '\n'
                 '2. Optional polyprenoid side chain at position 6\n'
                 '   - Made up of repeating isoprenoid units (-CC=C(C)-)\n'
                 '   - Variable length depending on species\n'
                 '\n'
                 "Here's the code to classify ubiquinones:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 16,
    'num_false_positives': 5,
    'num_true_negatives': 142272,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.7619047619047619,
    'recall': 0.6956521739130435,
    'f1': 0.7272727272727272,
    'accuracy': 0.9999156711173577,
    'negative_predictive_value': 0.9999508008912067}