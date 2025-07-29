"""
Classifies: CHEBI:15693 aldose
"""
"""
Classifies: aldose sugars
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_aldose(smiles: str):
    """
    Determines if a molecule is an aldose based on its SMILES string.
    Aldoses are polyhydroxy aldehydes H[CH(OH)]nC(=O)H (n >= 2) or their cyclic hemiacetal forms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aldose, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of unwanted atoms
    for atom in mol.GetAtoms():
        atomic_num = atom.GetAtomicNum()
        if atomic_num not in [1, 6, 8]:  # Only H, C, O allowed
            return False, f"Contains non-sugar atoms (not H, C, or O)"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 3:
        return False, "Too few carbons for an aldose"
    if o_count < 3:
        return False, "Too few oxygens for an aldose"

    # Check for aromatic rings
    if rdMolDescriptors.CalcNumAromaticRings(mol) > 0:
        return False, "Contains aromatic rings"

    # Check for carboxylic acids (exclude uronic acids)
    carboxyl_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")
    if mol.HasSubstructMatch(carboxyl_pattern):
        return False, "Contains carboxylic acid group"

    # Check for modified sugars
    ether_pattern = Chem.MolFromSmarts("[OX2]([CX4])[CX4]")  # Non-ring ethers
    ester_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2][CX4]")
    if mol.HasSubstructMatch(ester_pattern):
        return False, "Contains ester group"
    
    # Only allow cyclic ethers (hemiacetals)
    ether_matches = mol.GetSubstructMatches(ether_pattern)
    for match in ether_matches:
        atoms = [mol.GetAtomWithIdx(i) for i in match]
        if not all(atom.IsInRing() for atom in atoms):
            return False, "Contains non-cyclic ether (modified sugar)"

    # Pattern for aldehyde group
    aldehyde_pattern = Chem.MolFromSmarts("[CH1](=O)")
    
    # Pattern for hemiacetal
    hemiacetal_pattern = Chem.MolFromSmarts("[O;R]-[CH1](-[O])-[C,O]")
    
    # Pattern for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts("[OH1]")
    
    # Count hydroxyl groups
    hydroxyl_matches = len(mol.GetSubstructMatches(hydroxyl_pattern))
    if hydroxyl_matches < 2:
        return False, "Insufficient hydroxyl groups"

    # Check ring count
    rings = mol.GetRingInfo()
    if rings.NumRings() > 1:
        return False, "Too many rings for aldose"
    
    # If cyclic, check ring size
    if rings.NumRings() == 1:
        ring_sizes = [len(r) for r in rings.AtomRings()]
        if not any(size in [5,6] for size in ring_sizes):
            return False, "Ring size not typical for aldose"

    # Check for either aldehyde or hemiacetal
    has_aldehyde = mol.HasSubstructMatch(aldehyde_pattern)
    has_hemiacetal = mol.HasSubstructMatch(hemiacetal_pattern)
    
    if not (has_aldehyde or has_hemiacetal):
        return False, "No aldehyde or hemiacetal group found"

    # Pattern for carbon chain with hydroxyls
    polyhydroxy_chain = Chem.MolFromSmarts("[CH2,CH1,CH0]-[CH2,CH1,CH0]-[CH2,CH1,CH0]")
    if not mol.HasSubstructMatch(polyhydroxy_chain):
        return False, "No suitable carbon chain found"

    # Check hydroxyl ratio
    ratio_oh_to_c = hydroxyl_matches / c_count
    if ratio_oh_to_c < 0.3:
        return False, "Too few hydroxyls relative to carbons"

    if has_aldehyde:
        return True, "Contains aldehyde group with multiple hydroxyls"
    else:
        return True, "Contains cyclic hemiacetal form with multiple hydroxyls"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15693',
                          'name': 'aldose',
                          'definition': 'Aldehydic parent sugars (polyhydroxy '
                                        'aldehydes H[CH(OH)]nC(=O)H, n >= 2) '
                                        'and their intramolecular hemiacetals.',
                          'parents': ['CHEBI:35381'],
                          'xrefs': ['KEGG:C01370', 'Wikipedia:Aldose'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.7792207792207793 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O NAME: beta-D-fucose '
               'REASON: CORRECT Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: C[C@@H](O)[C@@H](O)CCC=O NAME: amicetose REASON: '
               'CORRECT Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1CO[C@H](O)[C@H](O)[C@H]1O NAME: '
               'alpha-D-xylose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: [H][C@@]1(O[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO '
               'NAME: beta-D-allofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C[C@@H]1OC(O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'L-rhamnopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: C1([C@H]([C@@H]([C@H]([C@H](O1)CO)O)O)O)O NAME: '
               'D-idopyranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO '
               'NAME: alpha-L-mannofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'beta-D-allose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'alpha-L-allose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O)CO NAME: '
               'beta-L-talopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1COC(O)[C@H](O)[C@H]1O NAME: '
               'L-arabinopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)CO NAME: L-glyceraldehyde REASON: '
               'CORRECT Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@H](O)[C@H](O)[C@@H](O)CO NAME: '
               'aldehydo-L-galactose REASON: CORRECT Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-rhamnose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'beta-L-lyxofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: '
               '[H]C([H])([C@]([H])(O)C=O)[C@]([H])(O)[C@@]([H])(C)O NAME: '
               'tyvelose REASON: CORRECT Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'D-glucopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@@H]1O NAME: D-ribofuranose '
               'REASON: CORRECT Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO NAME: '
               'beta-L-mannofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@@H](O)CO NAME: '
               'L-galactofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: [H][C@](C)(O)[C@]([H])(O)[C@@]([H])(O)CC=O NAME: '
               'boivinose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: O[C@H]([C@H](O)[C@@H](O)C=O)[C@@H](O)CO NAME: '
               'aldehydo-L-altrose REASON: CORRECT Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H](O)[C@H](O)[C@@H](O)C=O NAME: '
               'aldehydo-D-xylose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-L-mannose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H](O)[C@H](O)[C@H](O)[C@@H](O)C1 NAME: '
               'alpha-L-lyxopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@@H](C)O NAME: '
               'aldehydo-D-fucose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@@H](O)C1O)[C@@H](O)CO NAME: '
               'L-altrofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[13C@@H](O)[13C@H]1O)CO '
               'NAME: alpha-D-glucose-1,2-((13)C2) REASON: CORRECT Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@H](O)C1O)[C@H](O)CO NAME: '
               'D-idofuranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: C[C@H](O)[C@@H](O)CCC=O NAME: L-rhodinose REASON: '
               'CORRECT Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: C[C@@H](O)[C@H]1O[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-rhamnofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1COC(O)[C@H](O)[C@H]1O NAME: D-xylopyranose '
               'REASON: CORRECT Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: O[C@@H]1CO[C@@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-D-xylose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1OC(O)[C@@H](O)[C@H]1O NAME: L-ribofuranose '
               'REASON: CORRECT Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'beta-L-ribose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H](O)[C@@H](O)C=O NAME: D-erythrose REASON: '
               'CORRECT Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@@H](O)[C@H](O)[C@H]1O NAME: '
               'alpha-L-arabinofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-D-allose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C NAME: '
               '6-deoxy-beta-D-altrofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'beta-L-gulose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]([C@H](O)[C@@H](O)C=O)[C@@H](O)CO NAME: '
               'aldehydo-L-idose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'beta-D-ribose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@H](O)[C@H]1O)CO NAME: '
               'beta-L-xylofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O)C NAME: '
               '6-deoxy-beta-D-gulopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@@H](O)C1O)[C@@H](O)CO NAME: '
               'L-talofuranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@@H]1O)[C@H](O)C NAME: '
               'beta-D-quinovofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@H](O)[C@@H](O)C1O)CO NAME: '
               'L-altropyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@H](O)[C@@H]1O)CO NAME: '
               'beta-D-idopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: C[C@@H]1OC(O)[C@H](O)C[C@H]1O NAME: '
               'ascarylopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@H](O)CO NAME: '
               'D-altrofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'beta-D-mannose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: [H][C@]1(OC(O)[C@@H](O)[C@H]1O)[C@@H](O)CO NAME: '
               'L-allofuranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-glucose REASON: CORRECT Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)C[C@@H](O)[C@@H]1O NAME: '
               '2-deoxy-D-glucopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[H][C@@](O)(CO)[C@]([H])(O)[C@]([H])(O)[C@@]([H])(O)[C@@]([H])(O)[C@]([H])(O)C=O '
               'NAME: D-threo-L-galacto-octose REASON: CORRECT Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@@H](O)[C@@H]1O NAME: '
               'D-arabinofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1CO[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-lyxopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[C@@H]1(O)[C@H](O)[C@@H](O)[C@](OC1O)([C@H](O)CO)[H] NAME: '
               'D-glycero-D-gulo-heptopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@H](O)[C@H](O)[C@H](O)[C@@H](O)C1 NAME: '
               'beta-L-lyxopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-gulofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@H](O)[C@H]1O)CO NAME: '
               'alpha-D-talopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)C=O NAME: '
               'aldehydo-D-idose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'D-mannopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: C[C@@H]1O[C@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-L-rhamnopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[H]C([H])([C@@]([H])(O)C=O)[C@@]([H])(O)[C@@]([H])(C)O NAME: '
               'abequose REASON: CORRECT Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-arabinose REASON: CORRECT Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: C[C@@H](O)[C@H]1O[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'beta-D-rhamnofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1CO[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'alpha-L-ribopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [C@H]1([C@@H]([C@@H](CC(O1)O)O)O)CO NAME: '
               '2-deoxy-D-galactopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@@H]1O)CO NAME: '
               'beta-D-lyxofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: C[C@@H]1OC(O)[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'L-fucopyranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-mannose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)CO NAME: '
               'aldehydo-L-arabinose REASON: CORRECT Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@@H](O)[C@H]1O)[C@H](O)C NAME: '
               'alpha-D-fucofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-D-gulose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1COC(O)[C@@H](O)[C@H]1O NAME: L-ribopyranose '
               'REASON: CORRECT Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: [H][C@]1(O[C@@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO '
               'NAME: alpha-L-allofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'D-allopyranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-quinovopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O)CO '
               'NAME: beta-D-altropyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)C1O)[C@@H](O)CO NAME: '
               'L-idofuranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: [H]C([H])([C@]([H])(O)C=O)[C@]([H])(O)[C@]([H])(C)O '
               'NAME: colitose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: O1[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C1 NAME: '
               'alpha-L-xylopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1CO[C@@H](O)[C@H](O)[C@H]1O NAME: '
               'alpha-L-arabinopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)CO NAME: '
               'aldehydo-L-gulose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-talofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-galactose REASON: CORRECT Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@H](O)[C@@H](O)CO NAME: '
               'aldehydo-L-xylose REASON: CORRECT Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'D-gulopyranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1OC(O)[C@H](O)[C@H]1O NAME: '
               'L-arabinofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1O[C@H](O)[C@@H](O)C[C@@H]1O NAME: '
               'alpha-tyvelopyranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@H](O)C1O)[C@@H](O)CO NAME: '
               'L-glucofuranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)CO NAME: D-glyceraldehyde REASON: '
               'CORRECT Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO '
               'NAME: alpha-L-talofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1COC(O)[C@H](O)[C@@H]1O NAME: D-ribopyranose '
               'REASON: CORRECT Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@H]1O)CO NAME: '
               'alpha-D-xylofuranose REASON: CORRECT Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@@H]1OC(O)[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'L-allopyranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1CO[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'beta-L-xylopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'beta-D-talopyranose REASON: CORRECT Contains cyclic hemiacetal '
               'form with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)C1O)CO NAME: '
               'L-lyxofuranose REASON: CORRECT Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               'False positives: SMILES: O1[C@@H]([C@H]([C@H](C1O)O)O)C NAME: '
               '5-deoxy-D-ribofuranose REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: N[C@H]1[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-glucosamine REASON: WRONGLY CLASSIFIED Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: CC(=O)N[C@@H]1[C@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O '
               'NAME: N-acetyl-beta-D-mannosamine REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: CC(=O)N[C@H]1[C@@H](O)O[C@H](CO)[C@H](O)[C@@H]1O '
               'NAME: N-acetyl-alpha-D-galactosamine REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC[C@H](CC(C(=O)[H])=O)O NAME: '
               '(S)-4,5-dihydroxy-2-oxopentanal REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: NC(=O)[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: beta-D-glucuronamide REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@H]1OCC)CO '
               'NAME: 1-Ethyl-beta-D-galactoside REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: N[C@@H](C[C@@H](O)C=O)C(O)=O NAME: '
               'L-4-hydroxyglutamic semialdehyde REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: '
               'O([C@]([C@@](O[H])([C@](O[H])(C(=O)[H])[H])[H])([C@@](O[H])(C([H])([H])[H])[H])[H])[H] '
               'NAME: 6-deoxy-L-glucose REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]([C@H](O)[C@H](O)CO)[C@@H](O)[C@@H](O)C=O '
               'NAME: D-Glycero-D-gulo-Heptose REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: ON(CCCP(O)(O)=O)C=O NAME: fosmidomycin REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: OCC(O)(CO)[C@@H](O)C=O NAME: D-apiose REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: O1C[C@]([C@H](C1O)O)(O)CO NAME: D-apiofuranose '
               'REASON: WRONGLY CLASSIFIED Contains cyclic hemiacetal form '
               'with multiple hydroxyls\n'
               ' * SMILES: OC([C@@H]([C@H]([C@H](C=O)O)O)OC)(C)C NAME: noviose '
               'REASON: WRONGLY CLASSIFIED Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: O[C@H](COP([O-])([O-])=O)[C@@H](O)[C@H](O)CC=O '
               'NAME: 2-deoxy-D-glucose 6-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: OC1O[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)C(O)=O NAME: '
               'D-mannopyranuronic acid REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: CO[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O '
               'NAME: methyl beta-D-glucuronoside REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](F)[C@@H](O)[C@H]1O NAME: '
               '2-deoxy-2-fluoro-alpha-D-galactose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](N)[C@@H](O)[C@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-mannosamine REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](C[C@@H]1O)OP([O-])([O-])=O NAME: '
               '2-deoxy-alpha-D-ribose 1-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@H](O)COP([O-])([O-])=O NAME: '
               'D-erythrose 4-phosphate(2-) REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)C(OC)=O '
               'NAME: methyl alpha-D-glucopyranuronate REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC1O[C@H](CS(O)(=O)=O)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: 6-sulfo-D-quinovose REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-ribofuranose 5-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H]([18F])[C@@H](O)[C@H](O)[C@H](O)CO '
               'NAME: 2-deoxy-2-((18)F)fluoro-aldehydo-D-glucose REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: O[C@H](COP(O)(O)=O)[C@H](O)[C@@H](O)C=O NAME: '
               'D-xylose 5-phosphate REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: COC[C@H]1O[C@@H](O)[C@H](O)[C@@H](OC)[C@@H]1O NAME: '
               '3,6-di-O-methyl-beta-D-glucose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C(O)=O NAME: '
               'alpha-D-galacturonic acid REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)\\C=C\\C(C(O)=O)=C(\\O)C(O)=O NAME: '
               '2-hydroxy-3-(3-oxoprop-1-enyl)but-2-enedioic acid REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: O1[C@@]([C@H](O)[C@@H](O)[C@H]1OC)([C@H](O)CO)[H] '
               'NAME: Methyl alpha-D-glucofuranoside REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: CSC[C@H]1O[C@H](O)[C@H](O)[C@@H]1O NAME: '
               '5-S-methyl-5-thio-alpha-D-ribofuranose REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC(CS(O)(=O)=O)C=O NAME: 3-sulfolactaldehyde '
               'REASON: WRONGLY CLASSIFIED Contains aldehyde group with '
               'multiple hydroxyls\n'
               ' * SMILES: [H]C([H])(C=O)[C@]([H])(N)[C@]([H])(O)[C@]([H])(C)O '
               'NAME: daunosamine REASON: WRONGLY CLASSIFIED Contains aldehyde '
               'group with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)C1O)C=O NAME: '
               'Galacto-hexodialdose REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O '
               'NAME: beta-D-galacturonate REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1O[C@H](O)[C@H](O)[C@@H](N)[C@H]1O NAME: '
               '3-amino-3,6-dideoxy-alpha-D-galactopyranose REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OCC(CC=O)C(O)=O NAME: '
               '2-(hydroxymethyl)-4-oxobutanoic acid REASON: WRONGLY '
               'CLASSIFIED Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: N[C@H]1C(O)O[C@H](CO)[C@@H](O)[C@@H]1O NAME: '
               '2-amino-2-deoxy-D-glucopyranose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC(C(O)CC([H])=O)CO NAME: 2-deoxypentose REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: COC1OC[C@H](O)[C@@H](O)[C@@H]1O NAME: methyl '
               'L-xylopyranoside REASON: WRONGLY CLASSIFIED Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@]([H])(O)[C@@]1([H])OC[C@@H](O)[C@@H]1O '
               'NAME: 3,6-anhydro-D-galactose REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: OC1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)C(O)=O NAME: '
               'L-glucopyranuronic acid REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC1O[C@H](COP(O)(O)=O)[C@@H](O)[C@@H]1O NAME: '
               'D-arabinofuranose 5-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C([H])(=O)[C@H](O)[C@@H](O)[C@@H](O)C([O-])=O NAME: '
               'L-arabinuronate REASON: WRONGLY CLASSIFIED Contains aldehyde '
               'group with multiple hydroxyls\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OP(O)(O)=O)[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-L-fucose 1-phosphate REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)[C@@H](F)[C@@H](O)[C@@H]1O NAME: '
               '2-deoxy-2-fluoro-D-mannopyranose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1COC(OP(O)(O)=O)[C@H](O)[C@H]1O NAME: '
               'L-arabinose 1-phosphate REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1OC(=C[C@H](O)[C@H]1O)C(O)=O NAME: '
               '4-deoxy-Delta(4)-beta-D-GlcpA REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1OCC)C(O)=O NAME: '
               '6-ethoxy-3,4,5-trihydroxyoxane-2-carboxylic acid REASON: '
               'WRONGLY CLASSIFIED Contains cyclic hemiacetal form with '
               'multiple hydroxyls\n'
               ' * SMILES: O[C@@H](C=O)[C@@H](O)[C@@H](O)[C@H](O)C=O NAME: '
               'D-galacto-hexodialdose REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: '
               '[H][C@](C)(O)[C@]([H])(O)[C@]([H])(OC)[C@@]([H])(O)C=O NAME: '
               'digitalose REASON: WRONGLY CLASSIFIED Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: N[C@H]1[C@H](O)O[C@H](CO)[C@H](O)[C@@H]1O NAME: '
               '2-amino-2-deoxy-beta-D-galactopyranose REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: [C@H]1(CC[C@@H](O1)O)COP(O)(=O)O NAME: '
               '2,3-dideoxy-beta-D-ribose 5-phosphate REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@H](NC(=O)CO)[C@@H](O)[C@@H]1O '
               'NAME: N-glycoloyl-beta-D-glucosamine REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: N[C@@H]1[C@@H](O)[C@@H](O)O[C@H](CO)[C@H]1O NAME: '
               'alpha-D-kanosamine REASON: WRONGLY CLASSIFIED Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C(O)=O '
               'NAME: beta-D-galacturonic acid REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C([C@H]([C@H]([C@@H]([C@@H](CO)O)O)O)NC(=O)C)=O '
               'NAME: aldehydo-N-acetyl-D-mannosamine REASON: WRONGLY '
               'CLASSIFIED Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)C(C)(C)[C@@H](O)C(O)=O NAME: '
               '(R)-4-dehydropantoic acid REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@H](O)[C@@H](NC(=O)C)C1O)CO '
               'NAME: N-Acetyl-L-Idosamine REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OCC)CO '
               'NAME: Ethyl beta-D-glucopyranoside REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: CC(O)(CC=O)CC(O)=O NAME: mevaldic acid REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)COP(O)(O)=O NAME: L-glyceraldehyde '
               '3-phosphate REASON: WRONGLY CLASSIFIED Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'methyl beta-D-galactoside REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@H](O)COP(O)(O)=O NAME: '
               'D-threose 4-phosphate REASON: WRONGLY CLASSIFIED Contains '
               'aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O[C@H]1CO[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O NAME: '
               'alpha-L-arabinose 1-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1OC(O)[C@H](N)[C@@H](O)[C@H]1O NAME: '
               'D-Fucosamine REASON: WRONGLY CLASSIFIED Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[C@@H]1(O)[C@H](O)O[C@H](CS([O-])(=O)=O)[C@H]([C@@H]1O)O NAME: '
               '6-sulfo-beta-D-rhamnose(1-) REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: COC1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O NAME: methyl '
               'D-glucoside REASON: WRONGLY CLASSIFIED Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C1(C(C(OC(C1O)O)C(=O)O)O)O NAME: '
               '3,4,5,6-tetrahydroxyoxane-2-carboxylic acid REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: [H]C([H])(C=O)[C@@](C)(O)[C@@]([H])(O)[C@]([H])(C)O '
               'NAME: mycarose REASON: WRONGLY CLASSIFIED Contains aldehyde '
               'group with multiple hydroxyls\n'
               ' * SMILES: CO[C@@H]1OC[C@@H](O)[C@H](O)[C@H]1O NAME: methyl '
               'beta-D-xylopyranoside REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: CC(=O)N[C@H]1C(O)O[C@H](CO)[C@H](O)[C@@H]1O NAME: '
               'N-acetyl-D-galactosamine REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [NH3+][C@@H]1[C@@H](O)[C@@H](O)O[C@H](CO)[C@H]1O '
               'NAME: alpha-D-kanosamine(1+) REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@@H]1O NAME: '
               'beta-D-arabinofuranose 5-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[C@H]1(O)[C@H](O)O[C@H](CS([O-])(=O)=O)[C@H]([C@@H]1O)O NAME: '
               '6-sulfo-beta-D-quinovose(1-) REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1OC(O)[C@H](O)[C@@H](O)[C@H]1NC(C)=O NAME: '
               '4-acetamido-4,6-dideoxy-D-galactose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](OP(O)(O)=O)[C@H](O)[C@@H]1O NAME: '
               'alpha-D-ribose 1-phosphate REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O=CCC(=O)[C@H](O)CO NAME: '
               '(4R)-4,5-dihydroxy-3-oxopentanal REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: [H][C@]1([18F])C(O)O[C@H](CO)[C@@H](O)[C@@H]1O '
               'NAME: 2-deoxy-2-((18)F)fluoro-D-glucopyranose REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)C(=O)C(=O)[C@@H]1O NAME: '
               '2,3-didehydro-D-glucose REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C1(=C([C@@H]([C@H](C(O1)O)O)O)O)C(O)=O NAME: '
               '4,5-dehydro-D-glucuronic acid REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[H][C@](C)(O)[C@@]([H])(O)[C@]([H])(N)[C@]([H])(O)C=O NAME: '
               'mycosamine REASON: WRONGLY CLASSIFIED Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: [H][C@]1([18F])C(O)O[C@H](CO)[C@H](O)[C@@H]1O NAME: '
               '2-deoxy-2-((18)F)fluoro-D-galactopyranose REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: N[C@@H]1[C@@H](O)C(O)O[C@H](CO)[C@H]1O NAME: '
               '3-amino-3-deoxy-D-glucopyranose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C[C@H]1O[C@H](OP([O-])([O-])=O)[C@H](O)[C@@H]1O '
               'NAME: 5-deoxy-alpha-D-ribose 1-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: OC(=O)C(\\O)=C/C(=C\\C=O)C(O)=O NAME: '
               '4-carboxy-2-hydroxy-cis,cis-muconate 6-semialdehyde REASON: '
               'WRONGLY CLASSIFIED Contains aldehyde group with multiple '
               'hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H]([NH3+])[C@H](O)[C@H](O)CO '
               'NAME: aldehydo-D-kanosamine(1+) REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O=C(N[C@H]([C@@H](O)C=O)[C@@H](O)[C@H](O)C)C NAME: '
               'N-acetyl-3-amino-3,6-dideoxy-D-galactose REASON: WRONGLY '
               'CLASSIFIED Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: OCC1OC(O)C(F)C(O)C1O NAME: '
               '2-deoxy-2-fluorohexopyranose REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)CC(=O)C([O-])=O NAME: '
               '5-dehydro-4-deoxy-D-glucuronate REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O)C(OC)=O '
               'NAME: methyl beta-D-glucopyranuronate REASON: WRONGLY '
               'CLASSIFIED Contains cyclic hemiacetal form with multiple '
               'hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)[C@@H](NC(=O)C)C1O)CO '
               'NAME: N-Acetyl-D-Gulosamine REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O '
               'NAME: N-acetyl-beta-D-glucosamine REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: OC1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O NAME: '
               'D-glucopyranuronate REASON: WRONGLY CLASSIFIED Contains cyclic '
               'hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: C1C(C(C(O1)O)O)O NAME: '
               '2,3,4-trihydroxytetrahydrofuran REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: O1C[C@H]([C@H]([C@@H]1O)O)O NAME: '
               'beta-D-erythrofuranose REASON: WRONGLY CLASSIFIED Contains '
               'cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[H][C@](C)(O)[C@@]([H])(N)[C@]([H])(O)[C@@]([H])(N)C=O NAME: '
               'bacillosamine REASON: WRONGLY CLASSIFIED Contains aldehyde '
               'group with multiple hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)[C@H]1OC)CO NAME: '
               'alpha-d-Lyxofuranoside, methyl REASON: WRONGLY CLASSIFIED '
               'Contains cyclic hemiacetal form with multiple hydroxyls\n'
               ' * SMILES: '
               '[H]C([H])(C=O)[C@@]([H])(N)[C@]([H])(O)[C@]([H])(C)O NAME: '
               'acosamine REASON: WRONGLY CLASSIFIED Contains aldehyde group '
               'with multiple hydroxyls\n'
               ' * SMILES: O[C@H](COP(O)(O)=O)[C@@H](O)CC=O NAME: '
               '2-deoxy-D-ribose 5-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains aldehyde group with multiple hydroxyls\n'
               'False negatives: SMILES: '
               '[H][C@@]1(O[C@](O)([C@@H](O)[C@@H](O)[C@H]1O)C(O)=O)[C@H](O)CO '
               'NAME: alpha-D-Ko REASON: MISSED Molecule too large for simple '
               'aldose\n'
               ' * SMILES: '
               'OC[C@H]1OC(O)[C@H](OP(O)(=O)O[C@H]2[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O '
               'NAME: agrocinopine D REASON: MISSED Molecule too large for '
               'simple aldose\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1O[C@H]2[C@H](O[C@H](C2)C[C@H](O)C)C=3C1=C(O)C(OC)=C(OC)C3',
                                     'name': '(12R)-12-hydroxymonocerin',
                                     'reason': 'Contains aromatic rings'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(20:1(11Z)/16:0)',
                                     'reason': 'Contains non-sugar atoms (not '
                                               'H, C, or O)'},
                                 {   'smiles': 'O=C(C1=C(N)C2=C(OC(C)(C)C=C2)C=C1)C[C@@H](NC(=O)C)CO',
                                     'name': 'Fusarochromene',
                                     'reason': 'Contains non-sugar atoms (not '
                                               'H, C, or O)'},
                                 {   'smiles': 'COc1cc(\\C=C\\C(=O)c2c(O)cc(O)cc2O)ccc1O',
                                     'name': 'homoeriodictyol chalcone',
                                     'reason': 'Contains aromatic rings'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2R,3R,4S,5S,6S)-2-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5S)-5-acetamido-1,2,4,6-tetrahydroxyhexan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Contains non-sugar atoms (not '
                                               'H, C, or O)'},
                                 {   'smiles': 'O1C=2C(CC=C(C)C)=C(OC)C=C(O)C2C(=O)C=C1C3=CC=C(O)C=C3',
                                     'name': 'Artonin U',
                                     'reason': 'Contains aromatic rings'},
                                 {   'smiles': 'O=C(CCCCCCCCC)CCCCCC(O)=O',
                                     'name': '7-Keto palmitic acid',
                                     'reason': 'Contains carboxylic acid '
                                               'group'},
                                 {   'smiles': 'CNC(=N)NCCC[C@H]([NH3+])C([O-])=O',
                                     'name': 'N(omega)-methyl-L-arginine '
                                             'zwitterion',
                                     'reason': 'Contains non-sugar atoms (not '
                                               'H, C, or O)'},
                                 {   'smiles': '[C@]([C@@](/C=C/CCCCCCCCCCC)(O)[H])(NC(=O)C(CCCCCCCCCCCCCCCCCCCCCC)O)([H])CO',
                                     'name': 'N-(2-hydroxy-tetracosanoyl)-hexadecasphing-4-enine',
                                     'reason': 'Contains non-sugar atoms (not '
                                               'H, C, or O)'},
                                 {   'smiles': 'COc1cc2oc(-c3ccc(O)cc3O)c(CC=C(C)C)c(=O)c2c(O)c1\\C=C\\C(C)C',
                                     'name': 'artocarpin',
                                     'reason': 'Contains aromatic rings'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]1(O[C@](O)([C@@H](O)[C@@H](O)[C@H]1O)C(O)=O)[C@H](O)CO',
                                      'name': 'alpha-D-Ko',
                                      'reason': 'Contains carboxylic acid '
                                                'group'},
                                  {   'smiles': 'OC[C@H]1OC(O)[C@H](OP(O)(=O)O[C@H]2[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O',
                                      'name': 'agrocinopine D',
                                      'reason': 'Contains non-sugar atoms (not '
                                                'H, C, or O)'}],
    'attempt': 2,
    'reasoning': 'Let me analyze the outcomes and suggest improvements:\n'
                 '\n'
                 '1. **False Positives Analysis**:\n'
                 '- Many amino sugars (glucosamine, galactosamine) were '
                 'wrongly classified\n'
                 '- Sugar acids (glucuronic acid) were wrongly classified\n'
                 '- Modified sugars (methyl glycosides, phosphates, sulfates) '
                 'were wrongly classified\n'
                 '- Sugar derivatives with other functional groups were '
                 'wrongly classified\n'
                 '\n'
                 '2. **False Negatives Analysis**:\n'
                 '- Some larger but valid aldoses were rejected due to size '
                 'restrictions\n'
                 '- Complex aldoses with phosphate linkages were missed\n'
                 '\n'
                 '3. **Main Issues with Previous Code**:\n'
                 '- Size restrictions were too strict (250 Da cutoff)\n'
                 '- No exclusion of molecules with nitrogen atoms\n'
                 '- No exclusion of molecules with phosphate, sulfate groups\n'
                 '- No exclusion of molecules with carboxylic acid groups\n'
                 '- No proper check for modified sugars (methyl ethers, '
                 'esters)\n'
                 '\n'
                 '4. **Improvement Strategy**:\n'
                 '- Remove molecular weight restriction\n'
                 '- Add checks for unwanted atoms/groups:\n'
                 '  * Exclude molecules with nitrogen (amino sugars)\n'
                 '  * Exclude molecules with sulfur (sulfated sugars)\n'
                 '  * Exclude molecules with phosphorus (phosphated sugars)\n'
                 '- Add pattern matching for:\n'
                 '  * Carboxylic acids (exclude uronic acids)\n'
                 '  * Modified hydroxyl groups (exclude glycosides)\n'
                 '- Keep core aldose identification logic but make it more '
                 'specific\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 180,
    'num_false_positives': 66,
    'num_true_negatives': 142052,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.7317073170731707,
    'recall': 0.989010989010989,
    'f1': 0.8411214953271029,
    'accuracy': 0.9995221363316936,
    'negative_predictive_value': 0.9999859208470019}