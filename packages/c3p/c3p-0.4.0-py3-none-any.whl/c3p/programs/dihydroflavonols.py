"""
Classifies: CHEBI:48039 dihydroflavonols
"""
from rdkit import Chem

def is_dihydroflavonols(smiles: str):
    """
    Determines if a molecule is a dihydroflavonol based on its SMILES string.
    A dihydroflavonol is a hydroxyflavanone with a hydroxyl group at position 3 of the heterocyclic ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dihydroflavonol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for dihydroflavonol pattern: flavanone backbone with hydroxyl group at position 3
    dihydroflavonol_pattern = Chem.MolFromSmarts('O[C@H]1[C@@H](Oc2cc(O)cc(O)c2C1=O)')  # Simplified pattern
    if mol.HasSubstructMatch(dihydroflavonol_pattern):
        return True, "Contains dihydroflavonol structure"

    # Look for hydroxyflavanone pattern with hydroxyl group at position 3
    hydroxyflavanone_pattern = Chem.MolFromSmarts('OC1C(OC2=C(C=CC(O)=C2)C1=O)')  # More general pattern
    matches = mol.GetSubstructMatches(hydroxyflavanone_pattern)
    if matches:
        # Check the attachment positions to ensure hydroxyl is at position 3
        for match in matches:
            atom_positions = [mol.GetAtomWithIdx(idx).GetIdx() for idx in match]
            # Ensure one hydroxyl is attached at position 3
            # (This is a simplified check; actual check might require mapping atom indices correctly)
            has_hydroxy_at_3 = False
            for bond in mol.GetBonds():
                if bond.GetBeginAtomIdx() in atom_positions and bond.GetEndAtomIdx() in atom_positions:
                    if mol.GetAtomWithIdx(bond.GetBeginAtomIdx()).GetSymbol() == 'O' and \
                       mol.GetAtomWithIdx(bond.GetEndAtomIdx()).GetSymbol() == 'C':
                        has_hydroxy_at_3 = True
                        break
            if has_hydroxy_at_3:
                return True, "Contains hydroxyflavanone structure with hydroxyl group at position 3"

    return False, "Does not fit dihydroflavonol or hydroxyflavanone pattern adequately"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:48039',
                          'name': 'dihydroflavonols',
                          'definition': 'Any hydroxyflavanone in which a '
                                        'hydroxy group is present at position '
                                        '3 of the heterocyclic ring.',
                          'parents': ['CHEBI:24697'],
                          'xrefs': ['KEGG:C15570'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C1C2=C(OC(=C1)C)C3=C(OC)C=C(OC)C=C3C(=C2O)C4=C5OC(=CC(C5=C(O)C=6C4=CC(OC)=CC6OC)=O)C',
                                     'name': 'Isonigerone',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                     'name': '1-myristoyl-2-oleoyl-sn-glycero-3-phosphatidylglycerol(1-)',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'C(=C\\C/C=C\\CCCC(NC)=O)\\C/C=C\\C/C=C\\CCCCC',
                                     'name': 'N-methyl arachidonoyl amine',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'OC1(O)[C@]23N(CC1)C(N(O)[C@H]([C@@]3(N=C(N2)N)[H])CO)=N',
                                     'name': 'Decarbamoylneosaxitoxin',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'S([C@H]1N(C(=O)/C(=C\\C2=CC=C(OCC=C(C)C)C=C2)/N(C1=O)C)C)C',
                                     'name': 'Fusaperazine F',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'Oc1ccccc1I',
                                     'name': '2-iodophenol',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'O=C1N(CC(=O)N[C@H](C(=O)O[C@H]([C@@H](C(NC(C=C1)=C)=O)C)C(CCCCCCCCCCCCCC)C)C(O)C(=O)N)C',
                                     'name': 'Rakicidin H',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C',
                                     'name': 'Prenylterphenyllin F',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'Gal2GlcNAc2Man3GlcNAcFucGlcNAc',
                                     'reason': 'Does not fit dihydroflavonol '
                                               'or hydroxyflavanone pattern '
                                               'adequately'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@H]1[C@@H](OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1',
                                      'name': '(-)-trans-fustin',
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'},
                                  {   'smiles': 'O1C(C(O)C(=O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3',
                                      'name': "(2R,3R)-3,4',7-Trihydroxyflavanone",
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'},
                                  {   'smiles': 'O[C@@H]1[C@H](OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1',
                                      'name': '(+)-trans-fustin',
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'},
                                  {   'smiles': 'O[C@@H]1[C@H](Oc2cc(O)ccc2C1=O)c1ccc(O)cc1',
                                      'name': 'garbanzol',
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'},
                                  {   'smiles': 'OC1C(OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1',
                                      'name': 'fustin',
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'},
                                  {   'smiles': 'CC1=C[C@H]([C@@H]([C@H](C1)c1ccc(O)cc1O)C(=O)c1ccc(O)cc1O)c1c(O)ccc([C@H]2Oc3cc(O)ccc3C(=O)[C@@H]2O)c1O',
                                      'name': 'guangsangon K',
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'},
                                  {   'smiles': 'CC(C)=CCc1cc(ccc1O)[C@H]1Oc2c(CC=C(C)C)c(O)c(CC=C(C)C)cc2C(=O)[C@@H]1O',
                                      'name': 'lespeflorin B3',
                                      'reason': 'Does not fit dihydroflavonol '
                                                'or hydroxyflavanone pattern '
                                                'adequately'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as dihydroflavonols based on '
                 "their SMILES strings, we'll take the following approach:\n"
                 '\n'
                 '1. **Define Dihydroflavonols**: Dihydroflavonols are '
                 'hydroxyflavanones with a hydroxyl group at position 3 of the '
                 'heterocyclic ring. This corresponds to a specific bicyclic '
                 'structure with certain functional groups.\n'
                 '\n'
                 "2. **Structural Pattern Recognition**: We'll use SMARTS "
                 'patterns, which are like regular expressions for molecules, '
                 'to detect the key structural features of dihydroflavonols.\n'
                 '\n'
                 '3. **SMILES Parsing**: Use RDKit to parse the SMILES string '
                 'into a molecular structure.\n'
                 '\n'
                 '4. **Substructure Matching**: Use the defined SMARTS pattern '
                 'to match against the parsed molecular structure to determine '
                 'if it fits the dihydroflavonol template.\n'
                 '\n'
                 '5. **Return Classification Result**: If the structure '
                 'matches, return True with a suitable reason; otherwise, '
                 'return False with an explanation.\n'
                 '\n'
                 "Let's write the Python code for this classification task:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 56,
    'num_true_negatives': 142219,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.24324324324324326,
    'recall': 0.72,
    'f1': 0.3636363636363637,
    'accuracy': 0.9995572733661279,
    'negative_predictive_value': 0.9999507825573383}