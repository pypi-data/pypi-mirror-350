"""
Classifies: CHEBI:50753 isoflavonoid
"""
"""
Classifies: Any 1-benzopyran with an aryl substituent at position 3 (isoflavonoid).
An isoflavonoid is defined as a benzopyran (a 6‐membered pyran ring containing exactly one oxygen)
fused to a benzene ring (6‐membered, fully aromatic, carbon only) such that an exocyclic aryl substituent
(i.e. a 6‐membered aromatic ring not part of the fused core) is attached at the “3‐position” of the pyran.
This code implements a heuristic that uses ring order (via RDKit’s GetSymmSSSR) so that the position
two bonds away (clockwise from the oxygen in the ordered pyran) is taken as position 3.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_isoflavonoid(smiles: str):
    """
    Determines if a molecule is an isoflavonoid based on its SMILES string.
    An isoflavonoid is defined as any 1-benzopyran with an aryl substituent at position 3.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as an isoflavonoid, otherwise False.
        str: Explanation of the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return False, "Invalid SMILES string"

    # Get basic ring information from the molecule.
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()  # each ring is a tuple of atom indices
    if not atom_rings:
        return False, "No rings found in the molecule"

    # Use RDKit's Symmetry-based ring finder for ordered rings.
    # This returns RingInfo objects (as tuples representing a cyclic order)
    rings = list(Chem.GetSymmSSSR(mol))
    
    # Build candidate benzene rings: 6-membered rings with all aromatic carbons.
    benzene_rings = []
    for ring in atom_rings:
        if len(ring) == 6:
            if all(mol.GetAtomWithIdx(idx).GetIsAromatic() and
                   mol.GetAtomWithIdx(idx).GetAtomicNum() == 6
                   for idx in ring):
                benzene_rings.append(set(ring))
    if not benzene_rings:
        return False, "No benzene rings (6-membered, fully aromatic carbons) found."

    # Collect candidate pyran rings from the ordered rings (from GetSymmSSSR):
    # We require a 6-membered ring with exactly one oxygen and five carbons.
    pyran_candidates = []  # list of tuples (ordered_ring, set(ring))
    for cyc in rings:
        if len(cyc) == 6:
            atoms = [mol.GetAtomWithIdx(idx) for idx in cyc]
            ocount = sum(1 for a in atoms if a.GetAtomicNum() == 8)
            ccount = sum(1 for a in atoms if a.GetAtomicNum() == 6)
            if ocount == 1 and ccount == 5:
                pyran_candidates.append( (list(cyc), set(cyc)) )
    if not pyran_candidates:
        return False, "No candidate pyran ring (6-membered with exactly one oxygen) found."
    
    # Now try to detect a fused benzopyran system with the correct exocyclic substitution.
    for ordered_pyran, pyran_set in pyran_candidates:
        # Look for a fused benzene ring which shares 2 or 3 atoms with the pyran.
        for benzene in benzene_rings:
            shared = pyran_set.intersection(benzene)
            if len(shared) in (2, 3):
                fused_core = pyran_set.union(benzene)
                # Try to locate the oxygen atom in the ordered pyran ring.
                oxygen_index = None
                for i, idx in enumerate(ordered_pyran):
                    atom = mol.GetAtomWithIdx(idx)
                    if atom.GetAtomicNum() == 8:
                        oxygen_index = i
                        break
                if oxygen_index is None:
                    continue  # should not occur as we filtered for one oxygen

                # In a typical 1-benzopyran, the heterocyclic numbering (starting at the oxygen as 1)
                # implies that the atom two positions away (clockwise) is at position 3.
                candidate_pos = ordered_pyran[(oxygen_index + 2) % 6]
                # If this candidate atom is already in the fused interface, skip it.
                if candidate_pos in shared:
                    # It would be fused with the benzene, not free for exocyclic substitution.
                    continue

                candidate_atom = mol.GetAtomWithIdx(candidate_pos)
                # Look for neighbors of candidate_atom that are not in the pyran ring.
                for nbr in candidate_atom.GetNeighbors():
                    if nbr.GetIdx() in pyran_set:
                        continue  # Skip connections within the pyran
                    # For an aryl substituent, the neighbor should be an aromatic carbon.
                    if nbr.GetAtomicNum() != 6 or not nbr.GetIsAromatic():
                        continue
                    # Now check that this neighbor participates in a 6-membered aromatic ring (phenyl-like)
                    found_aryl_ring = False
                    for ring in atom_rings:
                        if len(ring) == 6 and nbr.GetIdx() in ring:
                            if all(mol.GetAtomWithIdx(i).GetIsAromatic() and mol.GetAtomWithIdx(i).GetAtomicNum() == 6 
                                   for i in ring):
                                # Ensure this ring is not completely part of the fused benzopyran core.
                                if not set(ring).issubset(fused_core):
                                    found_aryl_ring = True
                                    break
                    if found_aryl_ring:
                        return True, ("Molecule contains a fused benzopyran core (6-membered pyran with one oxygen fused "
                                      "with a benzene ring sharing 2–3 atoms) and an exocyclic aryl substituent attached at "
                                      "the position expected to be position 3.")
    # If we have exhausted the candidates without a positive identification.
    return False, "Scaffold not recognized as isoflavonoid (no fused benzopyran core with an aryl substituent at position 3 found)."

