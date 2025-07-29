"""
Classifies: CHEBI:35681 secondary alcohol
"""
"""
Classifies: Secondary Alcohol
Definition:
    A secondary alcohol is defined as a compound in which every –OH group 
    (after explicitly adding hydrogens) is attached to a saturated (sp³) carbon 
    that is bonded to exactly two other carbon atoms and one hydrogen.
    
    In addition, if disqualifying functional groups such as carboxylic acid/carboxylate 
    or phosphate groups (and certain carboxamide groups that are not directly linked to 
    the secondary alcohol carbon) are present, the molecule is not considered a pure 
    secondary alcohol.
    
Our approach:
  1. Parse the SMILES and add explicit hydrogens.
  2. Check for disqualifying substructures – for example a carboxylic acid (or its salt) 
     or a phosphate group. For carboxamides we allow only those directly adjacent to a secondary‐OH
     (e.g. in lactamide).
  3. Next, iterate over all oxygen atoms that may be part of an –OH group (i.e. atoms with exactly 
     two neighbors, one hydrogen and one carbon). For each, check that its attached carbon is sp³ 
     and (ignoring the –OH oxygen) has exactly two carbon neighbors and one hydrogen.
  4. If at least one –OH is encountered and every –OH conforms to the secondary pattern then 
     the molecule is classified as a secondary alcohol.
"""

from rdkit import Chem

def is_secondary_alcohol(smiles: str):
    """
    Determines if a molecule is a secondary alcohol based on its SMILES string.
    Here a “secondary alcohol” means that every hydroxyl group (–OH) in the molecule 
    is attached to a saturated (sp³) carbon that is bonded to exactly two other carbons
    and one hydrogen—and the molecule does not contain disqualifying functional groups.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a secondary alcohol, False otherwise.
        str: Explanation/reason for the classification decision.
    """
    # Parse molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Add explicit hydrogens so that we can accurately count attached hydrogens.
    mol = Chem.AddHs(mol)
    
    # --- STEP 1: DISQUALIFY MOLECULES WITH UNWANTED FUNCTIONAL GROUPS ---
    # Carboxylic acids (or their deprotonated forms): e.g. ...C(=O)[OH] or ...C(=O)[O-]
    acid_smarts = Chem.MolFromSmarts("[CX3](=O)[O;H1,-]")
    if mol.HasSubstructMatch(acid_smarts):
        return False, "Contains carboxylic acid or carboxylate group"
    
    # Phosphate group: common pattern P(=O)(O)(O)
    phosphate_smarts = Chem.MolFromSmarts("P(=O)(O)(O)")
    if mol.HasSubstructMatch(phosphate_smarts):
        return False, "Contains phosphate group"
    
    # Carboxamide groups – allow only when the –OH is directly attached to the same carbon
    # (as in lactamide). Generic carboxamide pattern:
    carboxamide_smarts = Chem.MolFromSmarts("[CX3](=O)N")
    # Allowed pattern: a secondary alcohol carbon directly adjacent to a carboxamide;
    # e.g. CH(O)C(=O)N
    allowed_amide_smarts = Chem.MolFromSmarts("[C;X4]([#6])([#6])[H]O[C](=O)N")
    if mol.HasSubstructMatch(carboxamide_smarts) and (not mol.HasSubstructMatch(allowed_amide_smarts)):
        return False, "Contains carboxamide group not adjacent to a secondary alcohol"
    
    # --- STEP 2: IDENTIFY AND EVALUATE ALL -OH GROUPS ---
    total_OH = 0
    secondary_OH = 0
    
    # Iterate over all atoms looking for oxygen atoms that might be in an -OH group.
    for atom in mol.GetAtoms():
        # We only care about oxygen atoms.
        if atom.GetAtomicNum() != 8:
            continue
        
        # In an -OH group (after adding hydrogens), oxygen should have exactly 2 neighbors:
        # one hydrogen and one other atom.
        if atom.GetDegree() != 2:
            continue
        
        neighbors = atom.GetNeighbors()
        h_neighbor = None
        c_neighbor = None
        for nb in neighbors:
            if nb.GetAtomicNum() == 1:
                h_neighbor = nb
            elif nb.GetAtomicNum() == 6:
                c_neighbor = nb
        # If not exactly one hydrogen and one carbon are found, skip this oxygen.
        if h_neighbor is None or c_neighbor is None:
            continue
        
        # We have identified an -OH group.
        total_OH += 1
        
        # Check that the carbon attached to the –OH is sp³.
        if c_neighbor.GetHybridization() != Chem.rdchem.HybridizationType.SP3:
            continue  # This -OH is not on a saturated carbon.
        
        # Now, for a secondary alcohol the attached carbon (excluding the -OH oxygen)
        # should have exactly: 2 carbon neighbors and 1 hydrogen.
        count_carbon = 0
        count_hydrogen = 0
        for nb in c_neighbor.GetNeighbors():
            # Skip the oxygen that defines the -OH group.
            if nb.GetIdx() == atom.GetIdx():
                continue
            if nb.GetAtomicNum() == 6:
                count_carbon += 1
            elif nb.GetAtomicNum() == 1:
                count_hydrogen += 1
            # Other atoms (e.g. heteroatoms) make the substitution pattern deviate from the ideal.
        if count_carbon == 2 and count_hydrogen == 1:
            secondary_OH += 1
            
    if total_OH == 0:
        return False, "No identifiable -OH groups (in proper -OH form) found"
    
    if total_OH == secondary_OH:
        return True, f"All {total_OH} alcohol group(s) are secondary (each -OH is on a sp³ carbon bound to 2 carbons and 1 hydrogen)"
    else:
        return False, (f"Not all identified alcohol groups are secondary "
                       f"(found {secondary_OH} secondary out of {total_OH} total -OH groups)")

