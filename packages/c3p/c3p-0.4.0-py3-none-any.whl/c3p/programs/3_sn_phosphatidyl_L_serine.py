"""
Classifies: CHEBI:11750 3-sn-phosphatidyl-L-serine
"""
"""
Classifies: 3-sn-phosphatidyl-L-serine
Definition:
  A 3-sn-glycerophosphoserine compound having acyl substituents at the 1- and 2-hydroxy positions.
Heuristic:
  1. Parse the SMILES and ensure at least one phosphorus atom is present.
  2. Confirm the presence of a serine fragment (using a simplified SMARTS: C(N)C(=O)O).
  3. For every ester bond (a single bond between a carbonyl carbon and an oxygen) in which:
       a. The carbonyl carbon has a double-bonded oxygen (confirming an ester carbonyl),
       b. The linking oxygen (which bridges the fatty acyl chain and the glycerol backbone)
          is connected via a short path (up to 5 bonds) to a phosphorus atom,
     follow from the carbonyl carbon the acyl chain branch (the neighbor opposite the linking oxygen)
     and count only contiguous carbon atoms.
  4. Accept the ester as valid if the acyl chain (including the carbonyl carbon) has a chain length of at least 6.
  5. Only if exactly 2 valid acyl chains are found is the molecule classified as a 3-sn-phosphatidyl-L-serine.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_3_sn_phosphatidyl_L_serine(smiles: str):
    """
    Determines if a molecule is a 3-sn-phosphatidyl-L-serine based on its SMILES string.
    Criteria:
     - The molecule must contain at least one phosphorus atom.
     - A serine fragment matching 'C(N)C(=O)O' must be present.
     - Exactly 2 ester bonds must be found in which:
         * The ester consists of a carbonyl carbon (which has a double-bonded oxygen)
           connected to a linking oxygen via a single bond.
         * The linking oxygen is connected (via a short path of at most 5 bonds) to a phosphorus atom.
         * Following the carbonyl carbon in the acyl branch (the bond not going to the linking oxygen)
           yields a contiguous chain of carbons (chain length including the carbonyl ≥ 6).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a 3-sn-phosphatidyl-L-serine, else False.
        str: Explanation of the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Ensure at least one phosphorus (P atomic number 15) exists.
    if not any(atom.GetAtomicNum() == 15 for atom in mol.GetAtoms()):
        return False, "Missing phosphorus (P) required for the phosphoglycerol head-group"
    
    # Look for a serine fragment using a simple SMARTS pattern.
    serine_smarts = "C(N)C(=O)O"
    serine_pat = Chem.MolFromSmarts(serine_smarts)
    if serine_pat is None:
        return False, "Internal error processing serine pattern"
    if not mol.HasSubstructMatch(serine_pat):
        return False, "Serine fragment (C(N)C(=O)O) not found in molecule"
    
    # Helper: Perform depth-first search to count contiguous carbons in the acyl chain.
    def dfs_chain_length(start_idx, banned):
        max_length = 0
        stack = [(start_idx, 0, set())]  # (current atom index, current chain length, visited set)
        while stack:
            cur_idx, cur_length, visited = stack.pop()
            if cur_idx in visited:
                continue
            visited = visited | {cur_idx}
            cur_length += 1
            if cur_length > max_length:
                max_length = cur_length
            atom = mol.GetAtomWithIdx(cur_idx)
            # Traverse only to carbon neighbors that are not banned.
            for nbr in atom.GetNeighbors():
                if nbr.GetAtomicNum() == 6 and nbr.GetIdx() not in banned:
                    stack.append((nbr.GetIdx(), cur_length, visited))
        return max_length

    # Helper: Check if a given oxygen is connected to a phosphorus atom via a path with at most max_bonds.
    def oxygen_connected_to_phosphorus(o_atom, max_bonds=5):
        for atom in mol.GetAtoms():
            if atom.GetAtomicNum() == 15:  # phosphorus
                try:
                    # GetShortestPath returns a tuple of atom indices
                    path = Chem.GetShortestPath(mol, o_atom.GetIdx(), atom.GetIdx())
                    if path and (len(path) - 1) <= max_bonds:
                        return True
                except Exception:
                    continue
        return False

    valid_acyl_count = 0
    counted_esters = set()  # To avoid double-counting same ester bond.
    
    # Iterate over all bonds to detect candidate ester bonds.
    for bond in mol.GetBonds():
        # Consider only single bonds (the linking bond in an ester is single).
        if bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
            continue
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        
        # Identify a candidate: one atom must be a carbon (potential carbonyl) and the other oxygen.
        if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 8:
            carbonyl = a1
            linking_oxygen = a2
        elif a2.GetAtomicNum() == 6 and a1.GetAtomicNum() == 8:
            carbonyl = a2
            linking_oxygen = a1
        else:
            continue
        
        # Confirm that the carbonyl carbon has a double-bonded oxygen.
        found_double = False
        for nbr in carbonyl.GetNeighbors():
            b = mol.GetBondBetweenAtoms(carbonyl.GetIdx(), nbr.GetIdx())
            if nbr.GetAtomicNum() == 8 and b is not None and b.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                found_double = True
                break
        if not found_double:
            continue
        
        # Verify that the linking oxygen is connected to phosphorus with a path of ≤5 bonds.
        if not oxygen_connected_to_phosphorus(linking_oxygen, max_bonds=5):
            continue
        
        # From the carbonyl carbon, select the neighbor that is not the linking oxygen and not the double-bonded oxygen.
        acyl_start = None
        for nbr in carbonyl.GetNeighbors():
            if nbr.GetIdx() == linking_oxygen.GetIdx():
                continue
            b = mol.GetBondBetweenAtoms(carbonyl.GetIdx(), nbr.GetIdx())
            # Skip the double-bonded oxygen.
            if nbr.GetAtomicNum() == 8 and b is not None and b.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                continue
            if nbr.GetAtomicNum() == 6:
                acyl_start = nbr
                break
        if acyl_start is None:
            continue
        
        # Use a unique identifier for the ester bond to avoid double-counting.
        bond_id = tuple(sorted((carbonyl.GetIdx(), linking_oxygen.GetIdx())))
        if bond_id in counted_esters:
            continue
        counted_esters.add(bond_id)
        
        # Count the acyl chain length: include the carbonyl carbon plus contiguous carbons from the acyl branch.
        chain_length = 1 + dfs_chain_length(acyl_start.GetIdx(), banned={carbonyl.GetIdx()})
        if chain_length >= 6:
            valid_acyl_count += 1

    if valid_acyl_count != 2:
        return False, f"Expected 2 acyl groups with chain length ≥6 in the ester bonds anchored to the phosphate backbone; found {valid_acyl_count}"
    
    return True, "Molecule contains a phosphoserine head-group with exactly 2 acyl groups anchored to the phosphoglycerol backbone"

