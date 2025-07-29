"""
Classifies: CHEBI:32877 primary amine
"""
"""
Classifies: Primary Amine
Definition: A compound formally derived from ammonia by replacing one hydrogen atom by a hydrocarbyl group.
For this classifier, the molecule is considered a primary amine if it contains at least one primary amine group.
A valid primary amine group is defined as an –NH2 group (with exactly two hydrogens) bonded to one non-hydrogen atom 
(that is, derived from ammonia by replacing one hydrogen by a hydrocarbyl group) and not being involved in an amide bond.
Also, if the molecule contains any amide bonds (indicative of peptides or similar compounds), the molecule is rejected.
"""
from rdkit import Chem

def is_primary_amine(smiles: str):
    """
    Determines if a molecule is a primary amine based on its SMILES string.
    A primary amine (R–NH2) is derived from ammonia by replacing one hydrogen with a hydrocarbyl group.
    For our purposes, the molecule is considered a primary amine if it meets the following criteria:
      - It does NOT contain any amide bonds (the presence of a pattern "C(=O)N" is grounds for rejection).
      - It contains at least one primary amine group. 
        A primary amine group is found by matching the SMARTS pattern "[NX3;H2;!$(NC=O)]":
            • NX3: a trivalent nitrogen,
            • H2: exactly two hydrogens attached,
            • !$(NC=O): not directly bonded to a carbonyl carbon.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a primary amine, False otherwise.
        str: Reason for the classification.
    """
    # Parse SMILES into a molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Add explicit hydrogens so that hydrogen counts are accessible.
    mol = Chem.AddHs(mol)
    
    # First, reject molecules that contain an amide bond.
    amide_smarts = Chem.MolFromSmarts("C(=O)N")
    if amide_smarts is None:
        return False, "Error generating amide SMARTS pattern"
    if mol.HasSubstructMatch(amide_smarts):
        return False, "Molecule contains amide bond(s) typical of peptides/amides"
    
    # Define the SMARTS for a primary amine:
    # [NX3;H2] means trigonal nitrogen with exactly two hydrogens.
    # !$(NC=O) ensures that the nitrogen is not bonded to a carbonyl group.
    primary_amine_smarts = Chem.MolFromSmarts("[NX3;H2;!$(NC=O)]")
    if primary_amine_smarts is None:
        return False, "Error generating primary amine SMARTS pattern"
    
    # Look for a match of the primary amine group in the molecule.
    if mol.HasSubstructMatch(primary_amine_smarts):
        return True, "Molecule contains a valid primary amine (R–NH2) group."
    
    return False, "No valid primary amine group (with two hydrogens and one substituent not involved in an amide) found."

