"""
Classifies: CHEBI:72544 flavonoids
"""
"""
Classifies: Flavonoids (a superclass comprising various flavonoid‐related chemotypes)
Definition (heuristic): Organic molecules whose aglycone is based on a phenyl‐substituted 
1-phenylpropane (typically a C15 or C16 skeleton) and often contains a characteristic benzopyrone 
or chalcone fragment.
Note: Because of the variability of glycosylation and other modifications the classification is heuristic.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold

def remove_sugars(mol):
    """
    Attempts to remove sugar rings from a molecule.
    This is done iteratively: any 5- or 6-membered ring that is non‐aromatic
    and is “isolated” (not fused to an aromatic ring) is removed.
    (This is heuristic and may over- or under-remove sugar-like fragments.)
    """
    # We loop until no more removals occur.
    mol_work = Chem.Mol(mol)
    removal_occurred = True
    while removal_occurred:
        removal_occurred = False
        ri = mol_work.GetRingInfo()
        sugar_indices = set()
        for ring in ri.AtomRings():
            ring_atoms = [mol_work.GetAtomWithIdx(idx) for idx in ring]
            n_atoms = len(ring)
            # Only consider rings that are not aromatic (sugars are aliphatic) 
            if any(atom.GetIsAromatic() for atom in ring_atoms):
                continue
            if n_atoms not in (5, 6):
                continue
            # Heuristic: if the ring atoms are mostly C and O, and at most one non C/O
            atom_syms = [atom.GetSymbol() for atom in ring_atoms]
            if all(sym in ('C','O') for sym in atom_syms):
                # Also require that none of these atoms are shared with an aromatic ring outside
                # (if fused with an aromatic ring, we expect it to be part of the flavonoid core)
                is_fused = False
                for idx in ring:
                    atom = mol_work.GetAtomWithIdx(idx)
                    for nb in atom.GetNeighbors():
                        if nb.GetIsAromatic() and nb.GetIdx() not in ring:
                            is_fused = True
                            break
                    if is_fused:
                        break
                if not is_fused:
                    sugar_indices.update(ring)
        if sugar_indices:
            # Remove atoms in descending order
            rw_mol = Chem.RWMol(mol_work)
            for idx in sorted(sugar_indices, reverse=True):
                try:
                    rw_mol.RemoveAtom(idx)
                except Exception:
                    pass
            mol_work = rw_mol.GetMol()
            Chem.SanitizeMol(mol_work, catchErrors=True)
            removal_occurred = True
    # After removal, if multiple fragments exist, keep the largest.
    frags = Chem.GetMolFrags(mol_work, asMols=True, sanitizeFrags=True)
    if frags:
        mol_work = max(frags, key=lambda m: rdMolDescriptors.CalcExactMolWt(m))
    return mol_work

def is_flavonoids(smiles: str):
    """
    Determines if a molecule is flavonoid-like based on its SMILES string.
    
    The algorithm works as follows:
      1. Parse the SMILES string.
      2. Remove putative sugar moieties iteratively.
      3. Search for one or both of two substructure motifs:
           - A benzopyrone/flavone motif: e.g. c1ccc2oc(=O)cc2c1
           - A chalcone-like fragment: e.g. an aromatic ring connected to a carbonyl and a short chain.
      4. Compute the Murcko scaffold of the sugar-removed aglycone and check:
           - That it contains no nitrogen atoms (most flavonoids are N-free)
           - That the number of carbon atoms is in a “flavonoid‐like” range (roughly 15–22)
           - That at least two ring systems remain.
      5. If either the motif is found or the Murcko scaffold criteria are met, classify as flavonoid.
    
    Args:
      smiles (str): SMILES string of the molecule.
    
    Returns:
      bool: True if the molecule is flavonoid-like, False otherwise.
      str: Reason for classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Remove putative sugars from the molecule.
    aglycone = remove_sugars(mol)

    # Count aromatic rings in the aglycone.
    ri = aglycone.GetRingInfo()
    aromatic_rings = 0
    for ring in ri.AtomRings():
        if all(aglycone.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            aromatic_rings += 1

    # Define two SMARTS patterns:
    # (a) Flavone motif (a benzopyrone): common in flavonoids.
    flavone_smarts = "c1ccc2oc(=O)cc2c1"
    flavone_pattern = Chem.MolFromSmarts(flavone_smarts)
    # (b) Chalcone-like fragment: an aromatic ring attached to a carbonyl and an sp2 carbon.
    chalcone_smarts = "c1ccc(cc1)C(=O)[C;!R]"  # [C;!R] indicates a non-ring carbon after the carbonyl.
    chalcone_pattern = Chem.MolFromSmarts(chalcone_smarts)
    
    match_flavone = aglycone.HasSubstructMatch(flavone_pattern)
    match_chalcone = aglycone.HasSubstructMatch(chalcone_pattern)
    motif_found = match_flavone or match_chalcone

    # Compute the Murcko scaffold (the “core” framework) from the aglycone.
    try:
        scaffold = MurckoScaffold.GetScaffoldForMol(aglycone)
    except Exception as e:
        return False, f"Error computing Murcko scaffold: {str(e)}"

    # Count carbon and oxygen atoms in the scaffold.
    scaffold_carbons = sum(1 for atom in scaffold.GetAtoms() if atom.GetAtomicNum() == 6)
    scaffold_oxygens = sum(1 for atom in scaffold.GetAtoms() if atom.GetAtomicNum() == 8)
    # Check for nitrogen atoms – flavonoid cores are usually nitrogen-free.
    if any(atom.GetAtomicNum() == 7 for atom in scaffold.GetAtoms()):
        return False, "Aglycone scaffold contains nitrogen, which is unusual in flavonoids."

    # Count number of rings in the scaffold.
    scaffold_ri = scaffold.GetRingInfo()
    scaffold_ring_count = scaffold_ri.NumRings()

    # Use a relaxed set of conditions on the Murcko scaffold.
    scaffold_ok = (15 <= scaffold_carbons <= 22) and (scaffold_ring_count >= 2)
    
    # Formulate the reason based on our observations.
    if motif_found:
        reason = "Molecule contains a flavonoid substructure motif (flavone or chalcone-like fragment) in its aglycone."
    elif scaffold_ok:
        reason = (f"Molecule’s aglycone Murcko scaffold has {scaffold_carbons} carbons and "
                  f"{scaffold_ring_count} rings, consistent with a C15/C16 flavonoid core (allowing for modifications).")
    else:
        reason = (f"No clear flavonoid features found: motifs found = {motif_found}, "
                  f"scaffold carbons = {scaffold_carbons} (expected between 15 and 22), "
                  f"scaffold ring count = {scaffold_ring_count}.")
        return False, reason

    # Additional sanity check: require that the aglycone has at least 2 aromatic rings.
    if aromatic_rings < 2:
        return False, f"Aglycone only has {aromatic_rings} aromatic rings; flavonoids normally have at least 2."
    
    # Also check that most atoms in the aglycone are typical (C, O and small halogens)
    allowed_atomic_nums = {6, 7, 8, 9, 17, 35}  # C, N, O, F, Cl, Br (N already ruled out in scaffold)
    for atom in aglycone.GetAtoms():
        if atom.GetAtomicNum() > 20 and atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Aglycone contains atom {atom.GetSymbol()} that is unusual in flavonoids."
    
    return True, f"Flavonoid-like: {reason}"

# Example usage:
if __name__ == "__main__":
    # Test with one example (azaleatin)
    test_smiles = "COc1cc(O)cc2oc(-c3ccc(O)c(O)c3)c(O)c(=O)c12"
    result, message = is_flavonoids(test_smiles)
    print(result, message)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:72544',
                          'name': 'flavonoids',
                          'definition': 'Any organic molecular entity whose '
                                        'stucture is based on derivatives of a '
                                        'phenyl-substituted 1-phenylpropane '
                                        'possessing a C15 or C16 skeleton, or '
                                        'such a structure which is condensed '
                                        'with a C6-C3 lignan precursors. The '
                                        "term is a 'superclass' comprising all "
                                        'members of the classes of flavonoid, '
                                        'isoflavonoid, neoflavonoid, '
                                        'chalcones, dihydrochalcones, aurones, '
                                        'pterocarpan, coumestans, rotenoid, '
                                        'flavonolignan, homoflavonoid and '
                                        'flavonoid oligomers. Originally '
                                        'restricted to natural products, the '
                                        'term is also applied to synthetic '
                                        'compounds related to them.',
                          'parents': ['CHEBI:25806', 'CHEBI:50860'],
                          'xrefs': ['Wikipedia:Flavonoids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 133,
                           'log_lines_of_code': 4.890349128221754,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 3,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 1,
                                                 0,
                                                 1,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from rdkit.Chem.Scaffolds import '
                                          'MurckoScaffold'],
                           'imports_count': 3,
                           'methods_called': [   'GetScaffoldForMol',
                                                 'NumRings',
                                                 'HasSubstructMatch',
                                                 'update',
                                                 'GetIsAromatic',
                                                 'Mol',
                                                 'GetSymbol',
                                                 'GetMol',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'GetMolFrags',
                                                 'SanitizeMol',
                                                 'GetNeighbors',
                                                 'RemoveAtom',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'CalcExactMolWt',
                                                 'RWMol',
                                                 'AtomRings',
                                                 'GetRingInfo',
                                                 'MolFromSmiles'],
                           'methods_called_count': 22,
                           'smarts_strings': [   'flavone_smarts',
                                                 'chalcone_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['remove_sugars(mol):'],
                           'defs_count': 1,
                           'returns': [   'mol_work',
                                          'False, "Invalid SMILES string"',
                                          'False, f"Error computing Murcko '
                                          'scaffold: {str(e)}"',
                                          'False, "Aglycone scaffold contains '
                                          'nitrogen, which is unusual in '
                                          'flavonoids."',
                                          'False, reason',
                                          'False, f"Aglycone only has '
                                          '{aromatic_rings} aromatic rings; '
                                          'flavonoids normally have at least '
                                          '2."',
                                          'False, f"Aglycone contains atom '
                                          '{atom.GetSymbol()} that is unusual '
                                          'in flavonoids."',
                                          'True, f"Flavonoid-like: {reason}"'],
                           'returns_count': 8,
                           'complexity': 8.578069825644352},
    'message': '\n'
               'Attempt failed: F1 score of 0.49375459221160906 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O1C(CC(=O)C=2C1=C(CC=C(C)C)C(O)=CC2O)C3=C(OC)C=C(OC)C=C3OC '
               'NAME: Heteroflavanone C REASON: CORRECT Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: O(C1=CC(O)=C(C(=O)CC(=O)C2=CC=CC=C2)C(O)=C1)C NAME: '
               "2',6',beta-Trihydroxy-4'-methoxychalcone REASON: CORRECT "
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O1C2=C(C(=O)C(OC(=O)/C(/C)=C\\C)=C1C3=CC(OC)=C(OC)C=C3)C(O)=CC(O)=C2OC '
               'NAME: Flaccidine REASON: CORRECT Flavonoid-like: Molecule has '
               'a Murcko scaffold (aglycone) with 15 carbons, consistent with '
               'a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1C2=C(C/C=C(/CO)\\C)C(O)=CC(O)=C2C(=O)C(C3=C(O)C=C(O)C=C3)=C1 '
               'NAME: 2,3-Dehydrokievitol REASON: CORRECT Flavonoid-like: '
               'Molecule has a Murcko scaffold (aglycone) with 15 carbons, '
               'consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1OC=2C3=C(OC(CC3=O)C4=CC=C(O)C=C4)C=C(O)C2O)CO '
               'NAME: Carthamidin 5-glucoside REASON: CORRECT Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O1C(C=CC=2C1=C(CC=C(C)C)C(O)=C(C2)C(=O)/C=C/C3=CC=CC=C3)(C)C '
               'NAME: Spinochalcone C REASON: CORRECT Flavonoid-like: Molecule '
               'contains a flavonoid motif (benzopyran or chalcone-like '
               'fragment) in its aglycone.\n'
               ' * SMILES: COc1cc(O)cc2oc(-c3ccc(O)c(O)c3)c(O)c(=O)c12 NAME: '
               'azaleatin REASON: CORRECT Flavonoid-like: Molecule has a '
               'Murcko scaffold (aglycone) with 15 carbons, consistent with a '
               'C15/C16 flavonoid core.\n'
               ' * SMILES: '
               '[H][C@@]1(CC=CC(=O)O1)C[C@@H]1C[C@@]2([H])C[C@@](O1)(Oc1c(C(=O)\\C=C\\c3ccccc3)c(O)cc(O)c21)\\C=C\\c1ccccc1 '
               'NAME: obochalcolactone REASON: CORRECT Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O1C(=C(C\\C=C(\\CCC=C(C)C)/C)C(=O)C2=C1C=C(O)C=C2)C3=C(O)C=C(O)C=C3 '
               'NAME: Rubraflavone A REASON: CORRECT Flavonoid-like: Molecule '
               'has a Murcko scaffold (aglycone) with 15 carbons, consistent '
               'with a C15/C16 flavonoid core.\n'
               ' * SMILES: COc1cc(O)c(cc1O)-c1oc2c(OC)c(OC)ccc2c(=O)c1OC NAME: '
               'diplotrin A REASON: CORRECT Flavonoid-like: Molecule has a '
               'Murcko scaffold (aglycone) with 15 carbons, consistent with a '
               'C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1C(CC=2C1=C3CC(OC3=C4C2OC(CC4=O)C5=CC=C(O)C=C5)C(O)(C)C)C(O)(C)C '
               'NAME: Lonchocarpol E REASON: CORRECT Flavonoid-like: Molecule '
               'contains a flavonoid motif (benzopyran or chalcone-like '
               'fragment) in its aglycone.\n'
               ' * SMILES: '
               'O1C(C2=CC(=C(O)C(=C2)CC=C(C)C)CC=C(C)C)CC(=O)C3=C1C=C(O)C=C3 '
               'NAME: Abyssinone IV REASON: CORRECT Flavonoid-like: Molecule '
               'contains a flavonoid motif (benzopyran or chalcone-like '
               'fragment) in its aglycone.\n'
               ' * SMILES: COC1=CC=CC=C1C2CC(C=3C(=CC4=C(C3OC)OCO4)O2)O NAME: '
               '2-methoxy-11-(2-methoxyphenyl)-4,6,10-trioxatricyclo[7.4.0.0,3,7]trideca-1,3(7),8-trien-13-ol '
               'REASON: CORRECT Flavonoid-like: Molecule has a Murcko scaffold '
               '(aglycone) with 16 carbons, consistent with a C15/C16 '
               'flavonoid core.\n'
               ' * SMILES: '
               'O1C2=C(C(OC)=C(OC)C(O)=C2)C(=O)C=C1C3=CC(OC)=C(OC)C=C3 NAME: '
               "7-Hydroxy-3',4',5,6-tetramethoxyflavone REASON: CORRECT "
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '15 carbons, consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'C1(=C(C(C2=C(C=C(C=C2O1)OC)O)=O)OC)C3=CC(=C(OC)C=C3)OC NAME: '
               "5-hydroxy-3,3',4',7-tetramethoxyflavone REASON: CORRECT "
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '15 carbons, consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: OC1Cc2ccccc2OC1c1ccccc1 NAME: Favan-3-ol REASON: '
               'CORRECT Flavonoid-like: Molecule has a Murcko scaffold '
               '(aglycone) with 15 carbons, consistent with a C15/C16 '
               'flavonoid core.\n'
               ' * SMILES: '
               'C12=CC(=CC(=C2C[C@@H]([C@@H](O1)C=3C=C(C(=CC3)O)O)OC(=O)C(CO)C)O)O '
               "NAME: epicatechin 3'-O-3-hydroxy-2-methyl-propanoate REASON: "
               'CORRECT Flavonoid-like: Molecule has a Murcko scaffold '
               '(aglycone) with 15 carbons, consistent with a C15/C16 '
               'flavonoid core.\n'
               ' * SMILES: OC(CC1=CC=C(O)C=C1)C(=O)C2=C(O)C=C(O)C=C2O NAME: '
               'Nubigenol REASON: CORRECT Flavonoid-like: Molecule contains a '
               'flavonoid motif (benzopyran or chalcone-like fragment) in its '
               'aglycone.\n'
               ' * SMILES: '
               'O1C2=C(C(=O)C(C3=CC(OCC=C(C)C)=C(OCC=C(C)C)C=C3)=C1)C(OC)=CC(OC)=C2 '
               'NAME: Glabrescione B REASON: CORRECT Flavonoid-like: Molecule '
               'has a Murcko scaffold (aglycone) with 15 carbons, consistent '
               'with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1C=2C(=C(O)C=3OCOC3C2)C(=O)C(OC)=C1C4=CC(O)=C(O)C=C4 NAME: '
               "5,3',4'-Trihydroxy-3-methoxy-6,7-methylenedioxyflavone REASON: "
               'CORRECT Flavonoid-like: Molecule has a Murcko scaffold '
               '(aglycone) with 16 carbons, consistent with a C15/C16 '
               'flavonoid core.\n'
               ' * SMILES: O1[C@@H](CCC2=C1C=C(OC)C=C2OC)C3=CC(OC)=C(O)C=C3 '
               "NAME: (2S)-4'-Hydroxy-5,7,3'-trimethoxyflavan REASON: CORRECT "
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '15 carbons, consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1C2=C(C=3C(OC2)=CC=4OCOC4C3)C(=O)C5=C1C=C6OC=CC6=C5 NAME: '
               'Dehydrodolineone REASON: CORRECT Flavonoid-like: Molecule '
               'contains a flavonoid motif (benzopyran or chalcone-like '
               'fragment) in its aglycone.\n'
               ' * SMILES: '
               'Oc1ccc(cc1)[C@@H]1Oc2cc(O)cc(O)c2C(=O)[C@H]1c1c(O)cc(O)c2c1oc(cc2=O)-c1ccc(O)c(O)c1 '
               'NAME: (+)-morelloflavone REASON: CORRECT Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: COc1ccc2c(O[C@H]3c4ccc(O)cc4OC[C@@]23O)c1CC=C(C)C '
               'NAME: Cristacarpin REASON: CORRECT Flavonoid-like: Molecule '
               'has a Murcko scaffold (aglycone) with 15 carbons, consistent '
               'with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1C=2C(=C(O)C(CC=C(C)C)=C(OC)C2)C(=O)C(C3=CC=C(O)C=C3)=C1 '
               'NAME: Gancaonin G REASON: CORRECT Flavonoid-like: Molecule has '
               'a Murcko scaffold (aglycone) with 15 carbons, consistent with '
               'a C15/C16 flavonoid core.\n'
               'False positives: SMILES: '
               'O=C1C2=C(O)C=CC3=C2[C@@]4(OC=5C=CC=C6C5[C@@](O3)([C@H](O)C[C@@H]6O)O4)[C@H]7[C@@H]1O7 '
               'NAME: Ymf 1029B REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(=C(CC(=O)O)C=C2C(=O)C=3C1=C(O)C=CC3)C(=O)CC(=O)N '
               'NAME: Protetrone REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'C1(OC(C)(C)C(O[Al](OC(=O)C(C)(C)OC2=CC=C(C=C2)Cl)O)=O)=CC=C(C=C1)Cl '
               'NAME: Aluminum clofibrate REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '16 carbons, consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O=C1C=2C3=C(C(O)=CC(=C3[C@H](C)[C@H](C2C4=C(O)C=CC=C4O)[C@@H](CC(=O)C5=C(O)C=CC=C5O)C)O)C(=C1)O '
               'NAME: (+)-dalmanol C REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C2=C(OC(C1)(C(=O)OC)[C@H]3OC(=O)C[C@@H]3C)C(C4=C5OC(C(=O)OC)([C@@H]6OC(=O)C[C@@H]6C)CC(C5=C(O)C=C4)=O)=CC=C2O '
               'NAME: Paecilin C REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C(C2=C(C(O)=CC=C2)C(=O)C3=C(O)C=C(C(=O)OC)C=C3O)=C(C4=C(O)C=C(C(=O)OC)C=C4O)C5=C1C=CC=C5O '
               'NAME: Alternaphenol A REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=3C(=C(C(O)=CC3C)C[C@@H](C(=O)OCC)C(=O)OC)C=C2[C@@H](O)CC1 '
               'NAME: Alokicenone G REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'COc1cc2O[C@H]3O[C@H]4O[C@H]4[C@H]3c2c2oc(=O)c3C(=O)CCc3c12 '
               'NAME: Aflatoxin B1-endo-8,9-epoxide REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '16 carbons, consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: O1C2=C(C(OC)=C(C=C2)C(=O)C)C=C1 NAME: '
               '1-(4-methoxy-1-benzofuran-5-yl)ethan-1-one REASON: WRONGLY '
               'CLASSIFIED Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: OCC(C(CC1=CC(O)=CC=C1)CO)CC2=CC(O)=C(O)C=C2 NAME: '
               '4-Hydroxyenterodiol REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule has a Murcko scaffold (aglycone) with 16 carbons, '
               'consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'COc1c(C)c(O)c(Cc2c(O)c(C)c(OC)c(C(=O)C(C)C)c2O)c(O)c1C(=O)C(C)C '
               'NAME: alpha-Kosin REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1OC(=C2C(=O)O[C@@H](C2=C1)C)C=CC3=CC(O)=C(O)C(=C3)O NAME: '
               'Clostyrylpyrone A REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule has a Murcko scaffold (aglycone) with 15 carbons, '
               'consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O1C(=O)C([C@H](CC(=O)C)C2=CC=CC=C2)=C(O)C3=C1C=C(O)C=C3 NAME: '
               'R-7-Hydroxywarfarin REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule has a Murcko scaffold (aglycone) with 16 carbons, '
               'consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: COc1cc([O-])c2c(c1)oc(-c1ccc(O)c(O)c1)c(OC)c2=O '
               "NAME: 3',4',5-trihydroxy-3,7-dimethoxyflavone(1-) REASON: "
               'WRONGLY CLASSIFIED Flavonoid-like: Molecule has a Murcko '
               'scaffold (aglycone) with 15 carbons, consistent with a C15/C16 '
               'flavonoid core.\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OCCCc1cc(OC)c2oc(cc2c1)-c1ccc2OCOc2c1 '
               'NAME: egonol-9(Z),12(Z)linoleate REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C3=C1[C@H](O[C@H](C3)C)C)C(=O)C=4OC5=C(C4C2=O)C(OC)=CC6=C(O)[C@@H]7C[C@H](C)O[C@@H]([C@]7(C(=C56)O)O)C '
               'NAME: Cardinalin-4 REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C(=O)C2=C(O)C=CC=C2C(=C1C3=C(O)C=C(CC)C=C3C(=O)OC)O NAME: '
               'WS-5995-D REASON: WRONGLY CLASSIFIED Flavonoid-like: Molecule '
               'contains a flavonoid motif (benzopyran or chalcone-like '
               'fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C=3C1=C(C(O)=C(C)C3)C4=C5C(=O)C6=C([C@H](O)[C@@H](O)[C@]([C@@H]6O)(O)C)C(C5=C(O)C=C4OC)=O)C(C7=C8C(=O)C9=C([C@H](O)[C@@H](O)[C@]([C@@H]9O)(O)C)C(C8=C(O)C=C7OC)=O)=C(OC)C=C2O '
               'NAME: Stemphylanthranol A REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C(OC)C1=C(C(OC)=CC(=C1)C2=CC=3OC([C@@H](OC(C=C)(C)C)COC3C=C2)(C)C)C '
               'NAME: Favolasin K REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule has a Murcko scaffold (aglycone) with 15 carbons, '
               'consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=CC=C2C3([C@@]1(O)C(=O)OC)OC=4C=5C(C=CC4)=CC=CC5O3 '
               'NAME: Palmarumycin B8 REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'O=C1C2=C(O[C@]3(C1=CC=4C=C(OC)C(=C(C34)O)O)C)C(O)=C(OC)C=C2CO '
               'NAME: Penicanesone C REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule contains a flavonoid motif '
               '(benzopyran or chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'COc1cc2O[C@H]3O[C@@H](O)[C@H](O)[C@H]3c2c2oc(=O)c3C(=O)CCc3c12 '
               'NAME: Aflatoxin B1 diol REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '16 carbons, consistent with a C15/C16 flavonoid core.\n'
               ' * SMILES: '
               'O=C1C(OC)=C(C(=O)C=2C1=C(O)C3=C(C(=O)C4(O)C5C3OC4(C(O[C@@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@](O)(C(=O)C)CC7)C)CC6)C)C(C5OC8O[C@H]([C@H](O)[C@@H](C8)O)C)O)CCC)C2O)C=9C(OC)=C(OC)C%10=CC=%11CC%12C(O[C@@H]%13O[C@H]([C@H](O)[C@@H](C%13)O)C)C(O)C(C(C%12(C(C%11C(=C%10C9O)O)=O)O)(O)CCC)O[C@@H]%14O[C@@H]([C@@H](O[C@H]%15O[C@@H]([C@@](O)(C(=O)C)CC%15)C)CC%14)C '
               'NAME: Hibarimicin B REASON: WRONGLY CLASSIFIED Flavonoid-like: '
               'Molecule contains a flavonoid motif (benzopyran or '
               'chalcone-like fragment) in its aglycone.\n'
               ' * SMILES: '
               'CO[C@@H]1[C@@H](O)[C@H](C)O[C@@H](Oc2cc3cc4C(=O)[C@@]5(O)[C@H](O)C(OC)=CC(=O)[C@@]5(O)C(=O)c4c(O)c3c(C)c2C(=O)OC)[C@@H]1OC '
               'NAME: '
               '8-demethyl-8-(2,3-O-dimethyl-alpha-L-rhamnosyl)tetracenomycin '
               'C REASON: WRONGLY CLASSIFIED Flavonoid-like: Molecule contains '
               'a flavonoid motif (benzopyran or chalcone-like fragment) in '
               'its aglycone.\n'
               ' * SMILES: '
               'O=C1OC(=CC=2C1=C(O)C=C(O)C2)/C=C/C=C\\[C@H]3O[C@@H]3C[C@H](O)C '
               'NAME: Paraphaeosphaerin A REASON: WRONGLY CLASSIFIED '
               'Flavonoid-like: Molecule has a Murcko scaffold (aglycone) with '
               '15 carbons, consistent with a C15/C16 flavonoid core.\n'
               'False negatives: SMILES: '
               'O(C1[C@@H](O)[C@H](O)C(O[C@]1(C=2C=3OC(=CC(=O)C3C(O)=CC2O)C4=CC=C(O)C=C4)[H])CO)[C@@H]5OC([C@@H](O)[C@H](O)C5O[C@@H]6OC([C@@H](O)[C@H](O)C6O)CO)CO '
               'NAME: Polygonatiin REASON: MISSED No clear flavonoid features '
               'found: neither a benzopyran/chalcone motif was detected nor '
               'was a core with 15 or 16 carbons identified (scaffold carbons '
               '= 30).\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C=C3OC(=C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)C(=O)C3=C(O)C2)C5=CC(O)=C(O)C=C5)CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO '
               'NAME: Quercetin-3-O-beta-D-glucose-7-O-beta-D-gentiobioside '
               'REASON: MISSED No clear flavonoid features found: neither a '
               'benzopyran/chalcone motif was detected nor was a core with 15 '
               'or 16 carbons identified (scaffold carbons = 31).\n'
               ' * SMILES: '
               '[Cl-].O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC=C(O)C=C4)CO '
               'NAME: Pelargonidin 3-galactoside REASON: MISSED No clear '
               'flavonoid features found: neither a benzopyran/chalcone motif '
               'was detected nor was a core with 15 or 16 carbons identified '
               '(scaffold carbons = 20).\n'
               ' * SMILES: '
               'O1[C@@H](OC=2C=3CC[C@H](OC3C=C(O)C2)C4=CC(O)=C(O)C=C4)C(O)[C@@H](O)[C@H](O)C1 '
               'NAME: Viscutin 3 REASON: MISSED No clear flavonoid features '
               'found: neither a benzopyran/chalcone motif was detected nor '
               'was a core with 15 or 16 carbons identified (scaffold carbons '
               '= 20).\n'
               ' * SMILES: '
               'O(C1C(O)C(O)C(OC1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(OC)=C(O)C=C4)C)C5OC(C(O)C(O)C5O)C '
               'NAME: Calendoflaside REASON: MISSED No clear flavonoid '
               'features found: neither a benzopyran/chalcone motif was '
               'detected nor was a core with 15 or 16 carbons identified '
               '(scaffold carbons = 25).\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)OC[C@H]2O[C@H]([C@@H]([C@H]([C@@H]2O)O)O)OC[C@H]3O[C@H]([C@@H]([C@H]([C@@H]3O)O)O)OC[C@H]4O[C@H]([C@@H]([C@H]([C@@H]4O)O)O)OC5=C(OC6=CC(=CC(=C6C5=O)O)O)C=7C=C(C(=CC7)O)O '
               'NAME: quercetin 3-O-gentiotetroside REASON: MISSED No clear '
               'flavonoid features found: neither a benzopyran/chalcone motif '
               'was detected nor was a core with 15 or 16 carbons identified '
               '(scaffold carbons = 38).\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=C(OC)C=3OC(=C(O)C(=O)C3C(O)=C2)C4=CC(OC)=C(O)C=C4)COC(=O)C '
               "NAME: Limocitrin 7-(6''-acetylglucoside) REASON: MISSED No "
               'clear flavonoid features found: neither a benzopyran/chalcone '
               'motif was detected nor was a core with 15 or 16 carbons '
               'identified (scaffold carbons = 20).\n'
               ' * SMILES: '
               'O(C1C(O)C(O)C(OC1OC=2C=C3OC(C4=CC=C(OC5OC(C(O)C(O)C5O)C(O)=O)C=C4)=CC(=O)C3=C(O)C2)C(O)=O)C6OC(C(O)C(O)C6O)C(O)=O '
               'NAME: '
               '6-{4-[7-({6-carboxy-3-[(6-carboxy-3,4,5-trihydroxyoxan-2-yl)oxy]-4,5-dihydroxyoxan-2-yl}oxy)-5-hydroxy-4-oxo-4H-chromen-2-yl]phenoxy}-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: MISSED No clear flavonoid features found: neither '
               'a benzopyran/chalcone motif was detected nor was a core with '
               '15 or 16 carbons identified (scaffold carbons = 30).\n'
               ' * SMILES: '
               'O(C1C(O)[C@@H](O)C(O[C@H]1OC2=C(OC=3C(C2=O)=C(O)C=C(O[C@@H]4OC([C@@H](O)[C@H](O)C4O)CO)C3)C5=CC(OC)=C(O)C=C5)CO)[C@@H]6OC([C@@H](O)C(O)[C@H]6O)CO '
               'NAME: Isorhamnetin 3-glucosyl-(1->2)-galactoside-7-glucoside '
               'REASON: MISSED No clear flavonoid features found: neither a '
               'benzopyran/chalcone motif was detected nor was a core with 15 '
               'or 16 carbons identified (scaffold carbons = 30).\n'
               ' * SMILES: '
               'O1C([C@H](O)C(O)C(O)[C@@H]1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(OC)=C(O)C=C4)CO[C@@H]5OC([C@@H](O)C(O)[C@H]5O)COC(=O)C '
               "NAME: Isorhamnetin 3-(6'''-acetylglucosyl)(1->6)-galactoside "
               'REASON: MISSED No clear flavonoid features found: neither a '
               'benzopyran/chalcone motif was detected nor was a core with 15 '
               'or 16 carbons identified (scaffold carbons = 26).\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Aglycone scaffold contains '
                                               'nitrogen, which is unusual in '
                                               'flavonoids.'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No clear flavonoid features '
                                               'found: motifs found = False, '
                                               'scaffold carbons = 0 (expected '
                                               'between 15 and 22), scaffold '
                                               'ring count = 0.'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Aglycone scaffold contains '
                                               'nitrogen, which is unusual in '
                                               'flavonoids.'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No clear flavonoid features '
                                               'found: motifs found = False, '
                                               'scaffold carbons = 15 '
                                               '(expected between 15 and 22), '
                                               'scaffold ring count = 1.'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No clear flavonoid features '
                                               'found: motifs found = False, '
                                               'scaffold carbons = 11 '
                                               '(expected between 15 and 22), '
                                               'scaffold ring count = 2.'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No clear flavonoid features '
                                               'found: motifs found = False, '
                                               'scaffold carbons = 0 (expected '
                                               'between 15 and 22), scaffold '
                                               'ring count = 0.'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Aglycone scaffold contains '
                                               'nitrogen, which is unusual in '
                                               'flavonoids.'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No clear flavonoid features '
                                               'found: motifs found = False, '
                                               'scaffold carbons = 0 (expected '
                                               'between 15 and 22), scaffold '
                                               'ring count = 0.'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No clear flavonoid features '
                                               'found: motifs found = False, '
                                               'scaffold carbons = 6 (expected '
                                               'between 15 and 22), scaffold '
                                               'ring count = 1.'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CC2=CC=CC=C2',
                                     'name': 'Thr-Phe-His',
                                     'reason': 'Aglycone scaffold contains '
                                               'nitrogen, which is unusual in '
                                               'flavonoids.'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)c([C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)c2oc(cc(=O)c2c1O)-c1ccc(O)c(O)c1',
                                      'name': 'lucenin-2',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 25 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 5.'},
                                  {   'smiles': 'Oc1ccc(cc1)[C@@H]1Oc2cc(O)cc(O)c2C(=O)[C@H]1c1c(O)cc(O)c2c1oc(cc2=O)-c1ccc(O)c(O)c1',
                                      'name': '(+)-morelloflavone',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 30 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 6.'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(O)=C(C3OCC(O)C(O)C3O)C(O)=C4C2OC(=CC4=O)C5=CC=C(O)C=C5',
                                      'name': 'Corymboside',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 25 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 5.'},
                                  {   'smiles': 'O1[C@](C(O[C@@H]2OC[C@@H](O)C(O)C2O)C(O)[C@H](O)[C@@H]1COC(=O)/C=C/C3=CC(OC)=C(O)C=C3)(C=4C=5OC(=CC(=O)C5C(O)=CC4O)C6=CC(O)=C(O)C=C6)[H]',
                                      'name': 'Orientin '
                                              "2''-O-xyloside-6''-ferulate",
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 30 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 5.'},
                                  {   'smiles': 'O1C=2C3=C(C(O)=C1C=4C=C(OC)C(O)=C(O)C4)C=C(OC3=CC(=[OH+])C2)C5=CC=C(O)C=C5',
                                      'name': '7-(3,4-dihydroxy-5-methoxyphenyl)-6,11-dihydroxy-3-(4-hydroxyphenyl)-2?,8-dioxatricyclo[7.3.1.0?,??]trideca-1(13),2,4,6,9,11-hexaen-2-ylium',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 23 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 5.'},
                                  {   'smiles': 'O1C2=C(C(CC1=O)C3=CC=CC=C3)C=4OC(=C(O)C(=O)C4C(O)=C2)C5=CC=CC=C5',
                                      'name': 'lmpk12111648',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 24 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 5.'},
                                  {   'smiles': 'O1C([C@@H](O)CC=2C1=CC(O)=CC2O)C=3C4=CC(C5OC=6C(C[C@@H]5O)=C(O)C=C(O)C6)=CC(=O)C(O)=C4C(O)=C(O)C3',
                                      'name': 'Isoneotheaflavin',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 29 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 6.'},
                                  {   'smiles': 'C1=2C(C=C(OC1=CC(=CC2O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)C=4C=C(OC)C(=C(C4)OC)O[C@H]([C@@H](C5=CC(OC)=C(C=C5)O)O)CO)=O',
                                      'name': 'tricin '
                                              "4'-O-(erythro-beta-guaiacylglyceryl) "
                                              'ether '
                                              '7-O-beta-D-glucopyranoside',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 23 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 4.'},
                                  {   'smiles': 'O1C(C(O)CC2=C1C(C(C(O)CC3=CC(O)=CC=C3)C4=C(O)C=C(O)C=C4)=C(O)C=C2O)C5=CC(OC6OC(C(O)C(O)C6O)C(O)=O)=C(O)C=C5',
                                      'name': '6-(5-{8-[1-(2,4-dihydroxyphenyl)-2-hydroxy-3-(3-hydroxyphenyl)propyl]-3,5,7-trihydroxy-3,4-dihydro-2H-1-benzopyran-2-yl}-2-hydroxyphenoxy)-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 30 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 5.'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)cc(O)c34)c3cc(O)c(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': '(+)-gallocatechin-(4alpha->8)-(-)-epicatechin',
                                      'reason': 'No clear flavonoid features '
                                                'found: motifs found = False, '
                                                'scaffold carbons = 30 '
                                                '(expected between 15 and 22), '
                                                'scaffold ring count = 6.'}],
    'attempt': 2,
    'reasoning': 'Below is one possible revised solution. One idea was to try '
                 'a “two‐prong” approach. First we look for one or two '
                 'flavonoid‐specific substructure patterns (for instance, a '
                 '2‐phenylchromenone “flavone” motif and a chalcone motif). '
                 'Second, we “clean” the molecule by iteratively removing '
                 'likely sugar rings (non\xadaromatic 5– or 6‐membered rings '
                 'that appear to be isolated from the flat flavonoid core) and '
                 'then compute its Murcko scaffold. In the scaffold we then '
                 'count the number of carbons, require that no nitrogen is '
                 'present, and additionally demand that the core appears '
                 '“flavonoid‐like” by having a total of (roughly) 15–22 '
                 'carbons and at least two ring systems. (Many flavonoids '
                 'contain three rings in a C6–C3–C6 arrangement, '
                 'though–especially after sugar removal–the Murcko scaffold '
                 'may merge two of these rings.)  \n'
                 ' \n'
                 'Because the definition is “heuristic” there is no single '
                 'perfect cut‐off. In our revised code we relax the strict '
                 'scaffold carbon counts and add an iterative sugar removal '
                 'step. (Note that this is only one possible solution.)  \n'
                 '\n'
                 'Below is the complete Python program in a single code '
                 'block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3421,
    'num_false_positives': 3526,
    'num_true_negatives': 135028,
    'num_false_negatives': 325,
    'num_negatives': None,
    'precision': 0.4924427810565712,
    'recall': 0.913240790176188,
    'f1': 0.6398578509305154,
    'accuracy': 0.972937456078707,
    'negative_predictive_value': 0.9975988711000126}