"""
Classifies: CHEBI:33838 nucleoside
"""
"""
Classifies: Nucleoside
Definition:
  “A nucleoside is an N-glycosyl compound that has both a nucleobase – normally adenine, guanine,
   xanthine, thymine, cytosine or uracil – and either a ribose or deoxyribose as functional parents.”
Improved strategy:
  1. Parse the SMILES string.
  2. Exclude molecules with phosphorus (e.g. phosphate groups => nucleotide).
  3. Identify candidate sugar rings by iterating over all rings of size 5 that contain exactly 4 carbons and 1 oxygen.
     Additionally, require that each atom in that ring belongs to only one ring (to avoid fused systems).
  4. Identify candidate nucleobase substructures using canonical SMARTS patterns, and if none are found, fall back
     to a heuristic of rings (size 5 or 6) with at least 2 nitrogen atoms.
  5. Look for a single bond from any carbon in a sugar ring to a nitrogen that is part of the nucleobase.
  
Returns:
   (True, <reason>) if the SMILES is classified as a nucleoside;
   (False, <reason>) otherwise.
   If parsing fails, returns (False, "Invalid SMILES string").
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_nucleoside(smiles: str):
    # Parse the molecule from SMILES.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # -------------------------------
    # Step 1. Exclude molecules with phosphorus (likely nucleotides, not nucleosides)
    if any(atom.GetAtomicNum() == 15 for atom in mol.GetAtoms()):
        return False, "Phosphate group detected; molecule is likely a nucleotide, not a nucleoside"
    
    # -------------------------------
    # Step 2. Identify candidate sugar rings.
    # For a ribose or deoxyribose ring, we expect a five-membered ring with exactly 4 carbons and 1 oxygen.
    # Additionally, each atom in a genuine sugar should not be fused into another ring.
    ring_info = mol.GetRingInfo().AtomRings()
    # Count how many rings each atom belongs to.
    atom_ring_counts = {i:0 for i in range(mol.GetNumAtoms())}
    for ring in ring_info:
        for idx in ring:
            atom_ring_counts[idx] += 1

    sugar_rings = []   # will store sets of atom indices that make up candidate sugar rings
    for ring in ring_info:
        if len(ring) != 5:
            continue
        oxygen_count = 0
        carbon_count = 0
        valid_ring = True
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            a_num = atom.GetAtomicNum()
            # In a ribose ring, only carbons (6) and one oxygen (8) are expected.
            if a_num == 8:
                oxygen_count += 1
            elif a_num == 6:
                carbon_count += 1
            else:
                valid_ring = False
                break
            # To avoid fused systems, require each atom in the ring belongs to only one ring.
            if atom_ring_counts[idx] > 1:
                valid_ring = False
                break
        if valid_ring and oxygen_count == 1 and carbon_count == 4:
            sugar_rings.append(set(ring))

    if not sugar_rings:
        return False, "No sugar moiety (furanose ring with 4 carbons and 1 oxygen) detected"

    # -------------------------------
    # Step 3. Identify candidate nucleobase regions.
    # First, try canonical SMARTS patterns for adenine, guanine, cytosine, thymine/uracil, and xanthine.
    nucleobase_atoms = set()
    canonical_smarts = {
        'adenine': "c1ncnc2ncnc12",
        'guanine':  "c1nc2c(n1)[nH]cnc2=O",
        'cytosine': "n1c(=O)ncn1",
        # thymine and uracil share the core pattern (thymine has one extra methyl group)
        'thymine/uracil': "n1c(=O)[nH]c(=O)n1",
        'xanthine': "c1[nH]c(=O)nc(=O)n1"
    }
    for name, smarts in canonical_smarts.items():
        pattern = Chem.MolFromSmarts(smarts)
        if pattern is None:
            continue
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            nucleobase_atoms.update(match)

    # Fallback: If canonical patterns yield nothing, use a heuristic:
    # look for any ring (5- or 6-membered) with at least 2 nitrogen atoms.
    if not nucleobase_atoms:
        for ring in ring_info:
            if len(ring) not in (5, 6):
                continue
            n_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 7)
            if n_count >= 2:
                nucleobase_atoms.update(ring)

    if not nucleobase_atoms:
        return False, "No nucleobase detected via canonical SMARTS or fallback heterocycle patterns"

    # -------------------------------
    # Step 4. Identify the N-glycosidic bond connecting the sugar and the nucleobase.
    # For each candidate sugar ring, examine each carbon atom in the ring.
    # The sugar carbon should be bonded (by a single bond) to a nitrogen that is part of the nucleobase region.
    for sugar in sugar_rings:
        for idx in sugar:
            atom = mol.GetAtomWithIdx(idx)
            # We only check the carbons in the sugar ring.
            if atom.GetAtomicNum() != 6:
                continue
            for nbr in atom.GetNeighbors():
                nbr_idx = nbr.GetIdx()
                # We want to leave the sugar ring.
                if nbr_idx in sugar:
                    continue
                if nbr.GetAtomicNum() != 7:  # must be a nitrogen
                    continue
                # Only consider it if the nitrogen is part of the nucleobase (i.e. in the match).
                if nbr_idx not in nucleobase_atoms:
                    continue
                bond = mol.GetBondBetweenAtoms(idx, nbr_idx)
                if bond is None:
                    continue
                if bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
                    continue
                # Found a single bond connecting a carbon in a sugar ring and a nitrogen in the nucleobase.
                return True, "Molecule contains an N-glycosidic bond connecting a sugar moiety to a nucleobase"
    
    return False, "Found sugar and nucleobase motifs but no connecting N-glycosidic bond detected"

# Example usage:
if __name__ == "__main__":
    # Test with a canonical nucleoside (adenosine)
    test_smiles = "Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O"
    result, reason = is_nucleoside(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33838',
                          'name': 'nucleoside',
                          'definition': 'An N-glycosyl compound that has both '
                                        'a nucleobase, normally adenine, '
                                        'guanine, xanthine, thymine, cytosine '
                                        'or uracil, and either a ribose or '
                                        'deoxyribose as functional parents.',
                          'parents': [   'CHEBI:21731',
                                         'CHEBI:26912',
                                         'CHEBI:61120'],
                          'xrefs': ['KEGG:C00801', 'Wikipedia:Nucleoside'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 106,
                           'log_lines_of_code': 4.663439094112067,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
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
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetBondType',
                                                 'GetNeighbors',
                                                 'items',
                                                 'AtomRings',
                                                 'GetRingInfo',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'update',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append',
                                                 'GetNumAtoms',
                                                 'GetBondBetweenAtoms'],
                           'methods_called_count': 16,
                           'smarts_strings': ['smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_nucleoside(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Phosphate group detected; '
                                          'molecule is likely a nucleotide, '
                                          'not a nucleoside"',
                                          'False, "No sugar moiety (furanose '
                                          'ring with 4 carbons and 1 oxygen) '
                                          'detected"',
                                          'False, "No nucleobase detected via '
                                          'canonical SMARTS or fallback '
                                          'heterocycle patterns"',
                                          'True, "Molecule contains an '
                                          'N-glycosidic bond connecting a '
                                          'sugar moiety to a nucleobase"',
                                          'False, "Found sugar and nucleobase '
                                          'motifs but no connecting '
                                          'N-glycosidic bond detected"'],
                           'returns_count': 6,
                           'complexity': 6.532687818822413},
    'message': '\n'
               'Attempt failed: F1 score of 0.6518518518518519 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O1C(N2C3=NC=NC(NC/C=C(/CO)\\C)=C3N=C2)C(O)C(O)C1CO NAME: '
               '9-(beta-D-Ribofuranosyl)zeatin REASON: CORRECT Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: O1[C@@H](N2C=CC(=NC2=O)NC(=O)C)C[C@H](O)[C@H]1CO '
               "NAME: N(4)-acetyl-2'-deoxycytidine REASON: CORRECT Molecule "
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: [C@@H]1(N2C(NC(=O)C(C2)C)=O)O[C@H](CO)[C@H](C1)O '
               'NAME: 5,6-dihydrothymidine REASON: CORRECT Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: COc1nc(N)nc2n(cnc12)[C@H]1C[C@H](O)[C@@H](CO)O1 '
               "NAME: O(6)-methyl-2'-deoxyguanosine REASON: CORRECT Molecule "
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: O=C1NC(=NC2=C1N=CN2C3OC(CO)C(C3O)O)NC NAME: '
               'N2-methyl-guanosine REASON: CORRECT Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: C1CCC(C1)NC2=NC=NC3=C2N=CN3C4C(C(C(O4)CO)O)O NAME: '
               '2-[6-(cyclopentylamino)-9-purinyl]-5-(hydroxymethyl)oxolane-3,4-diol '
               'REASON: CORRECT Molecule contains an N-glycosidic bond '
               'connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'CNC(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(NCc3cccc(I)c3)ncnc12 '
               "NAME: 3-iodobenzyl-5'-N-methylcarboxamidoadenosine REASON: "
               'CORRECT Molecule contains an N-glycosidic bond connecting a '
               'sugar moiety to a nucleobase\n'
               ' * SMILES: O1C(N2C=3NC(=NC(=O)C3N=C2)N)C(O)C(O)C1CO NAME: '
               '2-amino-9-[3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]-3H-purin-6-one '
               'REASON: CORRECT Molecule contains an N-glycosidic bond '
               'connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               '[H]C(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(O)ncnc12 NAME: '
               "5'-dehydroinosine REASON: CORRECT Molecule contains an "
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               '[H][C@@](O)(C[C@H]1O[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2NC(C)=O)[C@H](NC(=O)\\C=C\\CCCCCCCCCCCCCC)[C@@H](O)[C@H]1O)[C@@]1([H])O[C@H]([C@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=O '
               'NAME: tunicamycin D1 REASON: CORRECT Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'C1=C(CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)C(NC(N1[C@@H]3O[C@H](CO)[C@H](C3)O)=O)=O '
               'NAME: (beta-D-glucopyranosyloxymethyl)deoxyuridine REASON: '
               'CORRECT Molecule contains an N-glycosidic bond connecting a '
               'sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'O1[C@@H]([N+]=2C=3N=C(N(C(=O)C3N(C2)C)C)N)[C@H]([O-])[C@H](O)[C@H]1CO '
               'NAME: 1,7-Dimethylguanosine REASON: CORRECT Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'NC1=C2C(N(C=N2)[C@@H]3O[C@@H]([C@H]([C@H]3O)O)CO)=NC(=N1)N4C=C(C=N4)C(NC)=O '
               'NAME: regadenoson REASON: CORRECT Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'Nc1nc2n([C@H]3C[C@H](O)[C@@H](CO)O3)c(Br)nc2c(=O)[nH]1 NAME: '
               "8-bromo-2'-deoxyguanosine REASON: CORRECT Molecule contains an "
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: CC1C(CC(O1)N2C=NC3=C2N=CN=C3N)O NAME: '
               '5-(6-aminopurin-9-yl)-2-methyl-3-oxolanol REASON: CORRECT '
               'Molecule contains an N-glycosidic bond connecting a sugar '
               'moiety to a nucleobase\n'
               ' * SMILES: '
               'CN(C)C1=NC=NC2=C1N=CN2C3C(C(C(O3)CO)NC(=O)C(CC4=CC=C(C=C4)OC)N)O '
               'NAME: '
               '2-amino-N-[5-[6-(dimethylamino)-9-purinyl]-4-hydroxy-2-(hydroxymethyl)-3-oxolanyl]-3-(4-methoxyphenyl)propanamide '
               'REASON: CORRECT Molecule contains an N-glycosidic bond '
               'connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: O1C(N2C3=NC(=NC(N)=C3N=C2)N)C(O)C(O)C1CO NAME: '
               '2,6-Diaminopurine riboside REASON: CORRECT Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: O1C(N2C=3N=CNC(=O)C3N=C2)C(O)C(OC)C1CO NAME: '
               '9-[3-hydroxy-5-(hydroxymethyl)-4-methoxyoxolan-2-yl]-1H-purin-6-one '
               'REASON: CORRECT Molecule contains an N-glycosidic bond '
               'connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'O1C(N2C3=NC=NC(NCCC4=CC=C(N)C=C4)=C3N=C2)C(O)C(O)C1CO NAME: '
               'N6-2-(4-Aminophenyl)ethyladenosine REASON: CORRECT Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'ClC1=NC(N)=C2N=CN(C2=N1)[C@H]3O[C@H](COS(=O)(=O)N)[C@H]([C@H]3O)O '
               'NAME: Dealanylascamycin REASON: CORRECT Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               '[C@@H]1(N2C(NC(=O)C(=C2)O)=O)O[C@H](CO)[C@H]([C@H]1O)O NAME: '
               '5-hydroxyuridine REASON: CORRECT Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: Cc1cn([C@@H]2C[C@@H](O)[C@H](CO)O2)c(=O)[nH]c1=O '
               'NAME: telbivudine REASON: CORRECT Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CF)[C@@H](O)[C@H]1O '
               "NAME: 5'-deoxy-5'-fluoroadenosine REASON: CORRECT Molecule "
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: S(=O)(CC1OC(N2C3=NC=NC(N)=C3N=C2)C(O)C1O)C NAME: '
               "(S)-5'-Deoxy-5'-(methylsulfinyl)adenosine REASON: CORRECT "
               'Molecule contains an N-glycosidic bond connecting a sugar '
               'moiety to a nucleobase\n'
               ' * SMILES: '
               'C[Se+](CC[C@H](N)C(O)=O)C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               'NAME: L-adenosylselenomethionine REASON: CORRECT Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               'False positives: SMILES: '
               'OC[C@H]1O[C@H](C[C@@H]1O)N1C=NC2=C1[NH+]=CNC[C@H]2O NAME: '
               'pentostatin(1+) REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C/1N[C@]2(OC=3C=CC=CC3C2)C(=O)N\\C1=C/C4=C(O)C=CC=C4 NAME: '
               'Spirobrocazine C REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N2C(=NC3=C1C=CC=C3)C(=O)C(C)(C)[C@]4([C@@H]2C[C@@]5(C6=C(C=CC=C6)N7[C@H]5NC(C)(C)C7=O)O4)O '
               'NAME: Scedapin D REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N[C@@H](CCC[C@@H]1NC(=O)C=2O[C@H](O[C@@H](C(=O)N)[C@H]3O[C@@H](N4C(=O)NC(=O)C=C4)[C@@H]([C@@H]3OC)O)C[C@H](C2)O)C '
               'NAME: A-500359 D REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=CC(N1)=O)[C@@H]2O[C@H]([C@@H](O[C@@H]3O[C@H](CN)[C@H]([C@H]3OC)O)[C@H](NCCCNC(=O)[C@@H](NC(=O)[C@@H](NC(=O)N[C@H](C(=O)O)C(C)C)[C@H]4NC(=NCC4)N)[C@@H](OC(=O)CCCCCCC(CC)C)C(C)C)C(=O)O)[C@H]([C@H]2O)O '
               'NAME: Muraymycin B1 REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=CC(N1)=O)[C@@H]2O[C@H]([C@H](NC(=O)[C@@H](N)CC3=CC=C(O)C=C3)C(=O)O)[C@@H]([C@H]2O)O '
               'NAME: Nikkomycin WZ REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'S(CCC(NC(=O)NC(C(=O)O)CC1=CC(O)=CC=C1)C(=O)NC(C(=O)N/C=C/2\\OC(N3C(=O)NC(=O)CC3)C(C2)O)C(N(C(=O)C4NC(C=5C=CC(=CC5C4)O)C)C)C)C '
               'NAME: Napsamycin D REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'S(=O)(CCC(NC(=O)NC(C(=O)O)CC=1C2=C(C=CC=C2)NC1)C(=O)NC(C(=O)N/C=C\\3/OC(N4C(=O)NC(=O)C=C4)C(C3)O)C(N(C(=O)C(N)CC5=CC(O)=CC=C5)C)C)C '
               'NAME: Sansanmycin C REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: O=C1NC=2N(C(=O)C(C)=NC2C(N1)=O)C3OC(CO)C(C3O)O '
               'NAME: '
               '8-[3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]-6-methyl-1H-pteridine-2,4,7-trione '
               'REASON: WRONGLY CLASSIFIED Molecule contains an N-glycosidic '
               'bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'O=C1N2C(=NC3=C1C=CC=C3)C(=O)C(C)(C)[C@@]4([C@H]2C[C@]5(C(=O)NC6=C5C=CC=C6)O4)O '
               'NAME: Scedapin E REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=CC(NC1=O)=NO '
               'NAME: N(4)-hydroxycytidine REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=C(C(N1)=O)/C=C/Br)[C@@H]2O[C@@H]([C@H]([C@@H]2O)O)CO '
               'NAME: Sorivudine REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'C[S@@+](CC[C@H](N)C(O)=O)C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               'NAME: (S)-S-adenosyl-L-methionine REASON: WRONGLY CLASSIFIED '
               'Molecule contains an N-glycosidic bond connecting a sugar '
               'moiety to a nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=CC(N1)=O)[C@@H]2O[C@H]([C@H](NC(=O)[C@@H](N)[C@H](O)[C@@H](O)COC(=O)N)C(=O)O)[C@H]([C@H]2O)O '
               'NAME: Polyoxin L REASON: WRONGLY CLASSIFIED Molecule contains '
               'an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'S([C@@]12N(C(=O)[C@@]3(OC=4C=CC=CC4C3)NC1=O)[C@@H]5[C@@H](O)C=CC=C5C2)C '
               'NAME: Eutypellazine P REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=NC2=C1C=CC=C2)[C@H]3C(=O)O[C@@]4(C3)C5=C(C=CC=C5)N6[C@@H]4NC(C)(C)C6=O '
               'NAME: Tryptoquivaline U REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               '[H+].[Cl-].Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)C2(F)F)c(=O)n1 '
               'NAME: gemcitabine hydrochloride REASON: WRONGLY CLASSIFIED '
               'Molecule contains an N-glycosidic bond connecting a sugar '
               'moiety to a nucleobase\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2[C@H](O)CNC=[NH+]c12 '
               'NAME: coformycin(1+) REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N(C(C(=O)O)C(OC(=O)CC(OC(=O)CC(CC(=O)O[C@@H]2O[C@H]([C@H](OC)[C@H]([C@H]2OC)OC(=O)CCC(=O)O)CC)C)CCCCCCCCCCC)CN(C1C(O[C@@H]3O[C@H](CN)[C@H](C3)O)[C@H]4O[C@@H](N5C(=O)NC(=O)C=C5)C[C@@H]4O)C)C '
               'NAME: Muraminomicin F REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N[C@]2(O[C@H]3C=C[C@H]([C@@H]([C@@]3(C2)O)O)O)C(=O)NC1=CC4=C(O)C(OC)=C(OC)C=C4 '
               'NAME: Penispirozine E REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=CC(N1)=O)C2OC(C(NC(=O)C(N)C(C(O)C3=NC=CC=C3)C)C(=O)O)C(C2O)O '
               'NAME: Nikkomycin Lz REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'NC(=O)CNc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O NAME: '
               'alpha-N-(9-beta-D-ribofuranosylpurin-6-yl)glycinamide REASON: '
               'WRONGLY CLASSIFIED Molecule contains an N-glycosidic bond '
               'connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=CC(N1)=O)C2OC(C(OC3OC(C(=O)NC4=CC=C(C(O)C(O)C(=O)N/C=C/C(=O)NCC(=O)O)C=C4)=CC(C3O)O)C(=O)N)C(C2O)OC '
               'NAME: '
               '2-[[(E)-3-[[3-[4-[[2-[2-amino-1-[5-(2,4-dioxopyrimidin-1-yl)-4-hydroxy-3-methoxyoxolan-2-yl]-2-oxoethoxy]-3,4-dihydroxy-3,4-dihydro-2H-pyran-6-carbonyl]amino]phenyl]-2,3-dihydroxypropanoyl]amino]prop-2-enoyl]amino]acetic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains an '
               'N-glycosidic bond connecting a sugar moiety to a nucleobase\n'
               ' * SMILES: '
               'O=C1N(C=CC(N1)=O)[C@@H]2O/C(=C\\NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)N[C@H](C(=O)O)CC3=CC=CC=C3)C)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](N)C)CC4=CC(O)=CC=C4)C)C)/C[C@H]2O '
               'NAME: Pacidamycin 2 REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)O)[C@@H](OC(=O)C[C@@H](OC(=O)C[C@@H](CC(=O)O[C@@H]2O[C@@H]([C@@H](OC)[C@H]([C@H]2OC)OC)C)C)CCCCCCCCC(C)C)CN([C@H]1C(O[C@@H]3O[C@H](CN)[C@H]([C@H]3O)O)[C@H]4O[C@@H](N5C(=O)NC(=O)C=C5)[C@@H]([C@@H]4O)O)C)C '
               'NAME: (-)-Caprazamycin F REASON: WRONGLY CLASSIFIED Molecule '
               'contains an N-glycosidic bond connecting a sugar moiety to a '
               'nucleobase\n'
               'False negatives: SMILES: '
               'CN(CC[C@H](N)CC(=O)N[C@H]1C=C[C@@H](O[C@@H]1C(O)=O)n1ccc(N)nc1=O)C(N)=N '
               'NAME: blasticidin S REASON: MISSED No sugar moiety (furanose '
               'ring with 4 carbons and 1 oxygen) detected\n'
               ' * SMILES: '
               'CC(=O)N[C@H]1[C@@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)O[C@H](CC(O)[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H]1O '
               'NAME: UDP-N-acetyltunicamine-uracil REASON: MISSED Phosphate '
               'group detected; molecule is likely a nucleotide, not a '
               'nucleoside\n'
               ' * SMILES: '
               'P(OOOCC1OC(N2C=3N=C(NC(=O)C3N=C2)N)CC1O)(OP(O)(O)=O)(O)=O '
               'NAME: '
               '[5-(2-Amino-6-oxo-1H-purin-9-yl)-3-hydroxyoxolan-2-yl]methylperoxy '
               'phosphono hydrogen phosphate REASON: MISSED Phosphate group '
               'detected; molecule is likely a nucleotide, not a nucleoside\n'
               ' * SMILES: '
               'N[C@@H](CCCCNc1nc(=N)ccn1[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O)C(O)=O '
               'NAME: lysidine monophosphate REASON: MISSED Phosphate group '
               'detected; molecule is likely a nucleotide, not a nucleoside\n'
               ' * SMILES: '
               'C[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)C(O)=O '
               "NAME: L-lactyl-2-diphospho-5'-guanosine REASON: MISSED "
               'Phosphate group detected; molecule is likely a nucleotide, not '
               'a nucleoside\n'
               ' * SMILES: '
               'C[C@H](CNC(=O)CC[C@]1(C)[C@@H](CC(N)=O)[C@H]2N3C1=C(C)C1=[N+]4C(=CC5=[N+]6C(=C(C)C7=[N+]([C@]2(C)[C@@](C)(CC(N)=O)[C@@H]7CCC(N)=O)[Co--]346C[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@](C)(CC(N)=O)[C@@H]5CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O)OP(O)(O)=O '
               'NAME: adenosylcobinamide phosphate REASON: MISSED Phosphate '
               'group detected; molecule is likely a nucleotide, not a '
               'nucleoside\n'
               ' * SMILES: '
               'NC1=NC2=C(C(CN[C@H]3C=C[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H]3O)=CN2[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)C(=O)N1 '
               "NAME: O-4''-alpha-D-mannosylqueuosine REASON: MISSED Found "
               'sugar and nucleobase motifs but no connecting N-glycosidic '
               'bond detected\n'
               ' * SMILES: '
               'CNCC(=O)N[C@H](CO)C(=O)N[C@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1C(N)=O)N1C=CC(N)=NC1=O '
               'NAME: gougerotin REASON: MISSED No sugar moiety (furanose ring '
               'with 4 carbons and 1 oxygen) detected\n'
               ' * SMILES: '
               'N1=CN=C2C(=C1N)C(=CN2[C@H]3[C@H](O)[C@H](O)[C@H](O3)CO)C#N '
               'NAME: toyocamycin REASON: MISSED Found sugar and nucleobase '
               'motifs but no connecting N-glycosidic bond detected\n'
               ' * SMILES: '
               'Nc1nc2n(cc(CN[C@H]3C=C[C@H](O)[C@@H]3O)c2c(=O)[nH]1)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: queuosine REASON: MISSED Found sugar and nucleobase '
               'motifs but no connecting N-glycosidic bond detected\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Phosphate group detected; '
                                               'molecule is likely a '
                                               'nucleotide, not a nucleoside'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No sugar moiety (furanose ring '
                                               'with 4 carbons and 1 oxygen) '
                                               'detected'}],
    'sample_false_negatives': [   {   'smiles': 'CN(CC[C@H](N)CC(=O)N[C@H]1C=C[C@@H](O[C@@H]1C(O)=O)n1ccc(N)nc1=O)C(N)=N',
                                      'name': 'blasticidin S',
                                      'reason': 'No sugar moiety (furanose '
                                                'ring with 4 carbons and 1 '
                                                'oxygen) detected'},
                                  {   'smiles': 'CC(=O)N[C@H]1[C@@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)O[C@H](CC(O)[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H]1O',
                                      'name': 'UDP-N-acetyltunicamine-uracil',
                                      'reason': 'Phosphate group detected; '
                                                'molecule is likely a '
                                                'nucleotide, not a nucleoside'},
                                  {   'smiles': 'P(OOOCC1OC(N2C=3N=C(NC(=O)C3N=C2)N)CC1O)(OP(O)(O)=O)(O)=O',
                                      'name': '[5-(2-Amino-6-oxo-1H-purin-9-yl)-3-hydroxyoxolan-2-yl]methylperoxy '
                                              'phosphono hydrogen phosphate',
                                      'reason': 'Phosphate group detected; '
                                                'molecule is likely a '
                                                'nucleotide, not a nucleoside'},
                                  {   'smiles': 'N[C@@H](CCCCNc1nc(=N)ccn1[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O)C(O)=O',
                                      'name': 'lysidine monophosphate',
                                      'reason': 'Phosphate group detected; '
                                                'molecule is likely a '
                                                'nucleotide, not a nucleoside'},
                                  {   'smiles': 'C[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)C(O)=O',
                                      'name': "L-lactyl-2-diphospho-5'-guanosine",
                                      'reason': 'Phosphate group detected; '
                                                'molecule is likely a '
                                                'nucleotide, not a nucleoside'},
                                  {   'smiles': 'C[C@H](CNC(=O)CC[C@]1(C)[C@@H](CC(N)=O)[C@H]2N3C1=C(C)C1=[N+]4C(=CC5=[N+]6C(=C(C)C7=[N+]([C@]2(C)[C@@](C)(CC(N)=O)[C@@H]7CCC(N)=O)[Co--]346C[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@](C)(CC(N)=O)[C@@H]5CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O)OP(O)(O)=O',
                                      'name': 'adenosylcobinamide phosphate',
                                      'reason': 'Phosphate group detected; '
                                                'molecule is likely a '
                                                'nucleotide, not a nucleoside'},
                                  {   'smiles': 'NC1=NC2=C(C(CN[C@H]3C=C[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H]3O)=CN2[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)C(=O)N1',
                                      'name': "O-4''-alpha-D-mannosylqueuosine",
                                      'reason': 'Found sugar and nucleobase '
                                                'motifs but no connecting '
                                                'N-glycosidic bond detected'},
                                  {   'smiles': 'CNCC(=O)N[C@H](CO)C(=O)N[C@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1C(N)=O)N1C=CC(N)=NC1=O',
                                      'name': 'gougerotin',
                                      'reason': 'No sugar moiety (furanose '
                                                'ring with 4 carbons and 1 '
                                                'oxygen) detected'},
                                  {   'smiles': 'N1=CN=C2C(=C1N)C(=CN2[C@H]3[C@H](O)[C@H](O)[C@H](O3)CO)C#N',
                                      'name': 'toyocamycin',
                                      'reason': 'Found sugar and nucleobase '
                                                'motifs but no connecting '
                                                'N-glycosidic bond detected'},
                                  {   'smiles': 'Nc1nc2n(cc(CN[C@H]3C=C[C@H](O)[C@@H]3O)c2c(=O)[nH]1)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O',
                                      'name': 'queuosine',
                                      'reason': 'Found sugar and nucleobase '
                                                'motifs but no connecting '
                                                'N-glycosidic bond detected'}],
    'attempt': 3,
    'reasoning': 'Below is our revised Python code with added checks. In our '
                 'reasoning we realized that many of the false‐positives arose '
                 'because the sugar‐like ring was part of an extended, fused '
                 'system that is not an isolated ribose/deoxyribose. To '
                 'improve the classification, we now (1) exclude molecules '
                 'that contain any phosphorus atoms, (2) search for '
                 'five‐membered rings containing exactly four carbons and one '
                 'oxygen and (3) require that all atoms in such a ring belong '
                 'to exactly one ring (to avoid fused ring systems), (4) '
                 'identify canonical nucleobases using SMARTS (with a fallback '
                 'heuristic if necessary), and (5) require that one of the '
                 'sugar ring carbons is single‐bonded to a nitrogen that is '
                 'part of a nucleobase region. This extra ring membership '
                 'check helps remove false positives that arise from '
                 'sugar–like fragments that are part of polycyclic systems.\n'
                 '\n'
                 'Below is the complete code block in Python:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 307,
    'num_false_positives': 237,
    'num_true_negatives': 141733,
    'num_false_negatives': 23,
    'num_negatives': None,
    'precision': 0.5643382352941176,
    'recall': 0.9303030303030303,
    'f1': 0.702517162471396,
    'accuracy': 0.9981728742094167,
    'negative_predictive_value': 0.9998377493721606}