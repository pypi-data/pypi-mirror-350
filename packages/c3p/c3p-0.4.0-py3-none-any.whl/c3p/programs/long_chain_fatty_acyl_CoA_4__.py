"""
Classifies: CHEBI:83139 long-chain fatty acyl-CoA(4-)
"""
#!/usr/bin/env python
"""
Classifies: long-chain fatty acyl-CoA(4-)
Definition: A fatty acyl-CoA(4-) arising from deprotonation of the phosphate and diphosphate OH groups 
of any long-chain fatty acyl-CoA; major species at pH 7.3.
This program uses simple substructure searches to detect a CoA moiety and a thioester group from which
the acyl chain is identified. The fatty acyl chain is assumed to be “long‐chain” if it contains at least 
12 contiguous carbon atoms.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_long_chain_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule (given as a SMILES string) belongs to the class
    long-chain fatty acyl-CoA(4-).

    We check for three features:
      1. The presence of a CoA moiety (using a characteristic fragment of CoA).
      2. A thioester group (C(=O)S) which links the fatty acyl chain with the CoA.
      3. A long fatty acyl chain: we count the number of contiguous carbons attached 
         to the carbonyl carbon (threshold: at least 12 carbons).
      4. Overall formal charge of -4 (as expected for CoA(4-)).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is classified as long-chain fatty acyl-CoA(4-), False otherwise.
        str: Reason for the classification decision.
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check overall formal charge (expecting -4 for the deprotonated CoA species)
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if total_charge != -4:
        return False, f"Formal charge is {total_charge} (expected -4 for CoA(4-))"
    
    # Check for the CoA moiety using a recognizable fragment.
    # Here we use a fragment pattern from the pantetheine and nucleotide parts: "SCCNC(=O)CCNC(=O)"
    coa_pattern = Chem.MolFromSmarts("SCCNC(=O)CCNC(=O)")
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "CoA moiety not found"

    # Look for a thioester group: pattern for a carbonyl carbon (with degree 3) bound to a sulfur.
    # The SMARTS "[C;D3](=O)[S]" should capture the thioester group.
    thioester_pattern = Chem.MolFromSmarts("[C;D3](=O)[S]")
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if not thioester_matches:
        return False, "No thioester group (fatty acid linkage) found"

    # Define a recursive function to count the length of a contiguous carbon chain.
    # We only travel along carbon atoms and do not branch (if branching is encountered, we take the longest route).
    def count_chain_length(atom, from_idx, visited):
        # Count current atom (note: visited is used to avoid loops)
        length = 1
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() == from_idx or nbr.GetIdx() in visited:
                continue
            # We only continue if the neighbor is a carbon
            if nbr.GetAtomicNum() == 6:
                visited.add(nbr.GetIdx())
                branch_length = 1 + count_chain_length(nbr, atom.GetIdx(), visited)
                if branch_length > length:
                    length = branch_length
        return length

    # Try each thioester match to find a fatty acyl chain
    # In the pattern "[C;D3](=O)[S]", match[0] is the carbonyl carbon and match[1] is the sulfur.
    chain_found = False
    acyl_chain_length = 0
    for match in thioester_matches:
        carbonyl_idx = match[0]
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
        # Look among the neighbors of the carbonyl carbon for a carbon that is not the S from the thioester.
        fatty_start = None
        for nbr in carbonyl_atom.GetNeighbors():
            if nbr.GetAtomicNum() == 6 and nbr.GetIdx() != match[1]:
                fatty_start = nbr
                break
        if fatty_start is None:
            continue  # no attached carbon found; try next match
        
        # Count the acyl chain length. We start from fatty_start.
        # We assume the chain is linear so we take the maximal contiguous carbon count.
        chain_length = count_chain_length(fatty_start, carbonyl_idx, {fatty_start.GetIdx()})
        if chain_length >= 12:
            chain_found = True
            acyl_chain_length = chain_length
            break

    if not chain_found:
        return False, "Fatty acyl chain not long enough (requires at least 12 contiguous carbons)"

    return True, (
        f"Contains CoA moiety, thioester group with a fatty acyl chain of length {acyl_chain_length} carbons, "
        "and overall charge -4"
    )

# Example usage:
if __name__ == "__main__":
    test_smiles = "CCCC\\C=C/C\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12"
    result, reason = is_long_chain_fatty_acyl_CoA_4__(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:83139',
                          'name': 'long-chain fatty acyl-CoA(4-)',
                          'definition': 'A fatty acyl-CoA(4-) arising from '
                                        'deprotonation of the phosphate and '
                                        'diphosphate OH groups of any '
                                        'long-chain fatty acyl-CoA; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:77636'],
                          'xrefs': ['MetaCyc:Long-Chain-Acyl-CoAs'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 80,
                           'log_lines_of_code': 4.382026634673881,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 0,
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
                                                 2,
                                                 0,
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
                                                 0,
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
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
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
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'add',
                                                 'GetFormalCharge',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetIdx'],
                           'methods_called_count': 11,
                           'smarts_strings': [   'SCCNC(=O)CCNC(=O)',
                                                 '[C;D3](=O)[S]'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_long_chain_fatty_acyl_CoA_4__(smiles: '
                                       'str):',
                                       'count_chain_length(atom, from_idx, '
                                       'visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Formal charge is '
                                          '{total_charge} (expected -4 for '
                                          'CoA(4-))"',
                                          'False, "CoA moiety not found"',
                                          'False, "No thioester group (fatty '
                                          'acid linkage) found"',
                                          'length',
                                          'False, "Fatty acyl chain not long '
                                          'enough (requires at least 12 '
                                          'contiguous carbons)"',
                                          'True, ('],
                           'returns_count': 7,
                           'complexity': 5.876405326934776},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Formal charge is 0 (expected '
                                               '-4 for CoA(4-))'}],
    'sample_false_negatives': [   {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)C[C@@H](O)CCC/C=C\\CCCCCC)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '(3S,7Z)-3-hydroxytetradec-7-enoyl-CoA(4-)',
                                      'reason': 'Formal charge is 0 (expected '
                                                '-4 for CoA(4-))'}],
    'attempt': 0,
    'reasoning': 'Below is one possible solution. In our approach we first '
                 'parse the SMILES and then look for two key aspects: (1) a '
                 'characteristic CoA substructure (here we require a short '
                 'fragment common to CoA, namely "SCCNC(=O)CCNC(=O)") and (2) '
                 'a thioester group (i.e. a [C;D3](=O)S fragment) from which '
                 'we “extract” the fatty acyl chain. For the latter we find '
                 'the carbonyl carbon and then follow along the acyl chain '
                 '(limited to carbon atoms only) to get a crude estimate of '
                 'its (linear) chain length. Finally, we check that the '
                 'molecule’s overall formal charge is –4 (as expected for a '
                 'deprotonated acyl‐CoA(4–) under physiological conditions). '
                 '(Note that this is a heuristic algorithm; in practice these '
                 'molecules are large and flexible, and more sophisticated '
                 'approaches might be required.) \n'
                 '\n'
                 'Below is the complete Python code in a single code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 136,
    'num_false_positives': 248,
    'num_true_negatives': 141915,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.3541666666666667,
    'recall': 0.9927007299270073,
    'f1': 0.5220729366602688,
    'accuracy': 0.9982501756851722,
    'negative_predictive_value': 0.999992953578173}