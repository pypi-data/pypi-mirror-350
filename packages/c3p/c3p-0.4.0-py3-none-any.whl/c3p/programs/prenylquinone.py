"""
Classifies: CHEBI:26255 prenylquinone
"""
#!/usr/bin/env python
"""
Classifies: Prenylquinone
Definition: A quinone substituted by a polyprenyl‐derived side‐chain.
The molecule must contain a quinone core (e.g. p‐benzoquinone or 1,4–naphthoquinone)
and at least one prenyl (isoprene‐derived) side-chain (characterized here by the “C=C(C)” fragment)
found outside of the quinone core.
"""

from rdkit import Chem

def is_prenylquinone(smiles: str):
    """
    Determines if a molecule is a prenylquinone based on its SMILES string.
    A prenylquinone must contain a quinone moiety and also a prenyl (isoprene-derived)
    side-chain substituent (e.g. a C=C(C) fragment) that is not part of the quinone ring.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if the molecule is classified as a prenylquinone, False otherwise.
        str: Reason for the classification decision.
    """
    # Parse SMILES into a molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define two quinone SMARTS patterns:
    # Pattern 1: p-benzoquinone (a six-membered ring bearing two carbonyls in para positions)
    quinone_smarts1 = "O=C1C=CC(=O)C=C1"
    quinone_pat1 = Chem.MolFromSmarts(quinone_smarts1)
    
    # Pattern 2: 1,4-naphthoquinone core (two fused aromatic rings with two carbonyls)
    quinone_smarts2 = "O=C1C=CC2=C(C=CC(=O)C2=1)"
    quinone_pat2 = Chem.MolFromSmarts(quinone_smarts2)

    has_quinone = False
    quinone_atoms = set()
    
    # Try the first quinone pattern
    match1 = mol.GetSubstructMatch(quinone_pat1)
    if match1:
        has_quinone = True
        quinone_atoms = set(match1)
    else:
        # Otherwise try the second pattern
        match2 = mol.GetSubstructMatch(quinone_pat2)
        if match2:
            has_quinone = True
            quinone_atoms = set(match2)
    
    if not has_quinone:
        return False, "No quinone motif found"

    # Now search for a prenyl-derived side-chain.
    # A typical isoprene-derived fragment has a substituted double bond.
    # Here we look for the fragment "C=C(C)".
    prenyl_smarts = "C=C(C)"
    prenyl_pat = Chem.MolFromSmarts(prenyl_smarts)
    prenyl_matches = mol.GetSubstructMatches(prenyl_pat)
    
    # We require that at least one prenyl match is found that is not part of the quinone core.
    external_prenyl = []
    for match in prenyl_matches:
        # If none of the atoms in the prenyl match are part of the quinone core, use it.
        if quinone_atoms.isdisjoint(match):
            external_prenyl.append(match)
    
    if not external_prenyl:
        return False, "Quinone core found, but no prenyl side-chain detected outside the quinone ring"
    
    # If we reach this point, the molecule contains a quinone core and at least one prenyl fragment.
    return True, "Contains a quinone core with a prenyl-derived side-chain"