# Example usage:
# Uncomment the following lines to test a few examples:
# test_smiles = "CC(O)CC"   # Butan-2-ol, a classical secondary alcohol.
# print(is_secondary_alcohol(test_smiles))


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35681',
                          'name': 'secondary alcohol',
                          'definition': 'A secondary alcohol is a compound in '
                                        'which a hydroxy group, -OH, is '
                                        'attached to a saturated carbon atom '
                                        'which has two other carbon atoms '
                                        'attached to it.',
                          'parents': ['CHEBI:30879'],
                          'xrefs': ['KEGG:C00432', 'KEGG:C01612'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 84,
                           'log_lines_of_code': 4.430816798843313,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 0],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetHybridization',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetDegree',
                                                 'GetNeighbors',
                                                 'C',
                                                 'AddHs'],
                           'methods_called_count': 11,
                           'smarts_strings': [   '[CX3](=O)N',
                                                 'P(=O)(O)(O)',
                                                 '[CX3](=O)[O;H1,-]',
                                                 '[C;X4]([#6])([#6])[H]O[C](=O)N'],
                           'smarts_strings_count': 4,
                           'defs': ['is_secondary_alcohol(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains carboxylic acid or '
                                          'carboxylate group"',
                                          'False, "Contains phosphate group"',
                                          'False, "Contains carboxamide group '
                                          'not adjacent to a secondary '
                                          'alcohol"',
                                          'False, "No identifiable -OH groups '
                                          '(in proper -OH form) found"',
                                          'True, f"All {total_OH} alcohol '
                                          'group(s) are secondary (each -OH is '
                                          'on a sp³ carbon bound to 2 carbons '
                                          'and 1 hydrogen)"',
                                          'False, (f"Not all identified '
                                          'alcohol groups are secondary "'],
                           'returns_count': 7,
                           'complexity': 5.486163359768662},
    'message': '\n'
               'Attempt failed: F1 score of 0.1178800079202693 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]1(C[C@@]2([H])C[C@]3([H])C(=C)[C@H](C[C@H](O)[C@@]3(C)[C@@H](OC(C)=O)[C@H](OC(C)=O)C(=C1C)C2(C)C)OC(C)=O)OC(C)=O '
               'NAME: 7beta-hydroxytaxusin REASON: CORRECT All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: O=C(C(C1=CC(O)C(OC)=C(C1O)OC)C)C NAME: '
               '3-(3,6-dihydroxy-4,5-dimethoxycyclohexa-1,4-dien-1-yl)butan-2-one '
               'REASON: CORRECT All 2 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: CC(C)(C)NCC(O)COc1cccc2NC(=O)CCc12 NAME: carteolol '
               'REASON: CORRECT All 1 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: CCCCCCCCCCCCCCC(O)CCCC NAME: nonadecan-5-ol REASON: '
               'CORRECT All 1 alcohol group(s) are secondary (each -OH is on a '
               'sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'C[C@@H]1[C@@H]2[C@H](C[C@@H](C)[C@@H]3CCC(=O)[C@@]3(C)[C@H]2O)OC1=O '
               'NAME: '
               '(1S,5R,6S,7S,8S,10R,11R)-6-hydroxy-4-oxopseudoguai-12,8-olide '
               'REASON: CORRECT All 1 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)CCCCCCCCCCC NAME: pentacosan-12-ol '
               'REASON: CORRECT All 1 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'C=1(C(C[C@@H](C(C1C)=O)O)(C)C)/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=2C(C[C@@H](CC2C)O)(C)C)\\C)\\C)/C)/C '
               'NAME: adonixanthin REASON: CORRECT All 2 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(C)[C@]([H])(CC[C@]45OC(=O)[C@@]6(CCC(=C)[C@@H](C)[C@@]46[H])CC[C@@]35C)[C@@]1(C)CC[C@H](O)C2(C)C '
               'NAME: hyperinol A REASON: CORRECT All 1 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)C(=CC[C@@]34[H])[C@H](C)N(C)C)[C@@]1(C)CC[C@H](NC(=O)C=C(C)C)[C@@H]2O '
               'NAME: hookerianamide J REASON: CORRECT All 1 alcohol group(s) '
               'are secondary (each -OH is on a sp³ carbon bound to 2 carbons '
               'and 1 hydrogen)\n'
               ' * SMILES: COc1ccc(OC)c(c1)C(O)CN NAME: deglymidodrine REASON: '
               'CORRECT All 1 alcohol group(s) are secondary (each -OH is on a '
               'sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)C(=CC[C@@]21[H])C(C)=O '
               'NAME: 16,17-didehydropregnenolone REASON: CORRECT All 1 '
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: CC(=O)C(=O)[C@@H](O)COP(O)(O)=O NAME: '
               '(2S)-2-hydroxy-3,4-diketopentyl phosphate REASON: CORRECT All '
               '1 alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'O[C@@H](CCCCCCCCCCC\\C=C/CCCCCCCCC\\C=C\\[C@@H](O)C#C)\\C=C/C#C '
               'NAME: (-)-duryne F REASON: CORRECT All 2 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               '[H][C@]12OC(=O)C(=C)[C@]1([H])[C@H](C[C@@](C)(OC(C)=O)C(=O)CC[C@H](C)[C@@H]2O)OC(=O)C(C)=C '
               'NAME: lychnostatin 1 REASON: CORRECT All 1 alcohol group(s) '
               'are secondary (each -OH is on a sp³ carbon bound to 2 carbons '
               'and 1 hydrogen)\n'
               ' * SMILES: CCCCCCCCCCCCC(O)CCCCCCCCCCCC NAME: pentacosan-13-ol '
               'REASON: CORRECT All 1 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)N[C@H](CN1CCOCC1)[C@H](O)c1ccccc1 NAME: '
               '(1R,2R)-1-phenyl-2-palmitoylamino-3-morpholino-1-propanol '
               'REASON: CORRECT All 1 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]3([H])[C@@H](O)[C@H](O)[C@]4(C)OC[C@@]13[C@@]4([H])[C@@H](OC(=O)[C@H](C)CC)C(=O)O2 '
               'NAME: simalikalactone D REASON: CORRECT All 3 alcohol group(s) '
               'are secondary (each -OH is on a sp³ carbon bound to 2 carbons '
               'and 1 hydrogen)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)[C@@H](C)[C@@H]1CC3 '
               'NAME: 4alpha-methyl-5alpha-cholest-8-en-3beta-ol REASON: '
               'CORRECT All 1 alcohol group(s) are secondary (each -OH is on a '
               'sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'COc1cc2[C@H](OC(C)=O)[C@@H](C)[C@@H](C)[C@@H](O)c3cc4OCOc4c(OC)c3-c2c(OC)c1OC '
               'NAME: ananolignan E REASON: CORRECT All 1 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: CCCCCCCC(O)CCC NAME: undecan-4-ol REASON: CORRECT '
               'All 1 alcohol group(s) are secondary (each -OH is on a sp³ '
               'carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: CC(O)C(N)=O NAME: lactamide REASON: CORRECT All 1 '
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'O[C@H](\\C=C\\CCCCCCCCC\\C=C/CCCCCCCCC\\C=C\\[C@@H](O)C#C)C#C '
               'NAME: (-)-duryne REASON: CORRECT All 2 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               'CS([O-])(=O)=O.Cc1ccc(cc1)C(=O)Oc1ccc(cc1OC(=O)c1ccc(C)cc1)C(O)C[NH2+]C(C)(C)C '
               'NAME: bitolterol mesylate REASON: CORRECT All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'CC1=C(CC[C@H]2C(=C)CC[C@H]3C(C)(C)[C@@H](O)CC[C@]23C)[C@@]2(C)CCC(=O)C(C)(C)[C@@H]2CC1=O '
               'NAME: lamesticumin C REASON: CORRECT All 1 alcohol group(s) '
               'are secondary (each -OH is on a sp³ carbon bound to 2 carbons '
               'and 1 hydrogen)\n'
               ' * SMILES: CCCCCCCCCCCCCCC(O)CCCCCCCCC NAME: tetracosan-10-ol '
               'REASON: CORRECT All 1 alcohol group(s) are secondary (each -OH '
               'is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               'False positives: SMILES: CCCCCCCCCCCCCCCCCCC(O)C([O-])=O NAME: '
               '2-hydroxyarachidate REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               '[C@H]1(N2C=CC(=O)NC2=O)[C@@H]([C@@H]([C@@]([C@H](C(N)=O)O)(O1)[H])O)O '
               "NAME: uridine-5'-carboxamide REASON: WRONGLY CLASSIFIED All 3 "
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'COC1=CC=CC=C1CNC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC=C(C=C4)F)O '
               'NAME: '
               '(3R,6aS,8S,10aS)-N-(4-fluorophenyl)-3-hydroxy-8-[2-[(2-methoxyphenyl)methylamino]-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED All 1 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               'C1CCC(CC1)CN2C[C@H](COC[C@@H]3[C@@H]2CC[C@@H](O3)CC(=O)NCC4=CC=C(C=C4)F)O '
               'NAME: '
               '2-[(3R,6aS,8R,10aS)-1-(cyclohexylmethyl)-3-hydroxy-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[(4-fluorophenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED All 1 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: [O-]C(=O)CCCCCCCCC(CCCCCCCC)O NAME: '
               '10-hydroxyoctadecanoate REASON: WRONGLY CLASSIFIED All 1 '
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'C(C(CC([O-])=O)OC(=O)C[C@@H](CCCCCCC/C=C\\C/C=C\\CCCCC)O)[N+](C)(C)C '
               'NAME: O-[(3R,11Z,14Z)-3-hydroxyicosadienoyl]carnitine REASON: '
               'WRONGLY CLASSIFIED All 1 alcohol group(s) are secondary (each '
               '-OH is on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'C1[C@H]2[C@@H]([C@@H]([C@H](O2)N3C4=C(C(=NC=N4)N)N=C3SC5=CC=C(C=C5)Cl)O)OP(=O)(O1)O '
               'NAME: '
               '(4aS,6S,7S,7aR)-6-[6-amino-8-[(4-chlorophenyl)thio]-9-purinyl]-2-hydroxy-2-oxo-4a,6,7,7a-tetrahydro-4H-furo[3,2-d][1,3,2]dioxaphosphorin-7-ol '
               'REASON: WRONGLY CLASSIFIED All 1 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               '[C@]1([C@@H](CCC(C(C)C)CC)C)([C@]2(CC[C@@]3([C@]4(CC[C@@H](C[C@]4(CC[C@]3([C@@]2(CC1)[H])[H])[H])O)C)[H])C)[H] '
               'NAME: 24-ethylcoprostanol REASON: WRONGLY CLASSIFIED All 1 '
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(=O)OC(=O)CCCC[C@@H]2CCSS2)[C@@H](O)[C@H]1O '
               'NAME: (R)-lipoyl-GMP REASON: WRONGLY CLASSIFIED All 2 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@H]23)C[C@@H]1O '
               'NAME: 2alpha-Methyl-5alpha-androstane-3alpha,17beta-diol '
               'REASON: WRONGLY CLASSIFIED All 2 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (9Z,12Z,15Z,18Z,21Z)-3-oxotetracosapentaenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED All 2 alcohol group(s) are '
               'secondary (each -OH is on a sp³ carbon bound to 2 carbons and '
               '1 hydrogen)\n'
               ' * SMILES: '
               'CCCC\\C=C/CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: cis-3-octenoyl-CoA REASON: WRONGLY CLASSIFIED All 2 '
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: O=C[C@H](N)[C@@H](O)[C@@H](O)[C@H](O)C NAME: '
               'D-fucosamin REASON: WRONGLY CLASSIFIED All 3 alcohol group(s) '
               'are secondary (each -OH is on a sp³ carbon bound to 2 carbons '
               'and 1 hydrogen)\n'
               ' * SMILES: '
               'C([C@](COC(CCCCCCCCCCC/C=C\\CCCCCCCC)=O)([H])O)OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: LysoPC(22:1(13Z)) REASON: WRONGLY CLASSIFIED All 1 '
               'alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: CCCCCCCC[C@@H](O)[C@@H](O)CCCCCCCC([O-])=O NAME: '
               '(9S,10R)-dihydroxyoctadecanoate REASON: WRONGLY CLASSIFIED All '
               '2 alcohol group(s) are secondary (each -OH is on a sp³ carbon '
               'bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               '[C@@H]1(O[C@@H]2[C@H](C(=O)[C@H](C(O[C@@H]([C@@]3([C@H](NC(=O)O3)[C@H](C(=O)[C@H](C)C[C@]2(OCC(=C(C4=CC5=C(N=C4)C=CC=C5)[H])[H])C)C)C)CC)=O)C)C)O[C@@H](C[C@@H]([C@H]1O)N(C)C)C '
               'NAME: cethromycin REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)C(O)C1O)(OCC(OC(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PI 38:3 REASON: WRONGLY CLASSIFIED All 5 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@@](C1(C)C)(CC[C@]3([C@]2(C(=O)C4=C([C@@H]3OC(=O)C)C(=O)[C@H]([C@@H]4O)C)C)C)[H])[H] '
               'NAME: Euphoractine W from S.guyanensis REASON: WRONGLY '
               'CLASSIFIED All 2 alcohol group(s) are secondary (each -OH is '
               'on a sp³ carbon bound to 2 carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'O=C1C2=C(O[C@@]3(CC[C@H]([C@@H]3C2)C(=C)C)C)[C@@H](OC)C[C@@H]1O '
               'NAME: Guignardone D REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC(O)/C=C/C=O)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: OHOOA-PA REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: CS(=O)(=O)OC[C@H](O)[C@@H](O)COS(C)(=O)=O NAME: '
               'Treosulfan REASON: WRONGLY CLASSIFIED All 2 alcohol group(s) '
               'are secondary (each -OH is on a sp³ carbon bound to 2 carbons '
               'and 1 hydrogen)\n'
               ' * SMILES: '
               'CC\\C=C\\C=C(/OC)C(O)C(C)CC(OC)\\C=C\\C=C\\C1OC(=O)C=CC1OC '
               'NAME: Pterocidin REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: O=C1C(=C(CCC)O[C@@]1(/C=C/C=C/[C@@H](O)C)C)C(=O)OC '
               'NAME: Gregatin G2 REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'O1C(CCC1C(O)CCCCCCCCCCCC)C(O)CCCCCC(O)CCCCC2OC(=O)C(C2)CC(=O)C '
               'NAME: Isoannoreticuin REASON: WRONGLY CLASSIFIED All 3 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               ' * SMILES: '
               'O1[C@]23[C@@]([C@@]4([C@@](OC5=C(C4)C(OC)=C6C(=C5C)COC6=O)(C[C@H]2O)C)[H])([C@H](OC(=O)C)C[C@@]1(OC3(C)C)OC)C '
               'NAME: Austalide D REASON: WRONGLY CLASSIFIED All 1 alcohol '
               'group(s) are secondary (each -OH is on a sp³ carbon bound to 2 '
               'carbons and 1 hydrogen)\n'
               'False negatives: SMILES: '
               'C(C(O)=O)C/C=C\\C[C@H](\\C=C\\C=C/C=C/C=C/[C@H]([C@@H](C/C=C\\CC)O)O)O '
               'NAME: aspirin-triggered resolvin D2 REASON: MISSED Not all '
               'identified alcohol groups are secondary (found 3 secondary out '
               'of 4 total -OH groups)\n'
               ' * SMILES: '
               'CC(C)=CCc1c(O)c(CC(O)C(C)=C)c2occ(-c3ccc(O)c(O)c3)c(=O)c2c1O '
               'NAME: millewanin H REASON: MISSED Not all identified alcohol '
               'groups are secondary (found 1 secondary out of 5 total -OH '
               'groups)\n'
               ' * SMILES: '
               '[C@@]123O[C@]([C@H](C)CC1(C)C)(CC(O[C@@]([C@@H](C)O)(CC(OC(C2)[C@H](C)[C@](O3)([C@H](CC[C@@H](C=4C(=CC=C(C4)O)Br)OC)C)[H])=O)[H])=O)O '
               'NAME: aplysiatoxin REASON: MISSED Not all identified alcohol '
               'groups are secondary (found 1 secondary out of 3 total -OH '
               'groups)\n'
               ' * SMILES: '
               'CC(C)[C@@H](C)\\C=C\\[C@@H](C)[C@H]1CC[C@H]2C3=C[C@@H](O)[C@@]4(O)C[C@@H](O)CC[C@]4(C)[C@@]3(O)CC[C@]12C '
               'NAME: '
               '(22E,24R)-ergosta-7,22-diene-3beta,5alpha,6beta,9alpha-tetrol '
               'REASON: MISSED Not all identified alcohol groups are secondary '
               '(found 2 secondary out of 4 total -OH groups)\n'
               ' * SMILES: [H][C@@]12CCC(C)=CC[C@@]1(C)C[C@H](O)[C@@]2(O)C(C)C '
               'NAME: CAF-603 REASON: MISSED Not all identified alcohol groups '
               'are secondary (found 1 secondary out of 2 total -OH groups)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])CC[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCCC(C)CO '
               'NAME: 5beta-cholestane-3alpha,7alpha,26-triol REASON: MISSED '
               'Not all identified alcohol groups are secondary (found 2 '
               'secondary out of 3 total -OH groups)\n'
               ' * SMILES: '
               '[C@]12([C@]3([C@]([H])([C@@H](C[C@]2([H])[C@@]4([C@@]([H])([C@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)CO)C([C@H](CC4)O)(C)C)C)O)[C@]([H])(CC3)[C@](CCC=C(C)C)(O)C)C)C '
               'NAME: (20S)-ginsenoside Rh1 REASON: MISSED Not all identified '
               'alcohol groups are secondary (found 5 secondary out of 7 total '
               '-OH groups)\n'
               ' * SMILES: O[C@@H](CC\\C=C\\c1ccc(O)cc1)CCc1ccc(O)c(O)c1 NAME: '
               '(-)-(3S)-1-(3,4-dihydroxyphenyl)-7-(4-hydroxyphenyl)-(6E)-6-hepten-3-ol '
               'REASON: MISSED Not all identified alcohol groups are secondary '
               '(found 1 secondary out of 4 total -OH groups)\n'
               ' * SMILES: '
               'C(/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)=C\\[C@H]([C@H](CCCC(O)=O)O)O '
               'NAME: '
               '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoic '
               'acid REASON: MISSED Not all identified alcohol groups are '
               'secondary (found 2 secondary out of 3 total -OH groups)\n'
               ' * SMILES: O[C@@H]1[C@H](Oc2cc(O)cc(O)c2C1=O)c1ccc(O)c(O)c1 '
               'NAME: (+)-taxifolin REASON: MISSED Not all identified alcohol '
               'groups are secondary (found 1 secondary out of 5 total -OH '
               'groups)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Contains carboxamide group not '
                                               'adjacent to a secondary '
                                               'alcohol'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Contains carboxylic acid or '
                                               'carboxylate group'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Contains carboxamide group not '
                                               'adjacent to a secondary '
                                               'alcohol'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No identifiable -OH groups (in '
                                               'proper -OH form) found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Not all identified alcohol '
                                               'groups are secondary (found 10 '
                                               'secondary out of 14 total -OH '
                                               'groups)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Contains carboxylic acid or '
                                               'carboxylate group'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Contains carboxamide group not '
                                               'adjacent to a secondary '
                                               'alcohol'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Contains carboxamide group not '
                                               'adjacent to a secondary '
                                               'alcohol'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No identifiable -OH groups (in '
                                               'proper -OH form) found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No identifiable -OH groups (in '
                                               'proper -OH form) found'}],
    'sample_false_negatives': [   {   'smiles': 'C(C(O)=O)C/C=C\\C[C@H](\\C=C\\C=C/C=C/C=C/[C@H]([C@@H](C/C=C\\CC)O)O)O',
                                      'name': 'aspirin-triggered resolvin D2',
                                      'reason': 'Contains carboxylic acid or '
                                                'carboxylate group'},
                                  {   'smiles': 'CC(C)=CCc1c(O)c(CC(O)C(C)=C)c2occ(-c3ccc(O)c(O)c3)c(=O)c2c1O',
                                      'name': 'millewanin H',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 1 '
                                                'secondary out of 5 total -OH '
                                                'groups)'},
                                  {   'smiles': '[C@@]123O[C@]([C@H](C)CC1(C)C)(CC(O[C@@]([C@@H](C)O)(CC(OC(C2)[C@H](C)[C@](O3)([C@H](CC[C@@H](C=4C(=CC=C(C4)O)Br)OC)C)[H])=O)[H])=O)O',
                                      'name': 'aplysiatoxin',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 1 '
                                                'secondary out of 3 total -OH '
                                                'groups)'},
                                  {   'smiles': 'CC(C)(C)NCC(O)COc1cccc2NC(=O)CCc12',
                                      'name': 'carteolol',
                                      'reason': 'Contains carboxamide group '
                                                'not adjacent to a secondary '
                                                'alcohol'},
                                  {   'smiles': 'CC(C)[C@@H](C)\\C=C\\[C@@H](C)[C@H]1CC[C@H]2C3=C[C@@H](O)[C@@]4(O)C[C@@H](O)CC[C@]4(C)[C@@]3(O)CC[C@]12C',
                                      'name': '(22E,24R)-ergosta-7,22-diene-3beta,5alpha,6beta,9alpha-tetrol',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 2 '
                                                'secondary out of 4 total -OH '
                                                'groups)'},
                                  {   'smiles': '[H][C@@]12CCC(C)=CC[C@@]1(C)C[C@H](O)[C@@]2(O)C(C)C',
                                      'name': 'CAF-603',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 1 '
                                                'secondary out of 2 total -OH '
                                                'groups)'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])CC[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCCC(C)CO',
                                      'name': '5beta-cholestane-3alpha,7alpha,26-triol',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 2 '
                                                'secondary out of 3 total -OH '
                                                'groups)'},
                                  {   'smiles': '[C@]12([C@]3([C@]([H])([C@@H](C[C@]2([H])[C@@]4([C@@]([H])([C@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)CO)C([C@H](CC4)O)(C)C)C)O)[C@]([H])(CC3)[C@](CCC=C(C)C)(O)C)C)C',
                                      'name': '(20S)-ginsenoside Rh1',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 5 '
                                                'secondary out of 7 total -OH '
                                                'groups)'},
                                  {   'smiles': 'O[C@@H](CC\\C=C\\c1ccc(O)cc1)CCc1ccc(O)c(O)c1',
                                      'name': '(-)-(3S)-1-(3,4-dihydroxyphenyl)-7-(4-hydroxyphenyl)-(6E)-6-hepten-3-ol',
                                      'reason': 'Not all identified alcohol '
                                                'groups are secondary (found 1 '
                                                'secondary out of 4 total -OH '
                                                'groups)'},
                                  {   'smiles': '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)C(=CC[C@@]34[H])[C@H](C)N(C)C)[C@@]1(C)CC[C@H](NC(=O)C=C(C)C)[C@@H]2O',
                                      'name': 'hookerianamide J',
                                      'reason': 'Contains carboxamide group '
                                                'not adjacent to a secondary '
                                                'alcohol'}],
    'attempt': 4,
    'reasoning': 'Below is our updated solution. In our reasoning we noticed '
                 'that many molecules that “passed” the –OH analysis actually '
                 'contained additional functional groups (such as carboxylate '
                 'or phosphate groups or non‐adjacent carboxamides) so '
                 'that—even though every –OH group rendered in the molecule '
                 'was “secondary” by a strict local definition—the molecule '
                 'does not really belong to the secondary alcohol chemical '
                 'class. (For example, “2‐hydroxyarachidate” has a secondary '
                 '–OH group but it is actually a fatty acid; similarly, '
                 '“uridine‐5′‐carboxamide” contains a carboxamide that is not '
                 'immediately adjacent to the –OH group.) \n'
                 '\n'
                 'To improve matters we now (1) add explicit hydrogens and '
                 'iterate over oxygen atoms that formally belong to “–OH” '
                 'groups (i.e. exactly one hydrogen and one carbon neighbor), '
                 '(2) check that each such –OH is attached to a saturated '
                 '(sp³) carbon whose “other” three substituents are exactly '
                 'two carbon atoms and one hydrogen, and (3) we check for '
                 'disqualifying moieties such as carboxylic acid/carboxylate '
                 'and phosphate groups. Also for “carboxamides” we allow only '
                 'those that occur directly on the same carbon as the –OH (as '
                 'in lactamide). Only if at least one –OH is found and every '
                 '–OH meets the secondary pattern and no disqualifying groups '
                 'are present is the molecule considered a secondary '
                 'alcohol. \n'
                 '\n'
                 'Below is the complete Python code:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 809,
    'num_false_positives': 5525,
    'num_true_negatives': 134932,
    'num_false_negatives': 1034,
    'num_negatives': None,
    'precision': 0.12772339753710135,
    'recall': 0.4389582202930005,
    'f1': 0.1978720802250214,
    'accuracy': 0.9539072382290935,
    'negative_predictive_value': 0.9923951576129326}