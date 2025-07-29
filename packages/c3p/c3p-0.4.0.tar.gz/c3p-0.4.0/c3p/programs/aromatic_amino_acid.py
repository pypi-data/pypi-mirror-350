"""
Classifies: CHEBI:33856 aromatic amino acid
"""
#!/usr/bin/env python3
"""
Classifies: Aromatic Amino Acid
Definition: An amino acid whose structure includes an aromatic ring.
Improved criteria:
  - Must contain a carboxyl (or carboxylate) group in the amino acid backbone.
  - Must contain an amino group (which may be N‐substituted) attached at the α–carbon.
  - Must contain at least one aromatic ring.
  - Must be a small molecule (heavy atom count <= 30) to avoid peptides and larger molecules.
The approach uses a backbone SMARTS that looks for the fragment:
   [NX3;!$(NC(=O))][C;H1](C(=O)[O;H1,-])
which captures the connectivity of most (non–glycine) amino acids.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_aromatic_amino_acid(smiles: str):
    """
    Determines if a molecule is an aromatic amino acid.
    
    To be classified as an aromatic amino acid, the molecule must:
      - Have an amino acid backbone with a nitrogen directly bound to an α–carbon
        that carries a carboxyl (or carboxylate) group.
      - Contain at least one aromatic ring.
      - Not be too large (heavy atom count <= 30).
    
    This method uses a backbone SMARTS pattern:
      [NX3;!$(NC(=O))][C;H1](C(=O)[O;H1,-])
    which will match both free and N–substituted amino groups.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule meets criteria for an aromatic amino acid, False otherwise.
        str: Explanation for the decision.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Add explicit hydrogens so that hydrogen counts are correct.
    mol = Chem.AddHs(mol)
    
    # Check molecular size to avoid peptides and larger biomolecules.
    heavy_atoms = mol.GetNumHeavyAtoms()
    if heavy_atoms > 30:
        return False, f"Molecule is too large (has {heavy_atoms} heavy atoms) to be a single amino acid"
    
    # Check for at least one aromatic ring.
    ring_info = mol.GetRingInfo()
    aromatic_ring_found = False
    for ring in ring_info.AtomRings():
        if len(ring) < 5:
            continue
        # Verify every atom in the ring is aromatic.
        if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            aromatic_ring_found = True
            break
    if not aromatic_ring_found:
        return False, "No aromatic ring found"
    
    # SMARTS pattern to capture the amino acid backbone:
    # [NX3;!$(NC(=O))] : A trivalent nitrogen not attached to a carbonyl (thus not an amide).
    # [C;H1]         : An α–carbon carrying exactly one hydrogen (typical for non–glycine residues).
    # (C(=O)[O;H1,-]) : A carboxyl group (which can be protonated or deprotonated).
    amino_acid_smarts = "[NX3;!$(NC(=O))][C;H1](C(=O)[O;H1,-])"
    aa_pattern = Chem.MolFromSmarts(amino_acid_smarts)
    if aa_pattern is None:
        return False, "Error in parsing amino acid SMARTS pattern"
    
    if not mol.HasSubstructMatch(aa_pattern):
        return False, "No amino acid backbone (N–α–C–(C=O)[O]) fragment found"
    
    return True, "Molecule contains an amino acid backbone and an aromatic ring, with appropriate size."

