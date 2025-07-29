"""
Classifies: CHEBI:75874 para-terphenyl
"""
"""
Classifies: CHEBI:39158 para-terphenyl
A ring assembly based on a 1,4-diphenylbenzene skeleton and its substituted derivatives thereof.
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_para_terphenyl(smiles: str):
    """
    Determines if a molecule is a para-terphenyl based on its SMILES string.
    A para-terphenyl is a ring assembly based on a 1,4-diphenylbenzene skeleton
    and its substituted derivatives thereof.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a para-terphenyl, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for para-terphenyl core structure
    # C1=CC(=CC=C1C2=CC=CC=C2)C3=CC=CC=C3
    terphenyl_pattern = Chem.MolFromSmarts("c1ccc(-c2ccc(-c3ccccc3)cc2)cc1")
    if not mol.HasSubstructMatch(terphenyl_pattern):
        return False, "No para-terphenyl core structure found"

    # Check for allowed atoms
    allowed_atoms = [6, 8, 16, 17, 35, 53]  # C, O, S, Cl, Br, I
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atoms:
            return False, f"Atom {atom.GetSymbol()} not allowed in para-terphenyls"

    # Check for common functional groups
    functional_groups = ["CO", "OC", "CO.O", "C(=O)O", "C(=O)C", "C=C"]
    for fg in functional_groups:
        fg_pattern = Chem.MolFromSmarts(fg)
        if mol.HasSubstructMatch(fg_pattern):
            break
    else:
        return False, "No allowed functional groups found"

    # Additional checks
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200 or mol_wt > 1000:
        return False, "Molecular weight out of expected range for para-terphenyls"

    n_rings = mol.GetRingInfo().NumRings()
    if n_rings < 3 or n_rings > 6:
        return False, "Number of rings out of expected range for para-terphenyls"

    return True, "Meets structural and functional group requirements for para-terphenyls"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:75874',
                          'name': 'para-terphenyl',
                          'definition': 'A ring assembly based on a '
                                        '1,4-diphenylbenzene skeleton and its '
                                        'substituted derivatives thereof.',
                          'parents': ['CHEBI:33836', 'CHEBI:36820'],
                          'xrefs': ['Wikipedia:Terphenyl'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 40,
                           'log_lines_of_code': 3.6888794541139363,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
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
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'NumRings',
                                                 'GetRingInfo',
                                                 'GetAtoms',
                                                 'GetSymbol',
                                                 'CalcExactMolWt',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum'],
                           'methods_called_count': 9,
                           'smarts_strings': [   'c1ccc(-c2ccc(-c3ccccc3)cc2)cc1',
                                                 'fg'],
                           'smarts_strings_count': 2,
                           'defs': ['is_para_terphenyl(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No para-terphenyl core '
                                          'structure found"',
                                          'False, f"Atom {atom.GetSymbol()} '
                                          'not allowed in para-terphenyls"',
                                          'False, "No allowed functional '
                                          'groups found"',
                                          'False, "Molecular weight out of '
                                          'expected range for para-terphenyls"',
                                          'False, "Number of rings out of '
                                          'expected range for para-terphenyls"',
                                          'True, "Meets structural and '
                                          'functional group requirements for '
                                          'para-terphenyls"'],
                           'returns_count': 7,
                           'complexity': 4.737775890822787},
    'message': '\n'
               'Attempt failed: F1 score of 0.6571428571428571 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O(C1=C(OC)C(C2=CC=CC=C2)=CC(=C1C3=CC=C(OC)C=C3)OC)C NAME: '
               'Floricolin S REASON: CORRECT Contains para-terphenyl core and '
               'allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)CCC)C(=C(O)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)CC4=CC=CC=C4 '
               'NAME: Terrestrin C REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)CCC2=CC=CC=C2)C(=C1C3=CC=C(O)C=C3)O)C4=CC=C(O)C=C4)[C@@H]5CC(C)=CC5 '
               'NAME: '
               '[2,5-dihydroxy-3,6-bis(4-hydroxyphenyl)-4-(3-phenylpropanoyloxy)phenyl] '
               '3-methylcyclopent-3-ene-1-carboxylate REASON: CORRECT Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)C[C@H](O)C)C(=C(OC(=O)C)C(=C1C2=CC=C(O)C=C2)OC(=O)CCC3=CC=CC=C3)C4=CC=C(O)C=C4)C[C@H](O)C '
               'NAME: Curtisian V REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)C[C@@H](O)C)C(=C(OC(=O)C[C@@H](O)C)C(=C1C2=CC=C(O)C=C2)OC(=O)CCC3=CC=CC=C3)C4=CC=C(O)C=C4)C[C@@H](OC(=O)C)C '
               'NAME: Curtisian H REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: O(C1=C(O)C(C2=CC=CC=C2)=CC(=C1C3=CC=CC=C3)O)C NAME: '
               '3-methoxy-2,5-diphenylbenzene-1,4-diol REASON: CORRECT '
               'Contains para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=C(O)C=C3)C=C2OC)C=C1)CC=C(C)C '
               'NAME: 3-Methoxyterprenin REASON: CORRECT Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: COc1cc(-c2ccccc2)c(OC)c(O)c1-c1ccc(O)cc1 NAME: '
               "4''-deoxyterphenyllin REASON: CORRECT Contains para-terphenyl "
               'core and allowed functional group CO\n'
               ' * SMILES: COc1cc(-c2ccc(O)cc2)c(OC)c(O)c1-c1ccc(O)c(O)c1 '
               'NAME: 3-hydroxyterphenyllin REASON: CORRECT Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'CC(=O)Oc1c(OC(C)=O)c(-c2ccc(O)cc2)c(OC(=O)c2ccccc2)c(OC(C)=O)c1-c1ccc(O)cc1 '
               'NAME: curtisian A REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: COc1c(O)c(c(O)cc1-c1ccc(O)cc1)-c1ccc(O)c(O)c1 NAME: '
               "3-hydroxy-6'-O-desmethylterphenyllin REASON: CORRECT Contains "
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)CCC)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)CC4=CC=CC=C4 '
               'NAME: Thelephantin D REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C '
               'NAME: Prenylterphenyllin F REASON: CORRECT Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O(C1=C(O)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)CC=C(C)C '
               "NAME: 4''-deoxyterprenin REASON: CORRECT Contains "
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O1[C@@H](OC2=C(O)C(=C(O)C=C2C3=CC=CC=C3)C4=CC=CC=C4)C[C@H](O)[C@H]([C@H]1C)O '
               'NAME: Terfestatin D REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'COc1cc(-c2ccc(O)cc2)c(OC)c(O)c1-c1ccc(O)c(CC=C(C)C)c1 NAME: '
               'prenylterphenyllin REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=CC=C(C2=C(O)C(O)=C(C3=CC=C(OC(=O)CC4=CC=CC=C4)C=C3)C(=C2O)O)C=C1)CC5=CC=CC=C5 '
               'NAME: Ganbajunin C REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)CC2=CC=CC=C2)C(=C1C3=CC=C(O)C=C3)O)C4=CC=C(O)C=C4)CC5=CC=CC=C5 '
               'NAME: Ganbajunin E REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)C[C@@H](OC(=O)C)C)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C[C@@H](OC(=O)C)C '
               'NAME: Curtisian M REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)C)C(=C(O)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)CC4=CC=CC=C4 '
               'NAME: Terrestrin D REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)CCC2=CC=CC=C2)C(=C(OC(=O)C[C@@H](O)C)C(=C1C3=CC=C(O)C=C3)OC(=O)C)C4=CC=C(O)C=C4)C[C@@H](O)C '
               'NAME: Curtisian E REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)C)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C '
               'NAME: Kynapcin-12 REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)C)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C[C@@H](OC(=O)C)C '
               'NAME: Curtisian N REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               ' * SMILES: O(C1=C(O)C(C2=CC=C(OC)C=C2)=CC(=C1C3=CC=CC=C3)OC)C '
               'NAME: Floricolin T REASON: CORRECT Contains para-terphenyl '
               'core and allowed functional group CO\n'
               ' * SMILES: '
               'O(C1=C(OC)C(=C(O)C(=C1C2=CC=C(OC)C=C2)O)C3=CC=C(OC)C=C3)C '
               'NAME: Rickenyl A REASON: CORRECT Contains para-terphenyl core '
               'and allowed functional group CO\n'
               'False positives: SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)C[C@@H](C(C)C)C)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C4=CC=C(O)C=C4 '
               'NAME: Thelephantin C REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: c1ccc2c(c1)c1cccc3c4c5ccccc5c5cccc(c2c13)c45 NAME: '
               'rubicene REASON: WRONGLY CLASSIFIED Contains para-terphenyl '
               'core with allowed substituents\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)C2=CC=CC=C2)C(=C(O)C(=C1C3=CC=C(O)C=C3)OC(=O)C4=CC=CC=C4)C5=CC=C(O)C=C5)C6=CC=CC=C6 '
               'NAME: Thelephantin K REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: O1C2=C(O)C(C3=CC=C(O)C=C3)=CC(=C2C4=C1C=CC=C4)OC '
               'NAME: Floricolin M REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C2OC=3C=C(O)C(=CC3C2=C(OC(=O)C)C4=C1C5=C(C=C(O)C(=C5)O)O4)O)C '
               'NAME: Polyozellin REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: c1ccc2c(c1)cc1ccc3cc4c5ccccc5cc5ccc6cc2c1c3c6c45 '
               'NAME: pyranthrene REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core with allowed substituents\n'
               ' * SMILES: '
               'c1cc2c3ccc4ccc5c6ccc7ccc8c9ccc1c1c2c2c(c91)c1c8c7c6c1c1c5c4c3c21 '
               'NAME: circumtrindene REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core with allowed substituents\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)C)C(=C(O)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C4=CC=CC=C4 '
               'NAME: Concrescenin A REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O1C2=C(C=3C1=CC(O)=C(OC(=O)C)C3)C(OC(=O)C)=C(OC(=O)C)C(=C2OC(=O)C)C4=CC=C(O)C=C4 '
               'NAME: '
               '1,2,4,8-Tetraacetoxy-7-hydroxy-3-(4-hydroxyphenyl)dibenzofuran '
               'REASON: WRONGLY CLASSIFIED Contains para-terphenyl core and '
               'allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)C[C@H](OC(=O)C)C)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C4=CC=CC=C4 '
               'NAME: Curtisian T REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O1C2=C(C(O)=C(O)C(=C2C3=C1C4=C(O)C=CC=C4C=C3)C5=CC=CC=C5)C6=CC=CC=C6 '
               'NAME: Allantonaphthofuran A REASON: WRONGLY CLASSIFIED '
               'Contains para-terphenyl core with allowed substituents\n'
               ' * SMILES: '
               'c1cc2cccc3c4ccc5c6cccc7cccc(c8ccc(c(c1)c23)c4c58)c67 NAME: '
               'terrylene REASON: WRONGLY CLASSIFIED Contains para-terphenyl '
               'core with allowed substituents\n'
               ' * SMILES: '
               'O=C(OC1=C(OC(=O)CC2=CC=CC=C2)C(=C(O)C(=C1C3=CC=C(O)C=C3)O)C4=CC=C(O)C=C4)C5=CC=CC=C5 '
               'NAME: Thelephantin O REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(C(OC(=O)CC2=CC=CC=C2)=C(OC(=O)CC3=CC=CC=C3)C4=C1OC=5C=C(O)C(=CC45)O)C6=CC=C(O)C=C6)C7=CC=C(O)C=C7 '
               'NAME: Terrestrin G REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: COc1cc(-c2ccc(O)cc2)c(OC)c2oc3cc(O)c(O)cc3c12 NAME: '
               'candidusin A REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(C(O)=C(O)C2=C1OC=3C=C(O)C(=CC23)O)C4=CC=C(O)C=C4)C '
               'NAME: Boletopsin A REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(O)C(=C(OC(=O)CCC)C(=C1C2=CC=C(O)C=C2)O)C3=CC=C(O)C=C3)C4=CC=C(O)C=C4 '
               'NAME: Thelephantin A REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O1C2=C(OC)C(C3=CC=CC=C3)=CC(=C2C4=C1C=C(O)C(=C4)OCC=C(C)C)OC '
               'NAME: Prenylcandidusin E REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'CCCCCCCCc1ccc(cc1)-c1c(-c2ccc(CCCCCCCC)cc2)c(-c2ccc(Br)cc2)c2-c3cccc4cccc(-c2c1-c1ccc(Br)cc1)c34 '
               'NAME: '
               '7,10-bis(4-bromophenyl)-8,9-bis(4-octylphenyl)fluoranthene '
               'REASON: WRONGLY CLASSIFIED Contains para-terphenyl core with '
               'allowed substituents\n'
               ' * SMILES: '
               'O1C2=C(OC)C(C3=CC=CC=C3)=CC(=C2C4=C1C=C(O)C(=C4)O)OC NAME: '
               '4′′-deoxycandidusin A REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'c1cc2cc3ccc4cc5cc6ccc7cc8ccc9cc%10ccc%11cc%12cc%13ccc%14cc1c1c2c2c3c4c3c5c4c6c7c5c8c9c6c%10c%11c7c%12c8c%13c%14c1c1c2c3c2c4c5c6c7c2c81 '
               'NAME: circumovalene REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core with allowed substituents\n'
               ' * SMILES: '
               'O1C2=C(C=C(C3=C(OC)C=4OC=5C=C(OC)C(=CC5C4C(=C3)OC)O)C=C2)C=CC1(C)C '
               'NAME: Aspergicandidusin A REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(C(O)=C(OC(=O)CC2=CC=CC=C2)C3=C1OC=4C=C(O)C(=CC34)O)C5=CC=C(O)C=C5)C6=CC=C(O)C=C6 '
               'NAME: Thelephantin H REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O=C(OC1=C(C(OC(=O)C)=C(OC(=O)CC2=CC=CC=C2)C3=C1OC=4C=C(O)C(=CC34)O)C5=CC=C(O)C=C5)CC6=CC=CC=C6 '
               'NAME: Terrestrin F REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               ' * SMILES: '
               'O1C2=C(OC)C(C3=CC(OC)=C(O)C(=C3)CC=C(C)C)=CC(=C2C4=C1C=C(OC)C(=C4)OC)OC '
               'NAME: Prenylcandidusin F REASON: WRONGLY CLASSIFIED Contains '
               'para-terphenyl core and allowed functional group CO\n'
               'False negatives: SMILES: '
               'S1C2=C(C(O)=C(OC)C(=C2N=C1)C3=CC=C(OC)C=C3)C4=CC=C(OC)C=C4 '
               'NAME: '
               '4,7-bis(4-methoxyphenyl)-6-hydroxy-5-methoxybenzo[d]thiazole '
               'REASON: MISSED Atom S not allowed in para-terphenyls\n'
               ' * SMILES: '
               'S(=O)(=O)(OC1=C(C(OC)=C(O)C(=C1)C2=CC=C(OC)C=C2)C3=CC=C(O)C=C3)O '
               'NAME: Talarophenol sulfate REASON: MISSED Atom S not allowed '
               'in para-terphenyls\n'
               ' * SMILES: '
               'S1C(=O)N(C)C=2C1=C(C(O)=C(O[C@@H]3O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]3O)O)C2C4=CC=CC=C4)C5=CC=CC=C5 '
               'NAME: Echoside E REASON: MISSED Atom S not allowed in '
               'para-terphenyls\n'
               ' * SMILES: '
               'S1C2=C(C(O)=C(O[C@@H]3O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]3O)O)C(=C2N=C1)C4=CC=CC=C4)C5=CC=CC=C5 '
               'NAME: Echoside D REASON: MISSED Atom S not allowed in '
               'para-terphenyls\n'
               ' * SMILES: '
               'S1C2=C(NC(C1)=O)C(=C(OC)C(=C2C3=CC=C(OC)C=C3)O)C4=CC=C(OC)C=C4 '
               'NAME: Nocarterphenyl B REASON: MISSED Atom S not allowed in '
               'para-terphenyls\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n'
               'IMPORTANT NOTE: I do not have 100% confidence in the benchmark '
               'I am using. There may be occasional and systematic mistakes. '
               'Use your best judgment, and if you think the classifications '
               'your program are consistent with your understanding if the '
               'meaning of the chemical class, then you can ignore outliers, '
               'but explain your reasoning in doing so. I have great '
               'confidence in your broad understanding of chemistry and your '
               'ability to translate this into code.',
    'sample_true_negatives': [   {   'smiles': 'O=C(O)[C@@H](N)CCC1C=CC(N)C=C1',
                                     'name': 'Amiclenomycin',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': '[H]C(=O)OP(O)(O)=O',
                                     'name': 'formyl dihydrogen phosphate',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=C(O)C=CC(=C2)C(O)=O)C(O)=O',
                                     'name': '6-(5-carboxy-2-hydroxyphenoxy)-3,4,5-trihydroxyoxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'CC(C)CC#CC1=CC=C(C=C1)[C@@H]2[C@@H]3CN(CC(=O)N3[C@@H]2CO)C(=O)C4=CC(=CC=C4)F',
                                     'name': '(6R,7R,8S)-4-[(3-fluorophenyl)-oxomethyl]-8-(hydroxymethyl)-7-[4-(4-methylpent-1-ynyl)phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(C)O',
                                     'name': '17,20-dihydroxypregn-4-en-3-one',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'NCCCCC(CN)CCCN',
                                     'name': '4-(aminomethyl)octane-1,8-diamine',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'O=C1N[C@@H](CC2=CC=CC=C2)[C@H]3[C@]1(O)[C@@H](/C=C/C[C@@H]([C@H](O)C(=O)C)C)[C@H](O)C(C)=C3C',
                                     'name': 'Cytochalasin Z14',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C)[C@@H](C)CO)C)CN(C)C(=O)C3CCCCC3',
                                     'name': 'N-[[(3R,9S,10S)-12-[(2S)-1-hydroxypropan-2-yl]-16-(methanesulfonamido)-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methylcyclohexanecarboxamide',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(C)C',
                                     'name': 'Glu-Leu-Asp',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'},
                                 {   'smiles': 'CC(O)\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC([O-])=O',
                                     'name': '19-HEPE(1-)',
                                     'reason': 'No para-terphenyl core '
                                               'structure found'}],
    'sample_false_negatives': [   {   'smiles': 'S1C2=C(C(O)=C(OC)C(=C2N=C1)C3=CC=C(OC)C=C3)C4=CC=C(OC)C=C4',
                                      'name': '4,7-bis(4-methoxyphenyl)-6-hydroxy-5-methoxybenzo[d]thiazole',
                                      'reason': 'Atom N not allowed in '
                                                'para-terphenyls'},
                                  {   'smiles': 'S1C(=O)N(C)C=2C1=C(C(O)=C(O[C@@H]3O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]3O)O)C2C4=CC=CC=C4)C5=CC=CC=C5',
                                      'name': 'Echoside E',
                                      'reason': 'Atom N not allowed in '
                                                'para-terphenyls'},
                                  {   'smiles': 'O1C2(OC=3C(C4=CC=C(O)C=C4)=C5OC6(O[C@@H]([C@@H](O)C=C6)C)OC5=C(C3O2)C7=CC=C(O)C=C7)C=C[C@@H]([C@H]1C)O',
                                      'name': 'Spiromentin H',
                                      'reason': 'Number of rings out of '
                                                'expected range for '
                                                'para-terphenyls'},
                                  {   'smiles': 'S1C2=C(C(O)=C(O[C@@H]3O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]3O)O)C(=C2N=C1)C4=CC=CC=C4)C5=CC=CC=C5',
                                      'name': 'Echoside D',
                                      'reason': 'Atom N not allowed in '
                                                'para-terphenyls'},
                                  {   'smiles': 'S1C2=C(NC(C1)=O)C(=C(OC)C(=C2C3=CC=C(OC)C=C3)O)C4=CC=C(OC)C=C4',
                                      'name': 'Nocarterphenyl B',
                                      'reason': 'Atom N not allowed in '
                                                'para-terphenyls'},
                                  {   'smiles': 'c1ccc(cc1)-c1ccc(cc1)-c1ccccc1',
                                      'name': '1,4-diphenylbenzene',
                                      'reason': 'No allowed functional groups '
                                                'found'}],
    'attempt': 1,
    'reasoning': 'The previous program attempted to classify molecules as '
                 'para-terphenyls based on the presence of the para-terphenyl '
                 'core structure and the presence of certain allowed '
                 'functional groups and substituents. However, the outcomes '
                 'indicate that while the program correctly identified many '
                 'para-terphenyls, it also misclassified several molecules and '
                 'missed some true para-terphenyls.\n'
                 '\n'
                 'Here are some potential reasons for the misclassifications '
                 'and missed cases:\n'
                 '\n'
                 '1. **Missed cases**: The program missed some true '
                 'para-terphenyls because it did not account for certain atoms '
                 'or functional groups that are allowed in this class. For '
                 'example, it missed molecules containing sulfur atoms, which '
                 'are present in some natural product para-terphenyls.\n'
                 '\n'
                 '2. **False positives**: The program classified some '
                 'molecules as para-terphenyls even though they did not '
                 'contain the core para-terphenyl structure. This could be due '
                 'to the SMARTS pattern used to detect the core structure '
                 'being too permissive or not specific enough.\n'
                 '\n'
                 '3. **False positives**: The program classified some '
                 'molecules as para-terphenyls based solely on the presence of '
                 'allowed functional groups, even though they did not contain '
                 'the core para-terphenyl structure.\n'
                 '\n'
                 '4. **False negatives**: The program may have missed some '
                 'true para-terphenyls because it did not account for certain '
                 'allowed substituents or functional groups that were not '
                 'included in the initial list.\n'
                 '\n'
                 'To improve the program, we can take the following steps:\n'
                 '\n'
                 '1. **Refine the core structure pattern**: Review the SMARTS '
                 'pattern used to detect the para-terphenyl core structure and '
                 'make it more specific to avoid false positives.\n'
                 '\n'
                 '2. **Expand the list of allowed atoms and functional '
                 'groups**: Analyze the false negatives and missed cases to '
                 'identify additional atoms and functional groups that should '
                 'be allowed in para-terphenyls. Incorporate these into the '
                 'program.\n'
                 '\n'
                 '3. **Use a more comprehensive approach**: Instead of relying '
                 'solely on the presence of the core structure and allowed '
                 'functional groups, consider using a more comprehensive '
                 'approach that combines structural patterns, atom and '
                 'functional group checks, and other molecular descriptors '
                 '(e.g., molecular weight, number of rings, etc.) to improve '
                 'the accuracy of the classification.\n'
                 '\n'
                 '4. **Utilize expert knowledge**: If there are cases where '
                 'the benchmark classifications seem inconsistent with your '
                 'understanding of the chemical class, you can use your expert '
                 'knowledge to override or adjust the classifications as '
                 'needed, while providing a clear explanation for the '
                 'reasoning.\n'
                 '\n'
                 'By iteratively refining the program based on the outcomes '
                 'and incorporating expert knowledge, we can improve the '
                 'accuracy of the para-terphenyl classification.\n'
                 '\n'
                 "Here's an updated version of the program that incorporates "
                 'some of these improvements:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 68,
    'num_false_positives': 13,
    'num_true_negatives': 142213,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.8395061728395061,
    'recall': 0.918918918918919,
    'f1': 0.8774193548387097,
    'accuracy': 0.9998664792691497,
    'negative_predictive_value': 0.9999578115441679}