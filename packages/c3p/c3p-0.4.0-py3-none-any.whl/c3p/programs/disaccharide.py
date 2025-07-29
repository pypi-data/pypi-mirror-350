"""
Classifies: CHEBI:36233 disaccharide
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_disaccharide(smiles: str):
    """
    Determines if a molecule is a disaccharide based on its SMILES string.
    A disaccharide is defined as two monosaccharides joined by a glycosidic bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a disaccharide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for exactly two rings, as disaccharides should typically consist of two sugar rings
    if rdMolDescriptors.CalcNumRings(mol) != 2:
        return False, "Requires exactly two ring structures typical in disaccharides"
        
    # Define a glycosidic bond pattern - oxygen linking two anomeric carbons
    glycosidic_pattern = Chem.MolFromSmarts("O[C;R][C;R]")
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "No clear glycosidic bond pattern found"

    # Count typical atoms: carbon, oxygen; allow for substitutions
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)

    # Adjust carbon and oxygen limits slightly to account for common substituents in natural products
    if carbon_count < 10 or carbon_count > 30:
        return False, f"Unexpected number of carbons: {carbon_count} for disaccharide"
    if oxygen_count < 6 or oxygen_count > 18:
        return False, f"Unexpected number of oxygens: {oxygen_count} for disaccharide"

    # Check for sugar features: minimum number of hydroxyl groups for typical sugars
    if len(mol.GetSubstructMatches(Chem.MolFromSmarts("[OX2H]"))) < 6:
        return False, "Too few hydroxyl groups for a sugar-like structure"

    return True, "Contains features characteristic of disaccharides: two sugar units linked by a glycosidic bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36233',
                          'name': 'disaccharide',
                          'definition': 'A compound in which two '
                                        'monosaccharides are joined by a '
                                        'glycosidic bond.',
                          'parents': ['CHEBI:50699'],
                          'xrefs': ['KEGG:C01911'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 32,
                           'log_lines_of_code': 3.4657359027997265,
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
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetAtomicNum',
                                                 'CalcNumRings',
                                                 'GetAtoms',
                                                 'HasSubstructMatch',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 7,
                           'smarts_strings': ['"[OX2H]"))', 'O[C;R][C;R]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_disaccharide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Requires exactly two ring '
                                          'structures typical in '
                                          'disaccharides"',
                                          'False, "No clear glycosidic bond '
                                          'pattern found"',
                                          'False, f"Unexpected number of '
                                          'carbons: {carbon_count} for '
                                          'disaccharide"',
                                          'False, f"Unexpected number of '
                                          'oxygens: {oxygen_count} for '
                                          'disaccharide"',
                                          'False, "Too few hydroxyl groups for '
                                          'a sugar-like structure"',
                                          'True, "Contains features '
                                          'characteristic of disaccharides: '
                                          'two sugar units linked by a '
                                          'glycosidic bond"'],
                           'returns_count': 7,
                           'complexity': 4.093147180559945},
    'message': '\n'
               'Attempt failed: F1 score of 0.07456025203465477 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: alpha-D-Glcp-(1->6)-alpha-D-Galp REASON: CORRECT '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@H](OC[C@H]2O[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@@H](O)[C@H](O)[C@H]1CO '
               'NAME: alpha-D-Manp-(1->6)-beta-D-Galp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O[C@@H]2[C@@H](CO)O[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: alpha-maltose REASON: CORRECT Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O[C@@H]1CO[C@@H](O[C@@H]2COC(O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O '
               'NAME: xylobiose REASON: CORRECT Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: '
               'S(O)(N[C@@H]1[C@@H](O)[C@H](O[C@H]2OC(=C(O)[C@H](O)[C@H]2O)C(O)=O)[C@H](O[C@H]1O)CO)(=O)=O '
               'NAME: beta-L-threo-hex-4-enopyranuronosyl-(1->4)-beta-D-GlcpNS '
               'REASON: CORRECT Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)CO[C@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C '
               'NAME: beta-L-Fucp-(1->6)-alpha-D-Glcp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](OC[C@H]2O[C@@H](O)[C@@H](O)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O '
               'NAME: alpha-D-Manp-(1->6)-beta-D-Manp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](OC(O)[C@H]1O)C)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Glcp-(1->3)-L-Fucp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O[C@@H](O)[C@@H]1O)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Galp-(1->3)-alpha-L-Araf REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2O)CO)[C@@H](O)[C@@H](O)[C@@H]1O)(O)(=O)O '
               'NAME: alpha-D-Manp6P-(1->2)-alpha-D-Manp REASON: CORRECT '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@@H](O)[C@H](O[C@H]1O)CO)[C@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C '
               'NAME: beta-L-Fucp-(1->2)-beta-D-Galp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)[C@@H]2[C@@H](O)[C@@H](OC[C@H]2O)O '
               'NAME: beta-D-Glcp-(1->3)-beta-D-Xylp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](OC(O)[C@@H]1O)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Galp-(1->3)-D-Galp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O[C@H]2OC[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: alpha-D-Glcp-(1<->1)-alpha-D-Xylp REASON: CORRECT '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O)C(O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO '
               'NAME: beta-D-Manp-(1->4)-D-Galp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](O)[C@@H](O)CO[C@H]1OC[C@H]2O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]2O '
               'NAME: alpha-L-Arap-(1->6)-beta-D-Glcp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1N)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: 2-amino-2-deoxy-beta-D-glucopyranosyl '
               'beta-D-galactopyranoside REASON: CORRECT Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H](O)[C@@H]1O)CO)[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: alpha-D-Glcp-(1->3)-beta-D-Galp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               '[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)OC)O)OC)O)OC '
               "NAME: 1,3,3'-tri-O-methyl-4alpha-mannobiose REASON: CORRECT "
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@@](CO)(C[C@@H](O)[C@H]1O)O[C@@H]1C[C@@](O)(O[C@]([H])([C@H](O)CO)[C@@H]1O)C(O)=O)[C@H](O)CO '
               'NAME: alpha-Kdo-CH2OH-(2->4)-alpha-Kdo REASON: CORRECT '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)[C@@H]2[C@H](O)[C@@H](O)[C@@H](OC2)O '
               'NAME: beta-D-Glcp-(1->4)-alpha-L-Arap REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](OC[C@H]2O[C@@](O)(CO)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: 6-O-alpha-D-glucopyranosyl-alpha-D-fructofuranose '
               'REASON: CORRECT Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1O)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Galp-(1->2)-alpha-D-Glcp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)OC(O)[C@H](O)[C@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O '
               'NAME: beta-D-Manp-(1->4)-D-Glcp REASON: CORRECT Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO)[C@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: alpha-D-Galp-(1->3)-alpha-D-Manp REASON: CORRECT '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               'False positives: SMILES: '
               'O=C1C2=C(O)C3=C(O[C@H]4[C@@H]3CC[C@H](C4)O)C=C2C(=O)C=5C1=C(O)C=C(O)C5 '
               'NAME: UCT1072M2 REASON: WRONGLY CLASSIFIED Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: O(C1C(O)C(OC(O)C1O)CO)C2OC(C(O)C(O)C2O)CO NAME: '
               '3-alpha-Mannobiose REASON: WRONGLY CLASSIFIED Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O)[C@@H](O)[C@@H]1O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)O)CO '
               'NAME: beta-D-Galp-(1->4)-beta-D-Glcp-(1->4)-beta-D-Glcp '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2ccc(cc2O)-c2cc(=O)c3c(O)cc(O)cc3o2)[C@H](O)[C@@H](O)[C@@H]1O '
               "NAME: luteolin-4'-O-beta-D-glucopyranoside REASON: WRONGLY "
               'CLASSIFIED Contains features characteristic of disaccharides: '
               'two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'C[C@H]1O[C@@H](OC(C)(C)[C@@H]2CC[C@]3(C2)[C@@H](C)CC[C@H](O)C3=C)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: '
               'rel-(2R,5S,7S,10S)-10-Methyl-2-[(1-methyl-1-beta-D-fucopyranosyloxy)ethyl]-6-methylenespiro[4.5]decan-7-ol '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'CN[C@H]1[C@H](O)[C@@H](O)[C@H](CO)O[C@H]1O[C@H]1[C@@H](O[C@@H](C)[C@]1(O)C=O)O[C@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@H](NC(N)=N)[C@@H](O)[C@@H]1NC(N)=N '
               'NAME: streptomycin 6-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@H](O)[C@H](OC(O)[C@@H]2O)CO)[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: '
               '(3R,4S,5R,6R)-4-[(2S,3R,4S,5S,6R)-3,5-Dihydroxy-6-(hydroxymethyl)-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxane-2,3,5-triol '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@H](O)[C@@H](O)[C@@H]1O[C@H]3[C@H](O)[C@@H](O)[C@H](O[C@@H]3CO)O)CO '
               'NAME: beta-D-Glcp-(1->4)-beta-D-Galp-(1->4)-alpha-D-Glcp '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]34CCCC([C@]4([C@@]1(OC3)O)O)(C)C)[C@H](O)C[C@]([C@H]2O)(C=C)C '
               'NAME: Scopararane B REASON: WRONGLY CLASSIFIED Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(O)C=C(C=C2)CCO)C(O)=O '
               "NAME: hydroxytyrosol 4'-glucuronide REASON: WRONGLY CLASSIFIED "
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'C1=C(C2=C(C=C1O)OC(CC2=O)C3=CC(=C4C(=C3)C(C(C(O4)(C)C)O)O)O)O '
               'NAME: sigmoidin G REASON: WRONGLY CLASSIFIED Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@@H]1O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@@H]2[C@@H](O)[C@@H](O)O[C@H](CO)[C@@H]2O)[C@@H]1NC(C)=O '
               'NAME: '
               'alpha-D-GalpNAc-(1->3)-beta-D-GalpNAc-(1->3)-alpha-D-Galp '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'CC(CCNc1ncnc2[nH]cnc12)CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: Dihydrozeatin-O-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@H](O)[C@H](OC(=O)Cc2c[nH]c3ccccc23)[C@@H](O)[C@@H]1O '
               'NAME: 1L-1-O-(indol-3-yl)acetyl-myo-inositol REASON: WRONGLY '
               'CLASSIFIED Contains features characteristic of disaccharides: '
               'two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)CC=2C1=CC(O)=CC2O)C3=CC(O)=C(OC)C=C3 NAME: '
               "4'-O-Methylcatechin REASON: WRONGLY CLASSIFIED Contains "
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O[C@H]2[C@@H](CO)O[C@H](O[C@@H]3[C@@H](CO)O[C@@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: alpha-D-Galp-(1->4)-alpha-D-Galp-(1->4)-beta-D-Glcp '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=CC=3OC=C(C4=CC=C(O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O)C=C4)C(=O)C3C=C2)CO '
               "NAME: Daidzin 4'-O-glucuronide REASON: WRONGLY CLASSIFIED "
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               '[C@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@@H]2[C@@H]([C@H]([C@@H]([C@H](O2)COP([O-])(=O)[O-])O)O)O)O)O)O '
               "NAME: alpha-maltose 6'-phosphate(2-) REASON: WRONGLY "
               'CLASSIFIED Contains features characteristic of disaccharides: '
               'two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1C(OC2=C(O)C=C(C3OC4=C(C(=O)C3O)C(O)=C(OC)C(O)=C4)C=C2)C(O)C(O)C(O)C1C(O)=O '
               'NAME: '
               '3,4,5-trihydroxy-6-[2-hydroxy-4-(3,5,7-trihydroxy-6-methoxy-4-oxo-3,4-dihydro-2H-1-benzopyran-2-yl)phenoxy]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC=2C=3OC(CC3C=C4C2OC(=O)C=C4)C(C)=C)CO '
               'NAME: (R)-Apiumetin glucoside REASON: WRONGLY CLASSIFIED '
               'Contains features characteristic of disaccharides: two sugar '
               'units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O=C1OC(=CC=2C1=C(O)C=C(OC)C2O[C@H]3O[C@H]([C@H](OC)[C@@H]([C@@H]3O)O)CO)C '
               'NAME: '
               '5-[(2R,3S,4R,5R,6S)-3,4-dihydroxy-6-(hydroxymethyl)-5-methoxyoxan-2-yl]oxy-8-hydroxy-6-methoxy-3-methylisochromen-1-one '
               'REASON: WRONGLY CLASSIFIED Contains features characteristic of '
               'disaccharides: two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'C1(C(NC(=C1O)O)CC=2C=CC(=CC2)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)(C)C '
               'NAME: (beta-D-glucosyl)-O-mycofactocinol REASON: WRONGLY '
               'CLASSIFIED Contains features characteristic of disaccharides: '
               'two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'CC(C)(O[C@@H]1O[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@H]1O)C#N '
               'NAME: Linustatin REASON: WRONGLY CLASSIFIED Contains features '
               'characteristic of disaccharides: two sugar units linked by a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C[C@H]1C\\C=C/C(=O)[C@@H](O)[C@@H](O)C\\C=C\\c2cc(O)cc(O)c2C(=O)O1 '
               'NAME: 15-O-desmethyl-(5Z)-7-oxozeaenol REASON: WRONGLY '
               'CLASSIFIED Contains features characteristic of disaccharides: '
               'two sugar units linked by a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@]2([C@H](O)[C@@H](O)[C@@H]1CO)C3=C(OC2)C=C(O)C4=C3OC(=CC4=O)C5=CC=C(O)C=C5 '
               'NAME: Pinnatifinoside A REASON: WRONGLY CLASSIFIED Contains '
               'features characteristic of disaccharides: two sugar units '
               'linked by a glycosidic bond\n'
               'False negatives: SMILES: '
               'OC[C@@H](O)[C@@H](O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@@H](O)C(O)=O '
               'NAME: lactobionic acid REASON: MISSED Too few ring structures '
               'to represent a disaccharide\n'
               ' * SMILES: '
               'CO[C@@H]1[C@H]2OCO[C@H](NC(=O)[C@@H](O)[C@]3(CC(=C)[C@@H](C)[C@@H](C)O3)OC)[C@H]2OC(C[C@H](O)CO)C1(C)C '
               'NAME: Mycalamide A REASON: MISSED Too few hydroxyl groups for '
               'a sugar-like structure\n'
               ' * SMILES: '
               'OC[C@@H](O)[C@@H](O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)C=O '
               'NAME: alpha-D-glucosyl-(1->4)-aldehydo-D-mannose REASON: '
               'MISSED Too few ring structures to represent a disaccharide\n'
               ' * SMILES: '
               'O1[C@@H](O[C@@H]([C@H](O)[C@H](O)CO)[C@@H](O)CO)[C@H](O)[C@@H](O)[C@H](O)[C@H]1CO '
               'NAME: beta-D-Glcp-(1->3)-D-Glc-OH REASON: MISSED Too few ring '
               'structures to represent a disaccharide\n'
               ' * SMILES: '
               'C[C@@H](CC(O)=O)CC(=O)OC[C@H](C)\\C=C(/C)C[C@@H]1O[C@]2(C)C[C@@H]3O[C@@H]4C[C@@H]5O[C@@H]6CC[C@@H]7O[C@@H]8C[C@@H]9O[C@H](C[C@H](O)C[C@@H]%10C[C@@H](C)[C@H](O%10)[C@@H](C)CC(O)=O)[C@@](C)(O)CC[C@H]9O[C@@]8(C)C[C@@]7(C)O[C@H]6C\\C=C/[C@@H](C)[C@H]5O[C@@]4(C)[C@H](O)[C@H]3O[C@H]2CC1=C '
               'NAME: Gambieric acid D REASON: MISSED Unexpected number of '
               'carbons: 66 for disaccharide\n'
               ' * SMILES: '
               '[H][C@]1(OC[C@H](O)[C@H]1OC(=O)c1cc(O)cc(O)c1)[C@]1(CC[C@H](Cc2ccc(O)c(O)c2)C(=O)O1)c1ccc(O)c(O)c1 '
               'NAME: chimarrhinin, (rel)- REASON: MISSED Unexpected number of '
               'carbons: 29 for disaccharide\n'
               ' * SMILES: '
               '[H][C@@](O)(CO)[C@@]([H])(O)[C@]([H])(O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)C(=O)CO '
               'NAME: turanose REASON: MISSED Too few ring structures to '
               'represent a disaccharide\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@H]2OC(=C(O)[C@H](O)[C@H]2OS(O)(=O)=O)C(O)=O)[C@H](O)[C@@H](NS(O)(=O)=O)[C@@H]1O)CO '
               'NAME: '
               '2-O-sulfo-beta-L-threo-hex-4-enopyranuronosyl-(1->4)-beta-D-GlcpNS '
               'REASON: MISSED Unexpected number of oxygens: 17 for '
               'disaccharide\n'
               ' * SMILES: '
               'S(O)(=O)(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2OC(=C(O)[C@H](O)[C@H]2OS(O)(=O)=O)C(O)=O)[C@H](O[C@@H]1O)CO '
               'NAME: '
               '(2R,3R,4R)-2-[(2R,3S,4R,5R,6S)-4,6-Dihydroxy-2-(hydroxymethyl)-5-(sulfoamino)oxan-3-yl]oxy-4,5-dihydroxy-3-sulfooxy-3,4-dihydro-2H-pyran-6-carboxylic '
               'acid REASON: MISSED Unexpected number of oxygens: 17 for '
               'disaccharide\n'
               ' * SMILES: '
               'CC(C)(O)[C@H]1C[C@@]2(O)C[C@H](CC=C)C(=O)C(CC3=C4O[C@H](C[C@@]4(O)C[C@H](CC=C)C3=O)C(C)(C)O)=C2O1 '
               'NAME: Illicidione C REASON: MISSED Unexpected number of '
               'carbons: 29 for disaccharide\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C(COC(=O)C)=CC=C1',
                                     'name': 'Furfuryl acetate',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(NC1=C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CC(C)C)CO',
                                     'name': '[D-Ser1,D-Asp3,Dha7]MC-LR',
                                     'reason': 'No clear glycosidic bond '
                                               'pattern found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)NC(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CC(=O)NCC3=CC=CC=N3',
                                     'name': '2-[(2R,5S,6R)-6-(hydroxymethyl)-5-[[(4-methoxyanilino)-oxomethyl]amino]-2-oxanyl]-N-(2-pyridinylmethyl)acetamide',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'O=[N+]([O-])C1=CC=C(/C=C(/C=C(/C=C/C=2OC(OC)=C(C)C(C2C)=O)\\C)\\C)C=C1',
                                     'name': 'Dehydrodeoxyaureothin',
                                     'reason': 'No clear glycosidic bond '
                                               'pattern found'},
                                 {   'smiles': 'C1CNCCNCCCN(CCNC1)CC2=CC=C(C=C2)CN3CCCNCCNCCCNCC3',
                                     'name': 'plerixafor',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'O=C(C[C@@H]1O[C@H](CC[C@H]1O)C)C',
                                     'name': 'Decarestrictine L',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'O=C1OC(=CC2=C1C[C@@H]3[C@@]4([C@H](C(C)(C)O[C@H]4CC(=O)OC)[C@@H](C[C@]3(O2)C)OC(=O)C)C)C',
                                     'name': 'Asperversin A',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'O=C1OC(CC=2C1=C(O)C3=C(O)C(C4=C(O)C5=C(O)C=6C(=O)OC(CC(=O)C)CC6C=C5C=C4OC)=C(OC)C=C3C2)CC(=O)C',
                                     'name': 'SC-30532',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'C([C@H](NC(CC[C@H](N)C(=O)O)=O)C(O)=O)S[C@H](\\C=C\\C=C\\C=C/C/C=C\\CCCCC)[C@@H](O)CCCC(=O)O',
                                     'name': 'leukotriene F4',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'},
                                 {   'smiles': 'C1(=C(C=C2C(=C1)[C@@]34[C@@]([NH+](C2)CC3)(CC(CC4)=O)[H])O)OC',
                                     'name': '(4aS,10bR)-oxomaritidine(1+)',
                                     'reason': 'Requires exactly two ring '
                                               'structures typical in '
                                               'disaccharides'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@@H](O)[C@@H](O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@@H](O)C(O)=O',
                                      'name': 'lactobionic acid',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': '[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)OC)O)OC)O)OC',
                                      'name': "1,3,3'-tri-O-methyl-4alpha-mannobiose",
                                      'reason': 'Too few hydroxyl groups for a '
                                                'sugar-like structure'},
                                  {   'smiles': 'CO[C@@H]1[C@H]2OCO[C@H](NC(=O)[C@@H](O)[C@]3(CC(=C)[C@@H](C)[C@@H](C)O3)OC)[C@H]2OC(C[C@H](O)CO)C1(C)C',
                                      'name': 'Mycalamide A',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': 'OC[C@H]1O[C@]2(CO[C@]3(CO)O[C@H](CO)[C@@H](O)[C@@H]3O2)[C@@H](O)[C@@H]1O',
                                      'name': 'bis-beta-D-fructofuranose '
                                              "1,2':2,3'-dianhydride",
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': 'OC[C@@H](O)[C@@H](O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)C=O',
                                      'name': 'alpha-D-glucosyl-(1->4)-aldehydo-D-mannose',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': 'O1[C@@H](O[C@@H]([C@H](O)[C@H](O)CO)[C@@H](O)CO)[C@H](O)[C@@H](O)[C@H](O)[C@H]1CO',
                                      'name': 'beta-D-Glcp-(1->3)-D-Glc-OH',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': 'C[C@@H](CC(O)=O)CC(=O)OC[C@H](C)\\C=C(/C)C[C@@H]1O[C@]2(C)C[C@@H]3O[C@@H]4C[C@@H]5O[C@@H]6CC[C@@H]7O[C@@H]8C[C@@H]9O[C@H](C[C@H](O)C[C@@H]%10C[C@@H](C)[C@H](O%10)[C@@H](C)CC(O)=O)[C@@](C)(O)CC[C@H]9O[C@@]8(C)C[C@@]7(C)O[C@H]6C\\C=C/[C@@H](C)[C@H]5O[C@@]4(C)[C@H](O)[C@H]3O[C@H]2CC1=C',
                                      'name': 'Gambieric acid D',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': 'O1[C@]2(OC[C@@]3(OC2)OC[C@@H](O)[C@@H](O)[C@@H]3O)[C@@H](O)[C@H](O)[C@H]1CO',
                                      'name': 'alpha-D-Fructofuranose '
                                              'beta-D-fructopyranose '
                                              '1,2:2,1-dianhydride',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': '[H][C@]1(OC[C@H](O)[C@H]1OC(=O)c1cc(O)cc(O)c1)[C@]1(CC[C@H](Cc2ccc(O)c(O)c2)C(=O)O1)c1ccc(O)c(O)c1',
                                      'name': 'chimarrhinin, (rel)-',
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'},
                                  {   'smiles': '[C@]12(O[C@@H]3[C@](O[C@@H]([C@H]3O)CO)(CO)OC1)O[C@H](CO)[C@H]([C@@H]2O)O',
                                      'name': 'alpha-D-fructofuranose-beta-D-fructofuranose '
                                              "2',1:2,3'-dianhydride",
                                      'reason': 'Requires exactly two ring '
                                                'structures typical in '
                                                'disaccharides'}],
    'attempt': 2,
    'reasoning': 'The previous attempt involved several criteria for '
                 'identifying disaccharides: identifying the presence of at '
                 'least two rings, a glycosidic bond pattern, a typical range '
                 'of carbon and oxygen atoms, and sufficient hydroxyl groups '
                 'or ether linkages. Despite this, there were several false '
                 'positives and negatives, indicating the criteria were either '
                 'too broad or too strict.\n'
                 '\n'
                 'To improve the classification:\n'
                 '\n'
                 '1. **Rings**: Ensure that the method accurately identifies '
                 'compounds with precisely two sugar rings. Disaccharides '
                 'typically consist of two ring structures linked via a '
                 'glycosidic bond.\n'
                 '\n'
                 '2. **Carbons and Oxygens**: Relax the constraints on carbon '
                 'and oxygen counts to accommodate unusual rings or sugar '
                 'derivatives present in disaccharides.\n'
                 '\n'
                 '3. **Glycosidic Bond**: Improve detection of the glycosidic '
                 'bond. A more precise SMARTS pattern accounting for the '
                 'linkage details seen in sugars could help.\n'
                 '\n'
                 '4. **Exceptions**: Consider specific common exceptions or '
                 'derivatives in disaccharide structures, such as presence of '
                 'additional linked compounds or substitutions (e.g., '
                 'phosphates).\n'
                 '\n'
                 'Here is the revised code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 278,
    'num_false_positives': 840,
    'num_true_negatives': 141157,
    'num_false_negatives': 25,
    'num_negatives': None,
    'precision': 0.24865831842576028,
    'recall': 0.9174917491749175,
    'f1': 0.3912737508796622,
    'accuracy': 0.9939212930428671,
    'negative_predictive_value': 0.999822923602159}