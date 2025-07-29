"""
Classifies: CHEBI:47016 tetrahydrofuranone
"""
"""
Classifies: tetrahydrofuranone
Definition: Any oxolane (i.e. a 5‐membered saturated ring with one oxygen and four carbons)
that carries an oxo- substituent (a carbonyl, either as a direct C=O or through an acyl group)
on one of the ring carbons. Additionally, the oxolane ring must be isolated (i.e. not fused with other rings)
to avoid false positives.
"""

from rdkit import Chem
from rdkit.Chem import rdchem

def is_tetrahydrofuranone(smiles: str):
    """
    Determines if a molecule qualifies as a tetrahydrofuranone based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        (bool, str): Tuple where the boolean indicates if the molecule is classified as a tetrahydrofuranone,
                     and the string provides the reason for the classification.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Retrieve ring information.
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()

    # Iterate over rings to find a candidate oxolane ring.
    for ring in rings:
        # Only consider 5-membered rings.
        if len(ring) != 5:
            continue

        # Count atoms in the candidate ring: need exactly four carbons and one oxygen.
        oxygen_count = 0
        carbon_count = 0
        for idx in ring:
            atomic_num = mol.GetAtomWithIdx(idx).GetAtomicNum()
            if atomic_num == 8:
                oxygen_count += 1
            elif atomic_num == 6:
                carbon_count += 1
        if oxygen_count != 1 or carbon_count != 4:
            continue

        # Ensure the ring is saturated:
        # a) none of its atoms is aromatic,
        # b) all bonds between atoms in the ring are single bonds.
        saturated = True
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetIsAromatic():
                saturated = False
                break
        if not saturated:
            continue

        ring_bonds_saturated = True
        n = len(ring)
        for i in range(n):
            a1 = ring[i]
            a2 = ring[(i + 1) % n]  # wrap around for cyclicity
            bond = mol.GetBondBetweenAtoms(a1, a2)
            if bond is None or bond.GetBondType() != rdchem.BondType.SINGLE:
                ring_bonds_saturated = False
                break
        if not ring_bonds_saturated:
            continue

        # NEW CHECK: Ensure that the candidate oxolane ring is isolated.
        # Every atom in the ring should belong to exactly one ring.
        isolated = True
        for idx in ring:
            if ring_info.NumAtomRings(idx) != 1:
                isolated = False
                break
        if not isolated:
            continue

        # Now check for an oxo substituent on one of the ring carbons.
        # Possibility 1: The ring carbon directly bears an exocyclic oxygen by a double bond.
        # Possibility 2: The ring carbon is attached to a carbon (acyl group) that carries a C=O.
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # Only consider carbon atoms in the ring.
            if atom.GetAtomicNum() != 6:
                continue

            # Inspect neighbors that are not part of the ring.
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring:
                    continue
                bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                if bond is None:
                    continue
                # Possibility 1: Direct carbonyl group (C=O directly attached to ring carbon).
                if nbr.GetAtomicNum() == 8 and bond.GetBondType() == rdchem.BondType.DOUBLE:
                    return True, "Found a tetrahydrofuran ring with a direct carbonyl substituent on a ring carbon"
                # Possibility 2: Acyl substituent. Check that the neighbor is a carbon
                # that carries a double bonded oxygen.
                if nbr.GetAtomicNum() == 6:
                    for sub_nbr in nbr.GetNeighbors():
                        if sub_nbr.GetIdx() == atom.GetIdx():
                            continue
                        sub_bond = mol.GetBondBetweenAtoms(nbr.GetIdx(), sub_nbr.GetIdx())
                        if sub_bond is None:
                            continue
                        if sub_nbr.GetAtomicNum() == 8 and sub_bond.GetBondType() == rdchem.BondType.DOUBLE:
                            return True, "Found a tetrahydrofuran ring with an acyl substituent on a ring carbon"
    # If no candidate ring passed all checks, classification fails.
    return False, "No isolated tetrahydrofuran ring with an oxo substituent found"

# Example usage (feel free to add additional tests):
if __name__ == "__main__":
    # Example: N-isovaleryl-L-homoserine lactone
    test_smiles = "CC(C)CC(=O)N[C@H]1CCOC1=O"
    result, reason = is_tetrahydrofuranone(test_smiles)
    print(f"SMILES: {test_smiles}")
    print("Classification:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47016',
                          'name': 'tetrahydrofuranone',
                          'definition': 'Any oxolane having an oxo- '
                                        'substituent at any position on the '
                                        'tetrahydrofuran ring.',
                          'parents': ['CHEBI:26912'],
                          'xrefs': ['PMID:6047194'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
                           'indent_by_line': [   1,
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
                                                 0,
                                                 1,
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
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'AtomRings'],
                           'methods_called_count': 3,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_tetrahydrofuranone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No isolated tetrahydrofuran '
                                          'ring with an oxo substituent '
                                          'found"'],
                           'returns_count': 2,
                           'complexity': 2.466440902035041},
    'message': '\n'
               'Attempt failed: F1 score of 0.05957741600277104 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CC(C)CC(=O)N[C@H]1CCOC1=O NAME: '
               'N-isovaleryl-L-homoserine lactone REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: [C@]1([C@@](C(OC1)=O)(C(CCCCCCC)=O)[H])(CO)[H] '
               'NAME: 6-dehydro-SCB2 REASON: CORRECT Found a tetrahydrofuran '
               'ring with an acyl substituent on a ring carbon\n'
               ' * SMILES: CCCCCCCCC1OC(=O)C(=C)C1C(O)=O NAME: '
               '4-methylidene-2-octyl-5-oxotetrahydrofuran-3-carboxylic acid '
               'REASON: CORRECT Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: CCCCCCCCCC(=O)CC(=O)N[C@H]1CCOC1=O NAME: '
               'N-(3-oxododecanoyl)-L-homoserine lactone REASON: CORRECT Found '
               'a tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: CCCC(=O)N[C@@H]1CCOC1=O NAME: '
               'N-butyryl-L-homoserine lactone REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'CO[C@H]1CC(=O)C([C@H]2OC(=O)C(=C)[C@@H]2CCC(C)=O)=C1C NAME: '
               '3-O-methyl-isosecotanapartholide REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: CC12CCCCC1C(=O)OC2=O NAME: methylhexahydrophthalic '
               'anhydride REASON: CORRECT Found a tetrahydrofuran ring with a '
               'direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: O[C@@H]1COC(=O)[C@@H]1O NAME: erythrono-1,4-lactone '
               'REASON: CORRECT Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: CC1CC(=O)OC1=O NAME: 3-methylsuccinic anhydride '
               'REASON: CORRECT Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: '
               '[C@H]1([C@@H](CC2=CC3=C(OCO3)C=C2)COC1=O)CC4=CC(=C(OC)C(=C4)OC)OC '
               'NAME: dihydroanhydropodorhizol REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: O1C[C@@H](O)[C@H](O)C1=O NAME: D-threonolactone '
               'REASON: CORRECT Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: C[C@H]1CCC(=O)O1 NAME: (S)-gamma-valerolactone '
               'REASON: CORRECT Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: '
               'C[C@](O)(CCCCCCCC\\C=C\\C=C\\c1ccccc1)C[C@@]1(C)OC(=O)C[C@H]1O '
               'NAME: seco-plakortolide O REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'C=1(C(=C(C(=C(C1Cl)C)C([H])=O)O)C/C=C(/CC/C=C(\\C)/[C@@]2(CC(C(O2)(C)C)=O)[H])\\C)O '
               'NAME: ascofuranone REASON: CORRECT Found a tetrahydrofuran '
               'ring with a direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: COC1=C(C=CC(F)=C1F)C1C(C)[C@@](C)(OC1=O)C(F)(F)F '
               'NAME: '
               '(5R)-3-(3,4-difluoro-2-methoxyphenyl)-4,5-dimethyl-5-(trifluoromethyl)dihydrofuran-2(3H)-one '
               'REASON: CORRECT Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: CC1(C)CC(CSC#N)C(=O)O1 NAME: '
               '3-thiocyanatomethyl-5,5-dimethylbutyrolactone REASON: CORRECT '
               'Found a tetrahydrofuran ring with a direct carbonyl '
               'substituent on a ring carbon\n'
               ' * SMILES: N[C@@H]1CCOC1=O NAME: D-homoserine lactone REASON: '
               'CORRECT Found a tetrahydrofuran ring with a direct carbonyl '
               'substituent on a ring carbon\n'
               ' * SMILES: CC[C@@H]1[C@@H](COC1=O)Cc1cncn1C NAME: '
               '(-)-pilocarpine REASON: CORRECT Found a tetrahydrofuran ring '
               'with a direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: OC[C@H]1OC(=O)[C@H](O)[C@@H]1O NAME: '
               'D-ribono-1,4-lactone REASON: CORRECT Found a tetrahydrofuran '
               'ring with a direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: CCCCCCCCCCCC(=O)N[C@@H]1CCOC1=O NAME: '
               'N-dodecanoyl-L-homoserine lactone REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: C[C@@]1(O)OC[C@H](O)C1=O NAME: '
               '(2R,4S)-2-methyl-2,4-dihydroxydihydrofuran-3-one REASON: '
               'CORRECT Found a tetrahydrofuran ring with a direct carbonyl '
               'substituent on a ring carbon\n'
               ' * SMILES: C1(OC(=O)CC1)CCCC NAME: gamma-octalactone REASON: '
               'CORRECT Found a tetrahydrofuran ring with a direct carbonyl '
               'substituent on a ring carbon\n'
               ' * SMILES: COc1cccc(CCCCCCCCCC2CC(=C)C(=O)O2)c1OC NAME: '
               'bihapten 1 dimethyl ether REASON: CORRECT Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: O=C1OC(=O)C2CCCCC12 NAME: hexahydrophthalic '
               'anhydride REASON: CORRECT Found a tetrahydrofuran ring with a '
               'direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: C=C1CCOC1=O NAME: alpha-methylene '
               'gamma-butyrolactone REASON: CORRECT Found a tetrahydrofuran '
               'ring with a direct carbonyl substituent on a ring carbon\n'
               'False positives: SMILES: '
               'O=C1OCC=2[C@@]1(O)[C@@]3([C@H](C(CCC3)(C)C)[C@@H](C2)OC(=O)/C=C/C=C/CO)C '
               'NAME: Calidoustene A REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O1C2(C1C(=O)CC(C(OC(=O)/C(/C)=C\\C)C(O)C3C(OC(=O)C3=C)C2)=C)C '
               'NAME: '
               '(10-hydroxy-3-methyl-8,12-dimethylidene-6,13-dioxo-4,14-dioxatricyclo[9.3.0.03,5]tetradecan-9-yl) '
               '(Z)-2-methylbut-2-enoate REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=C1C2=C(OC(C1)(C(=O)OC)[C@H]3OC(=O)C[C@@H]3C)C(C4=C5OC(C(=O)OC)([C@@H]6OC(=O)C[C@@H]6C)CC(C5=C(O)C=C4)=O)=CC=C2O '
               'NAME: Paecilin C REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'CO[C@H]1CC(=O)[C@]2(C)[C@@H]1[C@H](C)C[C@@H]1OC(=O)C(=C)[C@H]1[C@@H]2OC(C)=O '
               'NAME: '
               '(1S,2S,5R,6S,7R,8S,10R)-6-acetoxy-2-methoxy-4-oxopseudoguai-11(13)-en-12,8-olide '
               'REASON: WRONGLY CLASSIFIED Found a tetrahydrofuran ring with a '
               'direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: O1[C@@](OC)([C@@H](O)/C(=C/CCCCCCCCC)/C1=O)C NAME: '
               'Actinolide B REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: O=C1O[C@@H](C=CC)[C@H]2C1=C[C@@H](O)[C@@H](C=CC)O2 '
               'NAME: Waol A REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'CC(=O)SC1CC2=CC(=O)CCC2(C3C1C4CCC5(C4(CC3)C)CCC(=O)O5)C NAME: '
               'ethanethioic acid '
               "S-(10,13-dimethyl-3,5'-dioxo-7-spiro[2,6,7,8,9,11,12,14,15,16-decahydro-1H-cyclopenta[a]phenanthrene-17,2'-oxolane]yl) "
               'ester REASON: WRONGLY CLASSIFIED Found a tetrahydrofuran ring '
               'with a direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: '
               'O1C2(C3(C(CC2)(C4=C(C5(C(CC4)C(C(=O)CC5)(CO)CO)C)CC3)C)C)C(CC1C(=O)CC)C '
               'NAME: '
               '(17alpha,23S)-Epoxy-28,29-dihydroxy-27-norlanost-8-ene-3,24-dione '
               'REASON: WRONGLY CLASSIFIED Found a tetrahydrofuran ring with '
               'an acyl substituent on a ring carbon\n'
               ' * SMILES: '
               'O=C1C=C2C(=CC(=O)OC2(C)C)[C@]3([C@@H]4[C@@]1([C@H]5C(=O)[C@@H](O[C@@H]6[C@@]5(O)[C@](C(=O)O6)(C)C4)C)C)OC3 '
               'NAME: Chrysogenolide F REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@H]3[C@H](C(C=C)=CC[C@@H]3[C@@]4([C@@]2([C@@]1([C@H](O)CC4)C)O)C)C '
               'NAME: Hawaiinolide F REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O1[C@@]23[C@]4([C@@H](OC(=O)C)[C@@H](O)[C@](OC(=O)[C@H]([C@@H](C=5N=CC=CC5C(OC[C@]1([C@@]([C@H]2OC(=O)C)(C(=O)[C@H]4OC(=O)C)[H])C)=O)C)C)([C@@]3(O)C)[H])COC(=O)C '
               'NAME: '
               '[(1S,3R,13S,14S,17S,18R,19R,20S,21S,23R,24R,25S)-19,21,24-triacetyloxy-18,25-dihydroxy-3,13,14,25-tetramethyl-6,15,22-trioxo-2,5,16-trioxa-11-azapentacyclo[15.7.1.01,20.03,23.07,12]pentacosa-7(12),8,10-trien-20-yl]methyl '
               'acetate REASON: WRONGLY CLASSIFIED Found a tetrahydrofuran '
               'ring with an acyl substituent on a ring carbon\n'
               ' * SMILES: '
               'O=[N+]([O-])C1=CC=C(C(=O)O[C@@H]2C=C3C(=O)OC[C@@H]3[C@@]4([C@@H]2[C@](CCC4)(CO)C)C)C=C1 '
               'NAME: 14-Hydroxy-6beta-p-nitrobenzoylcinnamolide REASON: '
               'WRONGLY CLASSIFIED Found a tetrahydrofuran ring with a direct '
               'carbonyl substituent on a ring carbon\n'
               ' * SMILES: CC(C)CCOCC1CC(C(=O)O1)CC(=NNC(=S)N)C NAME: '
               '[1-[5-(3-methylbutoxymethyl)-2-oxo-3-oxolanyl]propan-2-ylideneamino]thiourea '
               'REASON: WRONGLY CLASSIFIED Found a tetrahydrofuran ring with a '
               'direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: '
               'O1C(CCC1C(O)CCCCCCCCCCCC)C(O)CCCCCC(O)CCCCC2OC(=O)C(C2)CC(=O)C '
               'NAME: Isoannoreticuin REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=[N+]([O-])[C@@]1([C@@H](NC(=O)OC)[C@H](O[C@H](C1)O[C@@H]2C(=C[C@@H]3C=C([C@H](C)C[C@]34OC(=O)C(C4=O)=C([C@@]5([C@H](C(C(C2)OO)=C)C=C[C@@H]6[C@@H](O[C@@H]7O[C@H]([C@H](O)[C@@H](C7)O[C@H]8O[C@@H](O)[C@@H](O[C@@H]9O[C@H]([C@H](OC)[C@@H](C9)O)C)[C@@H](C8)C)C)[C@@H](C)C[C@@H]([C@@H]56)C)C)O)CO)C)C)C '
               'NAME: Lobophorin CR3 REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=C1O[C@@]2([C@@H](C3=CC=CC=C3)C[C@@H]([C@]([C@]42[C@@]1(O4)CC5=CC=CC=C5)(O)C6=CC=CC=C6)O)C(O)C7=CC=CC=C7 '
               'NAME: Maculalactone H REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=C1C2=C(C=C(/C=C/C)OC2)C[C@@H]3[C@@]1(OC(=O)[C@H]3C(O)CCCCCCC)C '
               'NAME: Monapilosusazaphilone REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with an acyl substituent on a ring '
               'carbon\n'
               ' * SMILES: '
               'O=C1C=C2C=CC3=C4[C@]([C@@H](/C(=C/[C@H]5OC(=O)[C@@H]([C@@H]5C)C)/C)CC4)(C)CC[C@@H]3[C@@]2(C)CC1 '
               'NAME: Penijanthoid A REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: O1C2C3C(CCC2C(C1=O)C)(CCC(=O)C3C)C NAME: '
               'Cadabicilone REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               '[P@]1(=O)(OC(=C2C(=O)OC[C@H]2CO1)CCC)OCCCCCCCCCCCCCCC NAME: '
               'Salinipostin F REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'CC(C)c1oc(=O)cc2c1[C@@H](O)[C@H]1OC(=O)[C@]3(C)[C@H]1[C@]2(C)[C@H]1O[C@H]1[C@@H]3O '
               'NAME: Nagilactone C REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=C1C(OC)=C(C(=O)C=2C1=C(O)C3=C(C(=O)C4(O)C5C3OC4(C(O[C@@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@](O)(C(=O)C)CC7)C)CC6)C)C(C5OC8O[C@H]([C@H](O)[C@@H](C8)O)C)O)CCC)C2O)C=9C(OC)=C(OC)C%10=CC=%11CC%12C(O[C@@H]%13O[C@H]([C@H](O)[C@@H](C%13)O)C)C(O)C(C(C%12(C(C%11C(=C%10C9O)O)=O)O)(O)CCC)O[C@@H]%14O[C@@H]([C@@H](O[C@H]%15O[C@@H]([C@@](O)(C(=O)C)CC%15)C)CC%14)C '
               'NAME: Hibarimicin B REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with an acyl substituent on a ring '
               'carbon\n'
               ' * SMILES: '
               'O1[C@]23[C@]4([C@@]5(C([C@@]2([C@@]([C@@H](O)C=C3)(C1=O)C)[H])C(O)=O)C[C@@](O)(CC4)C(C5)=C)[H] '
               'NAME: '
               '(1R,2R,5S,8S,10R,11S,12S)-5,12-Dihydroxy-11-methyl-6-methylidene-16-oxo-15-oxapentacyclo[9.3.2.15,8.01,10.02,8]heptadec-13-ene-9-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Found a tetrahydrofuran ring '
               'with a direct carbonyl substituent on a ring carbon\n'
               ' * SMILES: '
               'CC(=O)O[C@H]1\\C=C(C)\\CC\\C=C(C)\\CC2OC(=O)C(=C)C12 NAME: '
               'laurenobiolide REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with a direct carbonyl substituent on a '
               'ring carbon\n'
               ' * SMILES: '
               'O=C1OC([C@]2(C(=C3[C@@]([C@]45C(=C)[C@]([C@@H]3OC(=O)C)(OC([C@@]4(O)[C@H](C)OC5=O)=O)C)(C)CC2)C)C=C1)(C)C '
               'NAME: Austin REASON: WRONGLY CLASSIFIED Found a '
               'tetrahydrofuran ring with an acyl substituent on a ring '
               'carbon\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No isolated tetrahydrofuran '
                                               'ring with an oxo substituent '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CC12CCCCC1C(=O)OC2=O',
                                      'name': 'methylhexahydrophthalic '
                                              'anhydride',
                                      'reason': 'No isolated tetrahydrofuran '
                                                'ring with an oxo substituent '
                                                'found'},
                                  {   'smiles': 'O=C1OC(=O)C2CCCCC12',
                                      'name': 'hexahydrophthalic anhydride',
                                      'reason': 'No isolated tetrahydrofuran '
                                                'ring with an oxo substituent '
                                                'found'},
                                  {   'smiles': 'CC12CC=CCC1C(=O)OC2=O',
                                      'name': 'methyltetrahydrophthalic '
                                              'anhydride',
                                      'reason': 'No isolated tetrahydrofuran '
                                                'ring with an oxo substituent '
                                                'found'},
                                  {   'smiles': 'O=C1OC(=O)C2CC=CCC12',
                                      'name': '1,2,3,6-tetrahydrophthalic '
                                              'anhydride',
                                      'reason': 'No isolated tetrahydrofuran '
                                                'ring with an oxo substituent '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'The previous approach searched for 5‐membered (oxolane) '
                 'rings that are saturated and contain one oxygen and four '
                 'carbons. Then it looked at substituents on the ring carbons '
                 'to see if a carbonyl (either directly attached as C=O or via '
                 'an acyl group) was present. However, many false positives '
                 'stem from tetrahydrofuran rings that are part of fused or '
                 'polycyclic systems (i.e. not “isolated” oxolanes). In such '
                 'cases one or more atoms in the ring participate in '
                 'additional rings, and the current code mistakenly classifies '
                 'them as tetrahydrofuranones.\n'
                 '\n'
                 'To improve the classifier, I have added an extra filtering '
                 'step: after identifying a candidate 5‐membered oxolane ring, '
                 'we now check that each atom in the ring belongs to exactly '
                 'one ring (i.e. it is not fused with any other ring). This '
                 '“isolation” requirement helps to rule out many of the false '
                 'positives. The rest of the detection logic (checking for a '
                 'direct exocyclic carbonyl or an acyl substituent) remains '
                 'similar.\n'
                 '\n'
                 'Below is the complete code in a single Python block.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 82,
    'num_false_positives': 747,
    'num_true_negatives': 141467,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.09891435464414958,
    'recall': 0.9534883720930233,
    'f1': 0.1792349726775956,
    'accuracy': 0.9947224174279691,
    'negative_predictive_value': 0.9999717256540209}