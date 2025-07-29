"""
Classifies: CHEBI:72600 spiroketal
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_spiroketal(smiles: str):
    """
    Determines if a molecule is a spiroketal based on its SMILES string.
    A spiroketal is a cyclic ketal in which the ketal carbon is the only common atom of two rings.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a spiroketal, False otherwise
        str: Reason for classification
    """

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check if there are at least two rings in the molecule
    if mol.GetRingInfo().NumRings() < 2:
         return False, "Molecule does not have at least two rings."


    # 1. Identify ketal carbons: carbon bonded to two oxygens (sp3 hybridized), zero hydrogens and two carbons (within rings).
    ketal_pattern = Chem.MolFromSmarts("[CX4H0](-[OX2;R])(-[OX2;R])([CX4;R])([CX4;R])")
    ketal_matches = mol.GetSubstructMatches(ketal_pattern)

    if not ketal_matches:
        return False, "No ketal carbon found."
    
    
    for match in ketal_matches:
        ketal_carbon_idx = match[0]
        ketal_carbon = mol.GetAtomWithIdx(ketal_carbon_idx)
        
        # Get oxygen atoms bonded to ketal carbon
        oxygen_indices = [neighbor.GetIdx() for neighbor in ketal_carbon.GetNeighbors() if neighbor.GetAtomicNum() == 8]
        if len(oxygen_indices) != 2:
            continue # Should not happen

        oxy1_idx = oxygen_indices[0]
        oxy2_idx = oxygen_indices[1]

        # Verify that both oxygens are part of rings.
        oxy1 = mol.GetAtomWithIdx(oxy1_idx)
        oxy2 = mol.GetAtomWithIdx(oxy2_idx)
        if not oxy1.IsInRing() or not oxy2.IsInRing():
            continue

        # 2. Find the smallest ring containing each oxygen
        ring_info = mol.GetRingInfo()
        
        rings_oxy1 = [set(ring) for ring in ring_info.AtomRings() if oxy1_idx in ring]
        rings_oxy2 = [set(ring) for ring in ring_info.AtomRings() if oxy2_idx in ring]

        if not rings_oxy1 or not rings_oxy2:
             continue


        # Find smallest rings by size
        if rings_oxy1 and rings_oxy2:
            smallest_ring_oxy1 = min(rings_oxy1, key=len)
            smallest_ring_oxy2 = min(rings_oxy2, key=len)


            # 3. Verify if the two smallest rings intersect ONLY at the ketal carbon
            smallest_ring_oxy1.discard(ketal_carbon_idx)
            smallest_ring_oxy2.discard(ketal_carbon_idx)
            if not smallest_ring_oxy1.intersection(smallest_ring_oxy2):
                return True, "Spiroketal structure identified."
            
    return False, "No spiroketal structure detected."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:72600',
                          'name': 'spiroketal',
                          'definition': 'A cyclic ketal in which the ketal '
                                        'carbon is the only common atom of two '
                                        'rings.',
                          'parents': ['CHEBI:37948', 'CHEBI:59779'],
                          'xrefs': [   'PMID:19262920',
                                       'PMID:20024126',
                                       'PMID:21076755',
                                       'PMID:21604735',
                                       'PMID:21860857',
                                       'PMID:22421755'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
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
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'GetIdx',
                                                 'NumRings',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetNeighbors',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'GetSubstructMatches',
                                                 'GetRingInfo'],
                           'methods_called_count': 9,
                           'smarts_strings': [   '[CX4H0](-[OX2;R])(-[OX2;R])([CX4;R])([CX4;R])'],
                           'smarts_strings_count': 1,
                           'defs': ['is_spiroketal(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule does not have at '
                                          'least two rings."',
                                          'False, "No ketal carbon found."',
                                          'False, "No spiroketal structure '
                                          'detected."'],
                           'returns_count': 4,
                           'complexity': 4.0664409020350405},
    'message': '\n'
               'Attempt failed: F1 score of 0.2633228840125392 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C([C@]4([C@H]1C=C([C@@H](O)C4)C)O)C)C)C)O[C@@H]([C@@H](C)CC3)C '
               'NAME: Milbemycin beta12 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1OC2CC3(OC(C(C)CC3)C(CC)C)OC(C2)CC=C(C(O)C(C=CC=C4C5(C1C=C(C(O)C5OC4)C)O)C)C '
               'NAME: Ivermectin B1 aglycone REASON: CORRECT Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'CCC(C)[C@H]1O[C@@]2(C[C@@H]3C[C@@H](C\\C=C(C)\\[C@@H](O)[C@@H](C)\\C=C\\C=C4/CO[C@@H]5[C@H](O)C(C)=C[C@@H](C(=O)O3)[C@]45O)O2)C[C@H](O)[C@@H]1C '
               'NAME: Avermectin B2a aglycone REASON: CORRECT Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](C(=CC)C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](OC)[C@H]5OC4)C)O)C)C '
               'NAME: VM-44864 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               '[C@@]12(C3=CC=C[C@@H](CC(=CC[C@]4(O[C@@]5(C[C@H](C4)OC([C@]1([H])C=C(C)[C@H]([C@@]2([H])OC3)O)=O)O[C@@H]([C@H](CC5)C)C(C)C)[H])C)C)O '
               'NAME: milbemycin D REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](C)[C@H](O[C@@](O)([C@H](C)C(O)=O)[C@@H]1C)[C@H](C)[C@H]1O[C@@]2(CC[C@](C)(O2)[C@H]2CC[C@](C)(O2)[C@@H]2O[C@H](C[C@@H]2C)[C@H]2O[C@](C)(O)[C@H](C)C[C@@H]2C)C[C@H](O)[C@H]1C '
               'NAME: mutalomycin REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1OC2CC3(OC(C(C)CC3)C(CC)C)OC(C2)CC=C(C(OC4OC(C(O)C(C4)OC)C)C(C=CC=C5C6(C1C=C(C(O)C6OC5)C)O)C)C '
               'NAME: Ivermectin monosaccharide REASON: CORRECT Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@H](CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1([H])[C@H](C)[C@@]1(CC[C@@](C)(CO[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)O1)O2)O[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: avenacoside A REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               '[H][C@@]12C\\C=C(C)\\C[C@@H](C)\\C=C\\C=C3/CO[C@]4([H])[C@H](O)C(C)=C[C@@]([H])(C(=O)O[C@@H](C1)C[C@]1(CC[C@H](C)[C@@H](CC)O1)O2)[C@]34O '
               'NAME: milbemycin A4 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C(C4=C1C=C(C)C(=C4)O)CO)C)C)O[C@@H]([C@@H](C)CC3)C '
               'NAME: Milbemycin beta13 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               '[C@@H]1([C@H](CC[C@]2(O1)C[C@@H]3OC(C=C[C@H](C)[C@@H](O)[C@H](C)C(=O)[C@H](C)[C@@H](O)[C@H](C)C([C@@]([C@@H](O)[C@H](C)CC=CC=C[C@@H](CC[C@@H]([C@H]3C)O2)CC)(O)C)=O)=O)C)C[C@H](O)C '
               'NAME: oligomycin D REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)C5OC4C)C)O)C)C '
               'NAME: VM-44866 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C([C@]4([C@H]1C=C([C@@H](O)[C@H]4O)C)O)C)C)C)O[C@@H]([C@@H](C)CC3)C '
               'NAME: Milbemycin beta11 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C([C@H](O)[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](OC)[C@H]5OC4)C)O)C)C '
               'NAME: UK-78618 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1OC2CC3(OC(C(C)CC3)C(CC)C)OC(C2)CC=C(C(OC4OC(C(OC5OC(C(O)C(C5)OC)C)C(C4)OC)C)C(C=CC=C6C7(C1C=C(C(O)C7OC6)C)O)C)C '
               'NAME: epi-Ivermectin B1a REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)[C@H](C3)O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](OC)[C@H]5OC4)C)O)C)C '
               'NAME: LL-F28249gamma REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1OC2CC3(OC(C(=CC(C)C)C)C(C)C(C3)O)OC(C2)CC=C(CC(C=CC=C4C5(C1C=C(C(O)C5OC4)C)O)C)C '
               'NAME: Nemadectin REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'CCC(C)[C@@H]1[C@H](CC[C@@]2(O1)C[C@@H]3C[C@H](O2)CC=C([C@H]([C@H](C=CC=C4CO[C@H]5[C@@]4([C@@H](C=C([C@H]5O)C)C(=O)O3)O)C)OC6C[C@@H](C([C@@H](O6)C)O[C@H]7C[C@@H]([C@H]([C@@H](O7)C)O)OC)OC)C)C '
               'NAME: LSM-1593 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'CC[C@@H](O)C[C@H]1CCC[C@@]2(C[C@@H]3OC(=O)\\C=C\\[C@@](C)(O)[C@@H](O)[C@H](C)[C@@H](O)[C@H](O[C@H]4CC[C@@H]([C@H](C)O4)N(C)C)[C@@H](O)[C@](C)(O)CCCCC\\C=C\\[C@@H]4CC(C)(C)O[C@@]4(O)C[C@H](O2)[C@H]3C)O1 '
               'NAME: ossamycin REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)[C@H]5OC4)COC(=O)C=6NC=CC6)O)C)C)O[C@@H]([C@@H](C)[C@@H]([C@H]3O)OC(=O)C(CC)C)C '
               'NAME: Milbemycin alpha28 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)[C@@H]([C@H]3O)OC(=O)C(C)C)O[C@@H](C2)CC=C([C@H](O)[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)[C@H]5OC4)C)O)C)C '
               'NAME: UK-78621 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)[C@H]5OC4)CO)O)C)C)O[C@@H]([C@@H](C)CC3)C '
               'NAME: Milbemycin alpha26 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)CC3)O[C@@H](C2)CC=C([C@H](OC(=O)C(C)C)[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](OC)[C@H]5OC4)C)O)C)C '
               'NAME: UK-78630 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O1C2(OC3CC(OC(=O)C4C(O)(CC(OC)C(=C4)C)C(CO)=CC=CC(CC(=CC3)C)C)C2)CCC(C1CC)C '
               'NAME: Milbemycin beta2 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C([C@]4([C@H]1C=C([C@@H](OC)C4)C)O)CO)C)C '
               'NAME: VM48640 REASON: CORRECT Spiroketal structure '
               'identified.\n'
               'False positives: SMILES: '
               'O=C1C2=C(C[C@]3(O[C@H](CCC3)C)OC2)[C@H]([C@]1(O)C)O NAME: '
               'Thielavialide B REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@](CC4)(C[C@@H](O)CC5)[H])C)(CC3=O)[H])[H])(C2)[H])C)([C@@H]([C@]16OCC(CC6)=C)C)[H])[H] '
               'NAME: Schidigeragenin B REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               '[H][C@]12CCCC[C@]1(C)[C@@]1([H])CC[C@@]3(C)[C@@]([H])(C[C@]4([H])O[C@]5(CC[C@@H](C)CO5)[C@@H](C)[C@]34[H])[C@]1([H])CC2 '
               'NAME: (25R)-5alpha-spirostan REASON: WRONGLY CLASSIFIED '
               'Spiroketal structure identified.\n'
               ' * SMILES: '
               'O=C1OC(CCCCCC[C@@H]2O[C@]3(O[C@@H](C)CC3)CC2)C=4C1=C(OC)C=C(OC)C4 '
               'NAME: CJ-12,954 REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'CC[C@]1(CCC(O1)[C@@]2(CCC3(O2)C[C@@H]([C@H]([C@H](O3)[C@@H](C)[C@H]([C@H](C)C(=O)O)OC)C)O)C)C4[C@H](C[C@@H](O4)C5[C@H](C[C@H]([C@@](O5)(CO)O)C)C)C '
               'NAME: '
               '(2S,3R,4S)-4-[(2S,7S,8R,9S)-2-[(5S)-5-ethyl-5-[(3S,5R)-5-[(3S,5R,6R)-6-hydroxy-6-(hydroxymethyl)-3,5-dimethyl-2-oxanyl]-3-methyl-2-oxolanyl]-2-oxolanyl]-7-hydroxy-2,8-dimethyl-1,10-dioxaspiro[4.5]decan-9-yl]-3-methoxy-2-methylpentanoic '
               'acid REASON: WRONGLY CLASSIFIED Spiroketal structure '
               'identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C4C5=C1C=C(C)C(=C5OC4=O)O)C)C)O[C@@H]([C@@H](C)CC3)CC '
               'NAME: 27-oxomilbemycin alpha31 REASON: WRONGLY CLASSIFIED '
               'Spiroketal structure identified.\n'
               ' * SMILES: '
               'O1[C@@]2(OCC=3C(O)=C(C)C(=CC3[C@H]2O)O)[C@@H](O)CC[C@@H]1C '
               'NAME: Sargabetaopenilline A REASON: WRONGLY CLASSIFIED '
               'Spiroketal structure identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@@]2(O[C@]3(O[C@@]([C@H](O)CC)(C)[C@@H]([C@H]3C)O)[C@@H](C2)C)C)[C@@H](C)C=C1C '
               'NAME: Erythronolide I REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'OC(CC/C=C/[C@@]1(C=CC[C@]2(O1)OC3(CC2)[C@@H](C[C@@]4([C@](O3)(C[C@](O4)([C@H]([C@@]5(O[C@@]([C@H](C[C@H]5C)C)(C(=C)C[C@@]67C[C@H](C[C@@H](O6)[C@@]8([C@](O7)(C[C@]9(O8)[C@H](C[C@H](CN9)C)C)[H])[H])C)[H])O)O)[H])[H])[H])C)[H])=O '
               'NAME: azaspiracid-1 REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               '[H][C@]12C\\C=C/C[C@@]3([H])O[C@@]4([H])C=C[C@@]5([H])O[C@@]6([H])[C@H](O)[C@@]7([H])O[C@]([H])(C=CC[C@]7([H])O[C@]6([H])C[C@]5([H])O[C@]4([H])C=C[C@]3([H])O[C@]1([H])C[C@@H](O)[C@]1(C)O[C@]3([H])C[C@H](C)C[C@]4([H])O[C@]5([H])[C@@H](C)[C@H](O)[C@]6([H])O[C@]7(C[C@H](O)CO7)[C@@H](C)[C@H](C)[C@@]6([H])O[C@@]5([H])C[C@@]4([H])O[C@@]3([H])C[C@@]1([H])O2)\\C=C\\[C@H](O)CO '
               'NAME: ciguatoxin CTX1B REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'C[C@H]1[C@H]2[C@H](C[C@H]3[C@@H]4CC[C@H]5C[C@@H](O)[C@H](O)C[C@]5(C)[C@H]4CC[C@]23C)O[C@]11CC[C@H](C)CO1 '
               'NAME: Neogitogenin REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'CCC1CCC2[C@@H](C([C@H](C3(O2)CC[C@H](C(O3)C[C@H](C)O)C)C)OC(=O)C=C[C@H]([C@@H]([C@H](C(=O)[C@@H]([C@H]([C@@H](C(=O)[C@@]([C@@H]([C@H](CC=CC=C1)C)O)(C)O)C)O)C)C)O)C)C '
               'NAME: '
               "(5'R,10S,11R,12S,14S,15R,16R,18R,19S,20R,26R,29S)-4-ethyl-11,12,15,19-tetrahydroxy-6'-[(2S)-2-hydroxypropyl]-5',10,12,14,16,18,20,26,29-nonamethylspiro[24,28-dioxabicyclo[23.3.1]nonacosa-5,7,21-triene-27,2'-oxane]-13,17,23-trione "
               'REASON: WRONGLY CLASSIFIED Spiroketal structure identified.\n'
               ' * SMILES: '
               'O=C(O)/C=C/C=C/[C@@H]([C@@H]1O[C@]2(O[C@@H]([C@@H](C)[C@@H](C2)O)C)[C@@H](C)[C@@H]([C@@H]1C)O)C '
               'NAME: Pteridic acid E REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O=C1O[C@]2(OC[C@@H](CC[C@H]3C([C@H](C(=C)CC3)[C@@H](OC(=O)C)C=C4C(=O)OCC4)(C)C)CC2)[C@]5(C)C[C@@]1(O)C(O5)(C)C '
               'NAME: Terreolide F REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2[C@@H]([C@@H](O[C@]3(C2)O[C@H]([C@@H](C)CC3)C[C@H](O)CC)CC[C@H](C=CC=CCC[C@H]([C@H]([C@H](C[C@H](C[C@H]([C@@H]([C@@H]([C@H](C=C1)C)O)C)O)OC)O)C)O)CC)CCCO '
               'NAME: Neomaclafungin C REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O=C1O[C@@]2(O[C@H](OCC3=C(/C=C/CCCCC)[C@@H](O)[C@H]4[C@@]5([C@H]3OC([C@@H](O)C5)(C)C)O4)[C@]6(C2)[C@@H]7C(=C)[C@@H](OC(=O)C([C@@H](O)C)(C)C)C[C@H]6C7)C[C@@H]1C '
               'NAME: Eutypellacytosporin A REASON: WRONGLY CLASSIFIED '
               'Spiroketal structure identified.\n'
               ' * SMILES: '
               'O=C(O)/C=C(/C=C/[C@H](OC(=O)CCC(=O)O)[C@@]1(O[C@]2(O[C@@H]([C@@H](C)CC2)C/C=C(/C=C/[C@H](O)[C@H](/C=C/C(=O)O)C)\\C)CC1)CCCCCC)\\C '
               'NAME: Reveromycin G REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: O1[C@@]2(O[C@H](CCC2)C)C[C@@H](C[C@@H]1C)C NAME: '
               '(2S,4R,6R,8S)-2,4,8-Trimethyl-1,7-dioxaspiro-[5.5]undecane '
               'REASON: WRONGLY CLASSIFIED Spiroketal structure identified.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@H](CCCC(=O)O)CC3)O[C@@H]2C1(C)C NAME: '
               'Cephalosporolide I REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O1[C@]2(NC[C@H](C[C@H]2C)C)C[C@@]3(O[C@]4(O[C@]([C@]13[H])(C[C@H](C4)C)[H])CC([C@H]5O[C@@](O)([C@@H](O)[C@@]6(O[C@@]7([C@@](O[C@]8(O[C@]9(O[C@@H](CC=C9)/C=C/CCC(O)=O)CC8)[C@H](C7)C)(C6)[H])[H])[H])CC[C@@H]5C)=C)[H] '
               'NAME: Azaspiracid 3 REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O=C1C2=CC(=O)CC[C@@]2([C@@]3(O)C=C[C@]4([C@]5(C3=C1)O[C@@]6(OC(C)(C)[C@H]([C@H]6O)C)[C@@H](C)[C@H]4CC5)C)C '
               'NAME: Blazeispirol Y REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@@](CC4)(C[C@@H](O)CC5)[H])C)(CC3=O)[H])[H])(C2)[H])C)([C@@H]([C@]16OC[C@H](CC6)C)C)[H])[H] '
               'NAME: Sisalagenin REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               'O=C1C=2C(=CC([C@@]1(OC(=O)C)C)=O)[C@@H](OC(=O)/C(=C/C=C/C)/C)[C@]3(O[C@H](CC[C@H]3O)C)OC2 '
               'NAME: Daldinin E REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               ' * SMILES: '
               '[Na+].O=C([O-])C(C(OC)C(C1OC2(OC(C3OC(C4OC(C5OC(O)(C(C)CC5C)CO)CC4C)(CC)CC3)(C)CC2)CC(C1C)O)C)C '
               'NAME: Monensin sodium salt REASON: WRONGLY CLASSIFIED '
               'Spiroketal structure identified.\n'
               ' * SMILES: '
               'O=C(O)[C@H](C[C@H](C(=O)/C(=C/[C@@H]([C@H]1O[C@]2(O[C@@]([C@@H]3OC4(O[C@@H]([C@@H]5O[C@@](O)([C@@H](C)C[C@H]5C)CO)C[C@@H]4C)[C@H](C)CC3)(C)[C@@H](C2)O[C@@H]6O[C@@H]([C@@H](OC)CC6)C)C[C@@H]([C@H]1C)O)C)/C)C)C '
               'NAME: Endusamycin REASON: WRONGLY CLASSIFIED Spiroketal '
               'structure identified.\n'
               'False negatives: SMILES: '
               '[C@@]123O[C@]([C@H](C)CC1(C)C)(CC(O[C@@]([C@@H](C)O)(CC(OC(C2)[C@H](C)[C@](O3)([C@H](CC[C@@H](C=4C=CC=C(C4)O)OC)C)[H])=O)[H])=O)O '
               'NAME: debromoaplysiatoxin REASON: MISSED No spiroketal '
               'structure detected.\n'
               ' * SMILES: '
               'CCCCC\\C=C\\C=C\\C(=O)OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)O[C@]3(OCc4cc(O)cc(O)c34)[C@H](O)[C@H]2OC(=O)\\C=C\\C=C\\C[C@H](O)C(\\C)=C\\C=C\\CC[C@@H](C)CC)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: papulacandin A REASON: MISSED No ketal carbon found.\n'
               ' * SMILES: '
               '[C@]12([C@@H]([C@](O[C@]3(O1)[C@H]([C@H](O[C@]3(CC2=O)C)C)C(=O)OC)([C@H](C)/C=C(\\C)/C=C/C(=C/4\\C(NCC4=O)=O)/O)[H])C)[H] '
               'NAME: nocamycin I REASON: MISSED No spiroketal structure '
               'detected.\n'
               ' * SMILES: '
               'O1[C@@]23O[C@](C[C@@]1(CC2)C)([C@]4(O[C@](CC4=O)([C@@H](O)[C@]5(O[C@@]6(O[C@@](CCC6)([C@H](C(O[C@@]7(C[C@](O[C@@]7(C=CC(=C[C@@H](C[C@@]8(O[C@@]3(CC8)[H])C)C)C)[H])([C@]9(OCC[C@H]([C@H]9O)C)O)[H])[H])=O)C)[H])CC5)[H])C)[H])[H] '
               'NAME: Pectenotoxin 2 REASON: MISSED No spiroketal structure '
               'detected.\n'
               ' * SMILES: '
               'O1C23O[C@](C[C@]1(CC2)C(O)=O)([C@]4(O[C@@]([C@@H](O)[C@]5(OC6(O[C@@](CCC6)([C@H](C(O[C@@]7(C[C@](O[C@@]7(C=CC(=C[C@@H](C[C@@]8(O[C@@]3(CC8)[H])C)C)C)[H])([C@]9(OCC[C@H]([C@H]9O)C)O)[H])[H])=O)C)[H])CC5)[H])(CC4=O)C)[H])[H] '
               'NAME: Pectenotoxin 7 REASON: MISSED No spiroketal structure '
               'detected.\n'
               ' * SMILES: '
               '[C@@]123O[C@]([C@H](C)CC1(C)C)(CC(O[C@@]([C@@H](C)O)(CC(OC(C2)[C@H](C)[C@](O3)([C@H](CC[C@@H](C=4C(=CC(=C(C4)O)Br)Br)OC)C)[H])=O)[H])=O)O '
               'NAME: 19-bromoaplysiatoxin REASON: MISSED No spiroketal '
               'structure detected.\n'
               ' * SMILES: '
               '[C@]12([C@@H]([C@](O[C@]3(O1)[C@H]([C@H](O[C@]3(CC2=O)C)C)C(=O)O)([C@H](C)/C=C(\\C)/C=C/C(=C/4\\C(NCC4=O)=O)/O)[H])C)[H] '
               'NAME: nocamycin E REASON: MISSED No spiroketal structure '
               'detected.\n'
               ' * SMILES: NC(=N)NCC1COC2(CCCCC2)O1 NAME: guanadrel REASON: '
               'MISSED No spiroketal structure detected.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1(F)[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@H]2OC3(CCCC3)O[C@@]12C(=O)COC(C)=O '
               'NAME: amcinonide REASON: MISSED No spiroketal structure '
               'detected.\n'
               ' * SMILES: '
               'CC[C@@H]1CC[C@@H]2O[C@@]3(O[C@@H](C[C@@H](C)O)[C@@H](C)CC3=O)[C@@H](C)[C@H](OC(=O)\\C=C\\[C@H](C)[C@@H](O)[C@H](C)C(=O)[C@H](C)[C@@H](O)[C@H](C)C(=O)[C@](C)(O)[C@@H](O)[C@H](C)C\\C=C\\C=C\\1)[C@@H]2C '
               'NAME: oligomycin B REASON: MISSED No ketal carbon found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@@H](OC[C@H]2OC(O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1CO',
                                     'name': 'beta-D-Galp-(1->6)-D-GalpNAc',
                                     'reason': 'No ketal carbon found.'},
                                 {   'smiles': 'O1C=2C(C(=CC1=O)CC)=CC=C(OC(=O)C=3OC=CC3)C2',
                                     'name': '(4-Ethyl-2-oxochromen-7-yl) '
                                             'furan-2-carboxylate',
                                     'reason': 'No ketal carbon found.'},
                                 {   'smiles': 'CCCNC(=O)[C@H]1[C@@H]([C@H]2CN3C(=CC=C(C3=O)C4=CC=NC=C4)[C@@H]1N2CC5=CC=CC=C5F)CO',
                                     'name': 'LSM-13437',
                                     'reason': 'No ketal carbon found.'},
                                 {   'smiles': 'CC1(C)[C@H]2CC[C@]1(CS([O-])(=O)=O)C(=O)C2',
                                     'name': '(R)-camphorsulfonate',
                                     'reason': 'No ketal carbon found.'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O',
                                     'name': 'PS(18:2(9Z,12Z)/20:2(11Z,14Z))',
                                     'reason': 'Molecule does not have at '
                                               'least two rings.'},
                                 {   'smiles': 'N[C@@H](CCCC(O)=O)C(O)=O',
                                     'name': 'L-2-aminoadipic acid',
                                     'reason': 'Molecule does not have at '
                                               'least two rings.'},
                                 {   'smiles': 'C(\\CC)=C\\C/C=C\\CC1C(C/C=C\\C/C=C\\CCCC(=O)O)O1',
                                     'name': '(5Z,8Z,14Z,17Z)-11,12-epoxyicosatetraenoic '
                                             'acid',
                                     'reason': 'Molecule does not have at '
                                               'least two rings.'},
                                 {   'smiles': 'O[C@H]1[C@@H](CCC(=CCCC(=C1)C)C)C(C(O)=O)=C',
                                     'name': '2-[(1S,2R,3E,7E)-2-Hydroxy-4,8-dimethylcyclodeca-3,7-dien-1-yl]prop-2-enoic '
                                             'acid',
                                     'reason': 'Molecule does not have at '
                                               'least two rings.'},
                                 {   'smiles': 'C1[C@@H]2[C@H]([C@@H]([C@@H](N2CC3=CN=CC=C3)C4=CC=CC(=O)N41)C(=O)NCC5=CC6=C(C=C5)OCO6)CO',
                                     'name': 'LSM-8906',
                                     'reason': 'No ketal carbon found.'},
                                 {   'smiles': '[H][C@]1(CC(=O)c2c(O)cc(O)c(C[C@@H](CC=C(C)C)C(C)=C)c2O1)c1c(O)cccc1O',
                                     'name': 'exiguaflavanone A',
                                     'reason': 'No ketal carbon found.'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCC\\C=C\\C=C\\C(=O)OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)O[C@]3(OCc4cc(O)cc(O)c34)[C@H](O)[C@H]2OC(=O)\\C=C\\C=C\\C[C@H](O)C(\\C)=C\\C=C\\CC[C@@H](C)CC)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'papulacandin A',
                                      'reason': 'No ketal carbon found.'},
                                  {   'smiles': '[C@]12([C@@H]([C@](O[C@]3(O1)[C@H]([C@H](O[C@]3(CC2=O)C)C)C(=O)OC)([C@H](C)/C=C(\\C)/C=C/C(=C/4\\C(NCC4=O)=O)/O)[H])C)[H]',
                                      'name': 'nocamycin I',
                                      'reason': 'No spiroketal structure '
                                                'detected.'},
                                  {   'smiles': '[C@]12([C@@H]([C@](O[C@]3(O1)[C@H]([C@H](O[C@]3(CC2=O)C)C)C(=O)O)([C@H](C)/C=C(\\C)/C=C/C(=C/4\\C(NCC4=O)=O)/O)[H])C)[H]',
                                      'name': 'nocamycin E',
                                      'reason': 'No spiroketal structure '
                                                'detected.'},
                                  {   'smiles': 'NC(=N)NCC1COC2(CCCCC2)O1',
                                      'name': 'guanadrel',
                                      'reason': 'No spiroketal structure '
                                                'detected.'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1(F)[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@H]2OC3(CCCC3)O[C@@]12C(=O)COC(C)=O',
                                      'name': 'amcinonide',
                                      'reason': 'No spiroketal structure '
                                                'detected.'},
                                  {   'smiles': 'CC[C@@H]1CC[C@@H]2O[C@@]3(O[C@@H](C[C@@H](C)O)[C@@H](C)CC3=O)[C@@H](C)[C@H](OC(=O)\\C=C\\[C@H](C)[C@@H](O)[C@H](C)C(=O)[C@H](C)[C@@H](O)[C@H](C)C(=O)[C@](C)(O)[C@@H](O)[C@H](C)C\\C=C\\C=C\\1)[C@@H]2C',
                                      'name': 'oligomycin B',
                                      'reason': 'No ketal carbon found.'},
                                  {   'smiles': 'CCCN(CC)CC1COC2(CCC(CC2)C(C)(C)C)O1',
                                      'name': 'spiroxamine',
                                      'reason': 'No spiroketal structure '
                                                'detected.'},
                                  {   'smiles': 'CC[C@H](C)[C@H]1O[C@@]2(C[C@@H]3C[C@@H](C\\C=C(C)\\[C@@H](O[C@H]4C[C@H](OC)[C@@H](O[C@H]5C[C@H](OC)[C@@H](NC(C)=O)[C@H](C)O5)[C@H](C)O4)[C@@H](C)\\C=C\\C=C4/CO[C@@H]5[C@H](O)C(C)=C[C@@H](C(=O)O3)[C@]45O)O2)C=C[C@@H]1C',
                                      'name': 'eprinomectin component B1a',
                                      'reason': 'No ketal carbon found.'},
                                  {   'smiles': 'CO[C@H]1C[C@H](O[C@H]2[C@H](C)O[C@H](C[C@@H]2OC)O[C@H]2[C@@H](C)\\C=C\\C=C3/CO[C@@H]4[C@H](O)C(C)=C[C@@H](C(=O)O[C@H]5C[C@@H](C\\C=C2/C)O[C@@]2(C5)O[C@H](C(C)C)[C@@H](C)C=C2)[C@]34O)O[C@@H](C)[C@@H]1NC(C)=O',
                                      'name': 'eprinomectin component B1b',
                                      'reason': 'No ketal carbon found.'},
                                  {   'smiles': 'CC[C@H](C)CC\\C=C\\C=C(/C)[C@@H](O)C\\C=C\\C=C\\C(=O)O[C@@H]1[C@@H](O)[C@@]2(OCc3cc(O)cc(O)c23)O[C@H](CO)[C@H]1O[C@@H]1O[C@H](COC(=O)\\C=C\\C=C\\C=C\\C(O)CC)[C@H](O)[C@H](O)[C@H]1O',
                                      'name': 'papulacandin C',
                                      'reason': 'No ketal carbon found.'}],
    'attempt': 3,
    'reasoning': "Okay, let's analyze the performance of the previous "
                 '`is_spiroketal` function and devise a strategy to improve '
                 'it.\n'
                 '\n'
                 '**Analysis of Errors:**\n'
                 '\n'
                 '*   **False Positives:** The code incorrectly identified '
                 'several structures as spiroketals, including structures with '
                 'fused rings, hemiketals (where one of the oxygens is an OH), '
                 'and even simple ethers within complex molecules. This '
                 'suggests that the logic for determining if the two rings '
                 'sharing the ketal carbon are *distinct* is too permissive. '
                 'The code appears to check for the absence of common atoms '
                 'other than the spiro carbon, but does not adequately check '
                 'if the two rings are truly independent.\n'
                 '*   **False Negatives:** The code missed several true '
                 'spiroketals. Many of the missed examples are complex '
                 'macrocycles, which may indicate the code is having trouble '
                 'handling larger ring systems or multiple instances of ketal '
                 'functionality in the same molecule. The code also seems to '
                 'have issues with recognizing ketals that are part of larger '
                 'functional groups (e.g., a ketal linked to a sugar) and '
                 'ketals within complex stereochemistry, especially when they '
                 'are in an unusual position in a chain (e.g. side chains or '
                 'at the end of chains).\n'
                 '*   **Issues with Ring Detection:** The current '
                 'implementation tries to find all rings that contain each '
                 'oxygen and check if there are common atoms. However, the '
                 'approach of iterating through all possible ring combinations '
                 'becomes complex and is likely not robust enough, especially '
                 'with larger molecules. The problem is that '
                 '`rdkit.Chem.rdMolDescriptors.CalcNumRings()` gives a number '
                 'of rings but not the rings atoms and '
                 '`mol.GetRingInfo().AtomRings()` return all the rings, '
                 'including fused rings and cycles that are part of larger '
                 'structures that are not necessarily spiroketals.\n'
                 '*   **Pattern Matching**: The SMARTS pattern '
                 '`[CX4H0](-[OX2])(-[OX2])([CX4])([CX4])` identifies a ketal '
                 "carbon, but it doesn't check for the key characteristic of "
                 'spiroketals: a single common carbon in two *independent* '
                 'rings.\n'
                 '\n'
                 '**Proposed Improvements:**\n'
                 '\n'
                 '1.  **More Specific Ketal SMARTS:** The initial SMARTS '
                 'pattern needs to be more specific for a ketal carbon within '
                 'a spirocyclic structure. We want to find a carbon connected '
                 'to *two* oxygen atoms and have only two more carbons '
                 'attached as neighbours (forming rings).\n'
                 '2.  **Improved Ring Logic:** Instead of looping through each '
                 'ring combination we can directly check the smallest ring '
                 'containing a given atom. That way, we can verify if a ketal '
                 'is a true spiroketal by checking if the *smallest* rings '
                 'containing the oxygen atoms connected to the ketal carbon '
                 'share any atoms *other than the ketal carbon itself*.\n'
                 '3.  **Robustness:** Add explicit check for presence of at '
                 'least two rings. This should improve the detection of "true" '
                 'spiroketals.\n'
                 '4.  **Clarity:** Improve comments to clearly explain each '
                 'step, especially the logic for the ring analysis.\n'
                 '\n'
                 '**Implementation:**',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 90,
    'num_false_positives': 470,
    'num_true_negatives': 141729,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.16071428571428573,
    'recall': 0.8910891089108911,
    'f1': 0.2723146747352496,
    'accuracy': 0.996619817287421,
    'negative_predictive_value': 0.9999223931141527}