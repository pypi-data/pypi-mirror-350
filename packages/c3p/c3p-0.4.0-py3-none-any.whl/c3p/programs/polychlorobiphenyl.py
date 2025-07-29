"""
Classifies: CHEBI:53156 polychlorobiphenyl
"""
"""
Classifies: polychlorobiphenyl
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polychlorobiphenyl(smiles: str):
    """
    Determines if a molecule is a polychlorobiphenyl based on its SMILES string.
    A polychlorobiphenyl has 2-10 chlorine atoms attached to a biphenyl core.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polychlorobiphenyl, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for biphenyl core with more flexible pattern
    # This pattern matches two aromatic rings connected by a single bond
    biphenyl_pattern = Chem.MolFromSmarts("c:1:c:c:c:c:c:1-c:1:c:c:c:c:c:1")
    if not mol.HasSubstructMatch(biphenyl_pattern):
        return False, "No biphenyl core found"

    # Count chlorine atoms
    cl_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 17]
    n_chlorines = len(cl_atoms)
    
    if n_chlorines < 2:
        return False, f"Too few chlorines ({n_chlorines}), minimum is 2"
    if n_chlorines > 10:
        return False, f"Too many chlorines ({n_chlorines}), maximum is 10"

    # Get all atoms in the molecule
    all_atoms = mol.GetAtoms()
    
    # Check for unwanted elements or substituents
    allowed_atoms = {6, 17}  # Only carbon and chlorine allowed
    for atom in all_atoms:
        atomic_num = atom.GetAtomicNum()
        # Skip hydrogen as it's often implicit
        if atomic_num == 1:
            continue
        if atomic_num not in allowed_atoms:
            return False, f"Contains non-allowed element: {atom.GetSymbol()}"
        
        # For carbon atoms, check they're either part of aromatic system or single bonds only
        if atomic_num == 6:
            if not atom.GetIsAromatic():
                # Check all bonds are single
                bonds = atom.GetBonds()
                for bond in bonds:
                    if bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
                        return False, "Contains non-aromatic carbon with non-single bonds"

    # Get the two benzene rings from biphenyl core
    matches = mol.GetSubstructMatches(biphenyl_pattern)
    if len(matches) > 0:
        ring_atoms = set(matches[0])
        
        # Check if all atoms are part of the core structure or are chlorines
        for atom in all_atoms:
            idx = atom.GetIdx()
            if idx not in ring_atoms and atom.GetAtomicNum() != 17:
                return False, "Contains atoms outside biphenyl core that aren't chlorine"

        # Verify chlorines are attached to aromatic carbons
        for cl in cl_atoms:
            neighbors = cl.GetNeighbors()
            if len(neighbors) != 1:
                return False, "Invalid chlorine bonding"
            neighbor = neighbors[0]
            if not (neighbor.GetAtomicNum() == 6 and neighbor.GetIsAromatic()):
                return False, "Chlorine not attached to aromatic carbon"
            if neighbor.GetIdx() not in ring_atoms:
                return False, "Chlorine attached outside biphenyl core"

    return True, f"Valid polychlorobiphenyl with {n_chlorines} chlorine atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:53156',
                          'name': 'polychlorobiphenyl',
                          'definition': 'A biphenyl compound containing '
                                        'between 2 and 10 chlorine atoms '
                                        'attached to the two benzene rings.',
                          'parents': ['CHEBI:134045', 'CHEBI:35446'],
                          'xrefs': ['Wikipedia:Polychlorinated_biphenyl'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.6262626262626263 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: Clc1ccc(Cl)c(c1Cl)-c1c(Cl)ccc(Cl)c1Cl '
               "NAME: 2,2',3,3',6,6'-hexachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Clc1ccc(-c2cc(Cl)c(Cl)c(Cl)c2)c(Cl)c1Cl NAME: '
               "2,3,3',4,4',5'-Hexachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: ClC=1C(C=2C(Cl)=CC(Cl)=C(Cl)C2)=CC(Cl)=C(Cl)C1Cl '
               'NAME: PCB180 REASON: CORRECT Valid polychlorobiphenyl with 7 '
               'chlorine atoms\n'
               ' * SMILES: Clc1cc(-c2ccccc2)c(Cl)c(Cl)c1Cl NAME: '
               '2,3,4,5-tetrachlorobiphenyl REASON: CORRECT Valid '
               'polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Clc1ccc(cc1)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "3,4,4',5-Tetrachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: '
               'ClC1=C(OC)C=C(C2=C(OC)C=C(OC)C(=C2C)Cl)C3=C1C[C@@H]4C(C=5C=C(O)C=C(C5C([C@@]4(C3=O)O)=O)O)(C)C '
               'NAME: Formicamycin Q REASON: CORRECT Valid polychlorobiphenyl '
               'with 2 chlorine atoms\n'
               ' * SMILES: Clc1c(Cl)c(Cl)c(-c2ccccc2)c(Cl)c1Cl NAME: '
               '2,3,4,5,6-pentachlorobiphenyl REASON: CORRECT Valid '
               'polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Clc1ccc(Cl)c(-c2ccccc2)c1Cl NAME: '
               '2,3,6-trichlorobiphenyl REASON: CORRECT Valid '
               'polychlorobiphenyl with 3 chlorine atoms\n'
               ' * SMILES: Clc1cc(Cl)cc(c1)-c1cc(Cl)cc(Cl)c1 NAME: '
               "3,3',5,5'-tetrachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Clc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',4,4',5,5'-hexachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,3',4,4',5-Hexachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Clc1ccc(cc1)-c1ccc(Cl)cc1 NAME: '
               "4,4'-dichlorobiphenyl REASON: CORRECT Valid polychlorobiphenyl "
               'with 2 chlorine atoms\n'
               ' * SMILES: ClC1=C(C=2C(Cl)=CC(Cl)=C(Cl)C2)C=CC(Cl)=C1Cl NAME: '
               'PCB138 REASON: CORRECT Valid polychlorobiphenyl with 6 '
               'chlorine atoms\n'
               ' * SMILES: Clc1cccc(Cl)c1-c1ccccc1 NAME: 2,6-dichlorobiphenyl '
               'REASON: CORRECT Valid polychlorobiphenyl with 2 chlorine '
               'atoms\n'
               ' * SMILES: Clc1ccc(c(Cl)c1)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "2,3',4,4',5'-Pentachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Clc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,3',4,5-pentachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Clc1cc(Cl)cc(c1)-c1ccccc1 NAME: '
               '3,5-dichlorobiphenyl REASON: CORRECT Valid polychlorobiphenyl '
               'with 2 chlorine atoms\n'
               ' * SMILES: Clc1ccc(cc1)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "2,4,4',6-tetrachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Clc1ccc(cc1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,4,4',5-Pentachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Clc1ccccc1-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',4,5-tetrachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Clc1cc(Cl)c(Cl)c(-c2ccccc2)c1Cl NAME: '
               '2,3,5,6-tetrachlorobiphenyl REASON: CORRECT Valid '
               'polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Clc1ccc(Cl)c(c1)-c1ccccc1 NAME: '
               '2,5-dichlorobiphenyl REASON: CORRECT Valid polychlorobiphenyl '
               'with 2 chlorine atoms\n'
               ' * SMILES: Clc1cc(cc(Cl)c1Cl)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "3,4,5,3',4',5'-Hexachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1ccc(Cl)c(Cl)c1Cl NAME: '
               "2,3,4,3',4'-Pentachlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Clc1cccc(c1)-c1cc(Cl)ccc1Cl NAME: '
               "2,3',5-trichlorobiphenyl REASON: CORRECT Valid "
               'polychlorobiphenyl with 3 chlorine atoms\n'
               'False positives: SMILES: '
               'ClC1=C(OC)C(C2=C3C(=O)C=4C(=O)C5=C(O)C=C(O)C=C5C(C4C(C3=C(Cl)C(=C2)OC)=O)(C)C)=C(C)C=C1OC '
               'NAME: Naphthacemycin A10 REASON: WRONGLY CLASSIFIED Valid '
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: Oc1ccc(cc1)-c1c(Cl)cccc1Cl NAME: '
               "2,6-dichloro-4'-biphenylol REASON: WRONGLY CLASSIFIED Valid "
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(Cl)c(Cl)c1-c1cc(Cl)cc(Cl)c1Cl NAME: '
               "2,2',3,3',5,5'-Hexachloro-6-biphenylol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Oc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2',3',4',5'-tetrachlorobiphenyl-3-ol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)c(Cl)c(c(Cl)c1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',3,4',5,5',6-heptachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 7 chlorine atoms\n'
               ' * SMILES: Nc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(N)cc1Cl NAME: '
               "2,2',5,5'-Tetrachlorobenzidine REASON: WRONGLY CLASSIFIED "
               'Valid polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(Cl)cc1-c1ccccc1 NAME: '
               '2-Hydroxy-3,5-dichlorobiphenyl REASON: WRONGLY CLASSIFIED '
               'Valid polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: '
               'O=C(NC1=CC(Cl)=C(C2=CC=CC=C2OC(F)(F)F)C(Cl)=C1)CC3=CC=C(S(=O)(CC)=O)C=C3 '
               'NAME: GSK805 REASON: WRONGLY CLASSIFIED Valid '
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: Oc1cccc(c1)-c1cc(Cl)ccc1Cl NAME: '
               "2',5'-dichlorobiphenyl-3-ol REASON: WRONGLY CLASSIFIED Valid "
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(cc1Cl)-c1cc(Cl)ccc1Cl NAME: '
               "4-hydroxy-2',3,5,5'-tetrachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: '
               'ClC1=C(C2=C(Cl)C=C3N[C@@H]4[C@@](C3=C2)(O)C[C@H]5C(=O)N[C@@H](C(=O)N6NCCC[C@H]6C(=O)N7NCCC[C@@H]7C(N[C@H](C(N[C@@H](C(N45)=O)[C@@H](O)C)=O)COC)=O)C(C)C)C=C8[C@]9(O)C[C@H]%10C(=O)N[C@@H](C(=O)N%11NCCC[C@H]%11C(=O)N%12NCCC[C@@H]%12C(N[C@H](C(N[C@@H](C(N%10[C@@H]9NC8=C1)=O)[C@@H](O)C)=O)COC)=O)C(C)C '
               'NAME: Chloptosin REASON: WRONGLY CLASSIFIED Valid '
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(c(Cl)c1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',3,4',5,5'-Hexachloro-4-biphenylol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(cc1Cl)-c1ccc(Cl)cc1 NAME: '
               "4,3',5'-Trichloro-4'-biphenol REASON: WRONGLY CLASSIFIED Valid "
               'polychlorobiphenyl with 3 chlorine atoms\n'
               ' * SMILES: Oc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',4',5,5'-pentachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(cc1Cl)-c1cc(Cl)c(O)c(Cl)c1 NAME: '
               "3,3',5,5'-tetrachlorobiphenyl-4,4'-diol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Oc1ccc(cc1)-c1c(Cl)c(Cl)c(O)c(Cl)c1Cl NAME: '
               "2,3,5,6-tetrachloro-1,1'-biphenyl-4,4'-diol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(c(Cl)c1Cl)-c1ccc(Cl)c(Cl)c1Cl NAME: '
               "2,2',3,3',4',5-Hexachloro-4-biphenylol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: '
               'ClC1=C2C(=O)C3=C(C(=O)C=4C(O)=CC(=CC4C3(C)C)O)C(C2=C(C5=C(OC)C(Cl)=C(O)C=C5C)C=C1OC)=O '
               'NAME: Naphthacemycin A7 REASON: WRONGLY CLASSIFIED Valid '
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: Cn1cc(C(=O)Nc2ccc(F)cc2-c2ccc(Cl)c(Cl)c2)c(n1)C(F)F '
               'NAME: bixafen REASON: WRONGLY CLASSIFIED Valid '
               'polychlorobiphenyl with 2 chlorine atoms\n'
               ' * SMILES: '
               'CS(=O)(=O)c1cc(Cl)c(cc1Cl)-c1cc(Cl)c(cc1Cl)S(C)(=O)=O NAME: '
               "2,2',5,5'-tetrachloro-4,4'-bis(methylsulfonyl)biphenyl REASON: "
               'WRONGLY CLASSIFIED Valid polychlorobiphenyl with 4 chlorine '
               'atoms\n'
               ' * SMILES: Oc1ccc(c(Cl)c1)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',4',6'-tetrachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 4 chlorine atoms\n'
               ' * SMILES: Oc1cc(Cl)c(c(Cl)c1Cl)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "2,2'3,4',6,6'-Hexachloro-4-biphenylol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 6 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)cc(-c2ccc(Cl)c(Cl)c2)c(Cl)c1Cl NAME: '
               "4-Hydroxy-2,3,3',4',5-pentachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 5 chlorine atoms\n'
               ' * SMILES: Oc1c(Cl)c(Cl)cc(c1Cl)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,2',3',4,4',5,5'-Heptachloro-3-biphenylol REASON: WRONGLY "
               'CLASSIFIED Valid polychlorobiphenyl with 7 chlorine atoms\n'
               ' * SMILES: Nc1ccc(cc1Cl)-c1ccc(N)c(Cl)c1 NAME: '
               "3,3'-Dichlorobenzidine REASON: WRONGLY CLASSIFIED Valid "
               'polychlorobiphenyl with 2 chlorine atoms\n'
               'False negatives: SMILES: '
               'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(O)=CC(=C1C3=C(O)C(Cl)=CC(=C3)Cl)Cl '
               'NAME: Ambigol D REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin E REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(C3=C(O)C(Cl)=CC(=C3)Cl)=CC(=C1O)Cl '
               'NAME: Ambigol E REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin D REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin I REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'ClC1=C(O)C=2C(=O)[C@]3(O)C(=O)C4=C(C5=C(OC)C=C(OC)C(=C5C)Cl)C=C(OC)C(=C4C[C@@H]3C(C2C=C1O)(C)C)Cl '
               'NAME: Formicamycin F REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'BrC1=C(O)C(Cl)=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin L REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin J REASON: MISSED Chlorine attached outside '
               'biphenyl core\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1C=C(N=C2N1NN=N2)C3=CC=CC=C3',
                                     'name': '5-phenyl-1,7-dihydrotetrazolo[1,5-a]pyrimidine',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                     'name': 'TG(14:1(9Z)/22:1(13Z)/18:1(11Z))',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1O',
                                     'name': 'beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-D-Manp-(1->3)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-GlcpNAc-(1->4)-beta-D-GlcpNAc',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': '[C@@]12([C@@]([C@]([C@@H](CC1)C)(CCC(CC)C)C)(CCC[C@@H]2C)[H])C',
                                     'name': 'clerodane',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4R,5R,6R)-3,4-dihydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'O=C(NC(CC(C)C)C(=O)N[C@@H](CCCN=C(N)N)C=O)C(NC(=O)CC)CC(C)C',
                                     'name': 'Leupeptin Pr-LL',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)CCNC(=O)C(=C2C3=CC=CC=C3C(=N2)NC(=O)C4=CC=CS4)C#N',
                                     'name': 'N-[3-[1-cyano-2-[2-(4-methoxyphenyl)ethylamino]-2-oxoethylidene]-1-isoindolyl]-2-thiophenecarboxamide',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'O=C1O[C@@H](CC=2C1=C(OC)C(O)=CC2)CCC[C@@H](O)C',
                                     'name': 'Penicimarin C',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'CO[C@@H]1[C@@H]2[C@@H](C[C@@H]3[C@@](O2)([C@H]([C@@H]([C@H](O3)C(=O)OC)O)O)O)OC1N4C=NC5=C4N=CN=C5N',
                                     'name': 'LSM-4497',
                                     'reason': 'No biphenyl core found'},
                                 {   'smiles': 'C[C@@H]1[C@H](O)CCC2=CC[C@H](C[C@]12C)C(C)=C',
                                     'name': '1-deoxycapsidiol',
                                     'reason': 'No biphenyl core found'}],
    'sample_false_negatives': [   {   'smiles': 'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(O)=CC(=C1C3=C(O)C(Cl)=CC(=C3)Cl)Cl',
                                      'name': 'Ambigol D',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin E',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(OC)C=C(C2=C(OC)C=C(OC)C(=C2C)Cl)C3=C1C[C@@H]4C(C=5C=C(O)C=C(C5C([C@@]4(C3=O)O)=O)O)(C)C',
                                      'name': 'Formicamycin Q',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(C3=C(O)C(Cl)=CC(=C3)Cl)=CC(=C1O)Cl',
                                      'name': 'Ambigol E',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin D',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin I',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(O)C=2C(=O)[C@]3(O)C(=O)C4=C(C5=C(OC)C=C(OC)C(=C5C)Cl)C=C(OC)C(=C4C[C@@H]3C(C2C=C1O)(C)C)Cl',
                                      'name': 'Formicamycin F',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'BrC1=C(O)C(Cl)=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin L',
                                      'reason': 'Contains non-allowed element: '
                                                'Br'},
                                  {   'smiles': 'OC1=C(C=C(C=C1[N+]([O-])=O)Cl)C2=C(O)C([N+](=O)[O-])=CC(=C2)Cl',
                                      'name': 'niclofolan',
                                      'reason': 'Contains non-allowed element: '
                                                'O'},
                                  {   'smiles': 'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin J',
                                      'reason': 'Contains non-allowed element: '
                                                'O'}],
    'attempt': 1,
    'reasoning': 'Let me analyze the issues from the previous attempt:\n'
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- Most false positives are hydroxylated PCBs (e.g., '
                 '"2,6-dichloro-4\'-biphenylol") or other substituted '
                 'biphenyls\n'
                 '- The program is detecting the biphenyl core and chlorines '
                 'but not checking for other substituents\n'
                 '- We should ensure the biphenyl core only has chlorine '
                 'substitutions\n'
                 '\n'
                 '2. False Negatives Analysis:\n'
                 '- Most false negatives are complex molecules (like '
                 'Formicamycins and Ambigols)\n'
                 '- The current code is too strict about the biphenyl pattern\n'
                 '- Some valid PCBs might have slightly different aromatic '
                 'patterns that our SMARTS pattern misses\n'
                 '\n'
                 "Here's how we can improve:\n"
                 '\n'
                 '1. Make the biphenyl pattern more flexible to catch '
                 'different aromatic representations\n'
                 '2. Add checks to ensure only chlorine substitutions are '
                 'present\n'
                 '3. Improve the validation of the aromatic core structure\n'
                 '4. Add additional checks for unwanted substituents\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 29,
    'num_false_positives': 0,
    'num_true_negatives': 142261,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.7435897435897436,
    'f1': 0.8529411764705882,
    'accuracy': 0.9999297259311314,
    'negative_predictive_value': 0.9999297116067224}