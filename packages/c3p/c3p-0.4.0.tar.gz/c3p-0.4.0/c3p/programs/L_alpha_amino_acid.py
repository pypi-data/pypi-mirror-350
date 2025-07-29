"""
Classifies: CHEBI:15705 L-alpha-amino acid
"""
#!/usr/bin/env python
"""
Classifies: L-alpha-amino acid
Definition: Any alpha-amino acid having L-configuration at the alpha-carbon.
A free L-alpha-amino acid is defined here as a molecule with a free amino acid backbone,
i.e., an unmodified (non-amidated) amino group attached to a chiral alpha-carbon that bears
a protonated carboxylic acid group (-C(=O)O with an –OH), and with exactly one such backbone.
The alpha-carbon is assumed to have the CIP code "S" corresponding to the L configuration.
"""

from rdkit import Chem

def is_L_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is a free L-alpha-amino acid based on its SMILES string.
    Checks for:
      1. A free amino group that is not amidated.
      2. A chiral alpha-carbon attached to a protonated carboxylic acid (C(=O)[O;H1]).
      3. Exactly one such amino acid backbone in the molecule (to avoid peptides).
      4. The alpha-carbon has a CIP code of "S" (i.e. L-configuration).
      
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is a free L-alpha-amino acid, False otherwise.
        str: Explanation for the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Assign stereochemistry and compute CIP codes.
    Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # Define SMARTS patterns for the amino acid backbone:
    # The pattern looks for an amino group [NX3] (with one or two hydrogens) that is NOT bound
    # to a carbonyl (to ensure it is free and not in an amide). The amino is bonded to a chiral alpha-carbon,
    # which is in turn bonded to a carboxylic acid group (C(=O)[O;H1] ensures that one oxygen has a hydrogen).
    # We define two patterns to capture either possible chiral notations (@ or @@). In both,
    # the ordering is: atom0: amino nitrogen, atom1: alpha-carbon, atom2: carbonyl carbon.
    pattern1 = Chem.MolFromSmarts("[NX3;H2,H1;!$(N-C(=O))]-[C@H]([#6])-[C](=O)[O;H1]")
    pattern2 = Chem.MolFromSmarts("[NX3;H2,H1;!$(N-C(=O))]-[C@@H]([#6])-[C](=O)[O;H1]")
    
    # Get substructure matches (using useChirality so that pattern matching respects stereochemistry).
    matches1 = mol.GetSubstructMatches(pattern1, useChirality=True)
    matches2 = mol.GetSubstructMatches(pattern2, useChirality=True)
    all_matches = matches1 + matches2
    
    # Deduplicate matches by converting each match (a tuple of atom indices) into a sorted tuple.
    unique_matches = set()
    for m in all_matches:
        unique_matches.add(tuple(sorted(m)))
    
    if not unique_matches:
        return False, "Alpha-amino acid backbone (free amino group and free carboxylic acid) not found"
    
    if len(unique_matches) > 1:
        return False, f"Found {len(unique_matches)} amino acid backbones; likely a peptide, not a single amino acid"
    
    # We now have exactly one unique backbone. We need to check the chirality of the alpha-carbon.
    # We know that in our SMARTS, the second atom (index 1 in the match) is the chiral alpha-carbon.
    match = list(unique_matches)[0]
    # To preserve the SMARTS ordering, we retrieve the match using the SMARTS match from pattern1 if possible.
    # Otherwise, we use an arbitrary ordering from unique_matches.
    # NOTE: Since our patterns were defined with three atoms, we assume the center atom (alpha-carbon) is the second in our match.
    # Because we deduplicated by sorted order, we must find the corresponding match from the original list.
    target_alpha_idx = None
    for m in all_matches:
        if tuple(sorted(m)) == match:
            target_alpha_idx = m[1]  # second atom in the ordering from the SMARTS
            break
    if target_alpha_idx is None:
        return False, "Alpha-amino acid backbone detected but could not retrieve alpha-carbon information"
    
    alpha_atom = mol.GetAtomWithIdx(target_alpha_idx)
    if not alpha_atom.HasProp("_CIPCode"):
        return False, "Alpha-carbon has no CIP code; cannot determine configuration"
    cip = alpha_atom.GetProp("_CIPCode")
    if cip == "S":
        return True, "Found a free alpha-amino acid backbone with L (S CIP) configuration at the alpha-carbon"
    else:
        return False, f"Alpha-amino acid backbone found but alpha-carbon CIP code is '{cip}', not 'S'"

