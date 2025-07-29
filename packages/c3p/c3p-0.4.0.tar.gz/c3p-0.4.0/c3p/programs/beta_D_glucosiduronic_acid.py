"""
Classifies: CHEBI:15341 beta-D-glucosiduronic acid
"""
"""
Classifies: CHEBI:18085 beta-D-glucosiduronic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_beta_D_glucosiduronic_acid(smiles: str):
    """
    Determines if a molecule is a beta-D-glucosiduronic acid based on its SMILES string.
    A beta-D-glucosiduronic acid is a glucosiduronic acid resulting from the formal condensation
    of any substance with beta-D-glucuronic acid to form a glycosidic bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-D-glucosiduronic acid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the beta-D-glucuronic acid substructure pattern
    glucuronic_acid_pattern = Chem.MolFromSmarts("[C@H]1([C@@H]([C@H]([C@@H]([C@H](O1)C(=O)O)O)O)O)")
    if not mol.HasSubstructMatch(glucuronic_acid_pattern):
        return False, "No beta-D-glucuronic acid moiety found"

    # Check for the presence of a glycosidic bond (O-C bond between the glucuronic acid and another moiety)
    glycosidic_bond_pattern = Chem.MolFromSmarts("[OX2][C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)C(=O)O)O)O)")
    glycosidic_bond_matches = mol.GetSubstructMatches(glycosidic_bond_pattern)
    if len(glycosidic_bond_matches) == 0:
        return False, "No glycosidic bond found"

    # Ensure the molecule contains more than just the glucuronic acid moiety
    # This is a simple check to ensure there is another substructure connected via the glycosidic bond
    # We count the number of atoms not part of the glucuronic acid moiety
    glucuronic_acid_atoms = set()
    for match in mol.GetSubstructMatches(glucuronic_acid_pattern):
        glucuronic_acid_atoms.update(match)
    
    total_atoms = mol.GetNumAtoms()
    if len(glucuronic_acid_atoms) >= total_atoms:
        return False, "Molecule contains only the glucuronic acid moiety"

    # Basic stereochemistry check: Ensure the C1-OH is axial (beta configuration)
    # This is a simplified check and may not catch all cases
    for match in mol.GetSubstructMatches(glucuronic_acid_pattern):
        c1_atom = mol.GetAtomWithIdx(match[0])
        if not c1_atom.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
            return False, "Glucuronic acid moiety is not in beta configuration"

    return True, "Contains beta-D-glucuronic acid moiety with a glycosidic bond"

