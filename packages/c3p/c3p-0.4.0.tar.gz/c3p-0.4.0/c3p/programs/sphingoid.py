"""
Classifies: CHEBI:35785 sphingoid
"""
"""
Classifies: sphingoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_sphingoid(smiles: str):
    """
    Determines if a molecule is a sphingoid based on its SMILES string.
    A sphingoid is defined as sphinganine, its homologs and stereoisomers,
    and the hydroxy and unsaturated derivatives of these compounds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a sphingoid, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find primary amine nitrogen atoms (degree 1 nitrogen with no charge)
    amine_atoms = [atom for atom in mol.GetAtoms()
                   if atom.GetAtomicNum() == 7 and atom.GetDegree() == 1 and atom.GetFormalCharge() == 0]
    if not amine_atoms:
        return False, "No primary amino group found"

    for amine_atom in amine_atoms:
        n_idx = amine_atom.GetIdx()

        # Get the carbon atom attached to the amine nitrogen (C2)
        c2_atoms = [nbr for nbr in amine_atom.GetNeighbors() if nbr.GetAtomicNum() == 6]
        if not c2_atoms:
            continue  # No carbon attached to nitrogen
        c2_atom = c2_atoms[0]
        c2_idx = c2_atom.GetIdx()

        # Check for hydroxyl groups on carbons adjacent to C2 (C1 and C3)
        has_adjacent_hydroxyl = False
        
        # Get neighbors of C2 atom
        c2_neighbors = c2_atom.GetNeighbors()
        for atom in c2_neighbors:
            if atom.GetAtomicNum() == 6 and atom.GetIdx() != n_idx:  # Exclude nitrogen
                # Check if this carbon has a hydroxyl group
                for nbr in atom.GetNeighbors():
                    if nbr.GetAtomicNum() == 8 and nbr.GetDegree() == 1:
                        has_adjacent_hydroxyl = True
                        break
            if has_adjacent_hydroxyl:
                break

        if not has_adjacent_hydroxyl:
            continue  # No hydroxyl group adjacent to amino group

        # Now, check the aliphatic chain length starting from C2
        visited = set()
        chain_atoms = []

        def traverse_chain(atom):
            if atom.GetIdx() in visited:
                return
            visited.add(atom.GetIdx())
            if atom.GetAtomicNum() != 6:
                return
            chain_atoms.append(atom)
            for nbr in atom.GetNeighbors():
                bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                if bond.IsInRing():
                    continue  # Skip ring structures
                if nbr.GetAtomicNum() == 6 and nbr.GetIdx() != amine_atom.GetIdx():
                    traverse_chain(nbr)

        traverse_chain(c2_atom)
        chain_length = len(chain_atoms)

        if chain_length < 12:
            continue  # Chain too short to be sphingoid

        # If all checks passed
        return True, "Molecule matches sphingoid structural features"

    return False, "Molecule does not match sphingoid structural features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35785',
                          'name': 'sphingoid',
                          'definition': 'Sphinganine, its homologs and '
                                        'stereoisomers, and the hydroxy and '
                                        'unsaturated derivatives of these '
                                        'compounds.',
                          'parents': ['CHEBI:26739'],
                          'xrefs': ['LIPID_MAPS_class:LMSP01'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 22,
                           'log_lines_of_code': 3.091042453358316,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetDegree',
                                                 'GetFormalCharge',
                                                 'GetIdx',
                                                 'MolFromSmiles',
                                                 'GetAtoms',
                                                 'GetAtomicNum'],
                           'methods_called_count': 6,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_sphingoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No primary amino group '
                                          'found"',
                                          'False, "Molecule does not match '
                                          'sphingoid structural features"'],
                           'returns_count': 3,
                           'complexity': 3.0182084906716633},
    'message': '\n'
               'Error: Error executing '
               "is_sphingoid('CCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C'):\n"
               " 'Atom' object has no attribute 'GetBondBetweenAtoms'\n"
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'NCC(=O)CCC([O-])=O',
                                     'name': '5-aminolevulinate',
                                     'reason': 'Molecule does not match '
                                               'sphingoid structural features'},
                                 {   'smiles': '[H][C@@]12CCCC(C)(C)C1CC[C@]1([H])[C@@]2(C)CC[C@]2(C)[C@]([H])(CC[C@@]12C)[C@H](C)CCCC(C)C',
                                     'name': 'cucurbitane',
                                     'reason': 'No primary amino group found'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC2=CC=CC=C2',
                                     'name': 'Arg-Phe-Tyr',
                                     'reason': 'Molecule does not match '
                                               'sphingoid structural features'},
                                 {   'smiles': 'C(CC(C(=O)O)NC(CCC(=O)O)C(=O)O)CN',
                                     'name': 'ornaline',
                                     'reason': 'Molecule does not match '
                                               'sphingoid structural features'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(15:0/18:1(11Z))',
                                     'reason': 'Molecule does not match '
                                               'sphingoid structural features'},
                                 {   'smiles': 'O=CC1=C(O)C=CC2=C1[C@H](C3=C4O[C@H](C(O)(C)C)COC4=CC(=C3)C)[C@@H](C(O)(C)C)C2',
                                     'name': 'Diaporindene A',
                                     'reason': 'No primary amino group found'},
                                 {   'smiles': 'O(C(CCCCCCCCC)CCC/C=C/C)C(=O)/C=C(/C)\\C(O)=O',
                                     'name': 'Chaetomellic acid B',
                                     'reason': 'No primary amino group found'},
                                 {   'smiles': 'Oc1ccc(cc1)[C@H]1Oc2cc(O)cc([C@@H]3[C@H](Oc4ccc(\\C=C\\c5cc(O)cc(O)c5)cc34)c3ccc(O)cc3)c2[C@@H]1c1cc(O)cc(O)c1',
                                     'name': 'trans-diptoindonesin B',
                                     'reason': 'No primary amino group found'},
                                 {   'smiles': 'O1C(CC(=O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3',
                                     'name': "4',7-dihydroxyflavanone",
                                     'reason': 'No primary amino group found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO',
                                     'name': 'beta-D-GlcpNAc-(1->4)-beta-D-Galp-(1->4)-D-GlcpNAc',
                                     'reason': 'No primary amino group found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCC[C@@H](O)[C@@H]([NH3+])CO',
                                      'name': 'hexadecasphinganine(1+)',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-hexadecanoyl-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-nonadecanoyl-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxypentacosanoyl)-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxytetracosanoyl)-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)[NH+](C)C',
                                      'name': 'N,N-dimethylsphingosine(1+)',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-pentacosanoyl-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxynonadecanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxydocosanoyl)-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No primary amino group found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxyoctadecanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine',
                                      'reason': 'No primary amino group '
                                                'found'}],
    'attempt': 1,
    'reasoning': 'The error in the previous code occurred because the '
                 '`GetBondBetweenAtoms` method was incorrectly called on an '
                 '`Atom` object instead of the `Mol` object. In RDKit, '
                 '`GetBondBetweenAtoms` is a method of the `Mol` object. To '
                 'fix this, we need to call '
                 '`mol.GetBondBetweenAtoms(atom_idx1, atom_idx2)`.\n'
                 '\n'
                 'Additionally, to improve the classification, we can refine '
                 'our approach to more accurately capture the structural '
                 'features of sphingoids:\n'
                 '\n'
                 '1. **Identify primary amino groups**: Look for nitrogen '
                 'atoms with a degree of 1 (connected to one other atom) and '
                 'no formal charge.\n'
                 '2. **Check for adjacent hydroxyl groups**: Verify that there '
                 'are hydroxyl groups on carbons adjacent to the carbon '
                 'attached to the amino group (positions C1 and/or C3).\n'
                 '3. **Verify the aliphatic chain length**: Sphingoids '
                 'typically have a long carbon chain (usually at least 12 '
                 'carbons in the chain excluding the backbone carbons).\n'
                 '4. **Allow for unsaturation**: The aliphatic chain may '
                 'contain double bonds.\n'
                 '5. **Exclude ring structures**: Ensure that the main '
                 'aliphatic chain is not part of a ring.\n'
                 '\n'
                 'Here is the corrected and improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 42,
    'num_false_positives': 114,
    'num_true_negatives': 142091,
    'num_false_negatives': 53,
    'num_negatives': None,
    'precision': 0.2692307692307692,
    'recall': 0.4421052631578947,
    'f1': 0.3346613545816733,
    'accuracy': 0.9988264230498946,
    'negative_predictive_value': 0.999627138676272}