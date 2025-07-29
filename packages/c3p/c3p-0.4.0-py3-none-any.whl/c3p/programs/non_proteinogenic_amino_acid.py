"""
Classifies: CHEBI:83820 non-proteinogenic amino acid
"""
#!/usr/bin/env python3
"""
Classifies: Non-proteinogenic amino acid
Defined as: “Any amino acid that is not naturally encoded in the genetic code of any organism.”
This version uses several checks:
  1. It requires the presence of a carboxylic acid group.
  2. It searches for an α–carbon that is sp³ and is bound to both a carboxyl group and an [NX3] (any trivalent nitrogen),
     so that even substituted amines (N-methyl, N-hydroxy, etc.) are allowed.
  3. It excludes molecules that appear to be peptides (by looking for a peptide bond pattern).
  4. It rejects molecules whose molecular weight is far outside the typical range for single amino acids.
  5. It compares the canonical SMILES to a set of the 20 standard proteinogenic amino acids.
If the molecule has the amino acid backbone and is not one of the standard proteinogenic amino acids, 
it is classified as non–proteinogenic.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_non_proteinogenic_amino_acid(smiles: str):
    """
    Determines if a molecule is a non–proteinogenic amino acid.
    
    Checks performed:
      - The molecule must parse correctly.
      - Its molecular weight should be within a typical amino acid range (roughly 75–350 Da).
      - It must have at least one carboxylic acid group.
      - It must have an alpha carbon (sp³) that is attached to both a carboxylic acid and an amino group.
        (Here, any trivalent nitrogen [NX3] is allowed so that substituted amines are accepted.)
      - Molecules containing a peptide-bond substructure are excluded.
      - Its canonical SMILES is compared to that of the 20 standard amino acids.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if molecule is a non–proteinogenic amino acid, False otherwise.
        str: Reason for classification.
    """
    # Parse molecule from SMILES
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return False, "Invalid SMILES string"
    
    # Check molecular weight – typical amino acids fall roughly between 75 and 350 Da.
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 75 or mw > 350:
        return False, f"Molecular weight {mw:.1f} out of range for typical amino acids"
    
    # Check for a carboxylic acid group.
    acid_pattern = Chem.MolFromSmarts("C(=O)[O;H,-]")
    if not mol.HasSubstructMatch(acid_pattern):
        return False, "No carboxylic acid group detected"
    
    # Check for an alpha-carbon pattern:
    # We look for an sp3 carbon attached directly to a trivalent nitrogen ([NX3]) and to a carboxyl group.
    # This pattern should capture even N–substituted amino groups as in N,N–dihydroxydihomomethionine.
    alpha_pattern = Chem.MolFromSmarts("[C;X4]([NX3])C(=O)[O;H,-]")
    if not mol.HasSubstructMatch(alpha_pattern):
        return False, "No typical alpha-amino acid backbone detected"
    
    # Exclude molecules that appear to be peptides.
    # Peptide bonds (an amide bond linking two alpha-carbons) are detected by this pattern.
    peptide_bond_pattern = Chem.MolFromSmarts("C(=O)N[C;X4]")
    if mol.HasSubstructMatch(peptide_bond_pattern):
        return False, "Contains peptide bond; likely a peptide rather than a single amino acid"
    
    # Compute the canonical SMILES (including stereochemistry) for standardized comparison.
    input_canonical = Chem.MolToSmiles(mol, isomericSmiles=True)
    
    # Define canonical SMILES for the 20 standard proteinogenic amino acids.
    proteinogenic_aas = [
        "NCC(=O)O",                              # glycine
        "N[C@@H](C)C(=O)O",                       # L-alanine
        "N[C@@H](C(C)C)C(=O)O",                    # L-valine
        "N[C@@H](CC(C)C)C(=O)O",                   # L-leucine
        "N[C@@H](C[C@H](C)C)C(=O)O",               # L-isoleucine
        "O=C(O)N1CC[C@H](C1)O",                    # L-proline
        "N[C@@H](Cc1ccccc1)C(=O)O",                # L-phenylalanine
        "N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O",         # L-tryptophan
        "N[C@@H](Cc1ccc(O)cc1)C(=O)O",              # L-tyrosine
        "N[C@@H](CO)C(=O)O",                       # L-serine
        "N[C@@H]([C@H](O)C)C(=O)O",                # L-threonine
        "N[C@@H](CS)C(=O)O",                       # L-cysteine
        "N[C@@H](CCSC)C(=O)O",                      # L-methionine
        "N[C@@H](CC(=O)O)C(=O)O",                   # L-aspartic acid
        "N[C@@H](CCC(=O)O)C(=O)O",                  # L-glutamic acid
        "N[C@@H](CC(=O)N)C(=O)O",                   # L-asparagine
        "N[C@@H](CCC(=O)N)C(=O)O",                  # L-glutamine
        "N[C@@H](CCCCN)C(=O)O",                     # L-lysine
        "N[C@@H](CCCNC(=N)N)C(=O)O",                # L-arginine
        "N[C@@H](Cc1c[nH]cn1)C(=O)O"                # L-histidine
    ]
    prot_set = set()
    for aas in proteinogenic_aas:
        aas_mol = Chem.MolFromSmiles(aas)
        if aas_mol:
            canon = Chem.MolToSmiles(aas_mol, isomericSmiles=True)
            prot_set.add(canon)
    
    if input_canonical in prot_set:
        return False, "Matches a standard proteinogenic amino acid"
    
    # If all tests pass, classify as a non-proteinogenic amino acid.
    return True, "Has amino acid functional groups and does not match any standard proteinogenic amino acid"

# For debugging or simple testing:
if __name__ == "__main__":
    # A set of test examples drawn from the outcomes.
    test_examples = [
        # True positives (non‐proteinogenic):
        ("N[C@@H](CC1=CC=C(F)C=C1)C(O)=O", "4-fluorophenyl-L-alanine"),
        ("CSCCCCCC(N(O)O)C(O)=O", "N,N-dihydroxydihomomethionine"),
        ("NC(Cc1c[nH]c2cccc(O)c12)C(O)=O", "4-hydroxytryptophan"),
        ("O(C[C@@H](N)C(O)=O)CC1=CC=CC=C1", "O-Benzyl-D-serine"),
        ("CN[C@@H](Cc1ccccc1)C(O)=O", "N-methyl-L-phenylalanine"),
        ("IC=1C=CC(C[C@H](C(O)=O)N)=CC1", "4-iodo-D-phenylalanine"),
        ("[H][C@](N)(CS[C@H](\\C=C\\C=C\\C=C/C\\C=C/CCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O", "18-carboxy-19,20-dinor-leukotriene E4"),
        ("NC(CCCC(N)C(O)=O)C(O)CC(O)=O", "2,6-diamino-7-hydroxy-azelaic acid"),
        ("OC(=O)CNCC(O)=O", "iminodiacetic acid"),
        ("C([C@H]([C@@H](C(=O)N)O)N)(O)=O", "(3S)-3-hydroxy-L-asparagine"),
        ("NC(CC1=CC2=CC=CC=C2C=C1)C(O)=O", "3-naphthalen-2-ylalanine"),
        ("CC(NCCCC[C@H](N)C(O)=O)C(O)=O", "N(6)-(1-carboxyethyl)-L-lysine"),
        ("N[C@@H](CCCNO)C(O)=O", "N(5)-hydroxy-L-ornithine"),
        ("NCCC[C@H](N)C(O)=O", "L-ornithine"),
        ("NCCOP(O)(=O)OCC(N)C(O)=O", "serine phosphoethanolamine"),
        ("O=C(O)[C@@H](N)CCCCCCCSC", "L-pentahomomethionine"),
        ("OC([C@@H](N)CSC(=O)CCCCCCC)=O", "S-octanoyl-L-cysteine"),
        ("OC(=O)CNc1ccc(O)cc1", "N-(p-hydroxyphenyl)glycine"),
        ("CC(C)=CC\\C=C(\\C)[C@H]1CN[C@@H]([C@H]1CC(O)=O)C(O)=O", "dainic acid A"),
        ("N[C@H](Cc1c[nH]cn1)C(O)=O", "D-histidine"),
        ("N[C@H](Cc1ccc(O)c(O)c1)C(O)=O", "D-dopa"),
        ("N[C@@H](CS\\C(Cl)=C/Cl)C(O)=O", "S-(trans-1,2-dichlorovinyl)-L-cysteine"),
        ("CC(=O)CNCCCCC(N)C(O)=O", "N(6)-acetonyllysine"),
        ("N[C@@H]([C@H](O)CC(O)=O)C(O)=O", "(R)-3-hydroxy-L-glutamic acid"),
        ("NC(Cc1ccc(O)c(O)c1)C(O)=O", "dopa"),
        # Some examples that were previously (wrongly) classified:
        ("CNC(=N)NCCC[C@H](N)C([O-])=O", "N(omega)-methyl-L-argininate"),
        ("OC(=O)C(NCC(O)=O)CCCN=C(N)N", "L-Acetopine")
    ]
    for smi, name in test_examples:
        result, reason = is_non_proteinogenic_amino_acid(smi)
        print(f"SMILES: {smi}\nName: {name}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:83820',
                          'name': 'non-proteinogenic amino acid',
                          'definition': 'Any amino-acid that is not naturally '
                                        'encoded in the genetic code of any '
                                        'organism.',
                          'parents': ['CHEBI:33709'],
                          'xrefs': ['Wikipedia:Non-proteinogenic_amino_acids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 109,
                           'log_lines_of_code': 4.6913478822291435,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
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
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
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
                                                 2,
                                                 2],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'MolToSmiles',
                                                 'add',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 6,
                           'smarts_strings': [   'C(=O)[O;H,-]',
                                                 '[C;X4]([NX3])C(=O)[O;H,-]',
                                                 'C(=O)N[C;X4]'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_non_proteinogenic_amino_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight {mw:.1f} '
                                          'out of range for typical amino '
                                          'acids"',
                                          'False, "No carboxylic acid group '
                                          'detected"',
                                          'False, "No typical alpha-amino acid '
                                          'backbone detected"',
                                          'False, "Contains peptide bond; '
                                          'likely a peptide rather than a '
                                          'single amino acid"',
                                          'False, "Matches a standard '
                                          'proteinogenic amino acid"',
                                          'True, "Has amino acid functional '
                                          'groups and does not match any '
                                          'standard proteinogenic amino acid"'],
                           'returns_count': 7,
                           'complexity': 4.338269576445829},
    'message': '\n'
               'Attempt failed: F1 score of 0.4151957022256332 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: N[C@@H](CC1=CC=C(F)C=C1)C(O)=O NAME: '
               '4-fluorophenyl-L-alanine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: CSCCCCCC(NO)C(O)=O NAME: N-hydroxytrihomomethionine '
               'REASON: CORRECT Has amino acid functional groups and does not '
               'match any standard proteinogenic amino acid\n'
               ' * SMILES: NC(Cc1c[nH]c2cccc(O)c12)C(O)=O NAME: '
               '4-hydroxytryptophan REASON: CORRECT Has amino acid functional '
               'groups and does not match any standard proteinogenic amino '
               'acid\n'
               ' * SMILES: O(C[C@@H](N)C(O)=O)CC1=CC=CC=C1 NAME: '
               'O-Benzyl-D-serine REASON: CORRECT Has amino acid functional '
               'groups and does not match any standard proteinogenic amino '
               'acid\n'
               ' * SMILES: CN[C@@H](Cc1ccccc1)C(O)=O NAME: '
               'N-methyl-L-phenylalanine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: IC=1C=CC(C[C@H](C(O)=O)N)=CC1 NAME: '
               '4-iodo-D-phenylalanine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               '[H][C@](N)(CS[C@H](\\C=C\\C=C\\C=C/C\\C=C/CCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O '
               'NAME: 18-carboxy-19,20-dinor-leukotriene E4 REASON: CORRECT '
               'Has amino acid functional groups and does not match any '
               'standard proteinogenic amino acid\n'
               ' * SMILES: NC(CCCC(N)C(O)=O)C(O)CC(O)=O NAME: '
               '2,6-diamino-7-hydroxy-azelaic acid REASON: CORRECT Has amino '
               'acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: OC(=O)CNCC(O)=O NAME: iminodiacetic acid REASON: '
               'CORRECT Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               ' * SMILES: C([C@H]([C@@H](C(=O)N)O)N)(O)=O NAME: '
               '(3S)-3-hydroxy-L-asparagine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: NC(CC1=CC2=CC=CC=C2C=C1)C(O)=O NAME: '
               '3-naphthalen-2-ylalanine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: CC(NCCCC[C@H](N)C(O)=O)C(O)=O NAME: '
               'N(6)-(1-carboxyethyl)-L-lysine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: N[C@@H](CCCNO)C(O)=O NAME: N(5)-hydroxy-L-ornithine '
               'REASON: CORRECT Has amino acid functional groups and does not '
               'match any standard proteinogenic amino acid\n'
               ' * SMILES: NCCC[C@H](N)C(O)=O NAME: L-ornithine REASON: '
               'CORRECT Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               ' * SMILES: NCCOP(O)(=O)OCC(N)C(O)=O NAME: serine '
               'phosphoethanolamine REASON: CORRECT Has amino acid functional '
               'groups and does not match any standard proteinogenic amino '
               'acid\n'
               ' * SMILES: O=C(O)[C@@H](N)CCCCCCCSC NAME: '
               'L-pentahomomethionine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: OC([C@@H](N)CSC(=O)CCCCCCC)=O NAME: '
               'S-octanoyl-L-cysteine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: OC(=O)CNc1ccc(O)cc1 NAME: '
               'N-(p-hydroxyphenyl)glycine REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               'CC(C)=CC\\C=C(\\C)[C@H]1CN[C@@H]([C@H]1CC(O)=O)C(O)=O NAME: '
               'dainic acid A REASON: CORRECT Has amino acid functional groups '
               'and does not match any standard proteinogenic amino acid\n'
               ' * SMILES: N[C@H](Cc1c[nH]cn1)C(O)=O NAME: D-histidine REASON: '
               'CORRECT Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               ' * SMILES: N[C@H](Cc1ccc(O)c(O)c1)C(O)=O NAME: D-dopa REASON: '
               'CORRECT Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               ' * SMILES: N[C@@H](CS\\C(Cl)=C/Cl)C(O)=O NAME: '
               'S-(trans-1,2-dichlorovinyl)-L-cysteine REASON: CORRECT Has '
               'amino acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: CC(=O)CNCCCCC(N)C(O)=O NAME: N(6)-acetonyllysine '
               'REASON: CORRECT Has amino acid functional groups and does not '
               'match any standard proteinogenic amino acid\n'
               ' * SMILES: N[C@@H]([C@H](O)CC(O)=O)C(O)=O NAME: '
               '(R)-3-hydroxy-L-glutamic acid REASON: CORRECT Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: NC(Cc1ccc(O)c(O)c1)C(O)=O NAME: dopa REASON: '
               'CORRECT Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               'False positives: SMILES: CNC(=N)NCCC[C@H](N)C([O-])=O NAME: '
               'N(omega)-methyl-L-argininate REASON: WRONGLY CLASSIFIED Has '
               'amino acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: OC(=O)C(NCC(O)=O)CCCN=C(N)N NAME: L-Acetopine '
               'REASON: WRONGLY CLASSIFIED Has amino acid functional groups '
               'and does not match any standard proteinogenic amino acid\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(O-18:0/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED Has '
               'amino acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: N[C@@H](CCC(=O)Nc1ccccc1)C(O)=O NAME: '
               'N(5)-phenyl-L-glutamine REASON: WRONGLY CLASSIFIED Has amino '
               'acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(20:1(11Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'WRONGLY CLASSIFIED Has amino acid functional groups and does '
               'not match any standard proteinogenic amino acid\n'
               ' * SMILES: S(=O)(CC[C@H](N)C(O)=O)C[C@H](N)C(O)=O NAME: '
               'Cystathionine sulfoxide REASON: WRONGLY CLASSIFIED Has amino '
               'acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: [O-]C(=O)[C@@H](N)CCCC[N+](C)(C)C NAME: '
               'N-6-Trimethyllysine REASON: WRONGLY CLASSIFIED Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               'COc1cc(CC\\N=C/C=C2C[C@H](NC(=C\\2)C(O)=O)C(O)=O)ccc1O NAME: '
               '3-Methoxytyramine-betaxanthin REASON: WRONGLY CLASSIFIED Has '
               'amino acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC)CO/C=C\\CCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(P-18:0/12:0) REASON: WRONGLY CLASSIFIED Has amino '
               'acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: N[C@@H](CCC([O-])=O)C([O-])=O NAME: L-glutamate(2-) '
               'REASON: WRONGLY CLASSIFIED Has amino acid functional groups '
               'and does not match any standard proteinogenic amino acid\n'
               ' * SMILES: S(=O)(CCCCNC(SC[C@H](N)C(O)=O)=S)C NAME: '
               'sulforaphane-cysteine REASON: WRONGLY CLASSIFIED Has amino '
               'acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: N[C@H](Cc1ccc([O])cc1)C(O)=O NAME: D-tyrosinyl '
               'radical REASON: WRONGLY CLASSIFIED Has amino acid functional '
               'groups and does not match any standard proteinogenic amino '
               'acid\n'
               ' * SMILES: S(C[C@H](N)C(O)=O)C=C NAME: S-vinylcysteine REASON: '
               'WRONGLY CLASSIFIED Has amino acid functional groups and does '
               'not match any standard proteinogenic amino acid\n'
               ' * SMILES: CNC(C(C)C)C(O)=O NAME: N-methylvaline REASON: '
               'WRONGLY CLASSIFIED Has amino acid functional groups and does '
               'not match any standard proteinogenic amino acid\n'
               ' * SMILES: C[C@@H](NCCC(O)=O)C(O)=O NAME: (R)-beta-alanopine '
               'REASON: WRONGLY CLASSIFIED Has amino acid functional groups '
               'and does not match any standard proteinogenic amino acid\n'
               ' * SMILES: C(C[C@@H](C([O-])=O)N)(C([O-])=O)C([O-])=O NAME: '
               'gamma-carboxy-L-glutamate(3-) REASON: WRONGLY CLASSIFIED Has '
               'amino acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: OC(=O)C[C@@H]1CC[C@H](N1)C(O)=O NAME: '
               '(5S)-5-(carboxymethyl)-L-proline REASON: WRONGLY CLASSIFIED '
               'Has amino acid functional groups and does not match any '
               'standard proteinogenic amino acid\n'
               ' * SMILES: '
               'O=C1C(=C(C=2C3=C(C=CC=C3)NC2)C(C14N[C@H](C(=O)O)CC5=C4NC=6C=CC=CC56)=O)C=7C8=C(C=CC=C8)NC7 '
               'NAME: Pityriarubin A REASON: WRONGLY CLASSIFIED Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: OC(=O)CC(\\N=C/C=C1CC(NC(=C\\1)C(O)=O)C(O)=O)C(O)=O '
               'NAME: Miraxanthin-II REASON: WRONGLY CLASSIFIED Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               'N[C@@H](Cc1cc(I)c(Oc2ccc(OS(O)(=O)=O)c(I)c2)c(I)c1)C(O)=O '
               "NAME: 3,3',5-triiodo-L-thyronine sulfate REASON: WRONGLY "
               'CLASSIFIED Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC(=O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PKOOA-PS REASON: WRONGLY CLASSIFIED Has amino acid '
               'functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               ' * SMILES: '
               '[NH3+][C@@H](CCCCNN[C@@H](CCC([O-])=O)C([O-])=O)C([O-])=O '
               'NAME: 1-L-glutamo-2-N(6-)L-lysinohydrazine(2-) REASON: WRONGLY '
               'CLASSIFIED Has amino acid functional groups and does not match '
               'any standard proteinogenic amino acid\n'
               ' * SMILES: N.OC(=O)CNCP(O)(O)=O NAME: Glyphosate-monoammonium '
               'REASON: WRONGLY CLASSIFIED Has amino acid functional groups '
               'and does not match any standard proteinogenic amino acid\n'
               ' * SMILES: '
               'N[C@@H](CCCC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12)C(O)=O '
               'NAME: L-2-Aminoadipate adenylate REASON: WRONGLY CLASSIFIED '
               'Has amino acid functional groups and does not match any '
               'standard proteinogenic amino acid\n'
               ' * SMILES: '
               'C1O[C@]21[C@]3([C@@]4([C@@]([C@@H]([C@@H](C)C([C@H]4O)=O)SC[C@H](N)C(O)=O)(O[C@@]2([C@H](O)C3)[H])[H])CO)C '
               'NAME: DON-10-S-cysteine REASON: WRONGLY CLASSIFIED Has amino '
               'acid functional groups and does not match any standard '
               'proteinogenic amino acid\n'
               'False negatives: SMILES: CSCCCCC(N(O)O)C(O)=O NAME: '
               'N,N-dihydroxydihomomethionine REASON: MISSED No free amine '
               'group detected\n'
               ' * SMILES: '
               'C(NC(CCNC(=O)[C@@H](C(COP(OC[C@@H](C(O)=O)N)(=O)O)(C)C)O)=O)CS '
               "NAME: O-(pantetheine-4'-phosphoryl)serine REASON: MISSED "
               'Contains peptide bond; likely a peptide rather than a single '
               'amino acid\n'
               ' * SMILES: '
               'N1(C([C@H](C1)NC(/C(/C=2C=CC(OCC[C@@H](C(=O)O)N)=CC2)=N\\O)=O)=O)[C@@H](C(O)=O)C3=CC=C(C=C3)O '
               'NAME: isonocardicin A REASON: MISSED Contains peptide bond; '
               'likely a peptide rather than a single amino acid\n'
               ' * SMILES: '
               'CC(=O)N[C@H]1[C@@H](OC[C@H](N)C(O)=O)O[C@H](CO)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O '
               'NAME: '
               'O-(3-O-beta-D-galactosyl-N-acetyl-alpha-D-galactosaminyl)-L-serine '
               'REASON: MISSED Contains peptide bond; likely a peptide rather '
               'than a single amino acid\n'
               ' * SMILES: N[C@@H](CNC(N)=O)C(O)=O NAME: L-Albizziine REASON: '
               'MISSED Contains peptide bond; likely a peptide rather than a '
               'single amino acid\n'
               ' * SMILES: CNC(=O)C[C@H](N)C(O)=O NAME: '
               'N(4)-methyl-L-asparagine REASON: MISSED Contains peptide bond; '
               'likely a peptide rather than a single amino acid\n'
               ' * SMILES: C(N(C(=NO)NC)O)CC[C@@H](C(=O)[O-])[NH3+] NAME: '
               "N(delta),N(omega')-dihydroxy-N(omega)-methyl-L-arginine "
               'zwitterion REASON: MISSED No typical amino acid backbone '
               'detected\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H](CO)O[C@H]1NC(=O)C[C@H](N)C(O)=O '
               'NAME: '
               'N(4)-{alpha-D-mannosyl-(1->6)-[alpha-D-mannosyl-(1->2)-alpha-D-mannosyl-(1->2)-alpha-D-mannosyl-(1->3)]-beta-D-mannosyl-(1->4)-N-acetyl-beta-D-glucosaminyl-(1->4)-N-acetyl-beta-D-glucosaminyl}-L-asparagine '
               'REASON: MISSED Contains peptide bond; likely a peptide rather '
               'than a single amino acid\n'
               ' * SMILES: N[C@@H](CC(O)=O)C(N)=O NAME: L-aspartic 1-amide '
               'REASON: MISSED No typical amino acid backbone detected\n'
               ' * SMILES: '
               'N[C@@H](CCC[C@@H](NC(=O)CC[C@@H](N)C(O)=O)C(O)=O)C(O)=O NAME: '
               'gamma-D-glutamyl-meso-diaminopimelic acid REASON: MISSED '
               'Contains peptide bond; likely a peptide rather than a single '
               'amino acid\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Molecular weight 358.1 out of '
                                               'range for typical amino acids'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Molecular weight 364.1 out of '
                                               'range for typical amino acids'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No typical alpha-amino acid '
                                               'backbone detected'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Molecular weight 359.3 out of '
                                               'range for typical amino acids'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Molecular weight 757.4 out of '
                                               'range for typical amino acids'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Molecular weight 504.2 out of '
                                               'range for typical amino acids'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Molecular weight 991.7 out of '
                                               'range for typical amino acids'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No carboxylic acid group '
                                               'detected'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No carboxylic acid group '
                                               'detected'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Molecular weight 358.2 out of '
                                               'range for typical amino '
                                               'acids'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@](N)(CS[C@H](\\C=C\\C=C\\C=C/C\\C=C/CCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O',
                                      'name': '18-carboxy-19,20-dinor-leukotriene '
                                              'E4',
                                      'reason': 'Molecular weight 441.2 out of '
                                                'range for typical amino '
                                                'acids'},
                                  {   'smiles': 'C(NC(CCNC(=O)[C@@H](C(COP(OC[C@@H](C(O)=O)N)(=O)O)(C)C)O)=O)CS',
                                      'name': "O-(pantetheine-4'-phosphoryl)serine",
                                      'reason': 'Molecular weight 445.1 out of '
                                                'range for typical amino '
                                                'acids'},
                                  {   'smiles': 'N1(C([C@H](C1)NC(/C(/C=2C=CC(OCC[C@@H](C(=O)O)N)=CC2)=N\\O)=O)=O)[C@@H](C(O)=O)C3=CC=C(C=C3)O',
                                      'name': 'isonocardicin A',
                                      'reason': 'Molecular weight 500.2 out of '
                                                'range for typical amino '
                                                'acids'},
                                  {   'smiles': 'CC(=O)N[C@H]1[C@@H](OC[C@H](N)C(O)=O)O[C@H](CO)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O',
                                      'name': 'O-(3-O-beta-D-galactosyl-N-acetyl-alpha-D-galactosaminyl)-L-serine',
                                      'reason': 'Molecular weight 470.2 out of '
                                                'range for typical amino '
                                                'acids'},
                                  {   'smiles': 'N[C@@H](CNC(N)=O)C(O)=O',
                                      'name': 'L-Albizziine',
                                      'reason': 'Contains peptide bond; likely '
                                                'a peptide rather than a '
                                                'single amino acid'},
                                  {   'smiles': 'CNC(=O)C[C@H](N)C(O)=O',
                                      'name': 'N(4)-methyl-L-asparagine',
                                      'reason': 'Contains peptide bond; likely '
                                                'a peptide rather than a '
                                                'single amino acid'},
                                  {   'smiles': 'N[C@@H](CCSC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(O)ncnc12)C(O)=O',
                                      'name': 'S-inosyl-L-homocysteine',
                                      'reason': 'Molecular weight 385.1 out of '
                                                'range for typical amino '
                                                'acids'},
                                  {   'smiles': 'C(N(C(=NO)NC)O)CC[C@@H](C(=O)[O-])[NH3+]',
                                      'name': "N(delta),N(omega')-dihydroxy-N(omega)-methyl-L-arginine "
                                              'zwitterion',
                                      'reason': 'No typical alpha-amino acid '
                                                'backbone detected'},
                                  {   'smiles': 'CC(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H](CO)O[C@H]1NC(=O)C[C@H](N)C(O)=O',
                                      'name': 'N(4)-{alpha-D-mannosyl-(1->6)-[alpha-D-mannosyl-(1->2)-alpha-D-mannosyl-(1->2)-alpha-D-mannosyl-(1->3)]-beta-D-mannosyl-(1->4)-N-acetyl-beta-D-glucosaminyl-(1->4)-N-acetyl-beta-D-glucosaminyl}-L-asparagine',
                                      'reason': 'Molecular weight 1348.5 out '
                                                'of range for typical amino '
                                                'acids'},
                                  {   'smiles': 'N[C@@H](CC(O)=O)C(N)=O',
                                      'name': 'L-aspartic 1-amide',
                                      'reason': 'No typical alpha-amino acid '
                                                'backbone detected'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning. In the previous approach we noted '
                 'three main issues:\n'
                 '\n'
                 '1. The free‐amine SMARTS was too strict. In molecules like '
                 'N,N–dihydroxydihomomethionine the amino nitrogen is '
                 'substituted (e.g. N(O)O) and did not match the “[NX3;H2,H1]” '
                 'query. We therefore relax that check so that any trivalent '
                 'nitrogen (i.e. [NX3]) directly attached to an sp³‐carbon is '
                 'accepted.\n'
                 '\n'
                 '2. Some false negatives arose because the “typical α–amino '
                 'acid” pattern was not found. In many cases the best “anchor” '
                 'is an α–carbon attached both to a carboxyl group and to a '
                 'nearby nitrogen. Thus, we now search for a pattern that '
                 'explicitly requires an sp³–carbon bound to both C(=O)[O;…] '
                 'and an [NX3]. In this way, even substituted amines '
                 '(N–methyl, N–hydroxy, etc.) are recognized as part of the '
                 'amino acid backbone.\n'
                 '\n'
                 '3. Finally, many false positives were due to classifying '
                 'peptides (or even larger species with extra functional '
                 'groups such as phosphorus or multiple amide bonds) as single '
                 'amino acids. To avoid that we (a) add an exclusion using a '
                 'peptide–bond SMARTS (C(=O)N[C;X4]) and (b) require that the '
                 'overall molecular weight is within a “typical amino acid” '
                 'range (roughly 75–350 Da).\n'
                 '\n'
                 'The code below implements these revised ideas. (Again, if '
                 'the task turns out too hard the function may return (None, '
                 'None), but here we use our best heuristics.) \n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 522,
    'num_false_positives': 873,
    'num_true_negatives': 140744,
    'num_false_negatives': 161,
    'num_negatives': None,
    'precision': 0.3741935483870968,
    'recall': 0.7642752562225475,
    'f1': 0.5024061597690087,
    'accuracy': 0.9927336612789881,
    'negative_predictive_value': 0.9988573861821795}