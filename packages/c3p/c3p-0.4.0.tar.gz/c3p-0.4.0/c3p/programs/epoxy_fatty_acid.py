"""
Classifies: CHEBI:61498 epoxy fatty acid
"""
"""
Classifies: epoxy fatty acid
Definition: A heterocyclic fatty acid containing an epoxide ring as part of its structure.
A valid epoxy fatty acid must:
  - Have a carboxylic acid group (fatty acid functionality)
  - Contain a long, largely linear aliphatic chain (here we check that the chain 
    attached at the acid end has a sufficient number of allowed carbon atoms)
  - Contain at least one epoxide ring, defined as a three‐membered cycle [C;r3][O;r3][C;r3]
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_epoxy_fatty_acid(smiles: str):
    """
    Determines if a molecule is an epoxy fatty acid based on its SMILES string.
    
    The strategy is as follows:
      1. Parse the SMILES.
      2. Check that a carboxylic acid group is present.
      3. Check that the overall molecule has a sufficient number of carbon atoms.
      4. Look for a three‐membered epoxide ring.
      5. Starting at the carboxylic acid carbon, do a depth–first search 
         (only along carbons that are “allowed” – i.e. not in rings larger than 3 atoms)
         to compute the longest linear chain. This approximates the fatty acid chain.
      6. If these criteria are met then return True.
      
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if molecule qualifies as an epoxy fatty acid, False otherwise.
        str: Reason for classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # (1) Check for the carboxylic acid group.
    # Use a SMARTS that catches a typical free -COOH unit.
    acid_smarts = Chem.MolFromSmarts("C(=O)[O;H]")
    acid_matches = mol.GetSubstructMatches(acid_smarts)
    if not acid_matches:
        return False, "Missing carboxylic acid group (fatty acid functionality)"
    
    # (2) Check overall number of carbon atoms.
    c_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    if len(c_atoms) < 18:
        return False, f"Too few carbon atoms ({len(c_atoms)}); not long enough to be a fatty acid"
    
    # (3) Identify at least one epoxide ring.
    epoxide_pattern = Chem.MolFromSmarts("[C;r3][O;r3][C;r3]")
    epoxide_matches = mol.GetSubstructMatches(epoxide_pattern)
    if not epoxide_matches:
        return False, "No epoxide ring (three-membered heterocycle containing oxygen) detected."
        
    # (4) Check for a long linear chain emanating from the acid group.
    # For fatty acids the carboxylic acid is typically at one terminus of a long aliphatic chain.
    # We define a helper: allowed chain atoms are carbons that are either not in any ring
    # or if they are in a ring, the ring size must be exactly 3 (allowing for the epoxide).
    ring_info = mol.GetRingInfo()
    # Precompute a list of rings (as sets of atom indices) for efficiency.
    rings = [set(r) for r in ring_info.AtomRings()]
    
    def in_large_ring(atom_idx):
        # Returns True if the atom is in any ring larger than 3 atoms.
        for r in rings:
            if atom_idx in r and len(r) > 3:
                return True
        return False

    def is_allowed_chain_atom(atom):
        # We only allow carbon atoms for the chain.
        # If the atom is in a ring, then it is allowed only if it is exclusively
        # in three-membered rings (if any). (A pragmatic approximation.)
        if atom.GetAtomicNum() != 6:
            return False
        # If not in any ring, allow.
        atom_idx = atom.GetIdx()
        if not mol.GetAtomWithIdx(atom_idx).IsInRing():
            return True
        # If in a ring, check all rings that contain the atom:
        for r in rings:
            if atom_idx in r and len(r) > 3:
                return False
        return True

    # We now perform a DFS starting from the carbon atom that is the "acid carbon".
    # (The SMARTS "C(=O)[O;H]" returns a tuple with [acid carbon, oxygen].)
    # We will follow bonds only through atoms that meet is_allowed_chain_atom.
    def dfs(atom_idx, visited):
        max_length = 0
        current_atom = mol.GetAtomWithIdx(atom_idx)
        for nbr in current_atom.GetNeighbors():
            nbr_idx = nbr.GetIdx()
            if nbr_idx in visited:
                continue
            if is_allowed_chain_atom(nbr):
                visited.add(nbr_idx)
                path_length = 1 + dfs(nbr_idx, visited)
                if path_length > max_length:
                    max_length = path_length
                visited.remove(nbr_idx)
        return max_length

    longest_chain = 0
    # Try each acid group match and consider the acid carbon (first index in the match).
    for match in acid_matches:
        acid_carbon_idx = match[0]
        acid_atom = mol.GetAtomWithIdx(acid_carbon_idx)
        # Look at neighbors of the acid carbon that are allowed chain atoms.
        for nbr in acid_atom.GetNeighbors():
            if nbr.GetAtomicNum() == 6 and is_allowed_chain_atom(nbr):
                visited = {acid_carbon_idx, nbr.GetIdx()}
                chain_length = 1 + dfs(nbr.GetIdx(), visited)
                if chain_length > longest_chain:
                    longest_chain = chain_length

    # Require that the chain (not including the acid carbon itself) is long enough.
    # This threshold can be tuned – here we require at least 12 consecutive carbons.
    if longest_chain < 12:
        return False, f"Aliphatic chain too short (found chain length {longest_chain}, need at least 12 carbons)"
    
    return True, "Molecule has a carboxylic acid group, a sufficiently long aliphatic chain, and an epoxide ring."

