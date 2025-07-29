"""
Classifies: CHEBI:27208 unsaturated fatty acid
"""
"""
Classifies: Unsaturated Fatty Acid
Definition: An unsaturated fatty acid is defined here as an acyclic molecule that:
  1. Contains exactly one terminal free carboxylic acid group (i.e. –C(=O)[OH]). The carboxyl carbon
     must be acyclic and only bonded to exactly one carbon (which is non‐aromatic).
  2. Contains only C, H, and O atoms.
  3. Contains at least one C=C or C#C bond (unsaturation) outside of the carboxyl group.
  4. Has a minimum chain size (at least 5 carbon atoms).
By enforcing that the acid group is a free –COOH (and not part of an ester or other motifs),
and by limiting the allowed elements, many false positives (e.g. phospholipids or acetates) are avoided.
"""

from rdkit import Chem

def is_unsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is an unsaturated fatty acid based on its SMILES string.
    Criteria:
      1. The molecule must be acyclic.
      2. The molecule must contain only C, H, and O atoms.
      3. The molecule must have exactly one terminal free carboxylic acid group.
         (This is defined by a [CX3](=O)[OH] pattern on a carbon that is not in a ring and that
         has exactly one carbon neighbor (which must be non-aromatic)).
      4. The molecule must contain at least one carbon–carbon double or triple bond (unsaturation)
         outside of the carboxyl group.
      5. As a simple size check, the overall number of carbons should be at least 5.
    
    Args:
        smiles (str): SMILES string representing the molecule.
    
    Returns:
        bool: True if the molecule is classified as an unsaturated fatty acid; False otherwise.
        str: A reason explaining the classification decision.
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject molecules that contain rings – fatty acids are defined here as acyclic.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains ring(s); fatty acids are typically acyclic"
    
    # Reject molecules containing atoms other than C, H, and O.
    allowed = {1, 6, 8}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed:
            return False, "Molecule contains atoms other than C, H, and O; not a typical fatty acid"
    
    # Look for terminal free carboxylic acid groups.
    # Use SMARTS that strictly requires a free carboxyl: –C(=O)[OH]
    acid_smarts = "[CX3](=O)[OH]"
    acid_query = Chem.MolFromSmarts(acid_smarts)
    acid_matches = mol.GetSubstructMatches(acid_query)
    
    terminal_acid_matches = []
    acid_bond_idxs = set()  # store indices of bonds that are part of the acid group
    for match in acid_matches:
        # match[0] is the carboxyl carbon for the acid group
        acid_c = mol.GetAtomWithIdx(match[0])
        if acid_c.IsInRing():
            continue
        # Count carbon neighbors of the acid carbon (ignoring oxygens)
        carbon_neighbors = [nb for nb in acid_c.GetNeighbors() if nb.GetAtomicNum() == 6]
        if len(carbon_neighbors) == 1 and not carbon_neighbors[0].GetIsAromatic():
            terminal_acid_matches.append(match)
            # Record the bonds that form the carboxyl group so we can exclude them
            for atom_idx in match:
                atom = mol.GetAtomWithIdx(atom_idx)
                for bond in atom.GetBonds():
                    # If both bond endpoints are in the current acid match, record it.
                    if bond.GetBeginAtomIdx() in match and bond.GetEndAtomIdx() in match:
                        acid_bond_idxs.add(bond.GetIdx())
    
    if len(terminal_acid_matches) != 1:
        return False, ("Molecule does not have exactly one terminal free carboxylic acid group "
                       f"(found {len(terminal_acid_matches)}); not classified as a fatty acid")
    
    # Check overall carbon count.
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 5:
        return False, "Too few carbons to be a fatty acid"
    
    # Look for unsaturation (C=C or C#C bonds) outside of the carboxyl group.
    has_unsaturation = False
    unsat_types = set()
    for bond in mol.GetBonds():
        # Skip bonds that are part of the terminal acid group
        if bond.GetIdx() in acid_bond_idxs:
            continue
        if bond.GetBondType() == Chem.BondType.DOUBLE or bond.GetBondType() == Chem.BondType.TRIPLE:
            a1 = bond.GetBeginAtom()
            a2 = bond.GetEndAtom()
            # We only count if both atoms are carbon.
            if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 6:
                has_unsaturation = True
                if bond.GetBondType() == Chem.BondType.DOUBLE:
                    unsat_types.add("double")
                else:
                    unsat_types.add("triple")
    
    if not has_unsaturation:
        return False, ("Molecule appears to have a free carboxylic acid group but does not contain "
                       "any carbon–carbon double or triple bonds (unsaturation)")
    
    # Prepare a description of the unsaturation found.
    if "double" in unsat_types and "triple" in unsat_types:
        unsat_detail = "carbon–carbon double and triple bond(s)"
    elif "double" in unsat_types:
        unsat_detail = "carbon–carbon double bond(s)"
    else:
        unsat_detail = "carbon–carbon triple bond(s)"
        
    return True, f"Molecule is a fatty acid and contains unsaturation: {unsat_detail}"

