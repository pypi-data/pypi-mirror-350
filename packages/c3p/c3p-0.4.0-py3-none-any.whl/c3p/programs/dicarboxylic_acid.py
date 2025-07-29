"""
Classifies: CHEBI:35692 dicarboxylic acid
"""
"""
Classifies: CHEBI:35692 dicarboxylic acid
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_dicarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a dicarboxylic acid based on its SMILES string.
    A dicarboxylic acid is any carboxylic acid containing two free carboxy groups (-COOH or -COO^-),
    not involved in ester or amide bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dicarboxylic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define carboxyl group pattern (both protonated and deprotonated forms)
    carboxyl_group_pattern = Chem.MolFromSmarts("[CX3](=O)[O;H1,-1]")
    if carboxyl_group_pattern is None:
        return False, "Failed to create carboxyl group pattern"

    # Find all carboxyl groups in the molecule
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_group_pattern)
    num_carboxyl_groups = 0

    for match in carboxyl_matches:
        carboxyl_carbon_idx = match[0]
        hydroxyl_oxygen_idx = match[1]

        carboxyl_carbon = mol.GetAtomWithIdx(carboxyl_carbon_idx)
        hydroxyl_oxygen = mol.GetAtomWithIdx(hydroxyl_oxygen_idx)

        # Check if hydroxyl oxygen is connected only to carboxyl carbon and possibly hydrogen (not ester)
        oxygen_neighbors = [a.GetAtomicNum() for a in hydroxyl_oxygen.GetNeighbors() if a.GetIdx() != carboxyl_carbon_idx]
        if any(atomic_num > 1 for atomic_num in oxygen_neighbors):
            continue  # It's part of an ester

        # Check if carboxyl carbon is not single-bonded to nitrogen (not amide)
        carbon_neighbors = [a for a in carboxyl_carbon.GetNeighbors() if a.GetIdx() != hydroxyl_oxygen_idx]
        for neighbor in carbon_neighbors:
            if neighbor.GetAtomicNum() == 7:  # Nitrogen atom
                bond = mol.GetBondBetweenAtoms(carboxyl_carbon_idx, neighbor.GetIdx())
                if bond.GetBondType() == Chem.BondType.SINGLE:
                    break  # It's part of an amide
        else:
            # Increment count if not part of ester or amide
            num_carboxyl_groups += 1

    # Exclude peptides by checking for peptide bonds (amide bonds between carbonyl carbon and nitrogen)
    peptide_bond_pattern = Chem.MolFromSmarts("C(=O)N")
    if mol.HasSubstructMatch(peptide_bond_pattern):
        return False, "Molecule contains peptide bonds"

    # Exclude large molecules (e.g., molecular weight > 500 Da)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 500:
        return False, f"Molecular weight is too high ({mol_wt:.2f} Da)"

    # Check if there are exactly two carboxyl groups
    if num_carboxyl_groups == 2:
        return True, "Molecule contains exactly two free carboxyl groups"
    else:
        return False, f"Found {num_carboxyl_groups} free carboxyl group(s), expected exactly 2"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35692',
                          'name': 'dicarboxylic acid',
                          'definition': 'Any carboxylic acid containing two '
                                        'carboxy groups.',
                          'parents': ['CHEBI:131927', 'CHEBI:33575'],
                          'xrefs': ['KEGG:C02028'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 37,
                           'log_lines_of_code': 3.6109179126442243,
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
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 0,
                                                 0,
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
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetSubstructMatches',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 5,
                           'smarts_strings': ['[CX3](=O)[O;H1,-1]', 'C(=O)N'],
                           'smarts_strings_count': 2,
                           'defs': ['is_dicarboxylic_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Failed to create carboxyl '
                                          'group pattern"',
                                          'False, "Molecule contains peptide '
                                          'bonds"',
                                          'False, f"Molecular weight is too '
                                          'high ({mol_wt:.2f} Da)"',
                                          'True, "Molecule contains exactly '
                                          'two free carboxyl groups"',
                                          'False, f"Found '
                                          '{num_carboxyl_groups} free carboxyl '
                                          'group(s), expected exactly 2"'],
                           'returns_count': 6,
                           'complexity': 3.5221835825288452},
    'message': '\n'
               'Attempt failed: F1 score of 0.1796818510484454 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: OC(=O)C#CC(O)=O NAME: butynedioic acid '
               'REASON: CORRECT Molecule contains exactly two free carboxyl '
               'groups\n'
               ' * SMILES: [C@H](C(=O)O)(CCC[C@H](C(=O)O)N)N NAME: '
               'DD-2,6-diaminopimelic acid REASON: CORRECT Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'CC(O)c1c(C)c2cc3[nH]c(cc4nc(cc5[nH]c(cc1n2)c(C)c5CCC(O)=O)c(CCC(O)=O)c4C)c(C)c3C(C)O '
               'NAME: hematoporphyrin REASON: CORRECT Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: CC(C[C@H](N)C(O)=O)C(O)=O NAME: 4-methyl-L-glutamic '
               'acid REASON: CORRECT Molecule contains exactly two free '
               'carboxyl groups\n'
               ' * SMILES: N[C@]1(CN[C@H](C1)C(O)=O)C(O)=O NAME: '
               '(2R,4R)-4-aminopyrrolidine-2,4-dicarboxylic acid REASON: '
               'CORRECT Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: O[C@@H]1C=CC=C([C@@H]1C(O)=O)C(=O)CCC(O)=O NAME: '
               '(1S,6R)-2-succinyl-6-hydroxycyclohexa-2,4-diene-1-carboxylic '
               'acid REASON: CORRECT Molecule contains exactly two free '
               'carboxyl groups\n'
               ' * SMILES: OC(=O)CN(CC(O)=O)CP(O)(O)=O NAME: '
               'N-(phosphonomethyl)iminodiacetic acid REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: OC1C=CC2(CC1OC(C2)C(O)=O)C(O)=O NAME: '
               '8-hydroxy-2-oxabicyclo[3.3.1]non-6-ene-3,5-dicarboxylic acid '
               'REASON: CORRECT Molecule contains exactly two free carboxyl '
               'groups\n'
               ' * SMILES: OC(=O)CC(=O)\\C=C\\C(O)=O NAME: fumarylacetic acid '
               'REASON: CORRECT Molecule contains exactly two free carboxyl '
               'groups\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@H]3C[C@]1(CC3=C)[C@@H](C(O)=O)[C@]1([H])[C@@](C)(CCC[C@@]21CO)C(O)=O '
               'NAME: gibberellin A15 (diacid form) REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'C(/C=C\\CCCCC)[C@H](C/C=C/C=C/[C@H]([C@@H](O)CCCC(=O)O)SC[C@H](N)C(=O)O)O '
               'NAME: (12R)-hydroxy-10,11-dihydroleukotriene E4 REASON: '
               'CORRECT Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: O=C(O)C1(CCCCC1)CC(=O)O NAME: '
               '1-(carboxymethyl)cyclohexane-1-carboxylic acid REASON: CORRECT '
               'Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'OC(=O)[C@@H](CC1=CC(O)=C(O)C=C1)OC(=O)\\C=C\\C1=C2[C@@H]([C@H](OC2=C(O)C=C1)C1=CC(O)=C(O)C=C1)C(=O)O[C@H](CC1=CC(O)=C(O)C=C1)C(O)=O '
               'NAME: salvianolic acid B REASON: CORRECT Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: C(=C\\C=C(\\C(O)=O)/O)\\CC(O)=O NAME: '
               '(2Z,4Z)-2-hydroxyhepta-2,4-dienedioic acid REASON: CORRECT '
               'Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: OC(=O)CCC(=O)\\C=C\\C=C(/O)C(O)=O NAME: '
               '(2Z,4E)-2-hydroxy-6-oxonona-2,4-dienedioic acid REASON: '
               'CORRECT Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: OC(C[C@@H](C(=O)O)CCCCC)=O NAME: Nonate REASON: '
               'CORRECT Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: OC(=O)C(=O)C(O)=O NAME: oxomalonic acid REASON: '
               'CORRECT Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'CCN1CCCc2cc3c(Oc4cc5=[N+](CC)CCCc5cc4=C3c3ccc(cc3C(O)=O)C(O)=O)cc12 '
               'NAME: ATTO 565 meta-isomer(1+) REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'CC(C)C(=C)CC[C@H]([C@H]1CC[C@@]2(C)C3=CC[C@@H](C(C)=C)[C@](C)(CCC(O)=O)C3=CC[C@]12C)C(O)=O '
               'NAME: poricoic acid C REASON: CORRECT Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: C(C[C@@H](CC(C(O)=O)=O)O)C(O)=O NAME: '
               '(S)-4-hydroxy-2-oxoheptanedioic acid REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: OC(=O)c1ccc2cc(ccc2c1)C(O)=O NAME: '
               'naphthalene-2,6-dicarboxylic acid REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: O[C@H]([C@H](OC(=O)\\C=C\\c1ccc(O)cc1)C(O)=O)C(O)=O '
               'NAME: (2R,3S)-trans-coutaric acid REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: N[C@@H]([C@H](O)CC(O)=O)C(O)=O NAME: '
               '(R)-3-hydroxy-L-glutamic acid REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: C\\C(=C/C(O)=O)C(O)=O NAME: mesaconic acid REASON: '
               'CORRECT Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: OC(=O)C1CCCC(=N1)C(O)=O NAME: '
               '2,3,4,5-tetrahydrodipicolinic acid REASON: CORRECT Molecule '
               'contains exactly two free carboxyl groups\n'
               'False positives: SMILES: '
               'O=C(N[C@@H](CCC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)C '
               'NAME: Asn-Ala-Glu REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC(O)=O '
               'NAME: Gln-Asp-Gln REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](C)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)C)CC=3C=C[C@H](O)CC3)C '
               'NAME: MC-(H2)YA REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)C '
               'NAME: Asp-Ala-Phe REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O1C(C(NC(=O)C(NC(=O)C(NC)C(O)C2=CC1=C(O)C=C2)C(C)=C)C(=O)N3C(C=CC3)C(=O)N/C(=C(/CC)\\C)/C(=O)N/C(=C/C(O)=O)/C(O)=O)(CC)C '
               'NAME: Phomopsin B REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)COP(O)(OC[C@H]2O[C@@H]([C@@H]([C@H]([C@@H]2O)O[C@@H]3[C@@H]([C@H]([C@@H]([C@H](O3)COP(O)(OC[C@H]4O[C@@H]([C@@H]([C@H]([C@@H]4O)O[C@@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O)NC(C)=O)NC(C)=O)O[C@@H](C(O)=O)CO)=O)O)O)NC(C)=O)NC(C)=O)O[C@@H](C(O)=O)CO)=O)O)O)O)OC[C@H]6O[C@H]([C@@H]([C@H]([C@@H]6O)O)O)OC[C@H]7O[C@H]([C@@H]([C@H]([C@@H]7O)O)O)OC[C@@H](COC(CCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCC)=O '
               'NAME: '
               '3-{beta-D-GlcNAc-(1->3)-[D-GrO-(2->1)]-beta-D-GlcNAc-(6-P-6)-beta-D-GlcNAc-(1->3)-[D-GrO-(2->1)]-beta-D-GlcNAc-(6-P-6)-beta-D-Glc-(1->6)-beta-D-Glc-(1->6)-beta-D-Glc-yl}-1,2-dimyristoyl-sn-glycerol '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two free '
               'carboxyl groups\n'
               ' * SMILES: '
               'S1C(=NC(=C1)C(=O)N[C@H](C(=O)OC(C2N(C(=O)[C@@H](N)C(CC)C)CCC2OC(=O)CC)CC(=O)O)CCC(=O)N)[C@H]3N(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)/C(/NC(=O)N[C@H](C(=O)O)CC4=CC=C(O)C=C4)=C/C)C)CCCN=C(N)N)CCC3 '
               'NAME: Pseudovibriamide B2 REASON: WRONGLY CLASSIFIED Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCC(O)=O)C(=O)NCC(O)=O)[C@@H](N)CCCN=C(N)N NAME: '
               'Arg-Glu-Gly REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H]([C@H](O)C)C(O)=O)[C@H]1N(CCC1)C(=O)[C@@H](N)CC(O)=O '
               'NAME: Asp-Pro-Thr REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: N[C@@H](CCC(O)=O)C(=O)N1CCC[C@H]1C(O)=O NAME: '
               'Glu-Pro REASON: WRONGLY CLASSIFIED Molecule contains exactly '
               'two free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(=O)N '
               'NAME: Phe-Asn-Asp REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: O1C=2C(C(C(C(O)=O)C(O)=O)C=3C1=CC=CC3)=CC=CC2 NAME: '
               '2-(9h-xanthen-9-yl)-malonic acid REASON: WRONGLY CLASSIFIED '
               'Molecule contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@@H](CC(C)C)C(N[C@H](C(N[C@@H](C(N[C@H](C(N[C@@H]1CC(C)C)=O)CC(C)C)=O)CC(=O)O)=O)C)=O)C(C)C)CCC(=O)O)CCCCCCCCCCC(CC)C '
               'NAME: Gageopeptin B REASON: WRONGLY CLASSIFIED Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: O=C1O[C@](C(=O)O)([C@@H](C(=O)O)CCCCCCCCCC=C)CC1 '
               'NAME: Spiculisporic acid F REASON: WRONGLY CLASSIFIED Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)CN)CCCCN '
               'NAME: Gly-Lys-Asp REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: OC(=O)C(NC(C)C(O)=O)CCCCN NAME: L-Lysopine REASON: '
               'WRONGLY CLASSIFIED Molecule contains exactly two free carboxyl '
               'groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=2NC=NC2)CC(O)=O '
               'NAME: His-Asp-His REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O[C@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H](O)[C@@H]9O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO)CO '
               'NAME: CID 146017632 REASON: WRONGLY CLASSIFIED Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: O=C(O)[C@H]([C@@H](C(=O)O)C)CCCCCCCC NAME: Sphaeric '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'free carboxyl groups\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@@H](O)[C@H](OC(O)[C@@H]2NC(=O)C)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)O[C@@H]([C@H]1O)CO)[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4R,5R)-5-acetamido-4-[(2R,3R,4S,5R,6R)-4-[(2S,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,6-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'free carboxyl groups\n'
               ' * SMILES: '
               'O1[C@H]([C@@H]([C@H](C=C1C(=O)O)O)OS(O)(=O)=O)O[C@H]2[C@@H]([C@H]([C@H](O[C@@H]2COS(O)(=O)=O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3C(=O)O)O[C@H]4[C@@H]([C@H]([C@H](O[C@@H]4COS(O)(=O)=O)O)NS(O)(=O)=O)O)O)O)NS(O)(=O)=O)O '
               'NAME: HP_dp04_0003 REASON: WRONGLY CLASSIFIED Molecule '
               'contains exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O1C(O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@@H]([C@@H](O)[C@H](O)COC3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)(C[C@H](O)[C@@H](NC(=O)C)[C@@H]1[C@H](O)[C@H](O)CO)C(O)=O '
               'NAME: '
               '(4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4S,5S,6R)-4-[(4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC=1C=2C(NC1)=CC=CC2 '
               'NAME: Glu-Trp-Leu REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@@H]%10NC(=O)C)CO)CO '
               'NAME: '
               '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3S,4S,5S,6S)-6-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-6-[[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,4-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'free carboxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(O)=O)C(=O)N[C@@H](CC(=O)N)C(O)=O)[C@H]1NCCC1 '
               'NAME: Pro-Asp-Asn REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two free carboxyl groups\n'
               'False negatives: SMILES: '
               'O=C1N[C@H](C(=O)N[C@H]1CCCNC(=O)C=C(CCOC(=O)C)C)CCCNC(=O)C=C(CCOC(=O)C)C '
               'NAME: Trichocyclodipeptide A REASON: MISSED Found 0 free '
               'carboxyl group(s), expected exactly 2\n'
               ' * SMILES: O(CCCCCCC)C(=O)C(OCCC)=O NAME: Oxalic acid, heptyl '
               'propyl ester REASON: MISSED Found 0 free carboxyl group(s), '
               'expected exactly 2\n'
               ' * SMILES: '
               'O=C(O[C@H](C[C@H]1O[C@@H]([C@H](C(=O)O)C)CC1)CC)[C@H]([C@H]2O[C@@H](C[C@H](O)CC)CC2)C '
               'NAME: Homononactyl homononactate REASON: MISSED Found 1 free '
               'carboxyl group(s), expected exactly 2\n'
               ' * SMILES: '
               'O=C1OC(/C=C/C)C(C(O)CC=CC2OC2C=CC=CC=3OC=C(N3)C(OC(CC=CC=CC=CC(CC4=NC1=CO4)OC)C(C(O)/C=C/C)(C)C)=O)(C)C '
               'NAME: Disorazole-G2 REASON: MISSED Found 0 free carboxyl '
               'group(s), expected exactly 2\n'
               ' * SMILES: O=C1OC=CC=CCC(=O)OC=CC=CC1 NAME: Brevidiolide '
               'REASON: MISSED Found 0 free carboxyl group(s), expected '
               'exactly 2\n'
               ' * SMILES: O=C(OCC=1OC(COC(=O)C)=CC1)C NAME: '
               '2,5-bis(hydroxymethyl)furan diacetate REASON: MISSED Found 0 '
               'free carboxyl group(s), expected exactly 2\n'
               ' * SMILES: O=C(C1(O)C(OC(=O)C)C=C[C@H]1OC(=O)C)CCCCCCCCCCCCCC '
               'NAME: 1,4-di-O-acetyl hygrophorone E14 REASON: MISSED Found 0 '
               'free carboxyl group(s), expected exactly 2\n'
               ' * SMILES: O(C(CCOC(=O)C(C)=C)C)C(=O)C(C)=C NAME: '
               '1,3-Butyleneglycol dimethacrylate REASON: MISSED Found 0 free '
               'carboxyl group(s), expected exactly 2\n'
               ' * SMILES: O=C(C1(O)C(OC(=O)C)C=C[C@H]1OC(=O)C)CCCCCCCCCC '
               'NAME: 1,4-di-O-acetyl hygrophorone E10 REASON: MISSED Found 0 '
               'free carboxyl group(s), expected exactly 2\n'
               ' * SMILES: '
               'O=C1O[C@@H](C[C@@H](O)[C@@H](OC(=O)C)C=C[C@H]2[C@@H]1O2)C '
               'NAME: 7alpha-acetoxymultiplolide A REASON: MISSED Found 0 free '
               'carboxyl group(s), expected exactly 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'NCC(=O)CCC([O-])=O',
                                     'name': '5-aminolevulinate',
                                     'reason': 'Found 1 free carboxyl '
                                               'group(s), expected exactly 2'},
                                 {   'smiles': '[H][C@@]12CCCC(C)(C)C1CC[C@]1([H])[C@@]2(C)CC[C@]2(C)[C@]([H])(CC[C@@]12C)[C@H](C)CCCC(C)C',
                                     'name': 'cucurbitane',
                                     'reason': 'Found 0 free carboxyl '
                                               'group(s), expected exactly 2'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC2=CC=CC=C2',
                                     'name': 'Arg-Phe-Tyr',
                                     'reason': 'Molecule contains peptide '
                                               'bonds'},
                                 {   'smiles': 'C(CC(C(=O)O)NC(CCC(=O)O)C(=O)O)CN',
                                     'name': 'ornaline',
                                     'reason': 'Found 3 free carboxyl '
                                               'group(s), expected exactly 2'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(15:0/18:1(11Z))',
                                     'reason': 'Molecular weight is too high '
                                               '(703.52 Da)'},
                                 {   'smiles': 'O=CC1=C(O)C=CC2=C1[C@H](C3=C4O[C@H](C(O)(C)C)COC4=CC(=C3)C)[C@@H](C(O)(C)C)C2',
                                     'name': 'Diaporindene A',
                                     'reason': 'Found 0 free carboxyl '
                                               'group(s), expected exactly 2'},
                                 {   'smiles': 'O(C(CCCCCCCCC)CCC/C=C/C)C(=O)/C=C(/C)\\C(O)=O',
                                     'name': 'Chaetomellic acid B',
                                     'reason': 'Found 1 free carboxyl '
                                               'group(s), expected exactly 2'},
                                 {   'smiles': 'Oc1ccc(cc1)[C@H]1Oc2cc(O)cc([C@@H]3[C@H](Oc4ccc(\\C=C\\c5cc(O)cc(O)c5)cc34)c3ccc(O)cc3)c2[C@@H]1c1cc(O)cc(O)c1',
                                     'name': 'trans-diptoindonesin B',
                                     'reason': 'Molecular weight is too high '
                                               '(680.20 Da)'},
                                 {   'smiles': 'O1C(CC(=O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3',
                                     'name': "4',7-dihydroxyflavanone",
                                     'reason': 'Found 0 free carboxyl '
                                               'group(s), expected exactly 2'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO',
                                     'name': 'beta-D-GlcpNAc-(1->4)-beta-D-Galp-(1->4)-D-GlcpNAc',
                                     'reason': 'Molecule contains peptide '
                                               'bonds'}],
    'sample_false_negatives': [   {   'smiles': 'CC(O)c1c(C)c2cc3[nH]c(cc4nc(cc5[nH]c(cc1n2)c(C)c5CCC(O)=O)c(CCC(O)=O)c4C)c(C)c3C(C)O',
                                      'name': 'hematoporphyrin',
                                      'reason': 'Molecular weight is too high '
                                                '(598.28 Da)'},
                                  {   'smiles': 'O=C1N[C@H](C(=O)N[C@H]1CCCNC(=O)C=C(CCOC(=O)C)C)CCCNC(=O)C=C(CCOC(=O)C)C',
                                      'name': 'Trichocyclodipeptide A',
                                      'reason': 'Molecule contains peptide '
                                                'bonds'},
                                  {   'smiles': 'OC(=O)[C@@H](CC1=CC(O)=C(O)C=C1)OC(=O)\\C=C\\C1=C2[C@@H]([C@H](OC2=C(O)C=C1)C1=CC(O)=C(O)C=C1)C(=O)O[C@H](CC1=CC(O)=C(O)C=C1)C(O)=O',
                                      'name': 'salvianolic acid B',
                                      'reason': 'Molecular weight is too high '
                                                '(718.15 Da)'},
                                  {   'smiles': 'O(CCCCCCC)C(=O)C(OCCC)=O',
                                      'name': 'Oxalic acid, heptyl propyl '
                                              'ester',
                                      'reason': 'Found 0 free carboxyl '
                                                'group(s), expected exactly 2'},
                                  {   'smiles': 'O=C(O[C@H](C[C@H]1O[C@@H]([C@H](C(=O)O)C)CC1)CC)[C@H]([C@H]2O[C@@H](C[C@H](O)CC)CC2)C',
                                      'name': 'Homononactyl homononactate',
                                      'reason': 'Found 1 free carboxyl '
                                                'group(s), expected exactly 2'},
                                  {   'smiles': 'CCN1CCCc2cc3c(Oc4cc5=[N+](CC)CCCc5cc4=C3c3ccc(cc3C(O)=O)C(O)=O)cc12',
                                      'name': 'ATTO 565 meta-isomer(1+)',
                                      'reason': 'Molecular weight is too high '
                                                '(511.22 Da)'},
                                  {   'smiles': 'O=C1OC(/C=C/C)C(C(O)CC=CC2OC2C=CC=CC=3OC=C(N3)C(OC(CC=CC=CC=CC(CC4=NC1=CO4)OC)C(C(O)/C=C/C)(C)C)=O)(C)C',
                                      'name': 'Disorazole-G2',
                                      'reason': 'Molecular weight is too high '
                                                '(758.38 Da)'},
                                  {   'smiles': 'O=C1OC=CC=CCC(=O)OC=CC=CC1',
                                      'name': 'Brevidiolide',
                                      'reason': 'Found 0 free carboxyl '
                                                'group(s), expected exactly 2'},
                                  {   'smiles': '[H][C@@]12C[C@](C)(CC[C@]1(C)CC[C@]1(C)C2=CC(=O)[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C(O)=O)C(C)(C)[C@]3([H])CC[C@@]12C)C(O)=O',
                                      'name': 'glycyrrhetic acid '
                                              '3-O-glucuronide',
                                      'reason': 'Molecular weight is too high '
                                                '(646.37 Da)'},
                                  {   'smiles': 'C(=O)([C@@H](NC(=O)CC[C@@H](C(=O)O)N)CC=1C=CC(=CC1)O)O',
                                      'name': 'gamma-Glu-Tyr',
                                      'reason': 'Molecule contains peptide '
                                                'bonds'}],
    'attempt': 2,
    'reasoning': '**Analysis:**\n'
                 '\n'
                 'The previous program attempted to classify dicarboxylic '
                 'acids by counting the number of free carboxyl groups '
                 '(`-COOH`) that are not part of esters or amides. However, it '
                 'had several issues that led to a low F1 score:\n'
                 '\n'
                 '1. **Incomplete detection of carboxyl groups:** The SMARTS '
                 'pattern `"C(=O)[O;H1]"` only matches protonated carboxylic '
                 'acids (`-COOH`) but misses deprotonated carboxylates '
                 '(`-COO^-`), which are common in biological molecules.\n'
                 '\n'
                 '2. **Simplistic checks for esters and amides:** The method '
                 'for detecting esters and amides was too simplistic and may '
                 'have incorrectly classified some carboxyl groups.\n'
                 '\n'
                 '3. **False positives with peptides and large molecules:** '
                 'The code classified peptides and other large biomolecules '
                 'with two free carboxyl groups as dicarboxylic acids, which '
                 'is not accurate.\n'
                 '\n'
                 '**Improvements:**\n'
                 '\n'
                 '- **Use a more inclusive SMARTS pattern:** To detect both '
                 'protonated and deprotonated carboxyl groups, we can use the '
                 'pattern `"[CX3](=O)[O;H1,-1]"`.\n'
                 '\n'
                 '- **Enhanced ester and amide checks:** We can improve the '
                 'checks by examining the connectivity around the carboxyl '
                 'group. Specifically, we can verify that:\n'
                 '  - The hydroxyl oxygen is only connected to the carboxyl '
                 'carbon and possibly a hydrogen (not to any other heavy '
                 'atom).\n'
                 '  - The carboxyl carbon is not single-bonded to any nitrogen '
                 'atom (which would indicate an amide linkage).\n'
                 '\n'
                 '- **Exclude peptides and large molecules:** By detecting the '
                 'presence of peptide bonds (amide bonds between carbonyl '
                 'carbon and nitrogen) and setting a molecular weight '
                 'threshold (e.g., 500 Da), we can exclude large biomolecules '
                 'and peptides.\n'
                 '\n'
                 '---',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 425,
    'num_false_positives': 1229,
    'num_true_negatives': 140488,
    'num_false_negatives': 158,
    'num_negatives': None,
    'precision': 0.2569528415961306,
    'recall': 0.7289879931389366,
    'f1': 0.3799731783638802,
    'accuracy': 0.9902529866479269,
    'negative_predictive_value': 0.9988766122036887}