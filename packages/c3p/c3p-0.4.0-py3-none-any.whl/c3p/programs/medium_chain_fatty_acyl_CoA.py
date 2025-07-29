"""
Classifies: CHEBI:61907 medium-chain fatty acyl-CoA
"""
"""
Classifies: medium-chain fatty acyl-CoA

A medium-chain fatty acyl-CoA is defined as a fatty acyl-CoA that results from the
formal condensation of the thiol group of coenzyme A with the carboxy group of any
medium-chain fatty acid.

Heuristic checks:
  (i) The molecule must contain a CoA-like fragment; here we require detection of
      the adenine substructure (a decorated purine ring) commonly present in CoA.
  (ii) A thioester linkage [C(=O)S] must be present.
  (iii) After “cutting” the thioester bond, the isolated acyl fragment (the one that
        contains the carbonyl but not the sulfur from the thioester) should be aliphatic,
        with no aromatic atoms or rings, and should have a total of 6–12 carbon atoms.
        
Note: This heuristic is rough and may reject borderline cases.
"""

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

def is_medium_chain_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a medium‐chain fatty acyl‐CoA based on its SMILES.

    Steps:
      1. Parse the molecule.
      2. Check for a CoA-like fragment by requiring the adenine substructure.
         A loose SMARTS "c1nc2c(n1)nc(nc2)" is used to catch decorated adenine rings.
      3. Identify the thioester bond using the SMARTS pattern [CX3](=O)[S].
      4. Mark the carbonyl atom (acyl side) and the sulfur atom (CoA side).
      5. Fragment the molecule on the thioester bond.
      6. Identify the fragment containing the acyl (fatty acid) chain: it should contain
         the carbonyl marker but not the thioester sulfur marker.
      7. Count the number of carbon atoms in that fragment.
      8. Verify that the acyl fragment is aliphatic (i.e. without aromatic carbons or rings).

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if classified as a medium-chain fatty acyl-CoA, False otherwise.
        str: Explanation for the classification.
    """
    
    # Step 1: Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Step 2: Look for a CoA-like fragment by detecting an adenine substructure.
    # Use a less strict SMARTS so variations like "n1cnc2c(N)ncnc12" are detected.
    adenine_smarts = "c1nc2c(n1)nc(nc2)"
    adenine = Chem.MolFromSmarts(adenine_smarts)
    if adenine is None or not mol.HasSubstructMatch(adenine):
        return False, "Coenzyme A adenine substructure not detected"
    
    # Step 3: Locate the thioester group [CX3](=O)[S]
    thioester_smarts = "[CX3](=O)[S]"
    thioester = Chem.MolFromSmarts(thioester_smarts)
    th_matches = mol.GetSubstructMatches(thioester)
    if not th_matches:
        return False, "Thioester group (C(=O)S) not found"
    
    # For this heuristic, we take the first thioester match.
    # Each match yields a tuple of three atom indices: (carbonyl carbon, oxygen of C=O, sulfur)
    carbonyl_idx, _, sulfur_idx = th_matches[0]
    
    # Step 4: Mark the key atoms in the molecule for later identification.
    carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
    sulfur_atom = mol.GetAtomWithIdx(sulfur_idx)
    carbonyl_atom.SetProp("acyl_marker", "yes")
    sulfur_atom.SetProp("thioester_S", "yes")
    
    # Identify the bond connecting the carbonyl carbon and the sulfur atom.
    bond = mol.GetBondBetweenAtoms(carbonyl_idx, sulfur_idx)
    if bond is None:
        return False, "Thioester bond not properly defined"
    bond_idx = bond.GetIdx()
    
    # Step 5: Fragment the molecule on the thioester bond.
    fragmented = Chem.FragmentOnBonds(mol, [bond_idx], addDummies=True)
    frags = Chem.GetMolFrags(fragmented, asMols=True, sanitizeFrags=True)
    
    # Step 6: Determine which fragment corresponds to the acyl (fatty acid) chain.
    # We choose the fragment that has the carbonyl marker (acyl side) but not the sulfur marker.
    acyl_frag = None
    for frag in frags:
        has_acyl_marker = any(atom.HasProp("acyl_marker") for atom in frag.GetAtoms())
        has_thioester_S = any(atom.HasProp("thioester_S") for atom in frag.GetAtoms())
        if has_acyl_marker and not has_thioester_S:
            acyl_frag = frag
            break
    if acyl_frag is None:
        return False, "Could not isolate acyl (fatty acid) fragment from the thioester bond"
    
    # Step 7: Count carbon atoms in the acyl fragment.
    carbon_count = sum(1 for atom in acyl_frag.GetAtoms() if atom.GetAtomicNum() == 6)
    if not (6 <= carbon_count <= 12):
        return False, f"Acyl chain has {carbon_count} carbons, not in the medium-chain range (6-12)"
    
    # Step 8: Ensure that the acyl fragment is aliphatic:
    # It should not contain aromatic carbons or any atoms in rings.
    for atom in acyl_frag.GetAtoms():
        if atom.GetAtomicNum() == 6:  # check carbons
            if atom.GetIsAromatic():
                return False, "Acyl fragment contains aromatic carbon(s), not typical for fatty acyl chains"
            if atom.IsInRing():
                return False, "Acyl fragment contains ring atoms, expected a linear (or branched) chain"
    
    return True, f"Detected medium-chain fatty acyl-CoA with an acyl chain of {carbon_count} carbons"

# Example usage (for testing):
if __name__ == "__main__":
    # Test with one example: hexanoyl-CoA.
    test_smiles = "CCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12"
    result, explanation = is_medium_chain_fatty_acyl_CoA(test_smiles)
    print(result, explanation)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61907',
                          'name': 'medium-chain fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA that results from '
                                        'the formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any medium-chain fatty acid.',
                          'parents': ['CHEBI:37554'],
                          'xrefs': [   'PMID:11027146',
                                       'PMID:1309181',
                                       'PMID:19170545',
                                       'PMID:8218225',
                                       'PMID:8267794'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 79,
                           'log_lines_of_code': 4.3694478524670215,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 3,
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
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem, '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'HasProp',
                                                 'FragmentOnBonds',
                                                 'GetAtomicNum',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'SetProp',
                                                 'GetIdx',
                                                 'GetIsAromatic',
                                                 'GetMolFrags',
                                                 'IsInRing',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtoms',
                                                 'GetBondBetweenAtoms'],
                           'methods_called_count': 15,
                           'smarts_strings': [   'adenine_smarts',
                                                 'thioester_smarts'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_medium_chain_fatty_acyl_CoA(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Coenzyme A adenine '
                                          'substructure not detected"',
                                          'False, "Thioester group (C(=O)S) '
                                          'not found"',
                                          'False, "Thioester bond not properly '
                                          'defined"',
                                          'False, "Could not isolate acyl '
                                          '(fatty acid) fragment from the '
                                          'thioester bond"',
                                          'False, f"Acyl chain has '
                                          '{carbon_count} carbons, not in the '
                                          'medium-chain range (6-12)"',
                                          'False, "Acyl fragment contains '
                                          'aromatic carbon(s), not typical for '
                                          'fatty acyl chains"',
                                          'False, "Acyl fragment contains ring '
                                          'atoms, expected a linear (or '
                                          'branched) chain"',
                                          'True, f"Detected medium-chain fatty '
                                          'acyl-CoA with an acyl chain of '
                                          '{carbon_count} carbons"'],
                           'returns_count': 9,
                           'complexity': 6.673889570493404},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C(C(CCCCCCCC)C)(C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O)O '
               'NAME: 2-hydroxy-3-methylundecanoyl-CoA REASON: MISSED Coenzyme '
               'A adenine substructure not detected\n'
               ' * SMILES: '
               'CCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: heptanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'CC\\C=C/CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (Z)-hex-3-enoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'CCCCCCCCC[C@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (S)-3-hydroxylauroyl-CoA REASON: MISSED Coenzyme A '
               'adenine substructure not detected\n'
               ' * SMILES: '
               'C(C(CCCCCC)C)C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O '
               'NAME: 3-methylnonanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'C(C(CCCCCCCCC)C)C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O '
               'NAME: 3-methyldodecanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'CCCCCCCC(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-hydroxydecanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'CCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: nonanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'CCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: hexanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               ' * SMILES: '
               'CCCCCSCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-thiaoctanoyl-CoA REASON: MISSED Coenzyme A adenine '
               'substructure not detected\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Coenzyme A adenine '
                                               'substructure not detected'}],
    'sample_false_negatives': [   {   'smiles': 'C(C(CCCCCCCCC)C)C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O',
                                      'name': '3-methyldodecanoyl-CoA',
                                      'reason': 'Acyl chain has 13 carbons, '
                                                'not in the medium-chain range '
                                                '(6-12)'},
                                  {   'smiles': 'CC(C)CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': 'isotridecanoyl-CoA',
                                      'reason': 'Acyl chain has 13 carbons, '
                                                'not in the medium-chain range '
                                                '(6-12)'}],
    'attempt': 3,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'The previous attempt always failed in the first step because '
                 'our strict adenine (purine) SMARTS ("n1cnc2n(cnc12)") was '
                 'not catching the coenzyme A fragment. In many of the '
                 'provided SMILES the adenine ring is decorated (for example '
                 '“n1cnc2c(N)ncnc12”), so a looser match is needed. In the new '
                 'version I employ an alternative SMARTS pattern '
                 '("c1nc2c(n1)nc(nc2)") that is less restrictive and should '
                 'match decorated adenine rings. The rest of the workflow '
                 'remains similar: we check for a CoA‐like fragment (by '
                 'detecting an adenine substructure), then look for the '
                 'thioester group ([CX3](=O)[S]), mark the carbonyl and sulfur '
                 'atoms, break the bond between them, isolate the acyl '
                 'fragment (the one that carried the carbonyl but not the '
                 'thioester sulfur), count its carbon atoms (expecting between '
                 '6 and 12), and finally ensure it is aliphatic without '
                 'aromatic or ring atoms.\n'
                 '\n'
                 'Below is the complete single Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 46,
    'num_false_positives': 172,
    'num_true_negatives': 142080,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.21100917431192662,
    'recall': 0.9583333333333334,
    'f1': 0.3458646616541354,
    'accuracy': 0.9987772312016866,
    'negative_predictive_value': 0.9999859236215707}