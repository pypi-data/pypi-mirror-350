"""
Classifies: CHEBI:23053 catechin
"""
"""
Classifies: CHEBI:23053 catechin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_catechin(smiles: str):
    """
    Determines if a molecule is a catechin based on its SMILES string.
    A catechin is a member of the class of hydroxyflavan that has a flavan-3-ol skeleton and its substituted derivatives.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a catechin, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define core structure pattern (flavan-3-ol skeleton)
    # This pattern matches the basic 2-phenylchromane structure with at least one hydroxyl group
    # and allows for various substitutions
    core_pattern = Chem.MolFromSmarts("C1C(O)Cc2c(O)cc(O)cc2O1")
    if not mol.HasSubstructMatch(core_pattern):
        return False, "No flavan-3-ol core structure found"

    # Check for characteristic features
    # 1. At least two aromatic rings (one from flavan, one from phenyl)
    aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    if aromatic_rings < 2:
        return False, f"Found {aromatic_rings} aromatic rings, need at least 2"

    # 2. Check for hydroxyl groups (both free and in substitutions)
    hydroxyl_pattern = Chem.MolFromSmarts("[OH]")
    hydroxyl_matches = len(mol.GetSubstructMatches(hydroxyl_pattern))
    
    # 3. Check for common substitutions
    substitution_patterns = [
        Chem.MolFromSmarts("[OH]c1cc(O)c(O)c(O)c1"),  # Gallate
        Chem.MolFromSmarts("[OH]S(=O)(=O)[OH]"),      # Sulfate
        Chem.MolFromSmarts("C(=O)O"),                 # Ester
        Chem.MolFromSmarts("C(=O)[OH]"),              # Carboxyl
        Chem.MolFromSmarts("C=C"),                    # Double bond
        Chem.MolFromSmarts("C#N"),                    # Nitrile
        Chem.MolFromSmarts("C1OC1"),                  # Epoxide
        Chem.MolFromSmarts("CO"),                     # Methoxy
        Chem.MolFromSmarts("C=O"),                    # Carbonyl
    ]
    
    has_substitution = any(mol.HasSubstructMatch(patt) for patt in substitution_patterns)
    
    # Adjust hydroxyl count requirements based on substitutions
    if has_substitution:
        min_hydroxyl = 2  # Allow fewer hydroxyls if substitutions are present
    else:
        min_hydroxyl = 3  # Basic catechin needs at least 3 hydroxyls

    if hydroxyl_matches < min_hydroxyl:
        return False, f"Found {hydroxyl_matches} hydroxyl groups, need at least {min_hydroxyl}"

    # 4. Check molecular weight range (200-1000 Da typical for catechin derivatives)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200 or mol_wt > 1000:
        return False, f"Molecular weight {mol_wt:.1f} outside typical catechin range"

    # 5. Additional checks for common catechin features
    # Check for at least one aromatic hydroxyl group
    aromatic_oh_pattern = Chem.MolFromSmarts("c[OH]")
    if not mol.HasSubstructMatch(aromatic_oh_pattern):
        return False, "No aromatic hydroxyl groups found"

    return True, "Contains flavan-3-ol core structure with characteristic features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23053',
                          'name': 'catechin',
                          'definition': 'Members of the class of hydroxyflavan '
                                        'that have a flavan-3-ol skeleton and '
                                        'its substituted derivatives.',
                          'parents': ['CHEBI:72010'],
                          'xrefs': ['KEGG:C17590', 'LINCS:LSM-1682'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 57,
                           'log_lines_of_code': 4.04305126783455,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
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
                                                 2,
                                                 0,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'CalcExactMolWt',
                                                 'MolFromSmiles',
                                                 'CalcNumAromaticRings'],
                           'methods_called_count': 6,
                           'smarts_strings': [   '[OH]c1cc(O)c(O)c(O)c1',
                                                 'c[OH]',
                                                 'C(=O)O',
                                                 '[OH]',
                                                 'C1C(O)Cc2c(O)cc(O)cc2O1',
                                                 'C(=O)[OH]',
                                                 '[OH]S(=O)(=O)[OH]',
                                                 'C=O',
                                                 'C#N',
                                                 'C1OC1',
                                                 'CO',
                                                 'C=C'],
                           'smarts_strings_count': 12,
                           'defs': ['is_catechin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No flavan-3-ol core '
                                          'structure found"',
                                          'False, f"Found {aromatic_rings} '
                                          'aromatic rings, need at least 2"',
                                          'False, f"Found {hydroxyl_matches} '
                                          'hydroxyl groups, need at least '
                                          '{min_hydroxyl}"',
                                          'False, f"Molecular weight '
                                          '{mol_wt:.1f} outside typical '
                                          'catechin range"',
                                          'False, "No aromatic hydroxyl groups '
                                          'found"',
                                          'True, "Contains flavan-3-ol core '
                                          'structure with characteristic '
                                          'features"'],
                           'returns_count': 7,
                           'complexity': 4.00861025356691},
    'message': '\n'
               'Attempt failed: F1 score of 0.6127946127946128 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O[C@@H]1Cc2c(O)cc(O)cc2O[C@@H]1c1cc(O)c(O)c(O)c1 NAME: '
               '(-)-epigallocatechin REASON: CORRECT Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'O1C(C(OC(=O)C2=CC(O)=C(O)C(O)=C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(O)C(O)=C4 '
               'NAME: '
               '5,7-Dihydroxy-2-(3,4,5-trihydroxyphenyl)-3,4-dihydro-2H-chromen-3-yl '
               '3,4,5-trihydroxybenzoate REASON: CORRECT Contains flavan-3-ol '
               'core structure with characteristic features\n'
               ' * SMILES: '
               'S([C@@H]1[C@@H](OC(=O)C2=CC(O)=C(O)C(O)=C2)[C@H](OC=3C1=C(O)C=C(O)C3)C4=CC(O)=C(O)C=C4)CCN '
               'NAME: 4beta-(2-Aminoethylthio)epicatechin 3-gallate REASON: '
               'CORRECT Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](OC(=O)C2(O)C(=O)CCC=C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(O)C=C4 '
               'NAME: Catechin '
               '3-O-(1-hydroxy-6-oxo-2-cyclohexene-1-carboxylate) REASON: '
               'CORRECT Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C(C(OC(=O)C2=CC(O)=C(O)C(O)=C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(O)C=C4 '
               'NAME: 3-Galloylcatechin REASON: CORRECT Contains flavan-3-ol '
               'core structure with characteristic features\n'
               ' * SMILES: '
               'O1[C@@]([C@H](O)CC=2C1=CC(O)=CC2O)(C=3C4=CC([C@H]5OC=6C(C[C@@H]5O)=C(O)C=C(O)C6)=CC(=O)C(O)=C4C(O)=C(O)C3)[H] '
               'NAME: Isotheaflavin REASON: CORRECT Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)ccc34)c3cc(O)c(O)c(O)c3)c2O[C@@H]1c1cc(O)c(O)c(O)c1 '
               'NAME: robinetinidol-(4alpha,8)-gallocatechin REASON: CORRECT '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O[C@@H]1Cc2c(O)cc(O)c(C3CCC(=O)N3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: 8-(2-Pyrrolidinone-5-yl)-(-)-epicatechin REASON: CORRECT '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)ccc34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: fisetinidol-(4alpha,8)-catechin REASON: CORRECT Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc3O[C@@H](Cc4c(O)cc(O)cc4O)[C@@H](c3c2O[C@H]1c1ccc(O)c(O)c1)c1ccc(O)c(O)c1 '
               'NAME: Gambiriin B2 REASON: CORRECT Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'COc1cc(\\C=C\\C(=O)O[C@@H]2Cc3c(O)cc(O)cc3O[C@@H]2c2cc(O)c(OC)c(O)c2)ccc1O '
               "NAME: 4'-O-methylepigallocatechin-3-O-ferulate REASON: CORRECT "
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O[C@@H]1c1cc(O)c(O)c(O)c1)cc(O)c([C@H]1[C@H](O)[C@H](Oc3cc(O)ccc13)c1ccc(O)c(O)c1)c2O '
               'NAME: fisetinidol-(4alpha,6)-gallocatechin REASON: CORRECT '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'S(OC=1C=C2O[C@@H]([C@@H](O)CC2=C(O)C1)C3=CC(O)=C(O)C=C3)(O)(=O)=O '
               'NAME: catechin 7-sulfate REASON: CORRECT Contains flavan-3-ol '
               'core structure with characteristic features\n'
               ' * SMILES: '
               'COc1cc(\\C=C\\C(=O)O[C@@H]2Cc3c(O)cc(O)cc3O[C@@H]2c2cc(O)c(O)c(O)c2)ccc1O '
               'NAME: Epigallocatechin-3-O-ferulate REASON: CORRECT Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'O[C@@H]1Cc2c(O)cc3OC(=O)C[C@H](c4ccc(O)c(O)c4)c3c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: Cinchonain 1a REASON: CORRECT Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](OC(=O)C=2C=C(OC)C(O)=C(O)C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(O)C(O)=C4 '
               'NAME: (-)-Epigallocatechin 3-(3-methyl-gallate) REASON: '
               'CORRECT Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C(C(OC(=O)C2=CC(O)=C(O)C(O)=C2)CC=3C1=CC(O)=CC3O)C=4C5=C(C(O)=C(O)C4)C(=O)C(O)=CC(=C5)C(O)=O '
               "NAME: Epitheaflavic acid 3'-gallate REASON: CORRECT Contains "
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O[C@@H]1c1ccc(O)c(O)c1)cc1O[C@H](Cc3c(O)cc(O)cc3O)[C@@H](c1c2O)c1ccc(O)c(O)c1 '
               'NAME: Gambiriin B3 REASON: CORRECT Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'Oc1cc(O)c2C[C@@H](OC(=O)c3cc(O)c(O)c(O)c3)[C@H](Oc2c1)c1ccc(O)c(O)c1 '
               'NAME: (-)-epicatechin-3-O-gallate REASON: CORRECT Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: O1C(C(O)C(=O)C=2C1=CC(O)=CC2O)C=3C=C(OC)C(O)=C(O)C3 '
               'NAME: Hovenitin I REASON: CORRECT Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](OC(=O)C2=CC(O)=C(OC)C(O)=C2)CC=3C1=CC(O)=CC3O)C4=CC(O)=C(OC)C(O)=C4 '
               "NAME: 4'-Methyl-(-)-epigallocatechin 3-(4-methyl-gallate) "
               'REASON: CORRECT Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C(C(O)CC=2C1=CC(OC(=O)C3=CC(O)=C(O)C(O)=C3)=CC2O)C4=CC(O)=C(O)C=C4 '
               'NAME: 7-Galloylcatechin REASON: CORRECT Contains flavan-3-ol '
               'core structure with characteristic features\n'
               ' * SMILES: '
               'C1=C(C=C(C2=C1O[C@@H]([C@@H](C2)OC(\\C=C\\C3=CC=C(C=C3)O)=O)C4=CC(=C(C(=C4)O)O)O)O)O '
               'NAME: Epigallocatechin 3-O-p-coumarate REASON: CORRECT '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O[C@@H]1Cc2c(O)c(C3CCC(=O)N3)c(O)cc2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: 6-(2-Pyrrolidinone-5-yl)-(-)-epicatechin REASON: CORRECT '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'S(OC=1C(O)=CC(C2OC3=C(C(=O)C2O)C(O)=C(O)C(O)=C3)=CC1O)(O)(=O)=O '
               'NAME: '
               '[2,6-dihydroxy-4-(3,5,6,7-tetrahydroxy-4-oxo-3,4-dihydro-2H-1-benzopyran-2-yl)phenyl]oxidanesulfonic '
               'acid REASON: CORRECT Contains flavan-3-ol core structure with '
               'characteristic features\n'
               'False positives: SMILES: '
               'O1[C@@H](OC=2C=3C[C@@H](O)[C@@H](OC3C=C(O)C2)C4=CC(O)=C(O)C=C4)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O '
               'NAME: catechin 5-glucuronide REASON: WRONGLY CLASSIFIED '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: O[C@@H]1[C@H](Oc2cc([O-])cc(O)c2C1=O)c1ccc(O)cc1 '
               'NAME: (+)-dihydrokaempferol 7-oxoanion REASON: WRONGLY '
               'CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C(C(O)C(C=2C=3OC(C(O)CC3C(O)=CC2O)C4=CC(O)=C(O)C=C4)C=5C1=CC(O)=CC5O)C6=CC(O)=C(O)C(O)=C6 '
               'NAME: Epigallocatechin-(4beta->8)-catechin REASON: WRONGLY '
               'CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=C(C(O)=C3C[C@H](O)[C@H](OC3=C2)C4=CC(O)=C(O)C=C4)C/C=C/C5=CC=C(O)C=C5)CO '
               'NAME: Sachaliside 2 REASON: WRONGLY CLASSIFIED Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@](C=2C=3O[C@@H]([C@@H](O)CC3C(O)=CC2O)C4=CC(O)=C(O)C=C4)(C=5C1=CC(O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)=CC5O)[H])C7=CC(O)=C(O)C=C7 '
               'NAME: Procyanidin B3 7-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O1C(OC=2C=C(C3OC=4C(CC3O)=C(O)C=C(O)C4)C=CC2OC)C(O)C(O)C(O)C1C(O)=O '
               'NAME: '
               '3,4,5-trihydroxy-6-[2-methoxy-5-(3,5,7-trihydroxy-3,4-dihydro-2H-1-benzopyran-2-yl)phenoxy]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains flavan-3-ol core '
               'structure with characteristic features\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1CO)C2=C3OC(C(O)CC3=C(O)C(O)=C2O)C4=CC(O)=CC=C4 '
               'NAME: '
               '2-(3-hydroxyphenyl)-8-[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]-3,4-dihydro-2H-1-benzopyran-3,5,6,7-tetrol '
               'REASON: WRONGLY CLASSIFIED Contains flavan-3-ol core structure '
               'with characteristic features\n'
               ' * SMILES: O[C@H]1Cc2c(O)cc(O)cc2O[C@H]1c1cc(O)c(O)c(O)c1 '
               'NAME: (+)-epigallocatechin REASON: WRONGLY CLASSIFIED Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'O1[C@@H](OC=2C=C3O[C@@H]([C@@H](O)CC3=C(O)C2)C4=CC=C(O)C=C4)[C@H](O)[C@](O)(C1)CO '
               'NAME: Afzelechin 7-O-beta-D-apiofuranoside REASON: WRONGLY '
               'CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC=2C(=C3O[C@@H]([C@@H](O)[C@@H](O)C3=C(OC)C2)C4=CC=C(O)C=C4)CC=C(C)C)CO '
               'NAME: 3,4,7-Trihydroxy-5-methoxy-8-prenylflavan '
               '7-O-beta-D-glucopyranoside REASON: WRONGLY CLASSIFIED Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](Oc2cc(O)cc(O)c2[C@H]1c1c(O)cc(O)c2C[C@@H](OC(=O)c3cc(O)c(O)c(O)c3)[C@H](Oc12)c1ccc(O)c(O)c1)c1ccc(O)c(O)c1 '
               "NAME: procyanidin B4 3'-O-gallate REASON: WRONGLY CLASSIFIED "
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O1CC(O)(C2=C(OC)C(=C(OC)C=C2)CC=C(C)C)C(=O)C=3C1=CC(O)=CC3O '
               'NAME: (+)-echinoisoflavanone REASON: WRONGLY CLASSIFIED '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O[C@H]1CO[C@@H](O[C@@H]2[C@H](Oc3cc(O)cc(O)c3C2=O)c2ccc(O)c(O)c2)[C@H](O)[C@H]1O '
               'NAME: (+)-taxifolin 3-O-alpha-L-arabinopyranoside REASON: '
               'WRONGLY CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: O[C@@H]1[C@H](Oc2cc(O)cc(O)c2C1=O)c1ccccc1 NAME: '
               'pinobanksin REASON: WRONGLY CLASSIFIED Contains flavan-3-ol '
               'core structure with characteristic features\n'
               ' * SMILES: '
               'O1C2(OC=3C(C(C2O)C4=C1C=C(O)C5=C4OC(C(O)C5)C6=CC=C(O)C=C6)=C(O)C=C(O)C3)C7=CC=C(O)C=C7 '
               'NAME: '
               "(2S,2''S,3S,3''R,4S)-3,4',5,7-Tetrahydroxyflavan(2->7,4->8)-3,4',5,7-tetrahydroxyflavan "
               'REASON: WRONGLY CLASSIFIED Contains flavan-3-ol core structure '
               'with characteristic features\n'
               ' * SMILES: O1C(C(O)C(=O)C=2C1=CC(OC)=CC2O)C3=CC(O)=C(OC)C=C3 '
               "NAME: 3,3',5-Trihydroxy-4',7-dimethoxyflavanone REASON: "
               'WRONGLY CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'O1C([C@H](O)[C@@H](O)[C@H](O)[C@H]1CO)C=2C=3O[C@@H]([C@H](O)CC3C(O)=CC2O)C4=CC(O)=C(O)C=C4 '
               'NAME: (-)-Epicatechin 8-C-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'COC1=C(C=CC(=C1)C2C(OC3=C(O2)C=C(C=C3)C4C(C(=O)C5=C(C=C(C=C5O4)O)O)O)CO)O '
               'NAME: '
               '3,5,7-trihydroxy-2-[3-(4-hydroxy-3-methoxyphenyl)-2-(hydroxymethyl)-2,3-dihydro-1,4-benzodioxin-6-yl]-3,4-dihydro-2H-1-benzopyran-4-one '
               'REASON: WRONGLY CLASSIFIED Contains flavan-3-ol core structure '
               'with characteristic features\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1CO)C=2C=3OC(C(O)CC3C(O)=CC2O)C4=CC(O)=C(O)C=C4 '
               'NAME: (+)-Catechin 8-C-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains flavan-3-ol core structure with characteristic '
               'features\n'
               ' * SMILES: '
               'O(C1OC[C@@H](O)[C@@H](O)[C@@H]1O)C2C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC=C(O)C=C4 '
               'NAME: Tetrahydoxy-flavanone pentoside REASON: WRONGLY '
               'CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               '[H][C@@]1(Oc2c(C[C@H]1O)c(O)cc1O[C@@]3(Oc4cc(O)cc(O)c4[C@@]([H])([C@H]3O)c21)c1cc(O)c(O)c(O)c1)c1ccc(O)c(O)c1 '
               'NAME: epigallocatechin-(4beta->8,2beta->O-7)-epicatechin '
               'REASON: WRONGLY CLASSIFIED Contains flavan-3-ol core structure '
               'with characteristic features\n'
               ' * SMILES: '
               'O1[C@@H](O[C@H]2[C@H](OC=3C(C2)=C(O)C=C(O)C3)C4=CC(O)=C(O)C=C4)C(O)C(OC(=O)/C=C/C5=CC=CC=C5)[C@H](O)[C@H]1CO '
               'NAME: Epicatechin '
               '3-O-(3-trans-cinnamoyl-beta-D-allopyranoside) REASON: WRONGLY '
               'CLASSIFIED Contains flavan-3-ol core structure with '
               'characteristic features\n'
               ' * SMILES: '
               'S(OC=1C=C2OC(C(O)CC2=C([O-])C1O)C3=CC(OC)=CC=C3)(O)=O NAME: '
               '3,6-dihydroxy-2-(3-methoxyphenyl)-7-(sulfinooxy)-3,4-dihydro-2H-1-benzopyran-5-olate '
               'REASON: WRONGLY CLASSIFIED Contains flavan-3-ol core structure '
               'with characteristic features\n'
               ' * SMILES: '
               'O[C@@H]1Cc2c(O)cc3O[C@@]4(C[C@@H](c5c(O)cc(O)cc5O4)c3c2O[C@@H]1c1ccc(O)cc1)c1ccc(O)cc1 '
               'NAME: mahuannin D REASON: WRONGLY CLASSIFIED Contains '
               'flavan-3-ol core structure with characteristic features\n'
               ' * SMILES: '
               'C1=2C(C([C@@]3([C@](O1)(C=4C(O3)=CC(=CC4)O)CC=C(C)C)O)=O)=C(C5=C(C2)OC(C=C5)(C)C)O '
               'NAME: Sanggenon A REASON: WRONGLY CLASSIFIED Contains '
               'flavan-3-ol core structure with characteristic features\n'
               'False negatives: SMILES: '
               'O[C@H]1Cc2ccc(O)cc2O[C@@H]1c1ccc(O)c(O)c1 NAME: fisetinidol '
               'REASON: MISSED No flavan-3-ol core structure found\n'
               ' * SMILES: '
               'O1[C@@]([C@H](OC(=O)C2=CC(O)=C(O)C(O)=C2)CC=3C1=CC(O)=CC3O)(C=4C(C=5C([C@H]6OC=7C(C[C@H]6OC(=O)C8=CC(O)=C(O)C(O)=C8)=C(O)C=C(O)C7)=CC(O)=C(O)C5)=C(O)C(O)=C(O)C4)[H] '
               'NAME: Theasinensin F REASON: MISSED Molecular weight 898.2 '
               'outside typical catechin range\n'
               ' * SMILES: S(O)(=O)C=1C=2CC(O)C(OC2C=C(O)C1)C3=CC(OC)=C(O)C=C3 '
               "NAME: 3'-O-methyl-(-)-epicatechin-5-O-sulphate REASON: MISSED "
               'No flavan-3-ol core structure found\n'
               ' * SMILES: O1C(C(O)CC2=C1C=C(OC)C=C2OC)C3=CC(O)=C(OC)C=C3 '
               "NAME: 3,3'-Dihydroxy-4',5,7-trimethoxyflavan REASON: MISSED "
               'Found 2 hydroxyl groups, need at least 3\n'
               ' * SMILES: O1C(C(O)CC2=C1C=C(OC)C=C2OC)C3=CC=4OCOC4C=C3 NAME: '
               "3',4'-Methylenedioxy-5,7-dimethylepicatechin REASON: MISSED "
               'Found 1 hydroxyl groups, need at least 3\n'
               ' * SMILES: '
               'O1C(C(OC(=O)C2=CC(O)=C(O)C(O)=C2)CC3=C1C(C(C(OC(=O)C4=CC(O)=C(O)C(O)=C4)CC5=C(O)C=C(O)C=C5O)C6=CC(O)=C(O)C(O)=C6)=C(O)C=C3O)C7=CC(O)=C(O)C(O)=C7 '
               'NAME: '
               '1-[5,7-Dihydroxy-3-(3,4,5-trihydroxybenzoyloxy)-2-(3,4,5-trihydroxyphenyl)-3,4-dihydro-2H-1-benzopyran-8-yl]-3-(2,4,6-trihydroxyphenyl)-1-(3,4,5-trihydroxyphenyl)propan-2-yl '
               '3,4,5-trihydroxybenzoate REASON: MISSED Molecular weight 916.2 '
               'outside typical catechin range\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)CC2=C1C3=C(OC(=O)C=C3)C=C2O)C4=CC(O)=C(O)C=C4 '
               'NAME: Phyllocoumarin REASON: MISSED No flavan-3-ol core '
               'structure found\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)CC2=C1C=C(OC)C=C2OC)C3=CC(O)=C(OC)C=C3 NAME: '
               "Catechin 5,7,4'-trimethyl ether REASON: MISSED Found 2 "
               'hydroxyl groups, need at least 3\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](O)CC2=C1C=C(OC)C=C2OC)C3=CC=4OCOC4C=C3 NAME: '
               "3',4'-Methylenedioxy epicatechin 5,7-dimethyl ether REASON: "
               'MISSED Found 1 hydroxyl groups, need at least 3\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](OC(=O)C2=CC(OC(=O)C)=C(OC(=O)C)C(OC(=O)C)=C2)CC3=C1C=C(OC(=O)C)C=C3OC(=O)C)C4=CC(OC(=O)C)=C(OC(=O)C)C(OC(=O)C)=C4 '
               'NAME: EGCG Octaacetate REASON: MISSED Found 0 hydroxyl groups, '
               'need at least 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1N(C(=O)[C@@H](NC(=O)[C@H](NC(=O)C/C=C/[C@H]2O[C@H]2C(=O)CC(C)C)CN(C)C)C(C)C)[C@@H](CC(C)C)C(=C1C)O',
                                     'name': 'Sandarazol B',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'ClC1=CC=C(C=2OC(COC(C)(C)C(O)=O)=C(N2)C)C=C1',
                                     'name': 'romazarit',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N1C=NC2=C1N=CN=C2N',
                                     'name': '(5Z,8Z,11Z,14Z,17Z)-icosapentaenoyl-CoA(4-)',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'C[C@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)NC3CCCCC3)C(=O)N(C[C@@H]1OC)C)C)C',
                                     'name': '1-cyclohexyl-3-[(4R,7S,8R)-8-methoxy-4,5,7,10-tetramethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]urea',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C3=CC=CS3)[C@H](C)CO)C)CN(C)C(=O)NC4=CC=CC5=CC=CC=C54',
                                     'name': '1-[[(3S,9S,10S)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-16-(thiophen-2-ylsulfonylamino)-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-1-methyl-3-(1-naphthalenyl)urea',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'P(OC[C@@H](COC(CCCCCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCCCCC)=O)(=O)(OCC[NH3+])[O-]',
                                     'name': '1,2-diheptadecanoyl-sn-glycero-3-phosphoethanolamine '
                                             'zwitterion',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'O=C1N(C(CC1)C(O)=O)CCC(N)C(O)=O',
                                     'name': "(2S,3'S)-alpha-Amino-2-carboxy-5-oxo-1-pyrrolidinebutanoic "
                                             'acid',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'CC(=O)[C@@H](O)[C@H](O)CC(=O)C([O-])=O',
                                     'name': '3,7-dideoxy-D-threo-hepto-2,6-diuolosonate',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H]1OC[C@H]4O[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4O)CO',
                                     'name': 'N-[(2S,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxymethyl]-2,5-dihydroxy-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-3-yl]acetamide',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'},
                                 {   'smiles': 'COC(=O)C1=CC=CC=C1NC(=O)NC2=NC=C(C=C2)Cl',
                                     'name': '2-[[[(5-chloro-2-pyridinyl)amino]-oxomethyl]amino]benzoic '
                                             'acid methyl ester',
                                     'reason': 'No flavan-3-ol core structure '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@H]1Cc2ccc(O)cc2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'fisetinidol',
                                      'reason': 'No flavan-3-ol core structure '
                                                'found'},
                                  {   'smiles': 'S(O)(=O)C=1C=2CC(O)C(OC2C=C(O)C1)C3=CC(OC)=C(O)C=C3',
                                      'name': "3'-O-methyl-(-)-epicatechin-5-O-sulphate",
                                      'reason': 'No flavan-3-ol core structure '
                                                'found'},
                                  {   'smiles': 'O1C(C(O)CC2=C1C=C(OC)C=C2OC)C3=CC=4OCOC4C=C3',
                                      'name': "3',4'-Methylenedioxy-5,7-dimethylepicatechin",
                                      'reason': 'Found 1 hydroxyl groups, need '
                                                'at least 2'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)CC2=C1C3=C(OC(=O)C=C3)C=C2O)C4=CC(O)=C(O)C=C4',
                                      'name': 'Phyllocoumarin',
                                      'reason': 'No flavan-3-ol core structure '
                                                'found'},
                                  {   'smiles': 'O1[C@@H]([C@H](O)CC2=C1C=C(OC)C=C2OC)C3=CC=4OCOC4C=C3',
                                      'name': "3',4'-Methylenedioxy "
                                              'epicatechin 5,7-dimethyl ether',
                                      'reason': 'Found 1 hydroxyl groups, need '
                                                'at least 2'},
                                  {   'smiles': 'O1[C@@H]([C@H](OC(=O)C2=CC(OC(=O)C)=C(OC(=O)C)C(OC(=O)C)=C2)CC3=C1C=C(OC(=O)C)C=C3OC(=O)C)C4=CC(OC(=O)C)=C(OC(=O)C)C(OC(=O)C)=C4',
                                      'name': 'EGCG Octaacetate',
                                      'reason': 'Found 0 hydroxyl groups, need '
                                                'at least 2'},
                                  {   'smiles': 'COC1=C(C=C(C=C1)[C@@H]2[C@H](CC3=C(O2)C(=C(C=C3OC)OC)I)O)OC',
                                      'name': '(2R,3S)-2-(3,4-dimethoxyphenyl)-8-iodo-5,7-dimethoxy-3,4-dihydro-2H-1-benzopyran-3-ol',
                                      'reason': 'Found 1 hydroxyl groups, need '
                                                'at least 2'},
                                  {   'smiles': 'COC1=C(C=C(C=C1)[C@@H]2[C@H](CC3=C(C=C(C=C3O2)OC)OC)O)OC',
                                      'name': '(2R,3S)-2-(3,4-dimethoxyphenyl)-5,7-dimethoxy-3,4-dihydro-2H-1-benzopyran-3-ol',
                                      'reason': 'Found 1 hydroxyl groups, need '
                                                'at least 2'}],
    'attempt': 5,
    'reasoning': 'The previous code had several issues that led to both false '
                 'positives and false negatives:\n'
                 '\n'
                 '1. **Core Structure Matching**: The core pattern was too '
                 'restrictive, especially with stereochemistry. Many valid '
                 "catechin derivatives were missed because they didn't match "
                 'the exact stereochemistry pattern.\n'
                 '\n'
                 '2. **Hydroxyl Group Counting**: The requirement for hydroxyl '
                 'groups was too rigid. Some catechin derivatives with fewer '
                 'hydroxyl groups but other characteristic features were '
                 'incorrectly classified.\n'
                 '\n'
                 '3. **Molecular Weight Range**: The molecular weight range '
                 '(200-800 Da) was too narrow. Some larger catechin '
                 'derivatives were incorrectly classified as non-catechins.\n'
                 '\n'
                 '4. **Substitution Patterns**: The substitution patterns were '
                 'not comprehensive enough, leading to some valid catechin '
                 'derivatives being missed.\n'
                 '\n'
                 'To improve the classification, we need to:\n'
                 '- Relax the core structure matching to account for various '
                 'stereochemistry and substitution patterns.\n'
                 '- Adjust the hydroxyl group counting to be more flexible.\n'
                 '- Broaden the molecular weight range.\n'
                 '- Include more comprehensive substitution patterns.\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 98,
    'num_false_positives': 100,
    'num_true_negatives': 57095,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.494949494949495,
    'recall': 0.9245283018867925,
    'f1': 0.6447368421052632,
    'accuracy': 0.9981152161393344,
    'negative_predictive_value': 0.9998599022818416}