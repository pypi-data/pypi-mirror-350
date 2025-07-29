"""
Classifies: CHEBI:73011 germacranolide
"""
"""
Classifies: Germacranolide – A sesquiterpene lactone based on a germacrane skeleton.
This updated approach first checks for the presence of a 5‐membered lactone ring 
(γ‐lactone) using a SMARTS pattern. Then the Bemis–Murcko scaffold is computed to isolate 
the core of the molecule. Within that scaffold, we search for a 10‐membered ring that is 
predominantly carbons (heuristic: at least 8 of 10 atoms are carbons) and ensure that the 
scaffold contains roughly 15 carbon atoms (sesquiterpene tropism). These additional criteria 
help resolve some of the formerly misclassified cases.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold

def is_germacranolide(smiles: str):
    """
    Determines if a molecule is a germacranolide based on its SMILES string.
    A germacranolide is a sesquiterpene lactone based on a germacrane skeleton.
    
    The classification now uses the following heuristic criteria:
      1. The molecule must contain a 5‐membered lactone ring (γ‐lactone), detected using the SMARTS "[CX3](=O)[OX2r5]".
      2. The molecule’s core scaffold (Bemis–Murcko scaffold) should contain a 10‐membered ring 
         (with at least 8 carbons) suggesting a germacrane skeleton.
      3. The scaffold should also have a carbon count roughly characteristic of a sesquiterpene (≈15 ± a few).
      4. The molecular weight must be above a minimum threshold for sesquiterpene lactones.
      
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is likely a germacranolide.
        str: Reason for classification or error.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # --- Criterion 1: Check for a 5-membered γ-lactone ring ---
    # The SMARTS pattern below looks for a carbonyl group attached to an oxygen that is in a 5-membered ring.
    lactone_smarts = "[CX3](=O)[OX2r5]"
    lactone_pat = Chem.MolFromSmarts(lactone_smarts)
    if not mol.HasSubstructMatch(lactone_pat):
        return False, "No 5-membered γ-lactone group (ring ester) found."
    
    # --- Criterion 2: Evaluate the core scaffold via Bemis–Murcko ---
    try:
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
    except Exception as e:
        return False, f"Error obtaining scaffold: {e}"
        
    if scaffold is None:
        return False, "Could not obtain a Bemis–Murcko scaffold."
    
    scaffold_ring_info = scaffold.GetRingInfo()
    scaffold_rings = scaffold_ring_info.AtomRings() if scaffold_ring_info is not None else []
    
    has_10_membered = False
    # Look through rings in the scaffold
    for ring in scaffold_rings:
        if len(ring) == 10:
            carbon_count_ring = sum(1 for idx in ring if scaffold.GetAtomWithIdx(idx).GetAtomicNum() == 6)
            if carbon_count_ring >= 8:
                has_10_membered = True
                break
    if not has_10_membered:
        return False, "No suitable 10-membered carbocycle (germacrane skeleton) found in scaffold."
    
    # --- Criterion 3: Check the carbon count in the scaffold (expect about 15 carbons for sesquiterpenes) ---
    scaffold_atoms = scaffold.GetAtoms()
    scaffold_carbon_count = sum(1 for atom in scaffold_atoms if atom.GetAtomicNum() == 6)
    # Allow a tolerance (e.g., 12 to 18 carbons) because substituents might add extra atoms.
    if not (12 <= scaffold_carbon_count <= 18):
        return False, f"Scaffold carbon count ({scaffold_carbon_count}) is not in the expected range for a sesquiterpene."
    
    # --- Criterion 4: Check molecular weight to be above a lower limit, e.g. 200 Da ---
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200:
        return False, "Molecular weight is too low to be a sesquiterpene lactone."
    
    return True, "Contains a 10-membered germacrane skeleton (in the core scaffold), a 5-membered γ-lactone, and appropriate carbon count typical of germacranolides."

