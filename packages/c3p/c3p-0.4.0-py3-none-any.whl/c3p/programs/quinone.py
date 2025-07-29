"""
Classifies: CHEBI:36141 quinone
"""
"""
Classifies: quinone
Definition: Compounds having a fully conjugated cyclic dione structure, such as that of benzoquinones,
derived from aromatic compounds by conversion of an even number of -CH= groups into -C(=O)- groups
(with any necessary rearrangement of double bonds). (Polycyclic and heterocyclic analogues are included.)

This improved approach:
  - Uses RDKit’s SSSR (unique rings) to iterate over rings.
  - Only considers rings that are at least 5-membered and are composed entirely of carbon atoms that seem sp2 (or aromatic).
  - For each ring, counts “exocyclic carbonyls”: ring carbon atoms with a C=O bond where the oxygen is not part of the ring.
  - For 6-membered rings (typical quinones), further requires that at least one pair of carbonyls is separated by three bonds along the ring 
    (as in p-benzoquinones). Rings of other sizes only need to have at least two such carbonyl groups.
  - Returns a boolean and an explanatory reason.
"""

from rdkit import Chem
from rdkit.Chem import rdchem

def is_quinone(smiles: str):
    """
    Determines if a molecule is a quinone based on its SMILES string.

    Strategy:
      1. Parse the SMILES.
      2. Get the set of SSSR rings (which represent unique rings even in fused systems).
      3. For each ring with at least 5 atoms:
           - Check that every atom in the ring is carbon and has sp2 geometry or is aromatic.
           - Identify exocyclic carbonyl substituents: for a carbon in the ring, check if it is double‐bonded to an oxygen
             that is not also in the ring.
           - For 6-membered rings, further require that at least one pair of carbonyl-containing atoms is separated by three positions
             (i.e. “para” on the ring) to mirror the classical quinone structure.
           - For rings of other sizes, require at least two carbonyls.
      4. Return True, with a formatted reason if any ring meets these criteria; otherwise return False.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if molecule is classified as a quinone, False otherwise.
        str: Explanation for the classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Obtain SSSR rings (each as an ordered tuple of atom indices)
    ssr_rings = list(Chem.GetSymmSSSR(mol))
    if not ssr_rings:
        return False, "No rings found in molecule"

    for ring in ssr_rings:
        # Only consider rings with at least 5 atoms.
        if len(ring) < 5:
            continue

        # Get the ordered list of atom indices for the ring.
        ring_indices = list(ring)
        
        # Check that every atom is carbon and is sp2 or aromatic.
        all_carbon_sp2 = True
        for idx in ring_indices:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6:
                all_carbon_sp2 = False
                break
            # Check for aromaticity or sp2 hybridization.
            if not (atom.GetIsAromatic() or atom.GetHybridization() == rdchem.HybridizationType.SP2):
                all_carbon_sp2 = False
                break
        if not all_carbon_sp2:
            continue

        # Now look for exocyclic carbonyl groups attached to ring carbons.
        carbonyl_atoms = []  # store indices of ring carbons that bear an external C=O
        for idx in ring_indices:
            atom = mol.GetAtomWithIdx(idx)
            has_carbonyl = False
            for bond in atom.GetBonds():
                # Only consider double bonds.
                if bond.GetBondType() != Chem.BondType.DOUBLE:
                    continue
                nei = bond.GetOtherAtom(atom)
                # Check if neighbor is oxygen.
                if nei.GetAtomicNum() != 8:
                    continue
                # Exclude case where oxygen is part of the same ring.
                if nei.GetIdx() in ring_indices:
                    continue
                has_carbonyl = True
                break
            if has_carbonyl:
                carbonyl_atoms.append(idx)
                
        if len(carbonyl_atoms) < 2:
            continue
        
        # For 6-membered rings, further check that at least one pair of these carbonyl-bearing atoms
        # is separated by 3 positions in the ring ordering (i.e. para relationship).
        if len(ring_indices) == 6:
            # First, try to get an ordering. (Chem.GetSymmSSSR returns rings in arbitrary order,
            # but for a simple cycle we can assume the indices list is cyclically ordered.)
            found_para = False
            # Create a mapping from ring position to atom index.
            # We assume the list order is consistent; if not, we can try to order by connectivity.
            n = 6
            # Find positions of carbonyl atoms in the ring ordering.
            positions = []
            for pos, idx in enumerate(ring_indices):
                if idx in carbonyl_atoms:
                    positions.append(pos)
            # Check all unique pairs to see if cyclic distance is 3.
            for i in range(len(positions)):
                for j in range(i+1, len(positions)):
                    d = abs(positions[i] - positions[j])
                    cyclic_distance = min(d, n - d)
                    if cyclic_distance == 3:
                        found_para = True
                        break
                if found_para:
                    break
            if not found_para:
                continue  # skip this ring if no proper spacing of carbonyls
        
        # Formulate a reason string.
        reason = (f"Found ring with atoms {tuple(ring_indices)}: {len(carbonyl_atoms)} exocyclic carbonyl groups "
                  f"attached to an all-carbon conjugated ring of size {len(ring_indices)}.")
        return True, reason

    return False, "No fully conjugated all‐carbon ring with at least two exocyclic carbonyl groups (with proper spacing in 6‑membered rings) was found."


# Example calls (uncomment to test)
# print(is_quinone("Oc1ccc2C(=O)c3c(O)ccc(O)c3C(=O)c2c1O"))  # quinalizarin (true case)
# print(is_quinone("O=C1C(=C[C@@H]2C=C[C@@H]3CC(N[C@]43[C@@H]2C(=O)C5=C(C(O)=C(C)C(=C5C4=O)O)C([C@@H](C=C[C@H]([C@@H]1C)O)C)=O)=O)CC(C)C"))  # Ansaseomycin A (example false negative in previous attempt)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36141',
                          'name': 'quinone',
                          'definition': 'Compounds having a fully conjugated '
                                        'cyclic dione structure, such as that '
                                        'of benzoquinones, derived from '
                                        'aromatic compounds by conversion of '
                                        'an even number of -CH= groups into '
                                        '-C(=O)- groups with any necessary '
                                        'rearrangement of double bonds '
                                        '(polycyclic and heterocyclic '
                                        'analogues are included).',
                          'parents': ['CHEBI:3992'],
                          'xrefs': ['Wikipedia:Quinone'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 31,
                           'log_lines_of_code': 3.4339872044851463,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
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
                                                 1,
                                                 0,
                                                 0],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem'],
                           'imports_count': 2,
                           'methods_called': ['GetSymmSSSR', 'MolFromSmiles'],
                           'methods_called_count': 2,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_quinone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in molecule"',
                                          'False, "No fully conjugated '
                                          'all‐carbon ring with at least two '
                                          'exocyclic carbonyl groups (with '
                                          'proper spacing in 6‑membered rings) '
                                          'was found."'],
                           'returns_count': 3,
                           'complexity': 2.4867974408970293},
    'message': '\n'
               'Attempt failed: F1 score of 0.5186621425109065 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC(C)=CCc1ccc2[nH]cc(C3=C(O)C(=O)C(=C(O)C3=O)c3c[nH]c4ccccc34)c2c1 '
               'NAME: semicochliodinol A REASON: CORRECT Found ring with atoms '
               '(13, 15, 17, 18, 20, 12): 2 carbonyl groups and 6/6 carbon '
               'atoms (ratio 1.00).\n'
               ' * SMILES: OC1=C2C(=C(O)C(=C1C)C(=O)C)C(=O)C(O)=C(OC)C2=O '
               'NAME: Cordeauxione REASON: CORRECT Found ring with atoms (12, '
               '14, 16, 19, 2, 3): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C2=C3OC(=CC(C3=C(C)C=C2C(=O)C=4C1=C(O)C(=CC4)C5OC(C(OC(=O)C)C(C5)(N(C)C)C)C)=O)C6(OC6C)C '
               'NAME: Saptomycin E REASON: CORRECT Found ring with atoms (1, '
               '16, 15, 13, 12, 2): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: '
               'CC[C@@]1(O)C[C@H](O[C@H]2C[C@H](N)[C@H](O)[C@H](C)O2)c2c(O)c3C(=O)c4c(OC)cccc4C(=O)c3c(O)c2C1 '
               'NAME: 13-deoxydaunorubicin REASON: CORRECT Found ring with '
               'atoms (20, 22, 29, 30, 32, 19): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=C(O[C@H]3O[C@H](CO)[C@H]([C@H]3OC(=O)C)OC(=O)C)C=C2C(=O)C=4C1=C(O)C=C(C)C4 '
               'NAME: '
               '[(2R,3R,4R,5R)-4-acetyloxy-5-(4,5-dihydroxy-7-methyl-9,10-dioxoanthracen-2-yl)oxy-2-(hydroxymethyl)oxolan-3-yl] '
               'acetate REASON: CORRECT Found ring with atoms (1, 28, 27, 25, '
               '24, 2): 2 carbonyl groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'CN1CCN(CC1)C2=C(C(=O)C3=CC=CC=C3C2=O)NS(=O)(=O)C4=CC=CC=C4 '
               'NAME: '
               'N-[3-(4-methyl-1-piperazinyl)-1,4-dioxo-2-naphthalenyl]benzenesulfonamide '
               'REASON: CORRECT Found ring with atoms (9, 11, 16, 17, 7, 8): 2 '
               'carbonyl groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: O=C1C2=C(C(=O)C=C1[C@H]3OC(=O)C[C@H]3O)C(O)=CC=C2 '
               'NAME: Juglomycin A REASON: CORRECT Found ring with atoms (1, '
               '7, 6, 4, 3, 2): 2 carbonyl groups and 6/6 carbon atoms (ratio '
               '1.00).\n'
               ' * SMILES: O=C1C2=C(O)C(O)=C(C(=O)CCCCC)C(=C2C(O)=CC1=O)O '
               'NAME: Quambalarine B REASON: CORRECT Found ring with atoms (1, '
               '20, 19, 17, 16, 2): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: '
               'COc1cc(O)c2C(=O)c3cc4[C@H](O)[C@@H](O[C@@H]5O[C@H](C)[C@H](O)[C@H](O)[C@H]5O)c5cc(C)c(C(=O)NC(C)C(O)=O)c(O)c5-c4c(O)c3C(=O)c2c1 '
               'NAME: Dexylosylbenanomicin A REASON: CORRECT Found ring with '
               'atoms (7, 9, 45, 46, 48, 6): 2 carbonyl groups and 6/6 carbon '
               'atoms (ratio 1.00).\n'
               ' * SMILES: CC(C)=CCc1c(O)cc2C(=O)c3cc(C)cc(O)c3C(=O)c2c1O '
               'NAME: 2-Isoprenylemodin REASON: CORRECT Found ring with atoms '
               '(10, 12, 19, 20, 22, 9): 2 carbonyl groups and 6/6 carbon '
               'atoms (ratio 1.00).\n'
               ' * SMILES: Oc1ccc2C(=O)c3c(O)ccc(O)c3C(=O)c2c1O NAME: '
               'quinalizarin REASON: CORRECT Found ring with atoms (5, 7, 14, '
               '15, 17, 4): 2 carbonyl groups and 6/6 carbon atoms (ratio '
               '1.00).\n'
               ' * SMILES: '
               '[H][C@@]12C[C@]3(O)O[C@@]1(CCCC2(C)C)CC1=C3C(=O)C(C(C)C)=C(OC)C1=O '
               'NAME: komaroviquinone REASON: CORRECT Found ring with atoms '
               '(15, 17, 21, 24, 13, 14): 2 carbonyl groups and 6/6 carbon '
               'atoms (ratio 1.00).\n'
               ' * SMILES: '
               'C1(=C(C(C(=C(C1=O)OC)[O-])=O)C)C/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)\\C)\\C)\\C '
               'NAME: 3-demethyl-ubiquinone-7(1-) REASON: CORRECT Found ring '
               'with atoms (0, 5, 4, 3, 2, 1): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'COC(=O)c1c(O)cc2cc3C(=O)c4cc(O)cc(O)c4C(=O)c3c(O)c2c1C NAME: '
               'tetracenomycin D3 methyl ester REASON: CORRECT Found ring with '
               'atoms (11, 13, 20, 21, 23, 10): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: O=C1C(OC)=CC(=O)C=C1[C@H](C(=O)C)C NAME: '
               'Malbranicin REASON: CORRECT Found ring with atoms (1, 9, 8, 6, '
               '5, 2): 2 carbonyl groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C3=C1C(O)=CC=C3C4=C5C(=O)C6=C(O)C(=CC(=C6C(C5=C(O)C=C4)=O)O)C)C(O)=C(C)C=C2O '
               'NAME: Iridoskyrin REASON: CORRECT Found ring with atoms (1, 7, '
               '6, 4, 3, 2): 2 carbonyl groups and 6/6 carbon atoms (ratio '
               '1.00).\n'
               ' * SMILES: '
               'COc1cccc2C(=O)C3=C([C@@H](O)[C@H](O)c4cc(CO)cc(O)c34)C(=O)c12 '
               'NAME: PD116740 REASON: CORRECT Found ring with atoms (7, 9, '
               '10, 24, 26, 6): 2 carbonyl groups and 6/6 carbon atoms (ratio '
               '1.00).\n'
               ' * SMILES: '
               'COC1=C(OC)C2=C(C=C1)C(=O)C1=C(C=CC(\\C=C(\\C)CC(N)=O)=C1O)C2=O '
               'NAME: kinanthraquinone REASON: CORRECT Found ring with atoms '
               '(10, 12, 13, 26, 6, 7): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: C1=C(C=C2C(=C1O)C(=O)C3=C(C=C(C=C3C2=O)O)O)C(=O)O '
               'NAME: 4,5,7-trihydroxy-9,10-dioxo-2-anthracenecarboxylic acid '
               'REASON: CORRECT Found ring with atoms (7, 9, 14, 15, 3, 4): 2 '
               'carbonyl groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C(=C[C@@H]([C@@H](O)[C@H](C=C[C@@H](O)CC=C(C(=O)C[C@H](O)[C@H](C=CC=CC=CC(NC=2C(C(C=3C1=C(O)C(=CC3C2O)C)=O)=O)=O)C)C)C)C)C '
               'NAME: Actamycin REASON: CORRECT Found ring with atoms (30, 31, '
               '32, 38, 39, 29): 2 carbonyl groups and 6/6 carbon atoms (ratio '
               '1.00).\n'
               ' * SMILES: '
               'O1[C@]2([C@@]3([C@@]([C@]([C@@]14C(=C3)C(=O)C=5C(C4=O)=CC=CC5)(C)C=O)(CC2)[H])[H])C '
               'NAME: Sterekunthal B REASON: CORRECT Found ring with atoms (8, '
               '10, 11, 12, 5, 6): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: O=C1C(OC)=CC(=O)C(=C1[C@H](C(=O)C)C)O NAME: '
               '2-hydroxy-5-methoxy-3-(3-oxobutan-2-yl)cyclohexa-2,5-diene-1,4-dione '
               'REASON: CORRECT Found ring with atoms (1, 9, 8, 6, 5, 2): 2 '
               'carbonyl groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C2=C(O)C3=C(O[C@]4(CCC[C@@H]3O4)C)C=C2C(=O)C=5C1=C(OC)C=C(O)C5 '
               'NAME: 8-O-methylaverufin REASON: CORRECT Found ring with atoms '
               '(1, 20, 19, 17, 16, 2): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: OC(C=1C(=O)C=2C(C(=O)C1)=C(O)C=CC2O)CC=C(C)C NAME: '
               'C.I. Natural Red 20 REASON: CORRECT Found ring with atoms (2, '
               '9, 7, 6, 5, 3): 2 carbonyl groups and 6/6 carbon atoms (ratio '
               '1.00).\n'
               ' * SMILES: BrC1=C(Cl)C(=O)C(CO)=CC1=O NAME: '
               'Bromochlorogentisylquinone B REASON: CORRECT Found ring with '
               'atoms (1, 10, 9, 6, 4, 2): 2 carbonyl groups and 6/6 carbon '
               'atoms (ratio 1.00).\n'
               'False positives: SMILES: C=1C(C(=NC(C1O)=O)[O-])=O NAME: '
               '3,6-dihydroxypyridine-2,5-dione(1-) REASON: WRONGLY CLASSIFIED '
               'Found ring with atoms (0, 5, 4, 3, 2, 1): 2 carbonyl groups '
               'and 5/6 carbon atoms (ratio 0.83).\n'
               ' * SMILES: O=C1C=2C=C(C(C)(C)C)C=CC2NC1=O NAME: '
               '5-tert-butyl-1h-indole-2,3-dione REASON: WRONGLY CLASSIFIED '
               'Found ring with atoms (1, 2, 11, 12, 13): 2 carbonyl groups '
               'and 4/5 carbon atoms (ratio 0.80).\n'
               ' * SMILES: O=C1C2=C(O)C(O)=C(OC)C(=C2C(=O)C=3C1=C(OC3)C)O '
               'NAME: Isofuranonaphthoquinone E REASON: WRONGLY CLASSIFIED '
               'Found ring with atoms (1, 15, 14, 12, 11, 2): 2 carbonyl '
               'groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'C[C@@H]1O[C@H](CC[C@@H]1O)O[C@]12C(=O)C[C@](C)(O)C[C@@]1(O)C=CC1=C2C(=O)c2ccc([C@H]3C[C@@H](O[C@H]4CC[C@H](O[C@H]5C[C@@H](O)[C@H](O)[C@@H](C)O5)[C@H](C)O4)[C@H](O)[C@@H](C)O3)c(O)c2C1=O '
               'NAME: urdamycin A REASON: WRONGLY CLASSIFIED Found ring with '
               'atoms (23, 25, 57, 58, 21, 22): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'COc1cccc2C(=O)c3c(O)c4C[C@](O)(C[C@H](O[C@H]5C[C@H]([NH3+])[C@H](O)[C@H](C)O5)c4c(O)c3C(=O)c12)C(C)O '
               'NAME: 13-dihydrodaunorubicin(1+) REASON: WRONGLY CLASSIFIED '
               'Found ring with atoms (7, 9, 31, 32, 34, 6): 2 carbonyl groups '
               'and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'C1CC2=C(CC1)C(N(C2=O)C3=C(C=C(C(=C3)OC(C)C#C)Cl)F)=O NAME: '
               '2-[5-(but-3-yn-2-yloxy)-4-chloro-2-fluorophenyl]-4,5,6,7-tetrahydro-1H-isoindole-1,3(2H)-dione '
               'REASON: WRONGLY CLASSIFIED Found ring with atoms (6, 3, 2, 8, '
               '7): 2 carbonyl groups and 4/5 carbon atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C/1O[C@H](CC(=O)O)C(\\C1=C/2\\O[C@@](C[C@@H](CC)C)(C)C=C2)=O '
               'NAME: Nodulisporacid A REASON: WRONGLY CLASSIFIED Found ring '
               'with atoms (1, 2, 3, 8, 9): 2 carbonyl groups and 4/5 carbon '
               'atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C1N[C@@H](CC2=CC=C(O)C=C2)C(C1=C(O)/C=C/C(=C/[C@@H]([C@@H](O)C)C)/C)=O '
               'NAME: Syn-12-hydroxypretenellin A REASON: WRONGLY CLASSIFIED '
               'Found ring with atoms (1, 2, 3, 12, 13): 2 carbonyl groups and '
               '4/5 carbon atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C1NC(=O)C2=C1C3=C4N(C5(OC(N6C4=C2C7=C6C=CC=C7)CC(C5OC)NC)C)C8=C3C=CC=C8 '
               'NAME: 7-Oxostaurosporine REASON: WRONGLY CLASSIFIED Found ring '
               'with atoms (1, 2, 3, 5, 6): 2 carbonyl groups and 4/5 carbon '
               'atoms (ratio 0.80).\n'
               ' * SMILES: '
               'CCC(=O)CC(=O)c1c(O)c2C(=O)c3c([O-])cccc3C(=O)c2cc1CC(=O)OC '
               'NAME: methyl aklanonate(1-) REASON: WRONGLY CLASSIFIED Found '
               'ring with atoms (11, 13, 19, 20, 22, 10): 2 carbonyl groups '
               'and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'CO[C@H]([C@H](O)CC(=O)[C@@H](C)[C@@H](O)CC[C@@H](C)[C@@H]1O[C@]2(CC[C@@H](C)[C@H](CC[C@H](C)C(C)=O)O2)CC[C@@H]1C)[C@H](OC(=O)C[C@@H](O)C1=C(C)C(=O)OC1=O)C(C)C '
               'NAME: Tautomycin REASON: WRONGLY CLASSIFIED Found ring with '
               'atoms (44, 43, 49, 48, 46): 2 carbonyl groups and 4/5 carbon '
               'atoms (ratio 0.80).\n'
               ' * SMILES: O=C1C(OC)=C(C(=CN)C([C@@]1(CC)C)=O)[C@H](CC)C NAME: '
               'Mycosphine A REASON: WRONGLY CLASSIFIED Found ring with atoms '
               '(1, 10, 9, 6, 5, 2): 2 carbonyl groups and 6/6 carbon atoms '
               '(ratio 1.00).\n'
               ' * SMILES: '
               'C1=CC=C2C(=C1)C(=O)N(C2=O)CCC3=CSC(=N3)C4=CC(=CC=C4)F NAME: '
               '2-[2-[2-(3-fluorophenyl)-4-thiazolyl]ethyl]isoindole-1,3-dione '
               'REASON: WRONGLY CLASSIFIED Found ring with atoms (6, 4, 3, 9, '
               '8): 2 carbonyl groups and 4/5 carbon atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C1N2C(OC(C2(CO)C)=O)(CC=3C1=C(O)C4=C5C(=O)C6=C(OC=7C=C(OC)C(=CC7C6=O)OC)C(C5=CC=C4C3)=O)C '
               'NAME: Citreamicin n REASON: WRONGLY CLASSIFIED Found ring with '
               'atoms (18, 20, 21, 35, 36, 17): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: O=C1C(=O)C2=C(O)C=CC=C2C=3C1=C(O)C(=C(C(=O)CCC)C3)C '
               'NAME: Murayaquinone REASON: WRONGLY CLASSIFIED Found ring with '
               'atoms (1, 12, 11, 10, 4, 2): 2 carbonyl groups and 6/6 carbon '
               'atoms (ratio 1.00).\n'
               ' * SMILES: '
               'C1=CC(=CC=C1CN2C3=C(C=C(C=C3)OC(F)(F)F)C(=O)C2=O)C4=CSC=C4 '
               'NAME: '
               '1-[[4-(3-thiophenyl)phenyl]methyl]-5-(trifluoromethoxy)indole-2,3-dione '
               'REASON: WRONGLY CLASSIFIED Found ring with atoms (19, 9, 8, 7, '
               '21): 2 carbonyl groups and 4/5 carbon atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=[N+]([O-])C1(C(OC)C(OC(C1)OC2=C(O)C(=NC(=C2)C(=O)NC=3C(=O)OC=4C=C(OC)C=CC4C3O)C(=O)OC5C(O)C(=O)C6(OC7=C(C(=O)C8=C(C(C(C(=CC5C)C)=O)=C(O)C(=C8)C)C7=O)NC6)C)C)C '
               'NAME: Protorubradirin REASON: WRONGLY CLASSIFIED Found ring '
               'with atoms (48, 50, 51, 65, 46, 47): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: CC1OC(=C)C(=O)C1=O NAME: '
               '2-methyl-5-methylenefuran-3,4-dione REASON: WRONGLY CLASSIFIED '
               'Found ring with atoms (1, 2, 3, 5, 7): 2 carbonyl groups and '
               '4/5 carbon atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C1N2C(OC(C2(CO)C)=O)(CC=3C1=C(O)C4=C5C(=O)C6=C(OC=7C=CC(=C(C7C6=O)O)OC)C(C5=CC=C4C3)=O)C '
               'NAME: Citreamicin delta REASON: WRONGLY CLASSIFIED Found ring '
               'with atoms (18, 20, 21, 34, 35, 17): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C=2O[C@]([C@@H]3CC[C@@](C=C3C2C(=O)C=4C1=C(O)C=C(O)C4)(OC)C)(CCC=C(C)C)C '
               'NAME: Methoxydebromomarinone REASON: WRONGLY CLASSIFIED Found '
               'ring with atoms (1, 15, 14, 12, 11, 2): 2 carbonyl groups and '
               '6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=[N+]([O-])[C@@]1([C@@H](N)[C@H](O[C@H](C1)O[C@@H]2C(=C[C@H]3[C@@]4(OC(=O)C(C4=O)=C([C@@]5([C@H](C(=CC2)C)C=C[C@@H]6[C@@H](O[C@@H]7O[C@H]([C@H](OC(=O)C)[C@@H](C7)O[C@@H]8O[C@H]([C@H](O[C@H]9O[C@H]([C@H](O[C@@H]%10O[C@H]([C@H](O)CC%10)C)[C@@H](C9)O)C)CC8)C)COC(=O)C)[C@@H](C)C[C@@H]([C@@H]56)C)C)O)CC(C=O)=C[C@@H]3O)C)C(=O)OC)C '
               'NAME: Tetrocarcin Q REASON: WRONGLY CLASSIFIED Found ring with '
               'atoms (16, 15, 20, 19, 17): 2 carbonyl groups and 4/5 carbon '
               'atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C1NCCCC2NC(=O)C(C2=O)=C(O)C=CC3C(CC=C1)C4C(C5C(C(CC)C(C5)C)C6C4O6)C3 '
               'NAME: Ikarugamycin epoxide REASON: WRONGLY CLASSIFIED Found '
               'ring with atoms (7, 6, 11, 10, 8): 2 carbonyl groups and 4/5 '
               'carbon atoms (ratio 0.80).\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(=CC=C2C(=O)C3=C1C=CC=4C3=C(O)C=C(C)C4)[C@@H]5O[C@@H]([C@@H](O)[C@@H](C5)O)C '
               'NAME: Dehydroxyaquayamycin REASON: WRONGLY CLASSIFIED Found '
               'ring with atoms (1, 12, 11, 9, 8, 2): 2 carbonyl groups and '
               '6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'C=1(C(=C2C(C3=C(C=C(O)C(C([O-])=O)=C3C)C(C2=CC1[O-])=O)=O)O)[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O)CO '
               'NAME: flavokermesate 7-C-beta-D-glucoside(2-) REASON: WRONGLY '
               'CLASSIFIED Found ring with atoms (3, 4, 5, 15, 16, 2): 2 '
               'carbonyl groups and 6/6 carbon atoms (ratio 1.00).\n'
               ' * SMILES: '
               'O=C1C=2O[C@]([C@@H]3CCC(=C[C@@H]3C2C(=O)C=4C1=C(O)C=C(O)C4)C)(CCC=C(C)C)C '
               'NAME: Debromomarinone REASON: WRONGLY CLASSIFIED Found ring '
               'with atoms (1, 15, 14, 12, 11, 2): 2 carbonyl groups and 6/6 '
               'carbon atoms (ratio 1.00).\n'
               'False negatives: SMILES: '
               'O=C1C(=C[C@@H]2C=C[C@@H]3CC(N[C@]43[C@@H]2C(=O)C5=C(C(O)=C(C)C(=C5C4=O)O)C([C@@H](C=C[C@H]([C@@H]1C)O)C)=O)=O)CC(C)C '
               'NAME: Ansaseomycin A REASON: MISSED No fully conjugated ring '
               'with at least two carbonyl groups and high carbon content was '
               'found.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=C(C)C=C2C(=O)[C@@]34C15C(=O)[C@H]6C(OC)C3C7[C@]86C5(C(=O)C9=C(O)C=C(C)C=C9C8=O)C(=O)[C@H]4C7OC '
               'NAME: Rugulin REASON: MISSED No fully conjugated ring with at '
               'least two carbonyl groups and high carbon content was found.\n'
               ' * SMILES: '
               'Cl[C@]1(C(=O)C2=C(O)C(=C(O)C=C2C([C@@]1(O)C/C=C(/CC/C=C/C)\\C)=O)C)CC=C(C)C '
               'NAME: SF2415B1 REASON: MISSED No fully conjugated ring with at '
               'least two carbonyl groups and high carbon content was found.\n'
               ' * SMILES: '
               'Cl[C@]1(C(=O)C2=C(O)C=C(O)C=C2C([C@@]1(O)CC(=C(C)C)CC=C(CCC=C(C)C)C)=O)C '
               'NAME: Merochlorin D REASON: MISSED No fully conjugated ring '
               'with at least two carbonyl groups and high carbon content was '
               'found.\n'
               ' * SMILES: '
               'Cl[C@]1(C(=O)C2=C(O)C=C(O)C=C2C([C@@]1(O)C/C=C(/CCC=C(C)C)\\C)=O)CC=C(C)C '
               'NAME: Naphthomevalin REASON: MISSED No fully conjugated ring '
               'with at least two carbonyl groups and high carbon content was '
               'found.\n'
               ' * SMILES: O=C1C2=C(O)C(=C(C)C(=C2C(=O)CC1)O)CC(=O)C NAME: '
               'Karuquinone A REASON: MISSED No fully conjugated ring with at '
               'least two carbonyl groups and high carbon content was found.\n'
               ' * SMILES: '
               'Cl[C@]12C(=O)C3=C(O)C=C(O)C=C3[C@@]4(C1=O)CC(=C(C)C)C[C@H]4[C@@]2(CCC=C(C)C)C '
               'NAME: Merochlorin A REASON: MISSED No fully conjugated ring '
               'with at least two carbonyl groups and high carbon content was '
               'found.\n'
               ' * SMILES: '
               'Cl[C@@]12C(=O)C3=C(O)C=C(O)C=C3C([C@@]1(OC(C)(C)[C@@H](C2)Cl)CC=C(CCC=C(C=O)C)C)=O '
               'NAME: 18-oxonapyradiomycin A1 REASON: MISSED No fully '
               'conjugated ring with at least two carbonyl groups and high '
               'carbon content was found.\n'
               ' * SMILES: '
               'S(C12C(=O)C3=C(O)C=CC=C3C(C1(O)C4(O)C(=O)C=C(C)CC4(O)CC2O)=O)CC(NC(=O)C)C(=O)O '
               'NAME: WS 009 B REASON: MISSED No fully conjugated ring with at '
               'least two carbonyl groups and high carbon content was found.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(=C(O)C=C2C(=O)C3(C1(O3)CC=C(C)C)C/C=C(/CCC=C(C)C)\\C)C '
               'NAME: SF2415B2 REASON: MISSED No fully conjugated ring with at '
               'least two carbonyl groups and high carbon content was found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No fully conjugated all‐carbon '
                                               'ring with at least two '
                                               'exocyclic carbonyl groups '
                                               '(with proper spacing in '
                                               '6‑membered rings) was found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No fully conjugated all‐carbon '
                                               'ring with at least two '
                                               'exocyclic carbonyl groups '
                                               '(with proper spacing in '
                                               '6‑membered rings) was found.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No fully conjugated all‐carbon '
                                               'ring with at least two '
                                               'exocyclic carbonyl groups '
                                               '(with proper spacing in '
                                               '6‑membered rings) was found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No fully conjugated all‐carbon '
                                               'ring with at least two '
                                               'exocyclic carbonyl groups '
                                               '(with proper spacing in '
                                               '6‑membered rings) was found.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No fully conjugated all‐carbon '
                                               'ring with at least two '
                                               'exocyclic carbonyl groups '
                                               '(with proper spacing in '
                                               '6‑membered rings) was found.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No fully conjugated all‐carbon '
                                               'ring with at least two '
                                               'exocyclic carbonyl groups '
                                               '(with proper spacing in '
                                               '6‑membered rings) was found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No rings found in molecule'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C(=C[C@@H]2C=C[C@@H]3CC(N[C@]43[C@@H]2C(=O)C5=C(C(O)=C(C)C(=C5C4=O)O)C([C@@H](C=C[C@H]([C@@H]1C)O)C)=O)=O)CC(C)C',
                                      'name': 'Ansaseomycin A',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'O=C1C2=C(O)C(O)=C(C(=O)CCCCC)C(=C2C(O)=CC1=O)O',
                                      'name': 'Quambalarine B',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'O=C1C2=C(O)C=C(C)C=C2C(=O)[C@@]34C15C(=O)[C@H]6C(OC)C3C7[C@]86C5(C(=O)C9=C(O)C=C(C)C=C9C8=O)C(=O)[C@H]4C7OC',
                                      'name': 'Rugulin',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'O=C1C(=C[C@@H]([C@@H](O)[C@H](C=C[C@@H](O)CC=C(C(=O)C[C@H](O)[C@H](C=CC=CC=CC(NC=2C(C(C=3C1=C(O)C(=CC3C2O)C)=O)=O)=O)C)C)C)C)C',
                                      'name': 'Actamycin',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'O1[C@]2([C@@]3([C@@]([C@]([C@@]14C(=C3)C(=O)C=5C(C4=O)=CC=CC5)(C)C=O)(CC2)[H])[H])C',
                                      'name': 'Sterekunthal B',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'Cl[C@]1(C(=O)C2=C(O)C(=C(O)C=C2C([C@@]1(O)C/C=C(/CC/C=C/C)\\C)=O)C)CC=C(C)C',
                                      'name': 'SF2415B1',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'Cl[C@]1(C(=O)C2=C(O)C=C(O)C=C2C([C@@]1(O)CC(=C(C)C)CC=C(CCC=C(C)C)C)=O)C',
                                      'name': 'Merochlorin D',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'Cl[C@]1(C(=O)C2=C(O)C=C(O)C=C2C([C@@]1(O)C/C=C(/CCC=C(C)C)\\C)=O)CC=C(C)C',
                                      'name': 'Naphthomevalin',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'O=C1C2=C(O)C(=C(C)C(=C2C(=O)CC1)O)CC(=O)C',
                                      'name': 'Karuquinone A',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was found.'},
                                  {   'smiles': 'Cl[C@]12C(=O)C3=C(O)C=C(O)C=C3[C@@]4(C1=O)CC(=C(C)C)C[C@H]4[C@@]2(CCC=C(C)C)C',
                                      'name': 'Merochlorin A',
                                      'reason': 'No fully conjugated '
                                                'all‐carbon ring with at least '
                                                'two exocyclic carbonyl groups '
                                                '(with proper spacing in '
                                                '6‑membered rings) was '
                                                'found.'}],
    'attempt': 2,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'One hypothesis is that the earlier approach – “find any ring '
                 'that is mostly sp² and mostly carbon and that has at least '
                 'two C=O bonds”—was too loose in some cases while missing the '
                 'subtle geometry of many fused‐ring or polycyclic quinones. '
                 'For example, many true quinones come from aromatic '
                 '(all‐carbon) 6‐membered rings having two exocyclic carbonyls '
                 'at the “correct” positions (as in p‐benzoquinone or '
                 'anthraquinone fragments). But sometimes rings with one '
                 'heteroatom (e.g. pyridine‐like) or rings where the carbonyl '
                 'groups are too close (or not “para”) are mistakenly '
                 'flagged. \n'
                 '\n'
                 'To improve matters, the new strategy is to:\n'
                 '1. Use RDKit’s Symmetry‐unique Smallest Set of Small Rings '
                 '(SSSR) so that we handle fused systems.\n'
                 '2. Only consider rings that (a) are at least 5‐membered, (b) '
                 'consist solely of carbon atoms (as quinones are derived from '
                 'all‐carbon aromatics), and (c) have all atoms in an sp² '
                 'environment (or are aromatic).\n'
                 '3. For each such ring, look at each carbon atom and count if '
                 'it bears an exocyclic carbonyl group – that is, if the atom '
                 'is double bonded to an oxygen that is not part of the ring.\n'
                 '4. In rings of size 6 (the classical quinone ring), require '
                 'that at least one pair of carbonyl–bearing atoms is “para” '
                 '(i.e. separated by three bonds along the ring). For rings of '
                 'a different size, simply require at least two exocyclic '
                 'carbonyls.\n'
                 '5. Return True (with an explanation) if one ring meets these '
                 'criteria; otherwise return False.\n'
                 '\n'
                 'Below is the complete Python code implementing that improved '
                 'approach.\n'
                 '\n'
                 '--------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1006,
    'num_false_positives': 857,
    'num_true_negatives': 140286,
    'num_false_negatives': 151,
    'num_negatives': None,
    'precision': 0.5399892646269457,
    'recall': 0.8694900605012964,
    'f1': 0.6662251655629139,
    'accuracy': 0.9929163738580464,
    'negative_predictive_value': 0.99892478477894}