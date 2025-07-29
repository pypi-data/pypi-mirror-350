"""
Classifies: CHEBI:28892 ganglioside
"""
"""
Classifies: Ganglioside – A molecule composed of a glycosphingolipid (ceramide and oligosaccharide)
with one or more sialic acids linked on the sugar chain.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_ganglioside(smiles: str):
    """
    Determines if a molecule is a ganglioside based on its SMILES string.
    Gangliosides are complex lipids characterized by:
      - A ceramide portion (represented here by the presence of at least one amide bond).
      - An oligosaccharide chain containing one or more sialic acid residues (indicated by at least one carboxyl group and sugar rings).
      - A long aliphatic chain (many sp3 carbon atoms) to represent the fatty acid part.
      - A relatively high molecular weight (here, at least 700 Da).
      
    Improvements from the previous approach:
      - Instead of requiring two sugar rings with a high oxygen fraction, we count any ring of size 5–7 (nonaromatic) 
        that contains at least one oxygen as a plausible sugar ring. We require at least one such ring.
        
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a ganglioside, False otherwise.
        str: Explanation for the classification decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Add explicit hydrogens to improve substructure perception.
    mol = Chem.AddHs(mol)
    
    # Heuristic 1: Look for at least one amide bond as a proxy for the ceramide portion.
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide bond found – missing ceramide signature"
    
    # Heuristic 2: Look for carboxyl groups indicating sialic acid(s).
    # Check both deprotonated and neutral carboxyl forms.
    carboxyl1 = Chem.MolFromSmarts("C(=O)O")
    carboxyl2 = Chem.MolFromSmarts("C(=O)[O-]")
    if not (mol.HasSubstructMatch(carboxyl1) or mol.HasSubstructMatch(carboxyl2)):
        return False, "No carboxyl group found – sialic acid marker appears to be missing"
    
    # Heuristic 3: Identify sugar rings within the oligosaccharide portion.
    # We now count any nonaromatic ring of size 5, 6, or 7 that contains at least one oxygen atom.
    ring_info = mol.GetRingInfo()
    sugar_ring_count = 0
    for ring in ring_info.AtomRings():
        # Consider only rings of size 5-7.
        if len(ring) not in (5, 6, 7):
            continue
        # Skip the ring if any atom in it is aromatic.
        if any(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            continue
        # Count this ring as "sugar-like" if at least one atom is oxygen.
        if any(mol.GetAtomWithIdx(idx).GetAtomicNum() == 8 for idx in ring):
            sugar_ring_count += 1
    if sugar_ring_count < 1:
        return False, f"Only {sugar_ring_count} sugar-like ring(s) detected; oligosaccharide portion appears insufficient"
    
    # Heuristic 4: Check for a long aliphatic chain representing the fatty acid tail.
    longest_chain = 0
    # Iterate over all carbon atoms that are sp3 and nonaromatic.
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue  # not a carbon atom
        if atom.GetIsAromatic() or atom.GetHybridization().name != "SP3":
            continue
        chain_length = 1
        visited = {atom.GetIdx()}
        stack = [(atom, chain_length)]
        while stack:
            current, length = stack.pop()
            for nbr in current.GetNeighbors():
                if nbr.GetAtomicNum() == 6 and (not nbr.GetIsAromatic()) and \
                   (nbr.GetHybridization().name == "SP3") and (nbr.GetIdx() not in visited):
                    visited.add(nbr.GetIdx())
                    new_length = length + 1
                    if new_length > longest_chain:
                        longest_chain = new_length
                    stack.append((nbr, new_length))
    if longest_chain < 16:
        return False, f"Longest aliphatic chain is too short ({longest_chain} carbons) for the ceramide part"
    
    # Heuristic 5: Check overall molecular weight.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 700:
        return False, f"Molecular weight too low ({mol_wt:.1f} Da) for a typical ganglioside"
    
    return True, "Contains ceramide (amide bond), oligosaccharide (sugar-like ring and carboxyl group) and a long fatty acid chain characteristic of a ganglioside"

# Example usage:
# result, reason = is_ganglioside("CCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)...")
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28892',
                          'name': 'ganglioside',
                          'definition': 'A molecule composed of a '
                                        'glycosphingolipid (ceramide and '
                                        'oligosaccharide) with one or more '
                                        'sialic acids linked on the sugar '
                                        'chain.',
                          'parents': ['CHEBI:17761', 'CHEBI:36526'],
                          'xrefs': [   'MetaCyc:Gangliosides',
                                       'PMID:16158191',
                                       'PMID:2088646',
                                       'PMID:38623278',
                                       'PMID:38848944',
                                       'PMID:38887845',
                                       'PMID:39092231',
                                       'Wikipedia:Ganglioside'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 76,
                           'log_lines_of_code': 4.330733340286331,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
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
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'CalcExactMolWt',
                                                 'GetIdx',
                                                 'GetHybridization',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'pop',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'add',
                                                 'AddHs',
                                                 'GetRingInfo',
                                                 'GetIsAromatic'],
                           'methods_called_count': 17,
                           'smarts_strings': ['C(=O)O', 'C(=O)N', 'C(=O)[O-]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_ganglioside(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No amide bond found – '
                                          'missing ceramide signature"',
                                          'False, "No carboxyl group found – '
                                          'sialic acid marker appears to be '
                                          'missing"',
                                          'False, f"Only {sugar_ring_count} '
                                          'sugar-like ring(s) detected; '
                                          'oligosaccharide portion appears '
                                          'insufficient"',
                                          'False, f"Longest aliphatic chain is '
                                          'too short ({longest_chain} carbons) '
                                          'for the ceramide part"',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} Da) for a typical '
                                          'ganglioside"',
                                          'True, "Contains ceramide (amide '
                                          'bond), oligosaccharide (sugar-like '
                                          'ring and carboxyl group) and a long '
                                          'fatty acid chain characteristic of '
                                          'a ganglioside"'],
                           'returns_count': 7,
                           'complexity': 7.066146668057266},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               "beta-D-Gal-(1->3)-beta-D-GalNAc-(1->4)-[alpha-Neu5Ac-(2->3)]-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/16:0) "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; '
               'oligosaccharide portion appears insufficient\n'
               ' * SMILES: '
               '[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)C)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O '
               'NAME: ganglioside GM2 (2:0) REASON: MISSED Only 0 sugar-like '
               'ring(s) detected; oligosaccharide portion appears '
               'insufficient\n'
               ' * SMILES: '
               'O1C([C@H](NC(=O)C)C(O)C[C@]1(O[C@H]2[C@@H](O)C(O[C@@H](OC[C@H](NC(=O)CCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)C2O)CO)C(O)=O)[C@H](O)[C@H](O)CO '
               'NAME: GM4(d18:1/16:0) REASON: MISSED Only 0 sugar-like ring(s) '
               'detected; oligosaccharide portion appears insufficient\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H](CO)[C@@H](O)[C@]1([H])O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@@H]1[C@@H](O)[C@@H](O[C@H](CO)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@]([H])(O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H]1NC(C)=O)O[C@@H]1[C@@H](CO)O[C@@H](OC[C@H](NC(=O)CCCCCCCCCCCCCCCCC)[C@H](O)\\C=C\\CCCCCCCCCCCCC)[C@H](O)[C@H]1O)C(O)=O)C(O)=O)[C@H](O)[C@H](O)CO '
               'NAME: ganglioside GT1b REASON: MISSED Only 0 sugar-like '
               'ring(s) detected; oligosaccharide portion appears '
               'insufficient\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O[C@@]5(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)CO)C(O)=O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               "alpha-Neu5Ac-(2->3)-beta-D-Gal-(1->3)-beta-D-GalNAc-(1->4)-[alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->3)]-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/18:0) "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; '
               'oligosaccharide portion appears insufficient\n'
               ' * SMILES: '
               '[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])(C(O)=O)O[C@@H]([C@H]([C@@]2(O[C@](O[C@H]3[C@H]([C@H](O[C@H]([C@@H]3O)O[C@@H]4[C@H](O[C@H]([C@@H]([C@H]4O)O)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(CCCCCCCCCCCCCCCCC)=O)CO)CO)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O)O)CO)NC(C)=O)(C[C@H](O)[C@H]2NC(=O)C)C(O)=O)[H])O)CO '
               'NAME: '
               "beta-Gal-(1->3)-beta-GalNAc-(1->4)-[alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->3)]-beta-Gal-(1->4)-beta-Glc-(1<->1')-Cer(d18:1/18:0) "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; '
               'oligosaccharide portion appears insufficient\n'
               ' * SMILES: '
               '[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O '
               'NAME: ganglioside GM2 (24:0) REASON: MISSED Only 0 sugar-like '
               'ring(s) detected; oligosaccharide portion appears '
               'insufficient\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)C(O)=O)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               "beta-GalNAc-(1->4)-[alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->3)]-beta-Gal-(1->4)-beta-Glc-(1->1')-Cer(d18:1/18:0) "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; '
               'oligosaccharide portion appears insufficient\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O[C@@]5(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               "alpha-Neu5Ac-(2->3)-beta-D-Gal-(1->3)-beta-D-GalNAc-(1->4)-[alpha-Neu5Ac-(2->3)]-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/24:0) "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; '
               'oligosaccharide portion appears insufficient\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               "alpha-Neu5Ac-(2->3)-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/21:0) "
               'REASON: MISSED Only 0 sugar-like ring(s) detected; '
               'oligosaccharide portion appears insufficient\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No carboxyl group found – '
                                               'sialic acid marker appears to '
                                               'be missing'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No amide bond found – missing '
                                               'ceramide signature'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No carboxyl group found – '
                                               'sialic acid marker appears to '
                                               'be missing'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No amide bond found – missing '
                                               'ceramide signature'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No amide bond found – missing '
                                               'ceramide signature'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No amide bond found – missing '
                                               'ceramide signature'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No carboxyl group found – '
                                               'sialic acid marker appears to '
                                               'be missing'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No carboxyl group found – '
                                               'sialic acid marker appears to '
                                               'be missing'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No amide bond found – missing '
                                               'ceramide signature'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No amide bond found – missing '
                                               'ceramide signature'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': "beta-D-Gal-(1->3)-beta-D-GalNAc-(1->4)-[alpha-Neu5Ac-(2->3)]-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/16:0)",
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (15 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': '[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)C)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O',
                                      'name': 'ganglioside GM2 (2:0)',
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (13 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': 'O1C([C@H](NC(=O)C)C(O)C[C@]1(O[C@H]2[C@@H](O)C(O[C@@H](OC[C@H](NC(=O)CCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)C2O)CO)C(O)=O)[C@H](O)[C@H](O)CO',
                                      'name': 'GM4(d18:1/16:0)',
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (15 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': '[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@@]23O[C@]([C@@H]([C@H](C2)O)NC3=O)([C@@H]([C@@H](CO)O)O)[H])O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4COS(=O)(=O)O)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@@H]([C@H]([C@@H](O[C@@H]6CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCC)O)O)O)NC(=O)C)O',
                                      'name': "alpha-Neu5d5N;1,5-lactam-(2->3)-beta-D-Gal-(1->4)-beta-D-GlcNAc6S-(1->3)-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/18:0)",
                                      'reason': 'No carboxyl group found – '
                                                'sialic acid marker appears to '
                                                'be missing'},
                                  {   'smiles': 'O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(C)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(C)=O)O)C(=O)O)O',
                                      'name': "alpha-N-acetylneuraminosyl-(2->3)-[beta-D-galactosyl-(1->3)-N-acetyl-beta-D-galactosaminyl-(1->4)]-beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1')-N-acetylsphingosine",
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (13 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': 'O([C@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]4[C@H](O)[C@@H](O)[C@@H](O[C@@H]4CO)OC[C@@H](NC(=O)CCCCCCC/C=C\\CCCCCCCC)[C@@H](O)/C=C\\CCCCCCCCCCCCC)[C@@H]1O)CO)[C@]5(O[C@@]([C@H](NC(=O)C)[C@@H](O)C5)([C@@H](O)[C@@H](O)CO)[H])C(O)=O',
                                      'name': 'Ganglioside GM1 (18:1/9Z-18:1)',
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (13 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC\\C=C/CCCCCCCC',
                                      'name': "alpha-Neu5Ac-(2->3)-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/24:1(15Z))",
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (13 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': 'O1[C@](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@H](O)C(O)[C@@H](O[C@@H]3CO)OC[C@H](NC(=O)CCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)(C[C@H](O)[C@@H](NC(=O)C)C1[C@H](O)[C@H](O)CO)C(O)=O',
                                      'name': 'Ganglioside GM3 (d18:1/16:0)',
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (15 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': "alpha-Neu5Ac-(2->3)-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/16:0)",
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (15 carbons) for '
                                                'the ceramide part'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCC\\C=C/CCCCCCCC',
                                      'name': "alpha-Neu5Ac-(2->3)-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/22:1(13Z))",
                                      'reason': 'Longest aliphatic chain is '
                                                'too short (13 carbons) for '
                                                'the ceramide part'}],
    'attempt': 5,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'One major failure of the previous attempt was that many '
                 'valid ganglioside examples had “no sugar‐like rings” '
                 'detected. Even though gangliosides by definition must '
                 'contain an oligosaccharide chain, our heuristic based on '
                 'counting rings with at least a 20% oxygen fraction (and '
                 'requiring at least two such rings) ended up missing them. In '
                 'many cases the sugar rings are embedded, fused, or decorated '
                 'with substituents so that the original “sugar‐ring” SMARTS '
                 'fails. To improve classification I decided to (1) keep the '
                 'amide bond (as a proxy for the ceramide), (2) retain a check '
                 'for at least one carboxyl group (a hallmark of sialic acid) '
                 'and (3) change our sugar screening. Instead of using a '
                 'fractional oxygen threshold we now simply count any '
                 'nonaromatic ring of size 5–7 that contains at least one '
                 'oxygen atom (which should capture many (pyranose or '
                 'furanose) rings found in sugars). In this revised version we '
                 'require at least one sugar‐like ring. We also keep the check '
                 'for a long aliphatic chain (the fatty acid part) and an '
                 'overall molecular weight threshold. Although these are only '
                 'heuristics, they are expected to reduce the number of false '
                 'negatives (as in the previous attempt) for ganglioside '
                 'classification.\n'
                 '\n'
                 'Below is the complete Python program.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 30,
    'num_false_positives': 65,
    'num_true_negatives': 142185,
    'num_false_negatives': 20,
    'num_negatives': None,
    'precision': 0.3157894736842105,
    'recall': 0.6,
    'f1': 0.41379310344827586,
    'accuracy': 0.9994026704146171,
    'negative_predictive_value': 0.9998593579691291}