# Example use:
if __name__ == "__main__":
    example_smiles = "C\\C=C(/C)C(=O)O[C@H]1C\\C(C)=C\\C(=O)\\C=C(C)/[C@H](O)[C@H]2OC(=O)C(=C)[C@H]12"  # Molephantinin
    result, reason = is_germacranolide(example_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:73011',
                          'name': 'germacranolide',
                          'definition': 'A sesquiterpene lactone based on '
                                        'germacrane skeleton.',
                          'parents': ['CHEBI:37667'],
                          'xrefs': ['Wikipedia:Germacranolide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 58,
                           'log_lines_of_code': 4.060443010546419,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
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
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from rdkit.Chem.Scaffolds import '
                                          'MurckoScaffold'],
                           'imports_count': 3,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetScaffoldForMol',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'GetAtoms',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum'],
                           'methods_called_count': 10,
                           'smarts_strings': ['lactone_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_germacranolide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "No 5-membered γ-lactone '
                                          'group (ring ester) found."',
                                          'False, f"Error obtaining scaffold: '
                                          '{e}"',
                                          'False, "Could not obtain a '
                                          'Bemis–Murcko scaffold."',
                                          'False, "No suitable 10-membered '
                                          'carbocycle (germacrane skeleton) '
                                          'found in scaffold."',
                                          'False, f"Scaffold carbon count '
                                          '({scaffold_carbon_count}) is not in '
                                          'the expected range for a '
                                          'sesquiterpene."',
                                          'False, "Molecular weight is too low '
                                          'to be a sesquiterpene lactone."',
                                          'True, "Contains a 10-membered '
                                          'germacrane skeleton (in the core '
                                          'scaffold), a 5-membered γ-lactone, '
                                          'and appropriate carbon count '
                                          'typical of germacranolides."'],
                           'returns_count': 8,
                           'complexity': 5.412088602109284},
    'message': '\n'
               'Attempt failed: F1 score of 0.6960352422907489 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C\\C=C(/C)C(=O)O[C@H]1C\\C(C)=C\\C(=O)\\C=C(C)/[C@H](O)[C@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Molephantinin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'O1[C@]2([C@]([C@@H](C1=O)C)(CCC(=CCCC(=C2)C)C(O)=O)[H])[H] '
               'NAME: '
               '(3S,3As,6Z,10E,11aS)-3,10-dimethyl-2-oxo-3a,4,5,8,9,11a-hexahydro-3H-cyclodeca[b]furan-6-carboxylic '
               'acid REASON: CORRECT Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: '
               '[H][C@]12OC(=O)C(=C)[C@]1([H])[C@H](C[C@@](C)(OC(C)=O)C(=O)CC[C@H](C)[C@@H]2O)OC(=O)C(C)=C '
               'NAME: lychnostatin 1 REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'O1C2C(C(OC(=O)C(CC)C)C(OC)C(=CCCC(=C2)CO)C=O)C(C1=O)=C NAME: '
               '[(6Z,10Z)-6-Formyl-10-(hydroxymethyl)-5-methoxy-3-methylidene-2-oxo-3a,4,5,8,9,11a-hexahydrocyclodeca[b]furan-4-yl] '
               '2-methylbutanoate REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: O1C2C(C(O)C=C(CCC=C(C2)C)C)C(C1=O)=C NAME: '
               'Desacetyllaurenobiolide REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'O1[C@]2([C@]([C@H](C1=O)C)(CCC(=CCC(=O)[C@H](C2)C)C)[H])[H] '
               'NAME: Ketopelenolide a REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'CC(=O)O[C@H]1C[C@H]2O[C@]2(C)C[C@@H](OC(=O)C(C)=C)[C@@H]2[C@H](OC(=O)C2=C)\\C=C1\\C '
               'NAME: Erioflorin acetate REASON: CORRECT Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'O1[C@]2([C@@]([C@@H](O)CC(=CCCC(=C2)C)CO)(C(C1=O)=C)[H])[H] '
               'NAME: budlein B REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'C[C@H]1O[C@@]1(C)C(=O)OC1C(O)[C@@H]2[C@H](OC(=O)C2=C)\\C=C(C)/[C@H](C\\C=C1/C)OC(C)=O '
               'NAME: Eupatocunoxin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'C\\C=C(\\C)C(=O)O[C@H]1C\\C(C)=C\\C[C@H](O)\\C(C)=C/[C@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Nobilin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               '[H][C@]12OC(=O)C(=C)[C@]1([H])[C@H](O)C\\C(C)=C\\CC\\C(C)=C\\2 '
               'NAME: eupatolide REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'C\\C1=C/CC\\C(CO)=C\\[C@@H](O)[C@H]2[C@H](C1)OC(=O)C2=C NAME: '
               'Artemisiifolin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)\\C=C/C(=O)[C@@](C)(O)C[C@@H](OC(=O)CC(C)C)[C@@]1([H])C(=C)C(=O)O2 '
               'NAME: neurolenin A REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'C\\C=C(\\C)C(=O)O[C@@H]1\\C=C(C)/[C@@H](O)C[C@H](OC(C)=O)\\C(C)=C/[C@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Eupacunin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: O1C2C(C(O)CC(=CCCC(=C2)C)CO)C(C1=O)=C NAME: '
               '(6Z,10E)-4-hydroxy-6-(hydroxymethyl)-10-methyl-3-methylidene-3a,4,5,8,9,11a-hexahydrocyclodeca[b]furan-2-one '
               'REASON: CORRECT Contains a 10-membered germacrane skeleton and '
               'a 5-membered γ-lactone group typical of germacranolides.\n'
               ' * SMILES: '
               'C[C@H]1O[C@@]1(C)C(=O)O[C@@H]1C\\C(C)=C\\C[C@H](OC(C)=O)\\C(C)=C\\[C@@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Ursiniolide A REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'C\\C=C(\\C)C(=O)O[C@H]1[C@@H]2[C@H](OC(=O)C2=C)\\C=C(C)/[C@H](C\\C=C(C)\\C1O)OC(C)=O '
               'NAME: Eupatocunin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'CC(CO)C(=O)O[C@H]1C\\C(C)=C\\CC\\C(CO)=C\\[C@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Arctiopicrin REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: O1C2C(CC(=O)C(CCC=C(C2)C)C)=C(C1=O)C NAME: '
               '(9E)-3,6,10-trimethyl-4,6,7,8,11,11a-hexahydrocyclodeca[b]furan-2,5-dione '
               'REASON: CORRECT Contains a 10-membered germacrane skeleton and '
               'a 5-membered γ-lactone group typical of germacranolides.\n'
               ' * SMILES: C\\C1=C/CC\\C(C)=C\\[C@H]2OC(=O)C(=C)[C@@H]2CC1 '
               'NAME: costunolide REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: '
               'O1[C@@H]2[C@H]1C(=O)[C@](O)([C@H](OC(=O)C)[C@@H](OC(=O)C(C)=C)[C@@]3([C@](OC(=O)C3=C)(C[C@H]2C)[H])[H])C '
               'NAME: Calealactone B REASON: CORRECT Contains a 10-membered '
               'germacrane skeleton and a 5-membered γ-lactone group typical '
               'of germacranolides.\n'
               ' * SMILES: CC1=CCCC2(C(O2)C3C(CC1)C(=C)C(=O)O3)C NAME: '
               'LSM-6390 REASON: CORRECT Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: '
               'O1C2(C1C3OC(=O)C(C3C(OC(=O)C4(OC4C)C)C(OC(=O)C)C(=CCC2)C(OC)=O)=C)C '
               'NAME: PSF-A REASON: CORRECT Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: O1C2C(C(O)C(=O)C(=CC(O)CC(=C2)C)C)C(C1=O)=C NAME: '
               '2beta,9xi-Dihydroxy-8-oxo-1(10),4,11(13)-germacratrien-12,6alpha-olide '
               'REASON: CORRECT Contains a 10-membered germacrane skeleton and '
               'a 5-membered γ-lactone group typical of germacranolides.\n'
               ' * SMILES: '
               'CC1=CCC[C@@]2([C@@H](O2)[C@@H]3[C@@H](CC1)C(=C)C(=O)O3)C NAME: '
               'LSM-4225 REASON: CORRECT Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               'False positives: SMILES: '
               'O1C2(C1C(=O)CC(C(OC(=O)/C(/C)=C\\C)C(O)C3C(OC(=O)C3=C)C2)=C)C '
               'NAME: '
               '(10-hydroxy-3-methyl-8,12-dimethylidene-6,13-dioxo-4,14-dioxatricyclo[9.3.0.03,5]tetradecan-9-yl) '
               '(Z)-2-methylbut-2-enoate REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'C=1(CCC=C([C@H]([C@@H]([C@]2([C@@](C1)(OC(C2=C)=O)[H])[H])OC(/C(/C)=C\\C)=O)OC(=O)C)C(OC)=O)C '
               'NAME: polymatin B REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: O1C2(C1CCC3(OC3C(O)C=4C(OC(=O)C4C)C2)C)C NAME: '
               '(1beta,4alpha,5alpha,6beta,8alpha,10b)-1,10:4,5-Diepoxy-6-hydroxy-7(11)-germacren-12,8-olide '
               'REASON: WRONGLY CLASSIFIED Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: '
               'O=C1O[C@H]2C3=C(O)C=CC(=C3[C@H](OC)C(=CCC[C@@]14O[C@H]42)C)O '
               'NAME: Clavilactone E REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               '[H][C@]12CC(=C)[C@H](O)CC\\C(C)=C\\[C@@H](O)[C@]1([H])C(=C)C(=O)O2 '
               'NAME: tatridin B REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               '[H][C@]12OC(=O)C(=C)[C@]1([H])[C@@H](C[C@@](C)(O)\\C=C\\C(=O)\\C(C)=C/2)OC(=O)C(\\C)=C\\C '
               'NAME: eupaheliangolide A REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)\\C(C)=C\\[C@@]3([H])OC(=O)C(=C)[C@]3([H])[C@@H](C[C@@]1(C)O2)OC(=O)C(\\C)=C\\C '
               'NAME: heliangin REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'O=C1O[C@@H](C[C@@H]2O[C@@H]2C=C[C@@]3(C1)OC(=O)[C@@H](C3)O)C '
               'NAME: Botryolide C REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'Cl[C@@H]1[C@@]2(OC(=O)[C@@H]([C@@]2(O)C(OC(=O)C)[C@@]3([C@]([C@H]4O[C@H]4[C@@H](OC(=O)C)[C@@H]3C)([C@@H](O)C=CC1=C)C)[H])C)[H] '
               'NAME: Brianthein X REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'O=C1OCC2C=C(C34OC5C(C)C(C3C(C=CC4CC(C(OC2C(O)COC=CC6=C(CC1)C(=O)OC6=O)=O)OC)C5)O)C '
               'NAME: Coloradocin REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C[C@@]([H])(OC3=O)c3c(CO)coc3C[C@@]1(C)O2 NAME: '
               'daibulactone B, (rel)- REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'C=1(CCC=C([C@H]([C@@H]([C@]2([C@@](C1)(OC(C2=C)=O)[H])[H])OC([C@]3(C)[C@H](C)O3)=O)OCC)C=O)C '
               'NAME: '
               '8beta-epoxyangeloyloxy-9alpha-ethoxy-14-oxo-acanthospermolide '
               'REASON: WRONGLY CLASSIFIED Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](C)CCC(=O)\\C(C)=C\\C[C@]1([H])C(=C)C(=O)O2 '
               'NAME: inuloxin A REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: O1CC=2CC[C@H]([C@@](CCC=3C=COC3)(C)C=CC=CC2C1=O)C '
               'NAME: '
               '15,16-Epoxy-5,10-seco-clerodan-1(10),2,4,13(16),14-pentaen-18,19-olide '
               'REASON: WRONGLY CLASSIFIED Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: '
               'C[C@@]12CC[C@@H]3[C@H](OC(=O)C3=C)[C@H]3O[C@]3(C)CC[C@H]1O2 '
               'NAME: Michelenolide REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'CC(=O)O[C@@H]1C\\C(C)=C\\CC[C@@]2(C)OC2[C@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Lipiferolide REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'CC(=O)O[C@@H]1\\C=C(C)\\CC[C@H]2O[C@]2(C)C[C@@H]2OC(=O)C(=C)[C@@H]12 '
               'NAME: Pyrethrosin REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: Cc1coc2C\\C(C)=C\\CC[C@]34O[C@H]3[C@@H](OC4=O)c12 '
               'NAME: Linderane REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: O1C2(C1CCC3(OC3CC=4C(OC(=O)C4C)C2)C)C NAME: '
               '5,10,15-Trimethyl-4,9,13-trioxatetracyclo[10.3.0.03,5.08,10]pentadec-1(15)-en-14-one '
               'REASON: WRONGLY CLASSIFIED Contains a 10-membered germacrane '
               'skeleton and a 5-membered γ-lactone group typical of '
               'germacranolides.\n'
               ' * SMILES: '
               'CC(=O)OCC1=C2[C@H](OC1=O)[C@H]1O[C@]1(C)CCC(=O)[C@@](C)(C[C@@H]2OC(=O)C(C)=C)OC(C)=O '
               'NAME: Glaucolide A REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'C=1(CCC=C([C@H]([C@@H]([C@]2([C@@](C1)(OC(C2=C)=O)[H])[H])OC([C@]3(C)[C@H](C)O3)=O)OC(=O)C)C(OC)=O)C '
               'NAME: uvedalin REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'C[C@H]1C(=O)O[C@H]2\\C=C(C)/CC[C@@H](OC(C)=O)[C@@]3(C)C=CC(=O)[C@@](C)(O)[C@@H]3[C@H](OC(C)=O)[C@]12O '
               'NAME: Renillafoulin A REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               'CC(=C)C(=O)O[C@H]1C[C@@]23O[C@@H]2CC\\C(CO[C@H]3O)=C\\[C@H]2OC(=O)C(=C)[C@H]12 '
               'NAME: Vernolide REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]34O[C@@H]3[C@@]([H])(OC4=O)c3c(C)coc3C[C@]1(C)O2 '
               'NAME: linderadin REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)\\C(C)=C\\[C@@]3([H])OC(=O)C(=C)[C@]3([H])[C@@H](C[C@@]1(C)O2)OC(=O)C(\\C)=C\\C '
               'NAME: 3-epi-heliangin REASON: WRONGLY CLASSIFIED Contains a '
               '10-membered germacrane skeleton and a 5-membered γ-lactone '
               'group typical of germacranolides.\n'
               'False negatives: SMILES: '
               'CC(=C)C(=O)O[C@@H]1\\C=C(CO)/C2=CC(=O)[C@@](C)(C[C@@H]3OC(=O)C(=C)[C@@H]13)O2 '
               'NAME: Goyazensolide REASON: MISSED No suitable 10-membered '
               'carbocycle (germacrane skeleton) found.\n'
               ' * SMILES: '
               '[C@]12([C@H](C[C@@]([C@H](C[C@H]3OC(C([C@@H]3[C@@H](C1)OC(=O)C(C)CC)=C)=O)C)(O2)O)O)C '
               'NAME: viguilenin REASON: MISSED No suitable 10-membered '
               'carbocycle (germacrane skeleton) found.\n'
               ' * SMILES: '
               '[H][C@@]12O[C@@](OC)(\\C=C(C)\\C[C@H](OC(=O)C(\\C)=C\\C)[C@@]3([H])C(=C)C(=O)O[C@]13[H])C=C2C '
               'NAME: '
               '2beta-methoxy-2-deethoxy-8-O-deacylphantomolin-8-O-tiglinate '
               'REASON: MISSED No suitable 10-membered carbocycle (germacrane '
               'skeleton) found.\n'
               ' * SMILES: '
               '[H][C@@]12O[C@@](OCC)(\\C=C(C)/C[C@H](OC(=O)C(C)=C)[C@@]3([H])C(=C)C(=O)O[C@]13[H])C=C2C '
               'NAME: phantomolin REASON: MISSED No suitable 10-membered '
               'carbocycle (germacrane skeleton) found.\n'
               ' * SMILES: '
               'O1[C@]2([C@@H](O)C[C@]1(O)C(C[C@]3(OC(=O)C([C@]3([C@H](OC(=O)/C(/C)=C\\C)C2)[H])=C)[H])CO)C '
               'NAME: 4,5-Dihydroniveusin A REASON: MISSED No suitable '
               '10-membered carbocycle (germacrane skeleton) found.\n'
               ' * SMILES: O1C2(C3C4OC(=O)C(C4CCC(=C3C(=O)C12)C)=C)C NAME: '
               '9,14-Dimethyl-5-methylidene-3,13-dioxatetracyclo[8.4.0.02,6.012,14]tetradec-9-ene-4,11-dione '
               'REASON: MISSED No suitable 10-membered carbocycle (germacrane '
               'skeleton) found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No 5-membered γ-lactone group '
                                               '(ring ester) found.'}],
    'sample_false_negatives': [   {   'smiles': 'CC(=C)C(=O)O[C@@H]1\\C=C(CO)/C2=CC(=O)[C@@](C)(C[C@@H]3OC(=O)C(=C)[C@@H]13)O2',
                                      'name': 'Goyazensolide',
                                      'reason': 'No suitable 10-membered '
                                                'carbocycle (germacrane '
                                                'skeleton) found in scaffold.'},
                                  {   'smiles': '[C@]12([C@H](C[C@@]([C@H](C[C@H]3OC(C([C@@H]3[C@@H](C1)OC(=O)C(C)CC)=C)=O)C)(O2)O)O)C',
                                      'name': 'viguilenin',
                                      'reason': 'No suitable 10-membered '
                                                'carbocycle (germacrane '
                                                'skeleton) found in scaffold.'},
                                  {   'smiles': '[H][C@@]12O[C@@](OC)(\\C=C(C)\\C[C@H](OC(=O)C(\\C)=C\\C)[C@@]3([H])C(=C)C(=O)O[C@]13[H])C=C2C',
                                      'name': '2beta-methoxy-2-deethoxy-8-O-deacylphantomolin-8-O-tiglinate',
                                      'reason': 'No suitable 10-membered '
                                                'carbocycle (germacrane '
                                                'skeleton) found in scaffold.'},
                                  {   'smiles': '[H][C@@]12O[C@@](OCC)(\\C=C(C)/C[C@H](OC(=O)C(C)=C)[C@@]3([H])C(=C)C(=O)O[C@]13[H])C=C2C',
                                      'name': 'phantomolin',
                                      'reason': 'No suitable 10-membered '
                                                'carbocycle (germacrane '
                                                'skeleton) found in scaffold.'},
                                  {   'smiles': 'O1[C@]2([C@@H](O)C[C@]1(O)C(C[C@]3(OC(=O)C([C@]3([C@H](OC(=O)/C(/C)=C\\C)C2)[H])=C)[H])CO)C',
                                      'name': '4,5-Dihydroniveusin A',
                                      'reason': 'No suitable 10-membered '
                                                'carbocycle (germacrane '
                                                'skeleton) found in scaffold.'},
                                  {   'smiles': 'O1C2(C3C4OC(=O)C(C4CCC(=C3C(=O)C12)C)=C)C',
                                      'name': '9,14-Dimethyl-5-methylidene-3,13-dioxatetracyclo[8.4.0.02,6.012,14]tetradec-9-ene-4,11-dione',
                                      'reason': 'No suitable 10-membered '
                                                'carbocycle (germacrane '
                                                'skeleton) found in '
                                                'scaffold.'}],
    'attempt': 1,
    'reasoning': 'Below is our updated Python solution. In our reasoning we '
                 'looked at the previous approach and the outcomes. We noticed '
                 'that although requiring a five‐membered “lactone” (using the '
                 'SMARTS for an ester in a ring) and a 10‐membered ring (with '
                 'mostly carbons) can pick up many true germacranolide cases, '
                 'many molecules are missed (false negatives) or falsely '
                 'classified (false positives) because the 10‐membered ring is '
                 'sometimes “hidden” in a fused bicyclic structure. We '
                 'therefore decided to (1) compute the molecule’s Bemis–Murcko '
                 'scaffold to extract the core and then search that scaffold '
                 'for a 10‐membered ring; and (2) require that the scaffold '
                 'contain roughly 15 carbons (accepting a small range) as '
                 'expected for a sesquiterpene. These additional checks help '
                 'reject false positives and capture cases where the '
                 'germacrane skeleton is embedded in fused ring systems. \n'
                 '\n'
                 'Below is the full Python code for is_germacranolide:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 79,
    'num_false_positives': 62,
    'num_true_negatives': 142153,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.5602836879432624,
    'recall': 0.9294117647058824,
    'f1': 0.6991150442477876,
    'accuracy': 0.9995221363316936,
    'negative_predictive_value': 0.9999577937379976}