# For simple testing, you can run:
if __name__ == "__main__":
    # Example SMILES from the provided list, e.g. Napyradiomycin CNQ525.538
    test_smiles = "Br[C@H]1C(O[C@]2(C(=O)C=3C=C(O)C(=C(C3C([C@]2(C1)Cl)=O)O)C)C/C=C(/CCC=C(C)C)\\C)(C)C"
    result, reason = is_prenylquinone(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26255',
                          'name': 'prenylquinone',
                          'definition': 'A quinone substituted by a '
                                        'polyprenyl-derived side-chain. '
                                        'Prenylquinones occur in all living '
                                        'cells. Due to their amphiphilic '
                                        'character, they are mainly located in '
                                        'biological membranes where they '
                                        'function as electron and proton '
                                        'carriers in the photosynthetic and '
                                        'respiratory electron transport '
                                        'chains. Some prenylquinones also '
                                        'perform more specialised roles sucy '
                                        'as antioxidants and enzyme cofactors. '
                                        'Prenylquinones are classified '
                                        'according to ring structure: the main '
                                        'classes are menaquinones, '
                                        'phylloquinones, ubiquinones and '
                                        'plastoquinones.',
                          'parents': ['CHEBI:25830'],
                          'xrefs': [   'PMID:19928587',
                                       'PMID:21777468',
                                       'PMID:21844348',
                                       'PMID:22371323',
                                       'PMID:3985624'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 57,
                           'log_lines_of_code': 4.04305126783455,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
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
                                                 2,
                                                 3,
                                                 3,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'append',
                                                 'GetSubstructMatch',
                                                 'isdisjoint',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 6,
                           'smarts_strings': [   'quinone_smarts2',
                                                 'prenyl_smarts',
                                                 'quinone_smarts1'],
                           'smarts_strings_count': 3,
                           'defs': ['is_prenylquinone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No quinone motif found"',
                                          'False, "Quinone core found, but no '
                                          'prenyl side-chain detected outside '
                                          'the quinone ring"',
                                          'True, "Contains a quinone core with '
                                          'a prenyl-derived side-chain"'],
                           'returns_count': 4,
                           'complexity': 3.60861025356691},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'No quinone motif found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'No quinone motif found'}],
    'sample_false_negatives': [   {   'smiles': 'Br[C@H]1C(O[C@]2(C(=O)C=3C=C(O)C(=C(C3C([C@]2(C1)Cl)=O)O)C)C/C=C(/CCC=C(C)C)\\C)(C)C',
                                      'name': 'Napyradiomycin CNQ525.538',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'O=C1C=C(C(=O)C[C@]1(O)C[C@H]2C(=C)CC[C@@H]3[C@@]2(CCCC3(C)C)C)CO',
                                      'name': 'Purpurogemutantidin',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'C1(=O)C(C)=C(C(=O)C2=CC=CC=C12)C/C=C(\\C)/CCCC(C)CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C',
                                      'name': 'beta-dihydromenaquinone-9',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC1=C(C)C(=O)c2ccccc2C1=O',
                                      'name': 'menaquinone-4',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'ClC1=C(C(=C(O)C=C1C)C(=O)OC)CC=2C(=O)C(OC)=CC(C2)=O',
                                      'name': 'Cristaquinone A',
                                      'reason': 'Quinone core found, but no '
                                                'prenyl side-chain detected '
                                                'outside the quinone ring'},
                                  {   'smiles': 'O=C1C=C(C(=O)C[C@]1(O)C)/C=C/C(O)(C)C',
                                      'name': 'Acrimine B',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'O=C1C(CCCCCCCCCCC)=CC(=O)C(O)=C1O',
                                      'name': 'Myrsinone',
                                      'reason': 'Quinone core found, but no '
                                                'prenyl side-chain detected '
                                                'outside the quinone ring'},
                                  {   'smiles': 'Cl[C@]1(C(=O)C2=C(O)C=C(O)C=C2C([C@@]1(O)C/C=C(/CCC=C(C)C)\\C)=O)CC=C(C)C',
                                      'name': 'Naphthomevalin',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC1=C(C)C(=O)c2ccccc2C1=O',
                                      'name': 'omega-hydroxymenaquinone-4',
                                      'reason': 'No quinone motif found'},
                                  {   'smiles': 'C1(=O)C(C)=C(C(=O)C2=CC=CC=C12)C/C=C(\\C)/CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(\\C)/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C',
                                      'name': 'menaquinone-9',
                                      'reason': 'No quinone motif found'}],
    'attempt': 0,
    'reasoning': 'We can solve this problem by “looking” for two structural '
                 'features in the molecule: (1) a quinone core and (2) a '
                 'prenyl‐derived side‐chain. For the first, we use one or two '
                 'SMARTS patterns meant to catch common quinone moieties (for '
                 'example, p‐benzoquinone or 1,4–naphthoquinone cores). For '
                 'the prenyl side‐chain, one characteristic fragment of an '
                 'isoprene‐derived unit is the substituted carbon–carbon '
                 'double bond (for example, a substructure like “C=C(C)”). In '
                 'our program the steps are roughly as follows:\n'
                 '\n'
                 '1. Convert the SMILES string into an RDKit molecule.\n'
                 '2. Check whether a quinone motif can be found (we try two '
                 'SMARTS patterns in turn).\n'
                 '3. If a quinone is present, then search for a prenyl '
                 'substructure via the “C=C(C)” SMARTS.\n'
                 '4. To be sure that the “prenyl‐like” fragment is not '
                 'actually part of the quinone core, we filter out any matches '
                 'whose atoms overlap with the quinone.\n'
                 '5. If at least one non‐overlapping prenyl fragment is found, '
                 'we classify the molecule as a prenylquinone.\n'
                 '\n'
                 'Below is the complete code in one Python code block.\n'
                 '\n'
                 '----------------------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 46,
    'num_false_positives': 113,
    'num_true_negatives': 142108,
    'num_false_negatives': 33,
    'num_negatives': None,
    'precision': 0.2893081761006289,
    'recall': 0.5822784810126582,
    'f1': 0.3865546218487395,
    'accuracy': 0.9989739985945186,
    'negative_predictive_value': 0.9997678361626835}