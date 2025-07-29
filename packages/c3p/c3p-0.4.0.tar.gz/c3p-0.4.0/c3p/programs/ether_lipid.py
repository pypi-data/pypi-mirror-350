"""
Classifies: CHEBI:64611 ether lipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ether_lipid(smiles: str):
    """
    Determines if a molecule is an ether lipid based on its SMILES string.
    Ether lipids have one or more carbon atoms on glycerol bonded to an alkyl chain via an ether linkage.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an ether lipid, False otherwise
        str: Reason for classification
    """
    
    # Parse the SMILES string into a molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for glycerol backbone pattern (C-C-C) with potential for ether bonding
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Look for ether linkage pattern (C-O-C)
    ether_pattern = Chem.MolFromSmarts("[CX4]O[CX4]")
    ether_matches = mol.GetSubstructMatches(ether_pattern)
    if len(ether_matches) < 1:
        return False, "No ether linkage found"

    # Check for phosphate or choline groups that are common headgroups in ether lipids
    phosphate_pattern = Chem.MolFromSmarts("P(=O)(O)O")
    choline_pattern = Chem.MolFromSmarts("C[N+](C)(C)C")
    
    has_phosphate = mol.HasSubstructMatch(phosphate_pattern)
    has_choline = mol.HasSubstructMatch(choline_pattern)
    
    if has_phosphate or has_choline:
        return True, "Contains ether linkages along with common lipid headgroups (e.g., phosphate, choline)"
    else:
        return False, "Missing common lipid headgroups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:64611',
                          'name': 'ether lipid',
                          'definition': 'A lipid similar in structure to a '
                                        'glycerolipid but in which one or more '
                                        'of the carbon atoms on glycerol is '
                                        'bonded to an alkyl chain via an ether '
                                        'linkage, as opposed to the usual '
                                        'ester linkage.',
                          'parents': ['CHEBI:18059', 'CHEBI:52575'],
                          'xrefs': [   'PMID:21309516',
                                       'PMID:22114698',
                                       'PMID:22148427',
                                       'PMID:22306069',
                                       'PMID:22348073',
                                       'PMID:22366205',
                                       'PMID:22506086',
                                       'PMID:22609598',
                                       'Wikipedia:Ether_lipid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 31,
                           'log_lines_of_code': 3.4339872044851463,
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
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
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
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'HasSubstructMatch',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 4,
                           'smarts_strings': [   '[CX4]O[CX4]',
                                                 'C[N+](C)(C)C',
                                                 '[CH2X4][CHX4][CH2X4]',
                                                 'P(=O)(O)O'],
                           'smarts_strings_count': 4,
                           'defs': ['is_ether_lipid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycerol backbone found"',
                                          'False, "No ether linkage found"',
                                          'True, "Contains ether linkages '
                                          'along with common lipid headgroups '
                                          '(e.g., phosphate, choline)"',
                                          'False, "Missing common lipid '
                                          'headgroups"'],
                           'returns_count': 5,
                           'complexity': 3.086797440897029},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O1C=2C(=C(O)C(CC=C(C)C)=C(OC)C2)C(=O)C(C3=CC=C(O)C=C3)=C1',
                                     'name': 'Gancaonin G',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'S(CC[C@H](N)C(=O)N[C@@H](CCC(=O)N)C(=O)N[C@@H](C(C)C)C(O)=O)C',
                                     'name': 'Met-Gln-Val',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@@H](O)O[C@H](CO)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O',
                                     'name': 'beta-D-Galp3S-(1->3-)-alpha-D-GalpNAc',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CN(C)C(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@@H](CN2C(=O)NC3=CC(=CC=C3)OC)O',
                                     'name': '(3R,6aR,8R,10aR)-8-[2-(dimethylamino)-2-oxoethyl]-3-hydroxy-N-(3-methoxyphenyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Missing common lipid '
                                               'headgroups'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CC=CC=C4C#N)C5=CC=CC=C5N2C)[C@@H](C)CO',
                                     'name': 'LSM-9464',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CC1=CC=CC=C1S(=O)(=O)N2C[C@@H](COC[C@H]3[C@H]2CC[C@@H](O3)CC(=O)NCC4=CC=CC=C4Cl)O',
                                     'name': '2-[(3S,6aR,8R,10aR)-3-hydroxy-1-(2-methylphenyl)sulfonyl-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[(2-chlorophenyl)methyl]acetamide',
                                     'reason': 'Missing common lipid '
                                               'headgroups'},
                                 {   'smiles': 'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)C(=O)C3=NC=CN=C3',
                                     'name': 'N-[(4S,7S,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-[oxo(2-pyrazinyl)methyl]-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C1CCN(CC1)CCNC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@H](CN3S(=O)(=O)C4=CC=CC=C4)O',
                                     'name': '2-[(3S,6aS,8S,10aS)-1-(benzenesulfonyl)-3-hydroxy-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[2-(1-piperidinyl)ethyl]acetamide',
                                     'reason': 'Missing common lipid '
                                               'headgroups'},
                                 {   'smiles': 'OC1CC(N(C1)C(=O)C(N)CC2=CC=CC=C2)C(O)=O',
                                     'name': 'Phenylalanyl-Hydroxyproline',
                                     'reason': 'No ether linkage found'},
                                 {   'smiles': 'O([C@H]1O[C@@H]([C@H]([C@@H]([C@@H]1O)O)O)CO)CCC(CCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C)=O',
                                     'name': '1-(alpha-D-mannosyl)-3-keto-(1,27R)-octacosanediol',
                                     'reason': 'No glycerol backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'C(CCCCCCC/C=C\\CCCCCCCC)(OC[C@@H](COP(O)(=S)O)OC)=O',
                                      'name': '(2S)-1-oleoyl-2-methylglycero-3-phosphothionate',
                                      'reason': 'Missing common lipid '
                                                'headgroups'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC\\C=C/OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCCCCCC',
                                      'name': '1-(1Z-octadecenyl)-2-hexadecanoyl-sn-glycero-3-phosphocholine',
                                      'reason': 'No ether linkage found'},
                                  {   'smiles': '[C@@H](OC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(CO/C=C\\CCCCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-]',
                                      'name': '1-(1Z-octadecenyl)-2-(4Z,7Z,10Z,13Z,16Z,19Z-docosahexaenoyl)-sn-glycero-3-phosphocholine',
                                      'reason': 'No ether linkage found'},
                                  {   'smiles': '[C@H](OCCCCCCCCCCCC)(COCCCCCCCCCCCC)COC(CCCC(OC=1C(=C2C(=CC1)N=C3C(O2)=CC(C=C3)=O)C)=O)=O',
                                      'name': '(S)-1,2-di-O-dodecanylglycero-3-glutaric '
                                              "acid 6'-methylresorufin ester",
                                      'reason': 'Missing common lipid '
                                                'headgroups'},
                                  {   'smiles': '[C@@H](OC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(CO/C=C\\CCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-]',
                                      'name': '1-(1Z-hexadecenyl)-2-(4Z,7Z,10Z,13Z,16Z,19Z-docosahexaenoyl)-sn-glycero-3-phosphocholine',
                                      'reason': 'No ether linkage found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC)OC(C)=O',
                                      'name': '1-palmityl-2-acetyl-3-linoleoyl-sn-glycerol',
                                      'reason': 'Missing common lipid '
                                                'headgroups'},
                                  {   'smiles': 'C(CCCCCCC/C=C\\CCCCCCCC)(=O)O[C@@H](COP(=O)(OCC[N+](C)(C)C)[O-])CO/C=C\\CCCCCCCCCCCCCCCC',
                                      'name': '1-[(1Z)-octadecenyl]-2-[(9Z)-octadecenoyl]-sn-glycero-3-phosphocholine',
                                      'reason': 'No ether linkage found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOCC(=O)COP(O)(O)=O',
                                      'name': '1-palmitylglycerone 3-phosphate',
                                      'reason': 'No glycerol backbone found'},
                                  {   'smiles': 'C(CCCCCCCCCCCCCCCC)=COC[C@H](COP(=O)(OCC[NH3+])[O-])O',
                                      'name': '1-(octadec-1-enyl)-sn-glycero-3-phosphoethanolamine '
                                              'zwitterion',
                                      'reason': 'No ether linkage found'},
                                  {   'smiles': 'CCCCCCCCCCCCCC\\C=C\\OC[C@@H](O)CO',
                                      'name': '1-O-[(E)-hexadecen-1-yl]-sn-glycerol',
                                      'reason': 'No ether linkage found'}],
    'attempt': 0,
    'reasoning': 'To classify a SMILES string as an ether lipid, we will '
                 'follow these steps:\n'
                 '\n'
                 '1. **Definition Overview:** Ether lipids are characterized '
                 'by the presence of one or more ether linkages in place of '
                 'the usual ester bond found in glycerolipids. Typically, an '
                 'ether bond (C-O-C) replaces an ester bond (C-O-C(=O)) in '
                 'these molecules. \n'
                 '\n'
                 '2. **Identify Key Patterns:**\n'
                 '   - We will look for a glycerol backbone, which is commonly '
                 'present in ether lipids. This backbone usually consists of '
                 'three consecutive carbon atoms.\n'
                 '   - Identify ether linkages, which are C-O-C patterns '
                 'distinguished from ester linkages typical in other lipid '
                 'types. These are important for indicating the presence of an '
                 'ether lipid.\n'
                 '   - Look for possible phosphate or choline groups, as these '
                 'are common headgroups in ether phospholipids.\n'
                 '\n'
                 '3. **Use RDKit to Search for Patterns:**\n'
                 '   - Use SMARTS patterns to identify the key structural '
                 'features of ether lipids in the molecule parsed from the '
                 'SMILES string.\n'
                 '\n'
                 '4. **Return Classification and Reason:**\n'
                 '   - If the molecule has the requisite ether linkages and '
                 'other relevant features, classify it as an ether lipid.\n'
                 '   - Otherwise, return `False` with an appropriate reason.\n'
                 '\n'
                 'Here’s the Python code implementing this functionality:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 166,
    'num_false_positives': 826,
    'num_true_negatives': 141222,
    'num_false_negatives': 86,
    'num_negatives': None,
    'precision': 0.16733870967741934,
    'recall': 0.6587301587301587,
    'f1': 0.2668810289389067,
    'accuracy': 0.9935910049191848,
    'negative_predictive_value': 0.9993914003453449}