"""
Classifies: CHEBI:16366 anthocyanidin cation
"""
"""
Classifies: Anthocyanidin Cation (flavylium‐type aglycon of anthocyanin cation)
Definition: Any organic cation that is an aglycon of anthocyanin cation; they are oxygenated derivatives of flavylium (2-phenylchromenylium).
This heuristic function checks for a positively charged oxygen within a six-membered (pyran) ring that is fused to at least one other aromatic ring,
and an aromatic (phenyl) substituent attached to one of the ring carbons.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_anthocyanidin_cation(smiles: str):
    """
    Determines if a molecule is an anthocyanidin cation (flavylium-type aglycon) based on its SMILES string.
    
    Heuristic criteria:
      1. The molecule must be valid.
      2. The overall molecule must carry positive charge(s).
      3. There must be at least one aromatic oxygen with formal charge +1.
      4. This oxygen should lie within a six-membered aromatic ring (the pyran ring of the flavylium core).
      5. The ring containing the [O+ ] should be fused to at least one other aromatic ring.
      6. At least one carbon of the candidate ring should have a substituent that is an aromatic ring (a phenyl group)
         representing the 2-phenyl substitution expected in a 2-phenylchromenylium core.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is classified as an anthocyanidin cation, False otherwise.
        str: Reason for classification.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Ensure explicit hydrogens are added to support aromaticity assignments if needed.
    mol = Chem.AddHs(mol)
    Chem.SanitizeMol(mol)
    
    # Check that the molecule has at least one positive formal charge.
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if total_charge <= 0:
        return False, "Molecule does not carry a net positive charge"
    
    # Look for candidate atoms: aromatic oxygen atoms with formal charge +1.
    candidate_oatoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 1 and atom.GetIsAromatic():
            candidate_oatoms.append(atom.GetIdx())
    
    if not candidate_oatoms:
        return False, "No aromatic oxygen atom with +1 charge found (flavylium moiety missing)"
    
    # Get ring information.
    ring_info = mol.GetRingInfo().AtomRings()
    
    # Function to check if a given ring (given as a tuple of atom indices) is aromatic.
    def is_ring_aromatic(ring):
        return all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)
    
    # Check candidates: look for a six-membered aromatic ring that contains a candidate [O+] atom.
    candidate_rings = []
    for ring in ring_info:
        if len(ring) == 6 and is_ring_aromatic(ring):
            if any(idx in ring for idx in candidate_oatoms):
                candidate_rings.append(ring)
    
    if not candidate_rings:
        return False, "No six-membered aromatic ring containing an [O+ ] atom found"
    
    # For each candidate ring, check for ring fusion: at least one other aromatic ring sharing 2 atoms.
    fused_found = False
    for ring in candidate_rings:
        for other_ring in ring_info:
            if ring == other_ring:
                continue
            # Check if rings share at least 2 atoms (typical for fused rings)
            shared_atoms = set(ring).intersection(set(other_ring))
            if len(shared_atoms) >= 2 and is_ring_aromatic(other_ring):
                fused_found = True
                break
        if fused_found:
            candidate_ring = ring
            break
    if not fused_found:
        return False, "No fused aromatic ring detected with the candidate flavylium ring"
    
    # Check for a phenyl substituent (an aromatic ring attached as a side chain)
    # We look for a carbon atom in the candidate ring that has a neighbor (not in candidate_ring) that is aromatic,
    # and that neighbor is part of a six-membered ring (phenyl group).
    phenyl_found = False
    candidate_ring_set = set(candidate_ring)
    for idx in candidate_ring:
        atom = mol.GetAtomWithIdx(idx)
        # Consider non-oxygen atoms in the candidate ring (should be sp2 carbons).
        if atom.GetSymbol() != 'C':
            continue
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() in candidate_ring_set:
                continue
            if nbr.GetIsAromatic() and nbr.GetSymbol() == 'C':
                # Check if the neighbor is part of a six-membered aromatic ring.
                for ring in ring_info:
                    if len(ring) == 6 and nbr.GetIdx() in ring and is_ring_aromatic(ring):
                        phenyl_found = True
                        break
            if phenyl_found:
                break
        if phenyl_found:
            break
    
    if not phenyl_found:
        return False, "No phenyl substituent attached to the flavylium core detected"
    
    # If all heuristic criteria are met, we consider the molecule as an anthocyanidin cation.
    return True, "Molecule contains a flavylium-type (2-phenylchromenylium) core with a positively charged oxygen, fused aromatic rings, and an attached phenyl group"

