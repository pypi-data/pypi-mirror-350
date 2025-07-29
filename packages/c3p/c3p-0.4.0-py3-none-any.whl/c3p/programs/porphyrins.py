"""
Classifies: CHEBI:26214 porphyrins
"""
"""
Classifies: Porphyrins – natural pigments containing four pyrrole-like rings
united by four methine bridges to yield an aromatic, conjugated macrocyclic core.
This improved version uses two heuristics:
  1. It searches for a macrocyclic ring between 15 and 18 atoms that contains exactly
     4 nitrogen atoms and in which the vast majority of atoms are aromatic.
  2. It checks if the molecule has a metal center (e.g. Mg, Fe, Zn, Co, Ni, Cu, Pd, Pt)
     that is directly bonded to exactly 4 aromatic nitrogen atoms.
If at least one heuristic is met, the molecule is classified as a porphyrin.
"""

from rdkit import Chem

def is_porphyrins(smiles: str):
    """
    Determines if a molecule is a porphyrin based on its SMILES string using two heuristics:
      Heuristic 1:
        Searches for a macrocyclic ring (15–18 atoms) with exactly 4 nitrogen atoms
        and where at least 80% of the atoms in the ring are aromatic.
      Heuristic 2:
        Checks if the molecule contains a metal atom (e.g. Mg, Fe, Zn, Co, Ni, Cu, Pd, Pt)
        bonded to exactly 4 aromatic nitrogen atoms.
        
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a porphyrin, False otherwise.
        str: Explanation for the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()
    
    # Heuristic 1: Look for a macrocycle (15–18 atoms) with exactly 4 nitrogen atoms.
    # Also require that at least 80% of the atoms in the ring are aromatic.
    for ring in atom_rings:
        ring_size = len(ring)
        if 15 <= ring_size <= 18:
            atoms_in_ring = [mol.GetAtomWithIdx(idx) for idx in ring]
            n_count = sum(1 for atom in atoms_in_ring if atom.GetAtomicNum() == 7)
            aromatic_count = sum(1 for atom in atoms_in_ring if atom.GetIsAromatic())
            # We require exactly 4 nitrogen atoms and that most atoms in the ring are aromatic.
            if n_count == 4 and aromatic_count >= int(0.8 * ring_size):
                reason = (f"Found a macrocyclic ring of {ring_size} atoms with exactly 4 nitrogen atoms "
                          f"and high aromaticity ({aromatic_count}/{ring_size} atoms aromatic), "
                          "consistent with a porphyrin core.")
                return True, reason

    # Heuristic 2: Look for a metal center directly bonded to 4 aromatic nitrogen atoms.
    # List of common metal atomic numbers in porphyrins.
    metal_atomic_nums = {12, 26, 27, 28, 29, 30, 46, 78}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() in metal_atomic_nums:
            # Count neighboring nitrogen atoms that are aromatic.
            aromatic_n_neighbors = [nbr for nbr in atom.GetNeighbors() 
                                    if nbr.GetAtomicNum() == 7 and nbr.GetIsAromatic()]
            if len(aromatic_n_neighbors) == 4:
                reason = (f"Metal atom {atom.GetSymbol()} (atomic num {atom.GetAtomicNum()}) "
                          "is coordinated to 4 aromatic nitrogen atoms, consistent with a metalloporphyrin core.")
                return True, reason
    
    # If neither heuristic triggers, list both shortcomings.
    reasons = []
    reasons.append("No macrocyclic ring (15–18 atoms with exactly 4 nitrogen atoms and high aromaticity) found.")
    reasons.append("No metal center coordinated to exactly 4 aromatic nitrogen atoms was detected.")
    return False, " ".join(reasons)

# Example usage:
if __name__ == "__main__":
    # Test with one of the provided examples (e.g. for chlorophyll a')
    test_smiles = ("C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\C)=O)C)"
                   "[Mg-2]735)[C@@H](C(C8=C6C)=O)C(=O)OC)C(=C4C)C=C)=C(C2C)C=C")
    result, reason = is_porphyrins(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26214',
                          'name': 'porphyrins',
                          'definition': 'Natural pigments containing a '
                                        'fundamental skeleton of four pyrrole '
                                        'nuclei united through the '
                                        'alpha-positions by four methine '
                                        'groups to form a macrocyclic '
                                        'structure.',
                          'parents': ['CHEBI:36309'],
                          'xrefs': ['Wikipedia:Porphyrin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 56,
                           'log_lines_of_code': 4.02535169073515,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
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
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'join',
                                                 'GetSymbol',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'GetAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetRingInfo',
                                                 'GetIsAromatic'],
                           'methods_called_count': 11,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_porphyrins(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, reason',
                                          'True, reason',
                                          'False, " ".join(reasons)'],
                           'returns_count': 4,
                           'complexity': 4.80507033814703},
    'message': '\n'
               'Attempt failed: F1 score of 0.4099821746880571 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\C)=O)C)[Mg-2]735)[C@@H](C(C8=C6C)=O)C(=O)OC)C(=C4C)C=C)=C(C2C)C=C '
               "NAME: divinylchlorophyll a' REASON: CORRECT Metal atom Mg "
               '(atomic num 12) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'COC(=O)CCc1c(C)c2cc3[nH]c(cc4nc(cc5[nH]c(cc1n2)c(CCC(O)=O)c5C)c(C=C)c4C)C1=CC=C([C@@H](C(=O)OC)[C@@]31C)C(=O)OC '
               'NAME: '
               '(2R,2(1)S)-8-ethenyl-2(1),2(2)-bis(methoxycarbonyl)-17-(3-methoxy-3-oxopropyl)-2,7,12,18-tetramethyl-2,2(1)-dihydrobenzo[b]porphyrin-13-propanoic '
               'acid REASON: CORRECT Found a macrocyclic ring of 16 atoms with '
               'exactly 4 nitrogen atoms, consistent with a porphyrin core.\n'
               ' * SMILES: '
               'CC1=C(CCC(O)=O)C2=[N]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N]5[Fe]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2 '
               'NAME: heme b REASON: CORRECT Metal atom Fe (atomic num 26) is '
               'coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               'CC1OC(=O)C[C@@]2(C)[C@H](CCC(O)=O)C3=CC4=[N+]5C(=CC6=[N+]7C(=CC8=[N+]9C(=C(CC(O)=O)[C@@]8(C)CCC(O)=O)C12N3[Co--]579)C(CCC(O)=O)=C6CC(O)=O)[C@@H](CCC(O)=O)[C@]4(C)CC(O)=O '
               'NAME: cobalt(II)-factor IV REASON: CORRECT Metal atom Co '
               '(atomic num 27) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'CC1C2=[N+]3C(=Cc4c(C)c(CCC(O)=O)c5C=C6C(CCC(O)=O)=C(C)C7=[N+]6[Fe--]3(n45)n3c(=C2)c(C)c(C)c3=C7)C1(C)C '
               'NAME: iron methylchlorin REASON: CORRECT Metal atom Fe (atomic '
               'num 26) is coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               'CC1=C(CCC(O)=O)C2=[N]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N]5[Zn]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2 '
               'NAME: zinc protoporphyrin REASON: CORRECT Metal atom Zn '
               '(atomic num 30) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: chlorophyll a REASON: CORRECT Metal atom Mg (atomic num '
               '12) is coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               'CC(O)c1c(C)c2cc3[nH]c(cc4nc(cc5[nH]c(cc1n2)c(C)c5CCC(O)=O)c(CCC(O)=O)c4C)c(C)c3C(C)O '
               'NAME: hematoporphyrin REASON: CORRECT Found a macrocyclic ring '
               'of 16 atoms with exactly 4 nitrogen atoms, consistent with a '
               'porphyrin core.\n'
               ' * SMILES: '
               'C=1C=2C(=C(C=3N2[Pd]45N=6C(=CC=7N4C(C3)=C(C7CC)CC)C(C(C6C=C8N5C1C(=C8CC)CC)=O)(CC)CC)CC)CC '
               'NAME: palladium(II) octaethylporphyrinketone REASON: CORRECT '
               'Metal atom Pd (atomic num 46) is coordinated to 4 nitrogen '
               'atoms, consistent with a metalloporphyrin core.\n'
               ' * SMILES: '
               'CC1=C(CCC(O)=O)C2=[N+]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N+]5[Mg--]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2 '
               'NAME: magnesium protoporphyrin REASON: CORRECT Metal atom Mg '
               '(atomic num 12) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'CC1=C(CCC(O)=O)C2=[N+]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N+]5[Fe--]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2 '
               'NAME: ferroheme b REASON: CORRECT Metal atom Fe (atomic num '
               '26) is coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3C=C4C(C=C)=C(C=O)C5=[N+]4[Mg--]46n3c2C1=C1[C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@H](C)C(C=c2c(C)c(C=C)c(=C5)n42)=[N+]61 '
               'NAME: divinyl chlorophyll b REASON: CORRECT Metal atom Mg '
               '(atomic num 12) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'OC(=O)CCC1=C(C=2NC1=CC3=NC(C(=C3CCC(O)=O)C)=CC4=NC(C(=C4C)CCC(O)=O)=CC=5NC(=C(C5CCC(O)=O)C)C2)C '
               'NAME: Coproporphyrin II REASON: CORRECT Found a macrocyclic '
               'ring of 16 atoms with exactly 4 nitrogen atoms, consistent '
               'with a porphyrin core.\n'
               ' * SMILES: '
               'O=C1[C@@H](C2=C3NC([C@H]([C@@H]3CCC(O)=O)C)=CC=4NC(=C(C4C)C=C)C=C5NC(=CC=6NC2=C1C6C)C(=C5C)CC)C(OC)=O '
               'NAME: '
               '3-[(3R,21S,22S)-16-Ethenyl-11-ethyl-3-methoxycarbonyl-12,17,21,26-tetramethyl-4-oxo-7,23,24,25-tetrazahexacyclo[18.2.1.15,8.110,13.115,18.02,6]hexacosa-1,5,8(26),9,11,13,15,17,19-nonaen-22-yl]propanoic '
               'acid REASON: CORRECT Found a macrocyclic ring of 16 atoms with '
               'exactly 4 nitrogen atoms, consistent with a porphyrin core.\n'
               ' * SMILES: '
               'CC1=C(CCC([O-])=O)C2=[N+]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N+]5[Fe-]3(n14)n1c(=C6)c(C)c(CCC([O-])=O)c1=C2 '
               'NAME: ferriheme b(1-) REASON: CORRECT Metal atom Fe (atomic '
               'num 26) is coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]735)[C@H](C(C8C6C)=O)C(=O)OC)/C(/[C@H]4C)=C\\C)C(=C2C)C=C '
               'NAME: bacteriochlorophyllide g REASON: CORRECT Metal atom Mg '
               '(atomic num 12) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'CCC1=C(C)C2=[N+]3C1=Cc1c(C)c4C(=O)[C@H](C(=O)OC)C5=C6C(CCC(O)=O)=C(C)C7=[N+]6[Mg--]3(n1c45)n1c(=C7)c(C)c(C=C)c1=C2 '
               'NAME: protochlorophyllide REASON: CORRECT Metal atom Mg '
               '(atomic num 12) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               ' * SMILES: '
               'Bc1c2ccc(n2)c(B)c2ccc([nH]2)c(B)c2ccc(n2)c(B)c2ccc1[nH]2 NAME: '
               '5,10,15,20-tetraborylporphyrin REASON: CORRECT Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'CC(S)C1=C(C)C2=Cc3c(C(C)S)c(C)c4C=C5C(C)=C(CCC(O)=O)C6=[N+]5[Fe--]5(n34)n3c(=CC1=[N+]25)c(C)c(CCC(O)=O)c3=C6 '
               'NAME: ferroheme c REASON: CORRECT Metal atom Fe (atomic num '
               '26) is coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               'CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(O)=O)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: chlorophyllide a REASON: CORRECT Metal atom Mg (atomic '
               'num 12) is coordinated to 4 nitrogen atoms, consistent with a '
               'metalloporphyrin core.\n'
               ' * SMILES: '
               '[Zn+2].O=C(O)CCC=1C=2N=C(C1C)C=C3NC(=CC=4NC(C=C5N=C(C2)C(=C5CCC(=O)O)C)=C(C4CCC(=O)O)C)C(=C3CCC(=O)O)C '
               'NAME: Zincmethylphyrin I REASON: CORRECT Found a macrocyclic '
               'ring of 16 atoms with exactly 4 nitrogen atoms, consistent '
               'with a porphyrin core.\n'
               ' * SMILES: '
               'Nc1ccccc1-c1c2ccc(n2)c(-c2ccccc2N)c2ccc([nH]2)c(-c2ccccc2N)c2ccc(n2)c(-c2ccccc2N)c2ccc1[nH]2 '
               'NAME: tetrakis(o-aminophenyl)porphyrin REASON: CORRECT Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'c1ccc(cc1)-c1c2ccc(n2)c(-c2ccccc2)c2ccc([nH]2)c(-c2ccccc2)c2ccc(n2)c(-c2ccccc2)c2ccc1[nH]2 '
               'NAME: tetraphenylporphyrin REASON: CORRECT Found a macrocyclic '
               'ring of 16 atoms with exactly 4 nitrogen atoms, consistent '
               'with a porphyrin core.\n'
               ' * SMILES: '
               'CCC1=C(CC)C2=[N]3C1=Cc1c(CC)c(CC)c4C=C5[N]6=C(C=c7c(CC)c(CC)c(=C2)n7[Pt]36n14)C(=O)C5(CC)CC '
               'NAME: platinum(II) octaethylporphyrin ketone REASON: CORRECT '
               'Metal atom Pt (atomic num 78) is coordinated to 4 nitrogen '
               'atoms, consistent with a metalloporphyrin core.\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3C=C4C(C=C)=C(C)C5=[N+]4[Mg--]46n3c2C1=C1[C@@H](CCC(O)=O)[C@H](C)C(C=c2c(C)c(C=C)c(=C5)n42)=[N+]61 '
               'NAME: divinyl chlorophyllide a REASON: CORRECT Metal atom Mg '
               '(atomic num 12) is coordinated to 4 nitrogen atoms, consistent '
               'with a metalloporphyrin core.\n'
               'False positives: SMILES: '
               'C1=2NC(C=C3N=C(C=C4NC(=CC5=NC(=C1)C(=C5CCC(=O)[O-])C)C(=C4C)CCC(=O)[O-])C(=C3C)CCC(=O)[O-])=C(C2C)CCC(=O)[O-] '
               'NAME: coproporphyrin III(4-) REASON: WRONGLY CLASSIFIED Found '
               'a macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'O=C/1N[C@@H](C(=O)N[C@H](C(=O)O[C@H](C)[C@@H](C(N[C@H](C(N\\C1=C/C)=O)C)=O)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C=C(C)C)C(C)C)CC2=CC=C(O)C=C2)CC(C)C)CCC(=O)O '
               'NAME: Largamide A REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               '[H][C@]12[C@H](CC(O)=O)[C@@](C)(CCC(O)=O)C3=[N+]1[Co--]14N5C(=CC6=[N+]1C(C[C@@]1(C)C(CC(O)=O)=C(CCC(O)=O)C(C3)=[N+]41)=C(CCC(O)=O)[C@]6(C)CC(O)=O)[C@@H](CCC(O)=O)[C@](C)(CC(O)=O)[C@]25C '
               'NAME: cobalt-precorrin-6B REASON: WRONGLY CLASSIFIED Metal '
               'atom Co (atomic num 27) is coordinated to 4 nitrogen atoms, '
               'consistent with a metalloporphyrin core.\n'
               ' * SMILES: '
               'C=12NC3(C(C4=NC(=CC=5NC=6C(=C7N=C(C1)[C@H]([C@@H]7CCC([O-])=O)C)[C-](C(C6C5C)=O)C(=O)OC)C(=C4C)CC)O3)C(=C2C)C=C '
               'NAME: epoxypheophorbide a(2-) REASON: WRONGLY CLASSIFIED Found '
               'a macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'S(=O)(=O)(O)C1=C(O)C(O)=C(C(=O)NCCCCC(N)C(O)CC(=O)NC(C(=O)NC(C(=O)NC2C(=O)NC(C(=O)NC(C(=O)NCC(NCCCC2)=O)C(O)C(=O)O)CCCCN)C(O)C(=O)O)CC(=O)N)C=C1 '
               'NAME: Pseudoalterobactin A REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'C[C@]1(CC([O-])=O)[C@H](CCC([O-])=O)C2=CC3=[N+]4C(Cc5c(CCC([O-])=O)c(CC([O-])=O)c6C=C7[N+]8=C(C=C1N2[Co--]48n56)[C@@H](CCC([O-])=O)[C@]7(C)CC([O-])=O)=C(CCC([O-])=O)C3CC([O-])=O '
               'NAME: cobalt-precorrin-2(8-) REASON: WRONGLY CLASSIFIED Metal '
               'atom Co (atomic num 27) is coordinated to 4 nitrogen atoms, '
               'consistent with a metalloporphyrin core.\n'
               ' * SMILES: '
               'C=12[C@H]([C@@](CC(N)=O)(C)C=3[N+]1[Ni-2]45N6C(C3)=C(C(CCC([O-])=O)=C6C=C7[N+]5=C(C=C8N4C(=C2)[C@]([C@@H]8CCC([O-])=O)(CC(N)=O)C)C(=C7CCC([O-])=O)CC([O-])=O)CC([O-])=O)CCC([O-])=O '
               'NAME: nickel-sirohydrochlorin a,c-diamide(6-) REASON: WRONGLY '
               'CLASSIFIED Metal atom Ni (atomic num 28) is coordinated to 4 '
               'nitrogen atoms, consistent with a metalloporphyrin core.\n'
               ' * SMILES: '
               'CC(=O)C12N\\C(=C/C3=NC(Cc4[nH]c(CC5=NC1=C(CC([O-])=O)[C@@]5(C)CCC([O-])=O)c(CCC([O-])=O)c4CC([O-])=O)=C(CCC([O-])=O)[C@]3(C)CC([O-])=O)[C@@H](CCC([O-])=O)[C@]2(C)CC([O-])=O '
               'NAME: precorrin-4(8-) REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 15 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'O=C1OC(C(NC(=O)C2=C(N)C(=O)C(C)=C3C2=NC4=C(C(=C(N)C=C4C(=O)NC5C(=O)NC(C(=O)N6C(C(=O)N(C)CC(N(C(C(OC5C)=O)C(C)C)C)=O)CCC6)C(C)C)C)O3)C(=O)NC(C(=O)N7CCCC7C(N(CC(N(C1C(C)C)C)=O)C)=O)C(C)C)C '
               'NAME: 7-AAD REASON: WRONGLY CLASSIFIED Found a macrocyclic '
               'ring of 16 atoms with exactly 4 nitrogen atoms, consistent '
               'with a porphyrin core.\n'
               ' * SMILES: '
               'ClC[C@H]1OC(=O)[C@@H](N(C(=O)CN(C(=O)[C@H]2N(C([C@H](NC([C@H]1NC(=O)C3=C(N)C(=O)C(C)=C4C3=NC5=C(C(=CC=C5C(=O)N[C@@H]6C(=O)N[C@@H](C(=O)N7[C@H](C(=O)N(C)CC(N([C@H](C(O[C@@H]6C)=O)C(C)C)C)=O)[C@@H](O)C[C@@H]7C)C(C)C)C)O4)=O)C(C)C)=O)CC(O)C2)C)C)C '
               'NAME: Actinomycin Y2 REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC([O-])=O)C)[Mg-2]753)CC(C8C6C)=O)C(=C4C)CC)C(=C2C)C=C '
               'NAME: 3-vinylbacteriochlorophyllide d(1-) REASON: WRONGLY '
               'CLASSIFIED Metal atom Mg (atomic num 12) is coordinated to 4 '
               'nitrogen atoms, consistent with a metalloporphyrin core.\n'
               ' * SMILES: '
               'O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)CC(C)C)=O)CC(C)C)CC(C)C)CCCCCCCC(CC)C '
               'NAME: Bacilotetrin A REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'O=C1N[C@@H]2C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(O[C@@H]2C)=O)CC3=CC(OC4=CC=C(C[C@H]1NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CCC)CC(C)C)C)C=C4)=C(O)C=C3)=O)[C@H](CC)C)CC(C)C)CC(C)C '
               'NAME: Seongsanamide C REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@H](NC(=O)C(NC(=O)CC(O)CCCCCCCCCCC)CC(C)C)C(=O)N[C@@H](C(=O)N[C@H](C(NC(C(NC1CC(C)C)=O)CC(C)C)=O)[C@@H](O)C)CO)C '
               'NAME: Ngercheumicin G REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'O=C1N[C@@H]2C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(O[C@@H]2C)=O)CC3=CC(OC4=CC=C(C[C@H]1NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CC(C)C)CC(C)C)C)C=C4)=C(O)C=C3)=O)[C@H](CC)C)CC(C)C)CC(C)C '
               'NAME: Seongsanamide D REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'OC=1CC2=C3NC(C(C3CCC(O)=O)C)=CC4=NC(C(=C4C)C=C)=CC5=NC(=CC=6N=C2C1C6C)C(=C5C)CC '
               'NAME: Pyrophaeophorbide a REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'C1C\\C2=C\\C3=N\\C(CC3)=C/C3=N/C(CC3)=C\\C3=NC(CC3)C1N2 NAME: '
               'corrin REASON: WRONGLY CLASSIFIED Found a macrocyclic ring of '
               '15 atoms with exactly 4 nitrogen atoms, consistent with a '
               'porphyrin core.\n'
               ' * SMILES: '
               'ClC[C@H]1OC(=O)[C@@H](N(C(=O)CN(C(=O)[C@H]2N(C([C@H](NC([C@H]1NC(=O)C3=C(N)C(=O)C(C)=C4C3=NC5=C(C(=CC=C5C(=O)N[C@@H]6C(=O)N[C@@H](C(=O)N7[C@H](C(=O)N(C)CC(N([C@H](C(O[C@@H]6C)=O)C(C)C)C)=O)[C@@H](O)C[C@@H]7C)C(C)C)C)O4)=O)C(C)C)=O)CC(=O)C2)C)C)C '
               'NAME: Actinomycin Y1 REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               '[H]C(=O)c1c(CCC(O)=O)c2cc3[n-]c(cc4nc(cc5[n-]c(cc1n2)c(C)c5C(O)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)c(C)c4C=C)c(C)c3CCC(O)=O '
               'NAME: cytoporphyrinate REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'C[C@@H](O)[C@@H]1NC(=O)[C@@H](NC(=O)[C@H](CCCN(O)C=O)NC(=O)[C@H](CCCCNC1=O)NC(=O)[C@H](CCCN(O)C=O)NC(=O)[C@@H](CO)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@@H](CO)NC(=O)[C@@H]1CCN=C2N1c1cc(O)c(O)cc1C=C2NC(=O)CCC(O)=O)[C@@H](C)O '
               'NAME: Pyoverdine I REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 16 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'C[C@@]12CC3=C(CCC([O-])=O)[C@](C)(CC([O-])=O)C(/C=C4\\N[C@@](C)(C5=C(CC([O-])=O)[C@@](C)(CCC([O-])=O)C(CC(=N1)C(CCC([O-])=O)=C2CC([O-])=O)=N5)[C@@](C)(CC([O-])=O)[C@@H]4CCC([O-])=O)=N3 '
               'NAME: precorrin-6X(8-) REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 15 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'BrC1=C(O)C(Br)=CC(=C1)/C=C/C=C/C=C/C=C/C=C/C(=O)N[C@@H]2C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(O[C@@H]2C)=O)CC(C)C)=O)CC(=O)N)CC(=O)N)C(C)C '
               "NAME: Dibromoalterochromide B' REASON: WRONGLY CLASSIFIED "
               'Found a macrocyclic ring of 16 atoms with exactly 4 nitrogen '
               'atoms, consistent with a porphyrin core.\n'
               ' * SMILES: '
               '[H][C@]12CSc3[nH]c4ccccc4c3C[C@]([H])(NC(=O)[C@H](C)NC(=O)[C@]3([H])C[C@H](O)CN3C1=O)C(=O)N[C@@H](C[C@@](C)(O)CO)C(=O)N[C@@H](C)C(=O)N[C@]([H])([C@H](C)O)C(=O)N2 '
               'NAME: phalloidin REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 18 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               '[H][C@]12N=C(C(C)C3=N[C@@](C)(CC4=C(CCC(O)=O)[C@](C)(CC(O)=O)C(/C=C5\\N[C@]1(C)[C@@](C)(CC(O)=O)[C@@H]5CCC(O)=O)=N4)C(C)=C3CCC(O)=O)[C@](C)(CCC(O)=O)[C@H]2CC(O)=O '
               'NAME: precorrin-7 REASON: WRONGLY CLASSIFIED Found a '
               'macrocyclic ring of 15 atoms with exactly 4 nitrogen atoms, '
               'consistent with a porphyrin core.\n'
               ' * SMILES: '
               'CCC1=C(CO)C2=[N+]3C1=Cc1c(C)c4C(=O)[C@H](C(=O)OC)C5=C6[C@@H](CCC([O-])=O)[C@H](C)C7=[N+]6[Mg--]3(n1c45)n1c(=C7)c(C)c(C=C)c1=C2 '
               'NAME: 7(1)-hydroxychlorophyllide a(1-) REASON: WRONGLY '
               'CLASSIFIED Metal atom Mg (atomic num 12) is coordinated to 4 '
               'nitrogen atoms, consistent with a metalloporphyrin core.\n'
               'False negatives: SMILES: '
               'COC(=O)C1C(=O)c2c(C)c3=CC4=N\\C(=C/c5c(C=C)c(C)c6\\C=C7/N=C(C(\\C=C\\C(O)=O)=C/7C)C1=c2n3[Mg]n56)\\C(C)=C4C=C '
               'NAME: chlorophyll c2 REASON: MISSED No macrocyclic ring (15–18 '
               'atoms with exactly 4 nitrogen atoms) found. No metal center '
               'coordinated to exactly 4 nitrogen atoms was detected.\n'
               ' * SMILES: '
               'C1=2N3C(C(=C4N=C(C(=C5N(C(=C(C6=NC(=C1C7=CC=CC=C7)C=C6)C8=CC=CC=C8)C=C5)[Mg]3)C=9C=CC=CC9)C=C4)C=%10C=CC=CC%10)=CC2 '
               'NAME: magnesium tetraphenylporphyrin REASON: MISSED No '
               'macrocyclic ring (15–18 atoms with exactly 4 nitrogen atoms) '
               'found. No metal center coordinated to exactly 4 nitrogen atoms '
               'was detected.\n'
               ' * SMILES: '
               'C=12N3C(=CC4=NC(=CC=5N(C=6C(=C7N=C(C1)[C@H]([C@@H]7CCC(O)=O)C)[C@H](C(C6C5C)=O)C(=O)OC)[Mg]3)C(=C4CO)CC)C(=C2C)C=C '
               'NAME: 7(1)-hydroxychlorophyllide a REASON: MISSED No '
               'macrocyclic ring (15–18 atoms with exactly 4 nitrogen atoms) '
               'found. No metal center coordinated to exactly 4 nitrogen atoms '
               'was detected.\n'
               ' * SMILES: '
               '[H]C(=O)c1c(C=C)c2\\C=C3/N=C(C=c4c(C)c5C(=O)[C@H](C(=O)OC)C6=c5n4[Mg]n2c1\\C=C1/N=C6[C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]1C)C(CC)=C/3C '
               'NAME: chlorophyll f REASON: MISSED No macrocyclic ring (15–18 '
               'atoms with exactly 4 nitrogen atoms) found. No metal center '
               'coordinated to exactly 4 nitrogen atoms was detected.\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3=CC4=N\\C(=C/c5c(C(C)=O)c(C)c6\\C=C7/N=C([C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]7C)C1=c2n3[Mg]n56)[C@H](C)C/4=C/C '
               'NAME: (7R,8Z)-bacteriochlorophyll b REASON: MISSED No '
               'macrocyclic ring (15–18 atoms with exactly 4 nitrogen atoms) '
               'found. No metal center coordinated to exactly 4 nitrogen atoms '
               'was detected.\n'
               ' * SMILES: '
               '[H]C(=O)c1c(C)c2\\C=C3/N=C([C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]3C)C3=c4c(C(=O)[C@@H]3C(=O)OC)c(C)c3=CC5=N\\C(=C/c1n2[Mg]n43)\\C(C)=C5CC '
               'NAME: chlorophyll d REASON: MISSED No macrocyclic ring (15–18 '
               'atoms with exactly 4 nitrogen atoms) found. No metal center '
               'coordinated to exactly 4 nitrogen atoms was detected.\n'
               ' * SMILES: '
               'CCC1=C(C)/C2=C/c3c(C=C)c(C)c4\\C=C5/N=C(C(\\C=C\\C(O)=O)=C/5C)C5=c6c(C(=O)C5C(=O)OC)c(C)c(=CC1=N\\2)n6[Mg]n34 '
               'NAME: chlorophyll c1 REASON: MISSED No macrocyclic ring (15–18 '
               'atoms with exactly 4 nitrogen atoms) found. No metal center '
               'coordinated to exactly 4 nitrogen atoms was detected.\n'
               ' * SMILES: '
               'C1=C2C(=C(C=3N2[Mg]N4C(C=C5N=C(C3)C(=C5CC)CC)=C(C(=C4C=C6N=C1C(=C6CC)CC)CC)CC)CC)CC '
               'NAME: magnesium octaethylporphyrin REASON: MISSED No '
               'macrocyclic ring (15–18 atoms with exactly 4 nitrogen atoms) '
               'found. No metal center coordinated to exactly 4 nitrogen atoms '
               'was detected.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No macrocyclic ring (15–18 '
                                               'atoms with exactly 4 nitrogen '
                                               'atoms and high aromaticity) '
                                               'found. No metal center '
                                               'coordinated to exactly 4 '
                                               'aromatic nitrogen atoms was '
                                               'detected.'}],
    'sample_false_negatives': [   {   'smiles': 'C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\C)=O)C)[Mg-2]735)[C@@H](C(C8=C6C)=O)C(=O)OC)C(=C4C)C=C)=C(C2C)C=C',
                                      'name': "divinylchlorophyll a'",
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'CC1=C(CCC(O)=O)C2=[N]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N]5[Fe]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2',
                                      'name': 'heme b',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'COC(=O)C1C(=O)c2c(C)c3=CC4=N\\C(=C/c5c(C=C)c(C)c6\\C=C7/N=C(C(\\C=C\\C(O)=O)=C/7C)C1=c2n3[Mg]n56)\\C(C)=C4C=C',
                                      'name': 'chlorophyll c2',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'CC1OC(=O)C[C@@]2(C)[C@H](CCC(O)=O)C3=CC4=[N+]5C(=CC6=[N+]7C(=CC8=[N+]9C(=C(CC(O)=O)[C@@]8(C)CCC(O)=O)C12N3[Co--]579)C(CCC(O)=O)=C6CC(O)=O)[C@@H](CCC(O)=O)[C@]4(C)CC(O)=O',
                                      'name': 'cobalt(II)-factor IV',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'C1=2N3C(C(=C4N=C(C(=C5N(C(=C(C6=NC(=C1C7=CC=CC=C7)C=C6)C8=CC=CC=C8)C=C5)[Mg]3)C=9C=CC=CC9)C=C4)C=%10C=CC=CC%10)=CC2',
                                      'name': 'magnesium tetraphenylporphyrin',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'CC1C2=[N+]3C(=Cc4c(C)c(CCC(O)=O)c5C=C6C(CCC(O)=O)=C(C)C7=[N+]6[Fe--]3(n45)n3c(=C2)c(C)c(C)c3=C7)C1(C)C',
                                      'name': 'iron methylchlorin',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'CC1=C(CCC(O)=O)C2=[N]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N]5[Zn]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2',
                                      'name': 'zinc protoporphyrin',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'C=12N3C(=CC4=NC(=CC=5N(C=6C(=C7N=C(C1)[C@H]([C@@H]7CCC(O)=O)C)[C@H](C(C6C5C)=O)C(=O)OC)[Mg]3)C(=C4CO)CC)C(=C2C)C=C',
                                      'name': '7(1)-hydroxychlorophyllide a',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31',
                                      'name': 'chlorophyll a',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'},
                                  {   'smiles': 'C=1C=2C(=C(C=3N2[Pd]45N=6C(=CC=7N4C(C3)=C(C7CC)CC)C(C(C6C=C8N5C1C(=C8CC)CC)=O)(CC)CC)CC)CC',
                                      'name': 'palladium(II) '
                                              'octaethylporphyrinketone',
                                      'reason': 'No macrocyclic ring (15–18 '
                                                'atoms with exactly 4 nitrogen '
                                                'atoms and high aromaticity) '
                                                'found. No metal center '
                                                'coordinated to exactly 4 '
                                                'aromatic nitrogen atoms was '
                                                'detected.'}],
    'attempt': 5,
    'reasoning': 'Below is our revised solution. In our reasoning we noticed '
                 'that the previous heuristics were too permissive. Some '
                 'molecules were “picked up” because they happened to contain '
                 'a 15–18 membered ring with four nitrogens or a metal '
                 'coordinated to four nitrogen atoms even if the overall '
                 'molecular context wasn’t porphyrin‐like. To address this, we '
                 'now add extra filters. For the macrocyclic heuristic we '
                 'require that the candidate ring not only has 15–18 atoms '
                 'with exactly four nitrogen atoms but that most atoms in that '
                 'ring are aromatic (as expected from a conjugated, '
                 'porphyrin‐like core). For the metal heuristic we '
                 'additionally require that the nitrogen neighbors coordinated '
                 'to the metal be aromatic. This extra check helps remove '
                 'false positives while still catching porphyrin variants that '
                 'may have slight deviations in ring size or bonding.\n'
                 '\n'
                 'Below is the complete Python code using RDKit:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 52,
    'num_false_positives': 30,
    'num_true_negatives': 142147,
    'num_false_negatives': 71,
    'num_negatives': None,
    'precision': 0.6341463414634146,
    'recall': 0.42276422764227645,
    'f1': 0.5073170731707317,
    'accuracy': 0.9992902319044272,
    'negative_predictive_value': 0.9995007664290033}