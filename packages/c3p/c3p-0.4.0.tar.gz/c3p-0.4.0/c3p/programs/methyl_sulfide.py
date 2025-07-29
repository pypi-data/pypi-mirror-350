"""
Classifies: CHEBI:86315 methyl sulfide
"""
"""
Classifies: Methyl Sulfide
Definition: Any aliphatic sulfide (i.e. non-aromatic thioether in which S is bonded via single bonds to two carbons)
in which at least one of the organyl groups attached to the sulfur is a methyl group.
Additional requirements: if only one substituent is methyl then the other must be aliphatic.
Molecules with 2 or more amide bonds (SMARTS "[NX3][CX3](=O)") are assumed to be peptides/biopolymers and are rejected.
"""
from rdkit import Chem

def is_methyl_sulfide(smiles: str):
    """
    Determines whether the input molecule is classified as a methyl sulfide.
    
    A methyl sulfide is defined as a molecule that contains at least one sulfur atom meeting the criteria:
      - The sulfur atom (atomic number 16) is non-aromatic.
      - It is bonded via two single bonds to carbon atoms only.
      - Among its two carbon substituents, at least one is a methyl group. Here a methyl group is defined as
          a non-aromatic carbon atom whose only heavy-atom neighbor is sulfur (degree==1) and that has exactly 3 hydrogens.
      - If only one substituent is a methyl group then the other substituent must be aliphatic (non–aromatic).
    Also, if two or more amide bonds are detected (via "[NX3][CX3](=O)"), the molecule is assumed to be a peptide/biopolymer.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        tuple (bool, str): (True, explanation) if the molecule is a methyl sulfide; (False, explanation) otherwise.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Exclude peptides/biopolymers: if molecule has 2 or more amide bonds, reject.
    amide_smarts = Chem.MolFromSmarts("[NX3][CX3](=O)")
    amide_matches = mol.GetSubstructMatches(amide_smarts)
    if len(amide_matches) >= 2:
        return False, f"Found {len(amide_matches)} amide bonds; likely a peptide or biopolymer"
    
    # Function to determine if a carbon atom qualifies as a methyl group.
    # A methyl group: non-aromatic, degree==1 (only bonded to the S) and exactly 3 attached hydrogens.
    def is_methyl(neigh):
        if neigh.GetAtomicNum() != 6:
            return False
        if neigh.GetIsAromatic():
            return False
        if neigh.GetDegree() != 1:
            return False
        if neigh.GetTotalNumHs() != 3:
            return False
        return True

    # Look for candidate sulfur atoms.
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 16:  # must be sulfur
            continue
        # Sulfur must be non-aromatic.
        if atom.GetIsAromatic():
            continue
        bonds = atom.GetBonds()
        if len(bonds) != 2:
            continue
        # All bonds to S must be single bonds.
        if not all(bond.GetBondType() == Chem.rdchem.BondType.SINGLE for bond in bonds):
            continue
        # Get the two neighboring atoms; they must both be carbons.
        neighbors = atom.GetNeighbors()
        if len(neighbors) != 2 or not all(neigh.GetAtomicNum() == 6 for neigh in neighbors):
            continue

        # Evaluate each neighbor.
        # Determine if each neighbor is methyl (methyl group) and whether it is aliphatic.
        # Note: any carbon not qualifying as methyl must be aliphatic (i.e. non-aromatic) to pass.
        n1, n2 = neighbors[0], neighbors[1]
        n1_is_methyl = is_methyl(n1)
        n2_is_methyl = is_methyl(n2)
        n1_aliphatic = not n1.GetIsAromatic()
        n2_aliphatic = not n2.GetIsAromatic()
        
        # Accept the candidate if:
        #   (a) both substituents are methyl, or
        #   (b) one is methyl and the other (non-methyl) is aliphatic.
        if n1_is_methyl and n2_is_methyl:
            return True, "Found two methyl substituents on a non-aromatic thioether sulfur"
        elif n1_is_methyl and n2_aliphatic:
            return True, "Found a methyl substituent and an aliphatic substituent on the thioether sulfur"
        elif n2_is_methyl and n1_aliphatic:
            return True, "Found a methyl substituent and an aliphatic substituent on the thioether sulfur"
        # Otherwise, do not classify this sulfur as a valid methyl sulfide substructure.
        
    return False, "No appropriate aliphatic methyl thioether substructure found"


# Example usage: running some of the test cases provided.
if __name__ == "__main__":
    tests = [
        # True positives
        ("C(S)(=NO)CCCCCCCCSC", "9-[(methylthio)nonyl]thiohydroximic acid"),
        ("CSCC(=O)[C@H](O)[C@H](O)COP(O)(O)=O", "1-(methylthio)ribulose 5-phosphate"),
        ("S(CCCCCCCCN=C=S)C", "8-(methylthio)octylisothiocyanate"),
        ("CSc1ncncn1", "2-(methylthio)-1,3,5-triazine"),
        ("O=C(O)[C@@H](NO)CCCCCSC", "N-hydroxy-L-trihomomethionine"),
        ("CSc1nc(NC(C)C)nc(NC(C)C)n1", "promethin"),
        ("CSC(CC(N)C(O)=O)C(O)=O", "gamma-thiomethyl glutamate"),
        ("CSC[C@H]1O[C@H](O)[C@H](O)[C@@H]1O", "5-S-methyl-5-thio-alpha-D-ribofuranose"),
        ("CSC[C@H](NC(C)=O)C(O)=O", "N-acetyl-S-methyl-L-cysteine"),
        ("C(\\CCCCCCCCSC)=N/O", "(E)-9-(methylsulfanyl)nonanal oxime"),
        ("CSCC1=NC2=C(NC1=O)[C@@H](C)C1(C(=O)N(C)C3=C1C=CC=C3)C1=C2C(=O)CC1", "maremycin G"),
        ("CSCCCC(=O)C(O)=O", "5-methylthio-2-oxopentanoic acid"),
        ("O=C(O)[C@@H](N(O)O)CCCCSC", "N,N-dihydroxy-L-dihomomethionine"),
        ("S(CCCCCCN=C=S)C", "1-isothiocyanato-6-(methylsulfanyl)hexane"),
        ("CNC(=O)OC1=CC(C)=C(SC)C(C)=C1", "methiocarb"),
        ("C1=C(C=CC(=C1)C[C@@H](C(O)=O)OCC)OCCN2C(=CC=C2C)C=3C=CC(=CC3)SC", "saroglitazar"),
        ("C(\\CCCCCCCSC)=N/O", "(E)-8-(methylsulfanyl)octanal oxime"),
        ("[H]C(=NO)C(C)(C)SC", "2-methyl-2-(methylsulfanyl)propanal oxime"),
        ("O=C(O)[C@@H](N)CCCCCCSC", "L-tetrahomomethionine"),
        ("CCCCOC(CSC)=O", "butyl 2-(methylsulfanyl)acetate"),
        ("CSCC(O)=O", "(methylthio)acetic acid"),
        ("C(CCCCSC)=NO", "5-(methylsulfanyl)pentanal oxime"),
        # False positives (should be rejected)
        ("CSc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O", "6-methylthioinosine"),
        ("CC1=CC(=C(S1)SC)C2C(=C(N(C3=C2C(=O)CCC3)C4=CN=CC=C4)N)C#N", "2-amino-4-[5-methyl-2-(methylthio)-3-thiophenyl]-5-oxo-1-(3-pyridinyl)-4,6,7,8-tetrahydroquinoline-3-carbonitrile"),
        ("S(CCSC)C(SC)CC", "1-(Methylthio)propyl propyl disulfide"),
        ("CN1C(=O)C(=C(N=C1SC)C2=CC=C(C=C2)Cl)C#N", "4-(4-chlorophenyl)-1-methyl-2-(methylthio)-6-oxo-5-pyrimidinecarbonitrile"),
        ("S(C=1C=2C(N=C(C1)C)=CC=CC2)C", "2-Methyl-4-(methylthio)quinoline"),
        ("CCCN(CCC)S(=O)(=O)C1=CC=C(C=C1)C(=O)NC2=NN=C(O2)CSC", "4-(dipropylsulfamoyl)-N-[5-[(methylthio)methyl]-1,3,4-oxadiazol-2-yl]benzamide"),
        ("CCC1=CC=C(C=C1)C(=O)NC(CCSC)C(=O)OC", "2-[[(4-ethylphenyl)-oxomethyl]amino]-4-(methylthio)butanoic acid methyl ester"),
        ("CNC(=O)O\\N=C(\\C)C(C)SC", "butocarboxim"),
        ("S(C/C(=C/C)/C=O)C", "2-[(Methylthio)methyl]-2-butenal"),
        ("CSCC[C@H](NC([O-])=O)C([O-])=O", "N-carboxy-L-methionine(2-)"),
        ("CSC1=CC=CC=C1C(=O)C2CCCN(C2)C(=O)C3=CSN=N3", "[2-(methylthio)phenyl]-[1-[oxo(4-thiadiazolyl)methyl]-3-piperidinyl]methanone"),
        ("CSCC[C@H](NC(=O)CC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3[C@@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C)C(O)=O", "methioninoursodeoxycholic acid"),
        ("OC(CSC1=C2C(C=C(C3=CC=C(SC)C=C3)S2)=NC=N1)=O", "({6-[4-(methylsulfanyl)phenyl]thieno[3,2-d]pyrimidin-4-yl}sulfanyl)acetic acid"),
        ("CCCOP(=O)(OCCC)Oc1ccc(SC)cc1", "propaphos"),
        ("ClC(C(NC(=O)[C@H]1NC[C@@H](C1)CCC)[C@H]2O[C@H](SC)[C@H](O)[C@H]([C@H]2O)O)C", "1'-Demethylclindamycin"),
        ("CSC([C@H]([NH3+])C([O-])=O)C([O-])=O", "3-methylthioaspartate(1-)"),
        ("CSC1=CC=CC(=C1)NC(=S)N2CCCN(C2)CC3=CC=CC=C3F", "3-[(2-fluorophenyl)methyl]-N-[3-(methylthio)phenyl]-1,3-diazinane-1-carbothioamide"),
        ("C(O)C(=O)CCSC", "1-hydroxy-4-(methythio)butan-2-one"),
        ("CSCCCCCCCC([NH3+])C([O-])=O", "pentahomomethionine zwitterion"),
        ("CSCC[C@@H](N)C(O)=O", "D-methionine"),
        ("COC1=C(C=C(C=C1)C=C2C(=O)SC(=N2)SC)OC", "4-[(3,4-dimethoxyphenyl)methylidene]-2-(methylthio)-5-thiazolone"),
        ("S(CC([C@H]([C@@H](COP(=O)([O-])[O-])O)O)=O)C", "1-methylthio-D-xylulose 5-phosphate(2-)"),
        ("CSC(=S)NCc1c[nH]c2ccccc12", "brassinin"),
        ("O=C([O-])[C@@H](N(O)O)CCCCCCCCSC", "N,N-dihydroxy-L-hexahomomethioninate"),
        ("S(C=1C=C2OC(=O)C(=C2C=CC1)C=3C4=C(C=CC=C4)NC3)C", "Roseobacticide C")
    ]
    
    for s, name in tests:
        result, reason = is_methyl_sulfide(s)
        print(f"SMILES: {s}\nNAME: {name}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:86315',
                          'name': 'methyl sulfide',
                          'definition': 'Any aliphatic sulfide in which at '
                                        'least one of the organyl groups '
                                        'attached to the sulfur is a methyl '
                                        'group.',
                          'parents': ['CHEBI:16385'],
                          'xrefs': ['MetaCyc:Methyl-thioethers'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 106,
                           'log_lines_of_code': 4.663439094112067,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 0,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetTotalNumHs',
                                                 'GetBondType',
                                                 'GetDegree',
                                                 'GetIsAromatic',
                                                 'GetBonds',
                                                 'MolFromSmarts',
                                                 'GetAtoms',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'GetNeighbors',
                                                 'MolFromSmiles'],
                           'methods_called_count': 11,
                           'smarts_strings': ['[NX3][CX3](=O)'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_methyl_sulfide(smiles: str):',
                                       'is_methyl(neigh):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Found {len(amide_matches)} '
                                          'amide bonds; likely a peptide or '
                                          'biopolymer"',
                                          'False',
                                          'False',
                                          'False',
                                          'False',
                                          'True',
                                          'False, "No appropriate aliphatic '
                                          'methyl thioether substructure '
                                          'found"'],
                           'returns_count': 8,
                           'complexity': 5.732687818822414},
    'message': '\n'
               'Attempt failed: F1 score of 0.1903409090909091 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C(S)(=NO)CCCCCCCCSC NAME: '
               '9-[(methylthio)nonyl]thiohydroximic acid REASON: CORRECT Found '
               'a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSCC(=O)[C@H](O)[C@H](O)COP(O)(O)=O NAME: '
               '1-(methylthio)ribulose 5-phosphate REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: S(CCCCCCCCN=C=S)C NAME: '
               '8-(methylthio)octylisothiocyanate REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSc1ncncn1 NAME: 2-(methylthio)-1,3,5-triazine '
               'REASON: CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: O=C(O)[C@@H](NO)CCCCCSC NAME: '
               'N-hydroxy-L-trihomomethionine REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSc1nc(NC(C)C)nc(NC(C)C)n1 NAME: prometryn REASON: '
               'CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: CSC(CC(N)C(O)=O)C(O)=O NAME: gamma-thiomethyl '
               'glutamate REASON: CORRECT Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: CSC[C@H]1O[C@H](O)[C@H](O)[C@@H]1O NAME: '
               '5-S-methyl-5-thio-alpha-D-ribofuranose REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSC[C@H](NC(C)=O)C(O)=O NAME: '
               'N-acetyl-S-methyl-L-cysteine REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: C(\\CCCCCCCCSC)=N/O NAME: '
               '(E)-9-(methylsulfanyl)nonanal oxime REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: '
               'CSCC1=NC2=C(NC1=O)[C@@H](C)C1(C(=O)N(C)C3=C1C=CC=C3)C1=C2C(=O)CC1 '
               'NAME: maremycin G REASON: CORRECT Found a non-aromatic '
               'thioether with a methyl substituent\n'
               ' * SMILES: CSCCCC(=O)C(O)=O NAME: 5-methylthio-2-oxopentanoic '
               'acid REASON: CORRECT Found a non-aromatic thioether with a '
               'methyl substituent\n'
               ' * SMILES: O=C(O)[C@@H](N(O)O)CCCCSC NAME: '
               'N,N-dihydroxy-L-dihomomethionine REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: S(CCCCCCN=C=S)C NAME: '
               '1-isothiocyanato-6-(methylsulfanyl)hexane REASON: CORRECT '
               'Found a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CNC(=O)OC1=CC(C)=C(SC)C(C)=C1 NAME: methiocarb '
               'REASON: CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: '
               'C1=C(C=CC(=C1)C[C@@H](C(O)=O)OCC)OCCN2C(=CC=C2C)C=3C=CC(=CC3)SC '
               'NAME: saroglitazar REASON: CORRECT Found a non-aromatic '
               'thioether with a methyl substituent\n'
               ' * SMILES: C(\\CCCCCCCSC)=N/O NAME: '
               '(E)-8-(methylsulfanyl)octanal oxime REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: [H]C(=NO)C(C)(C)SC NAME: '
               '2-methyl-2-(methylsulfanyl)propanal oxime REASON: CORRECT '
               'Found a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: O=C(O)[C@@H](N)CCCCCCSC NAME: L-tetrahomomethionine '
               'REASON: CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: CCCCOC(CSC)=O NAME: butyl 2-(methylsulfanyl)acetate '
               'REASON: CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: CSCC(O)=O NAME: (methylthio)acetic acid REASON: '
               'CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: C(CCCCSC)=NO NAME: 5-(methylsulfanyl)pentanal oxime '
               'REASON: CORRECT Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: CSCCCC(O)(CC(O)=O)C(O)=O NAME: '
               '2-(3-methylthiopropyl)malic acid REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: C(#[N+][O-])CCCCCSC NAME: '
               '6-(methylthio)hexanonitrile oxide REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: C(\\CCCCCSC)=N/O NAME: '
               '(E)-6-(methylsulfanyl)hexanal oxime REASON: CORRECT Found a '
               'non-aromatic thioether with a methyl substituent\n'
               'False positives: SMILES: '
               'CSc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O NAME: '
               '6-methylthioinosine REASON: WRONGLY CLASSIFIED Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: '
               'CC1=CC(=C(S1)SC)C2C(=C(N(C3=C2C(=O)CCC3)C4=CN=CC=C4)N)C#N '
               'NAME: '
               '2-amino-4-[5-methyl-2-(methylthio)-3-thiophenyl]-5-oxo-1-(3-pyridinyl)-4,6,7,8-tetrahydroquinoline-3-carbonitrile '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: S(SCCC)C(SC)CC NAME: 1-(Methylthio)propyl propyl '
               'disulfide REASON: WRONGLY CLASSIFIED Found a non-aromatic '
               'thioether with a methyl substituent\n'
               ' * SMILES: CN1C(=O)C(=C(N=C1SC)C2=CC=C(C=C2)Cl)C#N NAME: '
               '4-(4-chlorophenyl)-1-methyl-2-(methylthio)-6-oxo-5-pyrimidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: S(C=1C=2C(N=C(C1)C)=CC=CC2)C NAME: '
               '2-Methyl-4-(methylthio)quinoline REASON: WRONGLY CLASSIFIED '
               'Found a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CCCN(CCC)S(=O)(=O)C1=CC=C(C=C1)C(=O)NC2=NN=C(O2)CSC '
               'NAME: '
               '4-(dipropylsulfamoyl)-N-[5-[(methylthio)methyl]-1,3,4-oxadiazol-2-yl]benzamide '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: CCC1=CC=C(C=C1)C(=O)NC(CCSC)C(=O)OC NAME: '
               '2-[[(4-ethylphenyl)-oxomethyl]amino]-4-(methylthio)butanoic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CNC(=O)O\\N=C(\\C)C(C)SC NAME: butocarboxim REASON: '
               'WRONGLY CLASSIFIED Found a non-aromatic thioether with a '
               'methyl substituent\n'
               ' * SMILES: S(C/C(=C/C)/C=O)C NAME: '
               '2-[(Methylthio)methyl]-2-butenal REASON: WRONGLY CLASSIFIED '
               'Found a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSCC[C@H](NC([O-])=O)C([O-])=O NAME: '
               'N-carboxy-L-methionine(2-) REASON: WRONGLY CLASSIFIED Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSC1=CC=CC=C1C(=O)C2CCCN(C2)C(=O)C3=CSN=N3 NAME: '
               '[2-(methylthio)phenyl]-[1-[oxo(4-thiadiazolyl)methyl]-3-piperidinyl]methanone '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: '
               'CSCC[C@H](NC(=O)CC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3[C@@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C)C(O)=O '
               'NAME: methioninoursodeoxycholic acid REASON: WRONGLY '
               'CLASSIFIED Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: OC(CSC1=C2C(C=C(C3=CC=C(SC)C=C3)S2)=NC=N1)=O NAME: '
               '({6-[4-(methylsulfanyl)phenyl]thieno[3,2-d]pyrimidin-4-yl}sulfanyl)acetic '
               'acid REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether '
               'with a methyl substituent\n'
               ' * SMILES: CCCOP(=O)(OCCC)Oc1ccc(SC)cc1 NAME: propaphos '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: '
               'ClC(C(NC(=O)[C@H]1NC[C@@H](C1)CCC)[C@H]2O[C@H](SC)[C@H](O)[C@H]([C@H]2O)O)C '
               "NAME: 1'-Demethylclindamycin REASON: WRONGLY CLASSIFIED Found "
               'a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSC([C@H]([NH3+])C([O-])=O)C([O-])=O NAME: '
               '3-methylthioaspartate(1-) REASON: WRONGLY CLASSIFIED Found a '
               'non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSC1=CC=CC(=C1)NC(=S)N2CCCN(C2)CC3=CC=CC=C3F NAME: '
               '3-[(2-fluorophenyl)methyl]-N-[3-(methylthio)phenyl]-1,3-diazinane-1-carbothioamide '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: C(O)C(=O)CCSC NAME: '
               '1-hydroxy-4-(methythio)butan-2-one REASON: WRONGLY CLASSIFIED '
               'Found a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSCCCCCCCC([NH3+])C([O-])=O NAME: '
               'pentahomomethionine zwitterion REASON: WRONGLY CLASSIFIED '
               'Found a non-aromatic thioether with a methyl substituent\n'
               ' * SMILES: CSCC[C@@H](N)C(O)=O NAME: D-methionine REASON: '
               'WRONGLY CLASSIFIED Found a non-aromatic thioether with a '
               'methyl substituent\n'
               ' * SMILES: COC1=C(C=C(C=C1)C=C2C(=O)SC(=N2)SC)OC NAME: '
               '4-[(3,4-dimethoxyphenyl)methylidene]-2-(methylthio)-5-thiazolone '
               'REASON: WRONGLY CLASSIFIED Found a non-aromatic thioether with '
               'a methyl substituent\n'
               ' * SMILES: S(CC([C@H]([C@@H](COP(=O)([O-])[O-])O)O)=O)C NAME: '
               '1-methylthio-D-xylulose 5-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: CSC(=S)NCc1c[nH]c2ccccc12 NAME: brassinin REASON: '
               'WRONGLY CLASSIFIED Found a non-aromatic thioether with a '
               'methyl substituent\n'
               ' * SMILES: O=C([O-])[C@@H](N(O)O)CCCCCCCCSC NAME: '
               'N,N-dihydroxy-L-hexahomomethioninate REASON: WRONGLY '
               'CLASSIFIED Found a non-aromatic thioether with a methyl '
               'substituent\n'
               ' * SMILES: S(C=1C=C2OC(=O)C(=C2C=CC1)C=3C4=C(C=CC=C4)NC3)C '
               'NAME: Roseobacticide C REASON: WRONGLY CLASSIFIED Found a '
               'non-aromatic thioether with a methyl substituent\n'
               'False negatives: SMILES: '
               'CSc1nsc(SC)c1C(=O)NC(=O)NNc1ccc(F)c(Cl)c1 NAME: '
               'N-{[2-(3-chloro-4-fluorophenyl)hydrazino]carbonyl}-3,5-bis(methylthio)isothiazole-4-carboxamide '
               'REASON: MISSED Found 3 amide bonds; likely a peptide or '
               'biopolymer\n'
               ' * SMILES: OC([C@H](CCC(N[C@H](C(NCC(O)=O)=O)CSC)=O)N)=O NAME: '
               'S-methylglutathione REASON: MISSED Found 2 amide bonds; likely '
               'a peptide or biopolymer\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Found 2 amide bonds; likely a '
                                               'peptide or biopolymer'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Found 4 amide bonds; likely a '
                                               'peptide or biopolymer'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No appropriate aliphatic '
                                               'methyl thioether substructure '
                                               'found'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Found 9 amide bonds; likely a '
                                               'peptide or biopolymer'}],
    'sample_false_negatives': [   {   'smiles': 'CSc1ncncn1',
                                      'name': '2-(methylthio)-1,3,5-triazine',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'CSc1nc(NC(C)C)nc(NC(C)C)n1',
                                      'name': 'prometryn',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'CNC(=O)OC1=CC(C)=C(SC)C(C)=C1',
                                      'name': 'methiocarb',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'C1=C(C=CC(=C1)C[C@@H](C(O)=O)OCC)OCCN2C(=CC=C2C)C=3C=CC(=CC3)SC',
                                      'name': 'saroglitazar',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'CSc1nsc(SC)c1C(=O)NC(=O)NNc1ccc(F)c(Cl)c1',
                                      'name': 'N-{[2-(3-chloro-4-fluorophenyl)hydrazino]carbonyl}-3,5-bis(methylthio)isothiazole-4-carboxamide',
                                      'reason': 'Found 3 amide bonds; likely a '
                                                'peptide or biopolymer'},
                                  {   'smiles': 'CSc1nc2ccccc2s1',
                                      'name': '2-methylthio-1,3-benzothiazole',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'CSC1=C(C)C=C(OC(=O)NCCC(O)=O)C=C1C',
                                      'name': 'MXNP',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'CC(C)C1=NC(=NC(=N1)C2=CC=CC=C2)SC',
                                      'name': '2-(methylthio)-4-phenyl-6-propan-2-yl-1,3,5-triazine',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': '[N+](C)([C@H](C(=O)[O-])CC=1NC(SC)=NC1)(C)C',
                                      'name': 'S-methyl-L-ergothioneine',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'},
                                  {   'smiles': 'CSC1=CC=C(C)O1',
                                      'name': '2-methyl-5-(methylthio)furan',
                                      'reason': 'No appropriate aliphatic '
                                                'methyl thioether substructure '
                                                'found'}],
    'attempt': 4,
    'reasoning': 'Below is our reasoning.\n'
                 '\n'
                 'We noticed that the previous code “found” the –S–CH₃ '
                 'substructure even when the sulfur’s other substituent was '
                 'part of a heterocycle (or other aromatic system). In other '
                 'words, if one neighbor was methyl and the other neighbor was '
                 'aromatic the check mistakenly “skipped” the aromatic '
                 'neighbor (because it was “continued” within the loop) so '
                 'that candidate was accepted. In our improved version we '
                 'first get both neighbors, then (a) require that both '
                 'neighbors are carbons and (b) check separately whether each '
                 'qualifies as a methyl group (“methyl” meaning a non‐aromatic '
                 'carbon with degree == 1 and three hydrogens). If both '
                 'neighbors are methyl we accept, and if only one is methyl '
                 'then the other must be aliphatic (i.e. non–aromatic). In '
                 'addition we keep the amide bond check to help avoid peptides '
                 'or biopolymers. \n'
                 '\n'
                 'Below is the complete updated Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 55,
    'num_false_positives': 404,
    'num_true_negatives': 141827,
    'num_false_negatives': 14,
    'num_negatives': None,
    'precision': 0.11982570806100218,
    'recall': 0.7971014492753623,
    'f1': 0.20833333333333334,
    'accuracy': 0.997062543921293,
    'negative_predictive_value': 0.9999012979321916}