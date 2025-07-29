"""
Classifies: CHEBI:50126 tetrasaccharide
"""
"""
Classifies: Tetrasaccharide
Definition: An oligosaccharide comprising four monomeric monosaccharide units.
This revised classifier:
  - Parses the SMILES and requires one connected component.
  - Detects candidate sugar rings as rings of size 5 (furanose) or 6 (pyranose) containing exactly one oxygen.
  - Requires that each candidate sugar ring has at least one exocyclic oxygen substituent carrying a hydrogen (e.g. –OH)
    and at least one chiral atom.
  - In addition, when checking connectivity, the candidate ring’s set is “grown” by including neighboring oxygen atoms
    that commonly act as glycosidic linkers.
If there are exactly 4 candidate rings and they are connected via such linkers, the molecule qualifies as a tetrasaccharide.
"""
from rdkit import Chem

def is_tetrasaccharide(smiles: str):
    """
    Determine if a molecule (given as a SMILES string) is a tetrasaccharide.
    The procedure:
      - Ensures the SMILES is valid and corresponds to a single (connected) molecule.
      - From the ring information, it gathers candidate sugar rings defined as:
          * A ring of 5 or 6 atoms,
          * Containing exactly one oxygen atom (and the remaining being carbons),
          * Having at least one exocyclic –OH substituent (an oxygen neighbor having at least one hydrogen),
          * And having at least one explicitly chiral center.
      - It then “grows” each candidate unit’s atom set by including neighbouring oxygen atoms (the typical glycosidic linker atoms).
      - Finally, it requires exactly 4 candidate sugar rings whose grown sets are mutually connected (i.e. intersect at least one other).
      
    Args:
      smiles (str): SMILES string of the molecule.
      
    Returns:
      (bool, str): (True, reason) if the molecule qualifies as a tetrasaccharide;
                   (False, reason) otherwise.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for a single connected component
    mol_smiles = Chem.MolToSmiles(mol)
    if '.' in mol_smiles:
        return False, "Molecule contains multiple disconnected fragments"
    
    ring_info = mol.GetRingInfo().AtomRings()
    
    def is_candidate_sugar_ring(atom_indices):
        """
        Evaluate whether a given ring (identified by its atom indices) meets the criteria for a
        candidate sugar ring.
          - Ring must be of size 5 (furanose) or 6 (pyranose).
          - The ring must have exactly one oxygen (rest assumed to be carbons).
          - At least one exocyclic -OH substituent: one neighbor (not in the ring) that is an oxygen
            with at least one hydrogen.
          - At least one chiral center should be specified in the ring.
        """
        n = len(atom_indices)
        if n not in (5, 6):
            return False
        oxy_count = 0
        carbon_count = 0
        for idx in atom_indices:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() == 8:
                oxy_count += 1
            elif atom.GetAtomicNum() == 6:
                carbon_count += 1
        # Check typical sugar ring composition: one oxygen and the rest carbons.
        if oxy_count != 1 or (n - oxy_count) != carbon_count:
            return False
        
        # Check for exocyclic hydroxyl group(s)
        exo_oh = 0
        for idx in atom_indices:
            a = mol.GetAtomWithIdx(idx)
            for nbr in a.GetNeighbors():
                if nbr.GetIdx() in atom_indices:
                    continue
                # We expect an -OH substituent: neighbor oxygen with at least one hydrogen
                if nbr.GetAtomicNum() == 8 and nbr.GetTotalNumHs() > 0:
                    exo_oh += 1
        if exo_oh < 1:
            return False
        
        # Relaxed chiral requirement: at least one chiral center in the ring.
        chiral = 0
        for idx in atom_indices:
            a = mol.GetAtomWithIdx(idx)
            if a.GetChiralTag() != Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
                chiral += 1
        if chiral < 1:
            return False
        
        return True

    # Gather candidate sugar rings (as sets of atom indices)
    candidate_rings = []
    for ring in ring_info:
        if is_candidate_sugar_ring(ring):
            candidate_rings.append(set(ring))
            
    if len(candidate_rings) != 4:
        return False, f"Found {len(candidate_rings)} candidate carbohydrate rings, need exactly 4"

    # Build a connectivity graph among candidate rings.
    # Instead of checking only for direct bonds between atoms in rings, we "grow" the candidate set by including
    # neighboring oxygen atoms (which may serve as glycosidic linkers).
    grown_sets = []
    for ring_atoms in candidate_rings:
        grown = set(ring_atoms)  # start with atoms in the ring
        for idx in ring_atoms:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                # If neighbor is oxygen, add it to the grown set.
                if nbr.GetAtomicNum() == 8:
                    grown.add(nbr.GetIdx())
        grown_sets.append(grown)
    
    n = len(grown_sets)
    connectivity_graph = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            # If the grown sets of candidate rings share any atom, treat them as connected.
            if grown_sets[i].intersection(grown_sets[j]):
                connectivity_graph[i].add(j)
                connectivity_graph[j].add(i)
    
    # Do a DFS to check if all four candidate rings are connected.
    visited = set()
    def dfs(node):
        stack = [node]
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            stack.extend(list(connectivity_graph[cur] - visited))
    
    dfs(0)
    if len(visited) != n:
        return False, "Candidate carbohydrate rings are not connected via glycosidic bonds"
    
    return True, "Molecule contains exactly 4 connected monosaccharide (sugar) units"

# For testing purposes (script usage)
if __name__ == '__main__':
    # A known tetrasaccharide example as provided.
    test_smiles = "OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H]3O[C@@H](OC[C@H]4OC(O)[C@H](O)[C@@H](O)[C@H]4O)[C@H](O)[C@@H](O)[C@H]3O)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O"
    result, reason = is_tetrasaccharide(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50126',
                          'name': 'tetrasaccharide',
                          'definition': 'An oligosaccharide comprising four '
                                        'monomeric monosaccharide units.',
                          'parents': ['CHEBI:50699'],
                          'xrefs': ['KEGG:C06768'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 116,
                           'log_lines_of_code': 4.7535901911063645,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
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
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'extend',
                                                 'GetNeighbors',
                                                 'MolToSmiles',
                                                 'GetTotalNumHs',
                                                 'GetChiralTag',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'add',
                                                 'GetIdx',
                                                 'pop',
                                                 'intersection',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append'],
                           'methods_called_count': 15,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_tetrasaccharide(smiles: str):',
                                       'is_candidate_sugar_ring(atom_indices):',
                                       'dfs(node):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains multiple '
                                          'disconnected fragments"',
                                          'False',
                                          'False',
                                          'False',
                                          'False',
                                          'True',
                                          'False, f"Found '
                                          '{len(candidate_rings)} candidate '
                                          'carbohydrate rings, need exactly 4"',
                                          'False, "Candidate carbohydrate '
                                          'rings are not connected via '
                                          'glycosidic bonds"',
                                          'True, "Molecule contains exactly 4 '
                                          'connected monosaccharide (sugar) '
                                          'units"'],
                           'returns_count': 10,
                           'complexity': 7.550718038221272},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'COC(=O)[C@@]1(O)OC[C@@]23[C@H]4[C@@H](OC[C@@]4([C@@H](C[C@@H]2OC(=O)C(\\C)=C\\C)OC(C)=O)C(=O)OC)[C@H]2O[C@]4(C)[C@H]5C[C@H](O[C@@H]6OC=C[C@]56O)[C@]4(O)[C@@]2(C)[C@H]13 '
               'NAME: 3-Acetyl-1-tigloylazadirachtinin REASON: WRONGLY '
               'CLASSIFIED Molecule contains exactly 4 connected '
               'monosaccharide (sugar) units\n'
               'False negatives: SMILES: '
               'OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H]3O[C@@H](OC[C@H]4OC(O)[C@H](O)[C@@H](O)[C@H]4O)[C@H](O)[C@@H](O)[C@H]3O)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: '
               'beta-D-Galp-(1->6)-beta-D-Galp-(1->6)-beta-D-Galp-(1->6)-D-Galp '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               ' * SMILES: OCC(O)C(O)CC(O)=O NAME: 2-Deoxypentonic acid '
               'REASON: MISSED Found 0 candidate carbohydrate rings, need '
               'exactly 4\n'
               ' * SMILES: '
               'OC[C@H]([C@@H](O)[C@]1([C@H](NC(C)=O)[C@@H](O)C[C@](O1)(O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@@]([C@@]([C@@H](O)C=O)(O[C@H]3[C@H]([C@H](O)[C@@H]([C@@H](O3)C)O)O)[H])([C@@H](CO)O)[H])C(O)=O)[H])O '
               "NAME: 3'-Sialyl-3-fucosyllactose REASON: MISSED Found 3 "
               'candidate carbohydrate rings, need exactly 4\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@H](O)[C@@H]1OC(=O)C(O)CO)CO NAME: '
               'beta-mannosylglycerate REASON: MISSED Found 1 candidate '
               'carbohydrate rings, need exactly 4\n'
               ' * SMILES: '
               'OC[C@H](O)[C@H]1O[C@H](OC[C@H](O)[C@H]2O[C@H](O[C@@H]3[C@H](O)[C@@H](O[C@@H]4[C@H](O)C[C@@](O)(O[C@@H]4[C@H](O)CO)C(O)=O)O[C@H]([C@@H](O)CO)[C@H]3O)[C@@H](O)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O '
               'NAME: '
               'L-alpha-D-Hepp-(1->7)-L-alpha-D-Hepp-(1->3)-L-alpha-D-Hepp-(1->5)-alpha-Kdo '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O)[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O)[C@@H]2O)[C@@H](O)[C@@H]1O '
               'NAME: '
               'alpha-D-Manp-(1->3)-alpha-D-Manp-(1->2)-alpha-D-Manp-(1->2)-alpha-D-Manp '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O[C@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]2O[C@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]2O[C@@H]2[C@H](O)[C@@H](O)O[C@H](CO)[C@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O '
               'NAME: '
               'alpha-D-Manp-(1->2)-alpha-D-Manp-(1->2)-alpha-D-Manp-(1->3)-alpha-D-Manp '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               ' * SMILES: '
               'C1([C@H]([C@H]([C@@H]([C@H](O1)CO[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)O)O[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O)O)O '
               'NAME: '
               'alpha-D-Manp-(1->2)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)-D-Manp '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@H](O[C@H]2[C@@H](O)[C@H](O)[C@]([H])(O[C@@H]2O[C@@H]2[C@H](O)[C@@H](O[C@@H]3[C@H](O)C[C@@](O)(O[C@]3([H])[C@H](O)CO)C(O)=O)O[C@]([H])([C@@H](O)CO)[C@H]2O)[C@@H](O)CO)[C@@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO '
               'NAME: '
               'L-glycero-alpha-D-manno-Hepp-(1->2)-L-glycero-alpha-D-manno-Hepp-(1->3)-L-glycero-alpha-D-manno-Hepp-(1->5)-alpha-Kdo '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)O[C@H](CO)[C@H]2O)[C@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2OC(=C[C@H](O)[C@H]2O)C(O)=O)[C@H](O)[C@H]1O '
               'NAME: '
               'beta-D-Delta(4)-GlcpA-(1->4)-beta-D-Glcp-(1->4)-alpha-L-Rhap-(1->3)-beta-D-Glcp '
               'REASON: MISSED Candidate carbohydrate rings are not connected '
               'via glycosidic bonds\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Found 2 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Found 1 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Found 0 candidate carbohydrate '
                                               'rings, need exactly 4'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H]3O[C@@H](OC[C@H]4OC(O)[C@H](O)[C@@H](O)[C@H]4O)[C@H](O)[C@@H](O)[C@H]3O)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'beta-D-Galp-(1->6)-beta-D-Galp-(1->6)-beta-D-Galp-(1->6)-D-Galp',
                                      'reason': 'Candidate carbohydrate rings '
                                                'are not connected via '
                                                'glycosidic bonds'},
                                  {   'smiles': 'OCC(O)C(O)CC(O)=O',
                                      'name': '2-Deoxypentonic acid',
                                      'reason': 'Found 0 candidate '
                                                'carbohydrate rings, need '
                                                'exactly 4'},
                                  {   'smiles': 'OC[C@H]([C@@H](O)[C@]1([C@H](NC(C)=O)[C@@H](O)C[C@](O1)(O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@@]([C@@]([C@@H](O)C=O)(O[C@H]3[C@H]([C@H](O)[C@@H]([C@@H](O3)C)O)O)[H])([C@@H](CO)O)[H])C(O)=O)[H])O',
                                      'name': "3'-Sialyl-3-fucosyllactose",
                                      'reason': 'Found 3 candidate '
                                                'carbohydrate rings, need '
                                                'exactly 4'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)[C@H](O)[C@@H]1OC(=O)C(O)CO)CO',
                                      'name': 'beta-mannosylglycerate',
                                      'reason': 'Found 1 candidate '
                                                'carbohydrate rings, need '
                                                'exactly 4'},
                                  {   'smiles': 'OC[C@H](O)[C@H]1O[C@H](OC[C@H](O)[C@H]2O[C@H](O[C@@H]3[C@H](O)[C@@H](O[C@@H]4[C@H](O)C[C@@](O)(O[C@@H]4[C@H](O)CO)C(O)=O)O[C@H]([C@@H](O)CO)[C@H]3O)[C@@H](O)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'L-alpha-D-Hepp-(1->7)-L-alpha-D-Hepp-(1->3)-L-alpha-D-Hepp-(1->5)-alpha-Kdo',
                                      'reason': 'Candidate carbohydrate rings '
                                                'are not connected via '
                                                'glycosidic bonds'},
                                  {   'smiles': 'C1([C@H]([C@H]([C@@H]([C@H](O1)CO[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)O)O[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O)O)O',
                                      'name': 'alpha-D-Manp-(1->2)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)-D-Manp',
                                      'reason': 'Candidate carbohydrate rings '
                                                'are not connected via '
                                                'glycosidic bonds'},
                                  {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]([C@@H](O)CO)[C@H](O)CO)[C@H](O)[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H]2O)[C@H]1O',
                                      'name': 'alpha-D-Galp-(1->3)-alpha-D-Glcp-(1->3)-alpha-L-Rhap-(1->3)-D-ribitol',
                                      'reason': 'Found 3 candidate '
                                                'carbohydrate rings, need '
                                                'exactly 4'},
                                  {   'smiles': '[H][C@]1(O[C@@H](O[C@H](CO)[C@]2([H])O[C@@H](O[C@H](CO)[C@]3([H])O[C@@H](O[C@H](CO)[C@]4([H])O[C@@H](O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)CO',
                                      'name': 'beta-D-Galf-(1->5)-beta-D-Galf-(1->5)-beta-D-Galf-(1->5)-beta-D-Galf',
                                      'reason': 'Candidate carbohydrate rings '
                                                'are not connected via '
                                                'glycosidic bonds'},
                                  {   'smiles': 'O(CCCCCCCCCC)CC(OC)C(O)=O',
                                      'name': '2-methoxy-4-oxatetradecanoic '
                                              'acid',
                                      'reason': 'Found 0 candidate '
                                                'carbohydrate rings, need '
                                                'exactly 4'},
                                  {   'smiles': 'OC[C@H]1O[C@H](OC[C@H]2O[C@H](O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@H]4[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]4CO)O[C@@H]3CO)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'alpha-D-Glcp-(1->6)-alpha-D-Glcp-(1->4)-alpha-D-Glcp-(1->4)-alpha-D-Glcp',
                                      'reason': 'Candidate carbohydrate rings '
                                                'are not connected via '
                                                'glycosidic bonds'}],
    'attempt': 2,
    'reasoning': 'Below is one possible revised solution. In our analysis we '
                 'noted that the first version’s detection of a “candidate '
                 'sugar ring” was too strict (for example, requiring three '
                 'chiral centers in pyranoses) and that the test for '
                 'inter‐ring connectivity ignored the role of the “bridge” '
                 '(often an exocyclic oxygen) that connects two rings via a '
                 'single bond. In the revised solution we relax the chiral '
                 'requirement (demanding at least one defined chiral center '
                 'rather than two/three) and “grow” each candidate unit’s '
                 'connectivity set to include adjacent oxygen atoms (which are '
                 'typical linking atoms in glycosidic bonds). Then, '
                 'connectivity among the four rings is decided by requiring '
                 'that each candidate’s connectivity (ring atoms plus linking '
                 'oxygens) intersects at least one other candidate’s '
                 'connectivity. (If one candidate “talks to” all of the others '
                 'then we assume that the four sugar units form one connected '
                 'carbohydrate chain.) \n'
                 '\n'
                 'Below is the complete Python code (contained in one block) '
                 'that uses RDKit:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 39,
    'num_false_positives': 543,
    'num_true_negatives': 141669,
    'num_false_negatives': 49,
    'num_negatives': None,
    'precision': 0.06701030927835051,
    'recall': 0.4431818181818182,
    'f1': 0.11641791044776117,
    'accuracy': 0.9958397751229796,
    'negative_predictive_value': 0.999654242933149}