# Example usage (for testing purposes – you may run several SMILES strings):
if __name__ == '__main__':
    test_smiles = [
        # Some test SMILES examples (these do not cover full complexity)
        "O1C(C2=CC=CC=C2)=CC(O)=C1",  # simple benzopyran (may lack the proper substitution)
        "COc1ccc(-c2coc3ccccc3c2)cc1"  # a rough example of benzopyran with a phenyl substituent.
    ]
    for smi in test_smiles:
        res, reason = is_isoflavonoid(smi)
        print(f"SMILES: {smi}\nResult: {res}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50753',
                          'name': 'isoflavonoid',
                          'definition': 'Any 1-benzopyran with an aryl '
                                        'substituent at position 3. The term '
                                        'was originally restricted to natural '
                                        'products, but is now also used to '
                                        'describe semi-synthetic and fully '
                                        'synthetic compounds.',
                          'parents': [   'CHEBI:26004',
                                         'CHEBI:38443',
                                         'CHEBI:72544'],
                          'xrefs': [   'MetaCyc:Isoflavonoids',
                                       'Wikipedia:Isoflavonoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 68,
                           'log_lines_of_code': 4.219507705176107,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
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
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 4,
                                                 5,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetAtomWithIdx',
                                                 'union',
                                                 'append',
                                                 'GetSymmSSSR',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetIsAromatic',
                                                 'GetRingInfo',
                                                 'intersection',
                                                 'AtomRings'],
                           'methods_called_count': 10,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_isoflavonoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in the '
                                          'molecule"',
                                          'False, "No benzene rings '
                                          '(6-membered, fully aromatic '
                                          'carbons) found."',
                                          'False, "No candidate pyran ring '
                                          '(6-membered with exactly one '
                                          'oxygen) found."',
                                          'False, "Scaffold not recognized as '
                                          'isoflavonoid (no fused benzopyran '
                                          'core with an aryl substituent at '
                                          'position 3 found)."'],
                           'returns_count': 5,
                           'complexity': 5.243901541035221},
    'message': '\n'
               'Attempt failed: F1 score of 0.18562144597887897 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1C(=C(OC=2C1=C(C(O)=C(O)C2)C(=O)O)OC)C3=C(C=4OC5=C(C(=C(O)C(=C5)O)C(=O)O)C(C4C=C3C(=O)C)=O)C(=O)C '
               "NAME: (aR)-2'-methoxyvinaxanthone REASON: CORRECT Molecule "
               'contains a fused benzopyran core (a six-membered pyran with '
               'one oxygen fused with a benzene ring sharing 2–3 atoms) with '
               'an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'S(OC1=CC=2OC=C(C3=CC=C(O[C@H]4O[C@H](C(O)[C@@H](O)C4O)C(O)=O)C=C3)C(=O)C2C=C1)(O)(=O)=O '
               "NAME: daidzein 4'-glucuronide-7-sulfate REASON: CORRECT "
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C2=C(CC=C(C)C)C(O)=CC(O)=C2C(=O)C(C3=CC=C(OC)C=C3)=C1 NAME: '
               'Gancaonin M REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O1C(C(O)CC=2C1=C(C=CC2O)C=3C(=O)C4=C(OC3)C=C(O)C(=C4O)CC=C(C)C)(C)C '
               'NAME: Lupinisolone C REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O1[C@H]([C@@H](O)C(O)C(O)[C@@]1(C=2C=3OC=C(C(=O)C3C=CC2O)C4=CC=C(O)C=C4)[H])CO[C@@H]5OC[C@@H](O)[C@H](O)C5O '
               'NAME: Pueraria glycoside 2 REASON: CORRECT Molecule contains a '
               'fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: CC1(C)Oc2ccc(cc2C=C1)-c1coc2cc(O)cc(O)c2c1=O NAME: '
               'isoderrone REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'COc1cc2OC[C@H](Cc2c(OC)c1CC=C(C)C)c1ccc(O)c(CC=C(C)C)c1O NAME: '
               'licorisoflavan A REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O=C1C2=C(OC=C1C3=CC=C(O)C=C3)C=C(O[C@@H]4OC(C(OC)[C@H]([C@@H]4O)O)CO)C=C2O '
               'NAME: '
               '5,7,4′-trihydroxyisoflavone-7-O-(4′′-O-methyl)-beta-D-glucopyranoside '
               'REASON: CORRECT Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc(O)c3c(c2)occ(-c2ccc(O)cc2)c3=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: genistein 7-O-beta-D-glucoside REASON: CORRECT Molecule '
               'contains a fused benzopyran core (a six-membered pyran with '
               'one oxygen fused with a benzene ring sharing 2–3 atoms) with '
               'an exocyclic aryl substituent.\n'
               ' * SMILES: CC(C)(O)CCc1cc(ccc1O)-c1coc2cc(O)cc(O)c2c1=O NAME: '
               'isowigtheone hydrate REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=CC=3OC=C(C(=O)C3C=C2)C4=CC=C(O)C=C4)COC(=O)C '
               'NAME: '
               '[6-[3-(4-Hydroxyphenyl)-4-oxidanylidene-chromen-7-yl]oxy-3,4,5-tris(oxidanyl)oxan-2-yl]methyl '
               'ethanoate REASON: CORRECT Molecule contains a fused benzopyran '
               'core (a six-membered pyran with one oxygen fused with a '
               'benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: Oc1ccc(C2COc3cc(O)cc(O)c3C2=O)c(O)c1 NAME: '
               '(+-)-dalbergioidin REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'COc1cc2c(cc1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)occ(-c1ccc(O)cc1)c2=O '
               'NAME: glycitin REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C(O)C=C2)=COC3=C1C=C(OC)C(=C3)O[C@@H]4O[C@H]([C@H](O)[C@H]([C@H]4O)O)C '
               'NAME: 6-O-methyl-7-O-alpha-rhamnopyranosyldaidzein REASON: '
               'CORRECT Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=CC=3OC=C(C(=O)C3C=C2)C4=C(O)C(OC)=C(OC)C=C4)CO '
               "NAME: 7,2'-Dihydroxy-3',4'-dimethoxyisoflavone 7-O-glucoside "
               'REASON: CORRECT Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: O1C[C@@H]([C@H](O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3 '
               'NAME: cis-4-Hydroxyequol REASON: CORRECT Molecule contains a '
               'fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C(O)C=C2)=COC3=C1C=CC(=C3)OC4O[C@H]([C@H](O)[C@H]([C@H]4OC)O)C '
               'NAME: Daidzein G3 REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'Oc1ccc-2c(c1)[C@@H]1Oc3ccccc3[C@H]3CC(=O)c4c(O)cc(O)c-2c4[C@@H]13 '
               'NAME: Ohioensin-A REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O1CC(C=2C=C(C/C=C(/CCC=C(C)C)\\C)C(O)=CC2O)C(=O)C3=C1C=C(O)C(=C3O)CC=C(C)C '
               'NAME: Sophoraisoflavanone D REASON: CORRECT Molecule contains '
               'a fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: O1C2=C(C(=O)C(C3=CC(OC)=C(OC)C=C3)=C1)C=CC=4OCOC24 '
               'NAME: Maximaisoflavone D REASON: CORRECT Molecule contains a '
               'fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'O1C(C(O)CC2=C1C=C3OC(=O)C(=CC3=C2OC)C4=C(O)C=C(O)C=C4)(C)C '
               'NAME: Isolicopyranocoumarin REASON: CORRECT Molecule contains '
               'a fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: O1C2=C(C(=O)C(C3=CC(=C(O)C=C3)C=O)=C1)C=CC(O)=C2 '
               'NAME: Corylinal REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: COc1cc2OC[C@H](Cc2c(OC)c1CC=C(C)C)c1ccc(O)cc1O '
               'NAME: glyasperin D REASON: CORRECT Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'S(OC1=CC=C(C=2C(=O)C=3C(OC2)=CC(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C([O-])=O)=CC3[O-])C=C1)(O)(=O)=O.[Na+].[Na+] '
               "NAME: genistein 7-glucuronide-4'-sulfate REASON: CORRECT "
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1CC(O)(C2=C(OC)C(=C(OC)C=C2)CC=C(C)C)C(=O)C=3C1=CC(O)=CC3O '
               'NAME: (+)-echinoisoflavanone REASON: CORRECT Molecule contains '
               'a fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               'False positives: SMILES: '
               'O1C([C@H](O)C(O)[C@H](O)[C@@H]1OC2=CC=C(C=C2)C=3OC4=C(C(=O)C3O)C(OC)=C(O)C(O)=C4)C '
               'NAME: Vogelin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'O=C1O[C@H]2[C@H](O)[C@@H](O)C(O)O[C@@H]2COC(=O)C3=C(C(O)=C(O)C(=C3)O)C4=C5C=6C7=C(C(C8=C1C=C(O)C(=C8O)O)=C(O)C(O)=C7OC5=O)C(=O)OC6C(O)=C4O '
               'NAME: Punicalin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\Cc1c(O)c(O)ccc1[C@@H]1CC(=O)c2c(O1)cc(O)c(CC=C(C)C)c2O '
               'NAME: nymphaeol C REASON: WRONGLY CLASSIFIED Molecule contains '
               'a fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)C(OC(=O)/C=C/C2=CC=C(O)C=C2)C(O)[C@@H]1OC3=C(OC=4C(C3=O)=C(O)C=C(O)C4)C5=CC(O)=C(O)C=C5)COC(=O)/C=C/C6=CC=C(O)C=C6 '
               "NAME: Quercetin 3-(3'',6''-di-p-coumarylglucoside) REASON: "
               'WRONGLY CLASSIFIED Molecule contains a fused benzopyran core '
               '(a six-membered pyran with one oxygen fused with a benzene '
               'ring sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C(C=2C(OC)=CC(OC)=C(OC)C2)=C(O)C(=O)C=3C1=CC(O)=CC3O NAME: '
               "3,5,7-Trihydroxy-2',4',5'-trimethoxyflavone REASON: WRONGLY "
               'CLASSIFIED Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'S(OC1C(COC=2C1=C(O)C=C(O)C2)C3=C(O)C=C(OC)C=C3)(O)(=O)=O NAME: '
               '[5,7-dihydroxy-3-(2-hydroxy-4-methoxyphenyl)-3,4-dihydro-2H-1-benzopyran-4-yl]oxidanesulfonic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'CCC1=CC=CC=C1NC(=O)COC2=CC3=C(C=C2)OC(=CC3=O)C4=CC=C(C=C4)OC '
               'NAME: '
               'N-(2-ethylphenyl)-2-[[2-(4-methoxyphenyl)-4-oxo-1-benzopyran-6-yl]oxy]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O[C@@H]1[C@H](OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1 NAME: '
               '(+)-trans-fustin REASON: WRONGLY CLASSIFIED Molecule contains '
               'a fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'O1C2(OC3=C(C(C2O)C4=C1C=C(O)C5=C4OC(C(O)C5)C6=CC(OC)=C(O)C=C6)C(O)=C(C7C(O)C(OC=8C7=C(O)C=C(O)C8)C9=CC(O)=C(O)C=C9)C(O)=C3)C%10=CC(O)=C(O)C=C%10 '
               'NAME: '
               '5-(3,4-dihydroxyphenyl)-18-[2-(3,4-dihydroxyphenyl)-3,5,7-trihydroxy-3,4-dihydro-2H-1-benzopyran-4-yl]-13-(4-hydroxy-3-methoxyphenyl)-4,12,14-trioxapentacyclo[11.7.1.0?,??.0?,?.0??,??]henicosa-2(11),3(8),9,15(20),16,18-hexaene-6,9,17,19,21-pentol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: Cc1c(O)c(C)c2O[C@@H](CC(=O)c2c1O)c1ccccc1O NAME: '
               "(2S)-2'-hydroxydemethoxymatteucinol REASON: WRONGLY CLASSIFIED "
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C2=C(C(OC=3C2=CC(O)=C(OC)C3)C=C(C)C)C(=O)C=4C1=C(CC=C(C)C)C(O)=CC4O '
               'NAME: Cycloaltilisin REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused benzopyran core (a six-membered pyran with '
               'one oxygen fused with a benzene ring sharing 2–3 atoms) with '
               'an exocyclic aryl substituent.\n'
               ' * SMILES: O=C1C2=C(OC3=C1C(C(=O)OC)=CC=C3)C=C(CCO)C=C2O NAME: '
               '1-hydroxy-3-hydroxyethyl-8-ethoxycarbonylxanthone REASON: '
               'WRONGLY CLASSIFIED Molecule contains a fused benzopyran core '
               '(a six-membered pyran with one oxygen fused with a benzene '
               'ring sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC2=C(OC3=C(C2=O)C(OC)=CC(O)=C3)C4=CC(O)=C(O)C=C4)CO '
               'NAME: Azaleatin 3-glucoside REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'S(C1C(O)C(OC2=C1C=3OC(=O)C=C(C3C(O)=C2)C4=CC=CC=C4)(C)C)CC(NC(=O)CCC(N)C(O)=O)C(=O)NCC(O)=O '
               'NAME: '
               '2-amino-4-({1-[(carboxymethyl)-C-hydroxycarbonimidoyl]-2-({5,9-dihydroxy-8,8-dimethyl-2-oxo-4-phenyl-2H,8H,9H,10H-pyrano[2,3-h]chromen-10-yl}sulfanyl)ethyl}-C-hydroxycarbonimidoyl)butanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: CC(C)(C=C)c1c(O)cc(O)c2c1oc(-c1ccccc1)c(O)c2=O '
               'NAME: 8-(1,1-dimethylallyl)galangin REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C2=C(C(OC)=CC(OCC=C(C)C)=C2OC)C(=O)C(OC)=C1C3=CC(OC)=C(O)C=C3 '
               "NAME: 4'-Hydroxy-3,5,8,3'-tetramethoxy-7-prenyloxyflavone "
               'REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: CC1=CC(=CC2=C1C(C3=C(C(=C(C(=C3O2)Cl)OC)Cl)O)=O)OC '
               'NAME: 2,4-dichlorolichexanthone REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC=2C=3C(C=4C(O)=CC(O)=C(O)C4)=CC(OC3C=C(OC)C2)=O)CO '
               "NAME: 5,2',4',5'-Tetrahydroxy-7-methoxy-4-phenylcoumarin "
               '5-O-glucoside REASON: WRONGLY CLASSIFIED Molecule contains a '
               'fused benzopyran core (a six-membered pyran with one oxygen '
               'fused with a benzene ring sharing 2–3 atoms) with an exocyclic '
               'aryl substituent.\n'
               ' * SMILES: '
               'O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)C1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(OC)=C(O)C=C4)CO[C@@]5(O[C@H]([C@H](O)[C@@H](O)[C@H]5O)C)[H] '
               'NAME: isorhamnetin 3-O-robinobioside REASON: WRONGLY '
               'CLASSIFIED Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)c(O)c2)c(O)c3=O)[C@H](O)[C@H](O)[C@H]1O '
               'NAME: quercetin 7-O-alpha-L-rhamnopyranoside REASON: WRONGLY '
               'CLASSIFIED Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1[C@H]([C@H](O)[C@@H](O)[C@H]1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC(O)=C(O)C=C4)CO '
               'NAME: Cyanidin 3-O-arabinoside REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: CC(C)OC1=CC2=C(C=C1)C(=O)C3=C(O2)C=CC(=C3)C(=O)O '
               'NAME: 9-oxo-6-propan-2-yloxy-2-xanthenecarboxylic acid REASON: '
               'WRONGLY CLASSIFIED Molecule contains a fused benzopyran core '
               '(a six-membered pyran with one oxygen fused with a benzene '
               'ring sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'O1C(OC2=C3C(CC(OC3=C4CC(O)C(OC4=C2)C5=CC(O)=C(O)C=C5)=O)C6=CC(OC)=C(O)C=C6)C(O)C(O)C(O)C1CO '
               'NAME: '
               '12-(3,4-dihydroxyphenyl)-13-hydroxy-6-(4-hydroxy-3-methoxyphenyl)-8-{[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy}-3,11-dioxatricyclo[8.4.0.0?,?]tetradeca-1,7,9-trien-4-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'benzopyran core (a six-membered pyran with one oxygen fused '
               'with a benzene ring sharing 2–3 atoms) with an exocyclic aryl '
               'substituent.\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC=2C=3OC(=O)C=4C=5C3C(=CC2O)C(OC5C(OC)=C(O)C4)=O)C '
               'NAME: 3-Methylellagic acid 8-rhamnoside REASON: WRONGLY '
               'CLASSIFIED Molecule contains a fused benzopyran core (a '
               'six-membered pyran with one oxygen fused with a benzene ring '
               'sharing 2–3 atoms) with an exocyclic aryl substituent.\n'
               ' * SMILES: '
               'C[C@@H]1Cc2c3O[C@@]4(O)[C@@H](C)O[C@H](C)c5c4c4c6c(cc(=O)c(c(O)c2[C@@H](C)O1)c36)oc1c(O)cc(O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)c(c41)c5=O '
               'NAME: viridaphin A1 glucoside REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused benzopyran core (a six-membered '
               'pyran with one oxygen fused with a benzene ring sharing 2–3 '
               'atoms) with an exocyclic aryl substituent.\n'
               'False negatives: SMILES: '
               'O=C1NCC2=C1C=C(O)C3=C2O[C@@]4([C@@H]([C@@]5([C@H](C([C@@H](OC(=O)C)CC5)(C)C)CC4)C)C3)C '
               'NAME: Memnobotrin A REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               ' * SMILES: '
               'O1CC(CC=2C1=C(OC)C(OC)=C(OC)C2)C=3C(=O)C(OC)=C(OC)C(=O)C3 '
               "NAME: 6,7,8,3',4'-Pentamethoxyisoflavanquinone REASON: MISSED "
               'Scaffold not recognized as isoflavonoid (no fused benzopyran '
               'core with suitable exocyclic aryl substituent found).\n'
               ' * SMILES: '
               'O1CC(CC2=C1C(OC)=C(O)C=C2)C=3C(=O)C(OC)=C(OC)C(=O)C3 NAME: '
               'Amorphaquinone REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               ' * SMILES: '
               'O=C(O)C1=C(O)C2=C(O[C@@]3(CC[C@@H]4[C@@]([C@H]3C2)(CCCC4(C)C)C)C)C=C1C '
               'NAME: Hongoquercin A REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               ' * SMILES: O1CC(CC2=C1C=C(O)C=C2)C=3C(=O)C=C(OC)C(=O)C3 NAME: '
               'Claussequinone REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               ' * SMILES: '
               'O1[C@@]2([C@H](O)C[C@H]3C(CCC[C@@]3([C@H]2C[C@@]4([C@H]1[C@H](O)C(=C)[C@@H]([C@H]4O)O)O)C)(C)C)C '
               'NAME: Coniothyrenol REASON: MISSED No benzene rings (aromatic '
               '6-membered all-carbon) found for a fused system\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@]([C@@H]3[C@](OC=4C(=C5COC(C5=C(C4C3)O)=O)C)(C)CC2)(C)CC1)(C)C '
               'NAME: Austalide V REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               ' * SMILES: '
               'C=1(C=C(C=C(C1O)O)CC2OC(CC2)=O)OC3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O)O)O '
               'NAME: '
               "5-(3',4',5'-Trihydroxyphenyl)-gamma-valerolactone-3'-O-glucuronide "
               'REASON: MISSED Scaffold not recognized as isoflavonoid (no '
               'fused benzopyran core with suitable exocyclic aryl substituent '
               'found).\n'
               ' * SMILES: '
               'O1C[C@H](CC2=C1C(OC)=C(O)C=C2)C=3C(=O)C=C(OC)C(=O)C3 NAME: '
               'Mucroquinone REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(C)Oc4c(C[C@]3([H])[C@@]1(C)CC[C@H](OC(C)=O)C2(C)C)c(O)cc1C(=O)OCc41 '
               'NAME: kampanol A REASON: MISSED Scaffold not recognized as '
               'isoflavonoid (no fused benzopyran core with suitable exocyclic '
               'aryl substituent found).\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'No candidate pyran ring '
                                               '(6-membered with exactly one '
                                               'oxygen) found.'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'No candidate pyran ring '
                                               '(6-membered with exactly one '
                                               'oxygen) found.'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No benzene rings (6-membered, '
                                               'fully aromatic carbons) '
                                               'found.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No candidate pyran ring '
                                               '(6-membered with exactly one '
                                               'oxygen) found.'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No benzene rings (6-membered, '
                                               'fully aromatic carbons) '
                                               'found.'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'No candidate pyran ring '
                                               '(6-membered with exactly one '
                                               'oxygen) found.'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'No candidate pyran ring '
                                               '(6-membered with exactly one '
                                               'oxygen) found.'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'No candidate pyran ring '
                                               '(6-membered with exactly one '
                                               'oxygen) found.'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1NCC2=C1C=C(O)C3=C2O[C@@]4([C@@H]([C@@]5([C@H](C([C@@H](OC(=O)C)CC5)(C)C)CC4)C)C3)C',
                                      'name': 'Memnobotrin A',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'CC1(C)Oc2ccc(cc2C=C1)-c1coc2cc(O)cc(O)c2c1=O',
                                      'name': 'isoderrone',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'O=C1C2=C(OC=C1C3=CC=C(O)C=C3)C=C(O[C@@H]4OC(C(OC)[C@H]([C@@H]4O)O)CO)C=C2O',
                                      'name': '5,7,4′-trihydroxyisoflavone-7-O-(4′′-O-methyl)-beta-D-glucopyranoside',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'CC(C)(O)CCc1cc(ccc1O)-c1coc2cc(O)cc(O)c2c1=O',
                                      'name': 'isowigtheone hydrate',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'Oc1ccc(C2COc3cc(O)cc(O)c3C2=O)c(O)c1',
                                      'name': '(+-)-dalbergioidin',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'O1CC(CC=2C1=C(OC)C(OC)=C(OC)C2)C=3C(=O)C(OC)=C(OC)C(=O)C3',
                                      'name': "6,7,8,3',4'-Pentamethoxyisoflavanquinone",
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'O1C[C@@H]([C@H](O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3',
                                      'name': 'cis-4-Hydroxyequol',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'Oc1ccc-2c(c1)[C@@H]1Oc3ccccc3[C@H]3CC(=O)c4c(O)cc(O)c-2c4[C@@H]13',
                                      'name': 'Ohioensin-A',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'O1CC(C=2C=C(C/C=C(/CCC=C(C)C)\\C)C(O)=CC2O)C(=O)C3=C1C=C(O)C(=C3O)CC=C(C)C',
                                      'name': 'Sophoraisoflavanone D',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'},
                                  {   'smiles': 'O1CC(O)(C2=C(OC)C(=C(OC)C=C2)CC=C(C)C)C(=O)C=3C1=CC(O)=CC3O',
                                      'name': '(+)-echinoisoflavanone',
                                      'reason': 'Scaffold not recognized as '
                                                'isoflavonoid (no fused '
                                                'benzopyran core with an aryl '
                                                'substituent at position 3 '
                                                'found).'}],
    'attempt': 2,
    'reasoning': 'Below is one possible improved solution. One hypothesis was '
                 'that the previous code was “too loose” in that it simply '
                 'looked for any non‐fused pyran atom having an aromatic '
                 'neighbor without checking that it was in fact the “correct” '
                 'position (position\u20053 from the heterocyclic oxygen) on a '
                 'genuine 1‐benzopyran. In the revised approach the code first '
                 'collects the ordered rings (using RDKit’s symmetry‐based '
                 'ring finder) so that we can locate the sole oxygen in a '
                 '6‐membered candidate pyran and then, using the cyclic order, '
                 'pick the atom two away (the “3‐position”) as the expected '
                 'attachment point. Then the code checks that the pyran is '
                 'fused to a benzene ring (by sharing 2–3 atoms) and finally '
                 'that the candidate 3‑position bears an exocyclic aromatic '
                 'substituent (a 6‐membered fully aromatic, carbon‐only ring '
                 'not included in the fused core). This extra ordering and '
                 '“positional” check is intended to reduce both false '
                 'positives (other extraneous aryl groups) and false negatives '
                 '(missing the proper connectivity). Note that given the '
                 'complexity of the many isoflavonoid subclasses, no automated '
                 'method will be perfect, and this heuristic may still not '
                 'catch some edge cases.\n'
                 '\n'
                 'Below is the complete code in a single Python code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 303,
    'num_false_positives': 784,
    'num_true_negatives': 141040,
    'num_false_negatives': 173,
    'num_negatives': None,
    'precision': 0.27874885004599814,
    'recall': 0.6365546218487395,
    'f1': 0.38771593090211126,
    'accuracy': 0.9932747716092761,
    'negative_predictive_value': 0.9987749003278735}