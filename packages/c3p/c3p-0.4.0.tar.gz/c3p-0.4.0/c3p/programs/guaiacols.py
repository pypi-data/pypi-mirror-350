"""
Classifies: CHEBI:134251 guaiacols
"""
#!/usr/bin/env python
"""
Classifies: guaiacols
Definition: Any phenol carrying an additional methoxy substituent at the ortho-position.
We require that a benzene ring (six-membered aromatic ring) has:
  - a phenolic –OH group (an oxygen attached to the ring with exactly one hydrogen) on one carbon, and
  - at least one adjacent (ortho) ring carbon carrying a methoxy (-OCH3) substituent.
  
This improved version restricts analysis to rings where every atom is an aromatic carbon.
"""

from rdkit import Chem

def is_guaiacols(smiles: str):
    """
    Determines if a molecule is classified as a guaiacol (a phenol with an additional methoxy
    substituent at an ortho-position) based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a guaiacol, False otherwise.
        str: Explanation for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    try:
        # Add explicit hydrogens so that –OH and –OCH3 details (including hydrogen counts) are explicit.
        mol = Chem.AddHs(mol)
        Chem.SanitizeMol(mol)
    except Exception as e:
        return False, f"Error during molecule sanitization: {e}"
    
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    
    # Iterate only over six-membered rings that are strictly benzene: all atoms are aromatic carbons.
    for ring in rings:
        if len(ring) != 6:
            continue  # we only consider six-membered rings
        # Check that every atom in the ring is a carbon and is aromatic.
        if not all(mol.GetAtomWithIdx(idx).GetSymbol() == "C" and mol.GetAtomWithIdx(idx).GetIsAromatic() 
                   for idx in ring):
            continue
        
        # For each ring atom, record if it carries a phenolic –OH or a methoxy group.
        # We will use dictionaries with keys as atom indices in the ring.
        has_OH = {}
        has_OMe = {}
        
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            oh_found = False
            ome_found = False
            # Examine each substituent (neighbor not in the ring)
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring:
                    continue
                # Case 1: Look for a hydroxyl (–OH) group.
                if nbr.GetAtomicNum() == 8:  # oxygen neighbor
                    # Count hydrogens attached to this oxygen.
                    h_neighbors = [n for n in nbr.GetNeighbors() if n.GetAtomicNum() == 1]
                    # For a phenolic OH we expect exactly one hydrogen.
                    if len(h_neighbors) == 1:
                        # Also check that, aside from the ring carbon, there is no other heavy atom attached.
                        heavy_neighbors = [n for n in nbr.GetNeighbors() if n.GetAtomicNum() != 1 and n.GetIdx() not in ring]
                        if len(heavy_neighbors) == 0:
                            oh_found = True
                # Case 2: Look for a methoxy group (-OCH3).
                if nbr.GetAtomicNum() == 8:
                    # For a methoxy group we require that this oxygen has exactly 2 neighbors: 
                    # one is the ring atom and the other should be a CH3.
                    if nbr.GetDegree() == 2:
                        other = None
                        for sub in nbr.GetNeighbors():
                            if sub.GetIdx() not in ring:
                                other = sub
                        if other is not None and other.GetAtomicNum() == 6:
                            # Check that the carbon is sp3 and has exactly 3 hydrogens.
                            if other.GetHybridization() == Chem.rdchem.HybridizationType.SP3:
                                h_on_c = [n for n in other.GetNeighbors() if n.GetAtomicNum() == 1]
                                if len(h_on_c) == 3:
                                    ome_found = True
            has_OH[idx] = oh_found
            has_OMe[idx] = ome_found
            
        # Now, for each ring atom that has an –OH, check that one of its ortho (adjacent within the ring) atoms 
        # has a methoxy substituent.
        for idx in ring:
            if not has_OH.get(idx, False):
                continue
            # Get the ring atom object.
            atom = mol.GetAtomWithIdx(idx)
            # Look for adjacent ring atoms (ortho positions) where has_OMe is True.
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring and has_OMe.get(nbr.GetIdx(), False):
                    return True, "Found benzene ring with a phenolic OH and an ortho methoxy group"
                    
    return False, "No benzene ring with ortho -OH and -OCH3 substituents found"
    
# Example usage (uncomment to test):
# test_smiles = [
#     "COc1ccc(O)cc1",  # 2-methoxyphenol (guaiacol): should return True
#     "c1cc(O)ccc1"     # phenol: should return False
# ]
# for s in test_smiles:
#     result, reason = is_guaiacols(s)
#     print(f"SMILES: {s}\nClassification: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134251',
                          'name': 'guaiacols',
                          'definition': 'Any phenol carrying an additional '
                                        'methoxy substituent at the '
                                        'ortho-position.',
                          'parents': ['CHEBI:25235', 'CHEBI:33853'],
                          'xrefs': ['MetaCyc:Guaiacols'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 79,
                           'log_lines_of_code': 4.3694478524670215,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
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
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 7,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 8,
                                                 6,
                                                 7,
                                                 7,
                                                 8,
                                                 8,
                                                 9,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 1,
                                                 1],
                           'max_indent': 9,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetDegree',
                                                 'GetHybridization',
                                                 'GetIsAromatic',
                                                 'MolFromSmiles',
                                                 'SanitizeMol',
                                                 'GetNeighbors',
                                                 'AddHs',
                                                 'GetRingInfo',
                                                 'GetSymbol',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'get',
                                                 'GetAtomicNum',
                                                 'AtomRings'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_guaiacols(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Error during molecule '
                                          'sanitization: {e}"',
                                          'True, "Found benzene ring with a '
                                          'phenolic OH and an ortho methoxy '
                                          'group"',
                                          'False, "No benzene ring with ortho '
                                          '-OH and -OCH3 substituents found"'],
                           'returns_count': 4,
                           'complexity': 6.473889570493403},
    'message': '\n'
               'Attempt failed: F1 score of 0.05443548387096774 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C=12O[C@@H]([C@H](C1C=C(C=C2OC)/C=C/CO)CO)C3=CC(=C(C=C3)O)OC '
               'NAME: (+)-dehydrodiconiferyl alcohol REASON: CORRECT Found '
               'benzene ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: CCCCc1ccc(CCNC(=O)\\C=C\\c2ccc(O)c(OC)c2)cc1 NAME: '
               'Cuscuta propenamide 2 REASON: CORRECT Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(ccc1O)[C@H]1O[C@@H](O)[C@H]2[C@H]1CO[C@H]2c1ccc(O)c(OC)c1 '
               'NAME: 4alpha-hydroxypinoresinol REASON: CORRECT Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(C[C@H]2CO[C@@H]([C@H]2CO)c2ccc(O)c(O)c2)ccc1O NAME: '
               'taxiresinol REASON: CORRECT Found benzene ring with a phenolic '
               'OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(ccc1O)[C@@H](O)[C@@H]1CO[C@@H]([C@H]1CO)c1ccc(O)c(OC)c1 '
               'NAME: tanegool REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'C1=C(C=C2C(=C1OC)O[C@H]([C@@H]2C=O)C3=CC=C(C(=C3)OC)O)/C=C/C(O)=O '
               'NAME: (-)-DCA-CL REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cccc(C\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)c1O '
               'NAME: 2-methoxy-6-(all-trans-nonaprenyl)phenol REASON: CORRECT '
               'Found benzene ring with a phenolic OH and an ortho methoxy '
               'group\n'
               ' * SMILES: COc1cc(\\C=C\\C(=O)c2c(O)cc(O)cc2O)ccc1O NAME: '
               'homoeriodictyol chalcone REASON: CORRECT Found benzene ring '
               'with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'C1=C(C=C2C(=C1OC)O[C@@H]([C@H]2C=O)C3=CC=C(C(=C3)OC)O)/C=C/C(O)=O '
               'NAME: (+)-DCA-CL REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               '[H][C@]12CO[C@H](c3ccc(O)c(OC)c3)[C@@]1([H])CO[C@@H]2c1ccc(O)c(OC)c1 '
               'NAME: (+)-pinoresinol REASON: CORRECT Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1cc(C[C@H](C)[C@H](C)Cc2ccc(O)cc2)ccc1O NAME: '
               "(+)-(8S,8'R)-4,4'-dihydroxy-3-methoxylignan REASON: CORRECT "
               'Found benzene ring with a phenolic OH and an ortho methoxy '
               'group\n'
               ' * SMILES: '
               'COc1cc2C[C@H](C)[C@H](C)[C@@H](c3cc(O)c(O)c(OC)c3)c2cc1O NAME: '
               "(+)-(7'S,8S,8'S)-3',4,4'-trihydroxy-5,5'-dimethoxy-2,7'-cyclolignan "
               'REASON: CORRECT Found benzene ring with a phenolic OH and an '
               'ortho methoxy group\n'
               ' * SMILES: COc1cc(ccc1O)C(O)C(CO)c1ccc(O)c(OC)c1 NAME: '
               '1,2-diguaiacylpropane-1,3-diol REASON: CORRECT Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(ccc1O)[C@H]1OC[C@@H]([C@@H]1CO)C(=O)c1ccc(O)c(OC)c1 '
               'NAME: vladinol D REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1ccc(CCNC(=O)\\C=C\\c2ccc(O)c(OC)c2)cc1O NAME: '
               "N-trans-feruloyl-4'-O-methyldopamine REASON: CORRECT Found "
               'benzene ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1cc(ccc1O)[C@H](O)[C@@H](O)CO NAME: '
               '(+)-(7S,8S)-guaiacylglycerol REASON: CORRECT Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O1[C@@H]([C@@]2([C@](C1)(C(OC2)=O)[H])[H])C3=CC(OC)=C(O)C=C3 '
               'NAME: salicifoliol REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(ccc1O)[C@H]1O[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]2[C@@H]1CO[C@H]2c1ccc(O)c(OC)c1 '
               'NAME: 4beta-[(beta-D-glucopyranosyl)hydroxy]-pinoresinol '
               'REASON: CORRECT Found benzene ring with a phenolic OH and an '
               'ortho methoxy group\n'
               ' * SMILES: COC(=O)\\C=C\\c1ccc(O)c(OC)c1 NAME: '
               'trans-methylferulate REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(CNC(=O)CCCCCCC(C)C)cc(c1O)-c1cc(CNC(=O)CCCC\\C=C\\C(C)C)cc(OC)c1O '
               "NAME: 6'',7''-dihydro-5',5'''-dicapsaicin REASON: CORRECT "
               'Found benzene ring with a phenolic OH and an ortho methoxy '
               'group\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3([C@]([C@]4([C@@](CC3)(CC[C@](C4)(C(=O)O)C)C)[H])(CC[C@]2(C=5C1=C(C(OC)=C(O)C5)CO)C)C)C '
               'NAME: triptohypol A REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1cc(ccc1O)[C@@H](O)[C@@H](O)CO NAME: '
               '(-)-(7R,8S)-guaiacylglycerol REASON: CORRECT Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1cc(cc(O)c1O)C(=O)Cc1cccc(O)c1C(O)=O NAME: '
               '2-hydroxy-6-[2-(3,4-dihydroxyphenyl-5-methoxy)-2-oxoethyl]benzoic '
               'acid REASON: CORRECT Found benzene ring with a phenolic OH and '
               'an ortho methoxy group\n'
               ' * SMILES: COC1=C(O)C(=CC(=C1)[N+]([O-])=O)[N+]([O-])=O NAME: '
               '4,6-dinitroguaiacol REASON: CORRECT Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cccc(C\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)c1O '
               'NAME: 2-decaprenyl-6-methoxyphenol REASON: CORRECT Found '
               'benzene ring with a phenolic OH and an ortho methoxy group\n'
               'False positives: SMILES: '
               'O(C1=C(O)C(C\\C=C(\\CCC=C(C)C)/C)=C(C(O)=C1OC)C)C NAME: '
               'ubiquinol-2 REASON: WRONGLY CLASSIFIED Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: O([C@@H]1C2=C(O)C=CC=C2[C@H](O)C[C@@H]1O)C NAME: '
               'Xylariol B REASON: WRONGLY CLASSIFIED Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(ccc1O)-c1[o+]c2cc(O)cc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)c2cc1O[C@@H]1O[C@H](COC(=O)\\C=C\\c2ccc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3OC(=O)\\C=C\\c3ccc(O)c(O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)c3)c(O)c2)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1OC(=O)\\C=C\\c1ccc(O)c(O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)c1 '
               'NAME: Heavenly blue anthocyanin REASON: WRONGLY CLASSIFIED '
               'Found benzene ring with a phenolic OH and an ortho methoxy '
               'group\n'
               ' * SMILES: C=1C(=CC=C(C1OC)O)CNC(CCCC/C=C\\C(C)C)=O NAME: '
               'zucapsaicin REASON: WRONGLY CLASSIFIED Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1ccc2CCC(=O)CCCCc3ccc(Oc1c2)c(OC)c3O NAME: '
               'juglanin A REASON: WRONGLY CLASSIFIED Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C(C=3C(=O)C=4C(OC3)=CC(O)=C(OC)C4)=CC(O)=C(OC)C2)CO '
               'NAME: Licoagroside A REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=C3OC(=CC(=O)C3=C(O)C(O)=C2O)C4=CC(OC)=C(O)C=C4)C '
               'NAME: Estragonoside REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1ccc2C[C@H]3[C@H]4C[C@]5([C@H]6Oc1c2[C@@]46CCN3C)N1CCc2ccc(OC)c3Oc4c(O)c(OC)ccc4C(C5=O)=C1c23 '
               'NAME: Cancentrine REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](CC2=CC(OC)=C(O)C=C2)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC3=CC=CC=C3)C)/C)=O)C)CCCN=C(N)N)C '
               'NAME: MC-RY(OMe) REASON: WRONGLY CLASSIFIED Found benzene ring '
               'with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(cc(O)c1O)-c1[o+]c2cc(O)cc(O)c2cc1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: petunidin 3-O-beta-D-glucoside REASON: WRONGLY '
               'CLASSIFIED Found benzene ring with a phenolic OH and an ortho '
               'methoxy group\n'
               ' * SMILES: '
               'CO[C@@H]1[C@@H](O)[C@@H]2[C@]3(C)[C@@H](C[C@H]4OC(=O)C[C@@](O)([C@]1(C)O)[C@@]24C)[C@H](C)C=C(OC)C3=O '
               'NAME: Nigakilactone H REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: [Cl-].COc1cc(ccc1O)-c1[o+]c2cc(O)cc(O)c2cc1O NAME: '
               'peonidin chloride REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COc1ccc(cc1)-c1coc2cc(O)c(OC)c(O)c2c1=O NAME: '
               'Irisolidone REASON: WRONGLY CLASSIFIED Found benzene ring with '
               'a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O(CC1C(C(C=2C(C1)=CC(OC)=C(O)C2)C3=CC(OC)=C(O)C=C3)CO)C4OC(C(O)C(O)C4O)CO '
               'NAME: Isolariciresinol 9-O-beta-D-glucoside REASON: WRONGLY '
               'CLASSIFIED Found benzene ring with a phenolic OH and an ortho '
               'methoxy group\n'
               ' * SMILES: O1C=2C(C(=O)C=3C1=CC(O)=C(OC)C3)=C(OC)C(OC)=C(OC)C2 '
               'NAME: 6-Hydroxy-1,2,3,7-tetramethoxy-9H-xanthen-9-one REASON: '
               'WRONGLY CLASSIFIED Found benzene ring with a phenolic OH and '
               'an ortho methoxy group\n'
               ' * SMILES: '
               'O1C=2C(C(=O)C(O)=C1C3=CC(OC)=C(OC)C=C3)=C(O)C(O)=C(OC)C2 NAME: '
               "3,5,6-Trihydroxy-3',4',7-trimethoxyflavone REASON: WRONGLY "
               'CLASSIFIED Found benzene ring with a phenolic OH and an ortho '
               'methoxy group\n'
               ' * SMILES: O=C(NCC1=CC(OC)=C(O)C=C1)CCCCCCC NAME: '
               'N-[(4-Hydroxy-3-methoxyphenyl)methyl]octanamide REASON: '
               'WRONGLY CLASSIFIED Found benzene ring with a phenolic OH and '
               'an ortho methoxy group\n'
               ' * SMILES: COc1cc(CNC(=O)CCCC\\C=C\\C(C)C)ccc1O NAME: '
               'capsaicin REASON: WRONGLY CLASSIFIED Found benzene ring with a '
               'phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'COc1cc(cc(OC)c1O)-c1[o+]c2cc(O)cc(O)c2cc1O[C@@H]1O[C@H](COC(=O)\\C=C\\c2ccc(O)cc2)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: malvidin 3-O-(6-O-(E)-4-coumaroyl-beta-D-glucoside) '
               'REASON: WRONGLY CLASSIFIED Found benzene ring with a phenolic '
               'OH and an ortho methoxy group\n'
               ' * SMILES: OC(C1=NC=CC=2C1=CC(O)=C(OC)C2)C3=CC=C(O)C=C3 NAME: '
               '(S)-Annocherine A REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: O1C(C(O)C(=O)C=2C1=CC(O)=CC2O)C=3C=C(OC)C(O)=C(O)C3 '
               'NAME: Hovenitin I REASON: WRONGLY CLASSIFIED Found benzene '
               'ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O(C1=C(O)C=CC(=C1)C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)CC=C(C)C '
               "NAME: 4''-Deoxyisoterprenin REASON: WRONGLY CLASSIFIED Found "
               'benzene ring with a phenolic OH and an ortho methoxy group\n'
               ' * SMILES: COC1=CC=C(C=C1)NC2=NC(=O)C(=CC3=CC(=C(C=C3)O)OC)S2 '
               'NAME: '
               '5-[(4-hydroxy-3-methoxyphenyl)methylidene]-2-(4-methoxyanilino)-4-thiazolone '
               'REASON: WRONGLY CLASSIFIED Found benzene ring with a phenolic '
               'OH and an ortho methoxy group\n'
               ' * SMILES: '
               'O1C=2C(C(=O)C(OC)=C1C=3C(O)=CC(OC)=C(OC)C3)=C(O)C(OC)=C(OC)C2OC '
               "NAME: 5,2'-Dihydroxy-3,6,7,8,4',5'-hexamethoxyflavone REASON: "
               'WRONGLY CLASSIFIED Found benzene ring with a phenolic OH and '
               'an ortho methoxy group\n'
               ' * SMILES: O(C1=C(O)C(C2=CC=CC=C2)=CC(=C1C3=CC=CC=C3)OC)C '
               'NAME: 2,4-dimethoxy-3,6-diphenylphenol REASON: WRONGLY '
               'CLASSIFIED Found benzene ring with a phenolic OH and an ortho '
               'methoxy group\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No benzene ring with ortho -OH '
                                               'and -OCH3 substituents found'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'We noticed that our previous approach interpreted any '
                 'six‐membered “benzene‐like” ring as a candidate for a '
                 'guaiacol even when it belonged to more complex or fused '
                 'systems. Also, the way in which –OH and –OCH₃ groups were '
                 'recognized needed to be more “strict” to avoid picking up '
                 'oxygen atoms that are part of larger substituents. In this '
                 'improved version we now restrict attention to rings that are '
                 'exactly six atoms long, where every atom is an aromatic '
                 'carbon (by checking both the element and its aromatic flag). '
                 'Then, for each ring atom we inspect its off‐ring neighbors '
                 'and (after having added explicit H’s) require that an –OH is '
                 'confirmed only if the oxygen has exactly one hydrogen and no '
                 'additional heavy atom substituents. Similarly, a methoxy '
                 '(–OCH₃) is only accepted if the oxygen has exactly two '
                 'neighbors (one coming from the ring and the other a carbon) '
                 'and that carbon is sp³ with exactly three hydrogens '
                 'attached. Finally, we check if at least one benzene ring '
                 'provides a phenol (–OH) with at least one of its ortho '
                 '(ring‐adjacent) positions carrying a methoxy group. We '
                 'expect this will reduce false positives coming from extended '
                 'systems, sugars, or fused rings.\n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 81,
    'num_false_positives': 2489,
    'num_true_negatives': 139730,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.03151750972762646,
    'recall': 1.0,
    'f1': 0.06110901546586194,
    'accuracy': 0.9825087842586085,
    'negative_predictive_value': 1.0}