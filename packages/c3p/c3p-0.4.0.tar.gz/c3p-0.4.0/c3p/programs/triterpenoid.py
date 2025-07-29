"""
Classifies: CHEBI:36615 triterpenoid
"""
"""
Classifies: CHEBI:26870 triterpenoid
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_triterpenoid(smiles: str):
    """
    Determines if a molecule is a triterpenoid based on its SMILES string.
    A triterpenoid is derived from a triterpene, typically containing 30 carbons,
    but may have modifications such as rearrangements, glycosylations, or additions/removals of methyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a triterpenoid, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count carbon atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 27 or c_count > 50:
        return False, f"Carbon count {c_count} not in typical triterpenoid range (27-50 carbons)"

    # Count oxygen atoms
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count == 0:
        return False, "No oxygen atoms found, likely not a triterpenoid"

    # Calculate number of rings
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()
    if num_rings < 4:
        return False, f"Only {num_rings} rings found, triterpenoids typically have at least 4 rings"

    # Check for fused ring systems
    # Get ring bonds
    ssr = Chem.GetSymmSSSR(mol)
    fused_rings = [set(ring) for ring in ssr]

    # Build a graph of ring adjacencies
    ring_adjacency = []
    for i in range(len(fused_rings)):
        neighbors = []
        for j in range(len(fused_rings)):
            if i != j and len(fused_rings[i] & fused_rings[j]) >= 2:
                neighbors.append(j)
        ring_adjacency.append(neighbors)

    # Find the largest set of fused rings using DFS
    max_fused_rings = 0
    visited = set()
    def dfs(ring_idx):
        visited.add(ring_idx)
        total = 1
        for nbr in ring_adjacency[ring_idx]:
            if nbr not in visited:
                total += dfs(nbr)
        return total

    for i in range(len(fused_rings)):
        if i not in visited:
            fused_ring_count = dfs(i)
            if fused_ring_count > max_fused_rings:
                max_fused_rings = fused_ring_count
                
    if max_fused_rings < 4:
        return False, f"Only {max_fused_rings} fused rings found, triterpenoids typically have at least 4 fused rings"

    # Calculate fraction of sp3 carbons
    sp3_carbons = 0
    total_carbons = 0
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6:
            total_carbons += 1
            if atom.GetHybridization() == Chem.rdchem.HybridizationType.SP3:
                sp3_carbons += 1
    sp3_fraction = sp3_carbons / total_carbons if total_carbons > 0 else 0
    if sp3_fraction < 0.6:
        return False, f"Fraction of sp3 carbons is {sp3_fraction:.2f}, which is too low for typical triterpenoids"

    return True, "Molecule meets criteria for a triterpenoid (carbon count, oxygen atoms, fused ring structures, saturation)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36615',
                          'name': 'triterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'triterpene. The term includes '
                                        'compounds in which the C30 skeleton '
                                        'of the parent triterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873'],
                          'xrefs': ['KEGG:C06085'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 68,
                           'log_lines_of_code': 4.219507705176107,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetSymmSSSR',
                                                 'NumRings',
                                                 'add',
                                                 'append',
                                                 'MolFromSmiles',
                                                 'GetHybridization',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'GetRingInfo'],
                           'methods_called_count': 9,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_triterpenoid(smiles: str):',
                                       'dfs(ring_idx):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Carbon count {c_count} not '
                                          'in typical triterpenoid range '
                                          '(27-50 carbons)"',
                                          'False, "No oxygen atoms found, '
                                          'likely not a triterpenoid"',
                                          'False, f"Only {num_rings} rings '
                                          'found, triterpenoids typically have '
                                          'at least 4 rings"',
                                          'total',
                                          'False, f"Only {max_fused_rings} '
                                          'fused rings found, triterpenoids '
                                          'typically have at least 4 fused '
                                          'rings"',
                                          'False, f"Fraction of sp3 carbons is '
                                          '{sp3_fraction:.2f}, which is too '
                                          'low for typical triterpenoids"',
                                          'True, "Molecule meets criteria for '
                                          'a triterpenoid (carbon count, '
                                          'oxygen atoms, fused ring '
                                          'structures, saturation)"'],
                           'returns_count': 8,
                           'complexity': 5.443901541035221},
    'message': '\n'
               'Attempt failed: F1 score of 0.10335158232073706 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1C2=C(C(=O)CC3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4(C(=O)C=C([C@]4([C@@H]1O)C)[C@@H](CC(=O)CC(C(=O)O)C)C)C '
               'NAME: Resinacein G REASON: CORRECT Molecule meets criteria for '
               'a triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O[C@@H]1C([C@]2([C@@](C3=C([C@]4([C@@]([C@](CC4)([C@@H](CCC=C(C)C)C(O)=O)[H])(CC3)C)C)CC2)(CC1)C)[H])(C)C '
               'NAME: Trametenolic acid B REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C=C(C(=C)[C@H]2O[C@@H](O)C([C@H]3[C@]4([C@@H]([C@@]5([C@H](C([C@@H](O)[C@@H](C5)O)(C)C)CC4)C)CC3)C)=CC2)OC1(C)C '
               'NAME: Sodagnitin E REASON: CORRECT Molecule meets criteria for '
               'a triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               '[H][C@@]1(CC=C(C)C(=O)O1)[C@@H](C)C1CC[C@@]2(C)C3=C(CC[C@]12C)[C@](CCC(=O)OC)(COC(C)=O)[C@@]([H])(CC3)C(C)(C)O '
               'NAME: colossolactone VII REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C=C2[C@]([C@H](C(=C)C)C[C@@H]3[C@]2(O3)[C@]4([C@]1([C@@H](/C(=C\\C(O)CC(C(=O)O)C)/C)C[C@H]4O)C)C)(CCC(=O)OC)C '
               'NAME: Elfvingic acid H Me ester REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(CC[C@@H]([C@]3(C1)C)[C@@H](CC/C=C(\\C(=O)O)/C)C)C)CC[C@@H]4[C@@]2(CCC(C4(C)C)=O)C '
               'NAME: 3,11-dioxolansta-8,24(Z)-diene-26-oic acid REASON: '
               'CORRECT Molecule meets criteria for a triterpenoid (carbon '
               'count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)CC3[C@@]2(CCC(C3(C)C)=O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1OC(=O)C)C)[C@@H](CCC(=O)OCCCC)C)C '
               'NAME: Butyl lucidenate D2 REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CC[C@@H](C([C@@H]3C1)(C)C)O)C)CC[C@]4([C@]2(CC[C@@H]4[C@@H](CC/C=C(/C(=O)O)\\C)C)C)C '
               'NAME: 7-oxo-ganoderic acid Z REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)C(O)(CC(O)CC(C(=O)O)C)C)C)[C@@H](O)C[C@@H]4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: 3beta,7beta,20,23xi-Tetrahydroxy-11,15-D REASON: CORRECT '
               'Molecule meets criteria for a triterpenoid (carbon count, '
               'oxygen atoms, ring structures)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2(C)C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@]1([H])CC3=O)[C@H](C)CC\\C=C(/C)C=O '
               'NAME: lucialdehyde C REASON: CORRECT Molecule meets criteria '
               'for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H]([C@H](OC(=O)C)/C=C/C(O)(C)C)C)CC4)(C)CC3)C)CC2)(C)CC1)(C)C '
               'NAME: '
               '(20S,22S,23E)-22O-acetyl-25-hydroxylanosta-8,23(E)-dien-3-one '
               'REASON: CORRECT Molecule meets criteria for a triterpenoid '
               '(carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'COC(=O)[C@@]12OC[C@@]34[C@H]1[C@@H](OC(C)=O)C(=O)O[C@@H]3C[C@H]1C(C)=C(OC(C)=O)C(=O)C[C@]1(C)[C@H]4[C@@H](O)[C@@H]2O '
               'NAME: 3,15-di-O-acetylbruceolide REASON: CORRECT Molecule '
               'meets criteria for a triterpenoid (carbon count, oxygen atoms, '
               'ring structures)\n'
               ' * SMILES: '
               '[C@]123[C@]([C@]4([C@]([C@](CC4)([C@@H](CCC=C(C)C)C)[H])(C)CC1)C)(CC[C@@]5([C@@]2(CC[C@@H]([C@]5(C=O)C)O)C3)[H])[H] '
               'NAME: '
               '4alpha-formyl-4beta,14alpha-dimethyl-9beta,19-cyclo-5alpha-cholest-24-en-3beta-ol '
               'REASON: CORRECT Molecule meets criteria for a triterpenoid '
               '(carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O=C(O)[C@@H]([C@@H]1[C@@]2([C@@](C=3C([C@@]4([C@H](C([C@@H](O)CC4)(C)C)CC3)C)=CC2)(C)C[C@H]1O)C)CCC(O)C(OC)(C)C '
               'NAME: Irpeksolactin I REASON: CORRECT Molecule meets criteria '
               'for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)[C@@H](CCC(=O)OCCCC)C)C)[C@@H](O)C[C@@H]4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: Butyl lucidenate N REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O([C@H]1C([C@@H](C2([C@@]3(C(C[C@@]1(C2=O)[H])=C4[C@@](CC3)([C@@H](OC(=O)C4)C=5C=COC5)C)[H])C)CC(OC)=O)(C)C)C(=O)C '
               'NAME: FISSINOLIDE REASON: CORRECT Molecule meets criteria for '
               'a triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@](C3=C([C@@]4([C@](C([C@@H](O)[C@H](O)C4)(C)C)(CC3)[H])C)C1)(CC[C@@]2([C@@H](CC[C@@H](O)C(O)(C)C)CO)[H])C)C '
               'NAME: Fasciculol C REASON: CORRECT Molecule meets criteria for '
               'a triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O1[C@H](O)[C@@H](C(C)C)C[C@H]1[C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5(C(C([C@@H](O)CC5)(C)C)CC4)C)CC3)(C)CC2)C)C '
               'NAME: (22S, '
               '24R)-24-methyllanosta-8-en-22,28-epoxy-3beta,28beta-diol '
               'REASON: CORRECT Molecule meets criteria for a triterpenoid '
               '(carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O=C1C(C2[C@](C3=C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/C(=O)O)\\C)C)C[C@@H]4OC(=O)C)(C)CC3)C)[C@@H](C2)O)(C)CC1)(C)C '
               'NAME: Ganoderique acid V REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@@]4(C(=O)C[C@@H]([C@]4(C1)C)[C@]5(OC(=O)CC5)C)C '
               'NAME: Ganoderlactone B REASON: CORRECT Molecule meets criteria '
               'for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]3([H])[C@@H](O)[C@H](O)[C@]4(OC[C@@]13[C@@]4([H])[C@@H](OC(=O)CC(C)C)C(=O)O2)C(=O)OC '
               'NAME: isobrucein A REASON: CORRECT Molecule meets criteria for '
               'a triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C[C@@]12CC[C@H]3C(=CC[C@H]4C(C)(C)C(=O)CC[C@]34C)[C@@]1(C)CC[C@H]2C1=CC(O)(CO)OC1=O '
               'NAME: dysolenticin C REASON: CORRECT Molecule meets criteria '
               'for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C([C@]2([C@@](C=3C([C@]4([C@@]([C@](CC4)([C@@H](CCC=C(CO)CO)C)[H])(CC3)C)C)=CC2)(CC1)C)[H])(C)C '
               'NAME: Ganoderiol F REASON: CORRECT Molecule meets criteria for '
               'a triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@@]4([C@H](O)C[C@@H]([C@]4([C@@H]1O)C)[C@@H](CC(=O)C[C@@H](C(=O)O)C)C)C '
               'NAME: Ganoweberianic acid D REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1C=C2O[C@@H]3C[C@@]4([C@H]([C@@H](OC(=O)C)C[C@]4(C5=C3[C@]2(C)[C@H](C1(C)C)CC5)C)[C@@H](CC/C=C(\\C(=O)O)/C)C)C '
               'NAME: Lepiotaprocerin A REASON: CORRECT Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               'False positives: SMILES: '
               'O=CC1=C(O)C=CC2=C1[C@H](C3=C4O[C@H](C(O)(C)C)COC4=CC(=C3)C)[C@@H](C(O)(C)C)C2 '
               'NAME: Diaporindene A REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'COC1=CC=C(C=C1)C(=O)NCC23C=CC(O2)C4C3C(=O)N(C4=O)CC5=CC=CC=C5 '
               'NAME: '
               'N-[[1,3-dioxo-2-(phenylmethyl)-7,7a-dihydro-3aH-octahydro-1H-4,7-epoxyisoindol-4-yl]methyl]-4-methoxybenzamide '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'COC1=CC=CC=C1CN2CC[C@H]3[C@@H]2C4=C(C=CC(=C4)C#CC5=CC=CC=C5)N[C@@H]3CO '
               'NAME: '
               '[(3aR,4S,9bR)-1-[(2-methoxyphenyl)methyl]-8-(2-phenylethynyl)-2,3,3a,4,5,9b-hexahydropyrrolo[3,2-c]quinolin-4-yl]methanol '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC([C@]4([C@]([C@@]3([C@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(O)=O)C)[H])C)=O)[H])C '
               'NAME: 3alpha,7beta-dihydroxy-12-oxo-5beta-cholanic acid '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)CCCN2C=C(CO[C@@H]1CN(C)CC3=CC4=C(C=C3)N(CCO4)C)N=N2)[C@@H](C)CO '
               'NAME: '
               '(8S,9S)-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-9-[[methyl-[(4-methyl-2,3-dihydro-1,4-benzoxazin-7-yl)methyl]amino]methyl]-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-5-one '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)NC4=CC=CC=C4)C5=CC=CC=C5N2C)[C@H](C)CO '
               'NAME: LSM-30741 REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CC=CC(=C4)C)C5=CC=CC=C5N2C)[C@@H](C)CO '
               'NAME: LSM-30762 REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@H](O)[C@@H]1NC(=O)C)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)C3O[C@@H]([C@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)[C@H]3O)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4R,5R,6S)-5-acetamido-4-[(3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,6-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C[C@H]1[C@@H]([C@H]([C@H]([C@@H](O1)OC[C@@H]2[C@H]([C@@H]([C@H](C(O2)OC3=C(OC4=CC(=CC(=C4C3=O)O)OCCO)C5=CC(=C(C=C5)OCCO)OCCO)O)O)O)O)O)O '
               'NAME: '
               '2-[3,4-bis(2-hydroxyethoxy)phenyl]-5-hydroxy-7-(2-hydroxyethoxy)-3-[[(3R,4S,5S,6R)-3,4,5-trihydroxy-6-[[(2R,3R,4R,5R,6S)-3,4,5-trihydroxy-6-methyl-2-oxanyl]oxymethyl]-2-oxanyl]oxy]-1-benzopyran-4-one '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C1C[C@H]2[C@@H](COC[C@H](CN2CCC(F)(F)F)O)O[C@H]1CC(=O)NCC3=CC=C(C=C3)OC4=CC=CC=C4 '
               'NAME: '
               '2-[(3S,6aS,8R,10aS)-3-hydroxy-1-(3,3,3-trifluoropropyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[(4-phenoxyphenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'ClC1=C2N(C=3C=4NC=5C=CC=CC5C4C6=C(C3C2=CC=C1)C(=O)N(C)C6=O)C7OC(C(OC)C(C7O)O)COC8OCC(N)C(C8)O '
               'NAME: AT2433-A2 REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O=C1NC2=C(C(=O)C[C@H]3[C@]1([C@@]4([C@](O)([C@@]56O[C@@H]5[C@@H](O)[C@H](O[C@H]6CC4)C(=C)C)CC3)C)C)C=CC(=C2)C(C=C)(C)C '
               'NAME: Sulpinine C REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'FC1=CC=C([C@H]2[C@H]3[C@H](CC[C@@H]2O[C@@H](C4=CC(=CC(=C4)C(F)(F)F)C(F)(F)F)C)CN(C3)C=5CCC(=O)C5)C=C1 '
               'NAME: serlopitant REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'C1CC1CC(=O)N2C[C@@H]3[C@@H]([C@H](N3C(=O)C2)CO)C4=CC=C(C=C4)C#CC5=CC(=CC=C5)F '
               'NAME: '
               '(6S,7S,8S)-4-(2-cyclopropyl-1-oxoethyl)-7-[4-[2-(3-fluorophenyl)ethynyl]phenyl]-8-(hydroxymethyl)-1,4-diazabicyclo[4.2.0]octan-2-one '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O=C1[C@@H](O)[C@@]2([C@@H](C(=O)OC)[C@@](C(=C)C[C@H]2[C@]3([C@H]1C(C4(O[C@H](C)[C@H](O4)C)CC3)(C)C)C)(C(=O)[C@](O)(C(=O)OC)C)C)C '
               'NAME: Spiroterreusnoid F REASON: WRONGLY CLASSIFIED Molecule '
               'meets criteria for a triterpenoid (carbon count, oxygen atoms, '
               'ring structures)\n'
               ' * SMILES: '
               'C1[C@@H](O[C@@H]([C@H]2[C@@H]1C3=C(O2)C=CC(=C3)NS(=O)(=O)C4=CC=C(C=C4)F)CO)CC(=O)NCC5=CC=C(C=C5)OC6=CC=CC=C6 '
               'NAME: '
               '2-[(1R,3R,4aS,9aR)-6-[(4-fluorophenyl)sulfonylamino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b][1]benzofuran-3-yl]-N-[(4-phenoxyphenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc3c(O)cc(O)cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](O[C@@H]2OC[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@@H]1O '
               'NAME: cyanidin 3-O-beta-D-sambubioside REASON: WRONGLY '
               'CLASSIFIED Molecule meets criteria for a triterpenoid (carbon '
               'count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@]3([H])[C@]4(C)[C@H](OC(C)=O)C=CC(C)(C)[C@@]4([H])C[C@H](OC(C)=O)[C@]33O[C@]3([H])C1=C(C)C(=O)O2 '
               'NAME: gelomulide M REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@@H](O[C@@H]2[C@@H](O)[C@H](O[C@@H]([C@@H]2O)CO)O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO)O[C@@H]([C@@H]1O)CO)[C@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4O)CO '
               'NAME: '
               '(2S,3R,4S,5R,6R)-2-[(2R,3R,4S,5S,6R)-2-[(2R,3R,4S,5S,6R)-2-[(2R,3S,4S,5R,6R)-3,5-Dihydroxy-2-(hydroxymethyl)-6-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)NC3=CC=CC4=CC=CC=C43)O[C@H]1CN(C)S(=O)(=O)C5=CC=CC=C5F)[C@@H](C)CO '
               'NAME: '
               '1-[(2R,3R)-2-[[(2-fluorophenyl)sulfonyl-methylamino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-10-yl]-3-(1-naphthalenyl)urea '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O(C1C(O)[C@H](O)C(O[C@H]1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC(OC)=C(O)C=C4)CO)[C@@H]5OC[C@@H](O)C(O)[C@H]5O '
               'NAME: Peonidin 3-sambubioside REASON: WRONGLY CLASSIFIED '
               'Molecule meets criteria for a triterpenoid (carbon count, '
               'oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C1CN(CCN1C2=CC(=NC3=CC(=NN32)C4=CC=C(C=C4)Br)C5=CC=CC=C5)C(=O)C6=COC=C6 '
               'NAME: '
               '[4-[2-(4-bromophenyl)-5-phenyl-7-pyrazolo[1,5-a]pyrimidinyl]-1-piperazinyl]-(3-furanyl)methanone '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CC3=CC=CC=C3)O[C@@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)C)[C@@H](C)CO '
               'NAME: '
               'N-[(2S,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-(4-methylphenyl)sulfonylamino]methyl]-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-2-phenylacetamide '
               'REASON: WRONGLY CLASSIFIED Molecule meets criteria for a '
               'triterpenoid (carbon count, oxygen atoms, ring structures)\n'
               ' * SMILES: '
               'O1C(C=CC=2C1=C(C=3OC=C(C(=O)C3C2O)C4=CC(O)=C(O)C=C4)CC=C(C)C)(C)C '
               'NAME: Auriculasin REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               ' * SMILES: '
               'C[C@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO '
               'NAME: LSM-11233 REASON: WRONGLY CLASSIFIED Molecule meets '
               'criteria for a triterpenoid (carbon count, oxygen atoms, ring '
               'structures)\n'
               'False negatives: SMILES: '
               'O(CC12C3(C(C4(C(CC3)C(C(OC5OCC(O)C(O)C5O)CC4)(C)C)C)CCC1C(C(=O)C2)C(O)(C/C=C/C(O)(C)C)C)C)C6OC(C(O)C(O)C6O)CO '
               'NAME: Hoduloside VI REASON: MISSED Carbon count 41 not in '
               'typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'C1[C@@H](C([C@]2([C@]3(C1)[C@]4([C@@](CC2)([C@]5([C@](CC4)([C@](CC5)([C@H](C)CCC=C(C)C)[H])C)C)[H])C3)[H])(C)C)OC(/C=C/C6=CC(=C(C=C6)O)OC)=O '
               'NAME: gamma-Oryzanol (TN) REASON: MISSED Carbon count 40 not '
               'in typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'O=C(O[C@H]1C(OC(=O)C)C(C2CCC3C([C@]2(C1)C)=CC[C@@]4([C@@H](C5[C@@H](O[C@@H](C(O)(C)C)CC5)O)CC[C@@]34C)C)(C)C)CC(O)(CC(=O)OC)C '
               'NAME: methyl aeruginosate B REASON: MISSED Carbon count 39 not '
               'in typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'O=C1C(C2=CC[C@H]3[C@]4([C@](C(C(O)(C(=O)/C=C/C(OC(=O)C)(C)C)C)[C@@H](C4)OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(C)CC([C@]3([C@@H]2C[C@@H]1O)C)=O)C)(C)C '
               'NAME: Cucurbitacin B linoleyl ester REASON: MISSED Carbon '
               'count 50 not in typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'OC1C2(C(C(C1)C(C(OC(=O)C)C/C=C(\\C)/C(O)=O)C)(CC=C3C4(C(C(C(OC(=O)C)CC4)(C)C)CC=C23)C)C)C '
               'NAME: Ganoderic acid Mk REASON: MISSED Carbon count 34 not in '
               'typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'CC1=CC(=O)[C@@H](O)[C@@]2(C)[C@H]1[C@@H](O)[C@H]1OC(=O)[C@H](O)[C@@]3(O)[C@]4(CO)OC[C@]13[C@@H]2[C@@H](O)[C@@H]4O '
               'NAME: yadanziolide B REASON: MISSED Carbon count 20 not in '
               'typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@](C)(CC[C@]1(C)CC[C@]1(C)C2=CC(=O)[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C(O)=O)C(C)(C)[C@]3([H])CC[C@@]12C)C(O)=O '
               'NAME: glycyrrhetic acid 3-O-glucuronide REASON: MISSED Carbon '
               'count 36 not in typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'O(C1C(C2(C(C3=C(C4(C(C(C(OC(=O)C)CC4)(C)C)CC3)C)CC2)(C1)C)C)C(CCC(C(C)C)CO)C(O)=O)C(=O)C '
               'NAME: O-acetylpachymic acid-25-ol REASON: MISSED Carbon count '
               '35 not in typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'O1C23C(C4(C(C5(C(C(CC5)C(C/C=C/C(OC6OC(C(O)C(O)C6O)CO)(C)C)C)(CC4)C)C)C=C2)C1OC)CCC(OC7OC(C(O)C(O)C7O)CO)C3(C)C '
               'NAME: Goyaglycoside g REASON: MISSED Carbon count 43 not in '
               'typical triterpenoid range (24-33 carbons)\n'
               ' * SMILES: '
               'CC(C)=CCC[C@](C)(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H]1CC[C@]2(C)[C@@H]1[C@H](O)C[C@@H]1[C@@]3(C)CC[C@H](O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)C(C)(C)[C@@H]3CC[C@@]21C '
               'NAME: ginsenoside F2 REASON: MISSED Carbon count 42 not in '
               'typical triterpenoid range (24-33 carbons)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'NCC(=O)CCC([O-])=O',
                                     'name': '5-aminolevulinate',
                                     'reason': 'Carbon count 5 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'},
                                 {   'smiles': '[H][C@@]12CCCC(C)(C)C1CC[C@]1([H])[C@@]2(C)CC[C@]2(C)[C@]([H])(CC[C@@]12C)[C@H](C)CCCC(C)C',
                                     'name': 'cucurbitane',
                                     'reason': 'No oxygen atoms found, likely '
                                               'not a triterpenoid'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC2=CC=CC=C2',
                                     'name': 'Arg-Phe-Tyr',
                                     'reason': 'Carbon count 24 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'},
                                 {   'smiles': 'C(CC(C(=O)O)NC(CCC(=O)O)C(=O)O)CN',
                                     'name': 'ornaline',
                                     'reason': 'Carbon count 10 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(15:0/18:1(11Z))',
                                     'reason': 'Only 0 rings found, '
                                               'triterpenoids typically have '
                                               'at least 4 rings'},
                                 {   'smiles': 'O=CC1=C(O)C=CC2=C1[C@H](C3=C4O[C@H](C(O)(C)C)COC4=CC(=C3)C)[C@@H](C(O)(C)C)C2',
                                     'name': 'Diaporindene A',
                                     'reason': 'Carbon count 25 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'},
                                 {   'smiles': 'O(C(CCCCCCCCC)CCC/C=C/C)C(=O)/C=C(/C)\\C(O)=O',
                                     'name': 'Chaetomellic acid B',
                                     'reason': 'Carbon count 21 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'},
                                 {   'smiles': 'Oc1ccc(cc1)[C@H]1Oc2cc(O)cc([C@@H]3[C@H](Oc4ccc(\\C=C\\c5cc(O)cc(O)c5)cc34)c3ccc(O)cc3)c2[C@@H]1c1cc(O)cc(O)c1',
                                     'name': 'trans-diptoindonesin B',
                                     'reason': 'Only 2 fused rings found, '
                                               'triterpenoids typically have '
                                               'at least 4 fused rings'},
                                 {   'smiles': 'O1C(CC(=O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3',
                                     'name': "4',7-dihydroxyflavanone",
                                     'reason': 'Carbon count 15 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO',
                                     'name': 'beta-D-GlcpNAc-(1->4)-beta-D-Galp-(1->4)-D-GlcpNAc',
                                     'reason': 'Carbon count 22 not in typical '
                                               'triterpenoid range (27-50 '
                                               'carbons)'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C=C(C(=C)[C@H]2O[C@@H](O)C([C@H]3[C@]4([C@@H]([C@@]5([C@H](C([C@@H](O)[C@@H](C5)O)(C)C)CC4)C)CC3)C)=CC2)OC1(C)C',
                                      'name': 'Sodagnitin E',
                                      'reason': 'Only 3 fused rings found, '
                                                'triterpenoids typically have '
                                                'at least 4 fused rings'},
                                  {   'smiles': '[H][C@@]1(CC=C(C)C(=O)O1)[C@@H](C)C1CC[C@@]2(C)C3=C(CC[C@]12C)[C@](CCC(=O)OC)(COC(C)=O)[C@@]([H])(CC3)C(C)(C)O',
                                      'name': 'colossolactone VII',
                                      'reason': 'Only 3 fused rings found, '
                                                'triterpenoids typically have '
                                                'at least 4 fused rings'},
                                  {   'smiles': 'CC1=CC(=O)[C@@H](O)[C@@]2(C)[C@H]1[C@@H](O)[C@H]1OC(=O)[C@H](O)[C@@]3(O)[C@]4(CO)OC[C@]13[C@@H]2[C@@H](O)[C@@H]4O',
                                      'name': 'yadanziolide B',
                                      'reason': 'Carbon count 20 not in '
                                                'typical triterpenoid range '
                                                '(27-50 carbons)'},
                                  {   'smiles': 'O=C(O[C@@H]1[C@](O)([C@H](OCC(OC(=O)C)C(OC(=O)C)C(OC(=O)C)CCC([C@@H]2[C@H]3[C@]([C@@H]4[C@@]([C@]5([C@@H]([C@@]6([C@H](C(CCC6)(C)C)CC5)C)CC4)C)(C)CC3)(C)CC2)C)[C@@H]([C@H]1OC(=O)C)NC(=O)C)COC(=O)C)C',
                                      'name': '[(1R,2R,3R,4R,5S)-2-[7-[(3R,3aS,5aR,5bR,7aS,11aS,11bR,13aR,13bS)-5a,5b,8,8,11a,13b-hexamethyl-1,2,3,3a,4,5,6,7,7a,9,10,11,11b,12,13,13a-hexadecahydrocyclopenta[a]chrysen-3-yl]-2,3,4-triacetyloxyoctoxy]-3-acetamido-4,5-diacetyloxy-1-hydroxycyclopentyl]methyl '
                                              'acetate',
                                      'reason': 'Carbon count 55 not in '
                                                'typical triterpenoid range '
                                                '(27-50 carbons)'},
                                  {   'smiles': 'O=C(OC)/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/CC(O)(C)C)\\C)\\C)\\C)/C)/C',
                                      'name': 'methyl '
                                              'hydroxy-3,4-dehydro-apo-8′-lycopenoate',
                                      'reason': 'Only 0 rings found, '
                                                'triterpenoids typically have '
                                                'at least 4 rings'},
                                  {   'smiles': 'O=C1C(C2[C@](C3=C([C@]4([C@]([C@@H](C(C(=O)O)C)CC4)(C)CC3)C)CC2)(C)CC1)(C)C',
                                      'name': 'Torulosic acid',
                                      'reason': 'Carbon count 25 not in '
                                                'typical triterpenoid range '
                                                '(27-50 carbons)'},
                                  {   'smiles': 'COC(=O)[C@@]12OC[C@@]34[C@H]1[C@@H](OC(C)=O)C(=O)O[C@@H]3C[C@H]1C(C)=C(OC(C)=O)C(=O)C[C@]1(C)[C@H]4[C@@H](O)[C@@H]2O',
                                      'name': '3,15-di-O-acetylbruceolide',
                                      'reason': 'Carbon count 25 not in '
                                                'typical triterpenoid range '
                                                '(27-50 carbons)'},
                                  {   'smiles': '[H][C@@]12C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]3([H])[C@@H](O)[C@H](O)[C@]4(OC[C@@]13[C@@]4([H])[C@@H](OC(=O)CC(C)C)C(=O)O2)C(=O)OC',
                                      'name': 'isobrucein A',
                                      'reason': 'Carbon count 26 not in '
                                                'typical triterpenoid range '
                                                '(27-50 carbons)'},
                                  {   'smiles': '[H][C@@]12OC(=O)[C@@]3([H])[C@]1(C)OC[C@]31C(=O)C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]1([H])[C@H]2O',
                                      'name': 'samaderine B',
                                      'reason': 'Carbon count 19 not in '
                                                'typical triterpenoid range '
                                                '(27-50 carbons)'},
                                  {   'smiles': 'O=C(OC)C(=CC=CC(=CC=CC(=CC=CC=C(C=CC=C(C=CCC(CC1OC(C(O)C(C1O)O)CO)(C)C)C)C)C)C)C',
                                      'name': 'methyl '
                                              '5-glucosyl-5,6-dihydro-apo-4,4′-lycopenoate',
                                      'reason': 'Only 1 rings found, '
                                                'triterpenoids typically have '
                                                'at least 4 rings'}],
    'attempt': 1,
    'reasoning': "After analyzing the previous program and the outcomes, it's "
                 'evident that the classification criteria were too simplistic '
                 'and resulted in both false positives and false negatives:\n'
                 '\n'
                 '**Issues with the Previous Code:**\n'
                 '\n'
                 '1. **False Negatives:** The carbon count range (24-33) was '
                 'too narrow, excluding valid triterpenoids that have higher '
                 'carbon counts due to modifications like glycosylation or '
                 'esterification. As a result, several true triterpenoids were '
                 'missed.\n'
                 '\n'
                 '2. **False Positives:** The criteria were not specific '
                 'enough to triterpenoids. Molecules that met the basic '
                 'requirements (carbon count, oxygen atoms, rings) but were '
                 'not triterpenoids were incorrectly classified as such.\n'
                 '\n'
                 '**Improvements to Address These Issues:**\n'
                 '\n'
                 '- **Adjust Carbon Count Range:** Expand the acceptable '
                 'carbon count range to include larger triterpenoids with '
                 'modifications. Set the range from 27 to 50 carbons.\n'
                 '\n'
                 '- **Implement Structural Checks:**\n'
                 '  - **Fused Ring Systems:** Triterpenoids typically have '
                 'tetracyclic or pentacyclic fused ring systems. Check for at '
                 'least four fused rings in the molecule.\n'
                 '  - **Saturation Level:** Triterpenoids often have a high '
                 'degree of saturation, meaning a high fraction of '
                 'sp<sup>3</sup> hybridized carbons. Calculate the fraction of '
                 "sp<sup>3</sup> carbons and ensure it's sufficiently high "
                 '(e.g., ≥ 0.6).\n'
                 '\n'
                 '- **Exclude Non-Triterpenoids:** Tighten the criteria to '
                 'exclude molecules that are not structurally similar to '
                 'triterpenoids, even if they meet the basic counts.\n'
                 '\n'
                 'By implementing these improvements, we aim to reduce both '
                 'false positives and false negatives, thereby improving the '
                 'overall classification performance.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1576,
    'num_false_positives': 3592,
    'num_true_negatives': 136777,
    'num_false_negatives': 355,
    'num_negatives': None,
    'precision': 0.30495356037151705,
    'recall': 0.8161574313827032,
    'f1': 0.4440061980560642,
    'accuracy': 0.9722628250175686,
    'negative_predictive_value': 0.9974112533908934}