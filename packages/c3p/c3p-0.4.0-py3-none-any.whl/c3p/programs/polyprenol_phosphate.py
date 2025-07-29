"""
Classifies: CHEBI:16460 polyprenol phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_polyprenol_phosphate(smiles: str):
    """
    Determines if a molecule is a polyprenol phosphate based on its SMILES string.
    A polyprenol phosphate is a prenol phosphate resulting from the formal condensation
    of the terminal allylic hydroxy group of a polyprenol with 1 mol eq. of phosphoric acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyprenol phosphate, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phosphate group (OP(O)(=O)O or OP(O)(O)=O)
    phosphate_pattern = Chem.MolFromSmarts("[OX2]P(=O)([OX2])[OX2]")
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Check for polyprenol chain (at least 2 isoprene units)
    # More flexible pattern to account for different bond types and stereochemistry
    isoprene_pattern = Chem.MolFromSmarts("[C]=[C]-[C]-[C]-[C]=[C]")
    isoprene_matches = mol.GetSubstructMatches(isoprene_pattern)
    if len(isoprene_matches) < 2:
        return False, f"Found {len(isoprene_matches)} isoprene units, need at least 2"

    # Check that the phosphate is attached to the terminal carbon of the polyprenol chain
    # The phosphate should be connected to a carbon with a single hydroxyl group
    # More specific pattern to ensure proper attachment
    terminal_phosphate_pattern = Chem.MolFromSmarts("[C]([OX2]P(=O)([OX2])[OX2])~[C]=[C]")
    if not mol.HasSubstructMatch(terminal_phosphate_pattern):
        return False, "Phosphate not properly attached to terminal carbon of polyprenol chain"

    # Check for long carbon chain (at least 6 carbons)
    carbon_chain_pattern = Chem.MolFromSmarts("[C]~[C]~[C]~[C]~[C]~[C]")
    if not mol.HasSubstructMatch(carbon_chain_pattern):
        return False, "No long carbon chain found"

    # Check molecular weight - polyprenol phosphates typically have MW > 200 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200:
        return False, "Molecular weight too low for polyprenol phosphate"

    return True, "Contains polyprenol chain with terminal phosphate group properly attached"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16460',
                          'name': 'polyprenol phosphate',
                          'definition': 'A prenol phosphate resulting from the '
                                        'formal condensation of the terminal '
                                        'allylic hydroxy group of a polyprenol '
                                        'with 1 mol eq. of phosphoric acid.',
                          'parents': ['CHEBI:26250', 'CHEBI:26875'],
                          'xrefs': ['KEGG:C01048'],
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
                                                 2,
                                                 0,
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
                                                 'MolFromSmiles',
                                                 'CalcExactMolWt'],
                           'methods_called_count': 5,
                           'smarts_strings': [   '[C]=[C]-[C]-[C]-[C]=[C]',
                                                 '[C]([OX2]P(=O)([OX2])[OX2])~[C]=[C]',
                                                 '[OX2]P(=O)([OX2])[OX2]',
                                                 '[C]~[C]~[C]~[C]~[C]~[C]'],
                           'smarts_strings_count': 4,
                           'defs': ['is_polyprenol_phosphate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No phosphate group found"',
                                          'False, f"Found '
                                          '{len(isoprene_matches)} isoprene '
                                          'units, need at least 2"',
                                          'False, "Phosphate not properly '
                                          'attached to terminal carbon of '
                                          'polyprenol chain"',
                                          'False, "No long carbon chain found"',
                                          'False, "Molecular weight too low '
                                          'for polyprenol phosphate"',
                                          'True, "Contains polyprenol chain '
                                          'with terminal phosphate group '
                                          'properly attached"'],
                           'returns_count': 7,
                           'complexity': 3.7327123292259294},
    'message': '\n'
               'Attempt failed: F1 score of 0.888888888888889 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@H]1OC(OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)[C@H](NC(C)=O)[C@@H](O)[C@H]1O '
               'NAME: N-acetyl-D-fucosaminyl undecaprenyl diphosphate REASON: '
               'CORRECT Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               'C[C@H]1OC(OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)[C@H](NC(C)=O)[C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](NC(C)=O)[C@@H]2NC(C)=O)C(O)=O)[C@H]1O '
               'NAME: '
               '2,3-diacetamido-2,3-dideoxy-beta-D-mannosyl-(1->3)-N-acetyl-D-fucosaminyl '
               'undecaprenyl diphosphate REASON: CORRECT Contains polyprenol '
               'chain with terminal phosphate group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)OP(O)(O)=O '
               'NAME: (2Z,6Z,10Z,14Z,18Z,22Z,26Z,30Z,34E)-decaprenyl '
               'diphosphate REASON: CORRECT Contains polyprenol chain with '
               'terminal phosphate group properly attached\n'
               ' * SMILES: '
               '[H]C(CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])COP(O)(=O)OP(O)(O)=O)=C(C)CCC=C(C)C '
               'NAME: dodecaprenyl diphosphate REASON: CORRECT Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]2O[C@H]2[C@@H](O)[C@@H](CO)O[C@H](O[C@H]3[C@@H](O)[C@@H](CO)O[C@H](OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)[C@@H]3NC(C)=O)[C@@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-L-Fuc-(1->2)-beta-D-Gal-(1->3)-alpha-D-GalNAc-(1->3)-alpha-D-GalNAc-diphospho-ditrans,octacis-undecaprenol '
               'REASON: CORRECT Contains polyprenol chain with terminal '
               'phosphate group properly attached\n'
               ' * SMILES: '
               '[H]C(CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])COP(O)(=O)OP(O)(O)=O)=C(C)CCC=C(C)C '
               'NAME: octadecaprenyl diphosphate REASON: CORRECT Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O '
               'NAME: all-trans-decaprenyl diphosphate REASON: CORRECT '
               'Contains polyprenol chain with terminal phosphate group '
               'properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)O[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: trans,octacis-decaprenylphospho-beta-D-ribofuranose '
               '5-phosphate REASON: CORRECT Contains polyprenol chain with '
               'terminal phosphate group properly attached\n'
               ' * SMILES: '
               'O(P(OP(O[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1NC(=O)C)O)O[C@@H]2O[C@@H]([C@H]([C@@H]([C@H]2O)O)O)CO)CO)(O)=O)(O)=O)C/C=C(/C)\\CC/C=C(/C)\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)/C)/C)/C)/C)/C '
               'NAME: beta-D-glucosyl-(1->4)-N-acetyl-alpha-D-glucosaminyl '
               'undecaprenyl diphosphate REASON: CORRECT Contains polyprenol '
               'chain with terminal phosphate group properly attached\n'
               ' * SMILES: '
               '[H]C(CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])COP(O)(=O)OP(O)(O)=O)=C(C)CCC=C(C)C '
               'NAME: pentaprenyl diphosphate REASON: CORRECT Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'O(P(OP(O[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1NC(=O)C)O)O[C@@H]2O[C@@H]([C@H]([C@@H]([C@H]2NC(=O)C)O)OP(OC[C@@H](CO)O)(O)=O)CO)CO)(O)=O)(O)=O)C/C=C(/C)\\CC/C=C(/C)\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)/C)/C)/C)/C)/C '
               'NAME: '
               '4-O-[(2R)-1-glycerylphosphono]-N-acetyl-beta-D-mannosaminyl-(1->4)-N-acetyl-alpha-D-glucosaminyl '
               'undecaprenyl diphosphate REASON: CORRECT Contains polyprenol '
               'chain with terminal phosphate group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)OP(O)(=O)O[C@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O)[C@H]2O)[C@H](O)[C@H]1O '
               'NAME: '
               'alpha-D-Man-(1->3)-beta-D-Glc-(1->4)-alpha-D-Glc-1-diphospho-ditrans,polycis-undecaprenol '
               'REASON: CORRECT Contains polyprenol chain with terminal '
               'phosphate group properly attached\n'
               ' * SMILES: '
               '[H]C(CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])COP(O)(=O)OP(O)(=O)O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O[C@@H]2O[C@@H](C)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O)[C@@H](O)[C@H]2O)[C@H]1O)=C(C)CCC=C(C)C '
               'NAME: '
               'alpha-D-mannosyl-(1->4)-alpha-L-rhamnosyl-(1->3)-beta-D-galactosyl-1-diphosphodecaprenol '
               'REASON: CORRECT Contains polyprenol chain with terminal '
               'phosphate group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(O)=O '
               'NAME: ditrans,polycis-undecaprenyl phosphate REASON: CORRECT '
               'Contains polyprenol chain with terminal phosphate group '
               'properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O '
               'NAME: all-trans-tridecaprenyl diphosphate REASON: CORRECT '
               'Contains polyprenol chain with terminal phosphate group '
               'properly attached\n'
               ' * SMILES: '
               'C[C@@H](NC(=O)[C@@H](C)NC(=O)[C@H](CCCCNC(=O)CNC(=O)CNC(=O)CNC(=O)CNC(=O)CN)NC(=O)CC[C@@H](NC(=O)[C@H](C)NC(=O)[C@@H](C)O[C@@H]1[C@@H](NC(C)=O)[C@H](O[C@H](CO)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1NC(C)=O)OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)C(N)=O)C(O)=O '
               'NAME: '
               'undecaprenyldiphospho-N-acetyl-(N-acetylglucosaminyl)muramoyl-L-alanyl-D-isoglutaminyl-(glycyl)5-L-lysyl-D-alanyl-D-alanine '
               'REASON: CORRECT Contains polyprenol chain with terminal '
               'phosphate group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP(O)(O)=O '
               'NAME: decaprenol phosphate REASON: CORRECT Contains polyprenol '
               'chain with terminal phosphate group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)O[C@@H]1O[C@H](CO)[C@@H](O)C1=O '
               'NAME: '
               'trans,octacis-decaprenylphospho-beta-D-erythro-pentofuranosid-2-ulose '
               'REASON: CORRECT Contains polyprenol chain with terminal '
               'phosphate group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP(O)(O)=O '
               'NAME: undecaprenyl dihydrogen phosphate REASON: CORRECT '
               'Contains polyprenol chain with terminal phosphate group '
               'properly attached\n'
               ' * SMILES: CC(C)=CCCC(C)=CCCC(C)=CCCC(C)=CCOP(O)(=O)OP(O)(O)=O '
               'NAME: geranylgeranyl diphosphate REASON: CORRECT Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'C[C@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)[C@H](NC(C)=O)[C@@H](O[C@H]2O[C@H](CO)[C@H](O[C@H]3O[C@H](CO)[C@H](O[C@H]4O[C@H](CO)[C@H](O[C@H]5O[C@H](CO)[C@H](O[C@H]6O[C@H](CO)[C@H](O)[C@H](O)[C@H]6NC(C)=O)[C@H](O)[C@H]5NC(C)=O)[C@H](O)[C@H]4NC(C)=O)[C@H](O)[C@H]3NC(C)=O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1NC(C)=O '
               'NAME: '
               '[alpha-D-GalNAc-(1->4)]4-alpha-D-GalNAc-(1->3)-alpha-D-diNAcBac-tritrans,heptacis-undecaprenyl '
               'diphosphate REASON: CORRECT Contains polyprenol chain with '
               'terminal phosphate group properly attached\n'
               ' * SMILES: '
               '[H]C(CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])COP(O)(=O)OP(O)(O)=O)=C(C)CCC=C(C)C '
               'NAME: nonaprenyl diphosphate REASON: CORRECT Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)OP(O)(O)=O '
               'NAME: ditrans,polycis-tetradecaprenyl diphosphate REASON: '
               'CORRECT Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               '[H]C(CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])CCC(C)=C([H])COP(O)(=O)OP(O)(O)=O)=C(C)CCC=C(C)C '
               'NAME: hexaprenyl diphosphate REASON: CORRECT Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](CO)OC1OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: beta-D-glucosyl-(1->4)-N-acetyl-D-glucosaminyl '
               'undecaprenyl diphosphate REASON: CORRECT Contains polyprenol '
               'chain with terminal phosphate group properly attached\n'
               'False positives: SMILES: '
               'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O '
               'NAME: ditrans,polycis-octaprenyl diphosphate REASON: WRONGLY '
               'CLASSIFIED Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               'P(=O)(OC1C=CC(=CCC(OC(=O)CC(=C)C(CC=CC=CC=CC=CC(=CC1O)C)C)/C=C/C(/C=C\\C=C)C)C)(O)O '
               'NAME: Rowithocin A REASON: WRONGLY CLASSIFIED Contains '
               'polyprenol chain with terminal phosphate group properly '
               'attached\n'
               ' * SMILES: '
               'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O '
               'NAME: ditrans,polycis-nonaprenyl diphosphate REASON: WRONGLY '
               'CLASSIFIED Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O '
               'NAME: ditrans,polycis-heptaprenyl diphosphate REASON: WRONGLY '
               'CLASSIFIED Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)OP(O)(O)=O '
               'NAME: ditrans,polycis-pentaprenyl diphosphate REASON: WRONGLY '
               'CLASSIFIED Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H](OC([C@@H]1NC(C)=O)OP(OP(OC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)(O)=O)(O)=O)CO)O[C@H]2[C@@H]([C@H]([C@H](O)[C@H](O2)CO)O)NC(C)=O)OC(C(N[C@H](C(NC(CCC(N[C@H](C(N[C@@H](C(N[C@@H](C(O)=O)C)=O)C)=O)CCCCNC([C@@H](N)C)=O)=O)C(O)=O)=O)C)=O)C '
               'NAME: '
               'Undecaprenyl-diphospho-N-acetylmuramoyl-(N-acetylglucosamine)-L-alanyl-gamma-D-glutamyl-L-lysyl-(L-alanyl)-D-alanyl-D-alanine '
               'REASON: WRONGLY CLASSIFIED Contains polyprenol chain with '
               'terminal phosphate group properly attached\n'
               ' * SMILES: '
               'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O '
               'NAME: ditrans,polycis-hexaprenyl diphosphate REASON: WRONGLY '
               'CLASSIFIED Contains polyprenol chain with terminal phosphate '
               'group properly attached\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](O)[C@@H]([C@H]([C@@H]1OP(=O)(O)OC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC/C=C(\\CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)/C)O)O)C(O)=O '
               'NAME: ditrans,polycis-dodecaprenyl phosphate-GalA REASON: '
               'WRONGLY CLASSIFIED Contains polyprenol chain with terminal '
               'phosphate group properly attached\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H](OC([C@@H]1NC(C)=O)OP(OP(OC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)(O)=O)(O)=O)CO)O[C@H]2[C@@H]([C@H]([C@H](O)[C@H](O2)CO)O)NC(C)=O)OC(C(N[C@H](C(NC(CCC(N[C@H](C(N[C@@H](C(N[C@@H](C(O)=O)C)=O)C)=O)CCCCNC([C@@H](NC([C@@H](N)C)=O)C)=O)=O)C(O)=O)=O)C)=O)C '
               'NAME: '
               'Undecaprenyl-diphospho-N-acetylmuramoyl-(N-acetylglucosamine)-L-alanyl-gamma-D-glutamyl-L-lysyl-(L-alanyl-L-alanyl)-D-alanyl-D-alanine '
               'REASON: WRONGLY CLASSIFIED Contains polyprenol chain with '
               'terminal phosphate group properly attached\n'
               'False negatives: SMILES: '
               'CC(C)=CCCC(C)=CCCC(C)=CCOP(O)(=O)OP(O)(O)=O NAME: farnesyl '
               'diphosphate REASON: MISSED Found 2 isoprene units, need at '
               'least 3\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC\\C(C)=C\\COP(O)(O)=O NAME: '
               'phytyl phosphate REASON: MISSED Found 0 isoprene units, need '
               'at least 3\n'
               ' * SMILES: '
               'CC(CCOP(O)(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: beta-D-mannosyl C35-phosphodolichol REASON: MISSED '
               'Phosphate not properly attached to terminal carbon of '
               'polyprenol chain\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O NAME: '
               'geranyl diphosphate REASON: MISSED Found 1 isoprene units, '
               'need at least 3\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CCC(C)(OP(O)(=O)OP(O)(O)=O)C=C '
               'NAME: nerolidyl diphosphate REASON: MISSED Found 1 isoprene '
               'units, need at least 3\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/COP(O)(=O)OP(O)(O)=O NAME: neryl '
               'diphosphate REASON: MISSED Found 1 isoprene units, need at '
               'least 3\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)OP(O)(O)=O '
               'NAME: 2-cis,6-cis-farnesyl diphosphate REASON: MISSED Found 2 '
               'isoprene units, need at least 3\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O '
               'NAME: phytyl diphosphate REASON: MISSED Found 0 isoprene '
               'units, need at least 3\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/COP(O)(=O)OP(O)(O)=O '
               'NAME: 2-cis,6-trans-farnesyl diphosphate REASON: MISSED Found '
               '2 isoprene units, need at least 3\n'
               ' * SMILES: '
               'P(O[C@@H]1OC([C@@H](O)[C@H](O)C1O)CO)(OCCC[C@H](CCC[C@H](CCC[C@H](CCC[C@H](CCC[C@H](CCCCCCCCC)C)C)C)C)C)(O)=O '
               'NAME: Mannosyl-1beta-phosphomycoketide C34 REASON: MISSED '
               'Found 0 isoprene units, need at least 3\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1COCCN1C2=C(C=C(C=C2)C(F)(F)F)NC(=O)C3=CC(=CN=C3)Br',
                                     'name': '5-bromo-N-[2-(4-morpholinyl)-5-(trifluoromethyl)phenyl]-3-pyridinecarboxamide',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'C[C@H]1C[C@@H]2CC[C@@H](O2)[C@@H](C)C(=O)O[C@H](C)C[C@H]2CC[C@H](O2)[C@H](C)C(=O)O[C@@H](C)C[C@@H]2CC[C@@H](O2)[C@@H](C)C(=O)O[C@H](C)C[C@H]2CC[C@H](O2)[C@H](C)C(=O)O1',
                                     'name': 'Nonactin',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O1OC23C(C14C(C5C(C(CC5)C(CCC(C(C)C)C)C)(CC4)C)=CC2=O)(CCC(O)C3)C',
                                     'name': '5,9-Epidioxy-3-hydroxyergost-7-en-6-one',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'CC1=C(SC=C1)C(=O)N2CCCC(C2)CNS(=O)(=O)C3=CC=C(C=C3)OC',
                                     'name': '4-methoxy-N-[[1-[(3-methyl-2-thiophenyl)-oxomethyl]-3-piperidinyl]methyl]benzenesulfonamide',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC',
                                     'name': 'DG(16:0/0:0/20:1n9)',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'Oc1cc2CC3(O)COc4c(O)c(O)ccc4C3c2cc1O',
                                     'name': 'haematoxylin',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO',
                                     'name': 'beta-D-Glcp-(1->4)-beta-D-Galp',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O=C(N)C(/C=C/[N+]([O-])=NC(C(O)C)C)CCC',
                                     'name': 'Maniwamycin F',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O1C2=C(C(=O)C(C3=C(O)C=C(O)C=C3)=C1)C(OC)=CC(O)=C2',
                                     'name': 'Barpisoflavone A',
                                     'reason': 'No phosphate group found'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC\\C(C)=C\\COP(O)(O)=O',
                                      'name': 'phytyl phosphate',
                                      'reason': 'Found 0 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'CC(CCOP(O)(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C',
                                      'name': 'beta-D-mannosyl '
                                              'C35-phosphodolichol',
                                      'reason': 'Phosphate not properly '
                                                'attached to terminal carbon '
                                                'of polyprenol chain'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O',
                                      'name': 'geranyl diphosphate',
                                      'reason': 'Found 1 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CCC(C)(OP(O)(=O)OP(O)(O)=O)C=C',
                                      'name': 'nerolidyl diphosphate',
                                      'reason': 'Found 1 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C/COP(O)(=O)OP(O)(O)=O',
                                      'name': 'neryl diphosphate',
                                      'reason': 'Found 1 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O',
                                      'name': 'phytyl diphosphate',
                                      'reason': 'Found 0 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'P(O[C@@H]1OC([C@@H](O)[C@H](O)C1O)CO)(OCCC[C@H](CCC[C@H](CCC[C@H](CCC[C@H](CCC[C@H](CCCCCCCCC)C)C)C)C)C)(O)=O',
                                      'name': 'Mannosyl-1beta-phosphomycoketide '
                                              'C34',
                                      'reason': 'Found 0 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'CC(C)CCCC(C)CCCC(C)CCC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O',
                                      'name': '(E)-3,7,11,15-tetramethylhexadec-2-en-1-yl '
                                              'diphosphate',
                                      'reason': 'Found 0 isoprene units, need '
                                                'at least 2'},
                                  {   'smiles': 'P(O[C@@H]1OC[C@@H](O)[C@H](O)C1O)(OCCC(CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)C)(O)=O',
                                      'name': 'dolichyl-4-D-xylosyl phosphate',
                                      'reason': 'Phosphate not properly '
                                                'attached to terminal carbon '
                                                'of polyprenol chain'},
                                  {   'smiles': 'CC(=CCC/C(=C/COP(O)(=O)O)/C)C',
                                      'name': 'geranyl phosphate',
                                      'reason': 'Found 1 isoprene units, need '
                                                'at least 2'}],
    'attempt': 5,
    'reasoning': 'The previous code had a few issues that led to both false '
                 'positives and false negatives:\n'
                 '\n'
                 '1. **False Positives**: The code incorrectly classified some '
                 'molecules because:\n'
                 '   - The phosphate pattern was too general and could match '
                 'phosphate groups not attached to the polyprenol chain.\n'
                 '   - The isoprene unit pattern was too flexible and could '
                 'match non-isoprene units.\n'
                 '   - The terminal phosphate attachment check was not strict '
                 'enough.\n'
                 '\n'
                 '2. **False Negatives**: The code missed some valid '
                 'polyprenol phosphates because:\n'
                 '   - The isoprene unit count requirement was too strict '
                 '(needing at least 3 units).\n'
                 '   - The terminal double bond check was too restrictive and '
                 'missed some valid structures.\n'
                 '   - The carbon chain length requirement was too strict.\n'
                 '\n'
                 'To improve the code, we need to:\n'
                 '- Make the phosphate attachment check more specific.\n'
                 '- Relax the isoprene unit count requirement.\n'
                 '- Remove the strict terminal double bond check.\n'
                 '- Adjust the carbon chain length requirement.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 101,
    'num_false_positives': 9,
    'num_true_negatives': 142180,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.9181818181818182,
    'recall': 0.9099099099099099,
    'f1': 0.914027149321267,
    'accuracy': 0.9998664792691497,
    'negative_predictive_value': 0.9999296715662143}