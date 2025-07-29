"""
Classifies: CHEBI:4194 D-hexose
"""
"""
Classifies: D-hexose
A D-hexose (for our purposes) is a hexose (exactly 6 carbons and 6 oxygens) that contains a sugar ring
(either a 5-membered or 6-membered ring with exactly one oxygen) and one ring-carbon that carries an
exocyclic –CH2OH substituent. The exocyclic CH2OH-bearing ring-carbon (the “C5” center) must have CIP
configuration 'R'.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_D_hexose(smiles: str):
    """
    Determines whether a molecule is a D-hexose.
    A D-hexose is defined here as a molecule that:
      - Has exactly 6 carbon atoms and 6 oxygen atoms.
      - Contains a sugar ring (a 5- or 6-membered ring containing exactly 1 oxygen atom).
      - Has exactly one exocyclic CH2OH group attached to a ring carbon. This ring carbon (the C5 center)
        must have the CIP configuration 'R'.
        
    Args:
        smiles (str): SMILES string for the molecule.
        
    Returns:
        (bool, str): Tuple with classification result and a message explaining the decision.
    """
    
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Assign stereochemistry so that CIP codes get computed.
    Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # Check for exactly 6 carbons and 6 oxygens.
    atoms = list(mol.GetAtoms())
    carbons = [atom for atom in atoms if atom.GetAtomicNum() == 6]
    oxygens = [atom for atom in atoms if atom.GetAtomicNum() == 8]
    if len(carbons) != 6:
        return False, "Molecule does not have exactly 6 carbon atoms (not a hexose)"
    if len(oxygens) != 6:
        return False, "Molecule does not have exactly 6 oxygen atoms (likely a modified hexose)"
    
    # Look for an exocyclic CH2OH group.
    # In a proper CH2OH group the carbon should be:
    #  - sp3 carbon (implicit in rdkit) with exactly 2 hydrogens,
    #  - bonded to exactly two heavy atoms (one oxygen and one ring carbon).
    exo_candidates = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue
        # We require that this carbon is NOT in a ring.
        if atom.IsInRing():
            continue
        # Check the number of attached hydrogens.
        if atom.GetTotalNumHs() != 2:
            continue
        # Count heavy neighbors (atoms with atomic number > 1)
        heavy_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() > 1]
        if len(heavy_neighbors) != 2:
            continue
        # We expect one neighbor to be oxygen (for the –OH) and the other to be a carbon.
        nbr_atomic_nums = sorted([nbr.GetAtomicNum() for nbr in heavy_neighbors])
        if nbr_atomic_nums != [6, 8]:
            continue
        # Identify the neighbor that is a carbon.
        ring_carbon = None
        for nbr in heavy_neighbors:
            if nbr.GetAtomicNum() == 6:
                # For a proper exocyclic attachment, the carbon neighbor should be in a ring.
                if nbr.IsInRing():
                    ring_carbon = nbr
        if ring_carbon is None:
            continue
        # This atom qualifies as a CH2OH substituent attached to a ring carbon.
        exo_candidates.append((atom, ring_carbon))
    
    if len(exo_candidates) == 0:
        return False, "No appropriate exocyclic CH2OH substituent found"
    if len(exo_candidates) > 1:
        return False, "Multiple exocyclic CH2OH substituents found (ambiguous candidate for C5)"
    
    # We have exactly one exocyclic CH2OH candidate.
    exo_atom, candidate_C5 = exo_candidates[0]
    
    # Check that candidate_C5 is in a sugar ring.
    # A typical sugar ring is either 5-membered (furanose) or 6-membered (pyranose)
    # and must contain exactly one oxygen.
    ring_info = mol.GetRingInfo()
    sugar_ring = None
    for ring in ring_info.AtomRings():
        if len(ring) not in (5, 6):
            continue
        if candidate_C5.GetIdx() not in ring:
            continue
        # Count oxygen atoms in the ring.
        oxygen_count = 0
        for idx in ring:
            if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8:
                oxygen_count += 1
        if oxygen_count != 1:
            continue
        # Accept the first ring that meets the criteria.
        sugar_ring = ring
        break
    
    if sugar_ring is None:
        return False, "Candidate C5 is not part of an appropriate sugar ring (5- or 6-membered with one oxygen)"
    
    # Now check the stereochemistry of the candidate C5 atom.
    # The CIP code should be available (R expected for D-hexose).
    if not candidate_C5.HasProp('_CIPCode'):
        return False, "Stereochemistry was not assigned for the candidate C5 atom"
    cip = candidate_C5.GetProp('_CIPCode')
    if cip != 'R':
        return False, f"C5 has CIP configuration {cip} (expected R for D-hexose)"
    
    return True, "Molecule is a D-hexose: 6 carbons with a sugar ring and the C5 center in R configuration"


# Example usage:
if __name__ == "__main__":
    # Test with a couple of SMILES strings for D-hexoses.
    test_smiles_list = [
        "OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@H]1O",  # alpha-D-galactose
        "O1[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO"   # beta-D-idopyranose
    ]
    for smi in test_smiles_list:
        res, reason = is_D_hexose(smi)
        print(f"SMILES: {smi}\nResult: {res}\nReason: {reason}\n{'-'*40}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:4194',
                          'name': 'D-hexose',
                          'definition': 'A hexose that has D-configuration at '
                                        'position 5.',
                          'parents': ['CHEBI:18133'],
                          'xrefs': ['KEGG:C00738'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 103,
                           'log_lines_of_code': 4.634728988229636,
                           'indent_by_line': [   1,
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
                                                 2,
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
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
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
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetProp',
                                                 'GetIdx',
                                                 'HasProp',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'IsInRing',
                                                 'GetRingInfo',
                                                 'AssignStereochemistry',
                                                 'GetTotalNumHs'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_D_hexose(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule does not have '
                                          'exactly 6 carbon atoms (not a '
                                          'hexose)"',
                                          'False, "Molecule does not have '
                                          'exactly 6 oxygen atoms (likely a '
                                          'modified hexose)"',
                                          'False, "No appropriate exocyclic '
                                          'CH2OH substituent found"',
                                          'False, "Multiple exocyclic CH2OH '
                                          'substituents found (ambiguous '
                                          'candidate for C5)"',
                                          'False, "Candidate C5 is not part of '
                                          'an appropriate sugar ring (5- or '
                                          '6-membered with one oxygen)"',
                                          'False, "Stereochemistry was not '
                                          'assigned for the candidate C5 atom"',
                                          'False, f"C5 has CIP configuration '
                                          '{cip} (expected R for D-hexose)"',
                                          'True, "Molecule is a D-hexose: 6 '
                                          'carbons with a sugar ring and the '
                                          'C5 center in R configuration"'],
                           'returns_count': 9,
                           'complexity': 6.726945797645928},
    'message': '\n'
               'Attempt failed: F1 score of 0.5 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O1[C@@H]([C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O)CO NAME: '
               'beta-D-altropyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@H](O)[C@H]1O)CO NAME: '
               'alpha-D-talopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@H](O)[C@@H]1O)CO NAME: '
               'beta-D-idopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-galactose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[13C@@H](O)[13C@H]1O)CO '
               'NAME: alpha-D-glucose-1,2-((13)C2) REASON: CORRECT Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: C1([C@H]([C@@H]([C@H]([C@H](O1)CO)O)O)O)O NAME: '
               'D-idopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'beta-D-talopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'beta-D-glucose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'D-talopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@H](O)[C@H]1O)CO NAME: '
               'alpha-D-idopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-D-gulose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'D-gulopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-mannose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'D-allopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-D-allose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'beta-D-mannose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'alpha-D-gulose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-glucose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'beta-D-allose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'D-mannopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'D-glucopyranose REASON: CORRECT Molecule is a D-hexose: 6 '
               'carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               'False positives: SMILES: '
               'OC[C@@]1(O)OC[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'beta-D-fructopyranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@](O)(CO)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-fructofuranose REASON: WRONGLY CLASSIFIED Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(=O)[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'D-galactono-1,5-lactone REASON: WRONGLY CLASSIFIED Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(=O)C(O)C(O)C1O NAME: Hexose-1,5-lactone '
               'REASON: WRONGLY CLASSIFIED Molecule is a D-hexose: 6 carbons '
               'with a sugar ring and the C5 center in R configuration\n'
               ' * SMILES: OC[C@H]1OC(O)(CO)[C@H](O)[C@H]1O NAME: '
               'D-sorbofuranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(=O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'D-glucono-1,5-lactone REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)(CO)[C@@H](O)[C@H]1O NAME: '
               'D-tagatofuranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)C(=O)[C@@H]1O NAME: '
               '3-dehydro-D-glucose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)C(=O)[C@@H](O)[C@@H]1O NAME: '
               '2-dehydro-D-glucopyranose REASON: WRONGLY CLASSIFIED Molecule '
               'is a D-hexose: 6 carbons with a sugar ring and the C5 center '
               'in R configuration\n'
               ' * SMILES: OC[C@H]1O[C@@](O)(CO)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-tagatofuranose REASON: WRONGLY CLASSIFIED Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)C(=O)C1=O NAME: '
               '3,4-didehydro-D-glucose REASON: WRONGLY CLASSIFIED Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)C(=O)[C@H]1O NAME: '
               '3-keto-beta-D-galactose REASON: WRONGLY CLASSIFIED Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@](O)(CO)[C@@H](O)[C@H]1O NAME: '
               'beta-D-tagatofuranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@]1(O)[C@H](O)OC[C@@H](O)[C@H]1O NAME: '
               'beta-D-hamamelose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1O[C@](O)(CO)[C@H](O)[C@H]1O NAME: '
               'beta-D-sorbofuranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)(CO)[C@@H](O)[C@@H]1O NAME: '
               'D-fructofuranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@@]1(O)OC[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'beta-D-tagatopyranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@@]1(O)OC[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-L-sorbopyranose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: O1[C@@]2(O)[C@@H](O)[C@H](O)[C@](C1)(O)OC2 NAME: '
               '5-Keto-D-fructose REASON: WRONGLY CLASSIFIED Molecule is a '
               'D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               ' * SMILES: OC[C@H]1OC(O)C(=O)C(=O)[C@@H]1O NAME: '
               '2,3-didehydro-D-glucose REASON: WRONGLY CLASSIFIED Molecule is '
               'a D-hexose: 6 carbons with a sugar ring and the C5 center in R '
               'configuration\n'
               'False negatives: SMILES: '
               'O1[C@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-idofuranose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: [H][C@]1(O[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CO NAME: '
               'beta-D-galactofuranose REASON: MISSED No appropriate sugar '
               'ring with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: [C@H]1(O)C(O)O[C@H](C=O)[C@H]([C@@H]1O)O NAME: '
               '6-dehydro-D-glucose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-galactose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@H](O)CO NAME: '
               'alpha-D-gulofuranose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@H](O)CO NAME: '
               'D-altrofuranose REASON: MISSED No appropriate sugar ring with '
               'exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-altrofuranose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: '
               'OC[C@H]1OC(O)[C@H](OP(O)(=O)O[C@H]2[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O '
               'NAME: agrocinopine D REASON: MISSED Molecule does not have '
               'exactly 6 carbon atoms (not a hexose)\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-gulofuranose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-glucose REASON: MISSED No appropriate sugar ring '
               'with exocyclic CH2OH substituent (C5 candidate) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a hexose)'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Molecule does not have exactly '
                                               '6 carbon atoms (not a '
                                               'hexose)'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO',
                                      'name': 'beta-D-idofuranose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': '[H][C@]1(O[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CO',
                                      'name': 'beta-D-galactofuranose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': '[C@H]1(O)C(O)O[C@H](C=O)[C@H]([C@@H]1O)O',
                                      'name': '6-dehydro-D-glucose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': '[H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)CO',
                                      'name': 'aldehydo-D-galactose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': 'O1[C@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@H](O)CO',
                                      'name': 'alpha-D-gulofuranose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@H](O)CO',
                                      'name': 'D-altrofuranose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO',
                                      'name': 'beta-D-altrofuranose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': 'OC[C@H]1OC(O)[C@H](OP(O)(=O)O[C@H]2[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O',
                                      'name': 'agrocinopine D',
                                      'reason': 'Molecule does not have '
                                                'exactly 6 carbon atoms (not a '
                                                'hexose)'},
                                  {   'smiles': 'O1[C@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)CO',
                                      'name': 'beta-D-gulofuranose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'},
                                  {   'smiles': '[H]C(=O)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO',
                                      'name': 'aldehydo-D-glucose',
                                      'reason': 'No appropriate exocyclic '
                                                'CH2OH substituent found'}],
    'attempt': 3,
    'reasoning': 'We can improve the previous approach by “inverting” the '
                 'search: rather than scanning the ring for a suitable '
                 'substituent, we first look for an exocyclic –CH2OH group '
                 '(i.e. a carbon with exactly two hydrogens and two heavy‐atom '
                 'neighbors, one of which must be an –OH) and then '
                 '“back‐trace” to the ring carbon to verify that it is part of '
                 'a simple sugar ring (a 5‐ or 6‐membered ring containing '
                 'exactly one oxygen) and that that ring carbon (assigned as '
                 '“C5”) has CIP configuration R. (We also check that the '
                 'molecule has exactly 6 carbons and 6 oxygens.) This “from '
                 'the substituent” method helps us catch cases (especially for '
                 'furanoses) where the exocyclic –CH2OH may not be directly '
                 'identified by iterating over ring atoms. \n'
                 '\n'
                 'Below is the complete Python code (using rdkit) that '
                 'implements these ideas. (Note that even with these '
                 'improvements, fully “correct” classification of sugars by '
                 'SMILES remains challenging so we return (False, …) if '
                 'something isn’t exactly as expected.)\n'
                 '\n'
                 'Below is the code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 21,
    'num_false_positives': 12,
    'num_true_negatives': 142245,
    'num_false_negatives': 22,
    'num_negatives': None,
    'precision': 0.6363636363636364,
    'recall': 0.4883720930232558,
    'f1': 0.5526315789473685,
    'accuracy': 0.9997610681658468,
    'negative_predictive_value': 0.9998453611870638}