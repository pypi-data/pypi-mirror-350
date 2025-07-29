"""
Classifies: CHEBI:33563 glycolipid
"""
"""
Classifies: glycolipid
Definition: Any member of the class of 1,2-di-O-acylglycerols joined at oxygen 3 by a glycosidic linkage
to a carbohydrate part (usually a mono-, di- or tri-saccharide). Some bacterial glycolipids have the sugar part acylated,
and the glycerol component may be absent.
This program uses several heuristic tests:
  1. It looks for a sugar moiety by scanning for a nonaromatic ring of size 5 or 6 that contains exactly one oxygen atom.
  2. It looks for a glycosidic (ether) linkage connecting a non‐ring carbon to a ring carbon.
  3. It looks for an acyl linkage (ester or amide) that could attach a fatty acid.
  4. It checks for the presence of a long aliphatic chain (heuristically, 8 or more consecutive carbon atoms).
  5. It checks that the molecular weight is above 500 Da and that there are a minimum number of rotatable bonds.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def has_sugar(mol):
    """
    Looks for a candidate sugar ring.
    We define a sugar ring as a nonaromatic ring of size 5 or 6 having exactly one oxygen atom in the ring.
    (Many carbohydrate rings are pyranoses/furanoses with one ring oxygen.)
    """
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) not in [5, 6]:
            continue
        # Skip rings that are aromatic (sugars are not aromatic)
        if any(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            continue
        # Count oxygen atoms in the ring 
        oxy_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8)
        if oxy_count == 1:
            return True
    return False

def has_long_aliphatic_chain(smiles):
    """
    Heuristic: check if the SMILES string contains 8 or more consecutive 'C' characters.
    To avoid being misled by bond characters, we remove backslash and forward slash.
    """
    clean_smiles = smiles.replace("\\", "").replace("/", "")
    return "CCCCCCCC" in clean_smiles

def is_glycolipid(smiles: str):
    """
    Determines if a molecule is a glycolipid based on its SMILES string.
    The algorithm uses the following heuristic tests:
      1. Identify a sugar moiety via a nonaromatic five-/six-membered ring with exactly one oxygen.
      2. Confirm a glycosidic linkage exists by finding an ether-bond [C!R]-O-[C R] (a non-ring to ring connection).
      3. Identify at least one acyl linkage (ester or amide) that can anchor a fatty acyl chain.
      4. Verify that there is a long aliphatic chain (at least 8 consecutive carbon characters).
      5. Ensure that molecular weight (>500 Da) and the number of rotatable bonds (>= 3) are in an acceptable range.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        (bool, str): A tuple where the first element indicates if the molecule is classified as a glycolipid,
                     and the second element gives the reason for the classification or failure.
    """
    # Parse the SMILES into a molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Test 1: Check for a sugar ring moiety
    if not has_sugar(mol):
        return False, "No carbohydrate (sugar ring) moiety found"
    
    # Test 2: Check for a glycosidic (ether) linkage connecting a non-ring carbon to a ring carbon.
    # This SMARTS pattern looks for a bond O linking a non-ring carbon ([C;!R]) and a ring carbon ([C;R]).
    glyco_pattern = Chem.MolFromSmarts("[C;!R]-O-[C;R]")
    if glyco_pattern is None or not mol.HasSubstructMatch(glyco_pattern):
        return False, "No glycosidic linkage (ether bond between a non‐ring and a ring atom) found"
    
    # Test 3: Check for acyl linkages.
    # Ester linkage: [OX2][CX3](=O)[#6]
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=O)[#6]")
    if ester_pattern is None:
        return False, "Error in ester SMARTS pattern"
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    # Amide linkage: NC(=O)[#6]
    amide_pattern = Chem.MolFromSmarts("NC(=O)[#6]")
    if amide_pattern is None:
        return False, "Error in amide SMARTS pattern"
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    
    if (len(ester_matches) + len(amide_matches)) < 1:
        return False, "No acyl linkage (ester or amide) found that could anchor a fatty acid chain"
    
    # Test 4: Check for the presence of a long fatty acyl chain
    if not has_long_aliphatic_chain(smiles):
        return False, "No long aliphatic (fatty acid) chain detected (need at least 8 consecutive carbons)"
    
    # Test 5: Check molecular weight (typically >500 Da for glycolipids)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 500:
        return False, f"Molecular weight too low ({mol_wt:.1f} Da) for a glycolipid"
    
    # Test 6: Check that there are enough rotatable bonds (>=3)
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 3:
        return False, "Not enough rotatable bonds to support the presence of long fatty acyl chains"
    
    return True, "Molecule contains a sugar ring linked via a glycosidic bond to an acylated lipid chain consistent with a glycolipid structure"

# For testing purposes, you may uncomment the following:
# if __name__ == "__main__":
#     test_smiles = "OC[C@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2OCCCCCCCC\\C=C/CCCCCCCC(O)=O"
#     result, reason = is_glycolipid(test_smiles)
#     print("Is glycolipid?", result)
#     print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33563',
                          'name': 'glycolipid',
                          'definition': 'Any member of class of '
                                        '1,2-di-O-acylglycerols joined at '
                                        'oxygen 3 by a glycosidic linkage to a '
                                        'carbohydrate part (usually a mono-, '
                                        'di- or tri-saccharide). Some '
                                        'substances classified as bacterial '
                                        'glycolipids have the sugar part '
                                        'acylated by one or more fatty acids '
                                        'and the glycerol part may be absent.',
                          'parents': ['CHEBI:35740'],
                          'xrefs': ['KEGG:C05005', 'Wikipedia:Glycolipids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 74,
                           'log_lines_of_code': 4.30406509320417,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
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
                                                 2,
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
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcNumRotatableBonds',
                                                 'CalcExactMolWt',
                                                 'replace',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'HasSubstructMatch',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetRingInfo',
                                                 'GetIsAromatic'],
                           'methods_called_count': 12,
                           'smarts_strings': [   '[OX2][CX3](=O)[#6]',
                                                 '[C;!R]-O-[C;R]',
                                                 'NC(=O)[#6]'],
                           'smarts_strings_count': 3,
                           'defs': ['has_sugar(mol):'],
                           'defs_count': 1,
                           'returns': [   'True',
                                          'False',
                                          '"CCCCCCCC" in clean_smiles',
                                          'False, "Invalid SMILES string"',
                                          'False, "No carbohydrate (sugar '
                                          'ring) moiety found"',
                                          'False, "No glycosidic linkage '
                                          '(ether bond between a non‐ring and '
                                          'a ring atom) found"',
                                          'False, "Error in ester SMARTS '
                                          'pattern"',
                                          'False, "Error in amide SMARTS '
                                          'pattern"',
                                          'False, "No acyl linkage (ester or '
                                          'amide) found that could anchor a '
                                          'fatty acid chain"',
                                          'False, "No long aliphatic (fatty '
                                          'acid) chain detected (need at least '
                                          '8 consecutive carbons)"',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} Da) for a glycolipid"',
                                          'False, "Not enough rotatable bonds '
                                          'to support the presence of long '
                                          'fatty acyl chains"',
                                          'True, "Molecule contains a sugar '
                                          'ring linked via a glycosidic bond '
                                          'to an acylated lipid chain '
                                          'consistent with a glycolipid '
                                          'structure"'],
                           'returns_count': 13,
                           'complexity': 6.660813018640835},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OCCCc1ccc2oc(cc2c1)-c1ccc2OCOc2c1 '
               'NAME: 7-demethoxyegonol oleate REASON: WRONGLY CLASSIFIED '
               'Molecule contains a sugar moiety, acyl linkage(s), and a long '
               'fatty acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O.CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)OC1O[C@@H](C)[C@@H](O)[C@@H](O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O[C@@H]2O[C@@H]3CO[C@@](C)(O[C@H]3[C@H](OC)[C@H]2O)C(O)=O)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)COC1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1O '
               'NAME: GPL-21 REASON: WRONGLY CLASSIFIED Molecule contains a '
               'sugar moiety, acyl linkage(s), and a long fatty acid chain '
               'consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O=C(N[C@H]([C@H]1OC(C)(C)O[C@@H]1CCCCCCCCCCC)CO)CCCCCCCCCCCCCCCCC '
               'NAME: '
               'N-(1-(2,2-dimethyl-5-undecyl-1,3-dioxolan-4-yl)-2-hydroxyethyl)stearamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a sugar moiety, '
               'acyl linkage(s), and a long fatty acid chain consistent with a '
               'glycolipid structure\n'
               ' * SMILES: '
               'O=C1O[C@]2([C@H](OC)[C@H](O[C@H]([C@H]2O)OC[C@]34[C@@]5(C(C(C)C)=C[C@H]3C[C@]5(C(=O)O)[C@@H]6CC[C@H]([C@H]6C4)C)C(=O)O)C)O[C@H]1CCCCCCCC(=O)OC '
               'NAME: Moriniafungin G REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O=C1O[C@]2([C@H](OC)[C@H](O[C@H]([C@H]2O)OC[C@]34[C@@]5(C(C(C)C)=C[C@H]3C[C@]5(C=O)[C@@H]6CC[C@H]([C@H]6C4)C)C(=O)O)C)O[C@H]1CCCCCCCC(=O)O '
               'NAME: Moriniafungin REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OCCCc1ccc2oc(cc2c1)-c1ccc2OCOc2c1 '
               'NAME: 7-demethoxyegonol-9(Z),12(Z)linoleate REASON: WRONGLY '
               'CLASSIFIED Molecule contains a sugar moiety, acyl linkage(s), '
               'and a long fatty acid chain consistent with a glycolipid '
               'structure\n'
               ' * SMILES: '
               '[H][C@@]12O[C@]1(CO)[C@@H](O)[C@]1(O)C(=O)C(C)=C[C@@]1([H])[C@]13O[C@]4(O[C@H]([C@]21[H])[C@@](O4)([C@H](OC(C)=O)[C@H]3C)C(C)=C)\\C=C\\C=C\\CCCCCCCCC '
               'NAME: 12beta-acetoxyhuratoxin REASON: WRONGLY CLASSIFIED '
               'Molecule contains a sugar moiety, acyl linkage(s), and a long '
               'fatty acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O=C(NCCCO)/C=C/NC(=O)C(O)CC[C@@H](O)/C=C(/C(O)[C@@H](O)C[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)[C@@H](O)[C@H](O)[C@@H](O)CC(O)CCCCCCCC2OC3(CC(CC2(O3)C)C)CCCCCCC[C@H](O)C(O)[C@H]4O[C@](O)(C(O)C(C4)O)C[C@H](O)[C@H](/C=C/[C@@H](O)CC[C@@H](O)[C@@H](O)[C@H]5OC([C@@H](O)[C@@H](C5)O)C[C@@H](O)[C@H](O)C[C@H]6O[C@H]([C@H](O)[C@H]([C@@H]6O)O)C[C@H](O)\\C=C/C=C/CC(O)[C@H](O)[C@H](O)C/C=C\\C(=C)CC[C@H](O)[C@@H](O)C(O)[C@@H](C[C@H]7O[C@H](/C=C\\[C@@H](O)[C@H](O)CC8OC9C(CC[C@H]%10O[C@H](CN)C[C@H]%10O)OC(C8)C9)[C@@H](O)[C@@H]([C@H]7O)O)C)C)\\C '
               'NAME: Ostreocin D REASON: WRONGLY CLASSIFIED Molecule contains '
               'a sugar moiety, acyl linkage(s), and a long fatty acid chain '
               'consistent with a glycolipid structure\n'
               ' * SMILES: '
               '[H][C@@]12O[C@]1(CO)[C@@H](O)[C@]1(O)C(=O)C(C)=C[C@@]1([H])[C@]13O[C@@]4(CCCCCCCCC)O[C@H]([C@]21[H])[C@@](O4)([C@H](OC(C)=O)[C@H]3C)C(C)=C '
               'NAME: Gnidiglaucin REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)OC1O[C@@H](C)[C@@H](O)[C@@H](O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O[C@@H]2O[C@@H]3CO[C@@](C)(O[C@H]3[C@H](OC)[C@H]2O)C(O)=O)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)COC1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1O '
               'NAME: GPL-8 REASON: WRONGLY CLASSIFIED Molecule contains a '
               'sugar moiety, acyl linkage(s), and a long fatty acid chain '
               'consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O[C@H]([C@@H](O)C(O)=O)C(O)=O.CCCCCCCC(=O)N[C@H](CN1CCCC1)[C@H](O)c1ccc2OCCOc2c1.CCCCCCCC(=O)N[C@H](CN1CCCC1)[C@H](O)c1ccc2OCCOc2c1 '
               'NAME: eliglustat tartrate REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'OC12C3(C(CC4C(C4(C)C)C(C3=O)C=C5C1OC(OC5)(C)C)C)C=C(C2OC(=O)CCCCCCCCCCCCCCC)C '
               'NAME: '
               '(5-hydroxy-3,8,8,15,15,18-hexamethyl-19-oxo-7,9-dioxapentacyclo[11.5.1.01,5.06,11.014,16]nonadeca-2,11-dien-4-yl) '
               'hexadecanoate REASON: WRONGLY CLASSIFIED Molecule contains a '
               'sugar moiety, acyl linkage(s), and a long fatty acid chain '
               'consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O=C(O)[C@@]1(O)[C@@]2(O[C@@](CCCC(OC(=O)C)C(C/C=C/C3=CC=CC=C3)C)(O[C@H]1C(=O)O)[C@H]([C@@H]2OC(=O)CCCCCCCCC4=CC=CC=C4)O)C(=O)O '
               'NAME: F-10863C REASON: WRONGLY CLASSIFIED Molecule contains a '
               'sugar moiety, acyl linkage(s), and a long fatty acid chain '
               'consistent with a glycolipid structure\n'
               ' * SMILES: '
               'C[C@@H]1[C@H](OC(=O)c2ccccc2)[C@]2(O)[C@H]3[C@H]1[C@H](C)CCCCCCCC14O[C@@H]5[C@H]([C@@H]6O[C@]6(CO)[C@H]2O)[C@]3(O1)[C@H](C)C[C@@]5(O4)C(C)=C '
               'NAME: Pimelea factor P2 REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O=C1O[C@]2([C@H](OC)[C@H](O[C@H]([C@H]2O)OC[C@]34[C@@]5(C(C(C)C)=C[C@H]3C[C@]5(C=O)[C@@H]6CC[C@H]([C@H]6C4)C)C(=O)O)C)O[C@H]1CCCCCCCC(=O)OC '
               'NAME: Moriniafungin E REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'O=C1O[C@]2([C@H](OC)[C@H](O[C@H]([C@H]2O)OC[C@]34[C@@]5(C(C(C)C)=C[C@H]3C[C@]5(C(=O)O)[C@@H]6CC[C@H]([C@H]6C4)C)C(=O)O)C)O[C@H]1CCCCCCCC(=O)O '
               'NAME: Moriniafungin F REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               '[H][C@]12OC3(OC4(C(C)C(OC(=O)\\C=C\\c5ccccc5)[C@@]1(O3)C(C)=C)C1C=C(C)CC1(O)C(O)C1(CO)OC1C24)\\C=C\\CCCCCCC '
               'NAME: gnidilatimonoein REASON: WRONGLY CLASSIFIED Molecule '
               'contains a sugar moiety, acyl linkage(s), and a long fatty '
               'acid chain consistent with a glycolipid structure\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OCCCc1cc(OC)c2oc(cc2c1)-c1ccc2OCOc2c1 '
               'NAME: egonol-9(Z),12(Z)linoleate REASON: WRONGLY CLASSIFIED '
               'Molecule contains a sugar moiety, acyl linkage(s), and a long '
               'fatty acid chain consistent with a glycolipid structure\n'
               'False negatives: SMILES: '
               'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2OCCCCCCCC\\C=C/CCCCCCCC(O)=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: (9Z)-18-hydroxyoctadec-9-enoic acid 18-O-sophoroside '
               'REASON: MISSED No carbohydrate (sugar ring) moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: beta-D-glucosyl-N-eicosanoylsphingosine REASON: MISSED '
               'No carbohydrate (sugar ring) moiety found\n'
               ' * SMILES: '
               'O=C(OC(CC(=O)O)CCCCCCC)CC(O[C@@H]1O[C@H]([C@H](O)[C@H]([C@H]1O)O)C)C/C=C/CCCCCC '
               'NAME: '
               '3-[(E)-3-[(2R,3R,4R,5R,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxydodec-5-enoyl]oxydecanoic '
               'acid REASON: MISSED No carbohydrate (sugar ring) moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               'alpha-D-galactosyl-(1->4)-beta-D-galactosyl-(1->4)-beta-D-glucosyl-N-hexacosanoylceramide '
               'REASON: MISSED No carbohydrate (sugar ring) moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CCCCCCCCCC)CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O[C@@H]2O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]2O)[C@H]1NC(C)=O '
               'NAME: Le(x)-C12L REASON: MISSED No carbohydrate (sugar ring) '
               'moiety found\n'
               ' * SMILES: '
               '[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O '
               'NAME: ganglioside GM2 (24:0) REASON: MISSED No carbohydrate '
               '(sugar ring) moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC '
               'NAME: Man-1-6-Ins-1-P-Cer(t20:0/2,3-OH-24:0) REASON: MISSED No '
               'carbohydrate (sugar ring) moiety found\n'
               ' * SMILES: '
               'C(O[C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)CO)[C@@H]([C@@H](/C=C/CC/C=C(/CCCCCCCCC)\\C)O)NC(=O)C(CCCCCCCCCCCCCCCC)O '
               'NAME: cerebroside D REASON: MISSED No carbohydrate (sugar '
               'ring) moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxydocosanoyl)-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine '
               'REASON: MISSED No carbohydrate (sugar ring) moiety found\n'
               ' * SMILES: '
               '[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C(O)=O '
               'NAME: '
               "alpha-Neu5Ac-(2->3)-beta-D-Gal(1->3)beta-GalNAc-(1->4)-[alpha-Neu5Ac-(2->3)]-beta-Gal-(1->4)-beta-Glc-(1->1')-Cer(d18:1/18:0) "
               'REASON: MISSED No carbohydrate (sugar ring) moiety found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No glycosidic linkage (ether '
                                               'bond between a non‐ring and a '
                                               'ring atom) found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No acyl linkage (ester or '
                                               'amide) found that could anchor '
                                               'a fatty acid chain'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No glycosidic linkage (ether '
                                               'bond between a non‐ring and a '
                                               'ring atom) found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No carbohydrate (sugar ring) '
                                               'moiety found'}],
    'sample_false_negatives': [   {   'smiles': 'O=C(OC(CC(=O)O)CCCCCCC)CC(O[C@@H]1O[C@H]([C@H](O)[C@H]([C@H]1O)O)C)C/C=C/CCCCCC',
                                      'name': '3-[(E)-3-[(2R,3R,4R,5R,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxydodec-5-enoyl]oxydecanoic '
                                              'acid',
                                      'reason': 'No long aliphatic (fatty '
                                                'acid) chain detected (need at '
                                                'least 8 consecutive carbons)'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC',
                                      'name': 'Man-1-6-Ins-1-P-Cer(t20:0/2,3-OH-24:0)',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP(O)(=O)O[C@@H]1OC[C@H](N)[C@H](O)[C@H]1O',
                                      'name': '4-amino-4-deoxy-alpha-L-arabinopyranosyl '
                                              'ditrans,polycis-undecaprenyl '
                                              'phosphate',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'O=C(O)C[C@H](O[C@@H]1O[C@H]([C@H](O)[C@H]([C@H]1O)O)C)CCCCCCCCCCCCC[C@H](O)C',
                                      'name': 'Dokdolipid A',
                                      'reason': 'Molecular weight too low '
                                                '(462.3 Da) for a glycolipid'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCC',
                                      'name': 'Man-1-6-Ins-1-P-Cer(t18:0/2-OH-26:0)',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC',
                                      'name': 'Ins-1-P-6-Man-beta1-6-Ins-1-P-Cer(d18:0/24:0)',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'CC(=O)N[C@H]1[C@H](O[C@H](CO)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)O[C@H]1[C@@H](O)[C@@H](CO)O[C@H](OP(O)(=O)OP(O)(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)[C@@H]1NC(C)=O',
                                      'name': 'beta-D-Gal-(1->3)-alpha-D-GalNAc-(1->3)-alpha-D-GalNAc-diphospho-ditrans,octacis-undecaprenol',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC(C(O)CCCCCCC\\C=C\\CCCCCC)C(=O)OC[C@H]1O[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': "alpha,alpha'-trehalose "
                                              '6-mycolate',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'O(P(OP(O[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1NC(=O)C)O)O[C@@H]2O[C@@H]([C@H]([C@@H]([C@H]2O)O)O)CO)CO)(O)=O)(O)=O)C/C=C(/C)\\CC/C=C(/C)\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)/C)/C)/C)/C)/C',
                                      'name': 'beta-D-glucosyl-(1->4)-N-acetyl-alpha-D-glucosaminyl '
                                              'undecaprenyl diphosphate',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCCCC',
                                      'name': 'Man-1-6-Ins-1-P-Cer(d20:0/2-OH-24:0)',
                                      'reason': 'No glycosidic linkage (ether '
                                                'bond between a non‐ring and a '
                                                'ring atom) found'}],
    'attempt': 2,
    'reasoning': 'Below is our revised, single‐file Python solution. In our '
                 'reasoning we noted that the previous version’s sugar '
                 'detection was too strict (requiring at least two oxygen '
                 'atoms in a five‐ or six‐membered ring) so that many sugar '
                 'rings (which in fact contain one ring oxygen—e.g. a typical '
                 'pyranose) were being rejected. We also recognized that '
                 'linking the sugar to the lipid part is key. Therefore, we '
                 'now (1) relax the sugar test by requiring that a nonaromatic '
                 'five‐ or six‐membered ring contain exactly one oxygen and '
                 '(2) add a test for a glycosidic (ether) bond linking a ring '
                 'carbon (i.e. in the sugar) to a non‐ring carbon, thereby '
                 'ensuring connectivity between a carbohydrate and a lipid '
                 'moiety. We keep a test for acyl linkages (ester or amide), '
                 'the presence of a long fatty chain (by searching for 8 '
                 'consecutive “C” characters in a “cleaned” SMILES string), '
                 'and additional sanity checks (molecular weight >500\u2009Da, '
                 'sufficient rotatable bonds). We hope that these revisions '
                 'will limit both false positives and negatives.\n'
                 '\n'
                 'Below is the complete code in one Python block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 443,
    'num_false_positives': 571,
    'num_true_negatives': 141139,
    'num_false_negatives': 147,
    'num_negatives': None,
    'precision': 0.4368836291913215,
    'recall': 0.7508474576271187,
    'f1': 0.5523690773067331,
    'accuracy': 0.9949543218552355,
    'negative_predictive_value': 0.9989595572101978}