# Example usage (for testing – these may be commented out in production):
if __name__ == "__main__":
    examples = [
        ("1,2-distearoyl-sn-glycero-3-phosphoserine", "CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCCCCCCCCCCCC"),
        ("1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine", "CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC")
    ]
    for name, smi in examples:
        result, reason = is_3_sn_phosphatidyl_L_serine(smi)
        print(name, "->", result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:11750',
                          'name': '3-sn-phosphatidyl-L-serine',
                          'definition': 'A 3-sn-glycerophosphoserine compound '
                                        'having acyl substituents at the 1- '
                                        'and 2-hydroxy positions.',
                          'parents': ['CHEBI:18303'],
                          'xrefs': [   'KEGG:C02737',
                                       'LIPID_MAPS_instance:LMGP03010000',
                                       'PMID:16341241'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 123,
                           'log_lines_of_code': 4.812184355372417,
                           'indent_by_line': [   1,
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
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetEndAtom',
                                                 'GetBondType',
                                                 'GetBonds',
                                                 'GetAtoms',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetShortestPath',
                                                 'GetBondBetweenAtoms',
                                                 'append',
                                                 'MolFromSmarts',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'GetBeginAtom',
                                                 'add',
                                                 'pop'],
                           'methods_called_count': 17,
                           'smarts_strings': ['serine_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_3_sn_phosphatidyl_L_serine(smiles: '
                                       'str):',
                                       'dfs_chain_length(start_idx, banned):',
                                       'oxygen_connected_to_phosphorus(o_atom, '
                                       'max_bonds=5):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Missing phosphorus (P) '
                                          'required for the phosphoglycerol '
                                          'head-group"',
                                          'False, "Internal error processing '
                                          'serine pattern"',
                                          'False, "Serine fragment '
                                          '(C(N)C(=O)O) not found in molecule"',
                                          'max_length',
                                          'True',
                                          'False',
                                          'False, f"Expected 2 acyl groups '
                                          'with chain length ≥6 in the ester '
                                          'bonds anchored to the phosphate '
                                          'backbone; found {valid_acyl_count}"',
                                          'True, "Molecule contains a '
                                          'phosphoserine head-group with '
                                          'exactly 2 acyl groups anchored to '
                                          'the phosphoglycerol backbone"'],
                           'returns_count': 9,
                           'complexity': 7.962436871074483},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCCCCCCCCCCCC '
               'NAME: 1,2-distearoyl-sn-glycero-3-phosphoserine REASON: MISSED '
               'Expected 2 acyl groups with chain length ≥6 in the ester bonds '
               'anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: 1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine '
               'REASON: MISSED Expected 2 acyl groups with chain length ≥6 in '
               'the ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'P(=O)(OC[C@H](OC(CCCCCNC=1C2=NON=C2C(=CC1)[N+]([O-])=O)=O)COC(CCCCCCC/C=C\\CCCCCCCC)=O)(OC[C@@H](C(O)=O)N)O '
               'NAME: '
               '1-oleoyl-2-{6-[(7-nitro-2-1,3-benzoxadiazol-4-yl)amino]hexanoyl}-sn-glycero-3-phospho-L-serine '
               'REASON: MISSED Expected 2 acyl groups with chain length ≥6 in '
               'the ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCCCCCC '
               'NAME: 1,2-dilauroyl-sn-glycero-3-phosphoserine REASON: MISSED '
               'Expected 2 acyl groups with chain length ≥6 in the ester bonds '
               'anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1-oleoyl-2-linoleoyl-sn-glycero-3-phospho-L-serine '
               'REASON: MISSED Expected 2 acyl groups with chain length ≥6 in '
               'the ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-heptadecanoyl-2-arachidonoyl-sn-glycero-3-phosphoserine '
               'REASON: MISSED Expected 2 acyl groups with chain length ≥6 in '
               'the ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCC\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-(8Z,11Z,14Z-icosatrienoyl)-sn-glycero-3-phosphoserine '
               'REASON: MISSED Expected 2 acyl groups with chain length ≥6 in '
               'the ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)COP(O)(=O)OC[C@H](N)C(O)=O '
               'NAME: 1-oleoyl-2-stearoyl-sn-glycero-3-phospho-L-serine '
               'REASON: MISSED Expected 2 acyl groups with chain length ≥6 in '
               'the ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1,2-dioleoyl-sn-glycero-3-phospho-L-serine REASON: '
               'MISSED Expected 2 acyl groups with chain length ≥6 in the '
               'ester bonds anchored to the phosphate backbone; found 1\n'
               ' * SMILES: '
               'C([C@](COP(O)(=O)OC[C@@](COC(=O)CCCCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCCCCCCC)[H])(N)[H])(=O)O '
               'NAME: PS(18:0/20:0) REASON: MISSED Expected 2 acyl groups with '
               'chain length ≥6 in the ester bonds anchored to the phosphate '
               'backbone; found 1\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Missing phosphorus (P) '
                                               'required for the '
                                               'phosphoglycerol head-group'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Serine fragment (C(N)C(=O)O) '
                                               'not found in molecule'}],
    'sample_false_negatives': [],
    'attempt': 5,
    'reasoning': 'We can hypothesize that the previous approach was too strict '
                 'when “anchoring” the acyl ester oxygen to the phosphate. In '
                 'a true phosphatidylserine the two acyl substituents are at '
                 'the sn‑1 and sn‑2 positions of a glycerol whose sn‑3 bears '
                 'the phosphate (and eventually the serine head‐group). '
                 'Because the sn‑1 oxygen is further away from the phosphorus '
                 '(typically by 5 bonds rather than 4) the previous code ended '
                 'up “seeing” only the sn‑2 ester as meeting the distance '
                 'criterion. We can therefore relax the allowed bond‐distance '
                 '(e.g. to 5 bonds) so that both ester bonds are detected. '
                 'Below is the revised code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 313,
    'num_true_negatives': 141962,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07396449704142012,
    'recall': 1.0,
    'f1': 0.13774104683195593,
    'accuracy': 0.9978004216444132,
    'negative_predictive_value': 1.0}