# Example usage:
# smiles = "O[C@H]1[C@@H](O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O)Oc1ccccc1C(O)=O"
# print(is_beta_D_glucosiduronic_acid(smiles))


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15341',
                          'name': 'beta-D-glucosiduronic acid',
                          'definition': 'A glucosiduronic acid resulting from '
                                        'the formal condensation of any '
                                        'substance with beta-D-glucuronic acid '
                                        'to form a glycosidic bond.',
                          'parents': ['CHEBI:24302'],
                          'xrefs': ['KEGG:C03033'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 39,
                           'log_lines_of_code': 3.6635616461296463,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 0],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetChiralTag',
                                                 'GetNumAtoms',
                                                 'MolFromSmarts',
                                                 'update',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx'],
                           'methods_called_count': 8,
                           'smarts_strings': [   '[C@H]1([C@@H]([C@H]([C@@H]([C@H](O1)C(=O)O)O)O)O)',
                                                 '[OX2][C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)C(=O)O)O)O)'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_beta_D_glucosiduronic_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No beta-D-glucuronic acid '
                                          'moiety found"',
                                          'False, "No glycosidic bond found"',
                                          'False, "Molecule contains only the '
                                          'glucuronic acid moiety"',
                                          'False, "Glucuronic acid moiety is '
                                          'not in beta configuration"',
                                          'True, "Contains beta-D-glucuronic '
                                          'acid moiety with a glycosidic '
                                          'bond"'],
                           'returns_count': 6,
                           'complexity': 4.332712329225929},
    'message': '\n'
               'Attempt failed: F1 score of 0.15988779803646563 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CNC1=NC2=C(C(C)=C(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C(O)=O)C(C)=C2S1)CC4=CN=CC=C4 '
               'NAME: E3040 glucuronide REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O)Oc1ccccc1C(O)=O '
               'NAME: 1-salicylate glucuronide REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=C(OC)C=C(C=C2)C=3OC=4C(C(=O)C3OC)=C(O)C=5OCOC5C4)C(O)=O '
               "NAME: 4',5-Dihydroxy-3,3'-dimethoxy-6,7-methylenedioxyflavone "
               "4'-glucuronide REASON: CORRECT Contains beta-D-glucuronic acid "
               'moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H](OC2=CC([C@H]3OC=4C(C[C@H]3O)=C(O)C=C(O)C4)=CC(O)=C2OC)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O '
               "NAME: 4'-Methyl-(-)-epigallocatechin 3'-glucuronide REASON: "
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@H](O)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])CC[C@@]2([H])C[C@@H](CC[C@]12C)O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O '
               'NAME: 5alpha-androstane-3beta,17beta-diol '
               '3-O-(beta-D-glucuronide) REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)C(=O)O)OC=2C=C3OC(C=4C=C(C=CC4C3=CC2)O)=O '
               'NAME: urolithin A 3-O-glucuronide REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2([C@H](O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)C1)C)[H])[H])[H] '
               'NAME: 17alpha-estradiol 17-O-(beta-D-glucuronide) REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O1[C@H](C(O)=O)[C@H]([C@H](O)[C@H]([C@@H]1O[C@@H]2C[C@H](N(C)C2=O)C=3C=NC=CC3)O)O '
               'NAME: trans-3-hydroxycotinine beta-D-glucuronide REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O(C1C(OC(C(=O)C1O)C)C2=C(O)C3=C(OC(=CC3=O)C4=CC=C(OC5OC(C(O)C(O)C5O)C(O)=O)C=C4)C=C2O)C6OC(C(O)C(O)C6O)C '
               'NAME: '
               '6-[4-(5,7-dihydroxy-6-{4-hydroxy-6-methyl-5-oxo-3-[(3,4,5-trihydroxy-6-methyloxan-2-yl)oxy]oxan-2-yl}-4-oxo-4H-chromen-2-yl)phenoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: CORRECT Contains beta-D-glucuronic acid moiety '
               'with a glycosidic bond\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)[H])O)[H])(CC[C@@]4([C@@H](CCC(O)=O)C)[H])[H])C)[H])C '
               'NAME: chenodeoxycholic acid 3-O-(beta-D-glucuronide) REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1(=NC(C=2N(C=3C1=CC(=CC3)Cl)C(=NC2)C)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O)=O)O)O)O)C=5C=CC=CC5F '
               'NAME: 4-hydroxymidazolam beta-D-glucuronide REASON: CORRECT '
               'Contains beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H](OC=2C=3C[C@@H](O)[C@@H](OC3C=C(O)C2)C4=CC(O)=C(O)C=C4)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O '
               'NAME: catechin 5-glucuronide REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               '[H][C@@]12CC(C)(C)C[C@@H](O)[C@]1(C)CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C(O)=O)[C@](C)(CO)[C@]3([H])CC[C@@]12C '
               'NAME: soyasapogenol B 3-O-beta-glucuronide REASON: CORRECT '
               'Contains beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]34C[C@@H](CC[C@@]3([H])[C@]1(C)C[C@@H](C[C@H]2C(O)=O)O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O)C(=C)[C@@H]4O '
               'NAME: atractyligenin 2-glucuronide REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@@H](O)[C@@H]([C@H]5O)O)C(O)=O)[H])[H])(CC[C@]4([H])[C@@H](CCC(O)=O)C)[H])C)O)[H])C '
               'NAME: deoxycholic acid 3-glucuronide REASON: CORRECT Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)[H])[H])(CC[C@@]4([C@@H](CCC(O)=O)C)[H])[H])C)[H])C '
               'NAME: lithocholic acid 3-O-(beta-D-glucuronide) REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C\\C=C(\\C)C(=O)O[C@H]1CC(C)(C)C[C@H]2C3=CC[C@@H]4[C@@]5(C)CC[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7OC[C@H](O)[C@H](O)[C@H]7O[C@@H]7OC[C@@H](O)[C@H](O)[C@H]7O)[C@H]6O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6O)C(O)=O)C(C)(C)[C@@H]5CC[C@@]4(C)[C@]3(C)[C@@H](O)[C@@H](O)[C@@]12CO '
               'NAME: gordonoside J REASON: CORRECT Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'CC(=O)Nc1ccc(O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)cc1 '
               'NAME: acetaminophen O-beta-D-glucosiduronic acid REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(CC3)C=C(C=C4)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)(CC[C@@]2(C(=O)[C@@H]1O)C)[H])[H])[H] '
               'NAME: 16alpha-hydroxyestrone 3-O-(beta-D-glucuronide) REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)O)O)O)O)C(=C4)OC)CC3)(CC[C@@]2([C@@H](O)C1)C)[H])[H])[H] '
               'NAME: 2-methoxy-17beta-estradiol 3-O-(beta-D-glucuronide) '
               'REASON: CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C=1(C(CCC(C1C)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(O)=O)O)O)O)(C)C)/C=C/C(=C/C=C/C(=C/C(O)=O)/C)/C '
               'NAME: 4-(beta-D-glucopyranuronosyloxy)retinoic acid REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2(C(=O)[C@@H]1O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)C)[H])[H])[H] '
               'NAME: 16alpha-hydroxyestrone 16-O-(beta-D-glucuronide) REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C[C@@H]([C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@@]4([C@@H](CCC(O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)=O)C)[H])[H])C)[H])C '
               'NAME: hyodeoxycholic acid 24-O-(beta-D-glucuronide) REASON: '
               'CORRECT Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1(=NCC=2N(C=3C1=CC(=CC3)Cl)C(=NC2)CO[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O)=O)O)O)O)C=5C=CC=CC5F '
               'NAME: 1-hydroxymidazolam beta-D-glucuronide REASON: CORRECT '
               'Contains beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O([C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)C(O)=O)O)O)O)C2=CC3=C([C@@]4([C@]([C@]5([C@@]([C@@H](O)CC5)(CC4)C)[H])(CC3)[H])[H])C=C2 '
               'NAME: 17beta-estradiol 3-glucosiduronic acid REASON: CORRECT '
               'Contains beta-D-glucuronic acid moiety with a glycosidic bond\n'
               'False positives: SMILES: '
               'COc1c(O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)cc2oc(cc(=O)c2c1O)-c1ccccc1 '
               'NAME: oroxylin A 7-O-beta-D-glucuronate REASON: WRONGLY '
               'CLASSIFIED Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O([C@@H]1C\\C(=C\\C=C/2\\[C@]3([C@@]([C@](CC3)([C@@H](CCCC(C)C)C)[H])(CCC2)C)[H])\\C([C@@H](O)C1)=C)[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C(O)=O '
               'NAME: 1-Hydroxyvitamin D3 3-D-glucopyranoside REASON: WRONGLY '
               'CLASSIFIED Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O(C1C(O)C(OC2C(O)C(O)C(OC2O)C)OC(C1O)C(O)=O)C3OC(C(O)C(O)C3O)C(O)=O '
               'NAME: '
               'b-D-Glucuronopyranosyl-(1->3)-a-D-galacturonopyranosyl-(1->2)-L-rhamnose '
               'REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic acid '
               'moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O)[C@@H]1O)C(=O)O)[C@@H]2OC[C@@H](O)[C@H](O)[C@H]2O '
               'NAME: beta-D-Xylp-(1->3)-beta-D-GlcpA REASON: WRONGLY '
               'CLASSIFIED Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP([O-])(=O)OP([O-])(=O)OC2O[C@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O '
               'NAME: UDP-L-iduronate(3-) REASON: WRONGLY CLASSIFIED Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'P(O[C@H]([C@@H](O)[C@H](O[C@@H]1O[C@@H]([C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5OC(=C(O)[C@H](O)[C@H]5O)C(O)=O)[C@H]4NC(=O)C)CO)[C@H](O)[C@H]3O)C(O)=O)[C@H]2O)CO)[C@H]1O)CO)CO)CO)(O)(O)=O '
               'NAME: '
               '(2R,3R,4R)-2-[(2S,3R,4R,5R,6R)-3-Acetamido-2-[(2S,3S,4R,5R,6R)-2-carboxy-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4S,5R,6S)-3,5-dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4S)-1,3,5-trihydroxy-4-phosphonooxypentan-2-yl]oxyoxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4,5-dihydroxyoxan-3-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,4,5-trihydroxy-3,4-dihydro-2H-pyran-6-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1CO)C=2C(OC3OC(C(O)C(O)C3O)C(O)=O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=C5C2OC(=CC5=O)C6=CC(O)=CC=C6 '
               'NAME: '
               '3,4,5-trihydroxy-6-{[5-hydroxy-2-(3-hydroxyphenyl)-4-oxo-6,8-bis[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]-4H-chromen-7-yl]oxy}oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'IC1=C(O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@@H]2O)C(O)=O)C(I)=CC(OC3=CC=C(C[C@@H](N)C(O)=O)C=C3)=C1 '
               'NAME: '
               '(2S,3R,4S,5S,6S)-6-(4-{4-[(2R)-2-amino-2-carboxyethyl]phenoxy}-2,6-diiodophenoxy)-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(OC=2C3=C(C=C(O)C2)C=CCCCC(=O)CCCC(OC3=O)C)C(O)C(O)C(O)C1C(O)=O '
               'NAME: '
               '3,4,5-trihydroxy-6-[(14-hydroxy-3-methyl-1,7-dioxo-3,4,5,6,7,8,9,10-octahydro-1H-2-benzoxacyclotetradecin-16-yl)oxy]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC(=O)C(OC(=O)/C=C/C2=CC(OC)=C(O)C=C2)C(O)C(O)=O)C(O)=O '
               'NAME: '
               '6-[(3-carboxy-3-hydroxy-2-{[3-(4-hydroxy-3-methoxyphenyl)prop-2-enoyl]oxy}propanoyl)oxy]-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@@H](O)[C@H](OS(O)(=O)=O)[C@H]3O)C(O)=O)[C@H]2O)[C@@H](CO)O[C@H]1O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](O)C(O)O[C@@H]2CO)[C@@H]1O '
               'NAME: '
               'beta-D-GlcpA3S-(1->3)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->3)-beta-D-Galp-(1->4)-D-Glcp '
               'REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic acid '
               'moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=C(OC(=O)/C=C/C3=CC(OC)=C(O)C=C3)C(O)=C4C(OC(=CC4=O)C5=CC=C(O)C=C5)=C2)C(O)=O '
               'NAME: Scutellarein 7-glucuronide-6-ferulate REASON: WRONGLY '
               'CLASSIFIED Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'C1[C@]2([C@]([C@]3([C@@](C(CC3)=O)(C1)C)[H])(CC[C@]4([C@@]2(CC[C@@H](C4)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(O)=O)O)O)O)C)[H])[H])[H] '
               'NAME: etiocholanolone 3-glucuronide REASON: WRONGLY CLASSIFIED '
               'Contains beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'COc1ccc(CO[C@@H]2O[C@H](CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C(O)=O)[C@@H](O)[C@H](OC(=O)c3ccccc3)[C@H]2O)cc1 '
               'NAME: locoracemoside B REASON: WRONGLY CLASSIFIED Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O(C1C(OC(=O)/C=C/C2=CC=C(O)C=C2)C(OC3C(O)C(O)C(OC3OC=4C=C5OC(=CC(=O)C5=C(O)C4)C6=CC=C(O)C=C6)C(O)=O)OC(C1O)C(O)=O)C7OC(C(O)C(O)C7O)C(O)=O '
               'NAME: Apigenin '
               '7-[p-coumaroyl-(->2)-[glucuronyl-(1->3)]-glucuronyl-(1->2)-glucuronide] '
               'REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic acid '
               'moiety with a glycosidic bond\n'
               ' * SMILES: O1C(OC2=C(C(C)C)C=CC(=C2)C)C(O)C(O)C(O)C1C(O)=O '
               'NAME: '
               '(2S,3S,4S,5R)-3,4,5-Trihydroxy-6-(5-methyl-2-propan-2-ylphenoxy)oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(OCC(C(=O)CCC2=CC=C(OC)C=C2)C)C(O)C(O)C(O)C1C(O)=O NAME: '
               '3,4,5-trihydroxy-6-{[5-(4-methoxyphenyl)-2-methyl-3-oxopentyl]oxy}oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(OC)C=C(C=C2)/C=C/C(=O)CC(=O)/C=C/C3=CC(OC)=C(O)C=C3)C(O)=O '
               'NAME: curcumin glucuronide REASON: WRONGLY CLASSIFIED Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=CC3=C(C=C2)C=C(OC3=O)/C=C/CC)C(O)=O '
               'NAME: '
               '6-({3-[(1E)-but-1-en-1-yl]-1-oxo-1H-isochromen-7-yl}oxy)-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(OC)C=C(C=C2)/C=C/C(O)=O)C(O)=O '
               'NAME: ferulic acid 4-glucuronide REASON: WRONGLY CLASSIFIED '
               'Contains beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O=C(O)[C@H]1O[C@H](OC[C@H](O)COCCCCCCCCCCCCC(C)C)[C@H](O)[C@H]([C@@H]1O[C@H]2O[C@@H]([C@@H](O)[C@@H]([C@H]2O)O)CO)O '
               'NAME: Kribelloside A REASON: WRONGLY CLASSIFIED Contains '
               'beta-D-glucuronic acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'S(OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](O[C@@H]2C(O)=O)O[C@H]([C@@H](NC(=O)C)CO)[C@@H](O)[C@H](O)COS(O)(=O)=O)[C@H](NC(=O)C)[C@@H](O)[C@H]1O)(O)(=O)=O '
               'NAME: '
               '(2S,3S,4R,5R,6R)-3-[(2S,3R,4R,5R,6R)-3-Acetamido-4,5-dihydroxy-6-(sulfooxymethyl)oxan-2-yl]oxy-6-[(2S,3R,4S,5R)-2-acetamido-1,4,5-trihydroxy-6-sulfooxyhexan-3-yl]oxy-4,5-dihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=C(C(=O)CCC3=CC=CC=C3)C=C(O)C=C2)C(O)=O '
               'NAME: '
               '3,4,5-trihydroxy-6-[4-hydroxy-2-(3-phenylpropanoyl)phenoxy]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               ' * SMILES: '
               'O1[C@@H](OC2=C(O)C=3OC(=CC(=O)C3C(O)=C2)C4=CC(O)=C(O)C(O)=C4)C(O)[C@@H](O)[C@H](O)C1C(O)=O '
               'NAME: 8-Hydroxytricetin 7-glucuronide REASON: WRONGLY '
               'CLASSIFIED Contains beta-D-glucuronic acid moiety with a '
               'glycosidic bond\n'
               ' * SMILES: '
               'O1C(OC2=CC(O)=C(CC(O)CC3=CC(OC)=CC=C3)C(O)=C2)C(O)C(O)C(O)C1C(O)=O '
               'NAME: '
               '6-{3,5-dihydroxy-4-[2-hydroxy-3-(3-methoxyphenyl)propyl]phenoxy}-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains beta-D-glucuronic '
               'acid moiety with a glycosidic bond\n'
               'False negatives: SMILES: '
               'CC\\C(c1ccccc1)=C(/c1ccccc1)c1ccc(OCC[N+](C)(C)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)cc1 '
               'NAME: tamoxifen N-beta-D-glucosiduronic acid REASON: MISSED No '
               'glycosidic bond found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CC3=CC=NC=C3)O[C@@H]1CN(C)C(=O)C4CCOCC4)[C@H](C)CO',
                                     'name': 'N-[[(4S,5S)-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-8-(2-pyridin-4-ylethynyl)-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methyl-4-oxanecarboxamide',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'O(C1C(C2C(C3C(C4(C(C5C(CC4)(CCC5C(C)=C)C(O)=O)CC3)C)(CC2)C)(CC1O)C)(C)C)C(=O)/C=C/C6=CC=C(O)C=C6',
                                     'name': '3-O-p-trans-Coumaroylalphitolic '
                                             'acid',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'CC1=CC(=CC(=C1)OC2=C(C(=O)N(N=C2)C(C)(C)C)Cl)C(C)C',
                                     'name': '2-tert-butyl-4-chloro-5-(3-methyl-5-propan-2-ylphenoxy)-3-pyridazinone',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'O=C1OC[C@@H]2[C@]1([C@@H]3[C@@H](C=C2)C[C@@H](CO)CC3)C',
                                     'name': 'Oblongolide F',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'O=C(O)/C(=C/C[C@H](OC(=O)C)[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](OC(=O)C)CC4)(C)C)C[C@H]3OC)C)CC2)(C)[C@H](C1)OC(=O)C)C)C)/C',
                                     'name': '(22S,24E)-3beta,22-7alpha-methoxy-3beta,15alpha,22-triacetoxylanosta-8,24-dien-26-oic '
                                             'acid',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': '[H][C@@]1(CC[C@@H](OC1)C(C)(C)O)[C@@]1([H])CC[C@@]2(C)C3=C(C=C[C@]12C)[C@@]1(C)CC[C@H](OC(C)=O)C(C)(C)[C@]1([H])CC3',
                                     'name': 'Hypocrellol E',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC(O)=O)C(O)=O',
                                     'name': 'Trp-Asp-Cys',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': '[As](=O)(CCCCCCCC(O)=O)(C)C',
                                     'name': '8-dimethylarsinoyl-octanoic acid',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)NC(=O)NC2=CC3=C(C=C2)O[C@H]4[C@@H]3C[C@@H](O[C@H]4CO)CC(=O)O',
                                     'name': '2-[(1S,3R,4aR,9aS)-1-(hydroxymethyl)-6-[[(4-methoxyanilino)-oxomethyl]amino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]acetic '
                                             'acid',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6O[C@@H]([C@H](O)[C@H]6O)CO)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-3-[(2S,3R,4R,5R)-3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]oxy-5-hydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No beta-D-glucuronic acid '
                                               'moiety found'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@H]1[C@@H](O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O)Oc1ccccc1C(O)=O',
                                      'name': '1-salicylate glucuronide',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=C(OC)C=C(C=C2)C=3OC=4C(C(=O)C3OC)=C(O)C=5OCOC5C4)C(O)=O',
                                      'name': "4',5-Dihydroxy-3,3'-dimethoxy-6,7-methylenedioxyflavone "
                                              "4'-glucuronide",
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'O1[C@@H](OC2=CC([C@H]3OC=4C(C[C@H]3O)=C(O)C=C(O)C4)=CC(O)=C2OC)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O',
                                      'name': "4'-Methyl-(-)-epigallocatechin "
                                              "3'-glucuronide",
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': '[C@H]1(O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)C(=O)O)OC=2C=C3OC(C=4C=C(C=CC4C3=CC2)O)=O',
                                      'name': 'urolithin A 3-O-glucuronide',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'O(C1C(OC(C(=O)C1O)C)C2=C(O)C3=C(OC(=CC3=O)C4=CC=C(OC5OC(C(O)C(O)C5O)C(O)=O)C=C4)C=C2O)C6OC(C(O)C(O)C6O)C',
                                      'name': '6-[4-(5,7-dihydroxy-6-{4-hydroxy-6-methyl-5-oxo-3-[(3,4,5-trihydroxy-6-methyloxan-2-yl)oxy]oxan-2-yl}-4-oxo-4H-chromen-2-yl)phenoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'C1(=NC(C=2N(C=3C1=CC(=CC3)Cl)C(=NC2)C)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O)=O)O)O)O)C=5C=CC=CC5F',
                                      'name': '4-hydroxymidazolam '
                                              'beta-D-glucuronide',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'O1[C@@H](OC=2C=3C[C@@H](O)[C@@H](OC3C=C(O)C2)C4=CC(O)=C(O)C=C4)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O',
                                      'name': 'catechin 5-glucuronide',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'C1[C@]2([C@]3([C@@](C4=C(C=C(O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)O)O)O)O)C(=C4)OC)CC3)(CC[C@@]2([C@@H](O)C1)C)[H])[H])[H]',
                                      'name': '2-methoxy-17beta-estradiol '
                                              '3-O-(beta-D-glucuronide)',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'C=1(C(CCC(C1C)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(O)=O)O)O)O)(C)C)/C=C/C(=C/C=C/C(=C/C(O)=O)/C)/C',
                                      'name': '4-(beta-D-glucopyranuronosyloxy)retinoic '
                                              'acid',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'},
                                  {   'smiles': 'C1(=NCC=2N(C=3C1=CC(=CC3)Cl)C(=NC2)CO[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O)=O)O)O)O)C=5C=CC=CC5F',
                                      'name': '1-hydroxymidazolam '
                                              'beta-D-glucuronide',
                                      'reason': 'Glucuronic acid moiety is not '
                                                'in beta configuration'}],
    'attempt': 1,
    'reasoning': 'The previous code had a few issues that led to incorrect '
                 'classifications:\n'
                 '\n'
                 '1. **False Positives**: The code incorrectly classified '
                 'molecules that contained a beta-D-glucuronic acid moiety but '
                 'were not beta-D-glucosiduronic acids. This happened because '
                 'the code only checked for the presence of the glucuronic '
                 'acid moiety and a glycosidic bond, but did not verify if the '
                 'glycosidic bond was formed with another substance (i.e., the '
                 'glucuronic acid was not the only component).\n'
                 '\n'
                 '2. **False Negatives**: The code missed some true positives, '
                 'likely because the glycosidic bond pattern was too '
                 'restrictive. The pattern '
                 '`[OX2][C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)C(=O)O)O)O)` might '
                 'not match all possible glycosidic bonds, especially if the '
                 'bond is formed with a different atom or if the '
                 'stereochemistry is not perfectly represented.\n'
                 '\n'
                 '3. **Stereochemistry**: The code assumed that the SMILES '
                 'string correctly represented the beta configuration, but '
                 'this might not always be the case. A more robust check for '
                 'stereochemistry could improve accuracy.\n'
                 '\n'
                 '### Improvements:\n'
                 '- **Refine the Glycosidic Bond Pattern**: The glycosidic '
                 'bond pattern should be more flexible to account for '
                 'different types of bonds and stereochemistry.\n'
                 '- **Check for Additional Substructure**: Ensure that the '
                 'molecule contains more than just the glucuronic acid moiety, '
                 'i.e., it should have another substructure connected via the '
                 'glycosidic bond.\n'
                 '- **Stereochemistry Check**: Implement a basic '
                 'stereochemistry check to ensure the glucuronic acid is in '
                 'the beta configuration.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 58,
    'num_false_positives': 456,
    'num_true_negatives': 141729,
    'num_false_negatives': 57,
    'num_negatives': None,
    'precision': 0.11284046692607004,
    'recall': 0.5043478260869565,
    'f1': 0.18441971383147854,
    'accuracy': 0.9963949402670415,
    'negative_predictive_value': 0.9995979856967543}