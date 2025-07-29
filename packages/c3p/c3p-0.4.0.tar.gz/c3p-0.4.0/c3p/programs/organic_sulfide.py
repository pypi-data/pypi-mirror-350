"""
Classifies: CHEBI:16385 organic sulfide
"""
"""
Classifies: Organic sulfide (thioether)
Definition: Compounds having the structure R–S–R (with R ≠ H).
Such compounds were once called thioethers.

Improvements compared with the previous classifier:
  • Excludes many peptides or free amino acids by checking for a typical amino acid zwitterion
    and by counting amide bonds.
  • For each sulfur atom, requires:
       - Exactly two explicit neighbors.
       - Each S–neighbor bond is a single bond.
       - Both neighbors are carbon (atomic number 6).
       - The sulfur is not flagged as aromatic (so that fused/sulfur‐in‐ring systems are avoided).
  • This more stringent approach helps to lower false positives.
"""

from rdkit import Chem

def is_organic_sulfide(smiles: str):
    """
    Determines if a molecule is an organic sulfide (thioether) based on its SMILES string.
    
    An organic sulfide is defined as a molecule containing at least one R–S–R moiety,
    where both substituents (R) are not hydrogen and the sulfur is not oxidized (e.g. no bonds
    to oxygen) and is not part of a fused aromatic moiety. In addition, we filter out
    many simple peptides or free amino acids.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as an organic sulfide, False otherwise.
        str: Explanation of the classification.
    """
    
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # ----- Filter out obvious peptides / free amino acids -----
    # (a) Check for a typical amino acid zwitterion (e.g. methionine side-chain in a free amino acid)
    amino_acid_pattern = Chem.MolFromSmarts("[C@H]([NH3+])C(=O)[O-]")
    if mol.GetNumAtoms() < 50 and mol.HasSubstructMatch(amino_acid_pattern):
        return False, "Molecule appears to be a free amino acid (not classified as organic sulfide)"
    
    # (b) Count amide bonds. Many peptide‐derived molecules contain more than one amide bond.
    # There is a risk that a lone amide is present in a non‐peptidic context
    # so we only disqualify if there is more than one.
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if len(amide_matches) > 1:
        return False, "Molecule appears to be peptide-derived (contains multiple amide bonds)"
    
    # ----- Scan for a genuine thioether motif (R–S–R) -----
    # Iterate over every sulfur atom. For each sulfur, we demand:
    #   1. The S atom is not aromatic.
    #   2. It has exactly two neighbors (explicit heavy atoms).
    #   3. Both connecting bonds are SINGLE bonds.
    #   4. Both neighbors are carbon atoms.
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 16:  # Only consider sulfur atoms.
            continue
        
        # Check if the sulfur atom is aromatic.
        if atom.GetIsAromatic():
            continue  # likely part of a fused or heterocyclic system (not our desired thioether)
        
        # We require exactly 2 explicit neighbors.
        neighbors = atom.GetNeighbors()
        if len(neighbors) != 2:
            continue
        
        # Check each bond from S to neighbor is SINGLE.
        valid_bonds = True
        for nbr in neighbors:
            bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
            if bond is None or bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
                valid_bonds = False
                break
        if not valid_bonds:
            continue
        
        # Check that both neighbors are carbon atoms.
        if not (neighbors[0].GetAtomicNum() == 6 and neighbors[1].GetAtomicNum() == 6):
            continue

        # If we pass all the checks, then we have found a genuine thioether moiety.
        return True, "Molecule contains at least one organic sulfide (thioether) group (R–S–R bond)"
    
    return False, "No organic sulfide (R–S–R) moiety found in the molecule"