# Example usage:
if __name__ == "__main__":
    # Test with trans-vaccenic acid, one of the provided examples.
    test_smiles = "CCCCCC\\C=C\\CCCCCCCCCC(O)=O"
    result, reason = is_unsaturated_fatty_acid(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27208',
                          'name': 'unsaturated fatty acid',
                          'definition': 'Any fatty acid containing at least '
                                        'one C=C or C#C bond.',
                          'parents': ['CHEBI:35366'],
                          'xrefs': [   'LIPID_MAPS_class:LMFA0103',
                                       'PMID:5322381'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 91,
                           'log_lines_of_code': 4.51085950651685,
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
                                                 2,
                                                 3,
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
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
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
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'append',
                                                 'GetEndAtomIdx',
                                                 'GetRingInfo',
                                                 'IsInRing',
                                                 'GetAtomicNum',
                                                 'GetBeginAtom',
                                                 'GetSubstructMatches',
                                                 'NumRings',
                                                 'GetBondType',
                                                 'GetAtoms',
                                                 'MolFromSmiles',
                                                 'GetIdx',
                                                 'add',
                                                 'GetBeginAtomIdx',
                                                 'GetBonds',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'GetEndAtom',
                                                 'GetAtomWithIdx',
                                                 'GetIsAromatic'],
                           'methods_called_count': 20,
                           'smarts_strings': ['acid_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_unsaturated_fatty_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains ring(s); '
                                          'fatty acids are typically acyclic"',
                                          'False, "Molecule contains atoms '
                                          'other than C, H, and O; not a '
                                          'typical fatty acid"',
                                          'False, ("Molecule does not have '
                                          'exactly one terminal free '
                                          'carboxylic acid group "',
                                          'False, "Too few carbons to be a '
                                          'fatty acid"',
                                          'False, ("Molecule appears to have a '
                                          'free carboxylic acid group but does '
                                          'not contain "',
                                          'True, f"Molecule is a fatty acid '
                                          'and contains unsaturation: '
                                          '{unsat_detail}"'],
                           'returns_count': 7,
                           'complexity': 7.7021719013033705},
    'message': '\n'
               'Attempt failed: F1 score of 0.31686239751828055 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CC(C)=CCCC(C)=CCCC(C)=CC(O)=O NAME: '
               'farnesoic acid REASON: CORRECT Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: OC(=O)C\\C=C\\C=C/C=C=CC#CC#C NAME: mycomycin '
               'REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double and triple bond(s)\n'
               ' * SMILES: CCCCCC\\C=C\\CCCCCCCCCC(O)=O NAME: trans-vaccenic '
               'acid REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CC(C)=CC(O)=O NAME: 3-methylbut-2-enoic acid '
               'REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: C(=C/CCCCC)\\C=C\\C(O)=O NAME: '
               '(2E,4E)-deca-2,4-dienoic acid REASON: CORRECT Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: OC(CCCCCCCC(O)=O)C=CC(O)C(O)CC=CCC NAME: '
               '9,12,13-Trihydroxyoctadeca-10,15-dienoic acid REASON: CORRECT '
               'Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCCC[C@@H](O)C\\C=C\\CCCCCCCC(O)=O NAME: '
               'ricinelaidic acid REASON: CORRECT Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCC(O)=O '
               'NAME: (12Z,15Z,18Z,21Z,24Z,27Z)-triacontahexaenoic acid '
               'REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CCCC\\C=C/C(O)=O NAME: cis-2-heptenoic acid REASON: '
               'CORRECT Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'OC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C=C\\[C@H](CCCCC)O)=O NAME: '
               '(4Z,7Z,10Z,13Z,15E,17S)-17-hydroxydocosapentaenoic acid '
               'REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'CCC(O)\\C=C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCC(O)=O NAME: '
               '20-HDoHE REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: [H]C(C)=CCCC([H])=CCCC([H])=CC(O)=O NAME: '
               'dodeca-2,6,10-trienoic acid REASON: CORRECT Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: '
               'C(CC/C=C\\C[C@H](O)/C=C/C=C/C=C\\[C@H](C/C=C\\C/C=C\\CC)O)(O)=O '
               'NAME: '
               '(7S,14S)-dihydroxy-(4Z,8E,10E,12Z,16Z,19Z)-docosahexaenoic '
               'acid REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: O[C@H](C/C=C\\CCCC(O)=O)/C=C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: 8R-HEPE REASON: CORRECT Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: OC(=O)CCCCCCCC/C=C/C=C/C=C/CCC NAME: '
               '10,12,14-octadecatrienoic acid REASON: CORRECT Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: OC(=O)CCCCC/C=C\\C=C/C/C=C\\CCCCC NAME: '
               '7Z,9Z,12Z-octadecatrienoic acid REASON: CORRECT Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: OC(=O)CCCCCCC\\C=C\\C=C\\CCCCCC NAME: '
               '(9E,11E)-octadecadienoic acid REASON: CORRECT Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/[C@H](O)[C@H](O)CCCCCC(O)=O '
               'NAME: (9Z,12Z,15Z)-(7S,8S)-Dihydroxyoctadeca-9,12,15-trienoic '
               'acid REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCCCCC[C@H](OO)\\C=C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '12(S)-HPE(5,8,10)TrE REASON: CORRECT Molecule is a fatty acid '
               'and contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'CCCCC[C@H](O)CC\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O NAME: '
               '13,14-dihydrolipoxin A4 REASON: CORRECT Molecule is a fatty '
               'acid and contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C=C/C(O)CCCC(O)=O NAME: '
               '5-HETE REASON: CORRECT Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C[C@H](OO)\\C=C\\C=C/CCCC(O)=O '
               'NAME: 9(S)-HPETE REASON: CORRECT Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCC(O)=O '
               'NAME: (9Z,12Z,15Z,18Z,21Z)-tetracosapentaenoic acid REASON: '
               'CORRECT Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: C([C@H](CC/C=C/C=C\\[C@H](CCCC(O)=O)O)O)/C=C\\CCCCC '
               'NAME: 10,11-dihydroleukotriene B4 REASON: CORRECT Molecule is '
               'a fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@H](O)\\C=C\\C=C\\C=C\\[C@@H](O)CCCC(O)=O NAME: '
               'Delta(6)-trans-12-epi-leukotriene B4 REASON: CORRECT Molecule '
               'is a fatty acid and contains unsaturation: carbon-carbon '
               'double bond(s)\n'
               'False positives: SMILES: O(CCCCCC/C=C\\CC)C(=O)C NAME: '
               '7Z-Decenyl acetate REASON: WRONGLY CLASSIFIED Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: '
               'O=C(O)C(O)C(O)CC(O)/C=C/CC(O)/C=C/CC(O)/C(=C/C(C(O)/C(=C/C(=C\\C(CC(CC)C)C)/CO)/C)C)/C '
               'NAME: Arthrinic acid REASON: WRONGLY CLASSIFIED Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COCCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(O-18:0/18:4(6Z,9Z,12Z,15Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: OC(=O)\\C=C\\C=C\\C=C\\C=C\\C=C\\CCCCCCCCCCC NAME: '
               'Docosa-2,4,6,8,10-pentaenoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: O(CCCCC\\C=C\\CCCCCCC)C(=O)C NAME: 6E-Tetradecenyl '
               'acetate REASON: WRONGLY CLASSIFIED Molecule is a fatty acid '
               'and contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'O(CCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(=O)CCCCCCC/C=C\\CCCCCC '
               'NAME: Linolenyl palmitatoleate REASON: WRONGLY CLASSIFIED '
               'Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCC([O-])=O NAME: '
               '(13Z,16Z,19Z,22Z,25Z)-octacosapentaenoate REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'P(OC[C@@H](COC(CCCCCCCCC/C=C\\CCCCCC)=O)O/C=C\\CCCCCC/C=C\\CCCCCCCC)(=O)(OCC[NH3+])[O-] '
               'NAME: PE(18:1(11Z)/P-18:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: O[C@@H]([C@@H](C)/C=C/C(O)=O)CC NAME: Mycinonic '
               'acid I REASON: WRONGLY CLASSIFIED Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: O(C(=O)CC(C)C)C/C=C/C#CC#C/C=C\\C NAME: '
               '(2E,8Z)-Decadiene-4,6-diyn-1-yl 3-methylbutanoate REASON: '
               'WRONGLY CLASSIFIED Molecule is a fatty acid and contains '
               'unsaturation: carbon-carbon double and triple bond(s)\n'
               ' * SMILES: O[C@H](CCC(=O)CC(O)=O)C/C=C\\CCCCC NAME: '
               '(6R,8Z)-6-Hydroxy-3-oxotetradecenoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCC\\C=C/CCCCCCCC([O-])=O NAME: '
               '(9Z)-pentadecenoate REASON: WRONGLY CLASSIFIED Molecule is a '
               'fatty acid and contains unsaturation: carbon-carbon double '
               'bond(s)\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])CCCCCCCCCC/C=C\\CCCCCCCC '
               'NAME: PC(o-20:1(11Z)/20:4(8Z,11Z,14Z,17Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: C[C@@H](O)CC[C@H](CC([O-])=O)C(C)=C NAME: '
               '(3R,6R)-6-hydroxy-3-isopropenylheptanoate REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: [H]C(=O)\\C=C\\C=C(/O)C(O)=O NAME: '
               '(2Z,4E)-2-hydroxy-6-oxohexa-2,4-dienoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCCCCCCC\\C=C/CCCCCCCCCC([O-])=O NAME: cetoleate '
               'REASON: WRONGLY CLASSIFIED Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(P-20:0/20:4(5Z,8Z,11Z,14Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: OC(=O)CCC/C=C/CC NAME: trans-delta-octenoic acid '
               'REASON: WRONGLY CLASSIFIED Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(OCC(O)CO)(O)=O '
               'NAME: LPG 20:2 REASON: WRONGLY CLASSIFIED Molecule is a fatty '
               'acid and contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'O[C@@H](C/C=C\\CCCCC)/C=C/C=C\\C/C=C\\CCCC(=O)NCC(O)=O NAME: '
               '12-HETE-Gly REASON: WRONGLY CLASSIFIED Molecule is a fatty '
               'acid and contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CC(=CCCC(=CCCC(=CCSCC(=O)O)C)C)C NAME: '
               '2-(3,7,11-trimethyldodeca-2,6,10-trienylthio)acetic acid '
               'REASON: WRONGLY CLASSIFIED Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: C\\C=C/CC(=O)C(O)=O NAME: cis-2-oxohex-4-enoic acid '
               'REASON: WRONGLY CLASSIFIED Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)CC NAME: '
               'Dihomo-gamma-linolenic acid ethyl ester REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               ' * SMILES: '
               'P(OC[C@H](O)COCC(OC)CCC/C=C\\CCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: 1-(2-methoxy-6Z-heptadecenyl)-sn-glycero-3-phosphoserine '
               'REASON: WRONGLY CLASSIFIED Molecule is a fatty acid and '
               'contains unsaturation: carbon-carbon double bond(s)\n'
               ' * SMILES: CCCCCC=CCC=CCCCCCCCC(=O)NCC(=O)O NAME: '
               '2-(1-oxooctadeca-9,12-dienylamino)acetic acid REASON: WRONGLY '
               'CLASSIFIED Molecule is a fatty acid and contains unsaturation: '
               'carbon-carbon double bond(s)\n'
               'False negatives: SMILES: C(C(=O)OC)[C@@H]1[C@H](C(CC1)=O)CCCCC '
               'NAME: Methyl dihydrojasmonate REASON: MISSED Molecule contains '
               'ring(s); fatty acids are typically acyclic\n'
               ' * SMILES: C(C(O)=O)CCCC/C=C\\C/C=C\\C/C=C\\CC1C(C/C=C\\CC)O1 '
               'NAME: (7Z,10Z,13Z,19Z)-16,17-epoxydocosatetraenoic acid '
               'REASON: MISSED Molecule contains ring(s); fatty acids are '
               'typically acyclic\n'
               ' * SMILES: C(\\CC)=C\\C/C=C\\CC1C(C/C=C\\C/C=C\\CCCC(=O)O)O1 '
               'NAME: (5Z,8Z,14Z,17Z)-11,12-epoxyicosatetraenoic acid REASON: '
               'MISSED Molecule contains ring(s); fatty acids are typically '
               'acyclic\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCC[C@H]1CCC=C1 NAME: '
               '(S)-chaulmoogric acid REASON: MISSED Molecule contains '
               'ring(s); fatty acids are typically acyclic\n'
               ' * SMILES: '
               'S([C@H]([C@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\C/C=C\\CC)C[C@H](N)C(=O)NCC(O)=O '
               'NAME: Leukotriene D5 REASON: MISSED Molecule does not have '
               'exactly one terminal carboxylic acid group (found 2), so not a '
               'fatty acid\n'
               ' * SMILES: '
               'C[C@H](C\\C=C\\C(\\C)=C\\[C@@H](C)C(=O)[C@@H](C)[C@H](O)[C@@H](C)C\\C(C)=C\\C(O)=O)\\C=C(/C)\\C=C\\[C@@H]1OC(=O)C=C[C@@H]1C '
               'NAME: leptomycin A REASON: MISSED Molecule contains ring(s); '
               'fatty acids are typically acyclic\n'
               ' * SMILES: CCC1OC1C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '17(18)-EpETE REASON: MISSED Molecule contains ring(s); fatty '
               'acids are typically acyclic\n'
               ' * SMILES: CC\\C=C/C[C@H]1[C@@H](CCCCCCCC(O)=O)C=CC1=O NAME: '
               '(15Z)-12-oxophyto-10,15-dienoic acid REASON: MISSED Molecule '
               'contains ring(s); fatty acids are typically acyclic\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2OCCCCCCCC\\C=C/CCCCCCCC([O-])=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: (9Z)-18-hydroxyoctadec-9-enoate 18-O-sophoroside REASON: '
               'MISSED Molecule contains ring(s); fatty acids are typically '
               'acyclic\n'
               ' * SMILES: C(CCCCCCC/C=C\\C([C@H]1[C@H](CCCCC)O1)O)(=O)O NAME: '
               '11-hydroxy-(12S,13S)-epoxy-(9Z)-octadecenoic acid REASON: '
               'MISSED Molecule contains ring(s); fatty acids are typically '
               'acyclic\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Molecule does not have exactly '
                                               'one terminal free carboxylic '
                                               'acid group (found 3); not '
                                               'classified as a fatty acid'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O; not a '
                                               'typical fatty acid'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Molecule contains ring(s); '
                                               'fatty acids are typically '
                                               'acyclic'}],
    'sample_false_negatives': [   {   'smiles': 'C(C(=O)OC)[C@@H]1[C@H](C(CC1)=O)CCCCC',
                                      'name': 'Methyl dihydrojasmonate',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'C(C(O)=O)CCCC/C=C\\C/C=C\\C/C=C\\CC1C(C/C=C\\CC)O1',
                                      'name': '(7Z,10Z,13Z,19Z)-16,17-epoxydocosatetraenoic '
                                              'acid',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'C(\\CC)=C\\C/C=C\\CC1C(C/C=C\\C/C=C\\CCCC(=O)O)O1',
                                      'name': '(5Z,8Z,14Z,17Z)-11,12-epoxyicosatetraenoic '
                                              'acid',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'OC(=O)CCCCCCCCCCCC[C@H]1CCC=C1',
                                      'name': '(S)-chaulmoogric acid',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'S([C@H]([C@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\C/C=C\\CC)C[C@H](N)C(=O)NCC(O)=O',
                                      'name': 'Leukotriene D5',
                                      'reason': 'Molecule contains atoms other '
                                                'than C, H, and O; not a '
                                                'typical fatty acid'},
                                  {   'smiles': 'C[C@H](C\\C=C\\C(\\C)=C\\[C@@H](C)C(=O)[C@@H](C)[C@H](O)[C@@H](C)C\\C(C)=C\\C(O)=O)\\C=C(/C)\\C=C\\[C@@H]1OC(=O)C=C[C@@H]1C',
                                      'name': 'leptomycin A',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'CCC1OC1C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O',
                                      'name': '17(18)-EpETE',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'CC\\C=C/C[C@H]1[C@@H](CCCCCCCC(O)=O)C=CC1=O',
                                      'name': '(15Z)-12-oxophyto-10,15-dienoic '
                                              'acid',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2OCCCCCCCC\\C=C/CCCCCCCC([O-])=O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '(9Z)-18-hydroxyoctadec-9-enoate '
                                              '18-O-sophoroside',
                                      'reason': 'Molecule contains ring(s); '
                                                'fatty acids are typically '
                                                'acyclic'},
                                  {   'smiles': 'CCCC\\C(Br)=C\\C(O)=O',
                                      'name': '(2Z)-3-bromohept-2-enoic acid',
                                      'reason': 'Molecule contains atoms other '
                                                'than C, H, and O; not a '
                                                'typical fatty acid'}],
    'attempt': 3,
    'reasoning': 'Below is our revised solution. In our reasoning we noted '
                 'that the previous approach sometimes “matched” an acid group '
                 'in an ester or in other functional groups. We now narrow the '
                 'acid‐SMARTS pattern to a true –COOH by requiring a hydroxyl '
                 '(with an explicit hydrogen) on the acid carbon. We also '
                 'reject molecules that have any atoms outside the allowed set '
                 '(C, H and O), which helps remove many phospholipids and '
                 'other derivatives. Lastly, we “tag” the acid group bonds so '
                 'that unsaturation is only searched for in the remainder of '
                 'the molecule. (See comments in the code for details.)\n'
                 '\n'
                 'Below is the complete Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 704,
    'num_false_positives': 917,
    'num_true_negatives': 140540,
    'num_false_negatives': 139,
    'num_negatives': None,
    'precision': 0.4342998149290561,
    'recall': 0.8351126927639383,
    'f1': 0.5714285714285715,
    'accuracy': 0.9925790583274772,
    'negative_predictive_value': 0.999011934972526}