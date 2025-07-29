"""
Classifies: CHEBI:73754 thiosugar
"""
#!/usr/bin/env python
"""
Classifies: Thiosugar

A thiosugar is defined as a carbohydrate derivative in which one or more of the oxygens 
or hydroxy groups of the parent carbohydrate is replaced by sulfur or –SR.

This improved algorithm uses explicit hydrogens to confirm that oxygen substituents are 
actually hydroxyl groups. For cyclic candidates (5- or 6-membered rings) it requires a 
typical sugar ring pattern (saturated, with exactly one intrinsic heteroatom and at least 
three external –OH substituents). If the intrinsic heteroatom is S or if one of the ring 
carbons bears a simple S substituent, the molecule is classified as a thiosugar.

If no sugar ring is found, then an open‐chain search is performed on contiguous chains of 
exactly 5 or 6 carbons (typical for linear carbohydrates). Such chains must display at least 
three hydroxyl (–OH attached) substituents, at least one S substituent, and only few other 
(“nonsugar”) substituents.
"""

from rdkit import Chem
from rdkit.Chem import rdchem

def is_thiosugar(smiles: str):
    """
    Determines if a molecule is a thiosugar based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if the molecule is classified as a thiosugar, False otherwise.
        str: Reason for the classification.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    # Add explicit hydrogens for better analysis of hydroxyl groups.
    mol = Chem.AddHs(mol)
    
    ring_info = mol.GetRingInfo()
    sugar_candidate_found = False
    
    # First, check for cyclic (ring) sugar candidates.
    for ring in ring_info.AtomRings():
        if len(ring) not in (5, 6):
            continue
        # Get atoms in the ring.
        atoms_in_ring = [mol.GetAtomWithIdx(i) for i in ring]
        # Discard aromatic rings.
        if any(atom.GetIsAromatic() for atom in atoms_in_ring):
            continue
        # Require that all atoms are sp3-hybridized.
        if any(atom.GetHybridization() != rdchem.HybridizationType.SP3 for atom in atoms_in_ring):
            continue
        
        # Count intrinsic heteroatoms in the ring (non-carbon and non-hydrogen).
        hetero_atoms = [atom for atom in atoms_in_ring if atom.GetAtomicNum() not in (6, 1)]
        if len(hetero_atoms) != 1:
            continue
        
        # Count external hydroxyl substituents on ring atoms.
        hydroxyl_count = 0
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring:
                    continue
                # Only count oxygen as -OH if it is single‐bonded and bears an explicit hydrogen.
                if nbr.GetSymbol() == "O":
                    if any(n.GetSymbol() == "H" for n in nbr.GetNeighbors()):
                        hydroxyl_count += 1
        # Require at least three hydroxyl substituents.
        if hydroxyl_count < 3:
            continue
        
        # We now have a good sugar ring candidate.
        sugar_candidate_found = True
        
        # CASE A: The intrinsic heteroatom is sulfur.
        hetero_atom = hetero_atoms[0]
        if hetero_atom.GetSymbol() == "S":
            return True, "Sugar ring has sulfur replacing the intrinsic ring oxygen"
        
        # CASE B: Check if a ring carbon bears a simple S substituent.
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6:  # only consider carbons
                continue
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring:
                    continue
                if nbr.GetSymbol() == "S":
                    # A simple S substituent should not be heavily decorated:
                    heavy_neighbors = [n for n in nbr.GetNeighbors() if n.GetAtomicNum() > 1 and n.GetIdx() != atom.GetIdx()]
                    if len(heavy_neighbors) <= 1:
                        return True, "Sugar ring has thio substitution at a hydroxyl-bearing carbon"
                    # Even if there is more substitution, we may consider sugar decoration.
                    # (More checks could be added here if needed.)
                    return True, "Sugar ring has thio substitution at a hydroxyl-bearing carbon"
        # No S substitution found in this ring candidate.
    
    # Next, search for open-chain sugar candidates only if no ring has returned a positive.
    # Look for a contiguous chain of exactly 5 or 6 sp3 carbons (non‐cyclic) that have predominantly
    # hydroxyl substituents and at least one S substituent.
    atoms = mol.GetAtoms()
    for atom in atoms:
        if atom.GetAtomicNum() != 6:
            continue
        if atom.IsInRing():
            continue
        chain = []
        visited = set()
        # Perform a simple Depth First Search to collect contiguous (non‐ring) carbons.
        def dfs(a):
            if a.GetAtomicNum() == 6 and (not a.IsInRing()):
                chain.append(a.GetIdx())
                visited.add(a.GetIdx())
                for nbr in a.GetNeighbors():
                    if nbr.GetAtomicNum() == 6 and nbr.GetIdx() not in visited and (not nbr.IsInRing()):
                        dfs(nbr)
        dfs(atom)
        if len(chain) not in (5, 6):
            continue
        hydroxyl_count = 0
        sulfur_count = 0
        extra_substituents = 0  # substituents that are neither -OH (from oxygen) nor sulfur.
        for idx in chain:
            a = mol.GetAtomWithIdx(idx)
            for nbr in a.GetNeighbors():
                if nbr.GetIdx() in chain:
                    continue
                symbol = nbr.GetSymbol()
                if symbol == "O":
                    # Check for a bonded H.
                    if any(n.GetSymbol() == "H" for n in nbr.GetNeighbors()):
                        hydroxyl_count += 1
                elif symbol == "S":
                    sulfur_count += 1
                elif nbr.GetAtomicNum() > 1:
                    extra_substituents += 1
        # Avoid chains decorated with many non-sugar substituents.
        if extra_substituents > len(chain):
            continue
        if hydroxyl_count >= 3 and sulfur_count >= 1:
            return True, "Open-chain carbohydrate derivative with thio substitution"
    
    # If a sugar-like candidate was found but no thio substitution evidence was detected.
    if sugar_candidate_found:
        return False, "Sugar-like patterns detected but no clear thio substitution found"
    else:
        return False, "No sugar-like pattern detected"

# For testing (uncomment below if running as a script):
# if __name__ == '__main__':
#     test_examples = {
#         "butylglucosinolic acid": "[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCC",
#         "celesticetin": "COC(C)C(NC(=O)[C@@H]1CCCN1C)[C@H]2O[C@H](SCCOC(=O)C3=CC=CC=C3O)[C@H](O)[C@@H](O)[C@H]2O",
#         "non-thiosugar control": "CC(=O)OC1=CC=CC=C1C(=O)O"  # example of a non-sugar molecule
#     }
#     for name, smi in test_examples.items():
#         flag, reason = is_thiosugar(smi)
#         print(f"{name}: {flag} ({reason})")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:73754',
                          'name': 'thiosugar',
                          'definition': 'A carbohydrate derivative in which '
                                        'one or more of the oxygens or hydroxy '
                                        'groups of the parent carbohydrate is '
                                        'replaced by sulfur or -SR, where R '
                                        'can be hydrogen or any group.',
                          'parents': ['CHEBI:33261', 'CHEBI:63299'],
                          'xrefs': ['PMID:16240117', 'PMID:23330717'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 118,
                           'log_lines_of_code': 4.770684624465665,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 5,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem'],
                           'imports_count': 2,
                           'methods_called': [   'GetHybridization',
                                                 'append',
                                                 'GetIsAromatic',
                                                 'add',
                                                 'AtomRings',
                                                 'GetSymbol',
                                                 'AddHs',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'GetNeighbors',
                                                 'GetAtomicNum',
                                                 'IsInRing',
                                                 'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'GetIdx'],
                           'methods_called_count': 15,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_thiosugar(smiles: str):', 'dfs(a):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Sugar ring has sulfur '
                                          'replacing the intrinsic ring '
                                          'oxygen"',
                                          'True, "Sugar ring has thio '
                                          'substitution at a hydroxyl-bearing '
                                          'carbon"',
                                          'True, "Sugar ring has thio '
                                          'substitution at a hydroxyl-bearing '
                                          'carbon"',
                                          'True, "Open-chain carbohydrate '
                                          'derivative with thio substitution"',
                                          'False, "Sugar-like patterns '
                                          'detected but no clear thio '
                                          'substitution found"',
                                          'False, "No sugar-like pattern '
                                          'detected"'],
                           'returns_count': 7,
                           'complexity': 6.954136924893133},
    'message': '\n'
               'Attempt failed: F1 score of 0.05091725945338825 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCC '
               'NAME: butylglucosinolic acid REASON: CORRECT Sugar ring has '
               'thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'COC(C)C(NC(=O)[C@@H]1CCCN1C)[C@H]2O[C@H](SCCOC(=O)C3=CC=CC=C3O)[C@H](O)[C@@H](O)[C@H]2O '
               'NAME: celesticetin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'O1[C@@H]([C@H]([C@@H]([C@H]([C@@H]1SC(CCCCCCCS(C)=O)=NOS(O)(=O)=O)O)O)O)CO '
               'NAME: glucoibarin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/C '
               'NAME: glucocapparin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCCCSC '
               'NAME: glucoberteroin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: CSCC(=O)[C@H](O)[C@H](O)COP(O)(O)=O NAME: '
               '1-(methylthio)ribulose 5-phosphate REASON: CORRECT Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'S(C1OC(C(OC(=O)C)C(OC(=O)C)C1N2C(=O)C=3C(C2=O)=CC=CC3)COC(=O)C)C '
               'NAME: Methyl '
               '3,4,6-tri-O-acetyl-2-deoxy-2-(1,3-dioxo-1,3-dihydro-2H-isoindol-2-yl)-1-thiohexopyranoside '
               'REASON: CORRECT Sugar ring has thio substitution at a '
               'hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCCCS(C)=O '
               'NAME: glucoalyssin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CC '
               'NAME: glucolepidiin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'COn1cc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS(O)(=O)=O)c2ccccc12 '
               'NAME: neoglucobrassicin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(SC(=NO)CC=2C3=CC=CC=C3NC2)[C@H](O)[C@H]([C@@H]([C@H](O1)CO)O)O '
               'NAME: indolylmethyl desulfoglucosinolate REASON: CORRECT Sugar '
               'ring has thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\S(O)(=O)=O)/CCC=CS(=O)C '
               'NAME: glucoraphenin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'CCCO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: propyl '
               'beta-D-mannopyranosyl-(1->2)-beta-D-mannopyranosyl-(1->2)-2-thio-beta-D-mannopyranoside '
               'REASON: CORRECT Sugar ring has thio substitution at a '
               'hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NO)CCC=C NAME: '
               '3-butenyldesulfoglucosinolate REASON: CORRECT Sugar ring has '
               'thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)/C(=N\\O)/CCCCCCCCSC '
               'NAME: Deoxydesulfoglucohirsutin REASON: CORRECT Sugar ring has '
               'thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)COC(\\C=C\\C2=CC(=C(C(=C2)OC)O)OC)=O)S/C(=N\\S(O)(=O)=O)/CCC=CS(=O)C '
               'NAME: 6-sinapoylglucoraphenin REASON: CORRECT Sugar ring has '
               'thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)CCCCCCCC NAME: '
               'n-Octyl-beta-D-thioglucopyranoside REASON: CORRECT Sugar ring '
               'has thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCCCCCCS(C)=O '
               'NAME: Glucohirsutin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(C)C '
               'NAME: Isopropyl 1-thio-beta-D-glucopyranoside REASON: CORRECT '
               'Sugar ring has thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NO)CC=2C=CC=CC2 '
               'NAME: desulfoglucotropeolin REASON: CORRECT Sugar ring has '
               'thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'C[C@@H](O)[C@@H]([NH3+])[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@@H](SC=2NC=C(C[C@@H](C(=O)[O-])[N+](C)(C)C)N2)O1 '
               'NAME: ergothioneyl-alpha-D-lincosamide(+1) REASON: CORRECT '
               'Sugar ring has thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\O)/CC=2C=CC=CC2 '
               'NAME: (Z)-desulfoglucotropeolin REASON: CORRECT Sugar ring has '
               'thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS(O)(=O)=O)/CCCCSC '
               'NAME: glucoerucin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: [C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CS)O)O)O)O '
               'NAME: 6-thio-beta-D-galactose REASON: CORRECT Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'CCC[C@@H]1C[C@H](N(C)C1)C(=O)N[C@H]([C@@H](C)O)[C@H]1O[C@H](SC)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: lincomycin REASON: CORRECT Sugar ring has thio '
               'substitution at a hydroxyl-bearing carbon\n'
               'False positives: SMILES: '
               'S(C1=C(N2C(=O)[C@@H]([C@H]2C1)[C@@H](O)C)C(=O)O)CCN NAME: '
               '8-epi-thienamycin REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'C[C@@H](CC([O-])=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (2S)-methylsuccinyl-CoA(5-) REASON: WRONGLY CLASSIFIED '
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (9Z,12Z,15Z,18Z)-3-oxotetracosatetraenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Open-chain carbohydrate derivative '
               'with thio substitution\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@@H](CC)O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (R)-2-hydroxybutanoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC[C@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (S)-3-hydroxyhexacosanoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[C@H]1(O)[C@@H](OC[C@@H](CO)O)O[C@H](CS([O-])(=O)=O)[C@H]([C@@H]1O)O '
               'NAME: 3-(alpha-D-6-sulfoquinovosyl)-sn-glycerol(1-) REASON: '
               'WRONGLY CLASSIFIED Open-chain carbohydrate derivative with '
               'thio substitution\n'
               ' * SMILES: '
               'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCCCCC=C NAME: '
               '6-Heptenyl glucosinolate REASON: WRONGLY CLASSIFIED Sugar ring '
               'has thio substitution at a hydroxyl-bearing carbon\n'
               ' * SMILES: '
               'CCCCCCCC(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-hydroxydecanoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-hydroxytetracosanoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Open-chain carbohydrate derivative with thio '
               'substitution\n'
               ' * SMILES: '
               'N[C@@H](CS[C@H](\\C=C\\C=C\\C=C/C=C/CC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O '
               'NAME: '
               '(13E)-16-carboxy-Delta(13)-17,18,19,20-tetranor-leukotriene E4 '
               'REASON: WRONGLY CLASSIFIED Open-chain carbohydrate derivative '
               'with thio substitution\n'
               ' * SMILES: '
               'CCOC(=O)OC(C)OC(=O)[C@H]1C(S[C@@H]2N1C(=O)[C@H]2NC(=O)[C@@H](C3=CC=CC=C3)N)(C)C '
               'NAME: 1-ethoxycarbonyloxyethyl '
               '(2S,5S,6R)-6-[[(2R)-2-amino-2-phenylacetyl]amino]-3,3-dimethyl-7-oxo-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylate '
               'REASON: WRONGLY CLASSIFIED Open-chain carbohydrate derivative '
               'with thio substitution\n'
               ' * SMILES: '
               'C([C@H](CC(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O)=O)O)C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: '
               '(3R,6Z,9Z,12Z,15Z,18Z,21Z)-3-hydroxytetracosahexaenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Open-chain carbohydrate derivative '
               'with thio substitution\n'
               ' * SMILES: '
               'S(CC1=C(N2[C@](SC1)([C@@](C2=O)(NC(CN3C=C(C(C(=C3)Cl)=O)Cl)=O)[H])[H])C(=O)O)C=4SC(=NN4)C '
               'NAME: cefazedone REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[Na+].[H][C@]12SCC=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\c1csc(N)n1)C([O-])=O '
               'NAME: ceftizoxime sodium REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCCCC(O)=O '
               'NAME: 3-oxohexadecanedioyl-CoA REASON: WRONGLY CLASSIFIED '
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[Na+].[H]C(=O)O[C@@H](C(=O)N[C@@H]1C(=O)N2C(C([O-])=O)=C(CSc3nnnn3C)CS[C@]12[H])c1ccccc1 '
               'NAME: cefamandole nafate REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[H][C@]12SCC(C[N+]3(C)CCCC3)=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\c1csc(N)n1)C([O-])=O '
               'NAME: cefepime REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[H]C(=O)c1ccc2oc3cc(=O)c(N)c(SC[C@H](NC(C)=O)C(O)=O)c3nc2c1 '
               'NAME: grixazone A REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC=3NC=NC3)C(O)=O)C '
               'NAME: Trp-His-Met REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: C1=COC(=C1)CSCCNC(=O)NC2=CC(=CC(=C2)Cl)Cl NAME: '
               '1-(3,5-dichlorophenyl)-3-[2-(2-furanylmethylthio)ethyl]urea '
               'REASON: WRONGLY CLASSIFIED Open-chain carbohydrate derivative '
               'with thio substitution\n'
               ' * SMILES: '
               'C(C(OCC(CCCC)CC)=O)(CC(OCC(CCCC)CC)=O)S(=O)(=O)[O-].[Na+] '
               'NAME: sodium docusate REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C(CCCCCCCCCCCCCCCCCCCCCCCC)O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 2-hydroxyhexacosanoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               '[S+](CC1OC(N2C3=NC=NC(N)=C3N=C2)C(O)C1O)(CCC(N)C(O)=O)C NAME: '
               "S-(5'-Adenosyl)-L-methionine (SAM) REASON: WRONGLY CLASSIFIED "
               'Open-chain carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC(=O)N)C(O)=O)C '
               'NAME: Arg-Asn-Met REASON: WRONGLY CLASSIFIED Open-chain '
               'carbohydrate derivative with thio substitution\n'
               ' * SMILES: '
               'C[S+](CCC(=O)C(O)=O)C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               'NAME: S-adenosyl-4-methylthio-2-oxobutanoic acid REASON: '
               'WRONGLY CLASSIFIED Open-chain carbohydrate derivative with '
               'thio substitution\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No sugar-like pattern '
                                               'detected'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No sugar-like pattern '
                                               'detected'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No sugar-like pattern '
                                               'detected'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Sugar-like patterns detected '
                                               'but no clear thio substitution '
                                               'found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Sugar-like patterns detected '
                                               'but no clear thio substitution '
                                               'found'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Sugar-like patterns detected '
                                               'but no clear thio substitution '
                                               'found'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No sugar-like pattern '
                                               'detected'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No sugar-like pattern '
                                               'detected'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No sugar-like pattern '
                                               'detected'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Sugar-like patterns detected '
                                               'but no clear thio substitution '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CSCC(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                      'name': '1-(methylthio)ribulose '
                                              '5-phosphate',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': 'S(C1OC(C(OC(=O)C)C(OC(=O)C)C1N2C(=O)C=3C(C2=O)=CC=CC3)COC(=O)C)C',
                                      'name': 'Methyl '
                                              '3,4,6-tri-O-acetyl-2-deoxy-2-(1,3-dioxo-1,3-dihydro-2H-isoindol-2-yl)-1-thiohexopyranoside',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': 'CCCO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O',
                                      'name': 'propyl '
                                              'beta-D-mannopyranosyl-(1->2)-beta-D-mannopyranosyl-(1->2)-2-thio-beta-D-mannopyranoside',
                                      'reason': 'Sugar-like patterns detected '
                                                'but no clear thio '
                                                'substitution found'},
                                  {   'smiles': '[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CS)O)O)O)O',
                                      'name': '6-thio-beta-D-galactose',
                                      'reason': 'Sugar-like patterns detected '
                                                'but no clear thio '
                                                'substitution found'},
                                  {   'smiles': 'S([C@H]1O[C@H](CN2C=3N=CNC(C3N=C2)=O)[C@H]([C@H]1O)O)C',
                                      'name': '9-[[(2R,3S,4R,5R)-3,4-dihydroxy-5-methylsulanyloxolan-2-yl]methyl]-1H-purin-6-one',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': 'ClC(C(NC(=O)C1N(CC(C1)CCC)C)C2OC(SC)C(OP(=O)(O)O)C(C2O)O)C',
                                      'name': 'Clindamycin 2-Phosphate',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': '[C@](NC(=O)[C@@H]1C[C@H](CN1C)CCC)([C@H](C)Cl)([C@]2(O[C@H](SC)[C@@H]([C@H]([C@H]2O)O)OC(CCCCCCCCCCCCCCC)=O)[H])[H]',
                                      'name': 'clindamycin palmitate',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': '[C@@]1([C@@H]([C@@H]([C@H]([C@H](O1)SC)OC(CCCCCCCCCCCCCCC)=O)O)O)([C@](NC([C@H]2N(C[C@@H](C2)CCC)C)=O)([C@@H](Cl)C)[H])[H].Cl',
                                      'name': 'Clindamycin palmitate '
                                              'hydrochloride',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': 'CC[P+](CC)(CC)[Au-]S[C@@H]1O[C@H](COC(C)=O)[C@@H](OC(C)=O)[C@H](OC(C)=O)[C@H]1OC(C)=O',
                                      'name': 'auranofin',
                                      'reason': 'No sugar-like pattern '
                                                'detected'},
                                  {   'smiles': 'Nc1ccc(S[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)cc1',
                                      'name': 'beta-D-Galp-(1->4)-beta-D-Glcp-SC6H4-p-NH2',
                                      'reason': 'Sugar-like patterns detected '
                                                'but no clear thio '
                                                'substitution found'}],
    'attempt': 5,
    'reasoning': 'Below is our revised solution. In our reasoning we noticed '
                 'that the original code was a bit too permissive. In '
                 'particular, open‐chain searches were matching long carbon '
                 'frameworks with a few oxygen and sulfur substituents that '
                 'are not really sugars. In our new version we first add '
                 'explicit hydrogens so that we can check that external atoms '
                 'truly behave like –OH groups. We then require that any '
                 'cyclic (ring) candidate be 5–6 members, saturated and '
                 'non‐aromatic, have exactly one non–C (non–H) atom in the '
                 'ring, and display at least three proper hydroxyl '
                 'substituents. For open‐chain candidates we insist on a '
                 'contiguous chain of exactly 5–6 carbons that are not in '
                 'rings – with at least three hydroxyl groups and at least one '
                 'S substituent, and few extra non‐sugar substituents. We hope '
                 'these more stringent criteria reduce the false positive rate '
                 'while still retaining all the true positives.\n'
                 '\n'
                 'Below is the complete Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 58,
    'num_false_positives': 78,
    'num_true_negatives': 142154,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.4264705882352941,
    'recall': 0.8529411764705882,
    'f1': 0.5686274509803922,
    'accuracy': 0.9993815881939564,
    'negative_predictive_value': 0.9999296587040319}