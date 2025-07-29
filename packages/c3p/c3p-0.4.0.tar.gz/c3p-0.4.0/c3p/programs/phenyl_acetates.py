"""
Classifies: CHEBI:140310 phenyl acetates
"""
"""
Classifies: Phenyl acetates
Definition: An acetate ester obtained by formal condensation of the carboxy group of acetic acid 
with the hydroxy group of any phenol.
Improvement strategy:
  1. Use a SMARTS pattern that exactly requires the acetate ester part as CH3C(=O)–.
  2. Check that the oxygen is directly attached to an aromatic carbon that belongs to at least one
     six-membered ring that is an isolated benzene ring: all atoms in that ring are aromatic 
     carbons and none of the ring atoms is shared with any other ring.
  3. Reject molecules that are likely too complex (here, with molecular weight >350 Da) to be 
     considered simple phenyl acetates.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_phenyl_acetates(smiles: str):
    """
    Determines if a molecule is a phenyl acetate based on its SMILES string.
    A phenyl acetate is defined as an acetate ester (CH3C(=O)-O-) where the ester oxygen is attached
    directly to an aromatic carbon, and that aromatic carbon must belong to an isolated six-membered
    benzene ring (i.e. no fusion with other rings). Additionally, the overall molecular weight must be
    in the range for a relatively simple phenyl acetate (<=350 Da).

    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a simple phenyl acetate, False otherwise.
        str: Explanation for the classification decision.
    """
    # Parse SMILES into an RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Compute molecular weight; if too heavy, consider the molecule too complex.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 350:
        return False, f"Molecular weight {mol_wt:.2f} too high for a simple phenyl acetate"
    
    # Define a SMARTS pattern for the acetate ester group:
    # The pattern enforces:
    # - an aromatic carbon (c) bound to an oxygen (O)
    # - that oxygen bound to a carbonyl (C=O) which is bound to a CH3.
    acetate_pattern = Chem.MolFromSmarts("cOC(=O)[CH3]")
    if acetate_pattern is None:
        return False, "Error processing SMARTS pattern"
    
    # Find all substructure matches for the acetate group in the molecule.
    matches = mol.GetSubstructMatches(acetate_pattern)
    if not matches:
        return False, "No phenyl acetate substructure found"
    
    # Get all ring information (each ring is a tuple of atom indices)
    rings = mol.GetRingInfo().AtomRings()
    
    # For each match, check the aromatic carbon (the first atom in the match) is part of an isolated benzene ring.
    for match in matches:
        aromatic_atom_idx = match[0]  # the aromatic carbon attached to oxygen
        # Iterate over rings that contain this aromatic carbon.
        for ring in rings:
            if aromatic_atom_idx in ring and len(ring) == 6:
                # First, verify that every atom in this ring is aromatic and is a carbon.
                if all(mol.GetAtomWithIdx(idx).GetAtomicNum() == 6 and mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
                    # Next, check that none of these ring atoms is part of any other ring (i.e. isolated ring).
                    isolated_ring = True
                    for idx in ring:
                        count = sum(1 for r in rings if idx in r)
                        if count > 1:
                            isolated_ring = False
                            break
                    if isolated_ring:
                        return True, "Found phenyl acetate group (acetate ester directly attached to an isolated benzene ring)"
    
    return False, "Phenyl acetate substructure found, but not attached to an isolated benzene ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140310',
                          'name': 'phenyl acetates',
                          'definition': 'An acetate ester obtained by formal '
                                        'condensation of the carboxy group of '
                                        'acetic acid with the hydroxy group of '
                                        'any phenol.',
                          'parents': ['CHEBI:22712', 'CHEBI:47622'],
                          'xrefs': ['MetaCyc:Phenyl-Acetates'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 51,
                           'log_lines_of_code': 3.9318256327243257,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
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
                                                 2,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 5,
                                                 6,
                                                 1,
                                                 1],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'CalcExactMolWt',
                                                 'GetAtomWithIdx',
                                                 'GetIsAromatic',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 9,
                           'smarts_strings': ['cOC(=O)[CH3]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_phenyl_acetates(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight '
                                          '{mol_wt:.2f} too high for a simple '
                                          'phenyl acetate"',
                                          'False, "Error processing SMARTS '
                                          'pattern"',
                                          'False, "No phenyl acetate '
                                          'substructure found"',
                                          'True, "Found phenyl acetate group '
                                          '(acetate ester directly attached to '
                                          'an isolated benzene ring)"',
                                          'False, "Phenyl acetate substructure '
                                          'found, but not attached to an '
                                          'isolated benzene ring"'],
                           'returns_count': 6,
                           'complexity': 5.386365126544865},
    'message': '\n'
               'Attempt failed: F1 score of 0.44628099173553726 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: COc1cc(ccc1OC(C)=O)C(C)=O NAME: '
               '4-acetyl-2-methoxyphenyl acetate REASON: CORRECT Found phenyl '
               'acetate group (acetate ester directly attached to a benzene '
               'ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(\\C=C\\C=O)cc1 NAME: 4-acetoxy '
               'cinnamaldehyde REASON: CORRECT Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: COC(=O)c1ccc(OC(C)=O)cc1 NAME: '
               'methyl-4-acetoxybenzoate REASON: CORRECT Found phenyl acetate '
               'group (acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: COC(=O)\\C=C\\c1ccc(OC(C)=O)c(OC)c1 NAME: methyl '
               '4-acetoxy-3-methoxycinnamate REASON: CORRECT Found phenyl '
               'acetate group (acetate ester directly attached to a benzene '
               'ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(cc1)[N+]([O-])=O NAME: 4-nitrophenyl '
               'acetate REASON: CORRECT Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(C=O)cc1 NAME: 4-acetoxy benzaldehyde '
               'REASON: CORRECT Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: COc1cc(\\C=C\\C=O)ccc1OC(C)=O NAME: '
               '4-acetoxy-3-methoxy-trans-cinnamaldehyde REASON: CORRECT Found '
               'phenyl acetate group (acetate ester directly attached to a '
               'benzene ring)\n'
               ' * SMILES: COc1cc(\\C=C\\C(O)=O)ccc1OC(C)=O NAME: '
               'O-acetylferulic acid REASON: CORRECT Found phenyl acetate '
               'group (acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1cccc(O)c1 NAME: resorcinol monoacetate '
               'REASON: CORRECT Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: COc1cc(\\C=C\\C)ccc1OC(C)=O NAME: isoeugenol '
               'acetate REASON: CORRECT Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccccc1 NAME: phenyl acetate REASON: '
               'CORRECT Found phenyl acetate group (acetate ester directly '
               'attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC\\C=C\\c1ccc(OC(C)=O)cc1 NAME: 4-hydroxy '
               'cinnamyl alcohol diacetate REASON: CORRECT Found phenyl '
               'acetate group (acetate ester directly attached to a benzene '
               'ring)\n'
               ' * SMILES: COc1cc(COC(C)=O)ccc1OC(C)=O NAME: vanillyl alcohol '
               'diacetate REASON: CORRECT Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: COc1cc(C=O)cc(OC)c1OC(C)=O NAME: syringaldehyde '
               'acetate REASON: CORRECT Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: COc1cc(C=O)ccc1OC(C)=O NAME: vanillin acetate '
               'REASON: CORRECT Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(cc1)C(O)=O NAME: 4-acetoxy benzoic '
               'acid REASON: CORRECT Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: COC(=O)\\C=C\\c1ccc(OC(C)=O)cc1 NAME: methyl '
               'p-coumarate acetate REASON: CORRECT Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(O)cc1 NAME: 4-hydroxyphenyl acetate '
               'REASON: CORRECT Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(cc1)C(C)=O NAME: 4-acetoxy '
               'acetophenone REASON: CORRECT Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC=1C=CC(=CC1OC)C(=O)OC NAME: methyl '
               '4-acetoxy-3-methoxybenzoate REASON: CORRECT Found phenyl '
               'acetate group (acetate ester directly attached to a benzene '
               'ring)\n'
               ' * SMILES: COc1cc(COC(C)=O)cc(OC)c1OC(C)=O NAME: syringyl '
               'alcohol diacetate REASON: CORRECT Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Nc1cc(C)ccc1OC(C)=O NAME: '
               '2-(acetylamino)-4-methylphenyl acetate REASON: CORRECT Found '
               'phenyl acetate group (acetate ester directly attached to a '
               'benzene ring)\n'
               ' * SMILES: COc1cc(cc(OC)c1OC(C)=O)C(C)=O NAME: acetosyringone '
               'acetate REASON: CORRECT Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: COc1cc(\\C=C\\C=O)cc(OC)c1OC(C)=O NAME: '
               '4-acetoxy-3,5-dimethoxy-trans-cinnamaldehyde REASON: CORRECT '
               'Found phenyl acetate group (acetate ester directly attached to '
               'a benzene ring)\n'
               ' * SMILES: COc1cc(\\C=C\\COC(C)=O)ccc1OC(C)=O NAME: '
               'trans-coniferyl alcohol diacetate REASON: CORRECT Found phenyl '
               'acetate group (acetate ester directly attached to a benzene '
               'ring)\n'
               'False positives: SMILES: O(C1=C(OC)C=C(OC)C=C1OC)C(=O)C NAME: '
               '2,4,6-Trimethoxyphenyl acetate REASON: WRONGLY CLASSIFIED '
               'Found phenyl acetate group (acetate ester directly attached to '
               'a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc2c(C)cc(=O)oc2c1 NAME: '
               '4-methylumbelliferyl acetate REASON: WRONGLY CLASSIFIED Found '
               'phenyl acetate group (acetate ester directly attached to a '
               'benzene ring)\n'
               ' * SMILES: CC(=O)OC1=CC=CC=C1C(=O)NC2=CC(=O)C=CC2(OC)OC NAME: '
               'acetic acid '
               '[2-[[(6,6-dimethoxy-3-oxo-1-cyclohexa-1,4-dienyl)amino]-oxomethyl]phenyl] '
               'ester REASON: WRONGLY CLASSIFIED Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC1=C(C=C(C=C1)C(=O)NC2=CC=C(C=C2)C(=O)O)OC '
               'NAME: '
               '4-[[(4-acetyloxy-3-methoxyphenyl)-oxomethyl]amino]benzoic acid '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: '
               'CC(=O)OC1=C(C=C(C=C1)C(=O)NC2=C(C=C(C=C2)O)C(=O)O)OC NAME: '
               '2-[[(4-acetyloxy-3-methoxyphenyl)-oxomethyl]amino]-5-hydroxybenzoic '
               'acid REASON: WRONGLY CLASSIFIED Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: C(OC1=C(OC)C=CC=C1)(=O)C2=C(OC(C)=O)C=CC=C2 NAME: '
               'guacetisal REASON: WRONGLY CLASSIFIED Found phenyl acetate '
               'group (acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC1=CC=CC=C1C(=O)NC2=CC=CC=C2 NAME: acetic '
               'acid [2-[anilino(oxo)methyl]phenyl] ester REASON: WRONGLY '
               'CLASSIFIED Found phenyl acetate group (acetate ester directly '
               'attached to a benzene ring)\n'
               ' * SMILES: CC1=CC=CC=C1C2=NC3=C(C=CC(=C3)OC(=O)C)C(=O)O2 NAME: '
               'acetic acid [2-(2-methylphenyl)-4-oxo-3,1-benzoxazin-7-yl] '
               'ester REASON: WRONGLY CLASSIFIED Found phenyl acetate group '
               '(acetate ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1c2ccccc2c(OC(C)=O)c2ccccc12 NAME: '
               'anthracene-9,10-diol diacetate REASON: WRONGLY CLASSIFIED '
               'Found phenyl acetate group (acetate ester directly attached to '
               'a benzene ring)\n'
               ' * SMILES: O(C(C)=O)C1=C(C(OC2=CC=CC=C2)=O)C=CC=C1 NAME: '
               'phenyl acetylsalicylate REASON: WRONGLY CLASSIFIED Found '
               'phenyl acetate group (acetate ester directly attached to a '
               'benzene ring)\n'
               ' * SMILES: C1(=C(C=C(OC(C)=O)C(=C1)C)C(C)C)OCCN(C)C.Cl NAME: '
               'Moxisylyte hydrochloride REASON: WRONGLY CLASSIFIED Found '
               'phenyl acetate group (acetate ester directly attached to a '
               'benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccccc1C([O-])=O NAME: acetylsalicylate '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: COc1cc(CC=C)ccc1OC(C)=O NAME: Acetyleugenol REASON: '
               'WRONGLY CLASSIFIED Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc(CCC(O)=O)cc1 NAME: '
               "3-(4'-acetoxyphenyl)propionic acid REASON: WRONGLY CLASSIFIED "
               'Found phenyl acetate group (acetate ester directly attached to '
               'a benzene ring)\n'
               ' * SMILES: CC(=O)OC1=CC=C(C=C1)NC(=O)CC2=CC=CC=C2 NAME: acetic '
               'acid [4-[(1-oxo-2-phenylethyl)amino]phenyl] ester REASON: '
               'WRONGLY CLASSIFIED Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)Oc1ccc2cc(-c3cccnc3)c(=O)oc2c1 NAME: '
               '7-(Acetyloxy)-3-(3-pyridinyl)-2H-1-benzopyran-2-one REASON: '
               'WRONGLY CLASSIFIED Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               ' * SMILES: C(OC1=CC=C(C=C1)NC(C)=O)(=O)C2=C(OC(C)=O)C=CC=C2 '
               'NAME: benorilate REASON: WRONGLY CLASSIFIED Found phenyl '
               'acetate group (acetate ester directly attached to a benzene '
               'ring)\n'
               ' * SMILES: O(C1=CC=C(CCC(=O)C)C=C1)C(=O)C NAME: Cuelure '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC1=CC=C(C=C1)C(=O)NCCC2=CC=CC=C2 NAME: '
               'acetic acid [4-[oxo-(2-phenylethylamino)methyl]phenyl] ester '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: CC1=C(CC2=C(C=CC(=C2C1)OC(=O)C)OC(=O)C)C NAME: '
               'acetic acid '
               '(4-acetyloxy-6,7-dimethyl-5,8-dihydronaphthalen-1-yl) ester '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: O(C=1C(=CC=CC1)C)C(=O)C NAME: o-Tolyl acetate '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: O1C(C2=C(O)C=CC(OC(=O)C)=C2)=CC(=O)C=3C1=CC=CC3 '
               "NAME: 2',5'-Dihydroxyflavone 5'-acetate REASON: WRONGLY "
               'CLASSIFIED Found phenyl acetate group (acetate ester directly '
               'attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC1=CC=CC(=C1OC(=O)C)C(=O)O NAME: '
               '2,3-diacetyloxybenzoic acid REASON: WRONGLY CLASSIFIED Found '
               'phenyl acetate group (acetate ester directly attached to a '
               'benzene ring)\n'
               ' * SMILES: O(C=1C(OC)=CC=CC1)C(=O)C NAME: Guaicyl acetate '
               'REASON: WRONGLY CLASSIFIED Found phenyl acetate group (acetate '
               'ester directly attached to a benzene ring)\n'
               ' * SMILES: CC(=O)OC1=CC2=C(C=C1)C(=O)C(=CO2)C3=CC=CC=C3 NAME: '
               'acetic acid (4-oxo-3-phenyl-1-benzopyran-7-yl) ester REASON: '
               'WRONGLY CLASSIFIED Found phenyl acetate group (acetate ester '
               'directly attached to a benzene ring)\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[NH+]1CCC(CC1)N1CCN(CC1)C(=O)[C@@H](CC1=CC2=C(NN=C2)C(C)=C1)NC(=O)N1CCC(CC1)C1=CC2=C(NC1=O)C=CC=C2',
                                     'name': 'zavegepant(1+)',
                                     'reason': 'Molecular weight 639.38 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'CC1=CC=CC(=C1)C(=O)NNC(=O)C2=C(C3=CC=CC=C3N(C2=O)C)O',
                                     'name': "4-hydroxy-1-methyl-N'-[(3-methylphenyl)-oxomethyl]-2-oxo-3-quinolinecarbohydrazide",
                                     'reason': 'Molecular weight 351.12 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CCCN(C)C)O[C@@H]1CN(C)C(=O)NC3CCCCC3)[C@H](C)CO',
                                     'name': 'N-[(2S,3S)-2-[[[(cyclohexylamino)-oxomethyl]-methylamino]methyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-4-(dimethylamino)butanamide',
                                     'reason': 'Molecular weight 545.36 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'O1C(OC2(C=3OC=4C(C(=O)C3)=C(OC)C(OC)=C(OC)C4)C=CC(=O)C=C2)C(O)C(O)C(O)C1C(O)=O',
                                     'name': '3,4,5-trihydroxy-6-{[4-oxo-1-(5,6,7-trimethoxy-4-oxo-4H-chromen-2-yl)cyclohexa-2,5-dien-1-yl]oxy}oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Molecular weight 520.12 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'O=C(N[C@@H]1C(OC2(C1)[C@H]3O[C@H]3C(O)(CC(=O)C)[C@@H]4[C@H]2O4)O)/C=C\\C(CC(CCCCCC)C)C',
                                     'name': 'Penicimutanolone',
                                     'reason': 'Molecular weight 479.29 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCC',
                                     'name': 'TG(16:0/14:1(9Z)/18:0)',
                                     'reason': 'Molecular weight 804.72 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'O1C(O)C(C(C1)CC2=CC=3OCOC3C=C2)CC4=CC(OC)=C(OC)C=C4',
                                     'name': "(8R,8'R,9S)-9-Hydroxy-3,4-dimethoxy-3',4'-methylenoxy-9,9'-epoxylignan",
                                     'reason': 'Molecular weight 372.16 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCCCCCC',
                                     'name': '1-palmitoyl-2-lauroyl-sn-glycero-3-phospho-1D-myo-inositol',
                                     'reason': 'Molecular weight 754.46 too '
                                               'high for a simple phenyl '
                                               'acetate'},
                                 {   'smiles': 'O=C1C2=C([C@@H](O)CC1)[C@@H]([C@H](O)CCC)OC2',
                                     'name': 'Phomopsiketone F',
                                     'reason': 'No phenyl acetate substructure '
                                               'found'},
                                 {   'smiles': 'C1CC(C1)CN(C[C@H]2[C@H]([C@H](N2)CO)C3=CC=CC=C3)C(=O)C4=CC=C(C=C4)F',
                                     'name': 'N-(cyclobutylmethyl)-4-fluoro-N-[[(2R,3R,4S)-4-(hydroxymethyl)-3-phenyl-2-azetidinyl]methyl]benzamide',
                                     'reason': 'Molecular weight 382.21 too '
                                               'high for a simple phenyl '
                                               'acetate'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'Below is my reasoning before presenting the complete code:\n'
                 '\n'
                 'We know that a phenyl acetate is defined as an acetate ester '
                 '(CH3C(=O)–O–) where the oxygen is directly attached to a '
                 'phenol (aromatic ring) that is a simple benzene ring. The '
                 'previous attempt used a SMARTS for "cOC(=O)[CH3]" and then '
                 'checked that the aromatic carbon belonged to a six‐membered '
                 'ring of aromatic carbons. However, many false positives '
                 'arose because the benzene ring might be part of fused or '
                 'otherwise extended ring systems. To improve the classifier '
                 'we:\n'
                 '\u2003• continue using a SMARTS that exactly detects the '
                 'acetate ester group,\n'
                 '\u2003• require that the aromatic carbon (the “c” in the '
                 'SMARTS) belongs to a six‐membered ring where every ring atom '
                 'is aromatic and, importantly, none of those atoms is part of '
                 'any other ring (thus ensuring it is an isolated benzene '
                 'ring),\n'
                 '\u2003• reject molecules whose molecular weight is too high '
                 'for a “simple” phenyl acetate (using <=350 Da).\n'
                 '\n'
                 'Below is the complete Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 46,
    'num_true_negatives': 142227,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3698630136986301,
    'recall': 1.0,
    'f1': 0.54,
    'accuracy': 0.9996767392832046,
    'negative_predictive_value': 1.0}