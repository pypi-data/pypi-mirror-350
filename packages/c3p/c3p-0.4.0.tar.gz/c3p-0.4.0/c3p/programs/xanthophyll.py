"""
Classifies: CHEBI:27325 xanthophyll
"""
"""
Classifies: Xanthophyll
Definition: A subclass of carotenoids consisting of the oxygenated carotenes.
Xanthophylls are characterized by a long conjugated polyene chain, an extensive carbon skeleton,
and oxygen-based functional groups. Many have cyclic endgroups, but some acyclic xanthophylls exist.
For classification, we require:
  - At least one oxygen atom.
  - A sufficiently large carbon backbone (≥30 carbons).
  - A long conjugated polyene chain: if a ring is present we require at least 4 consecutive C=C bonds;
    if no ring is present (acyclic) we require a longer conjugated chain (≥5 consecutive C=C bonds).
  - A relatively high molecular weight (≥400 Da).
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_xanthophyll(smiles: str):
    """
    Determines if a molecule is a xanthophyll based on its SMILES string.
    
    A xanthophyll is defined as an oxygenated carotenoid. Here, we enforce that the molecule:
      - Has at least one oxygen atom.
      - Contains at least 30 carbon atoms.
      - Possesses a long conjugated polyene chain.
         * If at least one ring exists, we require a pattern of 4 consecutive C=C bonds.
         * If no ring exists (acyclic candidate), we require a pattern of 5 consecutive C=C bonds.
      - Has a molecular weight of at least 400 Da.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is likely a xanthophyll, False otherwise.
        str: Reason for the classification.
    """
    
    # Parse the molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check oxygenation
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count < 1:
        return False, "No oxygen atoms found; not an oxygenated carotene"
    
    # Check carbon scaffold; require at least 30 carbon atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 30:
        return False, f"Too few carbon atoms ({c_count}); expected at least 30 for a carotenoid backbone"
    
    # Molecular weight check (xanthophylls are large molecules)
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 400:
        return False, f"Molecular weight too low ({mw:.1f} Da); expected ≥400 Da for a xanthophyll"
    
    # Check for rings.
    rings = mol.GetRingInfo().AtomRings()
    has_ring = len(rings) > 0
    
    # Depending on whether a ring exists, choose a SMARTS pattern for a conjugated polyene chain.
    # (Note: these SMARTS patterns are simplified; more elaborate conjugation detection is possible.)
    if has_ring:
        # For cyclic xanthophylls, require at least 4 consecutive C=C bonds.
        polyene_smarts = "C=C-C=C-C=C-C=C"
        chain_info = "a conjugated chain with at least 4 consecutive C=C bonds"
    else:
        # For acyclic xanthophylls, require a longer chain (here: 5 consecutive C=C bonds).
        polyene_smarts = "C=C-C=C-C=C-C=C-C=C"
        chain_info = "a conjugated chain with at least 5 consecutive C=C bonds (typical for acyclic carotenoids)"
    
    polyene_pattern = Chem.MolFromSmarts(polyene_smarts)
    if polyene_pattern is None:
        return False, "Internal error: could not generate polyene SMARTS pattern"
    
    if not mol.HasSubstructMatch(polyene_pattern):
        return False, f"No long conjugated polyene chain found; expected {chain_info}"
    
    # All conditions met.
    ring_info = "with at least one ring" if has_ring else "without ring structures (acyclic)"
    return True, (f"Contains {ring_info}, a long conjugated polyene chain, sufficient carbon scaffold "
                  f"({c_count} C atoms) and oxygen functionalities (O count: {o_count}), "
                  f"with molecular weight {mw:.1f} Da consistent with xanthophylls")

# Example usage (for testing); remove or comment out before production deployment:
if __name__ == '__main__':
    test_examples = [
        # A cyclic example: (5R,5'R,6S,8'R)-Luteochrome
        "O1C2(C1(CCCC2(C)C)\\C=C/C(/C)=C\\C=C\\C(\\C)=C\\C=C/C=C(/C=C/C=C(\\C3OC4(C(C(CCC4)(C)C)=C3)C)/C)\\C",
        # An acyclic xanthophyll candidate: spheroidene
        "COC(C)(C)C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CCC=C(C)C",
    ]
    for sm in test_examples:
        result, reason = is_xanthophyll(sm)
        print("SMILES:", sm)
        print("Result:", result, "|", reason)
        print("-" * 80)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27325',
                          'name': 'xanthophyll',
                          'definition': 'A subclass of carotenoids consisting '
                                        'of the oxygenated carotenes.',
                          'parents': ['CHEBI:23044'],
                          'xrefs': ['DrugBank:DB00137'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 65,
                           'log_lines_of_code': 4.174387269895637,
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
                                                 1,
                                                 1,
                                                 2,
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
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'CalcExactMolWt',
                                                 'AtomRings',
                                                 'GetRingInfo',
                                                 'GetAtoms',
                                                 'GetAtomicNum'],
                           'methods_called_count': 8,
                           'smarts_strings': ['polyene_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_xanthophyll(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No oxygen atoms found; not '
                                          'an oxygenated carotene"',
                                          'False, f"Too few carbon atoms '
                                          '({c_count}); expected at least 30 '
                                          'for a carotenoid backbone"',
                                          'False, f"Molecular weight too low '
                                          '({mw:.1f} Da); expected ≥400 Da for '
                                          'a xanthophyll"',
                                          'False, "Internal error: could not '
                                          'generate polyene SMARTS pattern"',
                                          'False, f"No long conjugated polyene '
                                          'chain found; expected {chain_info}"',
                                          'True, (f"Contains {ring_info}, a '
                                          'long conjugated polyene chain, '
                                          'sufficient carbon scaffold "'],
                           'returns_count': 7,
                           'complexity': 4.434877453979127},
    'message': '\n'
               'Attempt failed: F1 score of 0.4347826086956522 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O1C2(C1(CCCC2(C)C)C)\\C=C/C(/C)=C\\C=C\\C(\\C)=C\\C=C/C=C(/C=C/C=C(\\C3OC4(C(C(CCC4)(C)C)=C3)C)/C)\\C '
               "NAME: (5R,5'R,6S,8'R)-Luteochrome REASON: CORRECT Contains a "
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'O=C(OCC1OC(O[C@@H]2CC(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C3=C(C[C@@H](OC4C(O)C(O)C(O)C(C4)COC(=O)CCCCCCCCCC(C)C)CC3(C)C)C)\\C)\\C)/C)/C)C(C2)(C)C)C)C(O)C(C1O)O)CCCCCCCCCC(C)C '
               'NAME: Thermobiszeaxanthin Z2-13-13 REASON: CORRECT Contains a '
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'S(O[C@H]1[C@H](O)C(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@H](O)CC2C)(C)C)/C)/C)(C)C)([O-])(=O)=O.[Na+] '
               'NAME: Nostoxanthin sulfate REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/C(OC)C(O)(C)C)\\C)\\C)\\C)/C)/C)C(C)(C)CC1O)C '
               "NAME: 2'-methoxy-3,1'-dihydroxy-beta,psi-caroten-4-one REASON: "
               'CORRECT Contains a long conjugated polyene chain with ≥4 C=C '
               'bonds, sufficient carbon scaffold with ring(s), and oxygen '
               'functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\C1=C(C)C[C@@H](O)CC1(C)C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C1=C(C)C[C@@H](O)CC1(C)C '
               'NAME: zeaxanthin REASON: CORRECT Contains a long conjugated '
               'polyene chain with ≥4 C=C bonds, sufficient carbon scaffold '
               'with ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'O=C(O)/C(=C/C=C/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C1=C(CCCC1(C)C)C)\\C)\\C)/C)/C)/C)/C '
               'NAME: Torularhodin REASON: CORRECT Contains a long conjugated '
               'polyene chain with ≥4 C=C bonds, sufficient carbon scaffold '
               'with ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'C\\C(\\C=C\\C=C(/C)\\C=C\\C1=C(C)C[C@@H](O)CC1(C)C)=C/C=C/C=C(\\C)/C=C/C=C(\\C)/C=C/C1=C(C)C(=O)CCC1(C)C '
               "NAME: 3'-hydroxyechinenone REASON: CORRECT Contains a long "
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C(OCC1OC(O[C@@H]2CC(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C3=C(CCCC3(C)C)C)\\C)\\C)/C)/C)C(C2)(C)C)C)C(O)C(C1O)O)CCCCCCCC(C)C '
               'NAME: C1-11 thermocryptoxanthin-11 REASON: CORRECT Contains a '
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'O1C(C1CC/C(/C)=C\\C=C\\C(\\C)=C\\C=C\\C(=C/C=C/C=C(/C=C/C=C(\\C=C\\C2C(CCC=C2C)(C)C)/C)\\C)\\C)(C)C '
               'NAME: delta-Carotene-1,2-epoxide REASON: CORRECT Contains a '
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'S(O[C@H]1CC(C(=C(C1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=2C([C@@H](O)[C@H](O)CC2C)(C)C)\\C)\\C)(C)C)(O)(=O)=O '
               'NAME: Caloxanthin sulfate REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'OC1CC(C(=C(C1=O)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/C=C(C)C)\\C)\\C)\\C)(C)C '
               "NAME: 3-Hydroxy-3',4'-didehydro-beta,psi-caroten-4-one REASON: "
               'CORRECT Contains a long conjugated polyene chain with ≥4 C=C '
               'bonds, sufficient carbon scaffold with ring(s), and oxygen '
               'functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'OC1(C(C[C@@H](O)C=C1C)(C)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C(=O)CC=2C(C[C@H](O)CC2C)(C)C)\\COC(=O)CCCCCCCCCCCC)\\C '
               "NAME: 6'-Hydroxysiphonaxanthin ester/ 6'-Hydroxysiphonaxanthin "
               "dodecenoate/ 6'-Hydroxysiphonaxanthin "
               '19-(trans-delta2-dodecenoate) REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O[C@@H]1C(C(=C(C[C@H]1O)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@@H](O)C(=O)C2C)(C)C)/C)/C)(C)C '
               'NAME: 4-Ketonostoxanthin REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O[C@@H]1CC(/C(/C(=C1)C)=C/C=C(\\C)/C=C/C=C(\\C)/C=C/C=C/C(=C/C=C/C(=C/C=C\\2/C(C=CC=C2C)(C)C)/C)/C)(C)C '
               'NAME: Monoanhydroescholtzxanthin REASON: CORRECT Contains a '
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'O1C2(C(CC1CC2(O)C)(C)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C(/O)=C/C(=O)C3(C(C(O)CC3)(C)C)C)\\C)\\C '
               'NAME: '
               "(3S,3'S,5R,5'R,6R)-3,6-Epoxy-5,6-dihydro-3',5,8'-trihydroxy-beta,kappa-caroten-6'-one "
               'REASON: CORRECT Contains a long conjugated polyene chain with '
               '≥4 C=C bonds, sufficient carbon scaffold with ring(s), and '
               'oxygen functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'S(O[C@H]1CC(C(=C(C1=O)C)/C=C/C(/C)=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=2C([C@@H](O)[C@H](O)CC2C)(C)C)\\C)\\C)/C)(C)C)(O)(=O)=O '
               'NAME: Erythroxanthin sulfate REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\C(=O)[C@]1(C)CCCC1(C)C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C1=C(C)CCCC1(C)C '
               'NAME: Sapotexanthin REASON: CORRECT Contains a long conjugated '
               'polyene chain with ≥4 C=C bonds, sufficient carbon scaffold '
               'with ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'C=1(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/CC(C)(O)C)\\C)\\C)\\C)/C)/C)C(CCCC1C)(C)C '
               "NAME: 1'-hydroxytorulene REASON: CORRECT Contains a long "
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'CC(/C=C/C=C(C)/C=C/C1=C(C)CCCC1(C)C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C1=C(C)C(=O)[C@@H](O)CC1(C)C '
               'NAME: 3-Hydroxyechinenone REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\C1=C(C)C(=O)CCC1(C)C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C1=C(C)C(=O)[C@@H](O)CC1(C)C '
               'NAME: Phoenicoxanthin REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'C1(=C(C[C@H](CC1(C)C)O)C)/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/[C@H]2C(C=CCC2(C)C)=C)\\C)\\C)/C)/C '
               "NAME: (3R,6'R)-3-hydroxy-3',4'-didehydro-beta,gamma-carotene "
               'REASON: CORRECT Contains a long conjugated polyene chain with '
               '≥4 C=C bonds, sufficient carbon scaffold with ring(s), and '
               'oxygen functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\[C@H]1C(C)=C[C@H](O)CC1(C)C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/[C@@]12O[C@]1(C)C[C@@H](O)CC2(C)C '
               'NAME: lutein 5,6-epoxide REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C2=C(C[C@@H](O)[C@@H](C2(C)C)O)C)\\C)\\C)/C)/C)C(C)(C)[C@H]([C@@H]1O)O)C '
               'NAME: '
               '(2R,3S,2′R,3′R)-2,3,2′,3′-tetrahydroxy-beta,beta-caroten-4-one '
               'REASON: CORRECT Contains a long conjugated polyene chain with '
               '≥4 C=C bonds, sufficient carbon scaffold with ring(s), and '
               'oxygen functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'O[C@H]1CC([C@H](C(=C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C(C[C@@H](O)CC2C)(C)C)/CO)/C)(C)C '
               'NAME: loroxanthin REASON: CORRECT Contains a long conjugated '
               'polyene chain with ≥4 C=C bonds, sufficient carbon scaffold '
               'with ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'O1C2(C1(CC(O)CC2(C)C)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=3C(CCCC3C)(C)C)\\C)\\C '
               'NAME: Cryptoxanthin epoxide REASON: CORRECT Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               'False positives: SMILES: '
               'O=C(OC)/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/CC(OC1OC(C(O)C(C1O)O)CO)(C)C)\\C)\\C)\\C)/C)/C '
               'NAME: methyl glucosyl-3,4-dehydro-apo-8′-lycopenoate REASON: '
               'WRONGLY CLASSIFIED Contains a long conjugated polyene chain '
               'with ≥4 C=C bonds, sufficient carbon scaffold with ring(s), '
               'and oxygen functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](NC(=O)/C=C/C=C/C=C/C=C/C=C/C2=CC=C(O)C=C2)C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1CC(C)C)=O)CC(=O)N)=O)CC(=O)N)C(C)C)C '
               "NAME: Alterochromide B' REASON: WRONGLY CLASSIFIED Contains a "
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'O[C@H]1CC(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C#CC=2C(C[C@H](O)CC2C)(C)C)/C)/C)(C)C '
               'NAME: Diatoxanthin REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@@H](O)C=CC=CC=CC=CC=C([C@H](O)C([C@@H](C[C@@H](C[C@@H](C[C@@H](C[C@H](C[C@H]([C@H]1CCCC)O)O)O)O)O)O)O)C)C '
               'NAME: 14-hydroxyisochainin REASON: WRONGLY CLASSIFIED Contains '
               'a long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               '[H+].[H]C(=C([H])C1=[N+](CCCCS([O-])(=O)=O)c2ccc(cc2C1(C)C)C(O)=O)C1=C(Cl)C(CCC1)=C([H])C([H])=C1N(CCCCS([O-])(=O)=O)c2ccc(cc2C1(C)C)C(O)=O '
               'NAME: NIR-820 dye REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'C[C@@H]1[C@H]([C@@H]([C@@H]([C@@H](O1)OC2CC(C(C(CC(=O)CC(C(CCC(CC(CC(CC(=O)OC(C(C(C(C=CC=CCCC=CC=CC=CC=C2)C)O)C)C)O)O)O)O)O)O)C(=O)O)O)O)N)O '
               'NAME: '
               '20-[[(2R,3S,4S,5S,6R)-4-amino-3,5-dihydroxy-6-methyl-2-oxanyl]oxy]-4,6,8,11,12,16,18,36-octahydroxy-35,37,38-trimethyl-2,14-dioxo-1-oxacyclooctatriaconta-21,23,25,27,31,33-hexaene-17-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains a long conjugated '
               'polyene chain with ≥4 C=C bonds, sufficient carbon scaffold '
               'with ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'O=C1N2[C@H](C(=O)N([C@H](C(=O)N[C@@H](C)C(N3[C@H](C(OC[C@@H]1NC(=O)[C@@H](NC(=O)/C=C/C=C/C=C/C=C/C=C/C(=O)NC4=C(O)CCC4=O)CC5=CC=CC=C5)=O)C[C@@H](C)C3)=O)C)C)CCC2 '
               'NAME: Enopeptin A REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'CCC(C)C1OC(=O)\\C=C\\C=C\\C=C/C=C/C=C/CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)\\C=C\\C1C '
               'NAME: reedsmycin B REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'P(=O)(OP(=O)(O)O)(O[C@@H]1C(C2(O[C@H]([C@@H](C)[C@@H](C2)O)C/C=C/C=3N=C([C@H](CCNC(=O)[C@@H](O)[C@@H](O)[C@@H](N(C)C)COC)C)OC3)O[C@@H]1[C@@H](OC)C[C@H](O)[C@@H]([C@H](O)[C@@H](/C=C(/C(=C/C=C/C(=C\\[N+]#[C-])/C)/C)\\C)C)C)(C)C)O '
               'NAME: Phosphocalyculin A REASON: WRONGLY CLASSIFIED Contains a '
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'O1[C@]2(C(C(C[C@H](O)C2)(C)C)=C[C@H]1\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C#CC=3C(C[C@H](O)CC3C)(C)C)/C)/C)C '
               'NAME: Diadinochrome A REASON: WRONGLY CLASSIFIED Contains a '
               'long conjugated polyene chain with ≥4 C=C bonds, sufficient '
               'carbon scaffold with ring(s), and oxygen functionalities '
               'consistent with xanthophylls\n'
               ' * SMILES: '
               'O=C(OC1OC(C(O)C(C1OC(=O)CCCCCCCCCC=CCCCCCC)O)CO)C(=CC=CC(=CC=CC(=CC=CC=C(C=CC=C(C=CC=C(C(=O)O)C)C)C)C)C)C '
               'NAME: '
               '4-[2-O-11Z-octadecenoyl-beta-glucopyranosyl]-4,4′-diapolycopene-4,4′-dioic '
               'acid REASON: WRONGLY CLASSIFIED Contains a long conjugated '
               'polyene chain with ≥4 C=C bonds, sufficient carbon scaffold '
               'with ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'O1C2(C(C(CC(O)C2)(C)C)=CC1\\C(\\C)=C/C=C/C(/C)=C/C=C/C=C(\\C)/C=C/C=C(/C)\\C=O)C '
               "NAME: 5,8-Epoxy-5,8-dihydro-3-hydroxy-8'-apo-b,y-carotenal "
               'REASON: WRONGLY CLASSIFIED Contains a long conjugated polyene '
               'chain with ≥4 C=C bonds, sufficient carbon scaffold with '
               'ring(s), and oxygen functionalities consistent with '
               'xanthophylls\n'
               ' * SMILES: '
               'O1[C@@]([C@H](C/C(=C/[C@H]([C@H](O)C[C@H](O)C)C)/C)C)(CC=C(C[C@@H]([C@@H](OC(=O)/C=C/C(=C/C(=C/C(=C/C[C@H](O)C[C@H](O)C)/C)/C)/C)CCCC1=O)C)C)[H] '
               'NAME: Mycolactone F REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O1C2(O)CC(O)C(C1CC(O[C@H]3O[C@H]([C@H](O)[C@@H](N)[C@H]3O)C)C=CC=CC=CC=CC=CC=CC=CC(C(OC(=O)CC(O)CC(=O)CC(O)CC(O)CC(O)CC(O)C2)C(CCC(O)CC(=O)C4=CC=C(N)C=C4)C)C)C(O)=O '
               'NAME: Partricin REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1OC(C(C=CC=CC=CC=CC=CC(O)C(C(CC(CC(CCCC(CC(C1C)O)O)O)O)O)C)C)C(C)C '
               'NAME: Takanawaene C REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O([C@H]1CC(C(=C(C1=O)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=2C(C[C@H](O)CC2C)(C)C)\\C)\\C)(C)C)C3OC(C(O)C(O)C3O)CO '
               'NAME: adonixanthin 3-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains a long conjugated polyene chain with ≥4 C=C bonds, '
               'sufficient carbon scaffold with ring(s), and oxygen '
               'functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'O=C(OC1=C(C(O)=CC(=C1)CCCCCCC)CCCCCC)/C=C/C=C/C=C/C=C/C=C/C=C/C2=CC(OC)=CC=C2 '
               'NAME: Arcuflavin B REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](C=CC=CC=CC=CC=C[C@@H](O)[C@@H]([C@@H](C[C@@H](CCC[C@@H](C[C@@H](C[C@@H]([C@H]1C)O)O)O)O)O)C(=O)O)C)CC '
               'NAME: Strevertene C REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@@H](O)C=CC=CC=CC=CC=C([C@H](O)C[C@@H](C[C@@H](C[C@@H](C[C@@H](C[C@H](C[C@H]([C@H]1CCCC)O)O)O)O)O)O)C)C '
               'NAME: Isochainin REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C(O)CC(OC)/C=C/C=C/C=C/C=C/C=C/C(C(O)C(C1OC2(OC(C(C)C(C2)OC)C(C(O)C(C/C(=C/C)/C)C)C)C(O)CC1C)C)C '
               'NAME: Spirangiene A REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O[C@H]1CCC[C@@H](O)C[C@@H](O)[C@H]([C@H](O)C=CC=CC=CC=CC=C[C@@H]([C@H](OC(=O)[C@@H]([C@@H](O)C[C@@H](O)C1)C)C)C)C(O)=O '
               'NAME: Strevertene A REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1OC(C(C=CC=CC=CC=CC=CC=CC=CC(OC2O[C@@H]([C@@H](O)[C@@H]([C@@H]2O)N)C)CC3OC(CC(CC(CC(CCCC(CC(C1)O)O)O)O)O)(O)CC(O)C3C(=O)O)C)C(CCC(O)CC(=O)C4=CC=C(N)C=C4)C '
               'NAME: 3874 H1 REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O(C(=O)/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(\\C=C\\C=1C(CCCC1C)(C)C)/C)\\C)/C)/C)CC '
               'NAME: all-trans-Carophyll yellow REASON: WRONGLY CLASSIFIED '
               'Contains a long conjugated polyene chain with ≥4 C=C bonds, '
               'sufficient carbon scaffold with ring(s), and oxygen '
               'functionalities consistent with xanthophylls\n'
               ' * SMILES: '
               'O=C1OC(C(CCC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(CC2(OC(CC=CC=CC=CC=CC=C1C)CC(O)C2)O)O)C)C(C)C '
               'NAME: Flavomycoin REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@@H](C=CC=CC=CC=CC=CC=CC=C[C@H](O[C@H]2O[C@@H]([C@H](O)[C@H]([C@H]2O)N)C)C[C@@H]3O[C@@](C[C@@H](C[C@@H](C[C@@H](C[C@@H](CC(C[C@H](C1)O)=O)O)O)O)O)(O)C[C@H](O)[C@H]3C(=O)O)C)[C@@H](CC[C@@H](O)CC(=O)C4=CC=C(N)C=C4)C '
               'NAME: Partricin B REASON: WRONGLY CLASSIFIED Contains a long '
               'conjugated polyene chain with ≥4 C=C bonds, sufficient carbon '
               'scaffold with ring(s), and oxygen functionalities consistent '
               'with xanthophylls\n'
               'False negatives: SMILES: '
               'COC(C)(C)C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: spheroidene REASON: MISSED No ring structures found; '
               'typically xanthophylls contain at least one cyclic endgroup\n'
               ' * SMILES: '
               'COC(C)(C)C(=O)\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C(=O)C(C)(C)OC '
               "NAME: 2,2'-dioxospirilloxanthin REASON: MISSED No ring "
               'structures found; typically xanthophylls contain at least one '
               'cyclic endgroup\n'
               ' * SMILES: '
               'C(=C(/CCC=C(C)C)\\C)\\CC/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/C(C(OC)(C)C)(O)O)\\C)\\C)\\C)/C)/C '
               'NAME: 2,2-dihydroxyspheroidene REASON: MISSED No ring '
               'structures found; typically xanthophylls contain at least one '
               'cyclic endgroup\n'
               ' * SMILES: '
               'COC(C)(C)CCC\\C(C)=C\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(/C)\\C=C\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: 3,4-dihydrospheroidene REASON: MISSED No ring structures '
               'found; typically xanthophylls contain at least one cyclic '
               'endgroup\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(/C)\\C=C\\C=C(/C)\\C=C\\C=C(/C)CCCC(C)(C)O '
               'NAME: chloroxanthin REASON: MISSED No ring structures found; '
               'typically xanthophylls contain at least one cyclic endgroup\n'
               ' * SMILES: '
               'COC(C)(C)C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C=C(/C)CCCC(C)(C)O '
               'NAME: Rhodovibrin REASON: MISSED No ring structures found; '
               'typically xanthophylls contain at least one cyclic endgroup\n'
               ' * SMILES: '
               'C\\C(CO)=C/CC\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CO '
               'NAME: lycophyll REASON: MISSED No ring structures found; '
               'typically xanthophylls contain at least one cyclic endgroup\n'
               ' * SMILES: '
               'COC(C)(C)C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CCCC(C)(C)O '
               'NAME: Hydroxyspheroidene REASON: MISSED No ring structures '
               'found; typically xanthophylls contain at least one cyclic '
               'endgroup\n'
               ' * SMILES: '
               'OC(C/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/C(=O)C(O)(C)C)\\C)\\C)\\C)/C)(C)C '
               "NAME: 1,1'-(OH)2-2-keto-3,4,3',4'-tetradehydrolycopene REASON: "
               'MISSED No ring structures found; typically xanthophylls '
               'contain at least one cyclic endgroup\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\[C@H](O)C(C)(C)O)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C=C(C)/C=C/[C@H](O)C(C)(C)O '
               "NAME: (2S,2'S)-Oscillol REASON: MISSED No ring structures "
               'found; typically xanthophylls contain at least one cyclic '
               'endgroup\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Too few carbon atoms (26); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Too few carbon atoms (27); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Too few carbon atoms (8); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Too few carbon atoms (12); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Too few carbon atoms (14); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No long conjugated polyene '
                                               'chain found; expected a '
                                               'conjugated chain with at least '
                                               '4 consecutive C=C bonds'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No long conjugated polyene '
                                               'chain found; expected a '
                                               'conjugated chain with at least '
                                               '5 consecutive C=C bonds '
                                               '(typical for acyclic '
                                               'carotenoids)'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Too few carbon atoms (9); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Too few carbon atoms (15); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Too few carbon atoms (28); '
                                               'expected at least 30 for a '
                                               'carotenoid backbone'}],
    'sample_false_negatives': [   {   'smiles': 'CC(\\C=C\\C=C(/C)C(O)=O)=C/C=C/C=C(C)/C=C/C=C(\\C)C(O)=O',
                                      'name': 'crocetin',
                                      'reason': 'Too few carbon atoms (20); '
                                                'expected at least 30 for a '
                                                'carotenoid backbone'},
                                  {   'smiles': 'C\\C(C=O)=C/C=C/C=C(\\C)/C=C/C=C(\\C)C=[C@]=C1C(C)(C)C[C@H](O)C[C@@]1(C)O',
                                      'name': "(3S,5R,6R)-3,5-dihydroxy-6,7-didehydro-5,6-dihydro-12'-apo-beta-caroten-12'-al",
                                      'reason': 'Too few carbon atoms (25); '
                                                'expected at least 30 for a '
                                                'carotenoid backbone'},
                                  {   'smiles': 'C(\\C=C\\C(OC)=O)(=C\\C=C\\C(=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C(=O)O)/C)/C)\\C)/C',
                                      'name': 'bixin',
                                      'reason': 'Too few carbon atoms (25); '
                                                'expected at least 30 for a '
                                                'carotenoid backbone'},
                                  {   'smiles': 'C\\C(C=O)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/[C@@]12O[C@]1(C)C[C@@H](O)CC2(C)C',
                                      'name': "(3S,5R,6S)-5,6-epoxy-3-hydroxy-5,6-dihydro-12'-apo-beta-caroten-12'-al",
                                      'reason': 'Too few carbon atoms (25); '
                                                'expected at least 30 for a '
                                                'carotenoid backbone'},
                                  {   'smiles': '[H]C(=O)\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C1=C(C)CCCC1(C)C',
                                      'name': "14'-apo-beta-carotenal",
                                      'reason': 'Too few carbon atoms (22); '
                                                'expected at least 30 for a '
                                                'carotenoid backbone'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'One likely issue with the previous algorithm was that it '
                 '“hard‐coded” several features that many xanthophylls do '
                 'possess but are not strictly universal. In particular, '
                 'requiring at least one ring (to catch cyclic endgroups) '
                 'rejected bona fide acyclic xanthophylls (e.g. spheroidene '
                 'and related compounds). Also, the SMARTS for a conjugated '
                 'polyene chain was written in a “one‐size‐fits‐all” way. In '
                 'reality, cyclic xanthophylls tend to have a somewhat shorter '
                 'conjugated chain while acyclic ones often require a longer '
                 'chain to compensate for the absent ring(s).\n'
                 '\n'
                 'To improve classification we now:\n'
                 '\u2003• Still require the molecule to be oxygenated and to '
                 'have a large carbon scaffold (at least 30 carbons).\n'
                 '\u2003• Check the molecular weight remains high (≥400 Da).\n'
                 '\u2003• Compute whether the molecule contains any rings.\n'
                 '\u2003• If rings are found (a cyclic xanthophyll candidate), '
                 'we search for a conjugated segment defined by four '
                 'consecutive C=C bonds (SMARTS "C=C-C=C-C=C-C=C"). Otherwise '
                 '(an acyclic candidate) we require a longer conjugated chain '
                 'and use a pattern with five consecutive double bonds '
                 '("C=C-C=C-C=C-C=C-C=C").\n'
                 '\n'
                 'This adjustment should capture more true xanthophylls, while '
                 'hopefully reducing both false positives and false '
                 'negatives.\n'
                 '\n'
                 'Below is the complete Python code contained within a single '
                 'code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 174,
    'num_false_positives': 338,
    'num_true_negatives': 141783,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.33984375,
    'recall': 0.9720670391061452,
    'f1': 0.5036179450072359,
    'accuracy': 0.9975895994378075,
    'negative_predictive_value': 0.9999647360848591}