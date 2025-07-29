"""
Classifies: CHEBI:64583 sphingomyelin
"""
"""
Classifies: CHEBI:37550 sphingomyelin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_sphingomyelin(smiles: str):
    """
    Determines if a molecule is a sphingomyelin based on its SMILES string.
    A sphingomyelin has a sphingoid base with an amide-linked fatty acid and
    a phosphocholine group attached to the terminal hydroxyl.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sphingomyelin, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # More specific phosphocholine pattern that includes the ester linkage
    phosphocholine_pattern = Chem.MolFromSmarts("[N+](C)(C)CCOP(=O)([O-])O")
    if not mol.HasSubstructMatch(phosphocholine_pattern):
        return False, "No phosphocholine group found"

    # Check for amide linkage to fatty acid
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if len(amide_matches) != 1:
        return False, f"Found {len(amide_matches)} amide groups, need exactly 1"

    # More specific sphingoid base pattern that includes the characteristic structure
    sphingoid_pattern = Chem.MolFromSmarts("[C;H1,H2][C;H1,H2](O)[C;H1,H2][N;H1,H2]")
    if not mol.HasSubstructMatch(sphingoid_pattern):
        return False, "No sphingoid base pattern found"

    # Check molecular weight - sphingomyelins typically >500 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 500:
        return False, "Molecular weight too low for sphingomyelin"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 25:
        return False, "Too few carbons for sphingomyelin"
    if o_count < 5:
        return False, "Too few oxygens for sphingomyelin"

    # Count rotatable bonds to verify long chains
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 10:
        return False, "Chains too short for sphingomyelin"

    # Additional check for the characteristic sphingomyelin structure
    # Should have at least one long carbon chain (>= 12 carbons)
    long_chain_pattern = Chem.MolFromSmarts("[C;H2][C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]~[C;H2]")
    if not mol.HasSubstructMatch(long_chain_pattern):
        return False, "No long carbon chain found"

    return True, "Contains sphingoid base with amide-linked fatty acid and phosphocholine group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:64583',
                          'name': 'sphingomyelin',
                          'definition': 'Any of a class of phospholipids in '
                                        'which the amino group of a sphingoid '
                                        'base is in amide linkage with one of '
                                        'several fatty acids, while the '
                                        'terminal hydroxy group of the '
                                        'sphingoid base is esterified to '
                                        'phosphorylcholine.',
                          'parents': [   'CHEBI:140325',
                                         'CHEBI:35284',
                                         'CHEBI:35786',
                                         'CHEBI:36700'],
                          'xrefs': [   'LIPID_MAPS_class:LMSP0301',
                                       'PMID:27242221'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.7629629629629631 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[C@@H]([C@@H](/C=C/CCCCCCCC/C=C\\CCC)O)(COP(OCC[N+](C)(C)C)(=O)[O-])NC(=O)CCCCCCC/C=C\\CCCCCCCC '
               'NAME: N-oleoyl-(4E,14Z)-sphingadienine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxypentacosanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'C(CCCCCCCCCC)CCCC[C@@H](O)[C@@H](NC(CCCCCCCCC/C=C\\CCCCCC)=O)COP(=O)([O-])OCC[N+](C)(C)C '
               'NAME: N-[(11Z)-octadecenoyl]sphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-tricosanoyl-15-methylhexadecasphing-4-enine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               '[C@]([C@@](/C=C/CCCCCCCCCCC)(O)[H])(NC(=O)CCCCCCCCC/C=C\\CCCCCCCC)([H])COP(OCC[N+](C)(C)C)([O-])=O '
               'NAME: '
               'N-(11Z-eicosenoyl)-hexadecasphing-4-enine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxyoctacosanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-tricosanoyl-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxyicosanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-stearoylsphingosine-1-phosphocholine REASON: CORRECT '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-hexadecanoyl-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC/C=C/[C@H]([C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC(CCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)O '
               'NAME: SM(d18:0/20:2(11Z,14Z)) REASON: CORRECT Contains '
               'sphingoid base with amide-linked fatty acid and phosphocholine '
               'group\n'
               ' * SMILES: '
               'C(CCCCCCCCCC)CC\\C=C\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCC)COP(=O)([O-])OCC[N+](C)(C)C '
               'NAME: N-docosanoylsphingosine-1-phosphocholine REASON: CORRECT '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               '[C@]([C@@](/C=C/CCCCCCCCCCC)(O)[H])(NC(=O)CCCCCCCCCCCCCCCCCCCCC)([H])COP(OCC[N+](C)(C)C)([O-])=O '
               'NAME: N-(docosanoyl)-hexadecasphing-4-enine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxyhenicosanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               '[H][C@@](O)(\\C=C\\CCCCCCCCCCCCC)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCCCCCCCCCC '
               'NAME: N-myristoylsphingosine-1-phosphocholine REASON: CORRECT '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-icosanoylsphingosine-1-phosphocholine REASON: CORRECT '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@H]([C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC(CCCCCCCCCCCCC)=O)O '
               'NAME: SM(d18:0/14:0) REASON: CORRECT Contains sphingoid base '
               'with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-octacosanoyl-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-heneicosanoylsphingosine-1-phosphocholine REASON: '
               'CORRECT Contains sphingoid base with amide-linked fatty acid '
               'and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxytricosanoyl)-4-hydroxy-15-methylhexadecasphinganine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'O(P(OCC[N+](C)(C)C)(=O)[O-])C[C@@H]([C@@H](/C=C/CCCCCCCCC(CC)C)O)NC(CCCCCCCCCCCCCCCCCCCCC)=O '
               'NAME: '
               'N-docosanoyl-14-methylhexadecasphingosine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@H]([C@H](COP(=O)([O-])OCC[N+](C)(C)C)NC(CCCCCCCCCCCCCCCCCCCCC)=O)O '
               'NAME: SM(d18:0/22:0) REASON: CORRECT Contains sphingoid base '
               'with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-pentacosanoyl-15-methylhexadecasphing-4-enine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-hexadecanoylsphingosine-1-phosphocholine REASON: '
               'CORRECT Contains sphingoid base with amide-linked fatty acid '
               'and phosphocholine group\n'
               ' * SMILES: '
               'C(C/C=C\\CCCCCCCC)CCCCCCCCCC(CC(=O)N[C@@H](COP(OCC[N+](C)(C)C)(=O)[O-])[C@@H](\\C=C\\CCCCCCCCCCCCC)O)O '
               'NAME: '
               'N-[(15Z)-3-hydroxytetracos-15-enoyl]sphingosine-1-phosphocholine '
               'REASON: CORRECT Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               'False positives: SMILES: '
               'P(OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d41:1) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CC=CCCCCCCCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d44:2) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CC=CCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d38:2) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CCC/C=C\\C[C@H]1[C@@H](O)CC(O[C@@H]1/C=C/[C@@H](O)CCCCC)O)[C@H](O)/C=C/CCCCCCCC/C=C\\CCC)([O-])=O '
               'NAME: SM(d18:2(4E,14Z)/TXB2) REASON: WRONGLY CLASSIFIED '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyhexacosanoyl)sphingosine REASON: WRONGLY '
               'CLASSIFIED Contains sphingoid base with amide-linked fatty '
               'acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCC[C@@H](O)\\C=C/C=C/C=C/[C@@H](O)C/C=C\\CCCCC)[C@H](O)CCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d18:0/20:4(6Z,8E,10E,14Z)-2OH(5S,12R)) REASON: '
               'WRONGLY CLASSIFIED Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)C/C=C\\C[C@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCC/C=C\\CCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d18:2(4E,14Z)/5-iso PGF2VI) REASON: WRONGLY '
               'CLASSIFIED Contains sphingoid base with amide-linked fatty '
               'acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCC(=O)C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CC/C=C\\CCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d17:2(4E,8Z)/6 keto-PGF1alpha) REASON: WRONGLY '
               'CLASSIFIED Contains sphingoid base with amide-linked fatty '
               'acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCC)[C@H](O)CCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d14:0/20:0) REASON: WRONGLY CLASSIFIED Contains '
               'sphingoid base with amide-linked fatty acid and phosphocholine '
               'group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CCCC(O)C(O)C/C=C\\C/C=C\\C/C=C\\CCCCC)[C@H](O)/C=C/CCCCCCCCCCC)([O-])=O '
               'NAME: SM(d16:1/20:3(8Z,11Z,14Z)-2OH(5,6)) REASON: WRONGLY '
               'CLASSIFIED Contains sphingoid base with amide-linked fatty '
               'acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CCC[C@@H](O)[C@H](O)/C=C\\C=C/C=C/C=C/[C@@H](O)C/C=C\\CC)[C@H](O)\\C=C\\CCCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d19:1/20:5(7Z,9Z,11E,13E,17Z)-3OH(5,6,15)) REASON: '
               'WRONGLY CLASSIFIED Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCC(=O)C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d17:1/6 keto-PGF1alpha) REASON: WRONGLY CLASSIFIED '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCC/C=C\\CCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d18:2(4E,14Z)/PGE1) REASON: WRONGLY CLASSIFIED '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)C/C=C\\C[C@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d18:1/5-iso PGF2VI) REASON: WRONGLY CLASSIFIED '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCC\\C=C\\C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)[C@H](O)CCCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d19:0/PGF2alpha) REASON: WRONGLY CLASSIFIED Contains '
               'sphingoid base with amide-linked fatty acid and phosphocholine '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCC(=O)C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)[C@H](O)CCCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d19:0/6 keto-PGF1alpha) REASON: WRONGLY CLASSIFIED '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCC/C=C\\C[C@@H]1[C@H](C(=O)C=C1)/C=C/[C@@H](O)CCCCC)[C@H](O)CCCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d19:0/PGJ2) REASON: WRONGLY CLASSIFIED Contains '
               'sphingoid base with amide-linked fatty acid and phosphocholine '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CC/C=C\\CCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d17:2(4E,8Z)/PGF1alpha) REASON: WRONGLY CLASSIFIED '
               'Contains sphingoid base with amide-linked fatty acid and '
               'phosphocholine group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CC=CCCCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d40:2) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCC/C=C\\C[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d18:1/PGE2) REASON: WRONGLY CLASSIFIED Contains '
               'sphingoid base with amide-linked fatty acid and phosphocholine '
               'group\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CC=CCCCCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)([O-])=O '
               'NAME: SM(d41:2) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d34:1) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCC(O)\\C=C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)[C@H](O)CCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d18:0/22:6(5Z,7Z,10Z,13Z,16Z,19Z)-OH(4)) REASON: '
               'WRONGLY CLASSIFIED Contains sphingoid base with amide-linked '
               'fatty acid and phosphocholine group\n'
               ' * SMILES: '
               'S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC)C[C@H](N)C(=O)N[C@H]([C@H](O)\\C=C\\CCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d19:1/LTE4) REASON: WRONGLY CLASSIFIED Contains '
               'sphingoid base with amide-linked fatty acid and phosphocholine '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCC)[C@H](O)CC=CCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O '
               'NAME: SM(d38:1) REASON: WRONGLY CLASSIFIED Contains sphingoid '
               'base with amide-linked fatty acid and phosphocholine group\n'
               'False negatives: SMILES: '
               'O(P(O)(=O)OCC[N+](C)(C)C)C[C@]([C@](\\C=C\\CCCCCCCCCCCC)([H])O)([H])NC(CCCCCCCCCCCCCCCCCCCCCCC)=O '
               'NAME: SM(d17:1/24:0) REASON: MISSED No phosphocholine group '
               'found\n'
               ' * SMILES: '
               'O(P(O)(=O)OCC[N+](C)(C)C)C[C@@H]([C@@H](CCCCCCC\\C=C\\CCCCCCC)O)NC(CCCCCCC\\C=C\\CCCCCC)=O '
               'NAME: SM C16:1 REASON: MISSED No phosphocholine group found\n'
               ' * SMILES: '
               'O(P(O)(=O)OCC[N+](C)(C)C)C[C@]([C@](\\C=C\\CCCCCCCCCCC)([H])O)([H])NC(CCCCCCCCCCCCC/C=C\\CCCCCCCC)=O '
               'NAME: SM(d16:1/24:1(15Z)) REASON: MISSED No phosphocholine '
               'group found\n'
               ' * SMILES: '
               '[H][C@](C)(O)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(C)=O '
               'NAME: sphingomyelin 32:1 REASON: MISSED No sphingoid base '
               'pattern found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](COP([O-])(=O)OCC[N+](C)(C)C)NC(=O)CCCCC '
               'NAME: N-hexanoylsphingosine-1-phosphocholine REASON: MISSED '
               'Molecular weight too low for sphingomyelin\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'Cl.C=1C=C(OC)C(OC)=C(C1CN2CCNCC2)OC.Cl',
                                     'name': 'Trimetazidine hydrochloride',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(NCCS([O-])(=O)=O)=O)C)[H])C)O)[H])C',
                                     'name': 'tauroursocholate',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': '[H]S(=O)(=O)C[C@H](N)C(O)=O',
                                     'name': 'L-cysteine-S-dioxide',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)CCCN2C=C(CO[C@@H]1CN(C)CC3=CC=CC=C3OC)N=N2)[C@H](C)CO',
                                     'name': '(8R,9S)-6-[(2R)-1-hydroxypropan-2-yl]-9-[[(2-methoxyphenyl)methyl-methylamino]methyl]-8-methyl-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-5-one',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'Cc1ccc(cc1)N=C=Nc1ccc(C)cc1',
                                     'name': '1,3-di(p-tolyl)carbodiimide',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'O=C1[C@H]([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H]([C@H](O)CC(=C)C(C)C)C)CC4)(C)CC3)C)CC2)(C)CC1)C',
                                     'name': 'Gilvsin C',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)NC3=CC=CC=C3)C(=O)N(C[C@H]1OC)C)C)C(=O)C',
                                     'name': '1-[(4S,7S,8S)-5-acetyl-8-methoxy-4,7,10-trimethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-3-phenylurea',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@@H]1OC)C)C)C(=O)C3=NC=CN=C3',
                                     'name': 'N-[(4S,7R,8R)-8-methoxy-4,7,10-trimethyl-11-oxo-5-[oxo(2-pyrazinyl)methyl]-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'COc1ccc(cc1)\\C=C(NC=O)\\C(NC=O)=C\\c1ccc(OS(O)(=O)=O)cc1',
                                     'name': 'Fumiformamide',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'CCCCC(CC)COCCCN',
                                     'name': '3-(2-ethylhexoxy)propan-1-amine',
                                     'reason': 'No phosphocholine group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': '[C@@H]([C@@H](/C=C/CCCCCCCC/C=C\\CCC)O)(COP(OCC[N+](C)(C)C)(=O)[O-])NC(=O)CCCCCCC/C=C\\CCCCCCCC',
                                      'name': 'N-oleoyl-(4E,14Z)-sphingadienine-1-phosphocholine',
                                      'reason': 'No long carbon chain found'},
                                  {   'smiles': '[C@]([C@@](/C=C/CCCCCCCCCCC)(O)[H])(NC(=O)CCCCCCCCC/C=C\\CCCCCCCC)([H])COP(OCC[N+](C)(C)C)([O-])=O',
                                      'name': 'N-(11Z-eicosenoyl)-hexadecasphing-4-enine-1-phosphocholine',
                                      'reason': 'No long carbon chain found'},
                                  {   'smiles': 'O(P(O)(=O)OCC[N+](C)(C)C)C[C@]([C@](\\C=C\\CCCCCCCCCCCC)([H])O)([H])NC(CCCCCCCCCCCCCCCCCCCCCCC)=O',
                                      'name': 'SM(d17:1/24:0)',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': '[C@]([C@@](/C=C/CCCCCCCCCCC)(O)[H])(NC(=O)CCCCCCC/C=C\\CCCCCCCC)([H])COP(OCC[N+](C)(C)C)([O-])=O',
                                      'name': 'N-(9Z-octadecenoyl)-hexadecasphing-4-enine-1-phosphocholine',
                                      'reason': 'No long carbon chain found'},
                                  {   'smiles': 'O(P(O)(=O)OCC[N+](C)(C)C)C[C@@H]([C@@H](CCCCCCC\\C=C\\CCCCCCC)O)NC(CCCCCCC\\C=C\\CCCCCC)=O',
                                      'name': 'SM C16:1',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'O(P(O)(=O)OCC[N+](C)(C)C)C[C@]([C@](\\C=C\\CCCCCCCCCCC)([H])O)([H])NC(CCCCCCCCCCCCC/C=C\\CCCCCCCC)=O',
                                      'name': 'SM(d16:1/24:1(15Z))',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': '[H][C@](C)(O)[C@]([H])(COP([O-])(=O)OCC[N+](C)(C)C)NC(C)=O',
                                      'name': 'sphingomyelin 32:1',
                                      'reason': 'No sphingoid base pattern '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'The previous code had a few issues that led to both false '
                 'positives and false negatives:\n'
                 '\n'
                 '1. **False Positives**: The code incorrectly classified some '
                 'molecules as sphingomyelins because:\n'
                 '   - The phosphocholine pattern was too general and could '
                 'match other phosphate-containing groups\n'
                 '   - The sphingoid base pattern was too flexible and could '
                 'match other similar structures\n'
                 '   - The molecular weight and carbon count thresholds were '
                 'too low\n'
                 '\n'
                 '2. **False Negatives**: The code missed some valid '
                 'sphingomyelins because:\n'
                 '   - The phosphocholine pattern was too specific and missed '
                 'some valid variations\n'
                 '   - The sphingoid base pattern was too restrictive\n'
                 '   - The molecular weight threshold was too high for some '
                 'valid sphingomyelins\n'
                 '\n'
                 "Here's an improved version that addresses these issues:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 101,
    'num_false_positives': 42,
    'num_true_negatives': 142150,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.7062937062937062,
    'recall': 0.9351851851851852,
    'f1': 0.804780876494024,
    'accuracy': 0.9996556570625439,
    'negative_predictive_value': 0.999950758668233}