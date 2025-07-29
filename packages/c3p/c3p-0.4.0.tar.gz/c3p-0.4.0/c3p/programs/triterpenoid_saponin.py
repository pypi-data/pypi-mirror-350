"""
Classifies: CHEBI:61778 triterpenoid saponin
"""
"""
Classifies: triterpenoid saponin
Definition: A terpene glycoside in which the terpene moiety is a triterpenoid.
That is, the molecule must have at least one sugar (glycoside) unit and an aglycone part with roughly 30 carbon atoms
and several fused (non‐aromatic) rings.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import SanitizeFlags

def is_triterpenoid_saponin(smiles: str):
    """
    Determines if a molecule is a triterpenoid saponin based on its SMILES string.
    
    Heuristic:
      1. The input SMILES must be valid.
      2. At least one sugar moiety is present. We identify sugar rings as 5- or 6-membered rings 
         that contain exactly one oxygen and the remaining atoms as carbons.
      3. Remove the atoms belonging to sugar rings. The largest remaining fragment is considered the aglycone.
      4. The aglycone should have between 25 and 40 carbon atoms (typical for triterpenoids).
      5. The aglycone must contain at least 4 rings and none of these rings should be aromatic.
      6. The overall molecular weight should be > 500 Da.
      
    Args:
      smiles (str): SMILES string of the molecule.
      
    Returns:
      bool: True if the molecule is classified as a triterpenoid saponin, False otherwise.
      str: Explanation for the classification decision.
    """
    # Step 1. Parse the SMILES without immediate sanitization.
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        if mol is None:
            return False, "Invalid SMILES string."
    except Exception as e:
        return False, f"Error parsing SMILES: {e}"

    # Try to sanitize while skipping kekulization
    try:
        # Skip kekulization to avoid issues with problematic aromatic assignments.
        Chem.SanitizeMol(mol, sanitizeOps=SanitizeFlags.SANITIZE_ALL ^ SanitizeFlags.SANITIZE_KEKULIZE)
        # Now, try to kekulize in a controlled manner by clearing aromatic flags.
        Chem.Kekulize(mol, clearAromaticFlags=True)
    except Exception as e:
        return False, f"Sanitization error (even with kekulization skipped): {e}"

    # 2. Identify sugar rings.
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    sugar_rings = []
    for ring in all_rings:
        if len(ring) in [5, 6]:
            oxy_count = 0
            carbon_count = 0
            other_count = 0
            for idx in ring:
                atom = mol.GetAtomWithIdx(idx)
                num = atom.GetAtomicNum()
                if num == 8:
                    oxy_count += 1
                elif num == 6:
                    carbon_count += 1
                else:
                    other_count += 1
            # Typical sugar rings (furanose or pyranose) have exactly one oxygen and the rest carbons.
            if oxy_count == 1 and carbon_count == (len(ring) - 1) and other_count == 0:
                sugar_rings.append(set(ring))
    
    if not sugar_rings:
        return False, "No sugar (glycoside) moiety detected."

    # 3. Remove sugar ring atoms to get the aglycone.
    sugar_atom_indices = set()
    for sring in sugar_rings:
        sugar_atom_indices.update(sring)
    
    # Use an editable mol to remove atoms from highest index to lowest.
    editable = Chem.EditableMol(mol)
    for idx in sorted(sugar_atom_indices, reverse=True):
        try:
            # Removing an atom may change indices, so this is a heuristic removal.
            editable.RemoveAtom(idx)
        except Exception as e:
            return False, f"Error removing sugar atom index {idx}: {e}"
    
    aglycone_mol = editable.GetMol()
    
    # Some removals lead to disconnected fragments. Choose the largest fragment.
    frags = Chem.GetMolFrags(aglycone_mol, asMols=True, sanitizeFrags=True)
    if not frags:
        return False, "Sugar removal left no aglycone fragment."
    aglycone = max(frags, key=lambda m: m.GetNumAtoms())

    # 4. Count carbon atoms in aglycone.
    aglycone_carbons = sum(1 for atom in aglycone.GetAtoms() if atom.GetAtomicNum() == 6)
    if not (25 <= aglycone_carbons <= 40):
        return False, f"Aglycone carbon count not in acceptable range (found {aglycone_carbons})."
    
    # 5. Examine the aglycone's ring system.
    aglycone_ring_info = aglycone.GetRingInfo()
    aglycone_rings = aglycone_ring_info.AtomRings()
    if len(aglycone_rings) < 4:
        return False, f"Insufficient rings in aglycone (found {len(aglycone_rings)})."
    # Check that none of the rings are aromatic.
    for ring in aglycone_rings:
        if all(aglycone.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            return False, "Aglycone contains an aromatic ring, not typical of triterpenoids."
    
    # 6. Overall molecular weight check.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 500:
        return False, f"Molecular weight too low ({mol_wt:.1f} Da) for a triterpenoid saponin."
    
    return True, ("Molecule contains a sugar moiety plus a triterpenoid-like aglycone " +
                  f"(aglycone carbons: {aglycone_carbons}, rings: {len(aglycone_rings)}).")

# For testing purposes (this block can be modified or removed in production):
if __name__ == "__main__":
    test_smiles = [
        # known triterpenoid saponin examples:
        "OC1(C2C=3C(C4(C(C5(C(CC4)C(C(O)CC5)(C)C)C)CC3)C)(CCC2(CCC1C)C(OC6OC(C(O)C(O)C6O)CO)=O)C",
        # A SMILES known to cause kekulization issues:
        "CN(C)c1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](NC(=O)[C@@H]([NH3+])Cc2ccc(O)cc2)[C@H]1O",
    ]
    for smi in test_smiles:
        verdict, reason = is_triterpenoid_saponin(smi)
        print("SMILES:", smi)
        print("Verdict:", verdict, "| Reason:", reason)
        print("-" * 80)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61778',
                          'name': 'triterpenoid saponin',
                          'definition': 'A terpene glycoside in which the '
                                        'terpene moiety is a triterpenoid.',
                          'parents': ['CHEBI:26605', 'CHEBI:61777'],
                          'xrefs': ['Wikipedia:Triterpenoid_saponin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 102,
                           'log_lines_of_code': 4.624972813284271,
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
                                                 3,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
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
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 0,
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
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from rdkit.Chem import '
                                          'SanitizeFlags'],
                           'imports_count': 3,
                           'methods_called': [   'SanitizeMol',
                                                 'RemoveAtom',
                                                 'GetMolFrags',
                                                 'GetMol',
                                                 'GetIsAromatic',
                                                 'GetNumAtoms',
                                                 'GetAtomWithIdx',
                                                 'update',
                                                 'AtomRings',
                                                 'CalcExactMolWt',
                                                 'append',
                                                 'GetAtoms',
                                                 'EditableMol',
                                                 'GetAtomicNum',
                                                 'GetRingInfo',
                                                 'MolFromSmiles',
                                                 'Kekulize'],
                           'methods_called_count': 17,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_triterpenoid_saponin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, f"Error parsing SMILES: {e}"',
                                          'False, f"Sanitization error (even '
                                          'with kekulization skipped): {e}"',
                                          'False, "No sugar (glycoside) moiety '
                                          'detected."',
                                          'False, f"Error removing sugar atom '
                                          'index {idx}: {e}"',
                                          'False, "Sugar removal left no '
                                          'aglycone fragment."',
                                          'False, f"Aglycone carbon count not '
                                          'in acceptable range (found '
                                          '{aglycone_carbons})."',
                                          'False, f"Insufficient rings in '
                                          'aglycone (found '
                                          '{len(aglycone_rings)})."',
                                          'False, "Aglycone contains an '
                                          'aromatic ring, not typical of '
                                          'triterpenoids."',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} Da) for a '
                                          'triterpenoid saponin."',
                                          'True, ("Molecule contains a sugar '
                                          'moiety plus a triterpenoid-like '
                                          'aglycone " +'],
                           'returns_count': 11,
                           'complexity': 7.724994562656855},
    'message': '\n'
               'Error: Error executing '
               "is_triterpenoid_saponin('CN(C)c1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](NC(=O)[C@@H]([NH3+])Cc2ccc(O)cc2)[C@H]1O'):\n"
               " Can't kekulize mol.  Unkekulized atoms: 3 4 5 6 7 8 9 10 11\n"
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1CCCC1)CCCCCC/C=C\\C2=CC=3OCOC3C=C2',
                                     'name': '(8E)-Piperamide-C9:1',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'},
                                 {   'smiles': '[H][C@@]12OC(=O)[C@H](C)[C@@]1(O)[C@@H](OC(C)=O)[C@]1([H])[C@@](C)([C@H](OC(C)=O)\\C=C/C(=C)[C@H]2OC)[C@@H](OC(=O)CC(C)C)[C@@H](OC(C)=O)[C@@H](OC(C)=O)[C@]11CO1',
                                     'name': 'Gemmacolide M, (rel)-',
                                     'reason': 'Insufficient rings in aglycone '
                                               '(found 2).'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](NC(OCC1=CC=CC=C1)=O)CC=2C=3C(NC2)=CC=CC3)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](CC4=CC=CC=C4)C(=O)N)C',
                                     'name': 'Gatratet',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'},
                                 {   'smiles': 'O=C(NCCC(=O)O)[C@@H]1N(NCCC1)C(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H]2N=C(C3=C(O)C=CC=C3)OC2)CO)CCCN(O)C=O',
                                     'name': 'Cahuitamycin A',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'},
                                 {   'smiles': 'C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@H](C)CO)C)CN(C)C(=O)CC3=CC=CC=C3',
                                     'name': 'N-[[(3S,9S,10R)-16-(dimethylamino)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methyl-2-phenylacetamide',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'},
                                 {   'smiles': 'OC[C@H]1O[C@H](OC[C@H]2O[C@H](OC[C@H]3O[C@H](OC[C@H]4O[C@H](OC[C@H]5O[C@H](O[C@]6(CO)O[C@H](CO)[C@@H](O)[C@@H]6O)[C@H](O)[C@@H](O)[C@@H]5O)[C@H](O)[C@@H](O)[C@H]4O)[C@H](O)[C@@H](O)[C@H]3O)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'ajugose',
                                     'reason': 'Aglycone carbon count not in '
                                               'acceptable range (found 1).'},
                                 {   'smiles': 'NC(=O)C[C@H]([NH3+])C([O-])=O',
                                     'name': 'L-asparagine zwitterion',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=CC=C1)C([O-])=O)[C@@H]([NH3+])CC([O-])=O',
                                     'name': '(3S)-3-Azaniumyl-4-[[(1S)-1-carboxylato-2-phenylethyl]amino]-4-oxobutanoate',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'},
                                 {   'smiles': 'CC1=CC(O)OC1=O',
                                     'name': '5-hydroxy-3-methylfuran-2(5H)-one',
                                     'reason': 'Aglycone carbon count not in '
                                               'acceptable range (found 1).'},
                                 {   'smiles': '[Co++].CC([O-])=O.CC([O-])=O',
                                     'name': 'cobalt(II) acetate',
                                     'reason': 'No sugar (glycoside) moiety '
                                               'detected.'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])CC[C@]1([H])[C@@](C)(CCC(=O)OC)[C@@H](CC[C@@]21C)C(C)(C)O)[C@]1(C)CC[C@@H](O1)C(C)(C)O',
                                      'name': 'methyl foveolate A',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found 23).'},
                                  {   'smiles': '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@]1([H])O[C@H]1CC[C@@]2(C)[C@@]([H])(CC[C@]3(C)[C@]2([H])CC[C@]2([H])[C@]([H])([C@H](O)C[C@@]32C)[C@]2(C)CC[C@](CO[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)(O2)C(C)C)C1(C)C',
                                      'name': 'Operculinoside B',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found 22).'},
                                  {   'smiles': 'C[C@H]1O[C@@H](O[C@H]2CC[C@@]3(C)[C@@H](CC[C@]4(C)[C@@H]3C=C[C@]35OC[C@@]6(CCC(C)(C)C[C@@H]36)[C@@H](O)C[C@@]45C)[C@]2(C)CO)[C@H](O)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]1O',
                                      'name': 'Saikosaponin A',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found 20).'},
                                  {   'smiles': '[H][C@@]12CC[C@]3(C)[C@]([H])(C[C@H]4O[C@]44[C@]5([H])C[C@@](C)(C=O)[C@H](C[C@]5(C)[C@@H](O)C[C@@]34C)OC(=O)c3ccccc3NC)[C@@]1(C)CC[C@H](O[C@@H]1OC[C@H](O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@@]2(C)CO',
                                      'name': 'avenacin A-1',
                                      'reason': 'Aglycone contains an aromatic '
                                                'ring, not typical of '
                                                'triterpenoids.'},
                                  {   'smiles': '[H][C@]1(OC[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)CO[C@@]1([H])OC[C@H]1O[C@@]([H])(O[C@H]2CC[C@@]3(C)[C@@]([H])(CC[C@]4(C)[C@]3([H])CC=C3[C@]5([H])CC(C)(C)[C@]6([H])C[C@@]5([C@H](O)C[C@@]43C)C(=O)O6)C2(C)C)[C@H](NC(C)=O)[C@@H](O)[C@@H]1O',
                                      'name': '3-O-[beta-D-xylopyranosyl(1->2)-alpha-L-arabinopyranosyl(1->6)]-2-acetamido-2-deoxy-beta-D-glucopyranosyl '
                                              'acacic acid lactone',
                                      'reason': 'Insufficient rings in '
                                                'aglycone (found 3).'},
                                  {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])CC[C@]1([H])[C@@]3(C)CCC(=O)OC(C)(C)[C@]3([H])CC[C@@]21C)[C@]1(C)CC[C@H](O1)C(C)(C)O',
                                      'name': '20S,24S-epoxy-25-hydroxy-A-homo-4-oxadammaran-3-one',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found 22).'},
                                  {   'smiles': '[H][C@]1(OC[C@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)CO[C@@]1([H])OC[C@H]1O[C@@]([H])(O[C@H]2CC[C@@]3(C)[C@@]([H])(CC[C@]4(C)[C@]3([H])CC=C3[C@]5([H])CC(C)(C)[C@]6([H])C[C@@]5([C@H](O)C[C@@]43C)C(=O)O6)C2(C)C)[C@H](NC(C)=O)[C@@H](O)[C@@H]1O',
                                      'name': '3-O-[alpha-L-arabinopyranosyl(1->2)-alpha-L-arabinopyranosyl(1->6)]-2-acetamido-2-deoxy-beta-D-glucopyranosyl '
                                              'acacic acid lactone',
                                      'reason': 'Insufficient rings in '
                                                'aglycone (found 3).'},
                                  {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])CC[C@]1([H])[C@@]3(C)CCC(=O)OC(C)(C)[C@]3([H])CC[C@@]21C)[C@@]1(C)CC[C@H](O1)C(C)(C)O',
                                      'name': 'rel-20R,24S-epoxy-25-hydroxy-A-homo-4-oxadammaran-3-one',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found 22).'},
                                  {   'smiles': '[H][C@]1(O[C@H](C)[C@@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O[C@]3([H])O[C@H](CO)[C@@H](O)[C@H](OC)[C@H]3O)[C@H]2O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](CO[C@@]1([H])O[C@H]1CC[C@]2(C)C3=C[C@H](O)C45C(=O)O[C@@](C)(CCC(O)C(C)C)[C@@]4(O)CC[C@@]5(C)[C@]3([H])CC[C@@]2([H])C1(C)C)OS(O)(=O)=O',
                                      'name': 'holothurin A4 acid',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found 19).'},
                                  {   'smiles': 'O([C@H]1[C@@]2([C@](C=3[C@]([C@]4([C@@]([C@@]5([C@@](CC4)(C([C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7OC[C@H](O)[C@H](O)[C@H]7O[C@@H]8O[C@H]([C@H](O)[C@@H](O)[C@H]8O)C)[C@H]6O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)C(O)=O)CC5)(C)C)[H])C)(CC3)[H])C)(C1)C)(CC([C@@H](OC(=O)C)[C@@H]2OC(=O)/C=C/C%10=CC=CC=C%10)(C)C)[H])CO)C(=O)C',
                                      'name': 'Assamsaponin J',
                                      'reason': 'Aglycone carbon count not in '
                                                'acceptable range (found '
                                                '43).'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning. In our previous attempt the program '
                 'tried to parse and sanitize the SMILES string right from the '
                 'start. However, some molecules (like the one given) raise a '
                 'kekulization error; that means some atoms couldn’t be '
                 'assigned proper aromaticity. In our improved solution we '
                 'first disable sanitization when reading the SMILES. Then, we '
                 'try to sanitize the molecule while explicitly skipping the '
                 'kekulization step. Finally, if desired, we force a '
                 'kekulization with aromatic flags cleared. This '
                 '“fallback‐sanitization” makes our sugar‐ and '
                 'aglycone‐detection steps more robust. We also keep our '
                 'original logic (detecting sugar rings, removing them to '
                 'obtain an aglycone, counting carbons and rings, etc.) so '
                 'that our heuristic is unchanged. \n'
                 '\n'
                 'Below is the complete Python code in one block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 321,
    'num_false_positives': 452,
    'num_true_negatives': 141451,
    'num_false_negatives': 76,
    'num_negatives': None,
    'precision': 0.4152652005174644,
    'recall': 0.8085642317380353,
    'f1': 0.5487179487179487,
    'accuracy': 0.9962895291637386,
    'negative_predictive_value': 0.9994629999929342}