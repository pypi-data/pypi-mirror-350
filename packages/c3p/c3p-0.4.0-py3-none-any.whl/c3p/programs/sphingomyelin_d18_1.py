"""
Classifies: CHEBI:17636 sphingomyelin d18:1
"""
"""
Classifies: Any sphingomyelin having sphingosine as the sphingoid component (sphingomyelin d18:1).
This method checks that the molecule has a phosphocholine headgroup and an amide bond,
and then isolates the sphingosine backbone by breaking (a) the amide bond (separating the acyl chain) and
(b) the O–P bond that attaches the phosphocholine headgroup to the sphingosine sugar.
The sphingosine backbone is expected to have 18 carbon atoms and one carbon–carbon double bond.
"""

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

def is_sphingomyelin_d18_1(smiles: str):
    """
    Determines if a molecule is sphingomyelin d18:1 (i.e. has a sphingosine backbone of 18 carbons with one double bond)
    based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is classified as sphingomyelin d18:1, False otherwise.
        str: Reason for the classification.
    """
    # Parse the input SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # First check for the phosphocholine headgroup using SMARTS.
    # This pattern covers the fragment: -O-COP(=O)([O-])OCC[N+](C)(C)C
    phos_smarts = "COP(=O)([O-])OCC[N+](C)(C)C"
    phos_query = Chem.MolFromSmarts(phos_smarts)
    if phos_query is None:
        return False, "Invalid phosphocholine SMARTS"
    
    if not mol.HasSubstructMatch(phos_query):
        return False, "Phosphocholine headgroup not found"

    # Check for an amide bond connecting the sphingosine to the acyl chain.
    amide_smarts = "[N;!R]-C(=O)"
    amide_query = Chem.MolFromSmarts(amide_smarts)
    if amide_query is None:
        return False, "Invalid amide SMARTS"
    
    amide_matches = mol.GetSubstructMatches(amide_query)
    if not amide_matches:
        return False, "Amide bond not found (required for sphingomyelin structure)"
    
    # Use the first found amide bond and retrieve the two atoms in the bond.
    # The nitrogen will be part of the sphingosine backbone.
    amide_match = amide_matches[0]
    if len(amide_match) < 2:
        return False, "Unexpected amide match result"
    
    amide_N_idx = amide_match[0]
    amide_C_idx = amide_match[1]
    bond = mol.GetBondBetweenAtoms(amide_N_idx, amide_C_idx)
    if bond is None:
        return False, "Expected amide bond not found in molecule structure"
    
    bond_idx = bond.GetIdx()
    
    # Fragment the molecule by breaking the amide bond.
    frag_mol = Chem.FragmentOnBonds(mol, [bond_idx])
    # Get fragments as individual molecules.
    frags = Chem.GetMolFrags(frag_mol, asMols=True, sanitizeFrags=True)
    if len(frags) < 2:
        return False, "Fragmentation failed to separate acyl chain from sphingosine backbone"
    
    # Identify the fragment that contains the phosphocholine headgroup.
    backbone_with_head = None
    for frag in frags:
        if frag.HasSubstructMatch(phos_query):
            backbone_with_head = frag
            break
    if backbone_with_head is None:
        return False, "Could not isolate sphingosine fragment (phosphocholine headgroup not found in any fragment)"
    
    # Now, instead of deleting the entire phosphocholine headgroup (which may remove the connecting oxygen),
    # we search for the O-P bond (the ester linkage from sphingosine to the phosphocholine).
    op_bond_idx = None
    for bond in backbone_with_head.GetBonds():
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        # Look for a bond between an oxygen (atomic number 8) and phosphorus (atomic number 15)
        if (a1.GetAtomicNum() == 8 and a2.GetAtomicNum() == 15) or (a1.GetAtomicNum() == 15 and a2.GetAtomicNum() == 8):
            op_bond_idx = bond.GetIdx()
            break
    if op_bond_idx is None:
        return False, "O–P bond connecting phosphocholine headgroup not found"
    
    # Fragment the backbone fragment by breaking the O–P bond.
    backbone_frag = Chem.FragmentOnBonds(backbone_with_head, [op_bond_idx])
    # Get the fragments after breaking the O-P bond.
    frags_after_deletion = Chem.GetMolFrags(backbone_frag, asMols=True, sanitizeFrags=True)
    if not frags_after_deletion:
        return False, "Fragmentation after breaking O–P bond failed"
    
    # Choose the fragment that does not contain phosphorus (atomic number 15).
    sphingo_candidate = None
    for frag in frags_after_deletion:
        if not any(atom.GetAtomicNum() == 15 for atom in frag.GetAtoms()):
            sphingo_candidate = frag
            break
    if sphingo_candidate is None:
        return False, "Could not isolate sphingosine backbone after removal of phosphocholine headgroup"
    
    # Now count the number of carbon atoms in the sphingosine candidate.
    carbon_count = sum(1 for atom in sphingo_candidate.GetAtoms() if atom.GetAtomicNum() == 6)
    
    # Count the number of carbon–carbon double bonds.
    cc_double_bonds = 0
    for bond in sphingo_candidate.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            a1 = bond.GetBeginAtom()
            a2 = bond.GetEndAtom()
            if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 6:
                cc_double_bonds += 1
                
    # For sphingosine d18:1 we expect exactly 18 carbons and one C=C double bond.
    if carbon_count != 18:
        return False, f"Sphingosine backbone does not have 18 carbons (found {carbon_count} carbons after headgroup removal)"
    if cc_double_bonds != 1:
        return False, f"Sphingosine backbone does not have exactly one C=C double bond (found {cc_double_bonds})"
    
    # All criteria are met.
    return True, "Molecule contains a phosphocholine headgroup and a sphingosine (d18:1) backbone (18 carbons with one double bond)"