# Example usage (this example can be removed or commented out if using as a module)
if __name__ == "__main__":
    # Test examples: You can try with N-methyl-D-dopa and D-phenylalanine
    examples = {
        "N-methyl-D-dopa": "CN[C@H](CC1=CC=C(O)C(O)=C1)C(O)=O",
        "D-phenylalanine": "N[C@H](Cc1ccccc1)C(O)=O"
    }
    for name, smi in examples.items():
        result, reason = is_aromatic_amino_acid(smi)
        print(f"{name}: {result}\n  Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33856',
                          'name': 'aromatic amino acid',
                          'definition': 'An amino acid whose structure '
                                        'includes an aromatic ring.',
                          'parents': ['CHEBI:33659', 'CHEBI:33709'],
                          'xrefs': [   'KEGG:C01021',
                                       'Wikipedia:Aromatic_amino_acid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 57,
                           'log_lines_of_code': 4.04305126783455,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
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
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'items',
                                                 'GetNumHeavyAtoms',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'AddHs',
                                                 'GetIsAromatic',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles'],
                           'methods_called_count': 10,
                           'smarts_strings': ['amino_acid_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_aromatic_amino_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecule is too large (has '
                                          '{heavy_atoms} heavy atoms) to be a '
                                          'single amino acid"',
                                          'False, "No aromatic ring found"',
                                          'False, "Error in parsing amino acid '
                                          'SMARTS pattern"',
                                          'False, "No amino acid backbone '
                                          '(N–α–C–(C=O)[O]) fragment found"',
                                          'True, "Molecule contains an amino '
                                          'acid backbone and an aromatic ring, '
                                          'with appropriate size."'],
                           'returns_count': 6,
                           'complexity': 4.8086102535669095},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: CN[C@H](CC1=CC=C(O)C(O)=C1)C(O)=O '
               'NAME: N-methyl-D-dopa REASON: MISSED No free amino group (or '
               'N-H moiety) found\n'
               ' * SMILES: C1=CC(=C(C=C1I)F)NC2=C(C=CC(=C2F)F)C(=O)NOCC(CO)O '
               'NAME: '
               'N-(2,3-dihydroxypropoxy)-3,4-difluoro-2-(2-fluoro-4-iodoanilino)benzamide '
               'REASON: MISSED No carboxylic acid (or carboxylate) group '
               'found\n'
               ' * SMILES: N[C@H](Cc1ccccc1)C(O)=O NAME: D-phenylalanine '
               'REASON: MISSED No free amino group (or N-H moiety) found\n'
               ' * SMILES: CC(=O)Nc1c(I)cc(I)c(C(O)=O)c1I NAME: Acetrizoic '
               'acid REASON: MISSED No free amino group (or N-H moiety) found\n'
               ' * SMILES: Nc1cccc(c1)C(O)=O NAME: 3-aminobenzoic acid REASON: '
               'MISSED No free amino group (or N-H moiety) found\n'
               ' * SMILES: '
               'C(=C1C(N=C(S1)NC=2C=C(C(=CC2)Cl)C(=O)O)=O)(C=3OC(=CC3)C4=CC(=C(C=C4[N+]([O-])=O)C)C)[H] '
               'NAME: AMPK activator PT 1 REASON: MISSED Molecule is too large '
               '(has 34 heavy atoms) to be a single amino acid\n'
               ' * SMILES: N[C@@H](Cc1ccc(O)c(O)c1)C(O)=O NAME: L-dopa REASON: '
               'MISSED No free amino group (or N-H moiety) found\n'
               ' * SMILES: NC(Cc1ccc(OP(O)(O)=O)cc1)C(O)=O NAME: '
               'O(4)-phosphotyrosine REASON: MISSED No free amino group (or '
               'N-H moiety) found\n'
               ' * SMILES: Cc1cccc(Nc2ccccc2C(O)=O)c1C NAME: mefenamic acid '
               'REASON: MISSED No free amino group (or N-H moiety) found\n'
               ' * SMILES: Cc1cccc(C(O)=O)c1N NAME: 2-Amino-3-methylbenzoate '
               'REASON: MISSED No free amino group (or N-H moiety) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No aromatic ring found'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No amino acid backbone '
                                               '(N–α–C–(C=O)[O]) fragment '
                                               'found'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No aromatic ring found'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No amino acid backbone '
                                               '(N–α–C–(C=O)[O]) fragment '
                                               'found'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Molecule is too large (has 53 '
                                               'heavy atoms) to be a single '
                                               'amino acid'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Molecule is too large (has 36 '
                                               'heavy atoms) to be a single '
                                               'amino acid'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Molecule is too large (has 69 '
                                               'heavy atoms) to be a single '
                                               'amino acid'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No aromatic ring found'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No aromatic ring found'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No amino acid backbone '
                                               '(N–α–C–(C=O)[O]) fragment '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C1=CC(=C(C=C1I)F)NC2=C(C=CC(=C2F)F)C(=O)NOCC(CO)O',
                                      'name': 'N-(2,3-dihydroxypropoxy)-3,4-difluoro-2-(2-fluoro-4-iodoanilino)benzamide',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'CC(=O)Nc1c(I)cc(I)c(C(O)=O)c1I',
                                      'name': 'Acetrizoic acid',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'Nc1cccc(c1)C(O)=O',
                                      'name': '3-aminobenzoic acid',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'C(=C1C(N=C(S1)NC=2C=C(C(=CC2)Cl)C(=O)O)=O)(C=3OC(=CC3)C4=CC(=C(C=C4[N+]([O-])=O)C)C)[H]',
                                      'name': 'AMPK activator PT 1',
                                      'reason': 'Molecule is too large (has 34 '
                                                'heavy atoms) to be a single '
                                                'amino acid'},
                                  {   'smiles': 'Cc1cccc(Nc2ccccc2C(O)=O)c1C',
                                      'name': 'mefenamic acid',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'Cc1cccc(C(O)=O)c1N',
                                      'name': '2-Amino-3-methylbenzoate',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'CC(=O)NC1=CC=C(O)C(=C1)C(O)=O',
                                      'name': 'N-acetyl-5-aminosalicylic acid',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'C1=COC(=C1)NC(=O)C2=CC=C(C=C2)N',
                                      'name': '4-amino-N-(2-furanyl)benzamide',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'Cc1ccc(Cl)c(Nc2ccccc2C(O)=O)c1Cl',
                                      'name': 'meclofenamic acid',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'},
                                  {   'smiles': 'CC1=NC(=CC=C1)NC(=O)C2=CC(=C(C=C2)N(C)C3CCCCC3)[N+](=O)[O-]',
                                      'name': '4-[cyclohexyl(methyl)amino]-N-(6-methyl-2-pyridinyl)-3-nitrobenzamide',
                                      'reason': 'No amino acid backbone '
                                                '(N–α–C–(C=O)[O]) fragment '
                                                'found'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning before presenting the complete Python '
                 'code:\n'
                 '\n'
                 'Our previous attempt tried to check separately for a free '
                 'amino group, a carboxyl (or carboxylate) group, and an '
                 'aromatic ring. However, some structures commonly regarded as '
                 'aromatic amino acids (for example, N‐methyl‐D‐dopa) were '
                 'missed because the amino group was N‐alkylated (thus lacking '
                 'a free N–H) and the prior check looked only for a free (N–H) '
                 'moiety. In addition, a check on size as heavy atom count '
                 '(using a threshold of 30) helps rule out larger compounds '
                 'like peptides.\n'
                 '\n'
                 'An improved approach is to look for an amino acid “backbone” '
                 'substructure. In a typical amino acid (except glycine, which '
                 'is not aromatic) the nitrogen (which may be substituted) is '
                 'attached directly to an α–carbon that in turn is attached to '
                 'a carboxyl group. We can encapsulate this connectivity in a '
                 'SMARTS pattern. For our purposes we use a pattern such as\n'
                 '\n'
                 '  [NX3;!$(NC(=O))][C;H1](C(=O)[O;H1,-])\n'
                 '\n'
                 'This pattern means:\n'
                 '\u2003• a trivalent nitrogen that is not directly bonded to '
                 'a carbonyl (thereby avoiding amide nitrogens),\n'
                 '\u2003• attached to a carbon that has exactly one hydrogen '
                 '(the α–carbon in natural (non–glycine) amino acids)\n'
                 '\u2003• and then that carbon is bound to a carboxyl group '
                 '(which can be protonated or deprotonated).\n'
                 '\n'
                 'We then also check that there is at least one aromatic ring '
                 '(of at least five atoms where every ring atom is aromatic). '
                 'Also, we enforce an upper bound on heavy atom count so that '
                 'larger biomolecules (e.g. peptides) do not pass the test.\n'
                 '\n'
                 'Below is the complete single Python code block.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 28,
    'num_false_positives': 492,
    'num_true_negatives': 141720,
    'num_false_negatives': 60,
    'num_negatives': None,
    'precision': 0.05384615384615385,
    'recall': 0.3181818181818182,
    'f1': 0.09210526315789475,
    'accuracy': 0.996120871398454,
    'negative_predictive_value': 0.9995768091409225}