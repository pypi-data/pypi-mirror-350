"""
Classifies: CHEBI:39437 tocol
"""
#!/usr/bin/env python3
"""
Classifies: tocol
A tocol is defined as "A chromanol with a chroman-6-ol skeleton that is substituted at position 2 by a 
saturated or triply-unsaturated hydrocarbon chain consisting of three isoprenoid units".

The strategy is:
  1. Parse the SMILES.
  2. Identify a fused bicyclic core comprised of two 6-membered rings that share at least 2 atoms:
       • One ring must be aromatic and have at least one oxygen substituent attached via a single bond.
       • The other (saturated) ring should not be aromatic and must contain exactly one heteroatom – an oxygen.
  3. Identify a candidate attachment point on the saturated ring (a carbon that has a neighbor not in the fused core).
  4. Starting from that neighbor (which marks the beginning of the side chain), do a depth-first search 
     while not entering the fused core and while not traversing any ring atoms.
  5. In the extracted side chain, count only the carbon atoms and the carbon–carbon double bonds. 
     The chain must have between 12 and 17 carbons and either 0 or 3 double bonds.
  6. If all tests pass, classify the molecule as a tocol.
  
Note: This algorithm has been modified to allow some heteroatom substituents (eg. hydroxyl, acetyl) in the side chain,
and to relax the requirement on the substituent oxygen on the aromatic ring (which can be esterified).
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_tocol(smiles: str):
    """
    Determines whether the molecule specified by the SMILES string is a tocol.

    Args:
        smiles (str): SMILES representation of the molecule.
        
    Returns:
        (bool, str): (True, reason) if the molecule is classified as a tocol;
                     (False, reason) otherwise.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Precompute all ring atom indices in the molecule (for DFS check later)
    ring_info = mol.GetRingInfo()
    all_ring_atoms = set()
    for ring in ring_info.AtomRings():
        all_ring_atoms.update(ring)
        
    # Helpers:
    def ring_has_ox_substituent(ring):
        """Return True if any atom in the ring has a neighbor (not in the ring) 
           that is oxygen and attached via a SINGLE bond (allowing -OH or -O-acyl)."""
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nb in atom.GetNeighbors():
                if nb.GetIdx() in ring:
                    continue
                # only consider single-bond oxygen substituents
                bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nb.GetIdx())
                if nb.GetAtomicNum() == 8 and bond and bond.GetBondType() == Chem.rdchem.BondType.SINGLE:
                    return True
        return False

    def ring_is_aromatic(ring):
        """Return True if all atoms in the ring are set as aromatic."""
        return all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)
    
    # Search for a fused bicyclic core comprised of two 6-membered rings that share at least two atoms.
    fused_core = None
    aromatic_ring = None
    saturated_ring = None
    rings = ring_info.AtomRings()  # each ring is a tuple of atom indices
    for i in range(len(rings)):
        ring1 = rings[i]
        if len(ring1) != 6:
            continue
        for j in range(i+1, len(rings)):
            ring2 = rings[j]
            if len(ring2) != 6:
                continue
            shared = set(ring1).intersection(set(ring2))
            if len(shared) < 2:
                continue
            # Check if one ring is aromatic and has an oxygen substituent.
            if ring_is_aromatic(ring1) and ring_has_ox_substituent(ring1):
                aromatic_ring = set(ring1)
                saturated_ring = set(ring2)
            elif ring_is_aromatic(ring2) and ring_has_ox_substituent(ring2):
                aromatic_ring = set(ring2)
                saturated_ring = set(ring1)
            else:
                continue
            # For the saturated (non-aromatic) ring, expect exactly one non-carbon atom (should be oxygen)
            non_carbons = [mol.GetAtomWithIdx(idx).GetSymbol() for idx in saturated_ring if mol.GetAtomWithIdx(idx).GetAtomicNum() != 6]
            if len(non_carbons) != 1 or non_carbons[0] != "O":
                continue
            # Define the fused core as the union of the two rings.
            fused_core = aromatic_ring.union(saturated_ring)
            break
        if fused_core is not None:
            break
            
    if fused_core is None:
        return False, "Chromanol core (fused aromatic and heterocyclic rings) not found"
    
    # Now, search for an attachment point on the saturated ring.
    # The candidate is a carbon in saturated ring that has at least one neighbor outside the fused core.
    candidate_attachment = None
    for idx in saturated_ring:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetAtomicNum() != 6:
            continue
        for nb in atom.GetNeighbors():
            if nb.GetIdx() not in fused_core:
                # Accept if neighbor is carbon (even if later extra hetero atoms may be encountered).
                candidate_attachment = (idx, nb.GetIdx())
                break
        if candidate_attachment:
            break
            
    if candidate_attachment is None:
        return False, "Side chain attachment point on the chromanol core not found"
    
    # DFS to extract the side chain. We traverse from the side-chain-start (neighbor outside the core)
    # We allow any atom (even non-carbon) as long as it is not in the fused core.
    # However, if any visited atom is part of any ring, we abort (side chain must be acyclic).
    def extract_side_chain(start_idx):
        visited = set()
        stack = [start_idx]
        side_chain = set()
        while stack:
            curr = stack.pop()
            if curr in visited:
                continue
            visited.add(curr)
            # Check: if this atom is in any ring, then the chain is cyclic.
            if curr in all_ring_atoms:
                return None, "Side chain is cyclic (contains ring atoms)"
            side_chain.add(curr)
            curr_atom = mol.GetAtomWithIdx(curr)
            for nb in curr_atom.GetNeighbors():
                if nb.GetIdx() in fused_core:
                    continue  # do not traverse into the core
                if nb.GetIdx() not in visited:
                    stack.append(nb.GetIdx())
        return side_chain, None

    side_start = candidate_attachment[1]
    side_chain, err = extract_side_chain(side_start)
    if err:
        return False, f"Error in side chain extraction: {err}"
    
    # Count the number of carbon atoms present in the extracted side chain.
    chain_carbons = sum(1 for idx in side_chain if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
    if chain_carbons < 12 or chain_carbons > 17:
        return False, f"Side chain has {chain_carbons} carbons; expected between 12 and 17 for three isoprenoid units"
    
    # Count double bonds in the side chain (only count bonds between carbon atoms).
    chain_double_bonds = 0
    for bond in mol.GetBonds():
        a1 = bond.GetBeginAtomIdx()
        a2 = bond.GetEndAtomIdx()
        if a1 in side_chain and a2 in side_chain:
            atom1 = mol.GetAtomWithIdx(a1)
            atom2 = mol.GetAtomWithIdx(a2)
            if atom1.GetAtomicNum() == 6 and atom2.GetAtomicNum() == 6:
                if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                    chain_double_bonds += 1
    if chain_double_bonds not in (0, 3):
        return False, f"Side chain has {chain_double_bonds} C=C double bonds; expected 0 (saturated) or 3 (triply unsaturated)"
    
    return True, "Molecule contains a chromanol core (chroman-6-ol) with an appropriate isoprenoid side chain (tocol)"

# For testing when run as a script (example with some SMILES):
if __name__ == "__main__":
    test_smiles_list = [
        # True positives (beta-tocopherol, I(3)-Tocotrienol, etc.)
        "CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2c(C)c(O)cc(C)c2O1",  # beta-tocopherol
        "O1C(CCC=2C1=C(C(=C(O)C2)C)C)(CCC=C(CCC=C(CCC=C(C)C)C)C)C",         # I(3)-Tocotrienol
    ]
    for s in test_smiles_list:
        result, reason = is_tocol(s)
        print(f"SMILES: {s}")
        print(f"Result: {result}, Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:39437',
                          'name': 'tocol',
                          'definition': 'A chromanol with a chroman-6-ol '
                                        'skeleton that is substituted at '
                                        'position 2 by a saturated or '
                                        'triply-unsaturated hydrocarbon chain '
                                        'consisting of three isoprenoid units.',
                          'parents': ['CHEBI:23229'],
                          'xrefs': ['CAS:119-98-2', 'Reaxys:1436460'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 139,
                           'log_lines_of_code': 4.9344739331306915,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
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
                                                 4,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 1,
                                                 2,
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
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'add',
                                                 'update',
                                                 'GetIsAromatic',
                                                 'GetSymbol',
                                                 'GetIdx',
                                                 'pop',
                                                 'GetEndAtomIdx',
                                                 'intersection',
                                                 'append',
                                                 'GetNeighbors',
                                                 'union',
                                                 'GetAtomWithIdx',
                                                 'GetBonds',
                                                 'GetAtomicNum',
                                                 'GetBondBetweenAtoms',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'GetBeginAtomIdx',
                                                 'MolFromSmiles',
                                                 'GetBondType'],
                           'methods_called_count': 20,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_tocol(smiles: str):',
                                       'ring_has_ox_substituent(ring):',
                                       'ring_is_aromatic(ring):',
                                       'extract_side_chain(start_idx):'],
                           'defs_count': 4,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True',
                                          'False',
                                          'all(mol.GetAtomWithIdx(idx).GetIsAromatic() '
                                          'for idx in ring)',
                                          'False, "Chromanol core (fused '
                                          'aromatic and heterocyclic rings) '
                                          'not found"',
                                          'False, "Side chain attachment point '
                                          'on the chromanol core not found"',
                                          'None, "Side chain is cyclic '
                                          '(contains ring atoms)"',
                                          'side_chain, None',
                                          'False, f"Error in side chain '
                                          'extraction: {err}"',
                                          'False, f"Side chain has '
                                          '{chain_carbons} carbons; expected '
                                          'between 12 and 17 for three '
                                          'isoprenoid units"',
                                          'False, f"Side chain has '
                                          '{chain_double_bonds} C=C double '
                                          'bonds; expected 0 (saturated) or 3 '
                                          '(triply unsaturated)"',
                                          'True, "Molecule contains a '
                                          'chromanol core (chroman-6-ol) with '
                                          'an appropriate isoprenoid side '
                                          'chain (tocol)"'],
                           'returns_count': 12,
                           'complexity': 9.186894786626137},
    'message': '\n'
               'Attempt failed: F1 score of 0.6896551724137931 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2c(C)c(O)cc(C)c2O1 '
               'NAME: beta-tocopherol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'O1C(CCC=2C1=C(C(=C(O)C2)C)C)(CCC=C(CCC=C(CCC=C(C)C)C)C)C NAME: '
               'I(3)-Tocotrienol REASON: CORRECT Molecule contains a chromanol '
               'core (chroman-6-ol) with an appropriate isoprenoid side chain '
               '(tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@H](C)CCC[C@@]1(C)CCC2=C(C)C(O)=C(C)C(C)=C2O1 '
               'NAME: (S,S,R)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: CC(C)CCCC(C)CCCC(C)CCCC1(C)Oc2c(C)c(C)c(O)cc2C=C1 '
               'NAME: dehydro-gamma-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC[C@]1(C)CCc2c(C)c(O)c(C)c(C)c2O1 '
               'NAME: alpha-tocotrienol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@@]1(C)CCC2=C(C)C(O)=C(C)C(C)=C2O1 '
               'NAME: (S,R,R)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC[C@]1(C)CCc2c(C)c(O)cc(C)c2O1 '
               'NAME: beta-tocotrienol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2cc(O)cc(C)c2O1 '
               'NAME: delta-tocopherol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               '[H][C@@]1(CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)CCc2cc(O)ccc2O1 '
               'NAME: didesmethyl tocotrienol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC[C@]1(C)CCc2cc(O)ccc2O1 NAME: '
               'desmethyl tocotrienol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@H](C)CCC[C@@H](C)CCC[C@@]1(C)CCC2=C(C)C(O)=C(C)C(C)=C2O1 '
               'NAME: (S,R,S)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@H](C)CCC[C@]1(C)CCC2=C(C)C(O)=C(C)C(C)=C2O1 '
               'NAME: (R,S,R)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@H](C)CCC[C@H](C)CCC[C@]1(C)CCC2=C(C)C(O)=C(C)C(C)=C2O1 '
               'NAME: (R,S,S)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: O1C(CCCC(CCCC(CCCC(C)C)C)C)(CCC2=C1C(=CC(O)=C2C)C)C '
               'NAME: 2,5,8-Trimethyl-2-(4,8,12-trimethyltridecyl)-6-chromanol '
               'REASON: CORRECT Molecule contains a chromanol core '
               '(chroman-6-ol) with an appropriate isoprenoid side chain '
               '(tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2cc(O)c(C)c(C)c2O1 '
               'NAME: gamma-tocopherol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC[C@]1(C)CCc2cc(O)cc(C)c2O1 '
               'NAME: delta-tocotrienol REASON: CORRECT Molecule contains a '
               'chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2c(C)c(O)c(C)c(C)c2O1 '
               'NAME: (R,R,R)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'O1[C@](CCCC(CCCC(CCCC(C)C)C)C)(CCC2=C1C(=CC(O)=C2C)C)C NAME: '
               '(2R)-2,5,8-Trimethyl-2-(4,8,12-trimethyltridecyl)chroman-6-ol '
               'REASON: CORRECT Molecule contains a chromanol core '
               '(chroman-6-ol) with an appropriate isoprenoid side chain '
               '(tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@H](C)CCC[C@@H](C)CCC[C@]1(C)CCC2=C(C)C(O)=C(C)C(C)=C2O1 '
               'NAME: (R,R,S)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               ' * SMILES: '
               'CC(C)CCC[C@H](C)CCC[C@H](C)CCC[C@@]1(C)CCc2c(C)c(O)c(C)c(C)c2O1 '
               'NAME: (S,S,S)-alpha-tocopherol REASON: CORRECT Molecule '
               'contains a chromanol core (chroman-6-ol) with an appropriate '
               'isoprenoid side chain (tocol)\n'
               'False positives: SMILES: '
               'O1C(CCCCCCCCCCCCC)CC2=C(C1=O)C(O)=CC=C2 NAME: '
               '(R)-3,4-Dihydro-8-hydroxy-3-tridecyl-1H-2-benzopyran-1-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains a chromanol core '
               '(chroman-6-ol) with an appropriate isoprenoid side chain '
               '(tocol)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\C[C@@]12Oc3cc(O)cc(O)c3C(=O)[C@]1(O)Oc1cc(O)ccc21 '
               'NAME: sanggenol H REASON: WRONGLY CLASSIFIED Molecule contains '
               'a chromanol core (chroman-6-ol) with an appropriate isoprenoid '
               'side chain (tocol)\n'
               ' * SMILES: '
               'O1C(CCC2=C1C=CC(O)=C2)CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C NAME: '
               '(R)-3,4-Dihydro-2-(4,8,12-trimethyl-3,7,11-tridecatrienyl)-2H-1-benzopyran-6-ol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a chromanol core '
               '(chroman-6-ol) with an appropriate isoprenoid side chain '
               '(tocol)\n'
               ' * SMILES: '
               'O1C(CCC2=C1C=CC(O)=C2)(CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)C '
               'NAME: '
               '(R)-3,4-Dihydro-2-methyl-2-(4,8,12-trimethyl-3,7,11-tridecatrienyl)-2H-1-benzopyran-6-ol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a chromanol core '
               '(chroman-6-ol) with an appropriate isoprenoid side chain '
               '(tocol)\n'
               'False negatives: SMILES: '
               'O1[C@](CCC=2C1=C(C(=C(O)C2)C)C)(CC/C=C(/CC/C=C(/CC/C=C(/CO)\\C)\\C)\\C)C '
               "NAME: 13'-Hydroxy-gamma-tocotrienol REASON: MISSED Error in "
               'side chain extraction: Side chain contains non-carbon atoms\n'
               ' * SMILES: '
               'O1C(CCCC(CCCC(CCCC(C)C)C)C)(CCC2=C1C(=C(C(OC(=O)C)=C2C)C)C)C '
               'NAME: DL-alpha-Tocopherol acetate REASON: MISSED Chromanol '
               'core (fused aromatic and heterocyclic rings) not found\n'
               ' * SMILES: '
               'O1C(CCCC(CCCC(CCCC(C)C)C)C)(CCC2=C1C(=C(C(OC(=O)CCC(OCCO)=O)=C2C)C)C)C '
               'NAME: Tocophersolan REASON: MISSED Chromanol core (fused '
               'aromatic and heterocyclic rings) not found\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(=C/CC\\C(C)=C\\CC[C@]1(C)Oc2c(C)cc(O)cc2C=C1)C(O)=O '
               'NAME: (S)-Sargachromenol REASON: MISSED Error in side chain '
               'extraction: Side chain contains non-carbon atoms\n'
               ' * SMILES: '
               'O1[C@@](CCC2=C1C(=CC(O)=C2)C)(CC/C=C(/CC/C=C(/CC/C=C(\\C)/C(O)=O)\\C)\\C)C '
               'NAME: '
               '(2e,6e,10e)-13-[(2r)-6-hydroxy-2,8-dimethyl-3,4-dihydrochromen-2-yl]-2,6,10-trimethyltrideca-2,6,10-trienoic '
               'acid REASON: MISSED Error in side chain extraction: Side chain '
               'contains non-carbon atoms\n'
               ' * SMILES: '
               'CC1=C(C(=C2CCC(OC2=C1C)(C)CCCC(C)CCCC(C)CCCC(C)C)C)O NAME: '
               '2,5,7,8-tetramethyl-2-(4,8,12-trimethyltridecyl)-3,4-dihydro-2H-1-benzopyran-6-ol '
               'REASON: MISSED Side chain has 1 carbons; expected between 12 '
               'and 17 for three isoprenoid units\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2c(C)c(OC(C)=O)c(C)c(C)c2O1 '
               'NAME: alpha-Tocopherol acetate REASON: MISSED Chromanol core '
               '(fused aromatic and heterocyclic rings) not found\n'
               ' * SMILES: '
               'C/C(/CC/C=C(\\C)/C(O)=O)=C/CC/C(/C)=C\\CC[C@]1(C)CCC=2C(C)=C(O)C(C)=C(C)C2O1 '
               "NAME: 13'-carboxy-alpha-tocotrienol REASON: MISSED Error in "
               'side chain extraction: Side chain contains non-carbon atoms\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@]1(C)CCc2c(C)c(OC(=O)\\C=C(C)\\C=C\\C=C(C)\\C=C\\C3=C(C)CCCC3(C)C)c(C)c(C)c2O1 '
               'NAME: Tocoretinate REASON: MISSED Chromanol core (fused '
               'aromatic and heterocyclic rings) not found\n'
               ' * SMILES: '
               'C/C(/CC/C=C(\\C)/C(O)=O)=C\\CC/C(/C)=C/CC[C@]1(C)CCC=2C=C(O)C(C)=C(C)C2O1 '
               "NAME: 13'-carboxy-gamma-tocotrienol REASON: MISSED Error in "
               'side chain extraction: Side chain contains non-carbon atoms\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Chromanol core (fused aromatic '
                                               'and heterocyclic rings) not '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CC1=C(C(=C2CCC(OC2=C1C)(C)CCCC(C)CCCC(C)CCCC(C)C)C)O',
                                      'name': '2,5,7,8-tetramethyl-2-(4,8,12-trimethyltridecyl)-3,4-dihydro-2H-1-benzopyran-6-ol',
                                      'reason': 'Side chain has 1 carbons; '
                                                'expected between 12 and 17 '
                                                'for three isoprenoid units'}],
    'attempt': 3,
    'reasoning': 'Below is one possible revised solution. In our reasoning we '
                 'noticed that the previous code was too strict in two ways. '
                 'First, the detection of the fused “chromanol” core (the '
                 'aromatic ring plus the second saturated ring) was missing '
                 'many derivatized cores. We therefore relaxed the –OH '
                 'requirement into a requirement for a suitable oxygen '
                 'substituent attached via a single bond. Second, the '
                 'side‐chain extraction was aborted as soon as any non‐carbon '
                 'atom was encountered. Some tocols contain a hydroxyl or even '
                 'a carboxyl group in the side chain. In the new version we '
                 '“walk” the attached substituent as long as it is acyclic '
                 '(not in any ring) but we do not forbid heteroatoms. Finally, '
                 'we count only the carbon atoms (and double bonds between '
                 'carbons) when validating the side chain length and '
                 'unsaturation. (There are many ways to solve the problem; '
                 'this is one possible approach.)\n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 10,
    'num_true_negatives': 142256,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.7674418604651163,
    'recall': 0.9705882352941176,
    'f1': 0.8571428571428571,
    'accuracy': 0.9999226985242445,
    'negative_predictive_value': 0.99999297046894}