# Example usage (for testing purposes; remove or comment out if using as a module):
if __name__ == "__main__":
    # Test with one of the provided example SMILES strings:
    example_smiles = "[H][C@@](O)(\\C=C\\CCCCCCCCCCCCC)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCCCC\\C=C/CCCCCCCC"
    result, reason = is_sphingomyelin_d18_1(example_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17636',
                          'name': 'sphingomyelin d18:1',
                          'definition': 'Any sphingomyelin having sphingosine '
                                        'as the sphingoid component.',
                          'parents': ['CHEBI:64583'],
                          'xrefs': [   'KEGG:C00550',
                                       'LIPID_MAPS_instance:LMSP03010000',
                                       'PMID:3196084'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 102,
                           'log_lines_of_code': 4.624972813284271,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 2,
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
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem, '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetBonds',
                                                 'GetIdx',
                                                 'GetMolFrags',
                                                 'GetEndAtom',
                                                 'GetBondType',
                                                 'GetBondBetweenAtoms',
                                                 'GetBeginAtom',
                                                 'FragmentOnBonds',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 14,
                           'smarts_strings': ['phos_smarts', 'amide_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_sphingomyelin_d18_1(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Invalid phosphocholine '
                                          'SMARTS"',
                                          'False, "Phosphocholine headgroup '
                                          'not found"',
                                          'False, "Invalid amide SMARTS"',
                                          'False, "Amide bond not found '
                                          '(required for sphingomyelin '
                                          'structure)"',
                                          'False, "Unexpected amide match '
                                          'result"',
                                          'False, "Expected amide bond not '
                                          'found in molecule structure"',
                                          'False, "Fragmentation failed to '
                                          'separate acyl chain from '
                                          'sphingosine backbone"',
                                          'False, "Could not isolate '
                                          'sphingosine fragment '
                                          '(phosphocholine headgroup not found '
                                          'in any fragment)"',
                                          'False, "O–P bond connecting '
                                          'phosphocholine headgroup not found"',
                                          'False, "Fragmentation after '
                                          'breaking O–P bond failed"',
                                          'False, "Could not isolate '
                                          'sphingosine backbone after removal '
                                          'of phosphocholine headgroup"',
                                          'False, f"Sphingosine backbone does '
                                          'not have 18 carbons (found '
                                          '{carbon_count} carbons after '
                                          'headgroup removal)"',
                                          'False, f"Sphingosine backbone does '
                                          'not have exactly one C=C double '
                                          'bond (found {cc_double_bonds})"',
                                          'True, "Molecule contains a '
                                          'phosphocholine headgroup and a '
                                          'sphingosine (d18:1) backbone (18 '
                                          'carbons with one double bond)"'],
                           'returns_count': 15,
                           'complexity': 7.724994562656855},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'P(OC[C@H](NC(=O)CCC/C=C\\C[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d19:1/PGE2) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphocholine headgroup and a sphingosine (d18:1) '
               'backbone (18 carbons with one double bond)\n'
               ' * SMILES: '
               'S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC)C[C@H](N)C(=O)N[C@H]([C@H](O)\\C=C\\CCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d19:1/LTE4) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphocholine headgroup and a sphingosine (d18:1) '
               'backbone (18 carbons with one double bond)\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CCC[C@@H](O)[C@H](O)/C=C\\C=C/C=C/C=C/[C@@H](O)C/C=C\\CC)[C@H](O)\\C=C\\CCCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d19:1/20:5(7Z,9Z,11E,13E,17Z)-3OH(5,6,15)) REASON: '
               'WRONGLY CLASSIFIED Molecule contains a phosphocholine '
               'headgroup and a sphingosine (d18:1) backbone (18 carbons with '
               'one double bond)\n'
               'False negatives: SMILES: '
               '[H][C@@](O)(\\C=C\\CCCCCCCCCCCCC)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-[(15Z)-tetracosenoyl]sphing-4-enine-1-phosphocholine '
               'REASON: MISSED Sphingosine backbone does not have 18 carbons '
               '(found 17 carbons after removing headgroup)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCC\\C=C/CCCCCC '
               'NAME: N-(9Z-hexadecenoyl)sphingosine-1-phosphocholine REASON: '
               'MISSED Sphingosine backbone does not have 18 carbons (found 17 '
               'carbons after removing headgroup)\n'
               ' * SMILES: '
               'C(C/C=C\\CCCCCCCC)CCCCCCCCCC(CC(=O)N[C@@H](COP(OCC[N+](C)(C)C)(=O)[O-])[C@@H](\\C=C\\CCCCCCCCCCCCC)O)O '
               'NAME: '
               'N-[(15Z)-3-hydroxytetracos-15-enoyl]sphingosine-1-phosphocholine '
               'REASON: MISSED Sphingosine backbone does not have 18 carbons '
               '(found 17 carbons after removing headgroup)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-stearoylsphingosine-1-phosphocholine REASON: MISSED '
               'Sphingosine backbone does not have 18 carbons (found 17 '
               'carbons after removing headgroup)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-nonadecanoylsphingosine-1-phosphocholine REASON: '
               'MISSED Sphingosine backbone does not have 18 carbons (found 17 '
               'carbons after removing headgroup)\n'
               ' * SMILES: '
               'C(\\CCCCCC(CC(=O)N[C@@H](COP(OCC[N+](C)(C)C)(=O)[O-])[C@@H](\\C=C\\CCCCCCCCCCCCC)O)O)=C\\CCCCCC '
               'NAME: '
               'N-[(9Z)-3-hydroxyhexadec-9-enoyl]sphingosine-1-phosphocholine '
               'REASON: MISSED Sphingosine backbone does not have 18 carbons '
               '(found 17 carbons after removing headgroup)\n'
               ' * SMILES: '
               '[H][C@@](O)(\\C=C\\CCCCCCCCCCCCC)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-[(13Z)-docosenoyl]sphing-4-enine-1-phosphocholine '
               'REASON: MISSED Sphingosine backbone does not have 18 carbons '
               '(found 17 carbons after removing headgroup)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-lignoceroylsphingosine-1-phosphocholine REASON: MISSED '
               'Sphingosine backbone does not have 18 carbons (found 17 '
               'carbons after removing headgroup)\n'
               ' * SMILES: '
               '[H][C@@](O)(\\C=C\\CCCCCCCCCCCCC)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCCCCC '
               'NAME: N-pentadecanoylsphingosine-1-phosphocholine REASON: '
               'MISSED Sphingosine backbone does not have 18 carbons (found 17 '
               'carbons after removing headgroup)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCCC '
               'NAME: N-tridecanoylsphingosine-1-phosphocholine REASON: MISSED '
               'Sphingosine backbone does not have 18 carbons (found 17 '
               'carbons after removing headgroup)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Phosphocholine headgroup not '
                                               'found'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'We can hypothesize that the previous approach fails because '
                 'the procedure to “delete” the phosphocholine headgroup ends '
                 'up removing not only the headgroup but also its connecting '
                 'atom(s) from the sphingosine backbone. In sphingomyelin the '
                 'phosphocholine is attached via an O‐phosphate ester at the '
                 'primary hydroxyl of sphingosine. Removing the SMARTS '
                 'fragment for phosphocholine may “steal” the linking oxygen '
                 'so that only 17 carbons remain in the backbone. Also, if the '
                 'fragmentation does not properly isolate the sphingosine base '
                 'before counting its atoms, the count may be off. To improve '
                 'the approach we can (1) first break the acyl (amide) bond to '
                 'separate the fatty acyl chain; (2) then, instead of deleting '
                 'the entire phosphocholine group, identify and break just the '
                 'oxygen–phosphorus bond that connects the phosphocholine '
                 'headgroup to the sphingosine base; (3) select the fragment '
                 'that does not contain any phosphorus as the sphingosine '
                 'backbone and then count its carbon atoms and carbon–carbon '
                 'double bonds.\n'
                 '\n'
                 'Below is a complete Python code block implementing this '
                 'revised strategy.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 18,
    'num_true_negatives': 142259,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5609756097560976,
    'recall': 1.0,
    'f1': 0.71875,
    'accuracy': 0.9998735066760366,
    'negative_predictive_value': 1.0}