"""
Classifies: CHEBI:35359 carboxamidine
"""
"""
Classifies: Carboxamidine-containing compounds.
Definition: Compounds having the structure RC(=NR)NR2,
i.e. the –C(=NH)NH2 group or a substituted analogue is present.
This version refines matching by:
  • Using two SMARTS patterns (neutral and cationic)
  • Checking that the double‐bonded N is not directly bound to an –OH moiety
    (which would indicate an amidoxime rather than a carboxamidine)
  • Looking at the extra substituent on the carboxamidine carbon to rule out
    cases where it is bonded to an unexpected heteroatom (as in azo or other systems)
  • Relaxing the peptide filter: only very heavy molecules with many amide bonds are rejected.
  
Examples provided by the user include formamidine, acetamidine, benzamidine, guanidine etc.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_carboxamidine(smiles: str):
    """
    Determines if a molecule contains a carboxamidine group (RC(=NR)NR2).

    The algorithm:
      1. Parses the input SMILES.
      2. Adds hydrogen explicitly (to allow neighbor analysis).
      3. Uses two SMARTS patterns to capture both neutral and cationic representations.
         The SMARTS pattern "[CX3](=[NX2])[NX3]" matches a trigonal carbon double bonded to a nitrogen and
         singly bonded to another nitrogen.
      4. For each match, check:
         - That the double-bonded nitrogen is not bound (by a single bond) to any oxygen that carries at least one hydrogen.
           (This helps to filter out amidoxime-like groups.)
         - That the central carbon has one extra neighbor (its R group) and if present, that the extra substituent
           is acceptable (either carbon or hydrogen). If the extra neighbor is not present (as in formamidine) that is acceptable.
      5. Counts amide bonds (using a simple "C(=O)N" SMARTS) so that if a very heavy molecule (mol weight >600) shows
         many (>=4) amide bonds it is flagged as peptide-like (and rejected).
    Returns:
      bool: True if the molecule is classified as containing a carboxamidine group.
      str: Explanation for the classification.
    """
    # Parse SMILES and add explicit hydrogens for correct neighbor analysis.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    mol = Chem.AddHs(mol)
    
    # Define two SMARTS patterns to capture the carboxamidine motif.
    # These patterns look for a carbon with a double bond to a nitrogen and a single bond to another nitrogen.
    pattern_neutral = Chem.MolFromSmarts("[CX3](=[NX2])[NX3]")
    pattern_cationic = Chem.MolFromSmarts("[CX3](=[NX2+])[NX3]")
    if pattern_neutral is None or pattern_cationic is None:
        return False, "Error defining SMARTS patterns."
    
    # Get all matches from both patterns.
    matches1 = mol.GetSubstructMatches(pattern_neutral)
    matches2 = mol.GetSubstructMatches(pattern_cationic)
    # Use a set of tuples to avoid duplicates.
    all_matches = set(matches1) | set(matches2)
    if not all_matches:
        return False, "Carboxamidine moiety (-C(=NH)NH2 or substituted equivalent) not found."
    
    valid_matches = []
    for match in all_matches:
        # Expect match order: (idx_c, idx_dblN, idx_singleN)
        idx_c, idx_ndbl, idx_nsingle = match
        atom_c = mol.GetAtomWithIdx(idx_c)
        atom_ndbl = mol.GetAtomWithIdx(idx_ndbl)
        atom_nsingle = mol.GetAtomWithIdx(idx_nsingle)
        
        # ------------------------------
        # (A) Filter based on oxygen on the double-bonded N:
        # If the double bonded N has any neighbor oxygen where the bond type is SINGLE and that oxygen carries at least one hydrogen,
        # then skip this match as it likely is an amidoxime.
        skip_match = False
        for nbr in atom_ndbl.GetNeighbors():
            if nbr.GetAtomicNum() == 8 and nbr.GetIdx() not in (idx_c, idx_nsingle):
                # Get the bond between atom_ndbl and the oxygen
                bond = mol.GetBondBetweenAtoms(atom_ndbl.GetIdx(), nbr.GetIdx())
                if bond is not None and bond.GetBondType() == Chem.BondType.SINGLE:
                    # Check if oxygen has any explicit hydrogen attached.
                    if nbr.GetTotalNumHs() > 0:
                        skip_match = True
                        break
        if skip_match:
            continue
        
        # ------------------------------
        # (B) Check the extra substituent on the carboxamidine carbon.
        # The carbon is already bonded to the double-bonded N and the single-bonded N.
        # It may have a third neighbor (its R group). For formamidine there is no extra substituent (implicit hydrogen is fine).
        # If an extra neighbor exists, we require it to be a carbon (or hydrogen) rather than an unexpected heteroatom.
        extra_neighbours = [nbr for nbr in atom_c.GetNeighbors() if nbr.GetIdx() not in (idx_ndbl, idx_nsingle)]
        if extra_neighbours:
            for nbr in extra_neighbours:
                if nbr.GetAtomicNum() not in (1, 6):  # allow hydrogen or carbon.
                    # In some systems the substituent may be part of an aromatic ring but then it should be a carbon.
                    skip_match = True
                    break
        if skip_match:
            continue
        
        valid_matches.append(match)
    
    if not valid_matches:
        return False, "Carboxamidine moiety not found after refined filtering."
    
    # Count amide bonds in the molecule (using a simple SMARTS for C(=O)N).
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    num_amide = len(amide_matches)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    # If the molecule is very heavy and has many amide bonds, it is likely peptide‐like.
    if num_amide >= 4 and mol_wt > 600:
        return False, "Molecule appears to be peptide-like (many amide bonds in a heavy molecule), likely a false positive."
    
    return True, f"Found carboxamidine group in {len(valid_matches)} location(s)."

# For testing/debugging only (run when executed as a script).
if __name__ == "__main__":
    test_smiles = [
        "[H]C(N)=N",  # formamidine: expected true positive.
        "CN(Cc1ccc(Cl)nc1)C(\\C)=N/C#N",  # (Z)-acetamiprid: true positive.
        "CC(=N)NCC1=CC(CN)=CC=C1",       # N-[3-(aminomethyl)benzyl]acetamidine: true positive.
        "CN1CCCN=C1\\C=C\\c1cccs1",       # pyrantel: true positive.
        "CC1=N[C@@H]([C@@H](O)CN1)C(O)=O",# 5-hydroxyectoine: true positive.
        "CN(Cc1ccc(Cl)nc1)C(C)=NC#N",      # acetamiprid: true positive.
        "[H][C@@]1(COc2ccc(cc2)-c2ccc(cc2)C(N)=N)C[C@@H](CC(O)=O)C(=O)N1",  # fradafiban: true positive.
        "P(=O)(N=C(N(CC)CC)C)(OC)F",      # A-232 nerve agent: true positive.
        "NC(=N)c1ccc2cccc(Nc3ncccn3)c2c1",# 8-(pyrimidin-2-ylamino)naphthalene-2-carboximidamide: true positive.
        "CC(N)=N",                      # acetamidine: true positive.
        "O[C@H]1[C@@H](O)C(NC(=N)CNC=O)O[C@@H]1COP(O)(O)=O",  # 2-formamido-N(1)-(5-phospho-D-ribosyl)acetamidine: true positive.
        "N[C@@H](CCCCC(N)=N)C(O)=O",      # L-indospicine: true positive.
        "NC(=N)N1CC(O)c2ccccc2C1",        # 4-hydroxydebrisoquin: true positive.
        "Cc1cc(c(O)c(C)c1CC1=NCCN1)C(C)(C)C",  # oxymetazoline: true positive.
        "CC1([C@@H](N2[C@@H](S1)[C@@H](C2=O)N=CN3CCCCCC3)C(=O)OCOC(=O)C(C)(C)C)C",  # 2,2-dimethylpropanoyloxymethyl ...: true positive.
        "CN(C=Nc1ccc(C)cc1C)C=Nc1ccc(C)cc1C",# amitraz: true positive.
        "CC(Oc1c(Cl)cccc1Cl)C1=NCCN1",      # lofexidine: true positive.
        "CN=CNc1ccc(C)cc1C",              # N'-(2,4-dimethylphenyl)-N-methylformamidine: true positive.
        "NC(=N)N1CCc2ccccc2C1",           # debrisoquin: true positive.
        "P(=O)(N=C(N(CC)CC)C)(C)F",        # A-230 nerve agent: true positive.
        "CC1=N[C@@H](CCN1)C(O)=O",         # ectoine: true positive.
        "CCCCCNC(=N)N\\N=C\\c1c[nH]c2ccc(OC)cc12",  # tegaserod: true positive.
        "NC(=N)c1ccc(NN=Nc2ccc(cc2)C(N)=N)cc1",  # diminazene: true positive.
        "NC(=N)c1c[nH]c2nc(N)[nH]c(=O)c12",      # 7-formamidino-7-deazaguanine: true positive.
        "C(CCCOC1=CC=C(C=C1)C(N)=N)COC2=CC=C(C=C2)C(N)=N",  # pentamidine: true positive.
        "C[C@H]1O[C@H](O[C@@H]2[C@@H](O)[C@@H](O)[C@H](O)[C@H](O)[C@H]2O)[C@@H](N)C[C@@H]1NC(=N)C(O)=O",  # kasugamycin: true positive.
        "CON=CNC(=O)c1ccc(cc1C)C1=NO[C@@](C1)(c1cc(Cl)cc(Cl)c1)C(F)(F)F",  # (S)-fluxametamide: true positive expected but may be missed if too many oxygen neighbors occur.
        "CN(C)C=Nc1cccc(O)c1",  # N'-(3-hydroxyphenyl)-N,N-dimethylformamidine: true positive.
        "CC\\N=C(/N)c1ccc(cc1)-c1ccc(o1)-c1ccc(cc1)C(\\N)=N\\CC",  # 2,5-bis{[4-(N-ethylamidino)]phenyl}furan: true positive.
        # False positives examples (these should NOT be classified as carboxamidine):
        "CC(C)(C(=N)N)N=NC(C)(C)C(=N)N",  # wrongly classified: extra unsaturated groups etc.
        "[H+].[H+].[O-]C(=O)\\C=C/C([O-])=O.CCCCCNC(=N)N\\N=C\\c1c[nH]c2ccc(OC)cc12",  # tegaserod maleate: should be rejected.
        "C1(=NC=C(C=C1C(=O)O)COC)C2=NC(C(N2)(C)C(C)C)=O",  # another false positive.
        "C1C(N=C(C(=O)O1)NNC2=CC=CC=C2Cl)(CO)CO",  # another false positive.
        "CC1=CC=C(C=C1)C2=NC(C3=C(N2)N(C(=O)[C@H](NCC(O)=O)C1CCCCC1)C4=CC=C(C=C4)F)(C(F)(F)F)C(F)(F)F",  # another false positive.
        "CC1=CC=C(C=C1)N(CC2=NCCN2)C3=CC=C(C=C3)O",  # another false positive.
        "C=1(N(C(N=C(N1)N)(C)C)C=2C=CC(=CC2)Cl)N.C3=CC=CC4=C3C=C(C(=C4CC=5C6=C(C=C(C5O)C(=O)O)C=CC=C6)O)C(=O)O.C=7(N(C(N=C(N7)N)(C)C)C=8C=CC(=CC8)Cl)N",  # Cycloguanil pamoate: false positive.
        "S(=O)(=O)(O[C@@H]1C(O)(O)[C@]23NC(N)=N[C@H]2[C@H](CO)N=C(N3C1)N",  # Decarbamoylgonyautoxin-3: false positive.
        "OC(=O)CNC=N",  # N-formimidoylglycine: false positive.
        "S(/C(=N\\C#N)/N1CCC(C(=O)N)CC1)C",  # Methyl 4-(aminocarbonyl)-n-cyanotetrahydropyridine-1(2H)-carbimidothioate: false positive.
        "NC(=N)NCCCCCC(O)=O",  # 6-guanidinohexanoic acid: false positive.
        "O.Cl.Cl.C\\C(\\C=N\\NC(N)=N)=N/NC(N)=N",  # mitoguazone hydrochloride hydrate: false positive.
        "O(C1C(O)C(O)C(OC1)(O)CNC(CCCN=C(N)N)C(O)=O)C2OC(C(O)C(O)C2O)CO",  # N2-Maltulosylarginine: false positive.
        "CN1CCN(CC1)C=NC2=C(C3=C(S2)CCCCC3)C#N",  # another false positive.
        "OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1N=CNCC2=O",  # dehydrocoformycin: false positive.
        "OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H]",  # L-arginine-d7: false positive.
        "CN1COCN(Cc2cnc(Cl)s2)C1=N[N+]([O-])=O",  # thiamethoxam: false positive.
        "CC1=CC=C(C=C1)NC(=O)CSC2=NCCN2",  # another false positive.
        "C1CCC2(C1)C3=C(CCCC3=O)NC(=N2)NC4=NC5=CC=CC=C5O4",  # another false positive.
        "CC1=CC(=CC=C1)NC(=S)N=C(N)NC2=NC3=C(C=CC(=C3)C)C(=N2)C",  # another false positive.
        "COC1=CC(=CC(=C1O)OC)C=C2C(=O)N=C(S2)NC3=CC=C(C=C3)O",  # another false positive.
        "C1=CC=C(C=C1)CNC2=NC(=O)C(=CC3=CC=CC=C3)S2",  # another false positive.
        "COC1=C(C=CC(=C1)C=C2C(=O)N=C(S2)NC3=CC=CC=C3Cl)O",  # another false positive.
        "C1CNC2=NCCCN2C1"  # another false positive.
    ]
    
    for smi in test_smiles:
        res, reason = is_carboxamidine(smi)
        print(f"SMILES: {smi}\nResult: {res}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35359',
                          'name': 'carboxamidine',
                          'definition': 'Compounds having the structure '
                                        'RC(=NR)NR2. The term is used as a '
                                        'suffix in systematic nomenclature to '
                                        'denote the -C(=NH)NH2 group including '
                                        'its carbon atom.',
                          'parents': ['CHEBI:2634', 'CHEBI:35352'],
                          'xrefs': ['KEGG:C06060'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 145,
                           'log_lines_of_code': 4.976733742420574,
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
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetTotalNumHs',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'CCCCCNC',
                                                 'GetBondType',
                                                 'AddHs',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 14,
                           'smarts_strings': [   '[CX3](=[NX2+])[NX3]',
                                                 '[CX3](=[NX2])[NX3]',
                                                 'C(=O)N'],
                           'smarts_strings_count': 3,
                           'defs': ['is_carboxamidine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "Error defining SMARTS '
                                          'patterns."',
                                          'False, "Carboxamidine moiety '
                                          '(-C(=NH)NH2 or substituted '
                                          'equivalent) not found."',
                                          'False, "Carboxamidine moiety not '
                                          'found after refined filtering."',
                                          'False, "Molecule appears to be '
                                          'peptide-like (many amide bonds in a '
                                          'heavy molecule), likely a false '
                                          'positive."',
                                          'True, f"Found carboxamidine group '
                                          'in {len(valid_matches)} '
                                          'location(s)."'],
                           'returns_count': 6,
                           'complexity': 6.395346748484115},
    'message': '\n'
               'Attempt failed: F1 score of 0.05355648535564853 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: [H]C(N)=N NAME: formamidine REASON: '
               'CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CN(Cc1ccc(Cl)nc1)C(\\C)=N/C#N NAME: (Z)-acetamiprid '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CC(=N)NCC1=CC(CN)=CC=C1 NAME: '
               'N-[3-(aminomethyl)benzyl]acetamidine REASON: CORRECT Found '
               'carboxamidine group in 1 location(s).\n'
               ' * SMILES: CN1CCCN=C1\\C=C\\c1cccs1 NAME: pyrantel REASON: '
               'CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CC1=N[C@@H]([C@@H](O)CN1)C(O)=O NAME: '
               '5-hydroxyectoine REASON: CORRECT Found carboxamidine group in '
               '1 location(s).\n'
               ' * SMILES: CN(Cc1ccc(Cl)nc1)C(C)=NC#N NAME: acetamiprid '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: '
               '[H][C@@]1(COc2ccc(cc2)-c2ccc(cc2)C(N)=N)C[C@@H](CC(O)=O)C(=O)N1 '
               'NAME: fradafiban REASON: CORRECT Found carboxamidine group in '
               '1 location(s).\n'
               ' * SMILES: P(=O)(N=C(N(CC)CC)C)(OC)F NAME: A-232 nerve agent '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: NC(=N)c1ccc2cccc(Nc3ncccn3)c2c1 NAME: '
               '8-(pyrimidin-2-ylamino)naphthalene-2-carboximidamide REASON: '
               'CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CC(N)=N NAME: acetamidine REASON: CORRECT Found '
               'carboxamidine group in 1 location(s).\n'
               ' * SMILES: O[C@H]1[C@@H](O)C(NC(=N)CNC=O)O[C@@H]1COP(O)(O)=O '
               'NAME: 2-formamido-N(1)-(5-phospho-D-ribosyl)acetamidine '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: N[C@@H](CCCCC(N)=N)C(O)=O NAME: L-indospicine '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: NC(=N)N1CC(O)c2ccccc2C1 NAME: 4-hydroxydebrisoquin '
               'REASON: CORRECT Found carboxamidine group in 2 location(s).\n'
               ' * SMILES: Cc1cc(c(O)c(C)c1CC1=NCCN1)C(C)(C)C NAME: '
               'oxymetazoline REASON: CORRECT Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: '
               'CC1([C@@H](N2[C@@H](S1)[C@@H](C2=O)N=CN3CCCCCC3)C(=O)OCOC(=O)C(C)(C)C)C '
               'NAME: 2,2-dimethylpropanoyloxymethyl '
               '(2S,5S,6R)-6-(azepan-1-ylmethylideneamino)-3,3-dimethyl-7-oxo-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylate '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CN(C=Nc1ccc(C)cc1C)C=Nc1ccc(C)cc1C NAME: amitraz '
               'REASON: CORRECT Found carboxamidine group in 2 location(s).\n'
               ' * SMILES: CC(Oc1c(Cl)cccc1Cl)C1=NCCN1 NAME: lofexidine '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CN=CNc1ccc(C)cc1C NAME: '
               "N'-(2,4-dimethylphenyl)-N-methylformamidine REASON: CORRECT "
               'Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: NC(=N)N1CCc2ccccc2C1 NAME: debrisoquin REASON: '
               'CORRECT Found carboxamidine group in 2 location(s).\n'
               ' * SMILES: P(=O)(N=C(N(CC)CC)C)(C)F NAME: A-230 nerve agent '
               'REASON: CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CC1=N[C@@H](CCN1)C(O)=O NAME: ectoine REASON: '
               'CORRECT Found carboxamidine group in 1 location(s).\n'
               ' * SMILES: CCCCCNC(=N)N\\N=C\\c1c[nH]c2ccc(OC)cc12 NAME: '
               'tegaserod REASON: CORRECT Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: NC(=N)c1ccc(NN=Nc2ccc(cc2)C(N)=N)cc1 NAME: '
               'diminazene REASON: CORRECT Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: NC(=N)c1c[nH]c2nc(N)[nH]c(=O)c12 NAME: '
               '7-formamidino-7-deazaguanine REASON: CORRECT Found '
               'carboxamidine group in 1 location(s).\n'
               ' * SMILES: C(CCCOC1=CC=C(C=C1)C(N)=N)COC2=CC=C(C=C2)C(N)=N '
               'NAME: pentamidine REASON: CORRECT Found carboxamidine group in '
               '2 location(s).\n'
               'False positives: SMILES: CC(C)(C(=N)N)N=NC(C)(C)C(=N)N NAME: '
               '2-(1-amino-1-imino-2-methylpropan-2-yl)azo-2-methylpropanimidamide '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: '
               '[H+].[H+].[O-]C(=O)\\C=C/C([O-])=O.CCCCCNC(=N)N\\N=C\\c1c[nH]c2ccc(OC)cc12 '
               'NAME: tegaserod maleate REASON: WRONGLY CLASSIFIED Found '
               'carboxamidine group in 2 location(s).\n'
               ' * SMILES: C1(=NC=C(C=C1C(=O)O)COC)C2=NC(C(N2)(C)C(C)C)=O '
               'NAME: '
               '2-(4-isopropyl-4-methyl-5-oxo-4,5-dihydro-1H-imidazol-2-yl)-5-(methoxymethyl)nicotinic '
               'acid REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: C1C(N=C(C(=O)O1)NNC2=CC=CC=C2Cl)(CO)CO NAME: '
               '5-[(2-chlorophenyl)hydrazo]-3,3-bis(hydroxymethyl)-2H-1,4-oxazin-6-one '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)C2=NC(C3=C(N2)N(C(=O)NC3=O)C4=CC=C(C=C4)F)(C(F)(F)F)C(F)(F)F '
               'NAME: '
               '1-(4-fluorophenyl)-7-(4-methylphenyl)-5,5-bis(trifluoromethyl)-8H-pyrimido[4,5-d]pyrimidine-2,4-dione '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: CC1=CC=C(C=C1)N(CC2=NCCN2)C3=CC=C(C=C3)O NAME: '
               '4-[N-(4,5-dihydro-1H-imidazol-2-ylmethyl)-4-methylanilino]phenol '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: '
               'C=1(N(C(N=C(N1)N)(C)C)C=2C=CC(=CC2)Cl)N.C3=CC=CC4=C3C=C(C(=C4CC=5C6=C(C=C(C5O)C(=O)O)C=CC=C6)O)C(=O)O.C=7(N(C(N=C(N7)N)(C)C)C=8C=CC(=CC8)Cl)N '
               'NAME: Cycloguanil pamoate REASON: WRONGLY CLASSIFIED Found '
               'carboxamidine group in 6 location(s).\n'
               ' * SMILES: '
               'S(=O)(=O)(O[C@@H]1C(O)(O)[C@]23NC(N)=N[C@H]2[C@H](CO)N=C(N3C1)N)O '
               'NAME: Decarbamoylgonyautoxin-3 REASON: WRONGLY CLASSIFIED '
               'Found carboxamidine group in 4 location(s).\n'
               ' * SMILES: OC(=O)CNC=N NAME: N-formimidoylglycine REASON: '
               'WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: S(/C(=N\\C#N)/N1CCC(C(=O)N)CC1)C NAME: Methyl '
               '4-(aminocarbonyl)-n-cyanotetrahydropyridine-1(2H)-carbimidothioate '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: NC(=N)NCCCCCC(O)=O NAME: 6-guanidinohexanoic acid '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: O.Cl.Cl.C\\C(\\C=N\\NC(N)=N)=N/NC(N)=N NAME: '
               'mitoguazone hydrochloride hydrate REASON: WRONGLY CLASSIFIED '
               'Found carboxamidine group in 4 location(s).\n'
               ' * SMILES: '
               'O(C1C(O)C(O)C(OC1)(O)CNC(CCCN=C(N)N)C(O)=O)C2OC(C(O)C(O)C2O)CO '
               'NAME: N2-Maltulosylarginine REASON: WRONGLY CLASSIFIED Found '
               'carboxamidine group in 2 location(s).\n'
               ' * SMILES: CN1CCN(CC1)C=NC2=C(C3=C(S2)CCCCC3)C#N NAME: '
               '2-[(4-methyl-1-piperazinyl)methylideneamino]-5,6,7,8-tetrahydro-4H-cyclohepta[b]thiophene-3-carbonitrile '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1N=CNCC2=O '
               'NAME: dehydrocoformycin REASON: WRONGLY CLASSIFIED Found '
               'carboxamidine group in 1 location(s).\n'
               ' * SMILES: '
               'OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H] '
               'NAME: L-arginine-d7 REASON: WRONGLY CLASSIFIED Found '
               'carboxamidine group in 2 location(s).\n'
               ' * SMILES: CN1COCN(Cc2cnc(Cl)s2)C1=N[N+]([O-])=O NAME: '
               'thiamethoxam REASON: WRONGLY CLASSIFIED Found carboxamidine '
               'group in 2 location(s).\n'
               ' * SMILES: CC1=CC=C(C=C1)NC(=O)CSC2=NCCN2 NAME: '
               '2-(4,5-dihydro-1H-imidazol-2-ylthio)-N-(4-methylphenyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: C1CCC2(C1)C3=C(CCCC3=O)NC(=N2)NC4=NC5=CC=CC=C5O4 '
               'NAME: '
               "2-(1,3-benzoxazol-2-ylamino)-5-spiro[1,6,7,8-tetrahydroquinazoline-4,1'-cyclopentane]one "
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: '
               'CC1=CC(=CC=C1)NC(=S)N=C(N)NC2=NC3=C(C=CC(=C3)C)C(=N2)C NAME: '
               '1-[amino-[(4,7-dimethyl-2-quinazolinyl)amino]methylidene]-3-(3-methylphenyl)thiourea '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: COC1=CC(=CC(=C1O)OC)C=C2C(=O)N=C(S2)NC3=CC=C(C=C3)O '
               'NAME: '
               '2-(4-hydroxyanilino)-5-[(4-hydroxy-3,5-dimethoxyphenyl)methylidene]-4-thiazolone '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: C1=CC=C(C=C1)CNC2=NC(=O)C(=CC3=CC=CC=C3)S2 NAME: '
               '2-[(phenylmethyl)amino]-5-(phenylmethylene)-4-thiazolone '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: COC1=C(C=CC(=C1)C=C2C(=O)N=C(S2)NC3=CC=CC=C3Cl)O '
               'NAME: '
               '2-(2-chloroanilino)-5-[(4-hydroxy-3-methoxyphenyl)methylidene]-4-thiazolone '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 1 '
               'location(s).\n'
               ' * SMILES: C1CNC2=NCCCN2C1 NAME: '
               '3,4,6,7,8,9-hexahydro-2H-pyrimido[1,2-a]pyrimidine REASON: '
               'WRONGLY CLASSIFIED Found carboxamidine group in 2 '
               'location(s).\n'
               ' * SMILES: CCCSP(=O)(OCC)N1CCN(CC)\\C1=N/C#N NAME: Imicyafos '
               'REASON: WRONGLY CLASSIFIED Found carboxamidine group in 2 '
               'location(s).\n'
               'False negatives: SMILES: '
               'CCCCCCOC(=O)\\N=C(\\N)c1ccc(NCc2nc3cc(ccc3n2C)C(=O)N(CCC(=O)OCC)c2ccccn2)cc1 '
               'NAME: dabigatran etexilate REASON: MISSED Molecule appears to '
               'be peptide-like (many amide bonds in a heavy molecule), likely '
               'a false positive.\n'
               ' * SMILES: '
               '[H][C@]1(CCN1C(=O)[C@H](NCC(O)=O)C1CCCCC1)C(=O)NCc1ccc(cc1)C(N)=N '
               'NAME: melagatran REASON: MISSED Molecule appears to be '
               'peptide-like (many amide bonds in a heavy molecule), likely a '
               'false positive.\n'
               ' * SMILES: '
               'CON=CNC(=O)c1ccc(cc1C)C1=NO[C@](C1)(c1cc(Cl)cc(Cl)c1)C(F)(F)F '
               'NAME: (R)-fluxametamide REASON: MISSED Carboxamidine moiety '
               'not found after filtering out oxygen-substituted forms.\n'
               ' * SMILES: '
               'Fc1ccc(c(\\C(NC(=O)Cc2ccccc2)=N\\OCC2CC2)c1F)C(F)(F)F NAME: '
               'cyflufenamid REASON: MISSED Carboxamidine moiety not found '
               'after filtering out oxygen-substituted forms.\n'
               ' * SMILES: '
               'CON=CNC(=O)c1ccc(cc1C)C1=NO[C@@](C1)(c1cc(Cl)cc(Cl)c1)C(F)(F)F '
               'NAME: (S)-fluxametamide REASON: MISSED Carboxamidine moiety '
               'not found after filtering out oxygen-substituted forms.\n'
               ' * SMILES: '
               'CON=CNC(=O)c1ccc(cc1C)C1=NOC(C1)(c1cc(Cl)cc(Cl)c1)C(F)(F)F '
               'NAME: '
               '4-[5-(3,5-dichlorophenyl)-5-(trifluoromethyl)-4,5-dihydro-1,2-oxazol-3-yl]-N-[(methoxyamino)methylidene]-2-methylbenzamide '
               'REASON: MISSED Carboxamidine moiety not found after filtering '
               'out oxygen-substituted forms.\n'
               ' * SMILES: CNC(NCCSCc1csc(CN(C)C)n1)=C[N+]([O-])=O NAME: '
               'nizatidine REASON: MISSED Carboxamidine moiety (-C(=NH)NH2 or '
               'substituted equivalent) not found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Carboxamidine moiety '
                                               '(-C(=NH)NH2 or substituted '
                                               'equivalent) not found.'}],
    'sample_false_negatives': [   {   'smiles': 'NC(=N)N1CC(O)c2ccccc2C1',
                                      'name': '4-hydroxydebrisoquin',
                                      'reason': 'Carboxamidine moiety not '
                                                'found after refined '
                                                'filtering.'},
                                  {   'smiles': 'NC(=N)N1CCc2ccccc2C1',
                                      'name': 'debrisoquin',
                                      'reason': 'Carboxamidine moiety not '
                                                'found after refined '
                                                'filtering.'},
                                  {   'smiles': 'CCCCCNC(=N)N\\N=C\\c1c[nH]c2ccc(OC)cc12',
                                      'name': 'tegaserod',
                                      'reason': 'Carboxamidine moiety not '
                                                'found after refined '
                                                'filtering.'},
                                  {   'smiles': 'CNC(NCCSCc1csc(CN(C)C)n1)=C[N+]([O-])=O',
                                      'name': 'nizatidine',
                                      'reason': 'Carboxamidine moiety '
                                                '(-C(=NH)NH2 or substituted '
                                                'equivalent) not found.'},
                                  {   'smiles': 'NC(N)=N',
                                      'name': 'guanidine',
                                      'reason': 'Carboxamidine moiety not '
                                                'found after refined '
                                                'filtering.'}],
    'attempt': 2,
    'reasoning': 'Below is one complete Python solution. In the reflection '
                 'below I describe the reasoning:\n'
                 '\n'
                 '────────────────────────────\n'
                 'Reasoning:\n'
                 '────────────────────────────\n'
                 'The previous approach used one–or–two SMARTS patterns '
                 '([CX3](=[NX2])[NX3] and its cationic analogue) and then '
                 '“filtered out” any match in which the double‐bonded nitrogen '
                 'was neighboring any oxygen. In our analysis we noted that '
                 '(a) if we simply reject any match with an oxygen neighbor we '
                 'will miss cases where oxygen appears in an unrelated '
                 'carbonyl, (b) using only one match order leaves ambiguity '
                 'and (c) the “peptide‐like” filter (rejecting heavy molecules '
                 'with two or more amide bonds) was too strict and is causing '
                 'false negatives for valid carboxamidine examples embedded in '
                 'larger structures.\n'
                 '\n'
                 'To improve we have made a number of modifications:\n'
                 '\u2003• We use the same two SMARTS patterns (“neutral” and '
                 '“cationic”) for the –C(=N)N moiety.\n'
                 '\u2003• Instead of rejecting every match when any oxygen is '
                 'adjacent to the double‐bonded nitrogen, we now “reject” only '
                 'if that oxygen appears as –OH (i.e. when the oxygen atom '
                 'carries at least one hydrogen and is bound by a single bond) '
                 'because that is typical of an amidoxime.\n'
                 '\u2003• We also check that the central carbon has one extra '
                 'substituent (if present) that is “reasonable” (that is, if '
                 'an extra neighbor exists it should be C or H; a “non‐carbon” '
                 'extra neighbor may indicate a non‐carboxamidine '
                 'functionality such as an azo linkage).\n'
                 '\u2003• Finally, we relax the peptide filter (which counts '
                 'amide bonds) by requiring that only very heavy molecules '
                 'with many amide bonds are rejected. (The thresholds were '
                 'adjusted so that molecules like dabigatran etexilate or '
                 'melagatran – which are quite large – are not thrown out '
                 'although we note that some very peptide–like false positives '
                 'may slip through.)\n'
                 '\n'
                 'The code then obtains all matches (avoiding duplicate '
                 'matches) and loops through each match to apply the refined '
                 'filters. If at least one valid match remains, the '
                 'carboxamidine moiety is considered present.\n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '────────────────────────────\n'
                 'Code:\n'
                 '────────────────────────────',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 34,
    'num_false_positives': 432,
    'num_true_negatives': 141829,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.07296137339055794,
    'recall': 0.8717948717948718,
    'f1': 0.13465346534653466,
    'accuracy': 0.9969290231904427,
    'negative_predictive_value': 0.9999647475217508}