# For complex cases that may not be unambiguously classified, one could instead return (None, None).
# For example, if you prefer to use a more conservative approach, uncomment the next line.
# return None, None

# Example usage:
if __name__ == '__main__':
    # You can test one of the provided examples (e.g., hirsutidin)
    test_smiles = "COc1cc(O)c2cc(O)c([o+]c2c1)-c1cc(OC)c(O)c(OC)c1"
    result, reason = is_anthocyanidin_cation(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16366',
                          'name': 'anthocyanidin cation',
                          'definition': 'Any organic cation that is an aglycon '
                                        'of anthocyanin cation; they are '
                                        'oxygenated derivatives of flavylium '
                                        '(2-phenylchromenylium).',
                          'parents': ['CHEBI:25697', 'CHEBI:47916'],
                          'xrefs': [   'HMDB:HMDB0031460',
                                       'KEGG:C02003',
                                       'MetaCyc:Anthocyanidins',
                                       'Wikipedia:Anthocyanidins'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 95,
                           'log_lines_of_code': 4.553876891600541,
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
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 2,
                                                 3,
                                                 4,
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
                                                 3,
                                                 3,
                                                 4,
                                                 4,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'AddHs',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'SanitizeMol',
                                                 'GetSymbol',
                                                 'GetAtomWithIdx',
                                                 'GetIsAromatic',
                                                 'GetIdx',
                                                 'GetAtoms',
                                                 'GetFormalCharge',
                                                 'GetNeighbors',
                                                 'intersection',
                                                 'append'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_anthocyanidin_cation(smiles: str):',
                                       'is_ring_aromatic(ring):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule does not carry a '
                                          'net positive charge"',
                                          'False, "No aromatic oxygen atom '
                                          'with +1 charge found (flavylium '
                                          'moiety missing)"',
                                          'all(mol.GetAtomWithIdx(idx).GetIsAromatic() '
                                          'for idx in ring)',
                                          'False, "No six-membered aromatic '
                                          'ring containing an [O+ ] atom '
                                          'found"',
                                          'False, "No fused aromatic ring '
                                          'detected with the candidate '
                                          'flavylium ring"',
                                          'False, "No phenyl substituent '
                                          'attached to the flavylium core '
                                          'detected"',
                                          'True, "Molecule contains a '
                                          'flavylium-type '
                                          '(2-phenylchromenylium) core with a '
                                          'positively charged oxygen, fused '
                                          'aromatic rings, and an attached '
                                          'phenyl group"'],
                           'returns_count': 8,
                           'complexity': 6.910775378320108},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[NH+]1CCC(CC1)N1CCN(CC1)C(=O)[C@@H](CC1=CC2=C(NN=C2)C(C)=C1)NC(=O)N1CCC(CC1)C1=CC2=C(NC1=O)C=CC=C2',
                                     'name': 'zavegepant(1+)',
                                     'reason': 'No aromatic oxygen atom with '
                                               '+1 charge found (flavylium '
                                               'moiety missing)'},
                                 {   'smiles': 'CC1=CC=CC(=C1)C(=O)NNC(=O)C2=C(C3=CC=CC=C3N(C2=O)C)O',
                                     'name': "4-hydroxy-1-methyl-N'-[(3-methylphenyl)-oxomethyl]-2-oxo-3-quinolinecarbohydrazide",
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CCCN(C)C)O[C@@H]1CN(C)C(=O)NC3CCCCC3)[C@H](C)CO',
                                     'name': 'N-[(2S,3S)-2-[[[(cyclohexylamino)-oxomethyl]-methylamino]methyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-4-(dimethylamino)butanamide',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'O1C(OC2(C=3OC=4C(C(=O)C3)=C(OC)C(OC)=C(OC)C4)C=CC(=O)C=C2)C(O)C(O)C(O)C1C(O)=O',
                                     'name': '3,4,5-trihydroxy-6-{[4-oxo-1-(5,6,7-trimethoxy-4-oxo-4H-chromen-2-yl)cyclohexa-2,5-dien-1-yl]oxy}oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'O=C(N[C@@H]1C(OC2(C1)[C@H]3O[C@H]3C(O)(CC(=O)C)[C@@H]4[C@H]2O4)O)/C=C\\C(CC(CCCCCC)C)C',
                                     'name': 'Penicimutanolone',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCC',
                                     'name': 'TG(16:0/14:1(9Z)/18:0)',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'O1C(O)C(C(C1)CC2=CC=3OCOC3C=C2)CC4=CC(OC)=C(OC)C=C4',
                                     'name': "(8R,8'R,9S)-9-Hydroxy-3,4-dimethoxy-3',4'-methylenoxy-9,9'-epoxylignan",
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCCCCCC',
                                     'name': '1-palmitoyl-2-lauroyl-sn-glycero-3-phospho-1D-myo-inositol',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'O=C1C2=C([C@@H](O)CC1)[C@@H]([C@H](O)CCC)OC2',
                                     'name': 'Phomopsiketone F',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'},
                                 {   'smiles': 'C1CC(C1)CN(C[C@H]2[C@H]([C@H](N2)CO)C3=CC=CC=C3)C(=O)C4=CC=C(C=C4)F',
                                     'name': 'N-(cyclobutylmethyl)-4-fluoro-N-[[(2R,3R,4S)-4-(hydroxymethyl)-3-phenyl-2-azetidinyl]methyl]benzamide',
                                     'reason': 'Molecule does not carry a net '
                                               'positive charge'}],
    'sample_false_negatives': [   {   'smiles': '[Cl-].O1C(C(O)C(O)C(O)C1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC(O)=C(O)C=C4)CO',
                                      'name': 'cyanidin 3-glucoside',
                                      'reason': 'Molecule does not carry a net '
                                                'positive charge'},
                                  {   'smiles': 'O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC=C(O)C=C4)CO.[OH-]',
                                      'name': 'Fragarin',
                                      'reason': 'Molecule does not carry a net '
                                                'positive charge'},
                                  {   'smiles': '[Cl-].O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C=C3C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)=CC(O)=CC3=[O+]C2C5=CC(O)=C(O)C=C5)CO[C@@H]6O[C@H]([C@H](O)[C@@H](O)[C@H]6O)C',
                                      'name': 'Cyanidin '
                                              '3-rutinoside-5-glucoside',
                                      'reason': 'Molecule does not carry a net '
                                                'positive charge'},
                                  {   'smiles': 'C1(=C(O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)C=C3C(=[O+]1)C=C(O)C=C3[O-])C4=CC(=C(O)C(=C4)OC)O',
                                      'name': 'petunidin 3-O-beta-D-glucoside '
                                              'betaine',
                                      'reason': 'Molecule does not carry a net '
                                                'positive charge'},
                                  {   'smiles': '[Cl-].O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC=C(O)C=C4)CO',
                                      'name': 'Pelargonidin 3-galactoside',
                                      'reason': 'Molecule does not carry a net '
                                                'positive charge'}],
    'attempt': 0,
    'reasoning': 'Below is one possible solution. In this example the function '
                 'first makes sure that the SMILES can be parsed and that the '
                 'molecule is a cation. It then looks for an aromatic oxygen '
                 'atom carrying a +1 formal charge (as seen in many '
                 'anthocyanidin (flavylium‐type) cores) that is part of a '
                 'six‐membered ring. Finally, it uses a few heuristic checks – '
                 'namely, that the candidate ring is fused to at least one '
                 'other aromatic ring (as expected for a benzopyrylium core) '
                 'and that there is an aromatic (phenyl) substituent attached. '
                 '(Because these molecules are highly decorated, and the '
                 '“anthocyanidin cation” definition is subtle, the algorithm '
                 'uses heuristics and may not capture every nuance.) If any '
                 'step is missing the function returns False with an '
                 'explanation; otherwise it returns True with a reason. \n'
                 '\n'
                 'Note that if one thinks the problem is too hard to do '
                 'exactly, the function may instead return (None, None).\n'
                 '\n'
                 'Below is the complete Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 126,
    'num_false_positives': 89,
    'num_true_negatives': 142080,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.586046511627907,
    'recall': 0.9618320610687023,
    'f1': 0.7283236994219653,
    'accuracy': 0.9993394237526353,
    'negative_predictive_value': 0.9999648097969526}