# Example usage: (testing on a subset of the provided SMILES)
if __name__ == "__main__":
    test_smiles = [
        # True positives (should classify as organic sulfide)
        "CCCCCCCCCCCCCCCSC[C@H](COP(O)(=O)OCC[N+](C)(C)C)OP(O)(=O)CCCCCCCCCCCCCCCC",  # long-chain thioether
        "COC(=O)C(CC1=CC2C(CC(NC2C=C1)c1c(Cl)cccc1Cl)Sc1ccccc1)NC(=O)OC(C)(C)C",       # thioether with aromatic groups
        "C1CC2=C(C1)NC(=NC2=O)SCC3=CC=C(C=C3)Cl",                                      # thioether group present
        "CC1=C(C(=NN1)SCC(=O)N2CCCCCC2)[N+](=O)[O-]",                                 # another thioether motif
        # False positive candidates (expected to be rejected due to peptide patterns or non-thioether S)
        "CN1C(C(=O)Nc2ccccn2)=C(O)c2sccc2S1(=O)=O",  # tenoxicam-like structure, S in heterocycle
        "CCOC(=O)C1C(C2=C(CCCC2=O)N=C1C)C3=CC=CS3"     # thiophen-containing, not a genuine R–S–R pattern
    ]
    for s in test_smiles:
        result, reason = is_organic_sulfide(s)
        print(f"SMILES: {s}\nResult: {result} | Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16385',
                          'name': 'organic sulfide',
                          'definition': 'Compounds having the structure RSR (R '
                                        '=/= H). Such compounds were once '
                                        'called thioethers.',
                          'parents': ['CHEBI:26822', 'CHEBI:33261'],
                          'xrefs': ['KEGG:C00297'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 70,
                           'log_lines_of_code': 4.248495242049359,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 2,
                                                 2,
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
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'GetAtoms',
                                                 'GetIsAromatic',
                                                 'MolFromSmiles',
                                                 'GetNeighbors',
                                                 'HasSubstructMatch',
                                                 'GetBondBetweenAtoms',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'GetNumAtoms'],
                           'methods_called_count': 12,
                           'smarts_strings': [   '[C@H]([NH3+])C(=O)[O-]',
                                                 'C(=O)N'],
                           'smarts_strings_count': 2,
                           'defs': ['is_organic_sulfide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule appears to be a '
                                          'free amino acid (not classified as '
                                          'organic sulfide)"',
                                          'False, "Molecule appears to be '
                                          'peptide-derived (contains multiple '
                                          'amide bonds)"',
                                          'False, "No organic sulfide (R–S–R) '
                                          'moiety found in the molecule"'],
                           'returns_count': 4,
                           'complexity': 5.049699048409872},
    'message': '\n'
               'Attempt failed: F1 score of 0.165845909451946 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCCCCCCCCCCSC[C@H](COP(O)(=O)OCC[N+](C)(C)C)OP(O)(=O)CCCCCCCCCCCCCCCC '
               'NAME: '
               '1-S-hexadecyl-2-O-[hexadecyl(hydroxy)phosphoryl]-1-thio-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'COC(=O)C(CC1=CC2C(CC(NC2C=C1)c1c(Cl)cccc1Cl)Sc1ccccc1)NC(=O)OC(C)(C)C '
               'NAME: methyl '
               'N-(tert-butoxycarbonyl)-3-[2-(2,6-dichlorophenyl)-4-(phenylsulfanyl)-1,2,3,4,4a,8a-hexahydro-6-quinolyl]alaninate '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: C1CC2=C(C1)NC(=NC2=O)SCC3=CC=C(C=C3)Cl NAME: '
               '2-[(4-chlorophenyl)methylthio]-1,5,6,7-tetrahydrocyclopenta[d]pyrimidin-4-one '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: CC1=C(C(=NN1)SCC(=O)N2CCCCCC2)[N+](=O)[O-] NAME: '
               '1-(1-azepanyl)-2-[(5-methyl-4-nitro-1H-pyrazol-3-yl)thio]ethanone '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'N(C1=NC(=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]3O)SC)CC=C(C)C '
               "NAME: 2-methylthio-N(6)-dimethylallyladenine 5'-monophosphate "
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: S(C1=C(OC(=C1)C)C)C(=O)C NAME: '
               '2,5-Dimethyl-3-furanthiol acetate REASON: CORRECT Molecule '
               'contains at least one organic sulfide (thioether) group (R–S–R '
               'bond)\n'
               ' * SMILES: Nc1c(SC(F)(F)F)c(nn1-c1c(Cl)cc(cc1Cl)C(F)(F)F)C#N '
               'NAME: fipronil-sulfide REASON: CORRECT Molecule contains at '
               'least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CSc1ccc2Sc3ccccc3CC(N3CCN(C)CC3)c2c1 NAME: '
               'methiothepin REASON: CORRECT Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CC(C)(O)c1ccccc1CC[C@@H](SCC1(CC1)CC([O-])=O)c1cccc(\\C=C\\c2ccc3ccc(Cl)cc3n2)c1 '
               'NAME: montelukast(1-) REASON: CORRECT Molecule contains at '
               'least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'C1C[C@@H]2C(C(=C([C@H]1C2)SC3=CC=CC=C3)C(C4=CC=C(C=C4Cl)S(C)(=O)=O)=O)=O '
               'NAME: (1S,5R)-benzobicyclon REASON: CORRECT Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CSc1nnc(c(=O)n1N)C(C)(C)C NAME: metribuzin REASON: '
               'CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CC(C)CN(C1CCS(=O)(=O)C1)C(=O)CSC2=NN(C(=S)S2)C3=CC=C(C=C3)Cl '
               'NAME: '
               '2-[[4-(4-chlorophenyl)-5-sulfanylidene-1,3,4-thiadiazol-2-yl]thio]-N-(1,1-dioxo-3-thiolanyl)-N-(2-methylpropyl)acetamide '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: Clc1ccc(C(Cn2ccnc2)OCc2ccc(Sc3ccccc3)cc2)c(Cl)c1 '
               'NAME: '
               '1-[2-(2,4-dichlorophenyl)-2-{[4-(phenylsulfanyl)benzyl]oxy}ethyl]imidazole '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: CC1CCC2=C(C1)SC3=C2C(=NC(=N3)CN4CCOCC4)SC5=CC=CC=C5 '
               'NAME: '
               '4-[[7-methyl-4-(phenylthio)-5,6,7,8-tetrahydro-[1]benzothiolo[2,3-d]pyrimidin-2-yl]methyl]morpholine '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: O=C(O)[C@@H](NO)CCCCCCSC NAME: '
               'N-hydroxy-L-tetrahomomethionine REASON: CORRECT Molecule '
               'contains at least one organic sulfide (thioether) group (R–S–R '
               'bond)\n'
               ' * SMILES: OCCSCCO NAME: thiodiglycol REASON: CORRECT Molecule '
               'contains at least one organic sulfide (thioether) group (R–S–R '
               'bond)\n'
               ' * SMILES: CC#CC1=C(C)C2=C(C=C1)C(=O)NC(CSC1=NC=CC=N1)=N2 '
               'NAME: ITK7 REASON: CORRECT Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'COCCCN1C(=NN=C1SCC(=O)OC)CC2=CSC(=N2)NC3=CC(=CC=C3)Cl NAME: '
               '2-[[5-[[2-(3-chloroanilino)-4-thiazolyl]methyl]-4-(3-methoxypropyl)-1,2,4-triazol-3-yl]thio]acetic '
               'acid methyl ester REASON: CORRECT Molecule contains at least '
               'one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CC1=C(C(=O)NN1)C(C2=CC=C(C=C2)SC)C3=C(NNC3=O)C '
               'NAME: '
               '5-methyl-4-[(3-methyl-5-oxo-1,2-dihydropyrazol-4-yl)-[4-(methylthio)phenyl]methyl]-1,2-dihydropyrazol-3-one '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: [H]C(C)=C([H])SC([H])=C([H])C NAME: di-1-propenyl '
               'sulfide REASON: CORRECT Molecule contains at least one organic '
               'sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CC(C(=O)OC)SC1=NNC(=S)S1 NAME: '
               '2-[(2-sulfanylidene-3H-1,3,4-thiadiazol-5-yl)thio]propanoic '
               'acid methyl ester REASON: CORRECT Molecule contains at least '
               'one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CCC1=CC=C(C=C1)NC2=NN=C(S2)SC3CCOC3=O NAME: '
               '3-[[5-(4-ethylanilino)-1,3,4-thiadiazol-2-yl]thio]-2-oxolanone '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: CN1C(=NN=N1)SC2=NC=NC3=C2C(=CS3)C4=CC=CC=C4OC NAME: '
               '5-(2-methoxyphenyl)-4-[(1-methyl-5-tetrazolyl)thio]thieno[2,3-d]pyrimidine '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: S(C1=CC=CC=C1)C=C NAME: Phenyl vinyl sulfide '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CN1C(=NN=N1)SC2=NC=NC3=C2C(=CS3)C4=CC(=CC=C4)C(F)(F)F NAME: '
               '4-[(1-methyl-5-tetrazolyl)thio]-5-[3-(trifluoromethyl)phenyl]thieno[2,3-d]pyrimidine '
               'REASON: CORRECT Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               'False positives: SMILES: '
               'CN1C(C(=O)Nc2ccccn2)=C(O)c2sccc2S1(=O)=O NAME: tenoxicam '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CCCOC(=O)C1C(C2=C(CCCC2=O)N=C1C)C3=CC=CS3 NAME: '
               '2-methyl-5-oxo-4-thiophen-2-yl-4,6,7,8-tetrahydro-3H-quinoline-3-carboxylic '
               'acid propyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'C1=CC=C(C=C1)OC2=CC=C(C=C2)NC(=O)COC(=O)CCCSC3=NC4=CC=CC=C4N3 '
               'NAME: 4-(1H-benzimidazol-2-ylthio)butanoic acid '
               '[2-oxo-2-(4-phenoxyanilino)ethyl] ester REASON: WRONGLY '
               'CLASSIFIED Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CCOC(=O)C1=C(SC2=C1CCC2)NC(=S)NC(=O)C3=CC(=C(C=C3)OC)[N+](=O)[O-] '
               'NAME: '
               '2-[[[[(4-methoxy-3-nitrophenyl)-oxomethyl]amino]-sulfanylidenemethyl]amino]-5,6-dihydro-4H-cyclopenta[b]thiophene-3-carboxylic '
               'acid ethyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: COC(=O)C1=CC2=C(C=C1)N=C(S2)NC(=O)C3CCCCC3 NAME: '
               '2-[[cyclohexyl(oxo)methyl]amino]-1,3-benzothiazole-6-carboxylic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CC1=CC(=CC=C1)NC2=NN3C(=O)C4=CC=CC=C4N=C3S2 NAME: '
               '2-(3-methylanilino)-[1,3,4]thiadiazolo[2,3-b]quinazolin-5-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CSCC[C@@H](C(=O)O)NC(=O)C1=C(C=C(C=C1)NC[C@H](CS)N)C2=CC=CC=C2 '
               'NAME: '
               '(2S)-2-[[[4-[[(2R)-2-amino-3-mercaptopropyl]amino]-2-phenylphenyl]-oxomethyl]amino]-4-(methylthio)butanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CC1=CC(=NNC(=O)C2=CC=CS2)CC(C1)(C)C NAME: '
               'N-[(3,5,5-trimethyl-1-cyclohex-2-enylidene)amino]-2-thiophenecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: C1=CC=C2C=C(C=CC2=C1)SCCCCCCC(=O)NO NAME: '
               'N-hydroxy-7-(2-naphthalenylthio)heptanamide REASON: WRONGLY '
               'CLASSIFIED Molecule contains at least one organic sulfide '
               '(thioether) group (R–S–R bond)\n'
               ' * SMILES: CSCCC(N)C(=O)NO NAME: methioninehydroxamic acid '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'O.[C@@H]1(SC2=C(N3C([C@]([C@]3([C@H]2C)[H])([H])[C@@H](C)O)=O)C(O)=O)CN[C@@H](C1)CNS(N)(=O)=O '
               'NAME: Doripenem hydrate REASON: WRONGLY CLASSIFIED Molecule '
               'contains at least one organic sulfide (thioether) group (R–S–R '
               'bond)\n'
               ' * SMILES: '
               'CSc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               "NAME: 6-Methylthiopurine 5'-monophosphate ribonucleotide "
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CCC(C)(O)CC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O '
               'NAME: glucocleomin REASON: WRONGLY CLASSIFIED Molecule '
               'contains at least one organic sulfide (thioether) group (R–S–R '
               'bond)\n'
               ' * SMILES: COC(=O)C1=C(C=CS1)NC(=O)COC2=C(C=C(C=C2)F)Cl NAME: '
               '3-[[2-(2-chloro-4-fluorophenoxy)-1-oxoethyl]amino]-2-thiophenecarboxylic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CCOC(=O)C1=CC=CC=C1S(=O)(=O)N2CCN(CC2)C3=NC(=NC4=CC=CC=C43)C5=CC=CS5 '
               'NAME: '
               '2-[[4-(2-thiophen-2-yl-4-quinazolinyl)-1-piperazinyl]sulfonyl]benzoic '
               'acid ethyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CN1C2=C(C3=C1C(=O)N(N=C3)CC4=CC(=CC=C4)N)SC(=C2)S(=O)C NAME: '
               '6-[(3-aminophenyl)methyl]-4-methyl-2-methylsulfinyl-5-thieno[3,4]pyrrolo[1,3-d]pyridazinone '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CC(=O)NC(C(=O)OC)(C(F)(F)F)NC1=NC2=C(S1)C=C(C=C2)S(=O)(=O)C '
               'NAME: '
               '2-acetamido-3,3,3-trifluoro-2-[(6-methylsulfonyl-1,3-benzothiazol-2-yl)amino]propanoic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CCOC1=CC=C(C=C1)N2C=CN=C2SCC(=O)N3CCCC4=CC=CC=C43 '
               'NAME: '
               '1-(3,4-dihydro-2H-quinolin-1-yl)-2-[[1-(4-ethoxyphenyl)-2-imidazolyl]thio]ethanone '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: S1C(=N[C@@H](C1)CO)C2=C(O)C=3C(=CC=CC3)C(=C2)OC '
               'NAME: Karamomycin A REASON: WRONGLY CLASSIFIED Molecule '
               'contains at least one organic sulfide (thioether) group (R–S–R '
               'bond)\n'
               ' * SMILES: CC1=CSC(=N1)NC(=O)C2=C(C=C(C=C2)Cl)[N+](=O)[O-] '
               'NAME: 4-chloro-N-(4-methyl-2-thiazolyl)-2-nitrobenzamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CC1=CC=C(C=C1)CN2C=CC(=N2)C3=CN=C(S3)C4=CC=CC=C4 '
               'NAME: '
               '5-[1-[(4-methylphenyl)methyl]-3-pyrazolyl]-2-phenylthiazole '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: CCOC(=O)C1=CC2=C(N1CC(=O)NCCC3=CC=CC=C3)C=C(S2)C '
               'NAME: '
               '2-methyl-4-[2-oxo-2-(2-phenylethylamino)ethyl]-5-thieno[3,2-b]pyrrolecarboxylic '
               'acid ethyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'at least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: S(C(=O)C1=C(O)C(=C(O)C(=C1C)C)C)C NAME: '
               'Mortivinacin A REASON: WRONGLY CLASSIFIED Molecule contains at '
               'least one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: '
               'CC(=O)SC1CC2=CC(=O)CCC2(C3C1C4CCC5(C4(CC3)C)CCC(=O)O5)C NAME: '
               'ethanethioic acid '
               "S-(10,13-dimethyl-3,5'-dioxo-7-spiro[2,6,7,8,9,11,12,14,15,16-decahydro-1H-cyclopenta[a]phenanthrene-17,2'-oxolane]yl) "
               'ester REASON: WRONGLY CLASSIFIED Molecule contains at least '
               'one organic sulfide (thioether) group (R–S–R bond)\n'
               ' * SMILES: C1CCC(CC1)C2=NN=C(S2)NC(=O)C3=CC=CO3 NAME: '
               'N-(5-cyclohexyl-1,3,4-thiadiazol-2-yl)-2-furancarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains at least one '
               'organic sulfide (thioether) group (R–S–R bond)\n'
               'False negatives: SMILES: '
               '[H][C@@]12CCC3=C(SCCC(=O)NCCCCCC(=O)NCCCCCC(O)=O)C(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O '
               'NAME: '
               '6-(6-{3-[(progesterone-4-yl)thiopropionyl]aminohexanoyl}amino)hexanoic '
               'acid REASON: MISSED Molecule appears to be peptide-derived '
               '(contains multiple amide bonds)\n'
               ' * SMILES: S(C1=C(C=C(OC)C=C1)C(=O)NC)C=2C(=CC=CC2)C(=O)NC '
               'NAME: '
               'N1-methyl-5-methoxy-2-({2-[(methylamino)carbonyl]phenyl}thio)benzamide '
               'REASON: MISSED Molecule appears to be peptide-derived '
               '(contains multiple amide bonds)\n'
               ' * SMILES: OCC(NC=1N=C2N(C(C)C)C=NC2=C(N1)NCC3=CC=CC=C3)CC '
               'NAME: '
               '2-[[9-(1-Methylethyl)-6-[(phenylmethyl)amino]-9H-purin-2-yl]amino]-1-butanol '
               'REASON: MISSED No organic sulfide (R–S–R) moiety found in the '
               'molecule\n'
               ' * SMILES: '
               'C([C@H](NC(CC[C@@H](C(=O)O)N)=O)C(NCC(=O)O)=O)S[C@@H](\\C=C\\C=C\\CC(C/C=C\\CCCCC)=O)[C@H](O)CCCC(=O)O '
               'NAME: 11,12-dihydro-12-oxoleukotriene C4 REASON: MISSED '
               'Molecule appears to be peptide-derived (contains multiple '
               'amide bonds)\n'
               ' * SMILES: '
               'S(CC(NC(=O)CCC([NH3+])C([O-])=O)C(=O)NCC([O-])=O)/C(=N\\O)/CC1=CC=CC=C1 '
               'NAME: Phenylacetohydroximoyl-glutathione REASON: MISSED '
               'Molecule appears to be a free amino acid (not classified as '
               'organic sulfide)\n'
               ' * SMILES: '
               '[C@H]1([C@H]([C@H](CC1=O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)/C=C/[C@H](CCCCC)O)C/C=C\\CCCC(=O)O '
               'NAME: (S)-PGA2-S-glutathione conjugate REASON: MISSED Molecule '
               'appears to be peptide-derived (contains multiple amide bonds)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C(SCCC(=O)NCCCCCC(=O)NCCCCCC(=O)ON4C(=O)CCC4=O)C(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O '
               'NAME: 2,5-dioxo-1-pyrrolidinyl '
               '6-(6-{3-[(progesterone-4-yl)thiopropionyl]aminohexanoyl}amino)hexanoate '
               'REASON: MISSED Molecule appears to be peptide-derived '
               '(contains multiple amide bonds)\n'
               ' * SMILES: C=1(C=C(C=CC1O)NC(=O)C)SC[C@@H](C(O)=O)NC(=O)C '
               'NAME: S-(5-acetamido-2-hydroxyphenyl)-N-acetyl-L-cysteine '
               'REASON: MISSED Molecule appears to be peptide-derived '
               '(contains multiple amide bonds)\n'
               ' * SMILES: '
               'COC1CC(=O)Nc2c(O)c(CC\\C=C(C)/C(O)C(C)C(C\\C=C\\C=C\\C=C\\1)OC(=O)C(C)NC(=O)C1CCCCC1)cc(O)c2SC '
               'NAME: trierixin REASON: MISSED Molecule appears to be '
               'peptide-derived (contains multiple amide bonds)\n'
               ' * SMILES: '
               'N1(C2=C(C(=NC=N2)S)N=C1)[C@@H]3O[C@H](COP(O)(O)=O)[C@H]([C@H]3O)O '
               'NAME: 9-(5-phosphoribofuranosyl)-6-mercaptopurine REASON: '
               'MISSED No organic sulfide (R–S–R) moiety found in the '
               'molecule\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Molecule appears to be '
                                               'peptide-derived (contains '
                                               'multiple amide bonds)'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule appears to be '
                                               'peptide-derived (contains '
                                               'multiple amide bonds)'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Molecule appears to be '
                                               'peptide-derived (contains '
                                               'multiple amide bonds)'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No organic sulfide (R–S–R) '
                                               'moiety found in the molecule'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]12CCC3=C(SCCC(=O)NCCCCCC(=O)NCCCCCC(O)=O)C(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O',
                                      'name': '6-(6-{3-[(progesterone-4-yl)thiopropionyl]aminohexanoyl}amino)hexanoic '
                                              'acid',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'},
                                  {   'smiles': 'C1COCCN1C2=NC3=C(C(=N2)NCC4=NC5=CC=CC=C5N4)N=CN3C6=CSC=C6',
                                      'name': 'N-(1H-benzimidazol-2-ylmethyl)-2-(4-morpholinyl)-9-(3-thiophenyl)-6-purinamine',
                                      'reason': 'No organic sulfide (R–S–R) '
                                                'moiety found in the molecule'},
                                  {   'smiles': 'S(C1=C(C=C(OC)C=C1)C(=O)NC)C=2C(=CC=CC2)C(=O)NC',
                                      'name': 'N1-methyl-5-methoxy-2-({2-[(methylamino)carbonyl]phenyl}thio)benzamide',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'},
                                  {   'smiles': 'OCC(NC=1N=C2N(C(C)C)C=NC2=C(N1)NCC3=CC=CC=C3)CC',
                                      'name': '2-[[9-(1-Methylethyl)-6-[(phenylmethyl)amino]-9H-purin-2-yl]amino]-1-butanol',
                                      'reason': 'No organic sulfide (R–S–R) '
                                                'moiety found in the molecule'},
                                  {   'smiles': 'C([C@H](NC(CC[C@@H](C(=O)O)N)=O)C(NCC(=O)O)=O)S[C@@H](\\C=C\\C=C\\CC(C/C=C\\CCCCC)=O)[C@H](O)CCCC(=O)O',
                                      'name': '11,12-dihydro-12-oxoleukotriene '
                                              'C4',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'},
                                  {   'smiles': 'S(CC(NC(=O)CCC([NH3+])C([O-])=O)C(=O)NCC([O-])=O)/C(=N\\O)/CC1=CC=CC=C1',
                                      'name': 'Phenylacetohydroximoyl-glutathione',
                                      'reason': 'Molecule appears to be a free '
                                                'amino acid (not classified as '
                                                'organic sulfide)'},
                                  {   'smiles': '[C@H]1([C@H]([C@H](CC1=O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)/C=C/[C@H](CCCCC)O)C/C=C\\CCCC(=O)O',
                                      'name': '(S)-PGA2-S-glutathione '
                                              'conjugate',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'},
                                  {   'smiles': '[H][C@@]12CCC3=C(SCCC(=O)NCCCCCC(=O)NCCCCCC(=O)ON4C(=O)CCC4=O)C(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O',
                                      'name': '2,5-dioxo-1-pyrrolidinyl '
                                              '6-(6-{3-[(progesterone-4-yl)thiopropionyl]aminohexanoyl}amino)hexanoate',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'},
                                  {   'smiles': 'C=1(C=C(C=CC1O)NC(=O)C)SC[C@@H](C(O)=O)NC(=O)C',
                                      'name': 'S-(5-acetamido-2-hydroxyphenyl)-N-acetyl-L-cysteine',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'},
                                  {   'smiles': 'COC1CC(=O)Nc2c(O)c(CC\\C=C(C)/C(O)C(C)C(C\\C=C\\C=C\\C=C\\1)OC(=O)C(C)NC(=O)C1CCCCC1)cc(O)c2SC',
                                      'name': 'trierixin',
                                      'reason': 'Molecule appears to be '
                                                'peptide-derived (contains '
                                                'multiple amide bonds)'}],
    'attempt': 3,
    'reasoning': 'Below is one possible improved solution. In our reasoning we '
                 'noted that the previous approach “simply” iterated over all '
                 'S atoms meeting a degree‐2 condition and checking for two '
                 'carbon neighbors. Many false positives came from S atoms '
                 'that were in aromatic or fused systems (or had non‐single '
                 'bonds) or were part of peptide/ amino acid motifs. In the '
                 'revised code we\n'
                 '\n'
                 ' • First filter out very small molecules with an obvious '
                 'amino acid zwitterion and molecules with multiple amide '
                 'bonds (to avoid many peptide‑derived compounds).\n'
                 ' • Then for every sulfur atom we check that it is not '
                 'aromatic, has exactly two neighbors, and that each bond from '
                 'the S to its neighbor is single (to avoid assignments from '
                 'sulfoxides/sulfones or ring systems).\n'
                 ' • We also require that both substituents on the S are '
                 'carbons (thus two R groups, with R ≠ H).\n'
                 '\n'
                 'The code below implements these ideas.\n'
                 '\n'
                 'Below is the full Python code in one block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 517,
    'num_false_positives': 2770,
    'num_true_negatives': 138941,
    'num_false_negatives': 72,
    'num_negatives': None,
    'precision': 0.15728627928202008,
    'recall': 0.8777589134125636,
    'f1': 0.26676986584107326,
    'accuracy': 0.9800281096275474,
    'negative_predictive_value': 0.9994820628286563}