# Example test calls (you may remove these before deployment)
if __name__ == "__main__":
    test_smiles_list = [
        # acid fuchsin (free acid form)
        "Cc1cc(cc(c1N)S(O)(=O)=O)C(=C1\\C=CC(=N)C(=C1)S(O)(=O)=O)\\c1ccc(N)c(c1)S(O)(=O)=O",
        # N-[(3-methoxyphenyl)methyl]-N-methyl-1-[1-[2-(2-methylphenyl)ethyl]-3-piperidinyl]methanamine
        "CC1=CC=CC=C1CCN2CCCC(C2)CN(C)CC3=CC(=CC=C3)OC",
        # (R)-clenbuterol
        "CC(C)(C)NC[C@H](O)c1cc(Cl)c(N)c(Cl)c1",
        # 2-Methylbutylamine
        "NC[C@H](CC)C",
        # clenbuterol
        "CC(C)(C)NCC(O)c1cc(Cl)c(N)c(Cl)c1",
        # Phenelzine
        "NNCCc1ccccc1",
        # methylamine (a simple primary amine)
        "CN",
        # aniline
        "Nc1ccccc1",
        # pentan-1-amine
        "CCCCCN"
    ]
    for smi in test_smiles_list:
        result, reason = is_primary_amine(smi)
        print(f"SMILES: {smi}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32877',
                          'name': 'primary amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing one hydrogen '
                                        'atom by a hydrocarbyl group.',
                          'parents': ['CHEBI:32952', 'CHEBI:50994'],
                          'xrefs': [   'KEGG:C00375',
                                       'KEGG:C00893',
                                       'KEGG:C02580'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 61,
                           'log_lines_of_code': 4.110873864173311,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2,
                                                 1,
                                                 2,
                                                 1,
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
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'AddHs',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 4,
                           'smarts_strings': ['C(=O)N', '[NX3;H2;!$(NC=O)]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_primary_amine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error generating amide '
                                          'SMARTS pattern"',
                                          'False, "Molecule contains amide '
                                          'bond(s) typical of peptides/amides"',
                                          'False, "Error generating primary '
                                          'amine SMARTS pattern"',
                                          'True, "Molecule contains a valid '
                                          'primary amine (R–NH2) group."',
                                          'False, "No valid primary amine '
                                          'group (with two hydrogens and one '
                                          'substituent not involved in an '
                                          'amide) found."'],
                           'returns_count': 6,
                           'complexity': 3.6221747728346623},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'Cc1cc(cc(c1N)S(O)(=O)=O)C(=C1\\C=CC(=N)C(=C1)S(O)(=O)=O)\\c1ccc(N)c(c1)S(O)(=O)=O '
               'NAME: acid fuchsin (free acid form) REASON: MISSED No valid '
               'primary amine group (with two hydrogens and one substituent '
               'not involved in an amide) found.\n'
               ' * SMILES: CC1=CC=CC=C1CCN2CCCC(C2)CN(C)CC3=CC(=CC=C3)OC NAME: '
               'N-[(3-methoxyphenyl)methyl]-N-methyl-1-[1-[2-(2-methylphenyl)ethyl]-3-piperidinyl]methanamine '
               'REASON: MISSED No valid primary amine group (with two '
               'hydrogens and one substituent not involved in an amide) '
               'found.\n'
               ' * SMILES: CC(C)(C)NC[C@H](O)c1cc(Cl)c(N)c(Cl)c1 NAME: '
               '(R)-clenbuterol REASON: MISSED No valid primary amine group '
               '(with two hydrogens and one substituent not involved in an '
               'amide) found.\n'
               ' * SMILES: NC[C@H](CC)C NAME: 2-Methylbutylamine REASON: '
               'MISSED No valid primary amine group (with two hydrogens and '
               'one substituent not involved in an amide) found.\n'
               ' * SMILES: CC(C)(C)NCC(O)c1cc(Cl)c(N)c(Cl)c1 NAME: clenbuterol '
               'REASON: MISSED No valid primary amine group (with two '
               'hydrogens and one substituent not involved in an amide) '
               'found.\n'
               ' * SMILES: NNCCc1ccccc1 NAME: Phenelzine REASON: MISSED No '
               'valid primary amine group (with two hydrogens and one '
               'substituent not involved in an amide) found.\n'
               ' * SMILES: [H]C(=O)CCCNCCCN NAME: '
               'N-(3-aminopropyl)-4-aminobutanal REASON: MISSED No valid '
               'primary amine group (with two hydrogens and one substituent '
               'not involved in an amide) found.\n'
               ' * SMILES: NCCCCC(CN)CCCN NAME: '
               '4-(aminomethyl)octane-1,8-diamine REASON: MISSED No valid '
               'primary amine group (with two hydrogens and one substituent '
               'not involved in an amide) found.\n'
               ' * SMILES: Nc1ccc(cc1)N=Nc1ccc(cc1)[N+]([O-])=O NAME: '
               '4-(4-nitrophenylazo)aniline REASON: MISSED No valid primary '
               'amine group (with two hydrogens and one substituent not '
               'involved in an amide) found.\n'
               ' * SMILES: Nc1ccc(cc1S(O)(=O)=O)\\N=N\\c1ccc(cc1)S(O)(=O)=O '
               "NAME: 4-aminoazobenzene-3,4'-disulfonic acid REASON: MISSED No "
               'valid primary amine group (with two hydrogens and one '
               'substituent not involved in an amide) found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CC1=NC(=CC=C1)NC(=O)C23CCC(C2Br)(C3(C)C)C(Br)Br',
                                     'name': '6-bromo-1-(dibromomethyl)-5,5-dimethyl-N-(6-methyl-2-pyridinyl)-4-bicyclo[2.1.1]hexanecarboxamide',
                                     'reason': 'Molecule contains amide '
                                               'bond(s) typical of '
                                               'peptides/amides'},
                                 {   'smiles': 'O=C1[C@H]2C(=CC[C@H]3[C@]4(O[C@@H](C=C(C)C)C[C@@H]4C)CC[C@@]3(C[C@@H]2[C@@](C1)(O)C)C)C=O',
                                     'name': '6-epi-Ophiobolin A',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'O[C@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@@](CC3)(C([C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)CO)CC4)(C)C)[H])C)(C1)[H])C)(CC[C@@]2([C@@](O[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO[C@@H]8OC[C@H](O[C@@H]9OC[C@@H](O)[C@H](O)[C@H]9O)[C@H](O)[C@H]8O)(CCC=C(C)C)C)[H])C)[H]',
                                     'name': 'Ginsenoside Ra1',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'CN(CC1=CC=CC=C1F)CC2=CC(=O)OC3=CC(=C(C=C23)Cl)O',
                                     'name': '6-chloro-4-[[(2-fluorophenyl)methyl-methylamino]methyl]-7-hydroxy-1-benzopyran-2-one',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'C1=COC(=C1)CNC2=NC=NC3=C2N=CN3[C@H]4[C@@H]([C@@H]([C@H](O4)CO)O)O',
                                     'name': '(2R,3R,4S,5R)-2-[6-(2-furanylmethylamino)-9-purinyl]-5-(hydroxymethyl)oxolane-3,4-diol',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C(=C2[C@H](OC)[C@@H]3[C@H]1C[C@@H](O)[C@](C3)(O)C)O',
                                     'name': '4a-epi-9alpha-methoxydihydrodeoxybostrycin',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'C1CN(CCN1C2=C3C=CC(=CC3=NC=C2)Cl)S(=O)(=O)C4=CC(=CC=C4)Br',
                                     'name': '4-[4-(3-bromophenyl)sulfonyl-1-piperazinyl]-7-chloroquinoline',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'O=C1O[C@@H]2[C@@](O[C@@H](C)[C@@H]([C@H]2C)OC(=O)/C=C/[C@@H](O)CCCC)(C)[C@H]([C@@H]1C)O',
                                     'name': 'Botcinin F',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'},
                                 {   'smiles': 'OC(C(N)C(=O)NC(CC1=CC=C(O)C=C1)C(=O)NCC(=O)NCC(O)=O)C',
                                     'name': 'Thr Tyr Gly Gly',
                                     'reason': 'Molecule contains amide '
                                               'bond(s) typical of '
                                               'peptides/amides'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](OCC(O)c3ccc(O)c(O)c3)O[C@H](CO)[C@H]2OC(=O)\\C=C\\c2ccc(O)c(O)c2)[C@H](O)[C@H](O)[C@H]1O',
                                     'name': 'beta-Hydroxyacteoside',
                                     'reason': 'No valid primary amine group '
                                               '(with two hydrogens and one '
                                               'substituent not involved in an '
                                               'amide) found.'}],
    'sample_false_negatives': [   {   'smiles': 'CC1=CC=CC=C1CCN2CCCC(C2)CN(C)CC3=CC(=CC=C3)OC',
                                      'name': 'N-[(3-methoxyphenyl)methyl]-N-methyl-1-[1-[2-(2-methylphenyl)ethyl]-3-piperidinyl]methanamine',
                                      'reason': 'No valid primary amine group '
                                                '(with two hydrogens and one '
                                                'substituent not involved in '
                                                'an amide) found.'},
                                  {   'smiles': 'CN(CCC1=CC(=C(C=C1)Cl)Cl)CCN2CCCC2',
                                      'name': '2-(3,4-dichlorophenyl)-N-methyl-N-[2-(1-pyrrolidinyl)ethyl]ethanamine',
                                      'reason': 'No valid primary amine group '
                                                '(with two hydrogens and one '
                                                'substituent not involved in '
                                                'an amide) found.'},
                                  {   'smiles': 'O=C1C(C(=O)CC)=CN(CCC2=CC=CC=C2)C(C1(O)C)C(=CC(CC)C)C',
                                      'name': 'Neovasipyridone D',
                                      'reason': 'No valid primary amine group '
                                                '(with two hydrogens and one '
                                                'substituent not involved in '
                                                'an amide) found.'},
                                  {   'smiles': 'COC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=O)C=CC=C3[C@H]1N2CCC4=CC=CC=C4)CO',
                                      'name': 'LSM-12804',
                                      'reason': 'No valid primary amine group '
                                                '(with two hydrogens and one '
                                                'substituent not involved in '
                                                'an amide) found.'},
                                  {   'smiles': 'CC=CC1=CC=C2[C@@H]3[C@@H]([C@H]([C@@H](N3CCC4=CC=CC=C4)CN2C1=O)CO)C(=O)N(C)C',
                                      'name': 'LSM-14647',
                                      'reason': 'Molecule contains amide '
                                                'bond(s) typical of '
                                                'peptides/amides'},
                                  {   'smiles': 'CN(C)C(=O)NC1CC2CC1C1CCCC21',
                                      'name': 'Noruron',
                                      'reason': 'Molecule contains amide '
                                                'bond(s) typical of '
                                                'peptides/amides'},
                                  {   'smiles': 'CNCCc1ccc(O)c(Br)c1',
                                      'name': '3-Bromo-N-methyltyramine',
                                      'reason': 'No valid primary amine group '
                                                '(with two hydrogens and one '
                                                'substituent not involved in '
                                                'an amide) found.'},
                                  {   'smiles': 'CN[C@@H]1[C@H](O)[C@H](NC)[C@H]2O[C@]3(O)[C@@H](O[C@H](C)C=C3OC)O[C@@H]2[C@H]1O',
                                      'name': 'Spenolimycin',
                                      'reason': 'No valid primary amine group '
                                                '(with two hydrogens and one '
                                                'substituent not involved in '
                                                'an amide) found.'},
                                  {   'smiles': 'CCSC(=O)N(CC)C1CCCCC1',
                                      'name': 'Cycloate',
                                      'reason': 'Molecule contains amide '
                                                'bond(s) typical of '
                                                'peptides/amides'},
                                  {   'smiles': 'C[C@H](C(=O)N[C@@H](CC1=CNC2=CC=CC=C21)C(=O)O)NC(=O)[C@@H](CC3=CC=CC=C3)N',
                                      'name': 'sevadicin',
                                      'reason': 'Molecule contains amide '
                                                'bond(s) typical of '
                                                'peptides/amides'}],
    'attempt': 2,
    'reasoning': 'Below is our step‐by‐step reasoning followed by the complete '
                 'Python code.\n'
                 '\n'
                 'One hypothesis in our previous version is that trying to '
                 '“manually” count hydrogens and heavy‐atom neighbors (after '
                 'adding explicit hydrogens) may be too strict or unreliable. '
                 'Many molecules (especially aromatic amines) have nitrogen '
                 'atoms whose hydrogen counts (even after AddHs) do not '
                 '“cleanly” match our numeric criteria. In many cases the '
                 'underlying structure is indeed that of a primary amine '
                 '(R–NH2) as determined by substructure rather than '
                 'atom‐by‐atom counting. For example, aniline and related '
                 'aromatic amines should qualify even if their geometry and '
                 'explicit hydrogen assignments are impacted by conjugation. \n'
                 '\n'
                 'Our new approach uses RDKit SMARTS to directly search for a '
                 'primary amine pattern. We require that the nitrogen be '
                 'tri‐valent, have two attached hydrogens, and not be directly '
                 'bonded to a carbonyl (to avoid amides). In addition, if the '
                 'molecule has any amide bonds (which we flag via a separate '
                 'search), we will reject it outright. This way, we keep the '
                 'code simple and make the match less fragile to arbitrary '
                 'hydrogen counting. \n'
                 '\n'
                 'Below is the revised code in a single Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 95,
    'num_false_positives': 6910,
    'num_true_negatives': 135271,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.013561741613133477,
    'recall': 0.7983193277310925,
    'f1': 0.026670409882088714,
    'accuracy': 0.9512719606465214,
    'negative_predictive_value': 0.9998226098525445}