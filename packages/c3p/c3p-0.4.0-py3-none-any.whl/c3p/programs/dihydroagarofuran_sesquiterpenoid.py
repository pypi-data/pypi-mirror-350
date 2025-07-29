"""
Classifies: CHEBI:71548 dihydroagarofuran sesquiterpenoid
"""
#!/usr/bin/env python
"""
Classifies: dihydroagarofuran sesquiterpenoid
Definition: Any sesquiterpenoid with a dihydroagarofuran skeleton.

Heuristic:
  1. Look for at least one tetrahydrofuran ring (5-membered ring with 1 oxygen and 4 carbons).
  2. Check if that ring is fused with at least two other rings (i.e. shares at least 2 atoms with each additional ring).
  3. In the fused ring system, roughly 10–20 carbons should be present (the true dihydroagarofuran core has 15 carbons).
If these conditions are met then we classify the molecule as a dihydroagarofuran sesquiterpenoid.
"""
from rdkit import Chem

def is_dihydroagarofuran_sesquiterpenoid(smiles: str):
    """
    Determines if a molecule is a dihydroagarofuran sesquiterpenoid based on its SMILES string.
    
    This function uses a heuristic:
      - It searches for a tetrahydrofuran ring (a 5-membered ring with one oxygen and four carbons).
      - It then checks that this ring is fused (sharing at least two atoms) with at least two other rings.
      - It also checks that the union of atoms in the fused ring system has a carbon count roughly 
        consistent with a sesquiterpenoid core (about 15 carbons, here allowed in the 10 to 20 range).
        
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a dihydroagarofuran sesquiterpenoid, False otherwise.
        str: Explanation for the classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get all rings in the molecule as tuples of atom indices.
    ring_info = mol.GetRingInfo()
    if not ring_info or not ring_info.AtomRings():
        return False, "No rings detected in the molecule"
    rings = ring_info.AtomRings()
    
    # Look for candidate tetrahydrofuran rings:
    candidate_thf_rings = []
    for ring in rings:
        if len(ring) == 5:
            oxygen_count = 0
            carbon_count = 0
            for idx in ring:
                symbol = mol.GetAtomWithIdx(idx).GetSymbol()
                if symbol == 'O':
                    oxygen_count += 1
                elif symbol == 'C':
                    carbon_count += 1
            # A tetrahydrofuran ring typically has 1 O and 4 C.
            if oxygen_count == 1 and carbon_count == 4:
                candidate_thf_rings.append(set(ring))
    
    if not candidate_thf_rings:
        return False, "No tetrahydrofuran (5-membered, 1O/4C) ring found"
    
    # Now, for each candidate THF ring, check for fusion with other rings:
    for thf_ring in candidate_thf_rings:
        fused_rings = [thf_ring]  # start with the THF ring
        # Look for rings that share at least 2 atoms with our candidate THF ring.
        for other_ring in rings:
            other_ring_set = set(other_ring)
            if other_ring_set == thf_ring:
                continue
            if len(thf_ring.intersection(other_ring_set)) >= 2:
                fused_rings.append(other_ring_set)
        if len(fused_rings) < 3:
            # Not enough fused rings to match the dihydroagarofuran skeleton.
            continue
        
        # Compute union of atoms in the fused ring system.
        union_atoms = set()
        for ring_set in fused_rings:
            union_atoms = union_atoms.union(ring_set)
        # Count carbons in the fused system.
        core_carbons = 0
        for idx in union_atoms:
            if mol.GetAtomWithIdx(idx).GetSymbol() == 'C':
                core_carbons += 1
        # Many dihydroagarofuran cores are sesquiterpenoids (roughly 15 carbons).
        # Allow some variation with substituents removed (here we require between 10 and 20 C).
        if 10 <= core_carbons <= 20:
            return True, ("Fused ring system detected with a tetrahydrofuran ring and ~{} core carbons (expected "
                          "for a sesquiterpenoid).".format(core_carbons))
    
    return False, "No fused ring system consistent with a dihydroagarofuran skeleton was found"

# If run as a script, some test cases can be executed.
if __name__ == "__main__":
    # Example: one of the provided SMILES for wilforidine.
    test_smiles = "[C@@]12([C@@H]([C@@H]([C@@]3([C@H]([C@]14[C@]([C@H]([C@@H]([C@@H]2OC(=O)C)O)OC(C(CCC5=NC=CC=C5C(OC[C@@]3(O4)C)=O)(C)O)=O)(O)C)OC(C)=O)[H])OC(C)=O)OC(=O)C)COC(C)=O"
    result, reason = is_dihydroagarofuran_sesquiterpenoid(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:71548',
                          'name': 'dihydroagarofuran sesquiterpenoid',
                          'definition': 'Any sesquiterpenoid with a '
                                        'dihydroagarofuran skeleton.',
                          'parents': ['CHEBI:26658'],
                          'xrefs': ['PMID:17898902'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 71,
                           'log_lines_of_code': 4.2626798770413155,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
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
                                                 4,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSymbol',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'format',
                                                 'union',
                                                 'intersection',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'append'],
                           'methods_called_count': 9,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_dihydroagarofuran_sesquiterpenoid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings detected in the '
                                          'molecule"',
                                          'False, "No tetrahydrofuran '
                                          '(5-membered, 1O/4C) ring found"',
                                          'True, ("Fused ring system detected '
                                          'with a tetrahydrofuran ring and ~{} '
                                          'core carbons (expected "',
                                          'False, "No fused ring system '
                                          'consistent with a dihydroagarofuran '
                                          'skeleton was found"'],
                           'returns_count': 5,
                           'complexity': 4.852535975408263},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No rings detected in the '
                                               'molecule'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No rings detected in the '
                                               'molecule'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No tetrahydrofuran '
                                               '(5-membered, 1O/4C) ring '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(C)[C@@H](OC(C)=O)[C@H](C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccccc1)OC(=O)c1ccccc1',
                                      'name': 'orbiculin G',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(C)[C@@H](OC(C)=O)[C@H](C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccoc1)OC(C)=O',
                                      'name': 'orbiculin E',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(COC(C)=O)[C@@H](OC(C)=O)[C@H](C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccccc1)OC(=O)c1ccccc1',
                                      'name': '15-acetoxyorbiculin G',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(COC(=O)c4ccccc4)[C@@H](O)[C@H](C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccccc1)OC(C)=O',
                                      'name': '2alpha-acetoxy-1alpha-hydroxy-6beta,9beta,15-tribenzoyloxy-beta-dihydroagarofuran',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12[C@@H](OC(C)=O)[C@H](OC(=O)c3ccoc3)[C@]3(C)[C@H](CC[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccoc1)OC(C)=O',
                                      'name': 'orbiculin H',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(COC(=O)c4ccccc4)[C@@H](OC(C)=O)[C@@H](O)C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccccc1',
                                      'name': '1alpha-acetoxy-2alpha-hydroxy-6beta,9beta,15-tribenzoyloxy-beta-dihydroagarofuran',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12[C@H](OC(=O)c3ccccc3)[C@H](OC(=O)c3ccoc3)[C@]3(COC(C)=O)[C@H](CC[C@](C)(O)[C@@]3(OC1(C)C)[C@@H]2OC(=O)C(C)CC)OC(=O)C(C)CC',
                                      'name': '1S,6R-di(2-)methylbutanoyloxy-4S-hydroxy-8S-benzoyloxy-9R-(3-)furancarbonyloxy-13-acetyloxy-beta-dihydroagarofuran',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[C@]123[C@]([C@H]([C@H]([C@]([C@H]1OC(C)=O)(C(O2)(C)C)[H])OC(C=4C=CC=CC4)=O)OC(C5=CC=CC=C5)=O)([C@H]([C@H](C[C@]3(O)C)O)OC(=O)C)C',
                                      'name': 'triptofordin C 2',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(C)[C@@H](OC(C)=O)[C@H](C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccoc1)OC(=O)c1ccoc1',
                                      'name': 'orbiculin F',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'},
                                  {   'smiles': '[H][C@]12C[C@H](OC(=O)c3ccccc3)[C@]3(C)[C@@H](OC(C)=O)[C@H](C[C@@H](C)[C@@]3(OC1(C)C)[C@@H]2OC(=O)c1ccccc1)OC(C)=O',
                                      'name': 'orbiculin A',
                                      'reason': 'No fused ring system '
                                                'consistent with a '
                                                'dihydroagarofuran skeleton '
                                                'was found'}],
    'attempt': 0,
    'reasoning': 'Below is one possible solution. Note that the '
                 'dihydroagarofuran skeleton is a complex, polycyclic '
                 'structure. In this example we use a heuristic approach: we '
                 'first look for a tetrahydrofuran ring (a five‐membered ring '
                 'made up of four carbons and one oxygen) and then check '
                 'whether that ring is fused (shares at least two atoms) with '
                 'at least two other rings and that the union of atoms in the '
                 'fused system has roughly the right number of carbons (around '
                 '10–20) to be considered a sesquiterpenoid core (about 15 '
                 'carbons). This method will classify many dihydroagarofuran '
                 'sesquiterpenoids correctly, although it is necessarily '
                 'approximate given the complexity of these molecules. (If a '
                 'more robust classification is needed, one would likely '
                 'require a dedicated curated SMARTS pattern or more '
                 'elaborated logic.) \n'
                 '\n'
                 'Below is the full Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 3250,
    'num_true_negatives': 139024,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.004594180704441042,
    'recall': 0.5769230769230769,
    'f1': 0.00911577028258888,
    'accuracy': 0.9770836261419537,
    'negative_predictive_value': 0.9999208832308412}