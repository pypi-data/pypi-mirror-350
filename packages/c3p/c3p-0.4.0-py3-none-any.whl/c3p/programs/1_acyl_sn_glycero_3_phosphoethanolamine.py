"""
Classifies: CHEBI:29017 1-acyl-sn-glycero-3-phosphoethanolamine
"""
"""
Classifies: CHEBI:1-acyl-sn-glycero-3-phosphoethanolamine
Definition: A 1-O-acylglycerophosphoethanolamine having (R)-configuration.
This classifier requires:
  (1) Exactly one phosphorus atom.
  (2) A phosphoethanolamine headgroup in which an "OCCN" fragment is present;
      the oxygen of that fragment must be directly bonded to the phosphorus.
  (3) Exactly one acyl ester linkage (i.e. a C(=O)O–C fragment) where the O-linked carbon
      is not linked to any phosphorus.
  (4) A glycerol backbone substructure as seen in many glycerophospholipids.
  (5) A molecular weight below 1000 Da.
"""

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors, rdmolops

def is_1_acyl_sn_glycero_3_phosphoethanolamine(smiles: str):
    """
    Determines whether a molecule (given via its SMILES string) is a 1-acyl-sn-glycero-3-phosphoethanolamine.
    
    Returns:
       bool: True if the molecule meets the criteria, False otherwise.
       str: The reason for the decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Sanitize and assign stereochemistry.
    try:
        Chem.SanitizeMol(mol)
    except Exception as e:
        return False, "Molecule could not be sanitized: " + str(e)
    AllChem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # (1) Exactly one phosphorus atom.
    phosphorus = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15]
    if len(phosphorus) != 1:
        return False, f"Expected exactly one phosphorus atom; found {len(phosphorus)}"
    
    # (2) Phosphoethanolamine headgroup check.
    # Look for an OCCN fragment.
    headgroup_pat = Chem.MolFromSmarts("OCCN")
    headgroup_matches = mol.GetSubstructMatches(headgroup_pat)
    headgroup_found = False
    for match in headgroup_matches:
        # The match is a tuple of atom indices: (O, C, C, N)
        o_idx = match[0]  # the oxygen that should be connected to phosphorus
        o_atom = mol.GetAtomWithIdx(o_idx)
        # Check that one neighbor of this oxygen is a phosphorus.
        for neighbor in o_atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 15:
                # Also check that the nitrogen is neutral.
                n_atom = mol.GetAtomWithIdx(match[3])
                if n_atom.GetAtomicNum() == 7 and n_atom.GetFormalCharge() == 0:
                    headgroup_found = True
                    break
        if headgroup_found:
            break
    if not headgroup_found:
        return False, "Phosphoethanolamine headgroup (neutral OCCN attached directly to P) not found"
    
    # (3) Exactly one acyl ester linkage.
    # Look for ester fragments of the form: carbonyl C attached to oxygen attached to another carbon.
    ester_pat = Chem.MolFromSmarts("C(=O)O[C]")
    ester_matches = mol.GetSubstructMatches(ester_pat)
    acyl_ester_count = 0
    for match in ester_matches:
        # Match indices: 0 -> carbonyl carbon; 1 -> carbonyl oxygen; 2 -> O-linked carbon.
        o_linked_atom = mol.GetAtomWithIdx(match[2])
        # Exclude if this O-linked carbon is attached to any phosphorus.
        if any(neigh.GetAtomicNum() == 15 for neigh in o_linked_atom.GetNeighbors()):
            continue
        acyl_ester_count += 1
    if acyl_ester_count != 1:
        return False, f"Found {acyl_ester_count} acyl ester linkage(s); exactly one is required"
    
    # (4) Detect glycerol backbone.
    # Many glycerophospholipids have a backbone fragment like: O-C-C(O)-C-O-P .
    # We use a SMARTS pattern "OCC(O)COP" (ignoring chirality markers) as a heuristic.
    glycerol_pat = Chem.MolFromSmarts("OCC(O)COP")
    if not mol.HasSubstructMatch(glycerol_pat):
        return False, "Glycerol backbone substructure (OCC(O)COP) not detected"
    
    # (5) Molecular weight typical for a lipid: below 1000 Da.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 1000:
        return False, f"Molecular weight too high for a typical 1-acyl-GPE lipid (found {mol_wt:.1f} Da)"
    
    reason = (f"Molecule passes all tests: it contains a phosphoethanolamine headgroup (OCCN directly linked to P), "
              f"exactly one acyl ester linkage not bonded to P, a glycerol backbone substructure (OCC(O)COP), "
              f"and has a molecular weight of {mol_wt:.1f} Da.")
    return True, reason


# Optional testing block.
if __name__ == "__main__":
    # A list of example SMILES strings.
    test_smiles = [
        "P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O",  # LysoPE(18:3(9Z,12Z,15Z)/0:0)
        "P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCC)(OCCN)(O)=O",             # PE(15:1(9Z)/0:0)
        "P(OCC(O)COC(=O)CCCCCCCC=CCCCCCCCC)(OCC[NH3+])([O-])=O",           # 2-Azaniumylethyl (2-hydroxy-3-octadec-9-enoyloxypropyl) phosphate
        "P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCN)(O)=O",  # LysoPE(20:3(5Z,8Z,11Z)/0:0)
        "CCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN",                  # 1-heptadecanoyl-sn-glycero-3-phosphoethanolamine
        "CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN",             # 1-oleoyl-sn-glycero-3-phosphoethanolamine
        "C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(O)[H])OP(=O)(O)OCCN",         # PE(18:1(11Z)/0:0)
    ]
    for smi in test_smiles:
        result, reason = is_1_acyl_sn_glycero_3_phosphoethanolamine(smi)
        print("SMILES:", smi)
        print("Result:", result)
        print("Reason:", reason)
        print("-" * 80)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29017',
                          'name': '1-acyl-sn-glycero-3-phosphoethanolamine',
                          'definition': 'A 1-O-acylglycerophosphoethanolamine '
                                        'having (R)-configuration.',
                          'parents': ['CHEBI:55493'],
                          'xrefs': [   'KEGG:C04438',
                                       'LIPID_MAPS_instance:LMGP02050000'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 85,
                           'log_lines_of_code': 4.442651256490317,
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
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
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
                                                 2,
                                                 3,
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
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem, '
                                          'rdMolDescriptors, rdmolops'],
                           'imports_count': 2,
                           'methods_called': [   'GetFormalCharge',
                                                 'CalcExactMolWt',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'SanitizeMol',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'AssignStereochemistry',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['OCC(O)COP', 'C(=O)O[C]', 'OCCN'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_1_acyl_sn_glycero_3_phosphoethanolamine(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule could not be '
                                          'sanitized: " + str(e)',
                                          'False, f"Expected exactly one '
                                          'phosphorus atom; found '
                                          '{len(phosphorus)}"',
                                          'False, "Phosphoethanolamine '
                                          'headgroup (neutral OCCN attached '
                                          'directly to P) not found"',
                                          'False, f"Found {acyl_ester_count} '
                                          'acyl ester linkage(s); exactly one '
                                          'is required"',
                                          'False, "Glycerol backbone '
                                          'substructure (OCC(O)COP) not '
                                          'detected"',
                                          'False, f"Molecular weight too high '
                                          'for a typical 1-acyl-GPE lipid '
                                          '(found {mol_wt:.1f} Da)"',
                                          'True, reason'],
                           'returns_count': 8,
                           'complexity': 6.088530251298063},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'C1(=CN(C(NC1=O)=O)C/C=C/CP(N[C@H](C(OCC2=CC=CC=C2)=O)C)(=O)OC3=CC=CC=C3)Cl '
               'NAME: Benzyl '
               '(2S)-2-[[[(E)-4-(5-chloro-2,4-dioxopyrimidin-1-yl)but-2-enyl]-phenoxyphosphoryl]amino]propanoate '
               'REASON: WRONGLY CLASSIFIED Molecule passes all tests: it has a '
               'phosphoethanolamine headgroup with neutral OCCN adjacent to P, '
               'exactly one acyl ester linkage not involving P, and At least '
               'one chiral center is defined in the structure, with a '
               'molecular weight of 517.1 Da.\n'
               ' * SMILES: '
               'CCC(=O)O[C@H](C(C)C)OP(=O)(CCCCC1=CC=CC=C1)CC(=O)N2C[C@@H](C[C@H]2C(=O)O)C3CCCCC3 '
               'NAME: '
               '(2S,4S)-4-cyclohexyl-1-[2-[[(1S)-2-methyl-1-(1-oxopropoxy)propoxy]-(4-phenylbutyl)phosphoryl]-1-oxoethyl]-2-pyrrolidinecarboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule passes all tests: it '
               'has a phosphoethanolamine headgroup with neutral OCCN adjacent '
               'to P, exactly one acyl ester linkage not involving P, and At '
               'least one chiral center is defined in the structure, with a '
               'molecular weight of 563.3 Da.\n'
               ' * SMILES: '
               '[H][C@]1(C[C@H](N(C1)C(=O)CP(=O)(CCCCc1ccccc1)OC(OC(=O)CC)C(C)C)C([O-])=O)C1CCCCC1 '
               'NAME: fosinopril(1-) REASON: WRONGLY CLASSIFIED Molecule '
               'passes all tests: it has a phosphoethanolamine headgroup with '
               'neutral OCCN adjacent to P, exactly one acyl ester linkage not '
               'involving P, and At least one chiral center is defined in the '
               'structure, with a molecular weight of 562.3 Da.\n'
               ' * SMILES: '
               'N1=CN=C2C(=C1[NH3+])N=CN2C[C@H](OC[P@](N[C@H](C(OC(C)C)=O)C)(=O)OC3=CC=CC=C3)C '
               'NAME: tenofovir alafenamide(1+) REASON: WRONGLY CLASSIFIED '
               'Molecule passes all tests: it has a phosphoethanolamine '
               'headgroup with neutral OCCN adjacent to P, exactly one acyl '
               'ester linkage not involving P, and At least one chiral center '
               'is defined in the structure, with a molecular weight of 477.2 '
               'Da.\n'
               ' * SMILES: '
               'N1=CN=C2C(=C1N)N=CN2C[C@H](OC[P@](N[C@H](C(OC(C)C)=O)C)(=O)OC3=CC=CC=C3)C '
               'NAME: tenofovir alafenamide REASON: WRONGLY CLASSIFIED '
               'Molecule passes all tests: it has a phosphoethanolamine '
               'headgroup with neutral OCCN adjacent to P, exactly one acyl '
               'ester linkage not involving P, and At least one chiral center '
               'is defined in the structure, with a molecular weight of 476.2 '
               'Da.\n'
               ' * SMILES: '
               '[H][C@]1(C[C@H](N(C1)C(=O)CP(=O)(CCCCc1ccccc1)OC(OC(=O)CC)C(C)C)C(O)=O)C1CCCCC1 '
               'NAME: fosinopril REASON: WRONGLY CLASSIFIED Molecule passes '
               'all tests: it has a phosphoethanolamine headgroup with neutral '
               'OCCN adjacent to P, exactly one acyl ester linkage not '
               'involving P, and At least one chiral center is defined in the '
               'structure, with a molecular weight of 563.3 Da.\n'
               ' * SMILES: '
               '[Na+].[H][C@]1(C[C@H](N(C1)C(=O)CP(=O)(CCCCc1ccccc1)OC(OC(=O)CC)C(C)C)C([O-])=O)C1CCCCC1 '
               'NAME: fosinopril sodium REASON: WRONGLY CLASSIFIED Molecule '
               'passes all tests: it has a phosphoethanolamine headgroup with '
               'neutral OCCN adjacent to P, exactly one acyl ester linkage not '
               'involving P, and At least one chiral center is defined in the '
               'structure, with a molecular weight of 585.3 Da.\n'
               'False negatives: SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O '
               'NAME: LysoPE(18:3(9Z,12Z,15Z)/0:0) REASON: MISSED '
               'Phosphoethanolamine headgroup found but no neutral OCCN '
               'fragment is near a phosphorus atom\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCC)(OCCN)(O)=O '
               'NAME: PE(15:1(9Z)/0:0) REASON: MISSED Phosphoethanolamine '
               'headgroup found but no neutral OCCN fragment is near a '
               'phosphorus atom\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCCCCCCC=CCCCCCCCC)(OCC[NH3+])([O-])=O NAME: '
               '2-Azaniumylethyl (2-hydroxy-3-octadec-9-enoyloxypropyl) '
               'phosphate REASON: MISSED Phosphoethanolamine headgroup found '
               'but no neutral OCCN fragment is near a phosphorus atom\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCN)(O)=O '
               'NAME: LysoPE(20:3(5Z,8Z,11Z)/0:0) REASON: MISSED '
               'Phosphoethanolamine headgroup found but no neutral OCCN '
               'fragment is near a phosphorus atom\n'
               ' * SMILES: CCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN '
               'NAME: 1-heptadecanoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'MISSED Phosphoethanolamine headgroup found but no neutral OCCN '
               'fragment is near a phosphorus atom\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN '
               'NAME: 1-oleoyl-sn-glycero-3-phosphoethanolamine REASON: MISSED '
               'Phosphoethanolamine headgroup found but no neutral OCCN '
               'fragment is near a phosphorus atom\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(O)[H])OP(=O)(O)OCCN '
               'NAME: PE(18:1(11Z)/0:0) REASON: MISSED Phosphoethanolamine '
               'headgroup found but no neutral OCCN fragment is near a '
               'phosphorus atom\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O '
               'NAME: LysoPE(20:3(11Z,14Z,17Z)/0:0) REASON: MISSED '
               'Phosphoethanolamine headgroup found but no neutral OCCN '
               'fragment is near a phosphorus atom\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O NAME: '
               'LysoPE(22:0/0:0) REASON: MISSED Phosphoethanolamine headgroup '
               'found but no neutral OCCN fragment is near a phosphorus atom\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(OCCN)(O)=O '
               'NAME: LPE 22:3 REASON: MISSED Phosphoethanolamine headgroup '
               'found but no neutral OCCN fragment is near a phosphorus atom\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Expected exactly one '
                                               'phosphorus atom; found 0'}],
    'sample_false_negatives': [   {   'smiles': 'P(OCC(O)COC(=O)CCCCCCCC=CCCCCCCCC)(OCC[NH3+])([O-])=O',
                                      'name': '2-Azaniumylethyl '
                                              '(2-hydroxy-3-octadec-9-enoyloxypropyl) '
                                              'phosphate',
                                      'reason': 'Phosphoethanolamine headgroup '
                                                '(neutral OCCN attached '
                                                'directly to P) not found'},
                                  {   'smiles': 'P(OC[C@H](O)COC(=O)CCCCCCCC1C(C1)CCCCCC)(OCC[NH3+])([O-])=O',
                                      'name': 'LPE(17:1/0:0)',
                                      'reason': 'Phosphoethanolamine headgroup '
                                                '(neutral OCCN attached '
                                                'directly to P) not found'}],
    'attempt': 5,
    'reasoning': 'Below is my reasoning.\n'
                 '\n'
                 'It appears that the previous version looked separately for a '
                 '“neutral OCCN” fragment and then checked that some nitrogen '
                 'in that fragment was within three bonds of phosphorus. In '
                 'practice many of our valid lipid examples have the OCCN '
                 'attached directly to phosphorus (via an oxygen), but the '
                 'distance‐based check was too strict and therefore many '
                 'lipids were missed. In addition, many nonlipid molecules '
                 '(such as peptide‐like compounds) by chance have an OCCN '
                 'fragment, an ester motif, and even chiral centers even '
                 'though they lack a glycerol backbone. To improve matters, I '
                 'decided to (1) require that one “OCCN” fragment actually be '
                 'directly attached to P (by checking that the oxygen '
                 'immediately preceding the “CCN” is bonded to a phosphorus '
                 'atom) and (2) require that a glycerol “backbone” be present '
                 'using a SMARTS pattern that requires a three‐carbon chain '
                 'with two –OH groups and bound to phosphate (i.e. “OCC(O)COP” '
                 'appears in many valid lipids). Finally, I kept the original '
                 'check for exactly one acyl ester linkage (after making sure '
                 'that the O-linked carbon is not attached to phosphorus) and '
                 'a molecular weight cutoff. \n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 247,
    'num_true_negatives': 142026,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.09191176470588236,
    'recall': 0.9259259259259259,
    'f1': 0.16722408026755856,
    'accuracy': 0.9982501756851722,
    'negative_predictive_value': 0.999985918269637}