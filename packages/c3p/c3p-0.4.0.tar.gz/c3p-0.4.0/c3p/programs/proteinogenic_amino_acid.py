"""
Classifies: CHEBI:83813 proteinogenic amino acid
"""
#!/usr/bin/env python3
"""
Classifies: proteinogenic amino acid
Defined as one of the 23 canonical α–amino acids (including glycine, L–proline, selenocysteine,
pyrrolysine, and N–formylmethionine) incorporated into proteins by translation.
This implementation verifies that:
  - The molecule parses correctly.
  - It contains only allowed heavy atoms (C, N, O, S, and Se) and is small (≤25 heavy atoms).
  - It contains one of the free α–amino acid motifs (using SMARTS patterns for canonical, glycine, and proline).
  - For canonical motifs (and for proline) the free –NH2 and –COOH groups are unsubstituted and
    the α–carbon connectivity is as expected.
  - For chiral (non–glycine) amino acids, the α–carbon must have the L configuration (CIP code “S”).
If any check fails the function returns False with a reason.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_proteinogenic_amino_acid(smiles: str):
    """
    Determines if a molecule is a proteinogenic amino acid based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a proteinogenic amino acid, False otherwise.
        str: Explanation of the classification decision.
    """
    # Parse SMILES and remove explicit hydrogens (for consistency)
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    mol = Chem.RemoveHs(mol)
    
    # Check allowed heavy atoms (C, N, O, S, Se)
    allowed_atomic_nums = {6, 7, 8, 16, 34}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 1:
            continue
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Disallowed element found: atomic number {atom.GetAtomicNum()}"
    
    # Check molecule size: free amino acids are small (≤25 heavy atoms)
    heavy_atom_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() > 1)
    if heavy_atom_count > 25:
        return False, "Molecule is too large to be a single proteinogenic amino acid"
    
    # Assign stereochemistry so that CIP codes (R/S) are computed.
    Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # Define SMARTS patterns along with type tags.
    # For canonical amino acids (chiral, non glycine):
    #    Expected order: Atom0 = α–carbon, Atom1 = free amino nitrogen, Atom2 = carboxyl carbon.
    # For glycine, pattern "NCC(=O)[O]":
    #    Expected order: Atom0 = amino nitrogen, Atom1 = α–carbon, Atom2 = carboxyl carbon.
    # For proline, the pattern covers the cyclic structure; here we assume the chiral (α–carbon)
    #    is at index 2.
    patterns = [
        {"smarts": "[C@H](N)C(=O)[O]", "type": "canonical"},
        {"smarts": "[C@@H](N)C(=O)[O]", "type": "canonical"},
        {"smarts": "NCC(=O)[O]", "type": "glycine"},
        {"smarts": "OC(=O)[C@H]1CCCN1", "type": "proline"},
        {"smarts": "OC(=O)[C@@H]1CCCN1", "type": "proline"},
    ]
    
    # Iterate through each pattern and try to match.
    for entry in patterns:
        patt = Chem.MolFromSmarts(entry["smarts"])
        if patt is None:
            continue
        matches = mol.GetSubstructMatches(patt, useChirality=True)
        if not matches:
            continue
        
        # Evaluate each match.
        for match in matches:
            if entry["type"] in ("canonical", "glycine"):
                # Ensure the match contains at least three atoms.
                if len(match) < 3:
                    continue
                
                if entry["type"] == "canonical":
                    # For canonical patterns, the order is: [0]: α–carbon, [1]: amino nitrogen, [2]: carboxyl carbon.
                    alpha_idx = match[0]
                    amino_idx = match[1]
                    carboxyl_idx = match[2]
                    expected_alpha_degree = 3  # free amino acid: α–carbon has three heavy neighbors.
                else:  # glycine
                    # For glycine pattern "NCC(=O)[O]", order: [0]: amino nitrogen, [1]: α–carbon, [2]: carboxyl carbon.
                    amino_idx = match[0]
                    alpha_idx = match[1]
                    carboxyl_idx = match[2]
                    expected_alpha_degree = 2  # glycine: no side chain.
                
                # (a) Check amino nitrogen: it should be free (only attached to α–carbon).
                amino_atom = mol.GetAtomWithIdx(amino_idx)
                amino_neighbors = [nbr.GetIdx() for nbr in amino_atom.GetNeighbors() if nbr.GetAtomicNum() > 1]
                if set(amino_neighbors) != {alpha_idx}:
                    continue  # amino nitrogen appears substituted.
                
                # (b) Check carboxyl carbon connectivity: should be bonded to α–carbon and two oxygens,
                # with one O in a double bond and one in a single bond.
                carboxyl_atom = mol.GetAtomWithIdx(carboxyl_idx)
                nbrs = [nbr for nbr in carboxyl_atom.GetNeighbors() if nbr.GetAtomicNum() > 1]
                if len(nbrs) != 3:
                    continue
                oxygens = [nbr for nbr in nbrs if nbr.GetAtomicNum() == 8]
                if len(oxygens) != 2:
                    continue
                dbl_found = False
                sgl_found = False
                for o in oxygens:
                    bond = mol.GetBondBetweenAtoms(carboxyl_atom.GetIdx(), o.GetIdx())
                    if bond is None:
                        continue
                    if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                        dbl_found = True
                    elif bond.GetBondType() == Chem.rdchem.BondType.SINGLE:
                        sgl_found = True
                if not (dbl_found and sgl_found):
                    continue
                
                # (c) Check α–carbon connectivity: it should have the expected number of heavy atom neighbors.
                alpha_atom = mol.GetAtomWithIdx(alpha_idx)
                alpha_neighbors = [nbr.GetIdx() for nbr in alpha_atom.GetNeighbors() if nbr.GetAtomicNum() > 1]
                if len(alpha_neighbors) != expected_alpha_degree:
                    continue
                
                # (d) For canonical amino acids (non–glycine), check that the α–carbon has L configuration,
                # i.e. CIP code should be "S". (Glycine is achiral.)
                if entry["type"] == "canonical":
                    if not alpha_atom.HasProp('_CIPCode'):
                        continue
                    if alpha_atom.GetProp('_CIPCode') != "S":
                        continue  # wrong configuration (likely D amino acid)
                        
                return True, f"Matches canonical amino acid criteria: {entry['smarts']}"
                
            elif entry["type"] == "proline":
                # For proline, use the match and assume the cyclic backbone.
                # We assume that the chiral (α–carbon) appears at index 2 in the substructure match.
                if len(match) < 3:
                    continue
                alpha_idx = match[2]
                alpha_atom = mol.GetAtomWithIdx(alpha_idx)
                
                # For proline, we also check that the free carboxyl (or its ester equivalent) and amino groups are not substituted.
                # We will simply check that the amino nitrogen (which is in the ring) is not extra substituted.
                # Identify the amino nitrogen in the ring.
                ring_nitrogens = [nbr for nbr in alpha_atom.GetNeighbors() if nbr.GetAtomicNum() == 7]
                valid_ring_nitrogen = False
                for n in ring_nitrogens:
                    n_neighbors = [nbr.GetIdx() for nbr in n.GetNeighbors() if nbr.GetAtomicNum() > 1]
                    # If the nitrogen is connected only to atoms within the ring (typically 2 heavy neighbors) then accept.
                    if len(n_neighbors) <= 2:
                        valid_ring_nitrogen = True
                if not valid_ring_nitrogen:
                    continue
                    
                # Also enforce L configuration (α–carbon CIP code "S")
                if not alpha_atom.HasProp('_CIPCode'):
                    continue
                if alpha_atom.GetProp('_CIPCode') != "S":
                    continue
                    
                return True, f"Matches canonical amino acid criteria (proline): {entry['smarts']}"
    
    return False, "No appropriate free α–amino acid motif (with unsubstituted amino and carboxyl groups and L configuration) found"

# For ad-hoc testing when run as a script:
if __name__ == "__main__":
    test_smiles = {
        "L-glutamic acid": "N[C@@H](CCC(O)=O)C(O)=O",
        "L-histidine": "N[C@@H](Cc1c[nH]cn1)C(O)=O",
        "L-phenylalanine-d5": "OC(=O)[C@@H](N)CC1=C(C(=C(C(=C1[2H])[2H])[2H])[2H])[2H]",
        "L-arginine-d7": "OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H]",
        "L-proline": "OC(=O)[C@@H]1CCCN1",
        "L-arginine": "N[C@@H](CCCNC(N)=N)C(O)=O",
        "L-leucine": "CC(C)C[C@H](N)C(O)=O",
        "L-isoleucine": "OC([C@H]([C@H](CC)C)N)=O",
        "L-valine": "CC(C)[C@H](N)C(O)=O",
        "L-alanine": "C[C@H](N)C(O)=O",
        "L-valine-d8": "OC(=O)[C@@](N)(C(C([2H])([2H])[2H])(C([2H])([2H])[2H])[2H])[2H]",
        "L-asparagine": "N[C@@H](CC(N)=O)C(O)=O",
        "L-methionine-d3": "S(CC[C@H](N)C(O)=O)C([2H])([2H])[2H]",
        "L-glutamine": "N[C@@H](CCC(N)=O)C(O)=O",
        "L-tyrosine-d4": "OC(=O)[C@@H](N)CC1=C(C(=C(O)C(=C1[2H])[2H])[2H])[2H]",
        "L-aspartic acid-d7": "O(C(=O)[C@@](N([2H])[2H])(C(C(O[2H])=O)([2H])[2H])[2H])[2H]",
        "L-lysine": "NCCCC[C@H](N)C(O)=O",
        "L-serine": "N[C@@H](CO)C(O)=O",
        "L-pyrrolysine": "C(=O)([C@@H](N)CCCCNC([C@H]1[C@@H](CC=N1)C)=O)O",
        "glycine-13C2,15N": "O[13C](=O)[13CH2][15NH2]",
        "L-threonine": "C[C@@H](O)[C@H](N)C(O)=O",
        "L-cysteine": "N[C@@H](CS)C(O)=O",
        "glycine-d5": "C(C(N([2H])[2H])([2H])[2H])(=O)O[2H]",
        "L-aspartic acid": "N[C@@H](CC(O)=O)C(O)=O",
        "L-leucine-d3": "OC(=O)[C@@H](N)CC(C([2H])([2H])[2H])C",
        "L-methionine": "CSCC[C@H](N)C(O)=O",
        # Examples noted as false positives previously:
        "gamma-Glu-Trp(1-)": "[NH3+][C@H](C([O-])=O)CCC(=O)N[C@H](C(=O)[O-])CC1=CNC2=C1C=CC=C2",
        "4-dimethylamino-L-phenylalanine zwitterion": "C1=CC(=CC=C1C[C@@H](C([O-])=O)[NH3+])N(C)C",
        "D-citrulline": "N[C@H](CCCNC(N)=O)C(O)=O",
    }
    
    for name, smi in test_smiles.items():
        result, reason = is_proteinogenic_amino_acid(smi)
        print(f"{name}: {result} ({reason})")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:83813',
                          'name': 'proteinogenic amino acid',
                          'definition': 'Any of the 23 alpha-amino acids that '
                                        'are precursors to proteins, and are '
                                        'incorporated into proteins during '
                                        'translation. The group includes the '
                                        '20 amino acids encoded by the nuclear '
                                        'genes of eukaryotes together with '
                                        'selenocysteine, pyrrolysine, and '
                                        'N-formylmethionine. Apart from '
                                        'glycine, which is non-chiral, all '
                                        'have L configuration.',
                          'parents': ['CHEBI:33709'],
                          'xrefs': ['Wikipedia:Proteinogenic_amino_acid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 166,
                           'log_lines_of_code': 5.111987788356544,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 6,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 4,
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
                           'methods_called': [   'GetIdx',
                                                 'GetBondType',
                                                 'HasProp',
                                                 'MolFromSmarts',
                                                 'GetProp',
                                                 'RemoveHs',
                                                 'GetAtoms',
                                                 'items',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'AssignStereochemistry',
                                                 'MolFromSmiles'],
                           'methods_called_count': 15,
                           'smarts_strings': ['entry["smarts"]'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_proteinogenic_amino_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Disallowed element found: '
                                          'atomic number '
                                          '{atom.GetAtomicNum()}"',
                                          'False, "Molecule is too large to be '
                                          'a single proteinogenic amino acid"',
                                          'True, f"Matches canonical amino '
                                          'acid criteria: {entry[\'smarts\']}"',
                                          'True, f"Matches canonical amino '
                                          'acid criteria (proline): '
                                          '{entry[\'smarts\']}"',
                                          'False, "No appropriate free α–amino '
                                          'acid motif (with unsubstituted '
                                          'amino and carboxyl groups and L '
                                          'configuration) found"'],
                           'returns_count': 6,
                           'complexity': 6.6223975576713086},
    'message': '\n'
               'Attempt failed: F1 score of 0.03893294881038212 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: N[C@@H](CCC(O)=O)C(O)=O NAME: '
               'L-glutamic acid REASON: CORRECT Matches canonical amino acid '
               'criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: N[C@@H](Cc1c[nH]cn1)C(O)=O NAME: L-histidine '
               'REASON: CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'OC(=O)[C@@H](N)CC1=C(C(=C(C(=C1[2H])[2H])[2H])[2H])[2H] NAME: '
               'L-phenylalanine-d5 REASON: CORRECT Matches canonical amino '
               'acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H] '
               'NAME: L-arginine-d7 REASON: CORRECT Matches canonical amino '
               'acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: OC(=O)[C@@H]1CCCN1 NAME: L-proline REASON: CORRECT '
               'Matches canonical amino acid criteria (proline): '
               'OC(=O)[C@@H]1CCCN1\n'
               ' * SMILES: N[C@@H](CCCNC(N)=N)C(O)=O NAME: L-arginine REASON: '
               'CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: CC(C)C[C@H](N)C(O)=O NAME: L-leucine REASON: '
               'CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: OC([C@H]([C@H](CC)C)N)=O NAME: L-isoleucine REASON: '
               'CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: CC(C)[C@H](N)C(O)=O NAME: L-valine REASON: CORRECT '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: C[C@H](N)C(O)=O NAME: L-alanine REASON: CORRECT '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'OC(=O)[C@@](N)(C(C([2H])([2H])[2H])(C([2H])([2H])[2H])[2H])[2H] '
               'NAME: L-valine-d8 REASON: CORRECT Matches canonical amino acid '
               'criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: N[C@@H](CC(N)=O)C(O)=O NAME: L-asparagine REASON: '
               'CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: S(CC[C@H](N)C(O)=O)C([2H])([2H])[2H] NAME: '
               'L-methionine-d3 REASON: CORRECT Matches canonical amino acid '
               'criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: N[C@@H](CCC(N)=O)C(O)=O NAME: L-glutamine REASON: '
               'CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'OC(=O)[C@@H](N)CC1=C(C(=C(O)C(=C1[2H])[2H])[2H])[2H] NAME: '
               'L-tyrosine-d4 REASON: CORRECT Matches canonical amino acid '
               'criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O(C(=O)[C@@](N([2H])[2H])(C(C(O[2H])=O)([2H])[2H])[2H])[2H] '
               'NAME: L-aspartic acid-d7 REASON: CORRECT Matches canonical '
               'amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: NCCCC[C@H](N)C(O)=O NAME: L-lysine REASON: CORRECT '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'OC(=O)[C@]1(NC(C(C1([2H])[2H])([2H])[2H])([2H])[2H])[2H] NAME: '
               'L-proline-d7 REASON: CORRECT Matches canonical amino acid '
               'criteria (proline): OC(=O)[C@@H]1CCCN1\n'
               ' * SMILES: N[C@@H](CO)C(O)=O NAME: L-serine REASON: CORRECT '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: C(=O)([C@@H](N)CCCCNC([C@H]1[C@@H](CC=N1)C)=O)O '
               'NAME: L-pyrrolysine REASON: CORRECT Matches canonical amino '
               'acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: O[13C](=O)[13CH2][15NH2] NAME: glycine-13C2,15N '
               'REASON: CORRECT Matches canonical amino acid criteria: '
               'NCC(=O)[O]\n'
               ' * SMILES: C[C@@H](O)[C@H](N)C(O)=O NAME: L-threonine REASON: '
               'CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: N[C@@H](CS)C(O)=O NAME: L-cysteine REASON: CORRECT '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: C(C(N([2H])[2H])([2H])[2H])(=O)O[2H] NAME: '
               'glycine-d5 REASON: CORRECT Matches canonical amino acid '
               'criteria: NCC(=O)[O]\n'
               ' * SMILES: N[C@@H](CC(O)=O)C(O)=O NAME: L-aspartic acid '
               'REASON: CORRECT Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               'False positives: SMILES: '
               '[NH3+][C@H](C([O-])=O)CCC(=O)N[C@H](C(=O)[O-])CC1=CNC2=C1C=CC=C2 '
               'NAME: gamma-Glu-Trp(1-) REASON: WRONGLY CLASSIFIED Matches '
               'canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: C1=CC(=CC=C1C[C@@H](C([O-])=O)[NH3+])N(C)C NAME: '
               '4-dimethylamino-L-phenylalanine zwitterion REASON: WRONGLY '
               'CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: N[C@H](CCCNC(N)=O)C(O)=O NAME: D-citrulline REASON: '
               'WRONGLY CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: [NH3+][C@@H](CO)C([O-])=O NAME: L-serine zwitterion '
               'REASON: WRONGLY CLASSIFIED Matches canonical amino acid '
               'criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O=C([O-])[C@@H](N)[C@@H](C)[NH2+]C(CC([O-])=O)C(=O)[O-] NAME: '
               'N(3)-1,2-dicarboxyethyl-diaminobutanoate REASON: WRONGLY '
               'CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCCN=C(N)N)C(=O)N1[C@H](CCC1)C(O)=O '
               'NAME: Arg-Cys-Pro REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria (proline): OC(=O)[C@H]1CCCN1\n'
               ' * SMILES: [O-]C([C@H](CCCCN)[NH3+])=O NAME: L-lysine '
               'zwitterion REASON: WRONGLY CLASSIFIED Matches canonical amino '
               'acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: [H]C(=O)Nc1ccc(O)cc1C(=O)C[C@H](N)C(O)=O NAME: '
               '5-hydroxy-N-formyl-L-kynurenine REASON: WRONGLY CLASSIFIED '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: N[C@@H](CSSC[C@H](N)C(O)=O)C(O)=O NAME: L-cystine '
               'REASON: WRONGLY CLASSIFIED Matches canonical amino acid '
               'criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'C[C@H](N)C(=O)N[C@@H](CC(O)=O)C(=O)N1CCC[C@H]1C(O)=O NAME: '
               'Ala-Asp-Pro REASON: WRONGLY CLASSIFIED Matches canonical amino '
               'acid criteria (proline): OC(=O)[C@@H]1CCCN1\n'
               ' * SMILES: N[C@@H]([C@H](O)C([O-])=O)C([O-])=O NAME: '
               '(3S)-3-hydroxy-L-aspartate(2-) REASON: WRONGLY CLASSIFIED '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: C(=O)([C@@H](N)CCC(NC=1C=CC2=C(C1)C=CC=C2)=O)[O-] '
               'NAME: N-(gamma-L-glutamyl)-2-naphthylamine(1-) REASON: WRONGLY '
               'CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: C[C@@H]([C@H]([NH3+])C([O-])=O)C([O-])=O NAME: '
               'threo-3-methyl-L-aspartate(1-) REASON: WRONGLY CLASSIFIED '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CCCCN NAME: '
               'Ala-Lys-Pro REASON: WRONGLY CLASSIFIED Matches canonical amino '
               'acid criteria (proline): OC(=O)[C@H]1CCCN1\n'
               ' * SMILES: [O-]C([C@@](C[C@@H](C([O-])=O)[NH3+])(O)C)=O NAME: '
               '(2S,4R)-4-hydroxy-4-methylglutamate(1-) REASON: WRONGLY '
               'CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CCC(O)=O '
               'NAME: Thr-Glu-Pro REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria (proline): OC(=O)[C@H]1CCCN1\n'
               ' * SMILES: C(=O)([C@@H]([NH3+])CC#C)[O-] NAME: '
               'L-propargylglycine zwitterion REASON: WRONGLY CLASSIFIED '
               'Matches canonical amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: NC(=[NH2+])NOCC[C@H]([NH3+])C([O-])=O NAME: '
               'L-canavanine(1+) REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: [NH3+][C@@H](CCC[C@H]([NH3+])C([O-])=O)C([O-])=O '
               'NAME: (2S,6S)-2,6-diaminopimelic acid dizwitterion REASON: '
               'WRONGLY CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC2=CC=CC=C2)CO '
               'NAME: Phe-Ser-Pro REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria (proline): OC(=O)[C@H]1CCCN1\n'
               ' * SMILES: [NH3+][C@@H](Cn1cccn1)C([O-])=O NAME: '
               '3-(pyrazol-1-yl)-L-alanine zwitterion REASON: WRONGLY '
               'CLASSIFIED Matches canonical amino acid criteria: '
               '[C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)[C@H](CC)C '
               'NAME: Asn-Ile-Pro REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria (proline): OC(=O)[C@H]1CCCN1\n'
               ' * SMILES: OC(=O)[C@@H](N)CC(N[C@H](C(O)=O)CCC(=O)O)=O NAME: '
               'beta-Asp-Glu REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: [C@@H](N)(C(=O)O)CC=1C=CC(=CC1)C=2N=NC(=NN2)CC '
               'NAME: Tet2-Et REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria: [C@H](N)C(=O)[O]\n'
               ' * SMILES: '
               'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC(O)=O '
               'NAME: Asp-Asp-Pro REASON: WRONGLY CLASSIFIED Matches canonical '
               'amino acid criteria (proline): OC(=O)[C@H]1CCCN1\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No appropriate free α–amino '
                                               'acid motif (with unsubstituted '
                                               'amino and carboxyl groups and '
                                               'L configuration) found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'Disallowed element found: '
                                               'atomic number 15'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'Molecule is too large to be a '
                                               'single proteinogenic amino '
                                               'acid'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Molecule is too large to be a '
                                               'single proteinogenic amino '
                                               'acid'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Molecule is too large to be a '
                                               'single proteinogenic amino '
                                               'acid'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Molecule is too large to be a '
                                               'single proteinogenic amino '
                                               'acid'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'Disallowed element found: '
                                               'atomic number 9'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'Molecule is too large to be a '
                                               'single proteinogenic amino '
                                               'acid'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No appropriate free α–amino '
                                               'acid motif (with unsubstituted '
                                               'amino and carboxyl groups and '
                                               'L configuration) found'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Molecule is too large to be a '
                                               'single proteinogenic amino '
                                               'acid'}],
    'sample_false_negatives': [   {   'smiles': 'OC(=O)[C@](N([2H])[2H])(C(C(CN=C(N)N)([2H])[2H])([2H])[2H])[2H]',
                                      'name': 'L-arginine-d7',
                                      'reason': 'No appropriate free α–amino '
                                                'acid motif (with '
                                                'unsubstituted amino and '
                                                'carboxyl groups and L '
                                                'configuration) found'},
                                  {   'smiles': 'OC(=O)[C@@H]1CCCN1',
                                      'name': 'L-proline',
                                      'reason': 'No appropriate free α–amino '
                                                'acid motif (with '
                                                'unsubstituted amino and '
                                                'carboxyl groups and L '
                                                'configuration) found'},
                                  {   'smiles': 'OC(=O)[C@]1(NC(C(C1([2H])[2H])([2H])[2H])([2H])[2H])[2H]',
                                      'name': 'L-proline-d7',
                                      'reason': 'No appropriate free α–amino '
                                                'acid motif (with '
                                                'unsubstituted amino and '
                                                'carboxyl groups and L '
                                                'configuration) found'},
                                  {   'smiles': 'N[C@@H](CS)C(O)=O',
                                      'name': 'L-cysteine',
                                      'reason': 'No appropriate free α–amino '
                                                'acid motif (with '
                                                'unsubstituted amino and '
                                                'carboxyl groups and L '
                                                'configuration) found'}],
    'attempt': 4,
    'reasoning': 'Below is one possible solution. In my revised approach I '
                 'still begin by checking that the molecule only contains '
                 'allowed atoms and is small enough to be a free amino acid. '
                 'Then I use a set of SMARTS patterns for canonical free amino '
                 'acids, glycine, and proline. In addition to the '
                 'connectivity‐checks already present in the previous code, I '
                 'also assign stereochemistry and look up the CIP code for the '
                 'chiral (α–carbon) atom. For “true” proteinogenic (L‐) amino '
                 'acids (except for glycine, which is achiral) the CIP code '
                 'should be "S". (Molecules such as D–amino acids or other '
                 'erroneously substituted species will fail one or more of '
                 'these criteria.) \n'
                 '\n'
                 'Below is the complete Python code in one block.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 747,
    'num_true_negatives': 141526,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.02987012987012987,
    'recall': 0.8518518518518519,
    'f1': 0.05771643663739021,
    'accuracy': 0.9947224174279691,
    'negative_predictive_value': 0.9999717374408252}