# Testing examples if run as main:
if __name__ == "__main__":
    # One of the true positives:
    test_smiles = "O=C(CCC/C=C\\C/C=C\\C/C=C\\[C@@H]([C@H]1[C@H](CCCCC)O1)O)O"
    result, reason = is_epoxy_fatty_acid(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61498',
                          'name': 'epoxy fatty acid',
                          'definition': 'A heterocyclic fatty acid containing '
                                        'an epoxide ring as part of its '
                                        'structure.',
                          'parents': ['CHEBI:23931', 'CHEBI:48847'],
                          'xrefs': ['PMID:15145985'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 102,
                           'log_lines_of_code': 4.624972813284271,
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
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetNeighbors',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'add',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'IsInRing',
                                                 'GetSubstructMatches',
                                                 'remove',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum'],
                           'methods_called_count': 13,
                           'smarts_strings': [   '[C;r3][O;r3][C;r3]',
                                                 'C(=O)[O;H]'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_epoxy_fatty_acid(smiles: str):',
                                       'in_large_ring(atom_idx):',
                                       'is_allowed_chain_atom(atom):',
                                       'dfs(atom_idx, visited):'],
                           'defs_count': 4,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Missing carboxylic acid '
                                          'group (fatty acid functionality)"',
                                          'False, f"Too few carbon atoms '
                                          '({len(c_atoms)}); not long enough '
                                          'to be a fatty acid"',
                                          'False, "No epoxide ring '
                                          '(three-membered heterocycle '
                                          'containing oxygen) detected."',
                                          'True',
                                          'False',
                                          'False',
                                          'True',
                                          'False',
                                          'True',
                                          'max_length',
                                          'False, f"Aliphatic chain too short '
                                          '(found chain length '
                                          '{longest_chain}, need at least 12 '
                                          'carbons)"',
                                          'True, "Molecule has a carboxylic '
                                          'acid group, a sufficiently long '
                                          'aliphatic chain, and an epoxide '
                                          'ring."'],
                           'returns_count': 13,
                           'complexity': 7.924994562656854},
    'message': '\n'
               'Attempt failed: F1 score of 0.09759110562075354 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\[C@@H]([C@H]1[C@H](CCCCC)O1)O)O '
               'NAME: (13S)-hydroxy-(14S,15S)-epoxy-(5Z,8Z,11Z)-icosatrienoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'C(CCC/C=C\\C[C@@H]1/C(/O1)=C/C=C\\C/C=C\\CCCCC)(=O)O NAME: '
               '(5Z,8R,9Z,11Z,14Z)-8,9-epoxyicosatetraenoic acid REASON: '
               'CORRECT Molecule has a carboxylic acid group, sufficiently '
               'long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'C(CCC(O)=O)[C@@H](/C=C/C=C\\C/C=C\\C[C@@H]1[C@H](CCCCC)O1)OO '
               'NAME: '
               '(5S)-hydroperoxy-(14R,15S)-epoxy-(6E,8Z,11Z)-icosatrienoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@H]1O[C@@H]1\\C=C\\[C@H](O)C\\C=C/CCCC(O)=O '
               'NAME: (8R)-hydroxy-(11R,12R)-epoxyicosa-(5Z,9E,14Z)-trienoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'ClC[C@]1(O)[C@@H]([C@]2(O[C@@H]2CC=C(C)C)C)[C@H](OC)[C@H](OC(=O)CCC(=O)O)CC1 '
               'NAME: Ligerin REASON: CORRECT Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: C(C(O)=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC1C(CC)O1 '
               'NAME: (7Z,10Z,13Z,16Z)-19,20-epoxydocosatetraenoic acid '
               'REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H]1C/C=C\\C/C=C\\C/C=C\\CCCCC)CCCC(O)=O NAME: '
               '5R,6S-EpETrE REASON: CORRECT Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: [C@H]1(CCCCCCCC(=O)O)[C@@H](CCCCCCCC)O1 NAME: '
               '(9S,10R)-epoxyoctadecanoic acid REASON: CORRECT Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C[C@H]1[C@@H](C/C=C\\C/C=C\\CCCC(O)=O)O1 NAME: '
               '(11R,12S)-EET REASON: CORRECT Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: C1(C(C/C=C\\CCCCCO)O1)CCCCCCCC(=O)O NAME: '
               '9,10-epoxy-18-hydroxy-(12Z)-octadecenoic acid REASON: CORRECT '
               'Molecule has a carboxylic acid group, sufficiently long carbon '
               'chain, and an epoxide ring.\n'
               ' * SMILES: [H]C(\\C=C/CCCCCCCC(O)=O)=C1O[C@H]1C\\C=C/CC NAME: '
               '(9Z,13S,15Z)-12,13-epoxyoctadeca-9,11,15-trienoic acid REASON: '
               'CORRECT Molecule has a carboxylic acid group, sufficiently '
               'long carbon chain, and an epoxide ring.\n'
               ' * SMILES: CCCCCC1OC1C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '14,15-EET REASON: CORRECT Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: CC[C@]1(C)O[C@@H]1CC\\C(C)=C\\CC\\C(C)=C\\C(O)=O '
               'NAME: '
               '(2E,6E,10R,11S)-10,11-epoxy-3,7,11-trimethyltrideca-2,6-dienoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C[C@H]1[C@@H](CC)O1 '
               'NAME: (4Z,7Z,10Z,13Z,16Z,19S,20R)-19,20-epoxydocosapentaenoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: C(C(O)=O)CCCC/C=C\\C/C=C\\C/C=C\\CC1C(C/C=C\\CC)O1 '
               'NAME: (7Z,10Z,13Z,19Z)-16,17-epoxydocosatetraenoic acid '
               'REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'OC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C=C\\1/[C@@H](C/C=C\\CC)O1)=O '
               'NAME: '
               '17R,(16)-epoxy-(4Z,7Z,10Z,13Z,19Z)-docosahexa-4,7,10,13,15,19-enoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: CCCCCC1OC1C\\C=C/CCCCCCCC(O)=O NAME: vernolic acid '
               'REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'C(O)(=O)CCC[C@H]1[C@@H](/C=C/C=C/C=C\\C/C=C\\C=C\\[C@H](CC)O)O1 '
               'NAME: 5(S)6-epoxy-18(S)-HEPE REASON: CORRECT Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               'C(CCCC)[C@H]1[C@H](\\C=C\\[C@H](C/C=C\\C/C=C\\CCCC(O)=O)O)O1 '
               'NAME: 11(S)-hydroxy-14(S),15(S)-hepoxilin A3 REASON: CORRECT '
               'Molecule has a carboxylic acid group, sufficiently long carbon '
               'chain, and an epoxide ring.\n'
               ' * SMILES: '
               'C(=C/[C@]1([C@](C/C=C\\CCCCC)(O1)[H])[H])\\[C@H](C/C=C\\CCCC(=O)O)O '
               'NAME: (8S)-hepoxilin A3 REASON: CORRECT Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: C(CCCCCCC/C=C\\C([C@H]1[C@H](CCCCC)O1)O)(=O)O NAME: '
               '11-hydroxy-(12S,13S)-epoxy-(9Z)-octadecenoic acid REASON: '
               'CORRECT Molecule has a carboxylic acid group, sufficiently '
               'long carbon chain, and an epoxide ring.\n'
               ' * SMILES: C(C(O)=O)CCCC\\C=C/C=C/C=C/C1C(C/C=C\\C/C=C\\CC)O1 '
               'NAME: (7Z,9E,11E,16Z,19Z)-13,14-epoxydocosapentaenoic acid '
               'REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: CCCCCCCCC1OC1CCCCCCCC(O)=O NAME: '
               '9,10-epoxyoctadecanoic acid REASON: CORRECT Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               '[C@H]1(CCCC(O)=O)[C@H](/C=C/C=C/C=C\\C/C=C\\C=C\\C(CC)O)O1 '
               'NAME: '
               '5(S),6(S)-epoxy-18-hydroxy-(7E,9E,11Z,14Z,16E)-icosapentaenoic '
               'acid REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\C([C@@H]1[C@H](CCCCC)O1)O)O NAME: '
               '13-hydroxy-(14R,15S)-epoxy-(5Z,8Z,11Z)-icosatrienoic acid '
               'REASON: CORRECT Molecule has a carboxylic acid group, '
               'sufficiently long carbon chain, and an epoxide ring.\n'
               'False positives: SMILES: '
               'O=C1O[C@H](C[C@@H](O)[C@H]2O[C@H]2[C@H](C=CC=3C1=C(O)C=CC3)O)CC=CNC(=O)/C=C/C=NOC '
               'NAME: Necroxime C REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               'O1C2(C1C(=O)CC(C(OC(=O)/C(/C)=C\\C)C(O)C3C(OC(=O)C3=C)C2)=C)C '
               'NAME: '
               '(10-hydroxy-3-methyl-8,12-dimethylidene-6,13-dioxo-4,14-dioxatricyclo[9.3.0.03,5]tetradecan-9-yl) '
               '(Z)-2-methylbut-2-enoate REASON: WRONGLY CLASSIFIED Molecule '
               'has a carboxylic acid group, sufficiently long carbon chain, '
               'and an epoxide ring.\n'
               ' * SMILES: [C@H]1(CCCCCCCC(=O)[O-])[C@@H](CCCCCCCCO)O1 NAME: '
               '(9S,10R)-9,10-epoxy-18-hydroxyoctadecanoate REASON: WRONGLY '
               'CLASSIFIED Molecule has a carboxylic acid group, sufficiently '
               'long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'O1C23C1(C(O)(CC[C@]2([C@]4([C@](C3)([C@@]5([C@@](C(=O)C4)(C[C@@H](OC(=O)C)CC5)[H])C)[H])[H])[H])C(C6N(OC(=O)C)CC(CC6O)C)C)C '
               'NAME: 12,13-Epoxy-22S,25S,5alpha-Veratramine '
               '3beta,17,24alpha-triol-6-one-N,O(3)-diacetate REASON: WRONGLY '
               'CLASSIFIED Molecule has a carboxylic acid group, sufficiently '
               'long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'C(CCC([O-])=O)/C=C\\C[C@@H](/C=C/C=C\\C[C@H]1[C@@H](CCCCC)O1)OO '
               'NAME: '
               '(8S)-hydroperoxy-(14S,15R)-epoxy-(5Z,9E,11Z)-icosatrienoate '
               'REASON: WRONGLY CLASSIFIED Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'O=C1C=C2C(=CC(=O)OC2(C)C)[C@]3([C@@H]4[C@@]1([C@H]5C(=O)[C@@H](O[C@@H]6[C@@]5(O)[C@](C(=O)O6)(C)C4)C)C)OC3 '
               'NAME: Chrysogenolide F REASON: WRONGLY CLASSIFIED Molecule has '
               'a carboxylic acid group, sufficiently long carbon chain, and '
               'an epoxide ring.\n'
               ' * SMILES: '
               'O([C@@H]1C(C2[C@@]3([C@@]4(C3)[C@]([C@]5([C@](CC4)([C@](C(=O)[C@@H]5O)([C@@H](C[C@@H](OC(=O)C)[C@@]6(OC6(C)C)[H])C)[H])C)C)(CC2)[H])CC1)(C)C)[C@@H]7OC[C@H](O)[C@H](O)[C@H]7O '
               'NAME: '
               '[(1R,3R)-1-[(2S)-3,3-dimethyloxiran-2-yl]-3-[(1S,3R,6S,11R,12S,13R,15R,16R)-13-hydroxy-7,7,12,16-tetramethyl-14-oxo-6-[(2S,3R,4S,5S)-3,4,5-trihydroxyoxan-2-yl]oxy-15-pentacyclo[9.7.0.01,3.03,8.012,16]octadecanyl]butyl] '
               'acetate REASON: WRONGLY CLASSIFIED Molecule has a carboxylic '
               'acid group, sufficiently long carbon chain, and an epoxide '
               'ring.\n'
               ' * SMILES: '
               'O=C(O[C@H]1[C@@]23O[C@@H]2[C@@]4(OCC([C@@H]4C[C@@]3([C@@H](C)CC1)C)=C)O)C(O)(CO)CC(CC(CC)C)C '
               'NAME: Cryptosphaerolide REASON: WRONGLY CLASSIFIED Molecule '
               'has a carboxylic acid group, sufficiently long carbon chain, '
               'and an epoxide ring.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)OCC1CO1 NAME: Glycidyl '
               'oleate REASON: WRONGLY CLASSIFIED Molecule has a carboxylic '
               'acid group, sufficiently long carbon chain, and an epoxide '
               'ring.\n'
               ' * SMILES: '
               'O=C1O[C@@]2([C@@H](C3=CC=CC=C3)C[C@@H]([C@]([C@]42[C@@]1(O4)CC5=CC=CC=C5)(O)C6=CC=CC=C6)O)C(O)C7=CC=CC=C7 '
               'NAME: Maculalactone H REASON: WRONGLY CLASSIFIED Molecule has '
               'a carboxylic acid group, sufficiently long carbon chain, and '
               'an epoxide ring.\n'
               ' * SMILES: '
               'O1C(C1C/C=C\\CCCCC)CCCCCCCC(O[C@H](COC(=O)CCCCCCC)CO)=O NAME: '
               'DG(8:0/18:1(12Z)-O(9S,10R)/0:0) REASON: WRONGLY CLASSIFIED '
               'Molecule has a carboxylic acid group, sufficiently long carbon '
               'chain, and an epoxide ring.\n'
               ' * SMILES: O1C(C1C/C=C\\C/C=C\\CCCCC(O)=O)CCCCC NAME: gamma- '
               '12(13)-EpODE REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               'O=C1O[C@H](C(=CC=C[C@H](C[C@H]2O[C@@H]2[C@@H]([C@@H](O)CC)C)C)C)[C@H](C=C[C@H](OC(=O)C)[C@H](CC[C@H](C1)O)C)C '
               'NAME: Deoxypladienolide B REASON: WRONGLY CLASSIFIED Molecule '
               'has a carboxylic acid group, sufficiently long carbon chain, '
               'and an epoxide ring.\n'
               ' * SMILES: '
               'CC(C)c1oc(=O)cc2c1[C@@H](O)[C@H]1OC(=O)[C@]3(C)[C@H]1[C@]2(C)[C@H]1O[C@H]1[C@@H]3O '
               'NAME: Nagilactone C REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               'O1C2(C3(C(O)(C4C(C5(C6(OC6C4)C(O)C=CC5=O)C)CC3)C(OC(=O)C)C12)C)C(C7OC(=O)C(=C(C7)C)C)C '
               'NAME: Physagulin C REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               'ClC1=C(OC)C=C2CC(=CC=C[C@@H](OC)[C@]3(O)NC(O[C@H]([C@H]([C@H]4[C@]([C@H](CC(N(C1=C2)[C@@H]5O[C@@H]([C@@H](O)[C@@H]([C@H]5O)O)COC(=O)N)=O)OC(=O)CC)(O4)C)C)C3)=O)C '
               'NAME: '
               'N-(6-O-carbamoyl-beta-D-glucopyranosyl)-N-demethylansamitocin '
               'P REASON: WRONGLY CLASSIFIED Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               '[C@H]1(CCCC([O-])=O)[C@H](/C=C/C=C/C=C\\C/C=C\\C=C\\[C@H](CC)O)O1 '
               'NAME: '
               '5(S),6(S)-epoxy-18(S)-hydroxy-(7E,9E,11Z,14Z,16E)-icosapentaenoate '
               'REASON: WRONGLY CLASSIFIED Molecule has a carboxylic acid '
               'group, sufficiently long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'CO[C@H]1C[C@@H](O[C@@H](C)[C@@H]1O)O[C@H]1[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2OP([O-])([O-])=O)[NH+](C)C)[C@@H](C)C[C@@]2(CO2)C(=O)[C@H](C)[C@@H](O)[C@@H](C)[C@@H](C)OC(=O)[C@@H]1C '
               "NAME: oleandomycin 2'-O-phosphate(1-) REASON: WRONGLY "
               'CLASSIFIED Molecule has a carboxylic acid group, sufficiently '
               'long carbon chain, and an epoxide ring.\n'
               ' * SMILES: '
               'O=C1OC=C[C@@](O)(C(=O)[C@@H](C)CC=C[C@@H]2[C@]3(O1)C(=O)N[C@H]([C@@H]3[C@H](C)[C@@]4([C@H]2O4)C)CC5=CC=C(OC)C=C5)C '
               'NAME: Phenochalasin B REASON: WRONGLY CLASSIFIED Molecule has '
               'a carboxylic acid group, sufficiently long carbon chain, and '
               'an epoxide ring.\n'
               ' * SMILES: '
               'S1C2=C(N=C1C)C=C([C@H]3OC(=O)C[C@H](O)C(C(=O)[C@@H]([C@@H](O)[C@H](CCC[C@]4(O[C@]4(C3)[H])C)C)CC=C)(C)C)C=C2 '
               'NAME: Sagopilone REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: '
               '[C@@]12([C@]([C@@]3([C@@]([C@@H](C1)O)(C=4[C@@](CC3)([C@@](CC4)([C@@H]5C[C@@H](O[C@H]5OC(C)=O)[C@H]6C(C)(C)O6)[H])C)C)[H])(C)[C@H](CC(OC2(C)C)=O)OC(C)=O)[H] '
               'NAME: (1S)-1-acetoxy-luvungin A REASON: WRONGLY CLASSIFIED '
               'Molecule has a carboxylic acid group, sufficiently long carbon '
               'chain, and an epoxide ring.\n'
               ' * SMILES: '
               'O=C1N[C@@H](CC=2C3=C(C=CC=C3)NC2)[C@H]4[C@]1(C(=O)CCC(=O)OC)[C@@H](/C=C/CC(/C=C(/C=O)\\C)C)[C@@H]5O[C@]5(C)[C@H]4C '
               'NAME: Armochaetoglobin E REASON: WRONGLY CLASSIFIED Molecule '
               'has a carboxylic acid group, sufficiently long carbon chain, '
               'and an epoxide ring.\n'
               ' * SMILES: '
               'O=C1[C@](O)([C@@H]2O[C@H]2[C@@H](OC(=O)C)[C@@]34C(=O)N[C@H]([C@@H]3[C@H](C)C([C@H](C4C=CC[C@@H]1C)O)=C)CC5=CC=CC=C5)C '
               'NAME: 19,20-Epoxycytochalasin D REASON: WRONGLY CLASSIFIED '
               'Molecule has a carboxylic acid group, sufficiently long carbon '
               'chain, and an epoxide ring.\n'
               ' * SMILES: '
               'P(=O)(OC1C2OC2C(O)C(O)CCCCCCCCC=CCCCC(OC(CCC1)=O)C)(OCCN)O '
               'NAME: JBIR-19 REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               ' * SMILES: O=C1O[C@@H](CC2=C1[C@@H](O)[C@@H]3O[C@@H]3C2=O)CCC '
               'NAME: EI-1941-2 REASON: WRONGLY CLASSIFIED Molecule has a '
               'carboxylic acid group, sufficiently long carbon chain, and an '
               'epoxide ring.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Too few carbon atoms (14); not '
                                               'long enough to be a fatty '
                                               'acid'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Too few carbon atoms (16); not '
                                               'long enough to be a fatty '
                                               'acid'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Missing carboxylic acid group '
                                               '(fatty acid functionality)'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No epoxide ring '
                                               '(three-membered heterocycle '
                                               'containing oxygen) detected.'}],
    'sample_false_negatives': [   {   'smiles': 'ClC[C@]1(O)[C@@H]([C@]2(O[C@@H]2CC=C(C)C)C)[C@H](OC)[C@H](OC(=O)CCC(=O)O)CC1',
                                      'name': 'Ligerin',
                                      'reason': 'Aliphatic chain too short '
                                                '(found chain length 3, need '
                                                'at least 12 carbons)'},
                                  {   'smiles': 'CC[C@]1(C)O[C@@H]1CC\\C(C)=C\\CC\\C(C)=C\\C(O)=O',
                                      'name': '(2E,6E,10R,11S)-10,11-epoxy-3,7,11-trimethyltrideca-2,6-dienoic '
                                              'acid',
                                      'reason': 'Too few carbon atoms (16); '
                                                'not long enough to be a fatty '
                                                'acid'},
                                  {   'smiles': 'C\\C(CC[C@H]1OC1(C)C)=C/CC\\C(C)=C\\C(O)=O',
                                      'name': 'juvenile hormone III acid',
                                      'reason': 'Too few carbon atoms (15); '
                                                'not long enough to be a fatty '
                                                'acid'},
                                  {   'smiles': 'O1[C@H]([C@@H]1[C@H]([C@@H](O)C)C)C[C@@H]2[C@@H](O)[C@@H](O)[C@@H](OC2)C/C(/C)=C/C(O)=O',
                                      'name': 'Monic acid',
                                      'reason': 'Too few carbon atoms (17); '
                                                'not long enough to be a fatty '
                                                'acid'},
                                  {   'smiles': 'CC\\C(CC[C@H]1O[C@@]1(C)CC)=C/CC\\C(C)=C\\C(O)=O',
                                      'name': 'juvenile hormone I acid',
                                      'reason': 'Too few carbon atoms (17); '
                                                'not long enough to be a fatty '
                                                'acid'}],
    'attempt': 1,
    'reasoning': 'Below is one approach. In our reasoning we noticed that '
                 'simply checking for a carboxylic acid group, a minimum total '
                 'number of carbons, and a three‐membered (epoxide) ring was '
                 'not enough. Many non–fatty acid molecules (even if they have '
                 'at least one acid and one epoxide) can pass these basic '
                 'tests. Therefore, in the new code we add a “chain‐quality” '
                 'test. In many epoxy fatty acids the acid group is attached '
                 'to a long, mostly linear, aliphatic (nonaromatic) chain '
                 '(although an epoxide is present as a small three‐membered '
                 'ring). In our revised code we (1) insist on at least one '
                 'acid and one epoxide, (2) require a minimum overall number '
                 'of carbons, and (3) “walk” outward from the acid carbon '
                 'along allowed (i.e. acyclic or only in a three‐membered '
                 'ring) carbon atoms. In this way we compute the longest '
                 '“alkyl chain” attached to the acid group. If this chain '
                 '(apart from any extra rings larger than 3 members) is too '
                 'short, then the molecule is flagged. (Many of the false '
                 'positives had extra ring systems or other complex topologies '
                 'that interrupted a long linear chain.) \n'
                 '\n'
                 'Below is the complete Python code in one code block. (Note '
                 'that these criteria are heuristic and may require further '
                 'tuning.) \n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 74,
    'num_false_positives': 40,
    'num_true_negatives': 142181,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.6491228070175439,
    'recall': 0.9367088607594937,
    'f1': 0.766839378238342,
    'accuracy': 0.9996837666900914,
    'negative_predictive_value': 0.9999648347938616}