# Example usage:
# test_smiles = "N[C@@H](CC(=O)c1cc(O)ccc1N)C(O)=O"  # 5-hydroxy-L-kynurenine
# result, reason = is_L_alpha_amino_acid(test_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15705',
                          'name': 'L-alpha-amino acid',
                          'definition': 'Any alpha-amino acid having '
                                        'L-configuration at the alpha-carbon.',
                          'parents': ['CHEBI:33704'],
                          'xrefs': ['KEGG:C00151'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 60,
                           'log_lines_of_code': 4.0943445622221,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
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
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetProp',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'AssignStereochemistry',
                                                 'GetAtomWithIdx',
                                                 'add',
                                                 'HasProp'],
                           'methods_called_count': 8,
                           'smarts_strings': [   '[NX3;H2,H1;!$(N-C(=O))]-[C@H]([#6])-[C](=O)[O;H1]',
                                                 '[NX3;H2,H1;!$(N-C(=O))]-[C@@H]([#6])-[C](=O)[O;H1]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_L_alpha_amino_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Alpha-amino acid backbone '
                                          '(free amino group and free '
                                          'carboxylic acid) not found"',
                                          'False, f"Found '
                                          '{len(unique_matches)} amino acid '
                                          'backbones; likely a peptide, not a '
                                          'single amino acid"',
                                          'False, "Alpha-amino acid backbone '
                                          'detected but could not retrieve '
                                          'alpha-carbon information"',
                                          'False, "Alpha-carbon has no CIP '
                                          'code; cannot determine '
                                          'configuration"',
                                          'True, "Found a free alpha-amino '
                                          'acid backbone with L (S CIP) '
                                          'configuration at the alpha-carbon"',
                                          'False, f"Alpha-amino acid backbone '
                                          'found but alpha-carbon CIP code is '
                                          '\'{cip}\', not \'S\'"'],
                           'returns_count': 7,
                           'complexity': 4.61886891244442},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: N[C@@H](CC(=O)c1cc(O)ccc1N)C(O)=O '
               'NAME: 5-hydroxy-L-kynurenine REASON: MISSED Found 2 amino acid '
               'backbones; likely a peptide, not a single amino acid\n'
               ' * SMILES: N[C@@H](CC(=C)C(N)=O)C(O)=O NAME: '
               '4-methylene-L-glutamine REASON: MISSED Found 2 amino acid '
               'backbones; likely a peptide, not a single amino acid\n'
               ' * SMILES: CC[C@H](N)C(O)=O NAME: L-alpha-aminobutyric acid '
               'REASON: MISSED Found 2 amino acid backbones; likely a peptide, '
               'not a single amino acid\n'
               ' * SMILES: O=C(O)[C@@H](N)CCC1C=CC(N)C=C1 NAME: Amiclenomycin '
               'REASON: MISSED Found 2 amino acid backbones; likely a peptide, '
               'not a single amino acid\n'
               ' * SMILES: N[C@@H](CCCCC(O)=O)C(O)=O NAME: L-2-aminopimelic '
               'acid REASON: MISSED Found 2 amino acid backbones; likely a '
               'peptide, not a single amino acid\n'
               ' * SMILES: N[C@@H](CCCCNC(O)=O)C(O)=O NAME: '
               'N(6)-carboxy-L-lysine REASON: MISSED Found 2 amino acid '
               'backbones; likely a peptide, not a single amino acid\n'
               ' * SMILES: CNC(=O)C[C@H](N)C(O)=O NAME: '
               'N(4)-methyl-L-asparagine REASON: MISSED Found 2 amino acid '
               'backbones; likely a peptide, not a single amino acid\n'
               ' * SMILES: N[C@@H](COS(O)(=O)=O)C(O)=O NAME: L-serine '
               'O-sulfate REASON: MISSED Found 2 amino acid backbones; likely '
               'a peptide, not a single amino acid\n'
               ' * SMILES: N[C@@H](CCC(N)=O)C(O)=O NAME: L-glutamine REASON: '
               'MISSED Found 2 amino acid backbones; likely a peptide, not a '
               'single amino acid\n'
               ' * SMILES: Cn1cncc1C[C@H](N)C(O)=O NAME: '
               'N(pros)-methyl-L-histidine REASON: MISSED Found 2 amino acid '
               'backbones; likely a peptide, not a single amino acid\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Alpha-amino acid backbone '
                                               '(free amino group and free '
                                               'carboxylic acid) not found'}],
    'sample_false_negatives': [   {   'smiles': 'S1C(N[C@@H](C1)C(O)=O)CCCCCCCCCCC',
                                      'name': '4-thiazolidinecarboxylic acid, '
                                              '2-undecyl-, (4r)-',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"},
                                  {   'smiles': 'N[C@@H](CS[C@H](\\C=C\\C=C\\C=C/CCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O',
                                      'name': '16-carboxy-17,18,19,20-tetranor-leukotriene '
                                              'E3',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"},
                                  {   'smiles': 'N[C@@H](CS[C@H](\\C=C\\C=C\\C=C/CC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O',
                                      'name': '14-carboxy-15,16,17,18,19,20-hexanor-leukotriene '
                                              'E3',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"},
                                  {   'smiles': 'OC([C@@H](N)CSC(=O)CCCCCCC)=O',
                                      'name': 'S-octanoyl-L-cysteine',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CSC[C@H](N)C(O)=O',
                                      'name': 'S-geranylgeranyl-L-cysteine',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"},
                                  {   'smiles': 'N[C@@H](Cc1nc[nH]c1S(=O)C[C@H](N)C(O)=O)C(O)=O',
                                      'name': 'S-(5-histidyl)cysteine '
                                              'sulfoxide',
                                      'reason': 'Found 2 amino acid backbones; '
                                                'likely a peptide, not a '
                                                'single amino acid'},
                                  {   'smiles': 'C([C@@H](C([O-])=O)[NH3+])C=1N(C=NC1)C',
                                      'name': 'N(pros)-methyl-L-histidine '
                                              'zwitterion',
                                      'reason': 'Alpha-amino acid backbone '
                                                '(free amino group and free '
                                                'carboxylic acid) not found'},
                                  {   'smiles': 'N[C@@H](CSCC(O)=O)C(O)=O',
                                      'name': 'S-carboxymethyl-L-cysteine',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"},
                                  {   'smiles': 'CN(C)[C@@H](COP(O)(=O)OCCNC(N)=N)C(O)=O',
                                      'name': 'Thalassemine',
                                      'reason': 'Alpha-amino acid backbone '
                                                '(free amino group and free '
                                                'carboxylic acid) not found'},
                                  {   'smiles': 'N[C@@H](CS\\C(Cc1c[nH]c2ccccc12)=N/O)C(O)=O',
                                      'name': 'S-(Indolylmethylthiohydroximoyl)-L-cysteine',
                                      'reason': 'Alpha-amino acid backbone '
                                                'found but alpha-carbon CIP '
                                                "code is 'R', not 'S'"}],
    'attempt': 2,
    'reasoning': 'Below is my reasoning before the code: \n'
                 '\n'
                 'The previous attempt’s SMARTS patterns were written so that '
                 'the amino acid backbone was found twice in many examples '
                 '(likely because overlapping descriptions of the atoms '
                 'produced two distinct matches). To fix this we need to (a) '
                 'make our SMARTS pattern as specific as possible and (b) '
                 '“uniquify” the backbone hits so that if the same set of '
                 'atoms is matched in two different ways, we count it only '
                 'once. In our solution we define two SMARTS patterns (one for '
                 'each chiral encoding) and then deduplicate results by '
                 'sorting and creating a set of matched atom indices. Finally, '
                 'if we have exactly one unique backbone match then we check '
                 'for the CIP code on the alpha‐carbon (with index 1 in our '
                 'SMARTS match) to ensure that its configuration is “S” (L '
                 'configuration). If any step fails, we return False with an '
                 'explanation. \n'
                 '\n'
                 'Below is the complete Python code in a single code block.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 271,
    'num_false_positives': 936,
    'num_true_negatives': 141016,
    'num_false_negatives': 77,
    'num_negatives': None,
    'precision': 0.22452361226180614,
    'recall': 0.7787356321839081,
    'f1': 0.34855305466237946,
    'accuracy': 0.9928812368236121,
    'negative_predictive_value': 0.9994542606649515}