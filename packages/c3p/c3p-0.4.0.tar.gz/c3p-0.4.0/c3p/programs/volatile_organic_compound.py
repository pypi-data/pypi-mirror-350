"""
Classifies: CHEBI:134179 volatile organic compound
"""
"""
Classifies: Volatile Organic Compound (VOC)
Definition: “Any organic compound having an initial boiling point less than or equal 
to 250 °C (482 °F) measured at a standard atmospheric pressure of 101.3 kPa.”

Revised Heuristic Strategy:
  1. The molecule must contain at least one carbon atom.
  2. Calculate descriptors: molecular weight (MW) and topological polar surface area (TPSA).
  3. Count non‐halogen heteroatoms (excluding H, carbon and common halogens F, Cl, Br, I).
  4. Assess ring count – if acyclic, allow higher MW cutoff (<=400 Da); if one or more rings,
     use a stricter cutoff (<=300 Da).
  5. If the molecule is “highly functionalized” (≥3 non‐halogen heteroatoms, or if it has 
     ≥2 rings and ≥2 heteroatoms) then assume it has a high boiling point.
  6. If the molecule contains a problematic functional group (an ester group without also 
     having a carboxylic acid group, a carboxylic acid, aromatic hydroxyl (phenol), aromatic 
     amine, or a cyclic ketone), disqualify as VOC.
  7. Finally, if MW is below the cutoff and TPSA is <60 Å², classify as VOC.

Note: This heuristic is approximate.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_volatile_organic_compound(smiles: str):
    """
    Determines if a molecule is a volatile organic compound (VOC) based on a 
    heuristic estimation.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if the molecule is classified as VOC, False otherwise.
        str: Explanation of the classification.
    """
    # Parse SMILES into a molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check that the molecule is organic (has at least one carbon atom)
    if not any(atom.GetAtomicNum() == 6 for atom in mol.GetAtoms()):
        return False, "Not organic (contains no carbon)"
    
    # Calculate descriptors: molecular weight (MW) and topological polar surface area (TPSA)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    
    # Count the non-halogen heteroatoms (exclude H=1, C=6 and common halogens: F=9, Cl=17, Br=35, I=53).
    allowed_halogens = {9, 17, 35, 53}
    hetero_count = sum(1 for atom in mol.GetAtoms() 
                        if atom.GetAtomicNum() not in (1, 6) and atom.GetAtomicNum() not in allowed_halogens)
    
    # Get ring information: number of rings
    ring_count = mol.GetRingInfo().NumRings()
    # Define "simple" as having no rings.
    simple = (ring_count == 0)
    
    # Set molecular weight cutoff based on ring content:
    # For simple (acyclic) molecules, allow a higher cutoff (<=400 Da);
    # for molecules with rings, use a stricter cutoff (<=300 Da).
    cutoff_mw = 400 if simple else 300

    # Extra rejection based on high functionality:
    if hetero_count >= 3:
        return False, f"Too many heteroatoms ({hetero_count}), suggesting high functionality and high boiling point."
    if (not simple) and hetero_count >= 2 and ring_count >= 2:
        return False, f"Multiple rings ({ring_count}) and heteroatoms ({hetero_count}) suggest non‐volatile functionality."
    
    # Define SMARTS patterns for problematic functional groups:
    # 1. Ester group (but allow if there is also a carboxylic acid).
    ester_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H0]")
    acid_pattern  = Chem.MolFromSmarts("[CX3](=O)[OX1H]")
    if mol.HasSubstructMatch(ester_pattern) and not mol.HasSubstructMatch(acid_pattern):
        return False, "Contains an ester group (without accompanying acid functionality), which tends to increase the boiling point."
    
    # 2. Carboxylic acid group.
    if mol.HasSubstructMatch(acid_pattern):
        return False, "Contains a carboxylic acid group, which tends to raise the boiling point."
    
    # 3. Aromatic hydroxyl (phenol): oxygen directly attached to an aromatic carbon.
    phenol_pattern = Chem.MolFromSmarts("c[OH]")
    if mol.HasSubstructMatch(phenol_pattern):
        return False, "Contains an aromatic hydroxyl group (phenol), known to increase boiling point."
    
    # 4. Aromatic primary amine: aromatic carbon with attached NH2.
    arylamine_pattern = Chem.MolFromSmarts("c[NH2]")
    if mol.HasSubstructMatch(arylamine_pattern):
        return False, "Contains an aromatic amine group, which tends to increase boiling point."
    
    # 5. Cyclic ketone: carbonyl group within a ring.
    cyclic_ketone = Chem.MolFromSmarts("[R][CX3](=O)[R]")
    if mol.HasSubstructMatch(cyclic_ketone):
        return False, "Contains a cyclic ketone group, which tends to raise the boiling point."
        
    # Final decision based on descriptors:
    # We require TPSA to be under 60 Å² and molecular weight to be within the cutoff.
    if mol_wt <= cutoff_mw and tpsa < 60:
        return True, (f"Estimated as VOC: MW ({mol_wt:.1f} Da) <= {cutoff_mw} and TPSA ({tpsa:.1f} Å²) < 60, "
                      "suggesting a low boiling point (<=250 °C).")
    else:
        return False, (f"Estimated not VOC: MW ({mol_wt:.1f} Da) and TPSA ({tpsa:.1f} Å²) do not meet criteria "
                       f"for low boiling point (<=250 °C) with cutoff MW = {cutoff_mw} Da.")

# Example usage (for testing)
if __name__ == "__main__":
    test_cases = {
        "nonan-2-ol": "CCCCCCCC(C)O",
        "decan-2-ol": "CCCCCCCCC(C)O",
        "2-dodecene": "[H]C(C)=C([H])CCCCCCCCC",
        "henicosan-3-ol": "CCCCCCCCCCCCCCCCCC(O)CC",
        "hexacosan-4-ol": "CCCCCCCCCCCCCCCCCCCCCCCC(O)CCC",
        "thiophene": "c1ccsc1",
        "4-methylpent-3-enoic acid": "OC(=O)CC=C(C)C",
        "pre-flavunoidine(2+)": "C1(C2CC34C(C1(OC2(CC3)C)C)CCC4C)[NH2+]CCCCC[NH+](C)C",
    }
    
    for name, sm in test_cases.items():
        voc, reason = is_volatile_organic_compound(sm)
        print(f"Name: {name}\n  SMILES: {sm}\n  VOC: {voc}\n  Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134179',
                          'name': 'volatile organic compound',
                          'definition': 'Any organic compound having an '
                                        'initial boiling point less than or '
                                        'equal to 250 degreeC (482 degreeF) '
                                        'measured at a standard atmospheric '
                                        'pressure of 101.3 kPa.',
                          'parents': ['CHEBI:72695'],
                          'xrefs': ['Wikipedia:Volatile_organic_compound'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 78,
                           'log_lines_of_code': 4.356708826689592,
                           'indent_by_line': [   1,
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
                                                 2,
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
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'NumRings',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetRingInfo',
                                                 'CalcTPSA',
                                                 'MolFromSmarts',
                                                 'items',
                                                 'GetAtomicNum'],
                           'methods_called_count': 10,
                           'smarts_strings': [   '[R][CX3](=O)[R]',
                                                 '[CX3](=O)[OX1H]',
                                                 'c[OH]',
                                                 'c[NH2]',
                                                 '[CX3](=O)[OX2H0]'],
                           'smarts_strings_count': 5,
                           'defs': [   'is_volatile_organic_compound(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Not organic (contains no '
                                          'carbon)"',
                                          'False, f"Too many heteroatoms '
                                          '({hetero_count}), suggesting high '
                                          'functionality and high boiling '
                                          'point."',
                                          'False, f"Multiple rings '
                                          '({ring_count}) and heteroatoms '
                                          '({hetero_count}) suggest '
                                          'non‐volatile functionality."',
                                          'False, "Contains an ester group '
                                          '(without accompanying acid '
                                          'functionality), which tends to '
                                          'increase the boiling point."',
                                          'False, "Contains a carboxylic acid '
                                          'group, which tends to raise the '
                                          'boiling point."',
                                          'False, "Contains an aromatic '
                                          'hydroxyl group (phenol), known to '
                                          'increase boiling point."',
                                          'False, "Contains an aromatic amine '
                                          'group, which tends to increase '
                                          'boiling point."',
                                          'False, "Contains a cyclic ketone '
                                          'group, which tends to raise the '
                                          'boiling point."',
                                          'True, (f"Estimated as VOC: MW '
                                          '({mol_wt:.1f} Da) <= {cutoff_mw} '
                                          'and TPSA ({tpsa:.1f} Å²) < 60, "',
                                          'False, (f"Estimated not VOC: MW '
                                          '({mol_wt:.1f} Da) and TPSA '
                                          '({tpsa:.1f} Å²) do not meet '
                                          'criteria "'],
                           'returns_count': 11,
                           'complexity': 5.671341765337918},
    'message': '\n'
               'Attempt failed: F1 score of 0.07133343199644812 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCCC(C)O NAME: nonan-2-ol REASON: '
               'CORRECT Estimated as VOC: MW (144.2 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCC(C)O NAME: decan-2-ol REASON: CORRECT '
               'Estimated as VOC: MW (158.2 Da) <= 350 and TPSA (20.2 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: [H]C(C)=C([H])CCCCCCCCC NAME: 2-dodecene REASON: '
               'CORRECT Estimated as VOC: MW (168.2 Da) <= 350 and TPSA (0.0 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCC(O)CCCCCCC NAME: heptadecan-8-ol REASON: '
               'CORRECT Estimated as VOC: MW (256.3 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCC(O)CC NAME: henicosan-3-ol '
               'REASON: CORRECT Estimated as VOC: MW (312.3 Da) <= 350 and '
               'TPSA (20.2 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: C(CC(C)C)(C(C)C)C NAME: 2,3,5-trimethylhexane '
               'REASON: CORRECT Estimated as VOC: MW (128.2 Da) <= 350 and '
               'TPSA (0.0 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: CCC(C)CC NAME: 3-methylpentane REASON: CORRECT '
               'Estimated as VOC: MW (86.1 Da) <= 350 and TPSA (0.0 Å²) < 60, '
               'suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(O)CC NAME: octadecan-3-ol REASON: '
               'CORRECT Estimated as VOC: MW (270.3 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCC(O)CCCCCCC NAME: pentadecan-8-ol REASON: '
               'CORRECT Estimated as VOC: MW (228.2 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: c1ccsc1 NAME: thiophene REASON: CORRECT Estimated '
               'as VOC: MW (84.0 Da) <= 300 and TPSA (0.0 Å²) < 60, suggesting '
               'a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCC(O)CCCCCCCCC NAME: henicosan-10-ol '
               'REASON: CORRECT Estimated as VOC: MW (312.3 Da) <= 350 and '
               'TPSA (20.2 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC[C@](C)(O)C=C NAME: '
               '(3S,6E)-nerolidol REASON: CORRECT Estimated as VOC: MW (222.2 '
               'Da) <= 350 and TPSA (20.2 Å²) < 60, suggesting a low boiling '
               'point (<=250 °C).\n'
               ' * SMILES: CCCCCCC(C)O NAME: octan-2-ol REASON: CORRECT '
               'Estimated as VOC: MW (130.1 Da) <= 350 and TPSA (20.2 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCC(O)CCCCC NAME: heptadecan-6-ol REASON: '
               'CORRECT Estimated as VOC: MW (256.3 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)CCCC NAME: octadecan-5-ol REASON: '
               'CORRECT Estimated as VOC: MW (270.3 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: OC(=O)CC=C(C)C NAME: 4-methylpent-3-enoic acid '
               'REASON: CORRECT Estimated as VOC: MW (114.1 Da) <= 350 and '
               'TPSA (37.3 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: CCCCCCCCCO NAME: nonan-1-ol REASON: CORRECT '
               'Estimated as VOC: MW (144.2 Da) <= 350 and TPSA (20.2 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCC(O)CCCCCC NAME: tridecan-7-ol REASON: '
               'CORRECT Estimated as VOC: MW (200.2 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: C(/C=C/C=C/C)([H])=O NAME: (E,E)-2,4-hexadienal '
               'REASON: CORRECT Estimated as VOC: MW (96.1 Da) <= 350 and TPSA '
               '(17.1 Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CC/C=C\\CCCCCO NAME: (Z)-non-6-en-1-ol REASON: '
               'CORRECT Estimated as VOC: MW (142.1 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCO NAME: docosan-1-ol REASON: '
               'CORRECT Estimated as VOC: MW (326.4 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: C(CC(C)C)(CCC)C NAME: 2,4-dimethylheptane REASON: '
               'CORRECT Estimated as VOC: MW (128.2 Da) <= 350 and TPSA (0.0 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCCCCCCC(C)O NAME: octadecan-2-ol REASON: '
               'CORRECT Estimated as VOC: MW (270.3 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: CCCCCCCCCCCCCCC(C)O NAME: hexadecan-2-ol REASON: '
               'CORRECT Estimated as VOC: MW (242.3 Da) <= 350 and TPSA (20.2 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: ClC(Cl)C(Cl)(Cl)Cl NAME: pentachloroethane REASON: '
               'CORRECT Estimated as VOC: MW (199.9 Da) <= 350 and TPSA (0.0 '
               'Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               'False positives: SMILES: OC(=O)CCCCCCCC=CCC=CCCCC NAME: '
               '9,12-Heptadecadienoic acid REASON: WRONGLY CLASSIFIED '
               'Estimated as VOC: MW (266.2 Da) <= 350 and TPSA (37.3 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: '
               'O1C([C@]2([C@@](C[C@]1(C)C=C)(C=C(CC2)C)[H])[H])(C)C NAME: '
               'Cabreuva oxide D REASON: WRONGLY CLASSIFIED Estimated as VOC: '
               'MW (220.2 Da) <= 300 and TPSA (9.2 Å²) < 60, suggesting a low '
               'boiling point (<=250 °C).\n'
               ' * SMILES: O1C2(C(CCC=C2CC)(C)C)C=CC1C NAME: Etaspirene '
               'REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (206.2 Da) <= '
               '300 and TPSA (9.2 Å²) < 60, suggesting a low boiling point '
               '(<=250 °C).\n'
               ' * SMILES: O=C(\\C(=C\\CCC)\\C)C NAME: 3-Methyl-3-hepten-2-one '
               'REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (126.1 Da) <= '
               '350 and TPSA (17.1 Å²) < 60, suggesting a low boiling point '
               '(<=250 °C).\n'
               ' * SMILES: OC1(C(C2(C(C(CCC2)(C)C)CC1)C)CCC(C=C)=C)C NAME: '
               '8alpha-13(16),14-Labdadien-8-ol REASON: WRONGLY CLASSIFIED '
               'Estimated as VOC: MW (290.3 Da) <= 300 and TPSA (20.2 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               " * SMILES: C1CCC(C1)=C1CCCC1 NAME: 1,1'-bi(cyclopentylidene) "
               'REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (136.1 Da) <= '
               '300 and TPSA (0.0 Å²) < 60, suggesting a low boiling point '
               '(<=250 °C).\n'
               ' * SMILES: CN(C\\C=C\\C#CC(C)(C)C)Cc1cccc2ccccc12 NAME: '
               'terbinafine REASON: WRONGLY CLASSIFIED Estimated as VOC: MW '
               '(291.2 Da) <= 300 and TPSA (3.2 Å²) < 60, suggesting a low '
               'boiling point (<=250 °C).\n'
               ' * SMILES: OC(=O)CCCC\\C=C\\CCCCC NAME: 6-lauroleic acid '
               'REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (198.2 Da) <= '
               '350 and TPSA (37.3 Å²) < 60, suggesting a low boiling point '
               '(<=250 °C).\n'
               ' * SMILES: C(CCCC)CCC/C=C\\C/C=C\\C/C=C\\CC NAME: '
               '3Z,6Z,9Z-Octadecatriene REASON: WRONGLY CLASSIFIED Estimated '
               'as VOC: MW (248.3 Da) <= 350 and TPSA (0.0 Å²) < 60, '
               'suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: C1C(=CCC=C1)C NAME: 1,4-Cyclohexadiene, 1-methyl- '
               'REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (94.1 Da) <= '
               '300 and TPSA (0.0 Å²) < 60, suggesting a low boiling point '
               '(<=250 °C).\n'
               ' * SMILES: OC(=O)/C=C\\CC\\C=C\\CCC NAME: 2Z,6E-decadienoic '
               'acid REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (168.1 '
               'Da) <= 350 and TPSA (37.3 Å²) < 60, suggesting a low boiling '
               'point (<=250 °C).\n'
               ' * SMILES: C[C@H]1CC[C@H](CC2=C1CC[C@@H]2C)C(C)=C NAME: '
               'alpha-guaiene REASON: WRONGLY CLASSIFIED Estimated as VOC: MW '
               '(204.2 Da) <= 300 and TPSA (0.0 Å²) < 60, suggesting a low '
               'boiling point (<=250 °C).\n'
               ' * SMILES: ClC(Cl)(F)F NAME: dichlorodifluoromethane REASON: '
               'WRONGLY CLASSIFIED Estimated as VOC: MW (119.9 Da) <= 350 and '
               'TPSA (0.0 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: OCCCCCC/C=C/CC NAME: 7E-Decen-1-ol REASON: WRONGLY '
               'CLASSIFIED Estimated as VOC: MW (156.2 Da) <= 350 and TPSA '
               '(20.2 Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: C(CCC(C)C)CCCCCC NAME: Undecane, 2-methyl- REASON: '
               'WRONGLY CLASSIFIED Estimated as VOC: MW (170.2 Da) <= 350 and '
               'TPSA (0.0 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: OC(=O)C/C(=C\\CCCCCC)/C NAME: '
               '(Z)-3-Methyl-3-decenoic acid REASON: WRONGLY CLASSIFIED '
               'Estimated as VOC: MW (184.1 Da) <= 350 and TPSA (37.3 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: O1[C@H]([C@H]1C/C=C\\C/C=C\\CC)CCCCCCCCC NAME: '
               '9S,10R-Epoxy-3Z,6Z-nonadecadiene REASON: WRONGLY CLASSIFIED '
               'Estimated as VOC: MW (278.3 Da) <= 300 and TPSA (12.5 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CCCC[C@H]34)[C@@H]1CC[C@@]2(O)C#C '
               'NAME: Lynestrenol REASON: WRONGLY CLASSIFIED Estimated as VOC: '
               'MW (284.2 Da) <= 300 and TPSA (20.2 Å²) < 60, suggesting a low '
               'boiling point (<=250 °C).\n'
               ' * SMILES: CC(=O)CCCCC=C NAME: 7-octen-2-one REASON: WRONGLY '
               'CLASSIFIED Estimated as VOC: MW (126.1 Da) <= 350 and TPSA '
               '(17.1 Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: O=C(CCC)C(=O)CC NAME: 3,4-Heptanedione REASON: '
               'WRONGLY CLASSIFIED Estimated as VOC: MW (128.1 Da) <= 350 and '
               'TPSA (34.1 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               ' * SMILES: C1(C2C1C=C(CC2)C)(C)C NAME: '
               '3,7,7-Trimethylbicyclo[4.1.0]hept-2-ene REASON: WRONGLY '
               'CLASSIFIED Estimated as VOC: MW (136.1 Da) <= 300 and TPSA '
               '(0.0 Å²) < 60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: C1CCCCC1[NH+](C)C NAME: '
               'N,N-dimethylcyclohexylaminium REASON: WRONGLY CLASSIFIED '
               'Estimated as VOC: MW (128.1 Da) <= 300 and TPSA (4.4 Å²) < 60, '
               'suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: O1C(=NC(=C1C)CC)CCCCC NAME: '
               '4-Ethyl-5-methyl-2-pentyloxazol REASON: WRONGLY CLASSIFIED '
               'Estimated as VOC: MW (181.1 Da) <= 300 and TPSA (26.0 Å²) < '
               '60, suggesting a low boiling point (<=250 °C).\n'
               ' * SMILES: C1Oc2ccccc2C[C@H]1c1ccccc1 NAME: (S)-isoflavan '
               'REASON: WRONGLY CLASSIFIED Estimated as VOC: MW (210.1 Da) <= '
               '300 and TPSA (9.2 Å²) < 60, suggesting a low boiling point '
               '(<=250 °C).\n'
               ' * SMILES: CCCOCCC(C)=O NAME: 4-propoxy-2-butanone REASON: '
               'WRONGLY CLASSIFIED Estimated as VOC: MW (130.1 Da) <= 350 and '
               'TPSA (26.3 Å²) < 60, suggesting a low boiling point (<=250 '
               '°C).\n'
               'False negatives: SMILES: CCCCCCCCCCCCCCCCCCCCCCC(O)CCC NAME: '
               'hexacosan-4-ol REASON: MISSED Estimated not VOC: MW (382.4 Da) '
               'and TPSA (20.2 Å²) do not meet criteria for low boiling point '
               '(<=250 °C) with cutoff MW = 350 Da.\n'
               ' * SMILES: '
               'COc1cc(ccc1O)[C@@H](O)[C@@H]1CO[C@@H]([C@H]1CO)c1ccc(O)c(OC)c1 '
               'NAME: tanegool REASON: MISSED Too many heteroatoms (7), '
               'suggesting high functionality and high boiling point.\n'
               ' * SMILES: O=C1C(OC2=C(C(O)=CC(=C2)C)C)=C(C(=O)C(=C1C)O)C '
               'NAME: Aculeatusquinone A REASON: MISSED Too many heteroatoms '
               '(5), suggesting high functionality and high boiling point.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCC(O)CCCCC NAME: hexacosan-6-ol '
               'REASON: MISSED Estimated not VOC: MW (382.4 Da) and TPSA (20.2 '
               'Å²) do not meet criteria for low boiling point (<=250 °C) with '
               'cutoff MW = 350 Da.\n'
               ' * SMILES: '
               'C1(C2CC34C(C1(OC2(CC3)C)C)CCC4C)[NH2+]CCCCC[NH+](C)C NAME: '
               'pre-flavunoidine(2+) REASON: MISSED Too many heteroatoms (3), '
               'suggesting high functionality and high boiling point.\n'
               ' * SMILES: CCOC(=O)C1CCCCC1 NAME: ethyl cyclohexanecarboxylate '
               'REASON: MISSED Contains an ester group (without acid '
               'functionality), which tends to increase the boiling point.\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)CCCCCCCCCC NAME: tetracosan-11-ol '
               'REASON: MISSED Estimated not VOC: MW (354.4 Da) and TPSA (20.2 '
               'Å²) do not meet criteria for low boiling point (<=250 °C) with '
               'cutoff MW = 350 Da.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCC(C)O NAME: hexacosan-2-ol '
               'REASON: MISSED Estimated not VOC: MW (382.4 Da) and TPSA (20.2 '
               'Å²) do not meet criteria for low boiling point (<=250 °C) with '
               'cutoff MW = 350 Da.\n'
               ' * SMILES: CCOC(C)=O NAME: ethyl acetate REASON: MISSED '
               'Contains an ester group (without acid functionality), which '
               'tends to increase the boiling point.\n'
               ' * SMILES: OC1=C(C(O)=CC(=C1)C)C NAME: Beta-Orcinol REASON: '
               'MISSED Contains an aromatic hydroxyl group (phenol), known to '
               'increase boiling point.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Too many heteroatoms (10), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Too many heteroatoms (9), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Too many heteroatoms (7), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Too many heteroatoms (4), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Too many heteroatoms (5), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Too many heteroatoms (9), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Too many heteroatoms (4), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Contains an ester group '
                                               '(without accompanying acid '
                                               'functionality), which tends to '
                                               'increase the boiling point.'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Too many heteroatoms (4), '
                                               'suggesting high functionality '
                                               'and high boiling point.'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Too many heteroatoms (10), '
                                               'suggesting high functionality '
                                               'and high boiling point.'}],
    'sample_false_negatives': [   {   'smiles': 'COc1cc(ccc1O)[C@@H](O)[C@@H]1CO[C@@H]([C@H]1CO)c1ccc(O)c(OC)c1',
                                      'name': 'tanegool',
                                      'reason': 'Too many heteroatoms (7), '
                                                'suggesting high functionality '
                                                'and high boiling point.'},
                                  {   'smiles': 'O=C1C(OC2=C(C(O)=CC(=C2)C)C)=C(C(=O)C(=C1C)O)C',
                                      'name': 'Aculeatusquinone A',
                                      'reason': 'Too many heteroatoms (5), '
                                                'suggesting high functionality '
                                                'and high boiling point.'},
                                  {   'smiles': 'C1(C2CC34C(C1(OC2(CC3)C)C)CCC4C)[NH2+]CCCCC[NH+](C)C',
                                      'name': 'pre-flavunoidine(2+)',
                                      'reason': 'Too many heteroatoms (3), '
                                                'suggesting high functionality '
                                                'and high boiling point.'},
                                  {   'smiles': 'CCOC(=O)C1CCCCC1',
                                      'name': 'ethyl cyclohexanecarboxylate',
                                      'reason': 'Contains an ester group '
                                                '(without accompanying acid '
                                                'functionality), which tends '
                                                'to increase the boiling '
                                                'point.'},
                                  {   'smiles': 'CCOC(C)=O',
                                      'name': 'ethyl acetate',
                                      'reason': 'Contains an ester group '
                                                '(without accompanying acid '
                                                'functionality), which tends '
                                                'to increase the boiling '
                                                'point.'},
                                  {   'smiles': 'OC1=C(C(O)=CC(=C1)C)C',
                                      'name': 'Beta-Orcinol',
                                      'reason': 'Contains an aromatic hydroxyl '
                                                'group (phenol), known to '
                                                'increase boiling point.'},
                                  {   'smiles': 'C1(C2CC34C(C1(OC2(CC3O)C)C)CCC4C)[NH2+]CCCCC[NH+](C)C',
                                      'name': '10-hydroxy-pre-flavunoidine',
                                      'reason': 'Too many heteroatoms (4), '
                                                'suggesting high functionality '
                                                'and high boiling point.'},
                                  {   'smiles': 'CCOC(=O)C(C)CC',
                                      'name': 'ethyl 2-methylbutyrate',
                                      'reason': 'Contains an ester group '
                                                '(without accompanying acid '
                                                'functionality), which tends '
                                                'to increase the boiling '
                                                'point.'},
                                  {   'smiles': 'CCCCCC(=O)OCCCC',
                                      'name': 'butyl hexanoate',
                                      'reason': 'Contains an ester group '
                                                '(without accompanying acid '
                                                'functionality), which tends '
                                                'to increase the boiling '
                                                'point.'},
                                  {   'smiles': 'O=C1C(=C(O)[C@H](O)[C@]([C@@H]1OC2=C(C(O)=CC(=C2)C)C)(OC)C)C',
                                      'name': 'Aculeatusquinone C',
                                      'reason': 'Too many heteroatoms (6), '
                                                'suggesting high functionality '
                                                'and high boiling point.'}],
    'attempt': 4,
    'reasoning': 'Below is our reasoning and improved solution.\n'
                 '\n'
                 'One observation from our earlier attempt is that many '
                 'compounds were rejected solely because the “simple” '
                 '(acyclic) cutoff was set to 350 Da. For example, long‐chain '
                 'alcohols (such as hexacosan-4-ol, MW ≈ 382 Da) were '
                 'considered non‐volatile even though their overall low '
                 'polarity (TPSA) and flexible structure keep their boiling '
                 'points low. In addition, the status of problematic '
                 'functional groups (ester, carboxylic acid, aromatic –OH or '
                 'arylamines, cyclic ketones) sometimes caused false positives '
                 'when these features weren’t appropriately filtered.\n'
                 '\n'
                 'In this revision we:\n'
                 '1. Require the molecule to be organic (at least one carbon '
                 'atom).\n'
                 '2. Compute descriptors (MW and TPSA) using '
                 'rdMolDescriptors.\n'
                 '3. Count “non‐halogen” heteroatoms to decide on '
                 'functionality.\n'
                 '4. Adjust the MW cutoff so that “simple” (acyclic) molecules '
                 'are allowed a higher cutoff (now 400 Da) versus molecules '
                 'with rings (300 Da).\n'
                 '5. Reject molecules that are too functionalized (≥3 '
                 'non‐halogen heteroatoms, or if the molecule has both ≥2 '
                 'rings and ≥2 heteroatoms).\n'
                 '6. Look for specific problematic groups (ester without acid, '
                 'carboxylic acid, aromatic hydroxyl, aromatic amine, cyclic '
                 'ketone).\n'
                 '7. Finally, if the (adjusted) MW and TPSA (must be below 60 '
                 'Å²) criteria are met then we classify the molecule as VOC.\n'
                 '\n'
                 'The code below implements this revised heuristic. (Note that '
                 'the overall approximation is still heuristic – further '
                 'improvements might require more advanced boiling‐point '
                 'prediction methods.) \n'
                 '\n'
                 'Below is the complete Python code enclosed in one code '
                 'block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 271,
    'num_false_positives': 6364,
    'num_true_negatives': 135644,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.04084400904295403,
    'recall': 0.928082191780822,
    'f1': 0.07824455031037966,
    'accuracy': 0.9551300070274069,
    'negative_predictive_value': 0.9998452069435743}