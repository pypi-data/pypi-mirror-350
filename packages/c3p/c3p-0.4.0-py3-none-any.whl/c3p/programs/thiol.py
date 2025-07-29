"""
Classifies: CHEBI:29256 thiol
"""
"""
Classifies: Thiol – An organosulfur compound in which a thiol group (-SH) 
is attached to a carbon atom of any aliphatic or aromatic moiety.
However, when the -SH is part of an amino acid/peptide backbone (e.g. in cysteine
or peptide sequences), it should not be classified as a simple thiol.
"""

from rdkit import Chem

def is_thiol(smiles: str):
    """
    Determines if a molecule is a (nonpeptidic) thiol based on its SMILES string.
    
    A thiol is defined as having at least one -SH group attached to a carbon where the 
    local environment does not suggest that the thiol is part of an amino acid or peptide 
    backbone. In particular, in many peptides (or free amino acids like cysteine/homocysteine)
    the -SH group is attached to a CH2 that is also (through its only neighbor) attached to a 
    chiral α-carbon that bears an amine and a carboxyl group.
    
    For each putative thiol group we:
      1. Look for a carbon attached to sulfur where the sulfur has exactly one hydrogen (when Hs are added).
      2. Check whether the CH2 (or CH) bonded to S is also attached to a carbon that looks like the 
         α–carbon of an amino acid (i.e. having a nitrogen and a carbonyl fragment connected).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if at least one -SH group is found on a carbon that is not in a peptide-like environment.
        str: Explanation / Reason for the classification.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Add explicit hydrogens so that the hydrogen on S becomes explicit.
    mol = Chem.AddHs(mol)
    
    # Define a SMARTS for a thiol group: a carbon (atomic number 6) bonded to an S that has exactly one H.
    # This is written as a bond from a carbon to an S with X2 (valence 2) that has one H.
    thiol_pattern = Chem.MolFromSmarts("[#6]-[S;X2&H1]")
    thiol_matches = mol.GetSubstructMatches(thiol_pattern)
    if not thiol_matches:
        return False, "No thiol group (-SH attached to a carbon) found in the molecule"

    # For each matching thiol group, check if its environment seems peptide‐like.
    # Heuristic: for the carbon that is directly bonded to S (let's call it C_thiol),
    # check its neighbors (other than the sulfur) to see if any look like amino acid alpha carbons.
    # Typical alpha-carbon in amino acids is bonded to (at least) one nitrogen and one carbon that carries a C=O.
    for match in thiol_matches:
        carbon_idx, sulfur_idx = match  # match gives (index_of_C, index_of_S)
        C_thiol = mol.GetAtomWithIdx(carbon_idx)
        is_peptide_env = False   # flag for this thiol group
        
        # Examine neighbors of the thiol-bearing carbon (except the sulfur itself).
        for nb in C_thiol.GetNeighbors():
            if nb.GetIdx() == sulfur_idx:
                continue
            # Only consider if the neighbor is another carbon atom (which could be the alpha–carbon)
            if nb.GetAtomicNum() == 6:
                # Check if this neighbor (potential α–carbon) has at least one nitrogen neighbor ...
                has_nitrogen = any(nbr.GetAtomicNum() == 7 for nbr in nb.GetNeighbors())
                # ... and at least one neighboring carbon that is double-bonded to an oxygen.
                has_carbonyl = False
                for second_nb in nb.GetNeighbors():
                    # Skip if second_nb is C_thiol to avoid looping back.
                    if second_nb.GetIdx() == C_thiol.GetIdx():
                        continue
                    if second_nb.GetAtomicNum() == 6:
                        # Check bonds on this carbon for a double bond to oxygen.
                        for bond in second_nb.GetBonds():
                            # bond order 2.0 indicates a double bond.
                            if bond.GetBondTypeAsDouble() == 2.0:
                                other = bond.GetOtherAtom(second_nb)
                                if other.GetAtomicNum() == 8:
                                    has_carbonyl = True
                                    break
                    if has_carbonyl:
                        break
                if has_nitrogen and has_carbonyl:
                    is_peptide_env = True
                    break  # one peptide-like environment is enough
                
        # If we found at least one thiol that is NOT in a peptide environment, classify as thiol.
        if not is_peptide_env:
            return True, "Molecule contains a thiol group (-SH) attached to a carbon atom outside a peptide backbone"
    
    # If every detected thiol group seems to be tied to an amino acid/peptide-like environment, do not classify.
    return False, "Thiols detected are associated with peptide backbones or amino acid environments, not classified as simple thiol compounds"


# Example usage (for testing purposes)
if __name__ == "__main__":
    # A few examples:
    test_molecules = {
        "2-Methoxybenzenethiol": "SC=1C(OC)=CC=CC1",
        "Cysteamine hydrochloride": "Cl.SCCN",
        "3-mercaptopyruvic acid": "OC(=O)C(=O)CS",
        "Arg-Cys-Asp (peptide example)": "SC[C@H](NC(=O)[C@@H](N)CCCN=C(N)N)C(=O)N[C@@H](CC(O)=O)C(O)=O"
    }
    
    for name, smi in test_molecules.items():
        result, reason = is_thiol(smi)
        print(f"{name}:\n  SMILES: {smi}\n  Classified as thiol? {result}\n  Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29256',
                          'name': 'thiol',
                          'definition': 'An organosulfur compound in which a '
                                        'thiol group, -SH, is attached to a '
                                        'carbon atom of any aliphatic or '
                                        'aromatic moiety.',
                          'parents': ['CHEBI:33261'],
                          'xrefs': ['KEGG:C00145', 'Wikipedia:Thiol'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 80,
                           'log_lines_of_code': 4.382026634673881,
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
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 8,
                                                 8,
                                                 9,
                                                 9,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 5,
                                                 4,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 9,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetOtherAtom',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'GetBondTypeAsDouble',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetBonds',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'items',
                                                 'AddHs',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['[#6]-[S;X2&H1]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_thiol(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No thiol group (-SH '
                                          'attached to a carbon) found in the '
                                          'molecule"',
                                          'True, "Molecule contains a thiol '
                                          'group (-SH) attached to a carbon '
                                          'atom outside a peptide backbone"',
                                          'False, "Thiols detected are '
                                          'associated with peptide backbones '
                                          'or amino acid environments, not '
                                          'classified as simple thiol '
                                          'compounds"'],
                           'returns_count': 4,
                           'complexity': 6.076405326934776},
    'message': '\n'
               'Attempt failed: F1 score of 0.13298222514812374 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O[C@](CN1N=CN=C1S)(C1=CC=C(F)C=C1F)C(F)(F)C1=CC=C(OC2=CC=C(C=C2)C#N)C=N1 '
               'NAME: (S)-fluoxytioconazole (thiol) REASON: CORRECT Molecule '
               'contains a thiol group (-SH) attached to a carbon atom outside '
               'a peptide backbone\n'
               ' * SMILES: '
               'CCC(C)[C@@H](CO[C@@H](CC1=CC=CC=C1)C(=O)N[C@@H](CCS(C)(=O)=O)C(=O)OC(C)C)NC[C@H](CS)N '
               'NAME: '
               '(2S)-2-[[(2S)-2-[(2S)-2-[[(2R)-2-amino-3-mercaptopropyl]amino]-3-methylpentoxy]-1-oxo-3-phenylpropyl]amino]-4-methylsulfonylbutanoic '
               'acid propan-2-yl ester REASON: CORRECT Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCS '
               'NAME: coenzyme A REASON: CORRECT Molecule contains a thiol '
               'group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: OC(=O)C(=O)CS NAME: 3-mercaptopyruvic acid REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: Cl.SCCN NAME: Cysteamine hydrochloride REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: C(CC(CCO)(S)C)C NAME: 3-methyl-3-sulfanylhexan-1-ol '
               'REASON: CORRECT Molecule contains a thiol group (-SH) attached '
               'to a carbon atom outside a peptide backbone\n'
               ' * SMILES: SC=1C(OC)=CC=CC1 NAME: 2-Methoxybenzenethiol '
               'REASON: CORRECT Molecule contains a thiol group (-SH) attached '
               'to a carbon atom outside a peptide backbone\n'
               ' * SMILES: SC1=C(C=CC=C1C)C NAME: 2,6-Dimethylbenzenethiol '
               'REASON: CORRECT Molecule contains a thiol group (-SH) attached '
               'to a carbon atom outside a peptide backbone\n'
               ' * SMILES: CN[C@@H](Cc1c(S)ncn1C)C(O)=O NAME: ovothiol B '
               'REASON: CORRECT Molecule contains a thiol group (-SH) attached '
               'to a carbon atom outside a peptide backbone\n'
               ' * SMILES: OCCS NAME: mercaptoethanol REASON: CORRECT Molecule '
               'contains a thiol group (-SH) attached to a carbon atom outside '
               'a peptide backbone\n'
               ' * SMILES: CCSCCS NAME: 2-(ethylsulfanyl)ethanethiol REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'O[C@@](CN1N=CN=C1S)(C1=CC=C(F)C=C1F)C(F)(F)C1=CC=C(OC2=CC=C(C=C2)C#N)C=N1 '
               'NAME: (R)-fluoxytioconazole (thiol) REASON: CORRECT Molecule '
               'contains a thiol group (-SH) attached to a carbon atom outside '
               'a peptide backbone\n'
               ' * SMILES: C[C@H](C(NC1=CC=CC=C1C(N[C@H](CCS)O)=O)=O)N NAME: '
               'fusarithioamide A REASON: CORRECT Molecule contains a thiol '
               'group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: CCCCC(S)CCCO NAME: 4-sulfanyloctan-1-ol REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: O[C@@H](CS)[C@@H](O)CS NAME: L-1,4-dithiothreitol '
               'REASON: CORRECT Molecule contains a thiol group (-SH) attached '
               'to a carbon atom outside a peptide backbone\n'
               ' * SMILES: OC(=O)C(CS)CS NAME: '
               '3-mercapto-2-mercaptomethylpropanoic acid REASON: CORRECT '
               'Molecule contains a thiol group (-SH) attached to a carbon '
               'atom outside a peptide backbone\n'
               ' * SMILES: C[C@H](O)[C@@H](S)P(O)(O)=O NAME: '
               '[(1R,2S)-2-hydroxy-1-thiopropyl]phosphonic acid REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: SCCCCCCCCS NAME: 1,8-Octanedithiol REASON: CORRECT '
               'Molecule contains a thiol group (-SH) attached to a carbon '
               'atom outside a peptide backbone\n'
               ' * SMILES: CC(C)(S)[C@H](C(O)=O)n1ccnc1Cc1ccccc1 NAME: '
               'benzylpenillamine REASON: CORRECT Molecule contains a thiol '
               'group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: SCCCS NAME: propane-1,3-dithiol REASON: CORRECT '
               'Molecule contains a thiol group (-SH) attached to a carbon '
               'atom outside a peptide backbone\n'
               ' * SMILES: SCC=C(C)C NAME: 3-Methyl-2-butene-1-thiol REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: SC1CCCC1 NAME: Cyclopentanethiol REASON: CORRECT '
               'Molecule contains a thiol group (-SH) attached to a carbon '
               'atom outside a peptide backbone\n'
               ' * SMILES: SC/C=C(/CCC=C(C)C)\\C NAME: thiogeraniol REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: CC(=O)CC(C)(C)S NAME: '
               '4-mercapto-4-methylpentan-2-one REASON: CORRECT Molecule '
               'contains a thiol group (-SH) attached to a carbon atom outside '
               'a peptide backbone\n'
               ' * SMILES: SC=1C(CC)=CC=CC1 NAME: 2-Ethylbenzenethiol REASON: '
               'CORRECT Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               'False positives: SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCCN=C(N)N)C(=O)N[C@@H](CC(O)=O)C(O)=O '
               'NAME: Arg-Cys-Asp REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: SC[C@H](N)C(=O)N[C@@H](CC(C)C)C(=O)NCC(O)=O NAME: '
               'Cys-Leu-Gly REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H]([C@H](O)C)C(O)=O '
               'NAME: Glu-Cys-Thr REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CCCN=C(N)N)C(O)=O '
               'NAME: Trp-Cys-Arg REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CO)C(O)=O '
               'NAME: Trp-Cys-Ser REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: SC[C@H](N)C(=O)NCC(=O)N[C@@H](CCC(=O)N)C(O)=O NAME: '
               'Cys-Gly-Gln REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC=3NC=NC3)C(O)=O '
               'NAME: Trp-His-Cys REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: NC(CCS)C(O)=O NAME: homocysteine REASON: WRONGLY '
               'CLASSIFIED Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCSC)C(=O)N[C@@H]([C@H](O)C)C(O)=O '
               'NAME: Met-Cys-Thr REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: SC[C@H](N)C(=O)N[C@@H](CC(O)=O)C(O)=O NAME: Cys-Asp '
               'REASON: WRONGLY CLASSIFIED Molecule contains a thiol group '
               '(-SH) attached to a carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCSC)C(=O)N[C@@H](C(C)C)C(O)=O NAME: '
               'Met-Cys-Val REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: S(O)(=O)(=O)CCC(N)CS NAME: '
               '3-Amino-4-sulfanylbutane-1-sulfonic acid REASON: WRONGLY '
               'CLASSIFIED Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)[C@H](CC)C)[C@H](CC)C)C(O)=O '
               'NAME: Ile-Ile-Cys REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCSC(=O)C(\\S)=C\\CC(O)=O '
               'NAME: (2Z)-4-carboxy-2-sulfanylbut-2-enoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CCC(=O)N)C(O)=O)CO NAME: '
               'Cys-Ser-Gln REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: SC[C@H](N)C(=O)N[C@@H]([C@@H](O)C)C(O)=O NAME: '
               'Cys-Thr REASON: WRONGLY CLASSIFIED Molecule contains a thiol '
               'group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: '
               'S(C([C@](N(C(=O)C([H])([H])[H])[H])(C(=O)N([H])[H])[H])([H])[H])[H] '
               'NAME: N-Acetylcysteine amide REASON: WRONGLY CLASSIFIED '
               'Molecule contains a thiol group (-SH) attached to a carbon '
               'atom outside a peptide backbone\n'
               ' * SMILES: [O-][n+]1ccccc1S NAME: pyridine-2-thiol N-oxide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a thiol group '
               '(-SH) attached to a carbon atom outside a peptide backbone\n'
               ' * SMILES: SCCC(O)C NAME: 4-Mercapto-2-butanol REASON: WRONGLY '
               'CLASSIFIED Molecule contains a thiol group (-SH) attached to a '
               'carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](CC(=O)N)C(O)=O '
               'NAME: Glu-Cys-Asn REASON: WRONGLY CLASSIFIED Molecule contains '
               'a thiol group (-SH) attached to a carbon atom outside a '
               'peptide backbone\n'
               ' * SMILES: SC[C@H](NC(=O)CNC(=O)[C@@H](N)CCCCN)C(O)=O NAME: '
               'Lys-Gly-Cys REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CO)C(O)=O NAME: '
               'Asp-Ser-Cys REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               ' * SMILES: '
               'SCC(N)C(=O)NC(CC(C)C)C(=O)NC(CC1=CC=CC=C1)C(=O)NC(CS)C(O)=O '
               'NAME: Cys-Leu-Phe-Cys REASON: WRONGLY CLASSIFIED Molecule '
               'contains a thiol group (-SH) attached to a carbon atom outside '
               'a peptide backbone\n'
               ' * SMILES: [O-]C(=O)CC(S)C([O-])=O NAME: 2-mercaptosuccinate '
               'REASON: WRONGLY CLASSIFIED Molecule contains a thiol group '
               '(-SH) attached to a carbon atom outside a peptide backbone\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)CO)C(O)=O NAME: '
               'His-Ser-Cys REASON: WRONGLY CLASSIFIED Molecule contains a '
               'thiol group (-SH) attached to a carbon atom outside a peptide '
               'backbone\n'
               'False negatives: SMILES: COC1=C(C=CC(=C1)SC)C(=O)NC2=CC=NC=C2 '
               'NAME: 2-methoxy-4-(methylthio)-N-pyridin-4-ylbenzamide REASON: '
               'MISSED No thiol group (-SH attached to a carbon) found in the '
               'molecule\n'
               ' * SMILES: COC1=C(C=CC(=C1)SC)C(=O)NC2=C(C=C(C=N2)Cl)Cl NAME: '
               'N-(3,5-dichloro-2-pyridinyl)-2-methoxy-4-(methylthio)benzamide '
               'REASON: MISSED No thiol group (-SH attached to a carbon) found '
               'in the molecule\n'
               ' * SMILES: C1=CC(=CC=C1C(=O)O)SCC2=CN=C(S2)Cl NAME: '
               '4-[(2-chloro-5-thiazolyl)methylthio]benzoic acid REASON: '
               'MISSED No thiol group (-SH attached to a carbon) found in the '
               'molecule\n'
               ' * SMILES: COC1=C(C=CC(=C1)SC)C(=O)N2CCCCCC2 NAME: '
               '1-azepanyl-[2-methoxy-4-(methylthio)phenyl]methanone REASON: '
               'MISSED No thiol group (-SH attached to a carbon) found in the '
               'molecule\n'
               ' * SMILES: '
               '[H][C@]12Nc3nc(N)[nH]c(=O)c3N[C@@]1([H])C1=C(S[Mo](O)(O)(O)S1)[C@@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)O2 '
               'NAME: Mo(V)-molybdopterin cytosine dinucleotide REASON: MISSED '
               'No thiol group (-SH attached to a carbon) found in the '
               'molecule\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No thiol group (-SH attached '
                                               'to a carbon) found in the '
                                               'molecule'}],
    'sample_false_negatives': [   {   'smiles': 'COC1=C(C=CC(=C1)SC)C(=O)NC2=CC=NC=C2',
                                      'name': '2-methoxy-4-(methylthio)-N-pyridin-4-ylbenzamide',
                                      'reason': 'No thiol group (-SH attached '
                                                'to a carbon) found in the '
                                                'molecule'},
                                  {   'smiles': 'COC1=C(C=CC(=C1)SC)C(=O)NC2=C(C=C(C=N2)Cl)Cl',
                                      'name': 'N-(3,5-dichloro-2-pyridinyl)-2-methoxy-4-(methylthio)benzamide',
                                      'reason': 'No thiol group (-SH attached '
                                                'to a carbon) found in the '
                                                'molecule'},
                                  {   'smiles': 'CC(C)(S)[C@H](C(O)=O)n1ccnc1Cc1ccccc1',
                                      'name': 'benzylpenillamine',
                                      'reason': 'Thiols detected are '
                                                'associated with peptide '
                                                'backbones or amino acid '
                                                'environments, not classified '
                                                'as simple thiol compounds'},
                                  {   'smiles': 'C1=CC(=CC=C1C(=O)O)SCC2=CN=C(S2)Cl',
                                      'name': '4-[(2-chloro-5-thiazolyl)methylthio]benzoic '
                                              'acid',
                                      'reason': 'No thiol group (-SH attached '
                                                'to a carbon) found in the '
                                                'molecule'},
                                  {   'smiles': 'COC(=O)[C@@H](N)CS',
                                      'name': 'methyl L-cysteinate',
                                      'reason': 'Thiols detected are '
                                                'associated with peptide '
                                                'backbones or amino acid '
                                                'environments, not classified '
                                                'as simple thiol compounds'},
                                  {   'smiles': 'CC(C)(S)C(N)C(O)=O',
                                      'name': 'penicillamine',
                                      'reason': 'Thiols detected are '
                                                'associated with peptide '
                                                'backbones or amino acid '
                                                'environments, not classified '
                                                'as simple thiol compounds'},
                                  {   'smiles': 'C=1C=CC=C2NC=C(C12)CCCC(N[C@H](C(=O)O)CS)=O',
                                      'name': 'N-[4-(indol-3-yl)butanoyl]-L-cysteine',
                                      'reason': 'Thiols detected are '
                                                'associated with peptide '
                                                'backbones or amino acid '
                                                'environments, not classified '
                                                'as simple thiol compounds'},
                                  {   'smiles': 'CC(=O)N[C@@H](CS)C(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'mycothiol',
                                      'reason': 'Thiols detected are '
                                                'associated with peptide '
                                                'backbones or amino acid '
                                                'environments, not classified '
                                                'as simple thiol compounds'},
                                  {   'smiles': 'COC1=C(C=CC(=C1)SC)C(=O)N2CCCCCC2',
                                      'name': '1-azepanyl-[2-methoxy-4-(methylthio)phenyl]methanone',
                                      'reason': 'No thiol group (-SH attached '
                                                'to a carbon) found in the '
                                                'molecule'},
                                  {   'smiles': 'N[C@@H](CCC(=O)N[C@@H](CS)C(=O)NCC(=O)O)C(=O)O',
                                      'name': 'glutathione',
                                      'reason': 'Thiols detected are '
                                                'associated with peptide '
                                                'backbones or amino acid '
                                                'environments, not classified '
                                                'as simple thiol compounds'}],
    'attempt': 2,
    'reasoning': 'We can try to improve the classifier by being more '
                 '“surgical” about which –SH is considered a “free” thiol '
                 'rather than one that belongs to a peptide (or amino acid) '
                 'backbone. One idea is to first add explicit hydrogens so '
                 'that a free –SH group shows up as a sulfur atom with exactly '
                 'one hydrogen (using a SMARTS like “[#6]-[S;X2&H1]”). Then, '
                 'for each matching pair (the carbon that bears the sulfur and '
                 'the sulfur itself), we examine the local environment of the '
                 'carbon. In many peptides (or free α‐amino acids such as '
                 'cysteine/homocysteine) the –SH is on a –CH2 group that is '
                 'directly attached to an α‐carbon with both an amine and a '
                 'carbonyl group. For example, in cysteine the –CH2–S–H is '
                 'attached to the chiral α‐carbon that has –NH2 and –COOH. (In '
                 'contrast, a nonpeptidic thiol such as cysteamine has two '
                 'carbons but the carbon next to –SH is not “decorated” with '
                 'both an amine and a carbonyl.) \n'
                 '\n'
                 'The following code implements one heuristic. For each thiol '
                 'match we look at the carbon attached to the S. For every '
                 'neighbor of that carbon (other than the S) we check if it '
                 'might be an amino acid α–carbon by (a) having at least one '
                 'nitrogen neighbor and (b) at least one neighbor (aside from '
                 'the thiol carbon) that is a carbon carrying a double‐bond to '
                 'oxygen. If any such connection is found, we classify that '
                 '–SH as “peptide‐associated” and do not count it. Only if at '
                 'least one –SH group is not “tethered” to an amino acid–like '
                 'environment do we report that the molecule is a '
                 '(nonpeptidic) thiol.\n'
                 '\n'
                 'Below is the complete Python code (in one block) using '
                 'rdkit.\n'
                 '\n'
                 '--------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 92,
    'num_false_positives': 215,
    'num_true_negatives': 141979,
    'num_false_negatives': 14,
    'num_negatives': None,
    'precision': 0.2996742671009772,
    'recall': 0.8679245283018868,
    'f1': 0.44552058111380155,
    'accuracy': 0.9983907238229094,
    'negative_predictive_value': 0.9999014035903179}