"""
Classifies: CHEBI:15841 polypeptide
"""
from rdkit import Chem
from rdkit.Chem import rdchem

def is_polypeptide(smiles: str):
    """
    Determines if a molecule is a polypeptide based on its SMILES string.
    A polypeptide is defined as a peptide containing ten or more amino acid residues.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polypeptide, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate a list of common amino acid SMILES patterns to identify amino acids in a polypeptide
    # These are simplified, representative substructures of amino acids at the amine or carboxyl terminus.
    amino_acid_patterns = [
        Chem.MolFromSmarts('[NX3][CX4](C)C=O'),  # Glycine pattern, extends to other amino acids with similar backbone
        Chem.MolFromSmarts('[NX3][CX4H2]CC=O'),  # Alanine pattern
        Chem.MolFromSmarts('[NX3][CX4](CC)[CX3](=O)'),  # Random extended pattern to cover potential modifications
        # Add more patterns or variations for common and modified amino acids
    ]

    # Function to match and count amino acid patterns in the given molecule
    num_amino_acids = 0
    for pattern in amino_acid_patterns:
        matches = mol.GetSubstructMatches(pattern)
        num_amino_acids += len(matches)

    # Consider each peptide bond (represented correctly) represents two amino acids, adjust as necessary
    # This is a simplification, real molecules may need closer inspection
    # Typically each peptide bond implies the presences of two amino acids in chain, so half the simple counts
    if num_amino_acids / 2 >= 10:
        return True, f"Contains approximately {num_amino_acids // 2} amino acid residues, classifying as polypeptide"
    else:
        return False, f"Contains approximately {num_amino_acids // 2} amino acid residues, not enough for a polypeptide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15841',
                          'name': 'polypeptide',
                          'definition': 'A peptide containing ten or more '
                                        'amino acid residues.',
                          'parents': ['CHEBI:16670', 'CHEBI:33839'],
                          'xrefs': ['KEGG:C00403'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 33,
                           'log_lines_of_code': 3.4965075614664802,
                           'indent_by_line': [   1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[NX3][CX4H2]CC=O',
                                                 '[NX3][CX4](CC)[CX3](=O)',
                                                 '[NX3][CX4](C)C=O'],
                           'smarts_strings_count': 3,
                           'defs': ['is_polypeptide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, f"Contains approximately '
                                          '{num_amino_acids // 2} amino acid '
                                          'residues, classifying as '
                                          'polypeptide"',
                                          'False, f"Contains approximately '
                                          '{num_amino_acids // 2} amino acid '
                                          'residues, not enough for a '
                                          'polypeptide"'],
                           'returns_count': 3,
                           'complexity': 2.499301512293296},
    'message': '\n'
               'Attempt failed: F1 score of 0.3745064861816131 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC[C@H](C)[C@H](N)C1=N[C@@H](CS1)C(=O)N[C@@H](CC(C)C)C(=O)N[C@H](CCC(O)=O)C(=O)N[C@@H]([C@@H](C)CC)C(=O)N[C@H]1CCCCNC(=O)[C@H](CC(N)=O)NC(=O)[C@@H](CC(O)=O)NC(=O)[C@H](Cc2c[nH]cn2)NC(=O)[C@@H](Cc2ccccc2)NC(=O)[C@@H](NC(=O)[C@@H](CCCN)NC1=O)[C@@H](C)CC '
               'NAME: bacitracin A REASON: CORRECT Contains 12 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)(C)C)CCC(=O)N)(CC)C)C(C)C)(C)C)(C)C)(C)C '
               'NAME: Trichovirin II 3a REASON: CORRECT Contains 20 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N2[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](CC(N[C@H](C(N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1CCC(=O)N)=O)CC(C)C)=O)CCOC(=O)N)=O)C(O)C(C)C)=O)[C@@H](CC)C)=O)CCCCC)[C@H](O)C)CC3=CC=C(O)C=C3)CCC2)C(C)C)C(O)CO)[C@H](CC)C)C '
               'NAME: Heinamide B3 REASON: CORRECT Contains 14 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'CSCC[C@H](NC(=O)[C@H](Cc1c[nH]c2ccccc12)NC(=O)CNC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](C)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](Cc1c[nH]c2ccccc12)NC(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCCCN)NC(=O)[C@H](CCCCN)NC(=O)[C@H](CO)NC(=O)[C@@H]1CCCN1C(=O)[C@H](CC(O)=O)NC(=O)[C@H](C)NC(=O)[C@@H](NC(=O)[C@H](CC(C)C)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@@H]1CCCN1C(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CC(C)C)NC(=O)[C@@H](N)CCC(N)=O)C(C)C)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](Cc1ccccc1)C(O)=O '
               'NAME: gastrin-34 REASON: CORRECT Contains 36 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(CC)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)(C)C)(CC)C)CCC(=O)N)C(C)C)C(C)C)(C)C)CC(C)C)(C)C '
               'NAME: Trichorzin HA-7 REASON: CORRECT Contains 20 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'S(CC[C@@H]1NC(=O)[C@H](NC(=O)[C@@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC([C@@H](NC([C@H](NC([C@@H](NC([C@@H](NC([C@H](NC([C@@H](NC1=O)C(C)C)=O)[C@H](O)C)=O)C(CC)C)=O)[C@@H](O)C)=O)C(C)C)=O)C(C)C)=O)C(C)C)CC2=CC=CC=C2)C(C)C)=C/C)CCCN=C(N)N)CC3=CC=C(O)C=C3)C '
               'NAME: Tolybybetaidin B REASON: CORRECT Contains 13 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(NCC(=O)N[C@H](C(=O)N[C@H](CO)CC(C)C)[C@H](CC)C)C(NC(=O)[C@@H](NC(=O)CNC(=O)CNC(=O)C(NC(=O)[C@@H](NC(=O)CNC(=O)C(NC(=O)CCCCCCC)(C)C)CC(C)C)(C)C)CC(C)C)(C)C '
               'NAME: Trichogin A IV REASON: CORRECT Contains 11 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC=O)CC(C)C)C)CC(C)C)C(C)C)CC1=CC=C(O)C=C1)CC(C)C)C(C)C)[C@H](O)C)C(C)C)CC(C)C)C(C)C)CO)CC(C)C)C(C)C)C(C)C '
               'NAME: Kolobetain A REASON: CORRECT Contains 15 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)C)CCC(=O)N)(C)C)C(C)C)(C)C)(CC)C)(C)C '
               'NAME: Trichovirin II 2a REASON: CORRECT Contains 20 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(NCCCC(NC(=O)/C=C\\CCCCCCCC)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(=O)N)C(O)C(=O)N)CCNC(=O)C(N)C(O)C)C(O)C)N '
               'NAME: Rotihibin D REASON: CORRECT Contains 10 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1[C@H](C(=O)N[C@H](C(=O)N[C@H](CO)C)CCC(=O)N)CCC1)C(NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@@H](NC(=O)C)CC=2C3=C(C=CC=C3)NC2)(C)C)(C)C)CC(C)C)C(C)C)CCC(=O)N)(C)C)(C)C)(C)C)CCC(=O)N)CC(C)C)(C)C '
               'NAME: Chrysaibol REASON: CORRECT Contains 18 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N2C(C(=O)NC(CO)CC(C)C)CCC2)(C)C)CC(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CC(=O)N)CC(C)C)CC(C)C)(C)C '
               'NAME: Trichorovin-XI REASON: CORRECT Contains 12 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC2=CC=CC=C2)CCC(=O)N)CCC(=O)O)(C)C)(C)C)C(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)C)(C)C)C)(C)C)C)CCC(=O)N)(C)C)CC(C)C)(C)C)(C)C)(C)C '
               'NAME: Trichocellin-B-I REASON: CORRECT Contains 22 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)(CC)C)CCC(=O)N)(CC)C)(C)C)(C)C)(C)C)(C)C '
               'NAME: Trichovirin II 3b REASON: CORRECT Contains 20 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'C(N[C@H](C(N[C@@H](CC(=O)N)C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(O)=O)CC=1C=CC=CC1)=O)CC2=CNC=N2)=O)C(O)C)=O)CCCCN)=O)CC=3C=4C=CC=CC4NC3)=O)CC=5C=6C=CC=CC6NC5)=O)CCCCN)=O)C)=O)C(O)C)=O)=O)C(CC)C)([C@H](CCC(=O)N)N)=O '
               'NAME: QINTAKWWKTHF REASON: CORRECT Contains 13 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CN)CC=1C2=C(C=CC=C2)NC1)C(C)C)C)C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N)C(C)C)C(C)C)CO)C)CC(C)C)C(C)C)C(C)C)[C@H](O)C)CS)C)C(C)C '
               'NAME: Thuricin 439A REASON: CORRECT Contains 20 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1NC(C(=O)NCC(=O)NC(C(=O)NC2C(=O)NC(C(=O)NC(CC=3N=CNC3)C(NC(C(NC(C(NC(CC(OCC(C(NC1C(O)C)=O)NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(N)CCC(=O)O)CC(C)C)C(O)C)C(O)C)C(O)C)=O)C(=O)O)=O)CC(=O)NCCCC2)=O)CC4=CC=CC=C4)=O)C(O)C)CO)C '
               'NAME: Prunipeptin REASON: CORRECT Contains 17 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(N)C1=CC=C(O)C=C1)C2=CC(O)=CC(=C2)O)C(C)C)C3=CC(O)=CC(=C3)O)C4=CC=C(O)C=C4)C5=CC(O)=CC(=C5)O)C6=CC=C(O)C=C6)C7=CC(O)=CC(=C7)O)C(C)C)C8=CC(O)=CC(=C8)O)C9=CC=C(O)C=C9)CC%10=CC=CC=C%10)CC(=O)O '
               'NAME: Feglymycin REASON: CORRECT Contains 12 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC2=CC=CC=C2)CCC(=O)N)CCC(=O)N)(CC)C)(C)C)C(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)C)(C)C)C)(C)C)(C)C)CCC(=O)N)(C)C)C(C)C)(C)C)CC(C)C)(C)C '
               'NAME: Trichokonin-IX REASON: CORRECT Contains 23 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'CCC(C)[C@H](NC(=O)[C@H](CC(N)=O)NC(=O)[C@H](CCCCN)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]1CCCN1C(=O)[C@H](CC(N)=O)NC(=O)[C@H](CCC(N)=O)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)CNC(=O)[C@@H](N)CCCCN)C(C)C)C(C)C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](C(C)O)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@@H](C(C)O)C(=O)N1CCC[C@H]1C(O)=O '
               'NAME: KGKGKGKGKGENPVVHFFKNIVTPRTP REASON: CORRECT Contains 29 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'CSCC[C@H](NC(=O)[C@H](CO)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](Cc1cnc[nH]1)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(=O)NCC(=O)N[C@@H](CCCCN)C(=O)N1CCC[C@H]1C(=O)N[C@@H](C(C)C)C(=O)NCC(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N1CCC[C@H]1C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](Cc1ccc(O)cc1)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CC(N)=O)C(=O)NCC(=O)N[C@@H](C)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CO)C(=O)N[C@@H](C)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](C)C(=O)N[C@@H](Cc1ccccc1)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](Cc1ccccc1)C(O)=O '
               'NAME: corticotropin REASON: CORRECT Contains 39 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C=O)[C@H](CC)C)CC(=O)N)CCCNC(=N)N)CCCNC(=N)N)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CN)CC(C)C)CCCNC(=N)N)CCCNC(=N)N)CC(C)C)CC1=CC=CC=C1)C)CC(=O)O)CCC(=O)N)CC(C)C)C(C)C '
               'NAME: Labetaomycin REASON: CORRECT Contains 17 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'SCC(NC(=O)C(NC(=O)C1N(C(=O)C(NC(=O)C2N(C(=O)C3N(C(=O)C(NC(=O)C(N)[C@H](O)C)CC(=O)N)CCC3)CCC2)C)CCC1)[C@H](O)C)C(=O)NC(C(=O)NC(C(=O)N)[C@@H](O)C)[C@H](O)C '
               'NAME: POH 3 REASON: CORRECT Contains 11 amino acid residues, '
               'classifying as polypeptide\n'
               ' * SMILES: '
               'S1CC(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)CN)CC(=O)O)CC(C)C)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(NC(C(NC(C(NC(C1)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)C(=O)NC2C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(O)C)C(NC(C(NC(CNC(CSC2)C(=O)CC(C(=O)O)CC(C)C)CC(C)C)=O)CC(C)C)=O)=C)CC3=CC=CC=C3)C)CC4=CC=CC=C4)CCCCN)CC(=O)O)=O)CC(C)C)=O)CC(C)C)=O)CC(C)C)=C)C)=C '
               'NAME: Curvopeptin-4 REASON: CORRECT Contains 21 amino acid '
               'residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N2[C@H](C(=O)N3[C@H](C(=O)O)CCC3)CCC2)CCCCN)[C@H](CC)C)C(C)C)CC(=O)N)CO)CC=4NC=NC4)C(C)C)CC=5C6=C(C=CC=C6)NC5)CCC(=O)NCC(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H]1C(C)C)=O)CC(C)C)=O)CCC(=O)N)=O)CO)=O)CCCNC(=N)N)CC7=CC=C(O)C=C7 '
               'NAME: Lariatin B REASON: CORRECT Contains 22 amino acid '
               'residues, classifying as polypeptide\n'
               'False positives: SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO)[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO '
               'NAME: CID 91855737 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'CC(C)CCCCC(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CCNCS(O)(=O)=O)C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CCNCS(O)(=O)=O)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CCNCS(O)(=O)=O)NC1=O)[C@@H](C)O '
               'NAME: colistimethate B REASON: WRONGLY CLASSIFIED Contains 11 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N(CCC[C@@H]1NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C2NC(=NCC2)[C@H](NC(=O)[C@@H](N(O)C(=O)CNC(=O)CNC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H]3[N+]4=C(NCC3)C(NC(=O)CCC(=O)N)=CC=5C4=CC(O)=C(C5)O)C)CCCCN)CC(=O)N)CCC(=O)N)CO)C)C '
               'NAME: Pyoverdin Pf/3 ATCC 17400 REASON: WRONGLY CLASSIFIED '
               'Contains 14 amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO[C@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)C)O)[C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O[C@H]%19O[C@@H]([C@H](O)[C@H](O)[C@H]%19O)C)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91858331 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91852179 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N2C(C(=O)NC(C(=O)NC(C(=O)NC(CC(NC(C(NC(C(NC(C(NC1CCC(=O)N)=O)CC(=O)N)=O)CC3=CC=C(O)C=C3)=O)CC(=O)N)=O)CCCCCCCCCCC(CC)C)CC(=O)N)CO)CCC2 '
               'NAME: Mycosubtilin D REASON: WRONGLY CLASSIFIED Contains 12 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'C[C@@H](O)[C@H](NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CC[C@H](CN)O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)[C@H](Cc1cccc(C)c1)NC(=O)CNC(=O)[C@H](C)NC(=O)[C@@H](NC(=O)CN)C1CCCCC1)C(O)=O '
               'NAME: '
               'Gly-Chg-Ala-Gly-Phe(3-Me)-Lys(5-GalO)-Gly-Glu-Gln-Gly-Pro-Lys-Gly-Glu-Thr '
               'REASON: WRONGLY CLASSIFIED Contains 15 amino acid residues, '
               'classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(=O)O)CC(C)C)CC2=CC=CC=C2)CCCNC(=N)N)C(C)C)C)CCC(=O)ONCC(=O)NCC(N[C@H](C(NCC(N[C@H](C(N[C@@H]1CC3=CC=C(O)C=C3)=O)CCCCN)=O)=O)CO)=O)CCCCN '
               'NAME: Mycetohabin-16 REASON: WRONGLY CLASSIFIED Contains 15 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               '[C@@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@H]7[C@@H]([C@H]([C@@H]([C@H](O7)CO)O[C@H]8[C@@H]([C@H]([C@H]([C@H](O8)CO[C@]9(O[C@]([C@@H]([C@H](C9)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)O)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O)NC(C)=O)O)O[C@@H]%10[C@H]([C@H]([C@@H]([C@H](O%10)CO)O)O)O[C@H]%11[C@@H]([C@H]([C@@H]([C@H](O%11)CO)O[C@H]%12[C@@H]([C@H]([C@H]([C@H](O%12)CO)O)O[C@H]%13[C@@H]([C@H]([C@@H]([C@H](O%13)CO)O[C@H]%14[C@@H]([C@H]([C@H]([C@H](O%14)CO)O)O[C@H]%15[C@@H]([C@H]([C@@H]([C@H](O%15)CO)O[C@H]%16[C@@H]([C@H]([C@H]([C@H](O%16)CO[C@]%17(O[C@]([C@@H]([C@H](C%17)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)O)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O)NC(C)=O)O)O[C@H]%18[C@@H]([C@H]([C@@H](O[C@@H]%18CO)O[C@H]%19[C@@H]([C@H](C(O[C@@H]%19CO)O)NC(C)=O)O)NC(C)=O)O '
               'NAME: '
               'alpha-Neup5Ac-(2->6)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->3)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->3)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-[alpha-Neup5Ac-(2->6)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->3)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->3)-beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->6)]-beta-D-Manp-(1->4)-beta-D-GlcpNAc-(1->4)-beta-D-GlcpNAc '
               'REASON: WRONGLY CLASSIFIED Contains 10 amino acid residues, '
               'classifying as polypeptide\n'
               ' * SMILES: '
               'COC1NC(=O)c2nc(oc2C)\\C(NC(=O)C(NC(=O)c2csc(n2)-c2ccc(nc2-c2nc(oc2C)C(=C)NC(=O)C(=C)NC(=O)c2nc(oc2C)\\C(NC(=O)c2csc1n2)=C\\C)C(=O)NC(=C)C(=O)NC(=C)C(=O)NC(=C)C(N)=O)C(C)O)=C\\C(C)O '
               'NAME: Methylsulfomycin I REASON: WRONGLY CLASSIFIED Contains '
               '10 amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91845638 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](NC(=O)C2=C3N=C4C(=C(C(=O)C5=C4C(=O)OC[C@H](N5)[C@@H]6NC(=O)[C@@H](N(C(=O)CN(C)C([C@H]7N(C([C@H](NC6=O)C(C)C)=O)CC(=O)C7)=O)C)C)C)OC3=C(C)C=C2)C(=O)N[C@@H](C(=O)N8[C@@H](C)C[C@@H]([C@H]8C(N(CC(N([C@H]1C(C)C)C)=O)C)=O)O)C(C)C)C '
               'NAME: Actinomycin Y6 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               '[O-]C(=O)[C@H]1N(CCC1)C([C@H](CCSC)NC(=O)[C@H]2N(CCC2)C(=O)CNC([C@H](CCCC[NH3+])NC([C@H](CC3=CN=CN3)NC([C@H](CO)NC([C@H](CC(C)C)NC([C@H](CCCNC(=[NH2+])N)NC(=O)[C@H]4N(CCC4)C([C@H](CCCNC(=[NH2+])N)NC([C@H](CCC(=O)N)[NH3+])=O)=O)=O)=O)=O)=O)=O)=O '
               'NAME: apelin-12(3+) REASON: WRONGLY CLASSIFIED Contains 12 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O[C@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)C)[C@H]9NC(=O)C)CO)[C@H](O)[C@@H]8O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO)CO)[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O[C@H]%19O[C@@H]([C@H](O)[C@H](O)[C@H]%19O)C)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91845439 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N2C(C(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)NCC(NC(C(NC(C(N3C(C(NC(C1NC(=O)C(NC(=O)C/C=C/CCCCCCCC(C)C)CC(=O)N)C)=O)CCC3)=O)C(C)C)=O)C(N)C)=O)CC(=O)O)CC(=O)O)C(C(=O)O)C)CCCC2 '
               'NAME: Friulimicin B REASON: WRONGLY CLASSIFIED Contains 13 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'S(CCC(N)C(=O)NC(C(=O)NCC(=O)NC(C(=O)N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C=O)CC(C)C)CCCN=C(N)N)CC(C)C)C(C)C)CC(=O)O)CCC1)CC(=O)O)CCC(=O)N)C '
               'NAME: Mycobacterium leprae ferritin REASON: WRONGLY CLASSIFIED '
               'Contains 10 amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'C[C@@H](NC(=O)[C@@H](C)NC(=O)[C@H](CCCCNC(=O)CNC(=O)CNC(=O)C[NH3+])NC(=O)CC[C@@H](NC(=O)[C@H](C)NC(=O)[C@@H](C)O[C@@H]1[C@@H](NC(C)=O)[C@H](O[C@H](CO)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1NC(C)=O)OP([O-])(=O)OP([O-])(=O)OC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(\\C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)C(N)=O)C([O-])=O '
               'NAME: '
               'undecaprenyldiphospho-N-acetyl-(N-acetylglucosaminyl)muramoyl-L-alanyl-D-isoglutaminyl-(glycyl)3-L-lysyl-D-alanyl-D-alanine(2-) '
               'REASON: WRONGLY CLASSIFIED Contains 11 amino acid residues, '
               'classifying as polypeptide\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO '
               'NAME: CID 91862370 REASON: WRONGLY CLASSIFIED Contains 10 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1OC2=CC=C(CC(NC(=O)C(NC(=O)C(NC(=O)CCCCCCCCCCCCC(C)C)CCC(=O)O)CCCN)C(=O)NC(C(=O)NC(C(=O)NC(C(N3C(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CCC(=O)N)=O)CCC3)=O)C(C)C)CCC(=O)O)C(O)C)C=C2 '
               'NAME: SNA-60-367-17 REASON: WRONGLY CLASSIFIED Contains 11 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N2[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](CC(N[C@H](C(N[C@@H](C(N[C@@H](C(N[C@H]1CCC(=O)N)=O)CC(=O)N)=O)CC3=CC=C(O)C=C3)=O)CC(=O)N)=O)CCCCCCCCCCC(C)C)CO)CC(=O)N)CCC2 '
               'NAME: Iturin A6 REASON: WRONGLY CLASSIFIED Contains 12 amino '
               'acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1NCC(=O)N[C@@H](C(=O)NCC(=O)N[C@@H](C(=O)N[C@@H](CC(NCC(N[C@H](C(N[C@@H]1[C@H](CC)C)=O)CC2=CC=CC=C2)=O)=O)C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@@H](C(=O)N[C@@H](C(=O)O)CC3=CC=CC=C3)CC(=O)O)CO)CC4=CC=C(O)C=C4)CC=5NC=NC5)CC6=CC=CC=C6)[C@@H](CC)C)CC(=O)N)CC=7C8=C(C=CC=C8)NC7 '
               'NAME: Anantin REASON: WRONGLY CLASSIFIED Contains 18 amino '
               'acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'C[C@@H](O)[C@H](NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CC[C@H](CN)O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)[C@H](Cc1ccncc1)NC(=O)CNC(=O)[C@H](C)NC(=O)[C@H](CC1CC1)NC(=O)CN)C(O)=O '
               'NAME: '
               'Gly-Cpa-Ala-Gly-Ala(4-Py)-Lys(5-GalO)-Gly-Glu-Gln-Gly-Pro-Lys-Gly-Glu-Thr '
               'REASON: WRONGLY CLASSIFIED Contains 15 amino acid residues, '
               'classifying as polypeptide\n'
               ' * SMILES: '
               'CC(C)C[C@H](NC(=O)CNC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](CO)NC(=O)[C@H](Cc1c[nH]c2ccccc12)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@@H]1CCC(=O)N1)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N1CCC[C@H]1C(=O)NCC(N)=O '
               'NAME: gonadorelin REASON: WRONGLY CLASSIFIED Contains 11 amino '
               'acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C(N1C(C(=O)NC(C(=O)NC(CO)CC2=CC=CC=C2)(C)C)CC(C1)O)C(NC(=O)C(NC(=O)C3N(C(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)C(C)C)(C)C)(C)C)(C)C)C(C)C)CC(C)C)C(C)C)(C)C)CC(C3)O)CCC(=O)N)(CC)C '
               'NAME: Bergofungin B REASON: WRONGLY CLASSIFIED Contains 16 '
               'amino acid residues, classifying as polypeptide\n'
               ' * SMILES: '
               'O=C1N[C@@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@@H](CC(NC(C(N[C@@H]1[C@H](O)C2=CC=C(O)C=C2)=O)C)=O)C[C@@H](O)[C@@H](O)[C@@H](O[C@H]3OC[C@@H](O)[C@@H]([C@H]3O)O)CCCCCCCCCCC)=O)[C@H](O)C(=O)N)CO)CC(=O)N)CC(=O)N '
               'NAME: Burkholidine 1213 REASON: WRONGLY CLASSIFIED Contains 11 '
               'amino acid residues, classifying as polypeptide\n'
               'False negatives: SMILES: '
               'O=C1NC2C(=O)NC(C(=O)NC(C(=O)NC(C3=CC(O)=CC(=C3)O)C(=O)O)C=4C(C=5C=C(C2)C=CC5O)=C(O)C=C(O)C4)CC6=CC=C(OC=7C=C8C1NC(=O)C9NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)C%10=CC=C(O)C=C%10)C=%11C=C(C=C(OC=%12C=C9C=CC%12O)C%11)O)CC=%13C%14=C(C=C(C(=C8)C7O)C=C%14)NC%13)C=C6 '
               'NAME: Corbomycin REASON: MISSED Contains only 9 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'O=C(O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCC)C(C)C)CC1=CC=CC=C1)CCC(=O)O)CC(C)C)C)[C@H](CC)C '
               'NAME: Holrhizin O REASON: MISSED Contains only 6 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)O)[C@H](O)C)[C@H]1N(C(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)C[C@H](O)CCCCCCC)C(C)C)C)CCC(=O)N)C)C(C)C)C)CCC1 '
               'NAME: Thanafactin A REASON: MISSED Contains only 9 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'S1[C@H](NC(C1)C(=O)N[C@H](C(=O)OC)CCSC)[C@H]2N(C(=O)[C@@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)/C(/NC(=O)N[C@H](C(=O)O)CC3=CC=CC=C3)=C/C)CO)=C/C)CO)=C/C)CCCN=C(N)N)CCC2 '
               'NAME: Chitinimide B REASON: MISSED Contains only 9 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'S1C(=NC(=C1)C(=O)N[C@H](C(=O)O)CCC(=O)N)[C@H]2N(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)/C(/NC(=O)N[C@H](C(=O)O)CC3=CC=C(O)C=C3)=C/C)C)CCCN=C(N)N)CCC2 '
               'NAME: Pseudovibriamide A1 REASON: MISSED Contains only 7 amino '
               'acid residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N1[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CO)[C@H](O)C)C(C)C)C(C)C)CCC1)C(C)C)C=3NC=CC3 '
               'NAME: Endopyrrole B REASON: MISSED Contains only 7 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'ClC1=C2OC3=C(O)C=CC(=C3)C(NC(C4NC(C(C(=C1)C=C2)NC(=O)C5NC(=O)C(NC(=O)C(NC(=O)C(N)C6=CC=C(O)C=C6)CC=7C8=C(C=C(C9=CC5=CC(OC%10=CC=C(C4)C=C%10)=C9O)C=C8)NC7)C%11=CC(Cl)=C(O)C=C%11)=O)=O)C(=O)O '
               'NAME: Rimomycin C REASON: MISSED Contains only 6 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'ClC1=C2OC3=C(O[C@H]4O[C@H]([C@H](O)[C@@H]([C@@H]4N)O)CO)C=5OC6=CC=C(CC7NC(=O)C(N)C=8C=CC(=C(OC=9C=C(C(C(NC(C(=C3)C5)C(=O)NC%10C(NC(C(C(=C1)C=C2)O[C@H]%11O[C@@H]([C@@H](O)[C@@H]([C@H]%11NC(=O)C)O)CO)C(=O)NC(C%12=C(C(O[C@H]%13OC([C@@H](O)[C@@H]([C@@H]%13O)O)CO)=CC(=C%12)O)C=%14C=C%10C=CC%14O)C(=O)O)=O)=O)NC7=O)C=C(O)C9)C8)O)C=C6 '
               'NAME: Deacyl-GP1416 REASON: MISSED Contains only 7 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'O=C1NC(C(N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC=2NC=NC2)[C@H](O)C)C)CO)=N[C@H]1CC=3NC=NC3)CC(C)C '
               'NAME: Streptamidine REASON: MISSED Contains only 4 amino acid '
               'residues, not enough for a polypeptide\n'
               ' * SMILES: '
               'O=C(O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCC)C(C)C)CC1=CC=CC=C1)CCC(=O)O)[C@H](CC)C)C)[C@H](CC)C '
               'NAME: Holrhizin M REASON: MISSED Contains only 6 amino acid '
               'residues, not enough for a polypeptide\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Contains approximately 0 amino '
                                               'acid residues, not enough for '
                                               'a polypeptide'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1NC2C(=O)NC(C(=O)NC(C(=O)NC(C3=CC(O)=CC(=C3)O)C(=O)O)C=4C(C=5C=C(C2)C=CC5O)=C(O)C=C(O)C4)CC6=CC=C(OC=7C=C8C1NC(=O)C9NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)C%10=CC=C(O)C=C%10)C=%11C=C(C=C(OC=%12C=C9C=CC%12O)C%11)O)CC=%13C%14=C(C=C(C(=C8)C7O)C=C%14)NC%13)C=C6',
                                      'name': 'Corbomycin',
                                      'reason': 'Contains approximately 1 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'O=C(NCC(=O)N[C@H](C(=O)N[C@H](CO)CC(C)C)[C@H](CC)C)C(NC(=O)[C@@H](NC(=O)CNC(=O)CNC(=O)C(NC(=O)[C@@H](NC(=O)CNC(=O)C(NC(=O)CCCCCCC)(C)C)CC(C)C)(C)C)CC(C)C)(C)C',
                                      'name': 'Trichogin A IV',
                                      'reason': 'Contains approximately 6 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'O=C(NCCCC(NC(=O)/C=C\\CCCCCCCC)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(=O)N)C(O)C(=O)N)CCNC(=O)C(N)C(O)C)C(O)C)N',
                                      'name': 'Rotihibin D',
                                      'reason': 'Contains approximately 5 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'O=C(O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCC)C(C)C)CC1=CC=CC=C1)CCC(=O)O)CC(C)C)C)[C@H](CC)C',
                                      'name': 'Holrhizin O',
                                      'reason': 'Contains approximately 6 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'O=C(O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(N)C1=CC=C(O)C=C1)C2=CC(O)=CC(=C2)O)C(C)C)C3=CC(O)=CC(=C3)O)C4=CC=C(O)C=C4)C5=CC(O)=CC(=C5)O)C6=CC=C(O)C=C6)C7=CC(O)=CC(=C7)O)C(C)C)C8=CC(O)=CC(=C8)O)C9=CC=C(O)C=C9)CC%10=CC=CC=C%10)CC(=O)O',
                                      'name': 'Feglymycin',
                                      'reason': 'Contains approximately 4 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'SCC(NC(=O)C(NC(=O)C1N(C(=O)C(NC(=O)C2N(C(=O)C3N(C(=O)C(NC(=O)C(N)[C@H](O)C)CC(=O)N)CCC3)CCC2)C)CCC1)[C@H](O)C)C(=O)NC(C(=O)NC(C(=O)N)[C@@H](O)C)[C@H](O)C',
                                      'name': 'POH 3',
                                      'reason': 'Contains approximately 9 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'O=C(N1[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)NCCC(=O)N[C@H](CN(C)C)C)(C)C)(C)C)CC(C)C)CC(C)C)(C)C)[C@H](O)C(C)C)C[C@@H](CCCC(=O)CC)C)C[C@@H](C1)C)/C=C/[C@H](CC)C',
                                      'name': 'Leucinostatin NPDG B',
                                      'reason': 'Contains approximately 8 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'O=C(O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CC(O)CCCCCCC)CC(=O)N)C(C)C)CC1=CC=CC=C1)CC(=O)N)CC(=O)N)CCCCN)C(O)C)CC=2C3=C(C=CC=C3)NC2)C(CC)C',
                                      'name': 'Cerexin-D2',
                                      'reason': 'Contains approximately 9 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'Cl.C=12C(C[C@H](NC([C@H](CC3=CN=CN3)NC([C@H]4NC(=O)CC4)=O)=O)C(N[C@H](C(N[C@@H](CC5=CC=C(O)C=C5)C(NCC(N[C@H](C(N[C@H](C(N6[C@@H](CCC6)C(NCC(N)=O)=O)=O)CCCNC(N)=N)=O)CC(C)C)=O)=O)=O)CO)=O)=CNC1C=CC=C2',
                                      'name': 'Gonadorelin hydrochloride',
                                      'reason': 'Contains approximately 6 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'},
                                  {   'smiles': 'S1C(NC(=O)[C@H]2N(C(=O)CNC([C@H](C1)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)C)CO)=O)CCC2)(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC3C(=O)NCC(=O)NCC(NC(SC3)C(=O)N[C@H](C(=O)O)CCCN=C(N)N)=O)CO)CC=4NC=NC4)CO',
                                      'name': 'Streptosactin',
                                      'reason': 'Contains approximately 6 '
                                                'amino acid residues, not '
                                                'enough for a polypeptide'}],
    'attempt': 1,
    'reasoning': 'In reviewing the code and outcomes from the previous attempt '
                 'at classifying polypeptides, a couple of points need '
                 'improvement:\n'
                 '\n'
                 '1. **False Positives:** Some molecules were wrongly '
                 'classified as polypeptides because the previous definition '
                 'of counting peptide bonds was overly simplistic. Simply '
                 'counting peptide bonds with the pattern "C(=O)N" was not '
                 'sufficient because it can match structures that include '
                 'similar motifs outside of classic peptide sequences.\n'
                 '\n'
                 '2. **False Negatives:** Some genuine polypeptides were '
                 'missed, likely due to their complex structures or '
                 'modifications to the typical peptide backbone that our '
                 "simple pattern couldn't match. \n"
                 '\n'
                 'To address these issues, the SMILES string should be '
                 'examined more thoughtfully to specifically identify amino '
                 'acid residues. This can be achieved by using a more '
                 'sophisticated substructure pattern that encompasses '
                 'variations of peptide bonds and associated side chains or by '
                 'leveraging additional RDKit functionality to directly '
                 'analyze expected amino acid components.\n'
                 '\n'
                 "Let's update the function by:\n"
                 '- Counting the number of amino acid residues more reliably '
                 'by identifying typical peptide structures.\n'
                 '- Ensuring specific patterns of amino acids and their common '
                 'structural motifs are accounted for, which may involve '
                 'developing more comprehensive SMARTS patterns or additional '
                 'logic to verify peptide sequences.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 257,
    'num_false_positives': 357,
    'num_true_negatives': 141561,
    'num_false_negatives': 125,
    'num_negatives': None,
    'precision': 0.4185667752442997,
    'recall': 0.6727748691099477,
    'f1': 0.5160642570281124,
    'accuracy': 0.996612789880534,
    'negative_predictive_value': 0.9991177674576176}