"""
Classifies: CHEBI:87659 dodecanoate ester
"""
"""
Classifies: any fatty acid ester in which the carboxylic acid component is lauric acid,
i.e. a dodecanoate ester. The acyl group must be exactly CH3(CH2)10C(=O)O.
This program builds a SMARTS that encodes:
    [CH3;H3]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-C(=O)O
so that if a match is found the laurate (dodecanoate) ester substructure exists,
and extra bonds on the “terminal” atoms would lower the hydrogen counts so that the SMARTS does not match.
"""

from rdkit import Chem

def is_dodecanoate_ester(smiles: str):
    """
    Determines if a molecule contains a dodecanoate (laurate) ester group.
    A dodecanoate ester here is defined as having the acyl moiety CH3(CH2)10C(=O)O.
    
    The procedure is as follows:
      1. Convert the input SMILES into an RDKit molecule.
      2. Use a SMARTS pattern that demands a terminal CH3 (with three implicit/explcit H’s)
         followed by exactly ten CH2 groups (with exactly two hydrogens each), finishing in a carbonyl group bound to an -O.
         This pattern does not match if the chain is extended or branched.
      3. If at least one substructure match is found then we classify the molecule as containing
         a laurate ester group.
         
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule contains a laurate ester group, False otherwise.
        str: Explanation for the classification.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # Build a SMARTS for the exact laurate ester acyl fragment:
    # CH3(CH2)10C(=O)O
    # Note: each atom is annotated with a hydrogen count constraint:
    #  - The terminal CH3 must have exactly 3 hydrogen atoms.
    #  - Each CH2 must have exactly 2 hydrogens.
    #  - Then the carbonyl carbon (without H count constraint) is bound to =O and O.
    # The SMARTS string written out is:
    #   [CH3;H3]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-[CH2;H2]-C(=O)O
    smarts = ("[CH3;H3]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-[CH2;H2]"
              "-C(=O)O")
              
    query = Chem.MolFromSmarts(smarts)
    if query is None:
        return False, "Could not build SMARTS pattern for laurate ester."
    
    # Find matches of the laurate ester pattern in the molecule.
    matches = mol.GetSubstructMatches(query)
    if matches:
        return True, "Molecule contains a dodecanoate (laurate) ester group."
    else:
        # No match found – either the ester group is absent or 
        # the acyl chain is not exactly laurate (e.g. if it is extended or branched).
        return False, "No laurate ester group with an exact CH3(CH2)10C(=O)O acyl chain found."

# Example usage:
if __name__ == "__main__":
    # Test with a known laurate ester: 1-lauroyl-sn-glycerol.
    test_smiles = "CCCCCCCCCCCC(=O)OC[C@@H](O)CO"
    result, reasoning = is_dodecanoate_ester(test_smiles)
    print(result, reasoning)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:87659',
                          'name': 'dodecanoate ester',
                          'definition': 'Any fatty acid ester in which the '
                                        'carboxylic acid component is lauric '
                                        'acid.',
                          'parents': ['CHEBI:35748'],
                          'xrefs': ['PMID:23383323'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 55,
                           'log_lines_of_code': 4.007333185232471,
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
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': ['smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_dodecanoate_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "Could not build SMARTS '
                                          'pattern for laurate ester."',
                                          'True, "Molecule contains a '
                                          'dodecanoate (laurate) ester group."',
                                          'False, "No laurate ester group with '
                                          'an exact CH3(CH2)10C(=O)O acyl '
                                          'chain found."'],
                           'returns_count': 4,
                           'complexity': 2.8014666370464942},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'O[C@@H]1[C@@]2([C@@]([C@](C1)([C@@H](CC(=O)CC(C)C(O)=O)C)[H])(CC(=O)C=3[C@@]4([C@](C([C@@H](O)CC4)(C)C)(CCC23)[H])C)C)C '
               'NAME: Ganolucidic acid B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: O[C@@H](CCCCCCCC)CC(O)=O NAME: '
               '3S-hydroxy-undecanoic acid REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: O1C2C3C(C4C5(C2O)CC(CC4)C(C5)=C)(CCCC3(C1=O)CO)C '
               'NAME: 7,18-Dihydroxykaurenolide REASON: WRONGLY CLASSIFIED '
               'Molecule contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'C1CC(C(C=2[C@@]1([C@]3([C@](C(C2O)=O)([C@@]4([C@@](C(C3)=C)(C([C@](OC4=O)(C(OC)=O)C)=O)C)[H])C)O)C)(C)C)=O '
               'NAME: terretonin REASON: WRONGLY CLASSIFIED Molecule contains '
               'a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O[C@@H]1C([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@](CC4)(CC[C@](C5)(C)C(O)=O)C)[H])=CC3)C)(CC2)C)[H])(CC1)C)[H])(C)C '
               'NAME: 11-Deoxoglycyrrhetinic acid REASON: WRONGLY CLASSIFIED '
               'Molecule contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O[C@@H]1C([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@](CC4)(CC[C@@](C5)(C)C(O)=O)C)[H])=CC3)C)(CC2)C)[H])(CC1)C)[H])(C)C '
               'NAME: 3-Epikatonic acid REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'C[C@@]12C[C@H]3OC(=O)C(=C)[C@H]3C[C@H]1C(=C)C[C@H](O)C2 NAME: '
               'Ivalin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4(C(=O)C[C@]5([C@]4(C1)C)O[C@]6(OC(=O)[C@@H](C6)C)CC5C)C '
               'NAME: '
               '(17S,23S)-17,23-epoxy-3beta-hydroxy-7,11,15-trioxo-5alpha-lanosta-8-en-26,23-olide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a dodecanoate '
               'ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C1OC(C2=CN=CC=C2)=CC3=C1[C@H](O)[C@@]4(C(=CC[C@H]5[C@]4(CC[C@@]([C@@]56COC(=O)CC6)(O)C(=C)C)C)C)O3 '
               'NAME: Oxalicine B REASON: WRONGLY CLASSIFIED Molecule contains '
               'a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O(C1C(C2C(C3C(C4(C(C5C(C(O)C4)(CCC(C5)(C)C)C(O)=O)=CC3)C)(CC2)C)(CC1)C)(C)C)C6OC(C(O)C(O)C6O)COC7OCC(O)C(O)C7OC8OCC(O)C(O)C8O '
               'NAME: Pitheduloside D REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C(=CC[C@@]4(C)[C@]5([H])C[C@@](C)(CC[C@]5(C)CC[C@]34C)C(O)=O)[C@@]1(C)CC[C@H](OC(=O)\\C=C\\c1ccc(O)cc1)C2(C)C '
               'NAME: '
               '3-beta-O-(E)-coumaroyl-D:C-friedooleana-7,9(11)-dien-29-oic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a '
               'dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O1C23C45C6(C4C(C(C6)CC5)=C)C(C2C(CC(O)C3)(C1=O)C)C(O)=O NAME: '
               'Gibberellin A105 REASON: WRONGLY CLASSIFIED Molecule contains '
               'a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               '[Na+].[H][C@@]12CC[C@@]3(C)[C@@]([H])(CC(=O)\\C3=C(C)/C=C/C=C(C)/C=C/C(OC)C(C)(C)O)[C@@]1(C)CC[C@@H](O)[C@]2(C)C([O-])=O '
               'NAME: sodium globostellatate D REASON: WRONGLY CLASSIFIED '
               'Molecule contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C1OC([C@@H]2CC[C@@]3([C@@H]([C@]2([C@H](C1)O)C)CC=4C(=O)OC(=CC4O3)C)C)(C)C '
               'NAME: Asperversin D REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C(O)C1(OC2([C@H](O[C@@H](C(O)(C)C)CC2)CC1)C)CC(=O)C3=C(O)C=CC(=C3)O '
               'NAME: Cochlearol Q REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'C[C@H](CCC[C@@H](C)C(O)=O)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (25R)-3beta-hydroxycholest-5-en-26-oic acid REASON: '
               'WRONGLY CLASSIFIED Molecule contains a dodecanoate ester '
               '(laurate ester) group.\n'
               ' * SMILES: '
               'O=C(O)C([C@H](C1(O[C@H]2C3([C@](C=4CCC5C(C4C2)(CC[C@H](C5(C)C)OC(=O)CC(=O)OCCCC)C)(CC[C@@H]3[C@@H](C1)C)C)C)O)C)C '
               "NAME: 3alpha-(3'-butylcarboxyacetoxy)oxepanoquercinic acid C "
               'REASON: WRONGLY CLASSIFIED Molecule contains a dodecanoate '
               'ester (laurate ester) group.\n'
               ' * SMILES: OC12C3(C(C(CCC3)(C)C)CC=C1C(OC2O)=O)C NAME: '
               '1,9b-dihydroxy-6,6,9a-trimethyl-1,5,5a,7,8,9-hexahydrobenzo[e][2]benzofuran-3-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains a dodecanoate '
               'ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C(O)[C@@]1(O)[C@@]2(O[C@](CC/C(=C/C(CC3=CC=CC=C3)C)/C)(O[C@@H]1C(=O)O)CC2)C(=O)O '
               'NAME: 6,7-dideoxy-squalestatin H5 REASON: WRONGLY CLASSIFIED '
               'Molecule contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C1C2=C(C=CC(=C2)O)O[C@]13[C@H](C(=O)O)CC[C@H]3[C@]45[C@@H](O)[C@@](C(=O)O)(C[C@H](C4)C=C(C5)C=O)CC(=O)C6=C(O)C=CC(=C6)O '
               'NAME: Applanatumin A REASON: WRONGLY CLASSIFIED Molecule '
               'contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@@H](C=C(C)[C@]23[C@@H](C[C@@H]1OC)C=C[C@@H]4[C@H]2[C@H](O)[C@@H](C)[C@H]([C@@H]4O3)O)C)[C@H](OC(=O)C)C '
               'NAME: 18-O-acetyl-nodusmicin REASON: WRONGLY CLASSIFIED '
               'Molecule contains a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(CC=CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCC(O)=O)C)[H])[H])C '
               'NAME: 7alpha,12alpha-Dihydroxy-5beta-chol-2-en-24-oic Acid '
               'REASON: WRONGLY CLASSIFIED Molecule contains a dodecanoate '
               'ester (laurate ester) group.\n'
               ' * SMILES: '
               'O1[C@@]2([C@@]([C@@]3([C@@]([C@H](OC(=O)C)C2)(C(OC(=O)CC3)(C)C)[H])C)(CC4=C1C(=C5C(=C4OC)C(OC5)=O)C)[H])C '
               'NAME: Austalide I REASON: WRONGLY CLASSIFIED Molecule contains '
               'a dodecanoate ester (laurate ester) group.\n'
               ' * SMILES: '
               'O(C1C(C2C(C3C(C4(C(C5C(CC4)(CCC(C5)(C)C)C(O)=O)=CC3)C)(CC2)C)(CC1O)C)(C)C)C6OC(C(O)C(O)C6O)CO '
               'NAME: Maslinic acid 3-O-b-D-glucoside REASON: WRONGLY '
               'CLASSIFIED Molecule contains a dodecanoate ester (laurate '
               'ester) group.\n'
               ' * SMILES: C(CCCCCC(CCCC)C)CCC(O)=O NAME: '
               '10-methyltetradecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule contains a dodecanoate ester (laurate ester) group.\n'
               'False negatives: SMILES: '
               '[C@H]1(OP(=O)(O)O[C@H]2OC[C@@H]([C@@H]([C@H]2O)O)N)[C@H](OC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC)[C@@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@@H](O[C@@H]1CO)OC[C@@H]3[C@H]([C@@H]([C@H]([C@H](O3)OP(=O)(O)O)NC(=O)C[C@@H](CCCCCCCCCCC)O)OC(=O)C[C@@H](CCCCCCCCCCC)O)O '
               'NAME: beta-L-Ara4N-lipid A (E. coli) REASON: MISSED '
               'Dodecanoate ester substructure found but acyl chain is '
               'extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)O[C@H]1[C@H](C)O[C@@H](O[C@H]2[C@H](C)O[C@@H](O[C@H]3[C@H](C)O[C@H]4O[C@@H]5[C@@H](O)[C@@H](O)[C@@H](C)O[C@H]5O[C@@H](CCCCC)CCCCCCCCCC(=O)O[C@H]3[C@H]4O)[C@H](O)[C@@H]2OC(=O)CCCCCCCCC)[C@H](OC(=O)\\C=C\\c2ccccc2)[C@@H]1O '
               'NAME: ipomotaoside D REASON: MISSED Dodecanoate ester '
               'substructure found but acyl chain is extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCC '
               'NAME: 1,2-dilauroyl-sn-glycero-3-phosphocholine REASON: MISSED '
               'Dodecanoate ester substructure found but acyl chain is '
               'extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)OC[C@@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1,2-dioleoyl-3-lauroyl-sn-glycerol REASON: MISSED '
               'Dodecanoate ester substructure found but acyl chain is '
               'extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)O[C@H]1[C@H](C)O[C@@H](O[C@H]2[C@H](C)O[C@@H](O[C@H]3[C@H](C)O[C@H]4O[C@@H]5[C@@H](O)[C@@H](O)[C@@H](C)O[C@H]5O[C@@H](CCCCC)CCCCCCCCCC(=O)O[C@@H]4[C@@H]3O)[C@H](O)[C@@H]2OC(=O)CCCCCCCCC)[C@H](OC(=O)\\C=C\\c2ccccc2)[C@@H]1O '
               'NAME: ipomotaoside A REASON: MISSED Dodecanoate ester '
               'substructure found but acyl chain is extended beyond laurate.\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@@](C[C@@H](O)[C@H]1O)(O[C@@H]1C[C@@](OC[C@H]2O[C@@H](OC[C@H]3O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]3O)[C@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC)[C@@H]2OP(O)(O)=O)(O[C@]([H])([C@H](O)CO)[C@@H]1O[C@H]1O[C@H]([C@@H](O)CO)[C@@H](O)[C@H](O)[C@@H]1O)C(O)=O)C(O)=O)[C@H](O)CO '
               'NAME: heptosyl-(KDO)2-lipid A REASON: MISSED Dodecanoate ester '
               'substructure found but acyl chain is extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCC)OC(=O)CCCCCCCCCCC NAME: '
               'trilaurin REASON: MISSED Dodecanoate ester substructure found '
               'but acyl chain is extended beyond laurate.\n'
               ' * SMILES: CCCCCCCCCCCC(=O)OCC(O)CO NAME: '
               'rac-1-monolauroylglycerol REASON: MISSED Dodecanoate ester '
               'substructure found but acyl chain is extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)O[C@H](CCCCCCCCCCC)CC(=O)O[C@@H]1[C@@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@H](OC[C@H]2O[C@H](OP(O)(=O)OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]2O)O[C@H](CO[C@@]2(C[C@@H](O[C@@]3(C[C@@H](O)[C@@H](O)[C@H](O3)[C@H](O)CO)C(O)=O)[C@@H](O)[C@H](O2)[C@H](O)CO)C(O)=O)[C@H]1OP(O)(O)=O '
               'NAME: (Kdo)2-lipid A 1-diphosphate (E. coli) REASON: MISSED '
               'Dodecanoate ester substructure found but acyl chain is '
               'extended beyond laurate.\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)O[C@@H](CO)COC(=O)CCCCCCC\\C=C/CCCCCCCC NAME: '
               '1-oleoyl-2-lauroyl-sn-glycerol REASON: MISSED Dodecanoate '
               'ester substructure found but acyl chain is extended beyond '
               'laurate.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No laurate ester group with an '
                                               'exact CH3(CH2)10C(=O)O acyl '
                                               'chain found.'}],
    'sample_false_negatives': [   {   'smiles': '[C@H](OC(CCCCCCCCCCCC)=O)(C[N+](C([2H])([2H])[2H])(C)C)CC(=O)[O-]',
                                      'name': 'dodecanoyl-L-carnitine-d3',
                                      'reason': 'No laurate ester group with '
                                                'an exact CH3(CH2)10C(=O)O '
                                                'acyl chain found.'}],
    'attempt': 3,
    'reasoning': 'Below is one possible answer. I “learned” from the previous '
                 'attempt that simply matching a fragment string (and then '
                 'checking whether the first “C” is terminal by looking at '
                 'extra neighboring carbons) was not enough. In refining the '
                 'code we now encode the full laurate‐ester chain in the '
                 'SMARTS itself. In lauric acid (dodecanoic acid) the acyl '
                 'group is\n'
                 '\n'
                 '\u2003\u2003CH3(CH2)10C(=O)O\n'
                 '\n'
                 'so we require a terminal methyl (3 hydrogens) followed by '
                 'exactly ten methylene groups (each having exactly 2 '
                 'hydrogens) that end with a carbonyl ester. (If the chain '
                 'were embedded in a longer chain the “terminal” methyl would '
                 'lose one or more hydrogens.) In the code below the SMARTS is '
                 'written explicitly (with hydrogen constraints) so that only '
                 'an unbranched chain of the proper length will match. This '
                 'change avoids many of the previous false positives as well '
                 'as not “matching” chains that are extended beyond laurate.\n'
                 '\n'
                 'Below is the full code in one Python code‐block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 64,
    'num_false_positives': 218,
    'num_true_negatives': 142017,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.22695035460992907,
    'recall': 0.9846153846153847,
    'f1': 0.3688760806916427,
    'accuracy': 0.9984609978917779,
    'negative_predictive_value': 0.9999929586390458}