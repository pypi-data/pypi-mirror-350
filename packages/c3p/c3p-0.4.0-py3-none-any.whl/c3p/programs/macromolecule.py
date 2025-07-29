"""
Classifies: CHEBI:33839 macromolecule
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_macromolecule(smiles: str):
    """
    Determines if a molecule is a macromolecule based on its SMILES string.
    Considers molecular weight, presence of typical recurring monomer linkages, 
    and other structural motifs to determine macromolecule classification.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a macromolecule, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Calculate molecular weight
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    min_macromolecule_weight = 500  # Consider molecular weight threshold
    if mol_wt < min_macromolecule_weight:
        return False, f"Molecular weight {mol_wt:.2f} Da is less than the minimum macromolecule threshold {min_macromolecule_weight} Da"

    # Detect repeating linkages typical in macromolecules
    try:
        # Improved patterns for identifying macromolecular linkages
        peptide_bond_pattern = Chem.MolFromSmarts('C(=O)N[C@H]')
        glycosidic_bond_pattern = Chem.MolFromSmarts('O[C@@H]1C(O)C([C@@H]([C@H]1)O)O')
        nucleic_acid_pattern = Chem.MolFromSmarts('C1=NC=CC(=O)N1')
        
        # Expanded search for recurring patterns
        peptide_matches = mol.GetSubstructMatches(peptide_bond_pattern)
        glycosidic_matches = mol.GetSubstructMatches(glycosidic_bond_pattern)
        nucleic_matches = mol.GetSubstructMatches(nucleic_acid_pattern)

        # More vigorous pattern detection for typical macromolecules
        if len(peptide_matches) > 5 or len(glycosidic_matches) > 3 or len(nucleic_matches) > 2:
            if len(peptide_matches) + len(glycosidic_matches) + len(nucleic_matches) > 10:
                return True, "Considered a macromolecule based on recurrent macromolecular linkages."
        
    except Exception as e:
        return False, f"Failed to match structures due to error: {str(e)}"
    
    # Check for additional macromolecular characteristics
    if mol.GetNumAtoms() > 100:
        # Heuristic: Large structures often correlate with macromolecules
        return True, "Large molecular structure identified as potential macromolecule."

    return False, "No sufficient recurring motifs typical of macromolecules detected."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33839',
                          'name': 'macromolecule',
                          'definition': 'A macromolecule is a molecule of high '
                                        'relative molecular mass, the '
                                        'structure of which essentially '
                                        'comprises the multiple repetition of '
                                        'units derived, actually or '
                                        'conceptually, from molecules of low '
                                        'relative molecular mass.',
                          'parents': ['CHEBI:36357'],
                          'xrefs': ['Wikipedia:Macromolecule'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 36,
                           'log_lines_of_code': 3.58351893845611,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetNumAtoms',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches',
                                                 'CalcExactMolWt',
                                                 'MolFromSmarts'],
                           'methods_called_count': 5,
                           'smarts_strings': [   'O[C@@H]1C(O)C([C@@H]([C@H]1)O)O',
                                                 'C1=NC=CC(=O)N1',
                                                 'C(=O)N[C@H]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_macromolecule(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight '
                                          '{mol_wt:.2f} Da is less than the '
                                          'minimum macromolecule threshold '
                                          '{min_macromolecule_weight} Da"',
                                          'False, f"Failed to match structures '
                                          'due to error: {str(e)}"',
                                          'True, "Large molecular structure '
                                          'identified as potential '
                                          'macromolecule."',
                                          'False, "No sufficient recurring '
                                          'motifs typical of macromolecules '
                                          'detected."'],
                           'returns_count': 5,
                           'complexity': 3.316703787691222},
    'message': '\n'
               'Attempt failed: F1 score of 0.33263993948562787 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO)CO '
               'NAME: CID 91862434 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]5O)CO)[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%10NC(=O)C)CO '
               'NAME: CID 91860438 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@@H]4[C@H](O)[C@@H](O[C@@H]([C@H]4O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO)O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O)[C@@H]%10O[C@@H]([C@@H](O)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H]%10NC(=O)C)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-6-[(2S,3S,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-4-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3-hydroxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Molecule is considered a macromolecule '
               'based on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H]7[C@H](O)[C@H](O[C@@H](O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]7O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%10NC(=O)C)CO)CO '
               'NAME: CID 91854861 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O[C@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)C)[C@H]9NC(=O)C)CO)[C@H](O)[C@@H]8O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO)CO)[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O[C@H]%19O[C@@H]([C@H](O)[C@H](O)[C@H]%19O)C)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91845439 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'C[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](CO)O[C@H](O[C@H]3[C@H](C)O[C@@H](O[C@H]4[C@@H](O)[C@@H](CO)O[C@H](O[C@@H]5[C@H](O[C@H](CO)[C@@H](O)[C@@H]5O[C@H]5O[C@H](C)[C@H](O)C[C@H]5O)O[C@H]5[C@H](C)O[C@@H](O[C@H]6[C@@H](O)[C@@H](CO)O[C@H](O[C@@H]7[C@H](O[C@H](CO)[C@@H](O)[C@@H]7O[C@H]7O[C@H](C)[C@H](O)C[C@H]7O)O[C@H]7[C@H](C)O[C@@H](O)[C@H](O)[C@@H]7O)[C@@H]6O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@H](O)[C@@H]3O)[C@H]2O[C@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)C[C@H]1O '
               'NAME: '
               'alpha-D-Galp-(1->2)-[alpha-D-Abep-(1->3)]-alpha-D-Manp-(1->4)-alpha-L-Rhap-(1->3)-alpha-D-Galp-(1->2)-[alpha-D-Abep-(1->3)]-alpha-D-Manp-(1->4)-alpha-L-Rhap-(1->3)-alpha-D-Galp-(1->2)-[alpha-D-Abep-(1->3)]-alpha-D-Manp-(1->4)-alpha-L-Rhap '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]3[C@H](O)[C@H](O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@H]3O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)[C@H]%10NC(=O)C)CO)CO)[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO)[C@H](O[C@@H]%15O[C@H]([C@@H](O)[C@@H](O)[C@@H]%15O)C)[C@H]%13NC(=O)C)CO '
               'NAME: CID 91853224 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)N(CC(=O)N([C@H](C(=O)N2[C@H](C(=O)N(C)[C@H](C(N[C@H](C(N([C@H](C(N([C@H](C(N([C@H]1[C@H](CC)C)C)=O)CC(C)C)C)=O)C(C)C)C)=O)C)=O)CC3=CC=C(OC)C=C3)CCC2)CC(C)C)C)C)C)C '
               'NAME: Clonostachysin A REASON: CORRECT Molecule is considered '
               'a macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@@H]6[C@H](O)[C@@H](O[C@@H]([C@H]6O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%11CO)O '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO '
               'NAME: CID 91852766 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@@H]5[C@H](O)[C@@H](O[C@@H]([C@H]5O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO)O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO '
               'NAME: CID 91852622 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4R,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-hydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Molecule is considered a macromolecule '
               'based on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@H]%13O[C@@H]([C@@H](O)[C@H](O)[C@@H]%13O)CO)CO)CO)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-3-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-4-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4R,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-hydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Molecule is considered a macromolecule '
               'based on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)[C@@H]7O)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@H]%11O[C@@H]([C@@H](O)[C@H](O[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O)CO)[C@@H]%11O)CO)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3S,4S,5S,6R)-3-[(2R,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@H]2[C@@H](O)[C@H](OC(O)[C@@H]2NC(=O)C)CO[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO)[C@H](O)[C@H]3NC(=O)C)CO)[C@@H]1O)CO[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)CO)[C@H](O)[C@H]9NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[(2R,3R,4R,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-Acetamido-6-[[(2R,3S,4S,5R,6R)-6-[(2R,3R,4R,5R)-5-acetamido-2-[[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,6-dihydroxyoxan-4-yl]oxy-4-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N([C@H](C(N[C@H](C(N[C@H]1[C@H](O)C=2C3=C(C=CC=C3)N(C2)C(C=C)(C)C)=O)[C@@H](C=C(C)C)C)=O)CC(C)C)C)=O)C(C)C)[C@H](OC)C4=CC=CC=C4)C)C[C@H](CO)C)C '
               'NAME: Cyclomarin C REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'S(CC[C@@H]1NC(=O)[C@H](NC(=O)[C@@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC([C@@H](NC([C@H](NC([C@@H](NC([C@@H](NC([C@H](NC([C@@H](NC1=O)C(C)C)=O)[C@H](O)C)=O)C(CC)C)=O)[C@@H](O)C)=O)C(C)C)=O)C(C)C)=O)C(C)C)CC2=CC=CC=C2)C(C)C)=C/C)CCCN=C(N)N)CC3=CC=C(O)C=C3)C '
               'NAME: Tolybybetaidin B REASON: CORRECT Molecule is considered '
               'a macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O[C@H]2[C@H](O)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)O)[C@H]2O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)CO)[C@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H]7NC(=O)C)CO)CO)O[C@@H]([C@@H](O)[C@@H]1O)CO)[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H](O[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)[C@H]%11NC(=O)C)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: CID 91847722 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: CORRECT Molecule is considered a macromolecule '
               'based on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4R,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule is considered a macromolecule based '
               'on repeating peptide, glycosidic, or nucleic acid bond '
               'structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)[C@H]6O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO)CO)[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15O[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO)CO)[C@H](O)[C@H]%14NC(=O)C)CO '
               'NAME: CID 91860918 REASON: CORRECT Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               'False positives: SMILES: '
               'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CC)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CCCN=C(N)N)C '
               'NAME: [D-Asp3]MC-RAba REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O)[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@H](O)[C@H]5O)CO)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@H](O)[C@H]3NC(=O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-5-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5R)-3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]oxy-4,5-dihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)N([C@H](C(=O)OC[C@@H](C=C1)NC(=O)[C@@H](NC(=O)C[C@H](O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C/C=C\\CCCCCC)CC2=CC=C(O)C=C2)C(C)C)CO)C(C)C)CC3=CC=C(O)C=C3)C)C(C)C)C '
               'NAME: Thalabetaospiramide A6 REASON: WRONGLY CLASSIFIED '
               'Molecule is considered a macromolecule based on repeating '
               'peptide, glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H](O)[C@@H]1O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5S)-5-Acetamido-1,2,4,6-tetrahydroxyhexan-3-yl]oxy-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5R,6R)-4-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H]([C@H](O)CN)C(N[C@H](C(NC[C@H]([C@@H](C(NC1=CC)=O)NC(=O)CCCCCCCCC)O)=O)[C@@H](O)CN)=O)CCCN=C(N)N)CC(C)C)CCN '
               'NAME: Ogipeptin A REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)CO)[C@H]1CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4NC(=O)C)CO)CO)[C@@H]6[C@H](O)[C@@H](O[C@@H]([C@H]6O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%11CO)O[C@H]%12[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%12CO[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)O '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)OC[C@H]3OC(O)[C@H](NC(=O)C)[C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H]5NC(=O)C)CO)[C@H]4O)CO)[C@H]3O)O[C@@H]([C@@H]1O)CO)[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4R,5R)-5-acetamido-4-[(2R,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,6-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]%10O)CO)[C@H](O)[C@@H]9NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O1[C@@H](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@H](O[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)[C@@H](O)[C@@H](O[C@@H]3CO)O)[C@H](NC(=O)C)[C@@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]6O)CO)[C@H]1CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-5-[(2S,3R,4S,5S,6R)-3,5-Dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-2-[(2S,3R,4S,5S,6R)-2-[(2R,3R,4R,5R,6R)-5,6-dihydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'CC(C)CCCCC(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CCNCS(O)(=O)=O)NC1=O)[C@@H](C)O '
               'NAME: colistimethate B REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(C)=O)[C@H](OC[C@H]3OC(O)[C@H](NC(C)=O)[C@@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O[C@@]5(C[C@H](O)[C@@H](NC(C)=O)[C@@]([H])(O5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]4O)[C@H]3O)O[C@@H]2CO)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO '
               'NAME: '
               'alpha-Neup5Ac-(2->3)-beta-D-Galp-(1->3)-[alpha-Neup5Ac-(2->3)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->6)]-D-GalpNAc '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H]([C@H](O[C@@H]([C@@H]1O[C@@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO[C@H]3O[C@@]([C@H]([C@@H]([C@@H]3O[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O[C@@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)O)NC(=O)C)O)O)([C@H](O)CO)[H])O)O)NC(CN)=O)C(O)=O)O[C@@H]6[C@H](O)[C@H](O[C@@]([C@H]6O)([C@@H](OP(=O)(OCCN)O)CO[C@H]7O[C@@]([C@H]([C@@H]([C@@H]7O)O)O)([C@@H](O)CO)[H])[H])O[C@@H]8[C@H](O)[C@H](O[C@@]([C@H]8O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O)([C@@H](O)CO)[H])O[C@@H]%10[C@@H](C[C@@](O[C@@]%10([C@H](O)CO[C@@H]%11[C@@H]([C@H]([C@H](CO%11)N)O)O)[H])(C(O)=O)O)O[C@@]%12(C[C@H]([C@H]([C@](O%12)([C@H](O)CO)[H])O)O)C(O)=O)O[C@H]%13O[C@@]([C@H]([C@@H]([C@@H]%13O[C@H]%14O[C@@]([C@H]([C@@H]([C@@H]%14O)O)O)([C@@H](O)CO)[H])O)O)([C@H](O)CO)[H] '
               'NAME: '
               'alpha-D-Glc-(1->4)-alpha-D-GalNAc-(1->2)-alpha-DD-Hep-(1->6)-alpha-D-GlcNGly-(1->4)-[alpha-LD-Hep-(1->2)-alpha-DD-Hep-(1->2)]-alpha-D-GalA-(1->3)-[alpha-LD-Hep-(1->7)]-alpha-LD-Hep6PEtn-(1->3)-[beta-D-Glc-(1->4)]-alpha-LD-Hep-(1->5)-[alpha-Kdo-(2->4)][beta-L-Arap4N-(1->8)]-alpha-Kdo '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO)[C@@H]3O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO)[C@@H]6O)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](O)[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](O)[C@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](O)C(O[C@@H]4CO)O)O[C@@H]1CO)[C@H]5O[C@@H]([C@@H](O[C@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5O)CO '
               'NAME: '
               '(2S,3R,4S,5S,6R)-2-[[(2R,3S,4S,5R,6R)-6-[(2R,3S,4R,5R,6R)-6-[(2R,3S,4R,5R,6R)-6-[(2R,3S,4R,5R,6R)-6-[(2R,3S,4R,5R,6R)-6-[(2R,3S,4R,5R,6R)-4,5-Dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O=C1N(CCC[C@@H]1NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C2NC(=NCC2)[C@H](NC(=O)[C@@H](N(O)C(=O)CNC(=O)CNC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H]3[N+]4=C(NCC3)C(NC(=O)CCC(=O)N)=CC=5C4=CC(O)=C(C5)O)C)CCCCN)CC(=O)N)CCC(=O)N)CO)C)C '
               'NAME: Pyoverdin Pf/3 ATCC 17400 REASON: WRONGLY CLASSIFIED '
               'Molecule is considered a macromolecule based on repeating '
               'peptide, glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](CCCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)C)CCCCN=C(N)N)C '
               'NAME: MC-HarHar REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@@H](O)[C@H]5NC(=O)C)CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H]%12O[C@@H]%14O[C@H]([C@@H](O)[C@@H](O)[C@@H]%14O)C)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO '
               'NAME: CID 146015968 REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H]([C@H](O[C@@H]([C@@H]1O[C@@H]2[C@@H]([C@H]([C@@H]3[C@H](O2)CO[C@]([C@@H]([C@H]([C@H]([C@@H](CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)O)O)O)O)NC(C)=O)(O3)[H])O)N)C(O)=O)O[C@@H]6[C@H](O)[C@H](O[C@@]([C@H]6O)([C@@H](OP(=O)(OCCN)O)CO[C@H]7O[C@@]([C@H]([C@@H]([C@@H]7O)O)O)([C@@H](O)CO)[H])[H])O[C@@H]8[C@H](O)[C@H](O[C@@]([C@H]8O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O)([C@@H](O)CO)[H])O[C@@H]%10[C@@H](C[C@@](O[C@@]%10([C@H](O)CO[C@@H]%11[C@@H]([C@H]([C@H](CO%11)N)O)O)[H])(C(O)=O)O)O[C@@]%12(C[C@H]([C@H]([C@](O%12)([C@H](O)CO)[H])O)O)C(O)=O)O[C@H]%13O[C@@]([C@H]([C@@H]([C@@H]%13O[C@H]%14O[C@@]([C@H]([C@@H]([C@@H]%14O)O)O)([C@@H](O)CO)[H])O)O)([C@H](O)CO)[H] '
               'NAME: '
               'alpha-D-Glc-(1->6)-beta-D-Gal-(1->4)-(1S)-D-GaloNAc-(1->4,6)-alpha-D-GalN-(1->4)-[alpha-LD-Hep-(1->2)-alpha-DD-Hep-(1->2)]-alpha-D-GalA-(1->3)-[alpha-LD-Hep-(1->7)]-alpha-LD-Hep6PEtn-(1->3)-[beta-D-Glc-(1->4)]-alpha-LD-Hep-(1->5)-[alpha-Kdo-(2->4)][beta-L-Arap4N-(1->8)]-alpha-Kdo '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'S(O[C@@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3[C@@H](O[C@@H]4[C@H](O)[C@@H](O[C@@H]([C@H]4O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O[C@@H]([C@@H](O)[C@@H]3O)CO)O[C@@H]2CO)O[C@@H]1CO)(O)(=O)=O '
               'NAME: '
               '[(2R,3R,4R,5R,6S)-5-Acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5S)-5-acetamido-2,4,6-trihydroxy-1-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyhexan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl] '
               'hydrogen sulfate REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4R,5R,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3-hydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3CO[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4S,5R,6R)-2-[(2R,3S,4R,5R,6R)-5-acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-4,6-dihydroxy-2-[[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule is considered a '
               'macromolecule based on repeating peptide, glycosidic, or '
               'nucleic acid bond structures.\n'
               ' * SMILES: '
               'CN1[C@@H](Cc2ccc(Oc3cc4cc(-c5ccc6c(C[C@@H](NC(=O)C(=O)c7cc(Cl)c(O)c(Cl)c7)C(=O)N[C@@H](C(=O)N[C@H]4C(=O)N[C@@H](C1=O)c1cc(Cl)c(O)c(Cl)c1)c1cc(Cl)c(O)c(Cl)c1)c[nH]c6c5)c3O)cc2)C(=O)N[C@@H](C(O)=O)c1ccc(O)cc1 '
               'NAME: isocomplestatin REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               ' * SMILES: '
               'S1C2=NC(=C1)C(=O)N[C@H](C(=O)N3[C@H](C(=O)N[C@H](C(=O)NC(C4=NC(C(N[C@H](C(N[C@H](C(N[C@H]2CC5=CC=C(O)C=C5)=O)CC(C)C)=O)[C@H](CC)C)=O)CS4)CC(C)C)CO)CCC3)CC(=O)N '
               'NAME: Kororamide REASON: WRONGLY CLASSIFIED Molecule is '
               'considered a macromolecule based on repeating peptide, '
               'glycosidic, or nucleic acid bond structures.\n'
               'False negatives: SMILES: '
               'O([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)COC(=O)CCCCCCC(C)C)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: '
               '[(2R,3S,4S,5R,6S)-3,4,5-Trihydroxy-6-[(2S,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methyl '
               '8-methylnonanoate REASON: MISSED Molecular weight 496.25 Da is '
               'less than the minimum macromolecule threshold 500 Da\n'
               ' * SMILES: '
               'O1C(OC=2C=C(CC(O)CCC(O)=O)C=CC2O)C(O)C(O)C(O)C1C(O)=O NAME: '
               '6-[5-(4-carboxy-2-hydroxybutyl)-2-hydroxyphenoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: MISSED Molecular weight 402.12 Da is less than '
               'the minimum macromolecule threshold 500 Da\n'
               ' * SMILES: '
               'O=C1NCCC[C@@H]2N(C(=O)C(C2=O)=C(O)C=C[C@H]3[C@H](CC=C1)[C@H]4C=C[C@H]5[C@H](C(=O)C)[C@@H](C[C@@H]5[C@H]4C3)C)C '
               'NAME: 30-oxo-28-N-methylikarugamycin REASON: MISSED No '
               'sufficient repeating unit motifs commonly found in '
               'macromolecules detected.\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@@H](O)C=C[C@@H](CCC(C=2C=3C(C=4[C@]1(CCC(=O)NC4C(=O)C3C=C(C)C2O)C)=O)=O)CC)CC(O)(C)C '
               'NAME: Divergolide K REASON: MISSED No sufficient repeating '
               'unit motifs commonly found in macromolecules detected.\n'
               ' * SMILES: '
               'CCOC(=O)[C@H]1CC=CC[C@@H](C(=O)O[C@@H]2[C@H]([C@@H]([C@H](O[C@@H]2OC)CO)OC(=O)NC3=CC=C(C=C3)Br)OC1=O)C(=O)OCC '
               'NAME: LSM-36740 REASON: MISSED No sufficient repeating unit '
               'motifs commonly found in macromolecules detected.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)C(O)C1O[C@@H](CC=C(C)C)/C(/C)=C/C=C/C(=C/[C@@](O)(C/C=C/C=C/C(O)=O)C)/C)CO '
               'NAME: '
               '14-O-(alpha-D-mannopyranosyl)-7S,14S-dihydroxy-7,9,13,17-tetramethyl-2E,4E,8E,10E,12E,16E-octadecahexaenoic '
               'acid REASON: MISSED No sufficient repeating unit motifs '
               'commonly found in macromolecules detected.\n'
               ' * SMILES: '
               'O=C1C=CC(=O)[C@H](OC(=O)C)C(=C[C@H](CC=C[C@@H]2[C@@]13C(=O)N[C@H]([C@@H]3[C@H](C)[C@@]4([C@H]2O4)C)CC5=CC=CC=C5)C)C '
               'NAME: Cytochalasin K REASON: MISSED No sufficient repeating '
               'unit motifs commonly found in macromolecules detected.\n'
               ' * SMILES: '
               'O1C([C@@H](O)C(O)[C@H](O)[C@H]1OCC(OC(=O)CCCCCCCCCCCCCCC)CCCCCCCCCCCCCCCCCC)CO '
               'NAME: '
               '1-O-alpha-D-glucopyranosyl-(2-hexadecanoyloxy)-eicosan-1-ol '
               'REASON: MISSED No sufficient repeating unit motifs commonly '
               'found in macromolecules detected.\n'
               ' * SMILES: '
               'O(C1(OC(C(O)C1O)CO)CO)C2OC(C(O)C(O)C2O)COC3OC(C(O)C(O)C3O)COC(=O)/C(/C)=C/C '
               'NAME: '
               '[6-[[6-[3,4-dihydroxy-2,5-bis(hydroxymethyl)oxolan-2-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-3,4,5-trihydroxyoxan-2-yl]methyl '
               '(E)-2-methylbut-2-enoate REASON: MISSED No sufficient '
               'repeating unit motifs commonly found in macromolecules '
               'detected.\n'
               ' * SMILES: '
               'S1C2=NC(=C1)C(=O)NC(C=3SC=C(N3)C(=O)NC(C=4OC(=C(N4)C(=O)NC2C(C)C)C)C)C '
               'NAME: '
               '4,7,18-Trimethyl-11-propan-2-yl-6-oxa-13,20-dithia-3,10,17,22,23,24-hexazatetracyclo[17.2.1.15,8.112,15]tetracosa-1(21),5(24),7,12(23),14,19(22)-hexaene-2,9,16-trione '
               'REASON: MISSED Molecular weight 488.13 Da is less than the '
               'minimum macromolecule threshold 500 Da\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Molecular weight 226.10 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Molecular weight 313.17 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'No sufficient recurring motifs '
                                               'typical of macromolecules '
                                               'detected.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'No sufficient recurring motifs '
                                               'typical of macromolecules '
                                               'detected.'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Molecular weight 413.37 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Molecular weight 322.09 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Molecular weight 370.14 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Molecular weight 300.17 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Molecular weight 455.35 Da is '
                                               'less than the minimum '
                                               'macromolecule threshold 500 '
                                               'Da'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'No sufficient recurring motifs '
                                               'typical of macromolecules '
                                               'detected.'}],
    'sample_false_negatives': [   {   'smiles': 'O([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)COC(=O)CCCCCCC(C)C)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO',
                                      'name': '[(2R,3S,4S,5R,6S)-3,4,5-Trihydroxy-6-[(2S,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methyl '
                                              '8-methylnonanoate',
                                      'reason': 'Molecular weight 496.25 Da is '
                                                'less than the minimum '
                                                'macromolecule threshold 500 '
                                                'Da'},
                                  {   'smiles': 'O1C(OC=2C=C(CC(O)CCC(O)=O)C=CC2O)C(O)C(O)C(O)C1C(O)=O',
                                      'name': '6-[5-(4-carboxy-2-hydroxybutyl)-2-hydroxyphenoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Molecular weight 402.12 Da is '
                                                'less than the minimum '
                                                'macromolecule threshold 500 '
                                                'Da'},
                                  {   'smiles': 'O=C1N([C@H](C(=O)N(CC(=O)N([C@H](C(=O)N2[C@H](C(=O)N(C)[C@H](C(N[C@H](C(N([C@H](C(N([C@H](C(N([C@H]1[C@H](CC)C)C)=O)CC(C)C)C)=O)C(C)C)C)=O)C)=O)CC3=CC=C(OC)C=C3)CCC2)CC(C)C)C)C)C)C',
                                      'name': 'Clonostachysin A',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'O=C1NCCC[C@@H]2N(C(=O)C(C2=O)=C(O)C=C[C@H]3[C@H](CC=C1)[C@H]4C=C[C@H]5[C@H](C(=O)C)[C@@H](C[C@@H]5[C@H]4C3)C)C',
                                      'name': '30-oxo-28-N-methylikarugamycin',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'O=C1N([C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N([C@H](C(N[C@H](C(N[C@H]1[C@H](O)C=2C3=C(C=CC=C3)N(C2)C(C=C)(C)C)=O)[C@@H](C=C(C)C)C)=O)CC(C)C)C)=O)C(C)C)[C@H](OC)C4=CC=CC=C4)C)C[C@H](CO)C)C',
                                      'name': 'Cyclomarin C',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'O=C1O[C@H]([C@@H](O)C=C[C@@H](CCC(C=2C=3C(C=4[C@]1(CCC(=O)NC4C(=O)C3C=C(C)C2O)C)=O)=O)CC)CC(O)(C)C',
                                      'name': 'Divergolide K',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'CCOC(=O)[C@H]1CC=CC[C@@H](C(=O)O[C@@H]2[C@H]([C@@H]([C@H](O[C@@H]2OC)CO)OC(=O)NC3=CC=C(C=C3)Br)OC1=O)C(=O)OCC',
                                      'name': 'LSM-36740',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)C(O)C1O[C@@H](CC=C(C)C)/C(/C)=C/C=C/C(=C/[C@@](O)(C/C=C/C=C/C(O)=O)C)/C)CO',
                                      'name': '14-O-(alpha-D-mannopyranosyl)-7S,14S-dihydroxy-7,9,13,17-tetramethyl-2E,4E,8E,10E,12E,16E-octadecahexaenoic '
                                              'acid',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'O=C1C=CC(=O)[C@H](OC(=O)C)C(=C[C@H](CC=C[C@@H]2[C@@]13C(=O)N[C@H]([C@@H]3[C@H](C)[C@@]4([C@H]2O4)C)CC5=CC=CC=C5)C)C',
                                      'name': 'Cytochalasin K',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'},
                                  {   'smiles': 'CCC(C)\\C=C(C)\\C=C/C(O)C(C)C(=O)NCC(=O)N\\C(=C/C)C(=O)N[C@@H]([C@H](C)N)C(=O)N[C@@H]([C@@H](C)[C@@H](C)C(N)=O)C(=O)N[C@@H]1[C@H](OC(=O)[C@@H]2C[C@@H](Cl)CCN2C(=O)[C@H](NC(=O)[C@H]([C@@H](C)O)N(C)C(=O)[C@H](C)NC(=O)CNC(=O)[C@@H](COC)NC1=O)[C@H](OC)c1ccc(O)cc1)C(C)C',
                                      'name': 'Mirabamide H',
                                      'reason': 'No sufficient recurring '
                                                'motifs typical of '
                                                'macromolecules detected.'}],
    'attempt': 4,
    'reasoning': 'To improve the classification of macromolecules, the initial '
                 'attempt needs refinement in terms of both criteria and '
                 'structural pattern recognition. The existing code focuses on '
                 'molecular weight and identifying common repeating unit '
                 'linkages, like peptide bonds, glycosidic bonds, or nucleic '
                 'acid motifs. Here are potential improvements:\n'
                 '\n'
                 '1. **Molecular Weight Threshold**: The minimum molecular '
                 'weight for macromolecules was set as 500 Da. Given some '
                 'examples are slightly below this, consider setting a lower '
                 'threshold or using additional structural checks alongside '
                 'molecular weight.\n'
                 '\n'
                 '2. **Revisiting Linkage Patterns**: Current SMILES '
                 'substructure patterns for detecting peptide, glycosidic, and '
                 'nucleic acid linkages might not be exhaustive or precise '
                 "enough. Expand these patterns and ensure they've considered "
                 'variations like cyclic peptides or nucleic acids with '
                 'modifications.\n'
                 '\n'
                 '3. **Repetition and Chain Length**: Macromolecules often '
                 'feature repeating units or extended chains. Enhance '
                 'detection by:\n'
                 '   - Counting different types of repeated motifs alongside '
                 'peptide, glycosidic, and nucleic acid links.\n'
                 '   - Checking for extended polymer-like sequences.\n'
                 '\n'
                 '4. **Common Macromolecular Features**: Incorporate '
                 'additional macromolecular characteristics observed in '
                 'biological systems, such as:\n'
                 '   - Polyerization (long repetitive sequences).\n'
                 '   - Structural motifs typical for DNA/RNA, proteins (amino '
                 'acid sequences), or polysaccharides.\n'
                 '\n'
                 '5. **Fail-safe and Error Handling**: Ensure the program '
                 'includes error handling for unexpected SMILES '
                 'configurations.\n'
                 '\n'
                 '6. **Performance and Scalability**: Verify the methods can '
                 'process complex structures efficiently without missing key '
                 'structural elements.\n'
                 '\n'
                 "Here's a revised code block that incorporates these "
                 'improvements:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1582,
    'num_false_positives': 3134,
    'num_true_negatives': 137100,
    'num_false_negatives': 484,
    'num_negatives': None,
    'precision': 0.33545377438507207,
    'recall': 0.7657308809293321,
    'f1': 0.46652904747861995,
    'accuracy': 0.9745748418833451,
    'negative_predictive_value': 0.9964821490871032}