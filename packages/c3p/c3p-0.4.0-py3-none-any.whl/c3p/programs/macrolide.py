"""
Classifies: CHEBI:25106 macrolide
"""
"""
Classifies: macrolide
Definition: A macrolide is a macrocyclic lactone defined as a ring of 12 or more atoms 
            that features an ester (lactone) bond. Our algorithm identifies the lactone 
            feature by first finding a bond between an oxygen and a carbon where both atoms 
            are in a ring and where that carbon also bears a double bond to an oxygen that 
            is exocyclic (not part of the ring). In addition, we require that the macrocycle 
            (the ring containing the ester bond) does not contain any nitrogen atoms 
            (since macrolides are typically polyketide‐derived) and that the overall molecule 
            does not contain phosphorus (which would point to phospholipid‐like structures).
            
This version was revised after noticing that our previous approach both erroneously 
classified some non–macrolide structures (false positives) and missed some macrolides 
(false negatives). We therefore now use a targeted SMARTS query along with ring checks.
"""

from rdkit import Chem

def is_macrolide(smiles: str):
    """
    Determines whether the molecule is a macrolide based on its SMILES string.
    A macrolide is defined as a macrocyclic lactone having a ring of 12 or more atoms 
    that features an ester bond: an oxygen in the ring connected to a carbon that bears 
    a double bond to an exocyclic oxygen. Also, the ring should not contain nitrogen and 
    the molecule should not contain phosphorus.

    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        (bool, str): A tuple (True/False, explanation) indicating the classification result.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject molecules that contain phosphorus (atomic number 15),
    # which are not typical of polyketide-derived macrolides.
    if any(atom.GetAtomicNum() == 15 for atom in mol.GetAtoms()):
        return False, "Molecule contains phosphorus; likely not a macrolide (polyketide-derived) structure."
    
    # Define a SMARTS pattern for the lactone bond:
    #   [O;r] - an oxygen that is a member of a ring, bonded to
    #   [C;r](=[O;!r]) - a carbon (in a ring) that is double-bonded to an oxygen that is NOT in a ring.
    lactone_smarts = "[O;r]-[C;r](=[O;!r])"
    lactone_pat = Chem.MolFromSmarts(lactone_smarts)
    if lactone_pat is None:
        return False, "Error building SMARTS pattern"

    # Find all matches of lactone substructure.
    matches = mol.GetSubstructMatches(lactone_pat)
    if not matches:
        return False, "No lactone substructure (ester bond with exocyclic carbonyl oxygen) found."
    
    # Retrieve ring information from the molecule.
    ring_info = mol.GetRingInfo().AtomRings()
    if not ring_info:
        return False, "No rings found in the molecule"
    
    # Loop over each lactone substructure match.
    # The match gives a tuple of atom indices: (ring oxygen, ring carbon, carbonyl oxygen).
    for match in matches:
        ring_o, ring_c, exo_o = match
        # Now look for a ring (from RDKit's ring perception) that contains both ring_o and ring_c.
        for ring in ring_info:
            if len(ring) < 12:
                continue  # Only interested in macrocycles (size 12 or more).
            if (ring_o in ring) and (ring_c in ring):
                # For our purposes the ring itself must not contain any nitrogen.
                if any(mol.GetAtomWithIdx(idx).GetAtomicNum() == 7 for idx in ring):
                    continue
                reason = (f"Found macrocyclic lactone ring of size {len(ring)} with ester bond: "
                          "oxygen in ring attached to carbonyl carbon (carbonyl oxygen exocyclic).")
                return True, reason

    return False, "No macrocyclic lactone ring (ester embedded in a ring of 12 or more atoms) found"

# Example usage:
# test_smiles = "O1CCCCCCCCCC(OCCCCC1)=O"  # A tentative macrolide example.
# result, explanation = is_macrolide(test_smiles)
# print(result, explanation)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25106',
                          'name': 'macrolide',
                          'definition': 'A macrocyclic lactone with a ring of '
                                        'twelve or more members derived from a '
                                        'polyketide.',
                          'parents': ['CHEBI:26188', 'CHEBI:63944'],
                          'xrefs': ['Wikipedia:Macrolide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 50,
                           'log_lines_of_code': 3.912023005428146,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 0,
                                                 1,
                                                 0],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 8,
                           'smarts_strings': ['lactone_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_macrolide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains '
                                          'phosphorus; likely not a macrolide '
                                          '(polyketide-derived) structure."',
                                          'False, "Error building SMARTS '
                                          'pattern"',
                                          'False, "No lactone substructure '
                                          '(ester bond with exocyclic carbonyl '
                                          'oxygen) found."',
                                          'False, "No rings found in the '
                                          'molecule"',
                                          'True, reason',
                                          'False, "No macrocyclic lactone ring '
                                          '(ester embedded in a ring of 12 or '
                                          'more atoms) found"'],
                           'returns_count': 7,
                           'complexity': 4.982404601085629},
    'message': '\n'
               'Attempt failed: F1 score of 0.7429718875502008 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC[C@H]1OC(=O)[C@H](C)[C@@H](O[C@H]2C[C@H](OC)[C@@H](O)[C@H](C)O2)[C@H](C)[C@@H](O)[C@](C)(O)C[C@@H](C)C(=O)[C@H](C)[C@@H](O)[C@H]1C '
               'NAME: 3-O-(alpha-L-oleandrosyl)erythronolide B REASON: CORRECT '
               'Found macrocyclic lactone ring of size 14 with ester bond: '
               'oxygen in ring attached to carbonyl carbon (carbonyl oxygen '
               'exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)[C@H]5OC4)COC(=O)C=6NC=CC6)O)C)C)O[C@@H]([C@@H](C)[C@@H]([C@H]3O)OC(=O)C(CC(C)C)C)C '
               'NAME: Milbemycin alpha29 REASON: CORRECT Found macrocyclic '
               'lactone ring of size 16 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'S1C(=NC(=C1)/C=C/[C@H]2OC(=O)C[C@H](O)C(C(=O)[C@@H]([C@@H](O)[C@H](CCC[C@@H]3[C@H](C2)O3)C)C)(C)C)C '
               'NAME: Epothilone A8 REASON: CORRECT Found macrocyclic lactone '
               'ring of size 16 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: O=C1OC(CCCCCC(C(C=C1)=O)O)C NAME: Cladospolide D '
               'REASON: CORRECT Found macrocyclic lactone ring of size 12 with '
               'ester bond: oxygen in ring attached to carbonyl carbon '
               '(carbonyl oxygen exocyclic).\n'
               ' * SMILES: O1C2C3N(CC2)CC=C3COC(=O)C(O)(C(CC(C1=O)=CC)C)C '
               'NAME: '
               '4-Ethylidene-7-hydroxy-6,7-dimethyl-2,9-dioxa-14-azatricyclo[9.5.1.014,17]heptadec-11-ene-3,8-dione '
               'REASON: CORRECT Found macrocyclic lactone ring of size 12 with '
               'ester bond: oxygen in ring attached to carbonyl carbon '
               '(carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'S1C(=NC(=C1)/C=C(/[C@H]2OC(=O)C[C@H](OC3OC(CO)C(C3O)O)C(C(=O)[C@@H]([C@@H](O)[C@H](CCC[C@@]4([C@H](C2)O4)C)C)C)(C)C)\\C)C '
               'NAME: Epothilone B 3-alpha-D-arabinofuranoside REASON: CORRECT '
               'Found macrocyclic lactone ring of size 16 with ester bond: '
               'oxygen in ring attached to carbonyl carbon (carbonyl oxygen '
               'exocyclic).\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]([H])([C@H]1C)[C@@H](OC(=O)c1ccccc1)\\C=C\\C=C\\C(=O)O[C@@]1([H])[C@@H](C)C[C@]3([H])[C@]1(O)[C@H](O)[C@@]1(CO)O[C@@]1([H])[C@@]1([H])[C@@]4([H])O[C@@]5(O[C@@]([H])([C@H](C)[C@]31O5)[C@@]4(O)[C@](C)(O)C2)c1ccccc1 '
               'NAME: Trigonosin E, (rel)- REASON: CORRECT Found macrocyclic '
               'lactone ring of size 19 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC(C(OC)C=CC=C(CC(C(C(C=C(C=C1OC)C)C)O)C)C)C(C(O)C(C2(OC(C(C)C(C2)O[C@@H]3O[C@H]([C@H](O)[C@H]([C@H]3OC)O)C)C(C)C)O)C)C '
               'NAME: Leucanicidin REASON: CORRECT Found macrocyclic lactone '
               'ring of size 16 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@H]([C@@H](O)[C@H](CC[C@@H]2O[C@H](C[C@H](C2)OC)C)C)C)C[C@H](O)C[C@H](O)[C@@H]([C@@H](OC)C[C@H]3O[C@@H](C=CC3)C[C@@H](O[C@H]4OC[C@H](OC)[C@H]([C@@H]4OC(=O)[C@H](O)CO)OC)CC=C(C=CC(=O)O[C@@H](C[C@@H](C[C@@H]([C@@H]([C@H](C[C@H]5O[C@H](C[C@H](CC=C(C=C1)C)O[C@H]6OC[C@H](OC)[C@H]([C@@H]6OC(=O)[C@H](O)CO)OC)C=CC5)OC)C)O)O)[C@H]([C@@H](O)[C@H](CC[C@@H]7O[C@H](C[C@H](C7)OC)C)C)C)C)C '
               'NAME: Samholide B REASON: CORRECT Found macrocyclic lactone '
               'ring of size 40 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1C=CC(=C[C@@H]([C@H](OC(=O)C[C@H]([C@@H]([C@H]([C@H](C[C@H]1C)CC)O[C@@H]2O[C@H]([C@H](O)[C@H]([C@H]2O)O)C)C)O)CC)C)C '
               'NAME: 5-O-alpha-L-rhamnosyltylactone REASON: CORRECT Found '
               'macrocyclic lactone ring of size 16 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               '[C@@]123O[C@]([C@H](C)CC1(C)C)(CC(O[C@@]([C@@H](C)O)(CC(OC(C2)[C@H](C)[C@](O3)([C@H](CC[C@@H](C=4C(=CC=C(C4)O)Br)OC)C)[H])=O)[H])=O)O '
               'NAME: aplysiatoxin REASON: CORRECT Found macrocyclic lactone '
               'ring of size 12 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@@H](CCCC=CC=C[C@H](O[C@H]2O[C@H]([C@H](O)[C@H]([C@@H]2C)O)CO)C[C@@H](O)CC=CC=C[C@H](CC=CC=C1)O)C '
               'NAME: Macrolactin C REASON: CORRECT Found macrocyclic lactone '
               'ring of size 24 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CC[C@H]1CC[C@@H]2[C@@H]([C@@H]([C@H]([C@@]3(O2)CC[C@H]([C@H](O3)C[C@H](C)O)C)C)OC(=O)C=C[C@H]([C@@H]([C@H](C(=O)[C@H]([C@@H]([C@H](C(=O)[C@@H]([C@@H]([C@H](CC=CC=C1)C)O)C)C)O)C)C)O)C)C '
               'NAME: '
               "(1R,4S,5'R,6'R,10S,11R,12R,14R,15R,16S,18R,19S,20R,25S,26R,27S,29S)-4-ethyl-11,15,19-trihydroxy-6'-[(2S)-2-hydroxypropyl]-5',10,12,14,16,18,20,26,29-nonamethylspiro[24,28-dioxabicyclo[23.3.1]nonacosa-5,7,21-triene-27,2'-oxane]-13,17,23-trione "
               'REASON: CORRECT Found macrocyclic lactone ring of size 26 with '
               'ester bond: oxygen in ring attached to carbonyl carbon '
               '(carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](CCC[C@@H](C)[C@H](C=C[C@](CC1)(O)C)O)C)C '
               'NAME: 2,3,8,9-tetrahydrocineromycin B REASON: CORRECT Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@@H](O)C=CC(=O)O[C@@H](CC[C@H](C=C1)O)C)C NAME: '
               '4-keto-clonostachydiol REASON: CORRECT Found macrocyclic '
               'lactone ring of size 14 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC(CC(=O)OC(C=CC(C(=CCC=2C1=C(O)C=CC2)C)O)C)C/C=C/NC(=O)/C=C\\C=N\\OC '
               'NAME: Lobatamide A REASON: CORRECT Found macrocyclic lactone '
               'ring of size 15 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](CC(=O)O[C@H](C)C\\C=C\\C=C\\[C@H](O)[C@H](C)C[C@H](CC=O)[C@@H]1O[C@@H]1O[C@H](C)[C@@H](O[C@H]2C[C@@](C)(O)[C@@H](OC(=O)CC(C)C)[C@H](C)O2)[C@@H]([C@H]1O)N(C)C)OC(C)=O '
               'NAME: josamycin REASON: CORRECT Found macrocyclic lactone ring '
               'of size 16 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@@H](OC)C=CC=C(C[C@@H](C)[C@@H]([C@@H]([C@@H]([C@@H](C=C(C=C1OC)C)C)O)CC)O)C)[C@H]([C@@H](O)[C@@H]([C@@]2(O[C@H](/C=C/C)[C@@H](C)[C@@H](C2)O[C@@H]3O[C@H]([C@H](O)[C@H]([C@H]3O)O)C)O)C)C '
               'NAME: TAN-1323C REASON: CORRECT Found macrocyclic lactone ring '
               'of size 18 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CCOC(=O)CCC(=O)O[C@H]1[C@H](O[C@@H]2[C@@H](C)[C@H](O[C@H]3C[C@@](C)(OC)[C@@H](O)[C@H](C)O3)[C@@H](C)C(=O)O[C@H](CC)[C@@](C)(O)[C@H](O)[C@@H](C)C(=O)[C@H](C)C[C@@]2(C)O)O[C@H](C)C[C@@H]1N(C)C '
               'NAME: erythromycin ethylsuccinate REASON: CORRECT Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O1C23OC(O)(C(CC2(C)C)C)CC(OC(CC(OC(C3)C(C1C(CCC(OC)C4=CC(O)=CC=C4)C)C)=O)C(O)C)=O '
               'NAME: Aplysiatoxin, 17-debromo- REASON: CORRECT Found '
               'macrocyclic lactone ring of size 12 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'C[C@H]1CC[C@]2(C[C@@H]3C[C@H](O2)CC=C([C@H]([C@H](C=CC=C4CO[C@H]5[C@@]4([C@@H](C=C(C5=NO)C)C(=O)O3)O)C)OC6C[C@@H](C([C@@H](O6)C)O)OC)C)O[C@@H]1C7CCCCC7 '
               'NAME: LSM-1662 REASON: CORRECT Found macrocyclic lactone ring '
               'of size 16 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC(C(C(O)CCCN)C)CC=CC(O)CC(O)CC(O)C(C(O)C(C(O)CC(O)CC(O)C(C(O)C(O[C@H]2O[C@@H]([C@@H](O)[C@@H]([C@@H]2O)O)CO)C=C(C(C(C=CC(C(C=CCCC(C(C(C(C=CC=C1C)C)O)C)O)C)O)C)O)C)C)C)C '
               'NAME: Desertomycin G REASON: CORRECT Found macrocyclic lactone '
               'ring of size 42 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CC(O)CCCCCCCCCCCCCCC(CCCCCCCCCCCCCC1CC(=O)OC[C@H]2O[C@@H](OC(CCCCCCCCCCCCCC(CCCCCC(C)O)O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)CC(=O)OC[C@H]3O[C@@H](O1)[C@H](O)[C@@H](O)[C@@H]3O)[C@H](O)[C@@H](O)[C@@H]2O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: fattiviracin A1 REASON: CORRECT Found macrocyclic '
               'lactone ring of size 18 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'P(=O)(O[C@@H]1[C@@H]2O[C@@H]2[C@@H](O)[C@H](O)CCCCCCCCC=CCCC[C@H](OC(C=CC1)=O)C)(OCCN)O '
               'NAME: AKML D REASON: CORRECT Found macrocyclic lactone ring of '
               'size 24 with ester bond: oxygen in ring attached to carbonyl '
               'carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CC[C@H]1OC(=O)[C@H](C)[C@@H](O[C@H]2C[C@@](C)(O)[C@@H](O)[C@H](C)O2)[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2O)N(C)C)[C@](C)(O)C[C@@H](C)C(=O)[C@H](C)[C@@H](O)[C@]1(C)O '
               'NAME: erythromycin C REASON: CORRECT Found macrocyclic lactone '
               'ring of size 14 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               'False positives: SMILES: '
               'P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@@H](CC=CCCCC(OC[C@@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COP(O1)(O)=O)=O)C=CC(=O)[C@@H]([C@H](O)[C@@H]2O)/C=C/[C@@H](O)CCCCC)(O)=O '
               'NAME: CDP-DG(PGJ2/20:2(11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Found macrocyclic lactone ring of size 21 with ester bond: '
               'oxygen in ring attached to carbonyl carbon (carbonyl oxygen '
               'exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@H](CCCCCC(C2=C(C1)C=C(O)C=C2O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)O)CO)=O)C '
               'NAME: Curvularin-7-O-beta-D-glucopyranoside REASON: WRONGLY '
               'CLASSIFIED Found macrocyclic lactone ring of size 12 with '
               'ester bond: oxygen in ring attached to carbonyl carbon '
               '(carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@@H](CC=CCCCC(O[C@@H](COP(O1)(O)=O)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)C=CC(=O)[C@@H]([C@H](O)[C@@H]2O)/C=C/[C@@H](O)CCCCC)(O)=O '
               'NAME: CDP-DG(22:5(4Z,7Z,10Z,13Z,16Z)/PGJ2) REASON: WRONGLY '
               'CLASSIFIED Found macrocyclic lactone ring of size 20 with '
               'ester bond: oxygen in ring attached to carbonyl carbon '
               '(carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=CC[C@H](C)CCC[C@H](C=C1)O)CO)CC4=CC=CC=C4 '
               'NAME: Cytochalazin Z2 REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@H]([C@@H](O)C[C@@H](O)[C@@H]([C@H](O)[C@@H]2O)/C=C\\[C@@H](O)CCCCC)CC=CCCCC(O[C@@H](COP(O1)(O)=O)COC(=O)CCCCCCCCCCCCCCCCC(C)C)=O)(O)=O '
               'NAME: CDP-DG(i-20:0/PGF2alpha) REASON: WRONGLY CLASSIFIED '
               'Found macrocyclic lactone ring of size 20 with ester bond: '
               'oxygen in ring attached to carbonyl carbon (carbonyl oxygen '
               'exocyclic).\n'
               ' * SMILES: '
               'CO[C@H]1C[C@H](O[C@H]2[C@@H](C)\\C=C\\C=C3/CO[C@@H]4[C@H](OC)C(C)=C[C@@H](C(=O)O[C@H]5C[C@@H](C\\C=C2/C)O[C@]2(C5)C[C@H](O)[C@H](C)[C@H](O2)C(C)C)[C@]34O)O[C@@H](C)[C@@H]1O '
               'NAME: Avermectin A2b monosaccharide REASON: WRONGLY CLASSIFIED '
               'Found macrocyclic lactone ring of size 16 with ester bond: '
               'oxygen in ring attached to carbonyl carbon (carbonyl oxygen '
               'exocyclic).\n'
               ' * SMILES: '
               'CO[C@H]1C[C@@H](O[C@@H](C)[C@@H]1O)O[C@H]1[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2OP([O-])([O-])=O)[NH+](C)C)[C@@H](C)C[C@@]2(CO2)C(=O)[C@H](C)[C@@H](O)[C@@H](C)[C@@H](C)OC(=O)[C@@H]1C '
               "NAME: oleandomycin 2'-O-phosphate(1-) REASON: WRONGLY "
               'CLASSIFIED Found macrocyclic lactone ring of size 14 with '
               'ester bond: oxygen in ring attached to carbonyl carbon '
               '(carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC[C@]2([C@H]3[C@@]([C@H](C(=C)CC3)CO[C@@H](C(=O)O)[C@@H](C(=O)OC[C@]4([C@H]5[C@@]([C@@H](CO[C@H]([C@@H]1CC(=O)O)C(=O)O)C(=C)CC5)(CCC4)C)C)CC(=O)O)(CCC2)C)C '
               'NAME: Cryptoporic acid D REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 22 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: O1OC(=O)[C@H](N)CCC(OOC(=O)CCC(N)C1=O)=O NAME: '
               'Glutamic acid glutamate REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC(/C(=C/C=C/C(O)(CC2OC2C(C(O)CC)C)C)/C)C(C=CC(OC(=O)C)C(CCC(C1)O)(O)C)C '
               'NAME: Pladienolide D REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 12 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OCCC2=CC(OC3=CC=C(C[C@]14OC(=O)C(=C4C=5C=COC(CC5)=O)O)C=C3)=C(O)C(=C2)O '
               'NAME: Retipolide D REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CC[C@H]1OC(=O)[C@H](C)C(=O)[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2O)[NH+](C)C)[C@@H](C)C[C@@H](C)C(=O)\\C=C\\[C@H]1C '
               'NAME: narbomycin(1+) REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CC[C@H]1OC(=O)C[C@@H](O)[C@H](C)[C@@H](O[C@@H]2O[C@H](C)[C@@H](O)[C@@H]([C@H]2O)[NH+](C)C)[C@@H](CC=O)C[C@@H](C)C(=O)\\C=C\\C(\\C)=C\\[C@@H]1CO[C@@H]1O[C@H](C)[C@@H](O)[C@@H](O)[C@H]1O '
               'NAME: demethyllactenocin(1+) REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 16 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@H](C[C@@H](OC(=O)[C@@H](NC(=O)CCC)CCCCN)[C@H]2O[C@H]2[C@H](C=CC=3C1=C(O)C=CC3)O)CC=CNC(=O)C=CC=NOC '
               'NAME: Necroxime B REASON: WRONGLY CLASSIFIED Found macrocyclic '
               'lactone ring of size 12 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@@H]([C@@H](O)/C(=C/C=C/C(=C/C=2N=C(C)OC2)/C)/C)C)C[C@H](O)C(=CC=C[C@H]([C@@H](C[C@@H](CC=C1)CC(=O)O)O)C)C '
               'NAME: Rhizoxin D3 REASON: WRONGLY CLASSIFIED Found macrocyclic '
               'lactone ring of size 16 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'S(OC1C2OC(=O)C=3C(C=4C(C(OCC1OC(O)C2O)=O)=CC(O)=C(O)C4O)=C(O)C(O)=C(O)C3)(O)(=O)=O '
               'NAME: '
               '{6,7,8,11,12,13,21,22-octahydroxy-3,16-dioxo-2,17,20-trioxatetracyclo[17.3.1.0?,?.0??,??]tricosa-4,6,8,10,12,14-hexaen-23-yl}oxidanesulfonic '
               'acid REASON: WRONGLY CLASSIFIED Found macrocyclic lactone ring '
               'of size 12 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC(C=CC(O)CC(O)CCCC(O)C(C(O)CCC(C(O)CC(O)CC(O)CCCC(C(C=C(C(CC(CCCC(C(C(CC=CC=C(C(C(C2OC(C1)(O)C(C(O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)N(C)C)C)C2)C)C)O)C)O)C)O)O)O)C)CCCC(C)C)O)C)C)C '
               'NAME: 28-deoxystambomycin C REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 49 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1OC(C(C(O)C(C(O)C(C(O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@@H](O)CC3)C)CC2)C)CC)C)C)C)CC=CC=CC(O)CC(O)C(C(O)CC(O[C@@H]4O[C@@H]([C@H](O)[C@@H]([C@H]4NC(=O)C)O)CO)C(C5CC(C(C(CC(C(CCC(CC(CC=CC=C1)O)O)C)O[C@@H]6O[C@@H]([C@@H](O)[C@@H]([C@H]6O[C@@H]7O[C@@H]([C@@H](O)[C@@H]([C@H]7O)O)C)O[C@@H]8O[C@@H]([C@@H](O)[C@@H](C8)O)C)C)(O5)O)O)O)C)C '
               'NAME: JBIR-139 REASON: WRONGLY CLASSIFIED Found macrocyclic '
               'lactone ring of size 32 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CCC(C)[C@H]1O[C@@]2(C[C@@H]3C[C@@H](C\\C=C(C)\\[C@@H](O[C@H]4C[C@H](OC)[C@@H](O[C@H]5C[C@H](OC)[C@@H](O)[C@H](C)O5)[C@H](C)O4)[C@@H](C)\\C=C\\C=C4/CO[C@@H]5[C@H](OC)C(C)=C[C@@H](C(=O)O3)[C@]45O)O2)C[C@H](O)[C@@H]1C '
               'NAME: Avermectin A2a REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 16 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@@H](CCCCCCC(O[C@@H](COP(O1)(O)=O)COC(=O)CCCCCCCCCCCCCCCCCCCCC(CC)C)=O)C(=O)C[C@@H](O)[C@@H]([C@H](O)[C@@H]2O)/C=C\\[C@@H](O)CCCCC)(O)=O '
               'NAME: CDP-DG(a-25:0/PGE1) REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 20 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'P1(O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@H]([C@@H](O)CC(O[C@@H]([C@@H](O)[C@H]2O)C=C[C@@H](O)CCCCC)O)CC=CCCCC(O[C@@H](CO1)COC(=O)CCCCCCC/C=C\\CCCCCC)=O)(O)=O '
               'NAME: PI(16:1(9Z)/TXB2) REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 18 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1[C@@H](C[C@@H](O)[C@@H]2O[C@](CCC=3C(O[C@H](C1)[C@H](C3O)CC)=O)(C)C[C@@H]2C)CO '
               'NAME: Mangromicin F REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 14 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@](O)([C@H]2O[C@H]2C=CC(=O)[C@@H](CC[C@@H]([C@H](C=C1)C)O[C@@H]3O[C@@H](C[C@@H](C3O)N(C)C)C)C)CO[C@@H]4OC([C@H](O)[C@@H]([C@@H]4OC)OC)C)CC '
               'NAME: Mycinamicin XII REASON: WRONGLY CLASSIFIED Found '
               'macrocyclic lactone ring of size 16 with ester bond: oxygen in '
               'ring attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'CCC(=O)O[C@@H]1CC(=O)O[C@@H](CC=CC=C[C@@H]([C@@H](C[C@@H]([C@@H]([C@H]1OC)OC2C(C(C(C(O2)C)OC3CC(C(C(O3)C)OC(=O)CC)(C)O)N(C)C)O)CC=O)C)O)C '
               'NAME: propanoic acid '
               '[(4R,5S,6S,7R,9R,10R,16R)-6-[[4-(dimethylamino)-3-hydroxy-5-[[4-hydroxy-4,6-dimethyl-5-(1-oxopropoxy)-2-oxanyl]oxy]-6-methyl-2-oxanyl]oxy]-10-hydroxy-5-methoxy-9,16-dimethyl-2-oxo-7-(2-oxoethyl)-1-oxacyclohexadeca-11,13-dien-4-yl] '
               'ester REASON: WRONGLY CLASSIFIED Found macrocyclic lactone '
               'ring of size 16 with ester bond: oxygen in ring attached to '
               'carbonyl carbon (carbonyl oxygen exocyclic).\n'
               ' * SMILES: '
               'O=C1C=CC=CC[C@H](OC(=O)C[C@H]([C@@H]([C@H]([C@H](C[C@H]1C)CC=O)O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@H]([C@H](OC(=O)CC)[C@@](C3)(O)C)C)[C@@H]([C@H]2O)N(C)C)C)OC)OC(=O)CC)C '
               'NAME: SF-837 A3 REASON: WRONGLY CLASSIFIED Found macrocyclic '
               'lactone ring of size 16 with ester bond: oxygen in ring '
               'attached to carbonyl carbon (carbonyl oxygen exocyclic).\n'
               'False negatives: SMILES: '
               'O=C1O[C@@H]2C[C@@H](O)[C@@H]3O[C@H](CC=CC=C[C@@H](C[C@H]4O[C@@H](C[C@@H]([C@]1(O)[C@H]2O)OC(=O)C)C[C@@H](O)C4)C)[C@@H](C3)C '
               'NAME: Mandelalide C REASON: MISSED No macrocyclic lactone ring '
               '(ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'O=C1OC(/C(=C/C=C/CCCCCCC)/C)CC(=O)NC[C@H](O)[C@@H](C(=O)NCCC=CC=CC=C1)C '
               'NAME: FR252921 REASON: MISSED No macrocyclic lactone ring '
               '(ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'O=C1OC(CC(=O)N[C@H](C(=O)OC(CC(N[C@H]1CO)=O)CCCCCCC)CO)CC=CCCCCCC '
               'NAME: Serratamolide B REASON: MISSED No macrocyclic lactone '
               'ring (ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'O=C1O[C@@H](C(O)(C)C)CCC(=CCCC(C)=CCOC2=C(C=3CN([C@H]1CCC(=O)OC)C(=O)C3C=C2OC)O)C '
               'NAME: Emericellolide B REASON: MISSED No macrocyclic lactone '
               'ring (ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'O=C1O[C@H](/C(=C/[C@H]2C[C@@H](O)[C@H](O)CC2)/C)[C@@H]([C@@H](O)CC(=O)[C@@H](C=C(C[C@@H](C[C@@H]([C@H]3O[C@](CC(N4[C@H]1CCCC4)=O)(O)[C@@H](C[C@@H]3OC)C)OC)C)C)CC=C)C '
               'NAME: 9-Deoxo-31-O-demethyl FK506 REASON: MISSED No '
               'macrocyclic lactone ring (ester embedded in a ring of 12 or '
               'more atoms) found\n'
               ' * SMILES: '
               'C[C@@H]1CC[C@H]2C[C@@H](C(=CC=CC=C[C@H](C[C@H](C(=O)[C@@H]([C@@H](C(=C[C@H](C(=O)C[C@H](OC(=O)[C@@H]3CCCCN3C(=O)C(=O)[C@@]1(O2)O)[C@H](C)C[C@@H]4CC[C@H]([C@@H](C4)OC)OCCO)C)C)O)OC)C)C)C)OC '
               'NAME: LSM-5313 REASON: MISSED No macrocyclic lactone ring '
               '(ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'ClC=1NC(C(=O)N[C@H]2[C@H](O)C[C@H](O[C@@H]3[C@H]4C=C[C@H]5CCCCC=C[C@@]6([C@]7(C(C(=C([C@]5([C@H]4CC[C@@H]3C)CC)O)C(=O)O7)=O)C[C@H](CC)C(=C6)C(=O)O)C)O[C@@H]2C)=C(C1)Cl '
               'NAME: Nai414-A REASON: MISSED No macrocyclic lactone ring '
               '(ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)O[C@H]([C@@H]([C@H](OC(=O)C)[C@H](C=C([C@H]([C@@H](C=C1)C)O)C)C)C)C)CC2=CC=CC=C2)C '
               'NAME: Torrubiellutin C REASON: MISSED No macrocyclic lactone '
               'ring (ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'CC1CCC2CC(C(=CC=CC=CC(CC(C(=O)C(C(C(=CC(C(=O)CC(OC(=O)C3CCCCN3C(=O)C(=O)C1(O2)O)C(C)CC4CCC(C(C4)OC)OCCO)C)C)O)OC)C)C)C)OC '
               'NAME: LSM-4258 REASON: MISSED No macrocyclic lactone ring '
               '(ester embedded in a ring of 12 or more atoms) found\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)O[C@H]([C@@H]([C@H](O)[C@H](C=C([C@H]([C@@H](C=C1)C)O)C)C)C)C)CC2=CC=CC=C2)C '
               'NAME: Torrubiellutin A REASON: MISSED No macrocyclic lactone '
               'ring (ester embedded in a ring of 12 or more atoms) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No lactone substructure (ester '
                                               'bond with exocyclic carbonyl '
                                               'oxygen) found.'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1O[C@@H]2C[C@@H](O)[C@@H]3O[C@H](CC=CC=C[C@@H](C[C@H]4O[C@@H](C[C@@H]([C@]1(O)[C@H]2O)OC(=O)C)C[C@@H](O)C4)C)[C@@H](C3)C',
                                      'name': 'Mandelalide C',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'O=C1OC(/C(=C/C=C/CCCCCCC)/C)CC(=O)NC[C@H](O)[C@@H](C(=O)NCCC=CC=CC=C1)C',
                                      'name': 'FR252921',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'O=C1OC(CC(=O)N[C@H](C(=O)OC(CC(N[C@H]1CO)=O)CCCCCCC)CO)CC=CCCCCCC',
                                      'name': 'Serratamolide B',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'P(=O)(O[C@@H]1[C@@H]2O[C@@H]2[C@@H](O)[C@H](O)CCCCCCCCC=CCCC[C@H](OC(C=CC1)=O)C)(OCCN)O',
                                      'name': 'AKML D',
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely not a macrolide '
                                                '(polyketide-derived) '
                                                'structure.'},
                                  {   'smiles': 'O=C1O[C@@H](C(O)(C)C)CCC(=CCCC(C)=CCOC2=C(C=3CN([C@H]1CCC(=O)OC)C(=O)C3C=C2OC)O)C',
                                      'name': 'Emericellolide B',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'O=C1O[C@H](/C(=C/[C@H]2C[C@@H](O)[C@H](O)CC2)/C)[C@@H]([C@@H](O)CC(=O)[C@@H](C=C(C[C@@H](C[C@@H]([C@H]3O[C@](CC(N4[C@H]1CCCC4)=O)(O)[C@@H](C[C@@H]3OC)C)OC)C)C)CC=C)C',
                                      'name': '9-Deoxo-31-O-demethyl FK506',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'C[C@@H]1CC[C@H]2C[C@@H](C(=CC=CC=C[C@H](C[C@H](C(=O)[C@@H]([C@@H](C(=C[C@H](C(=O)C[C@H](OC(=O)[C@@H]3CCCCN3C(=O)C(=O)[C@@]1(O2)O)[C@H](C)C[C@@H]4CC[C@H]([C@@H](C4)OC)OCCO)C)C)O)OC)C)C)C)OC',
                                      'name': 'LSM-5313',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'ClC=1NC(C(=O)N[C@H]2[C@H](O)C[C@H](O[C@@H]3[C@H]4C=C[C@H]5CCCCC=C[C@@]6([C@]7(C(C(=C([C@]5([C@H]4CC[C@@H]3C)CC)O)C(=O)O7)=O)C[C@H](CC)C(=C6)C(=O)O)C)O[C@@H]2C)=C(C1)Cl',
                                      'name': 'Nai414-A',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'O=C1N([C@H](C(=O)O[C@H]([C@@H]([C@H](OC(=O)C)[C@H](C=C([C@H]([C@@H](C=C1)C)O)C)C)C)C)CC2=CC=CC=C2)C',
                                      'name': 'Torrubiellutin C',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'},
                                  {   'smiles': 'CC1CCC2CC(C(=CC=CC=CC(CC(C(=O)C(C(C(=CC(C(=O)CC(OC(=O)C3CCCCN3C(=O)C(=O)C1(O2)O)C(C)CC4CCC(C(C4)OC)OCCO)C)C)O)OC)C)C)C)OC',
                                      'name': 'LSM-4258',
                                      'reason': 'No macrocyclic lactone ring '
                                                '(ester embedded in a ring of '
                                                '12 or more atoms) found'}],
    'attempt': 3,
    'reasoning': 'Below is our revised Python program. In our reasoning we '
                 'noticed that simply iterating over bonds in all large rings '
                 '(size ≥12) could both miss lactone features that are better '
                 'captured by a SMARTS query and inadvertently mark molecules '
                 'with “macrolactone‐like” rings that are not '
                 'polyketide‐derived (for example those containing '
                 'phosphorus). In our new approach we therefore:\n'
                 '\n'
                 '1. Immediately reject molecules containing phosphorus (P, '
                 'atomic number 15) because macrolide polyketides typically do '
                 'not contain this element.\n'
                 '2. Use a SMARTS pattern to search for a lactone substructure '
                 'encoded as an oxygen (that is in a ring) bonded to a carbon '
                 '(also in a ring) that carries a C=O where the carbonyl '
                 'oxygen is exocyclic (not in the ring). This pattern is '
                 'written as "[O;r]-[C;r](=[O;!r])".\n'
                 '3. For each substructure match we then look among the '
                 'RDKit‐determined rings to check whether the two ring atoms '
                 '(the oxygen and its bonded carbon) belong to at least one '
                 'ring of size 12 or greater and that that ring does not '
                 'include any nitrogen atom. (This helps focus on '
                 'polyketide‐derived rings.)\n'
                 '4. Only if such a match is found do we classify the molecule '
                 'as a macrolide; otherwise we return False along with an '
                 'explanation.\n'
                 '\n'
                 'Below is the complete code in one code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1104,
    'num_false_positives': 577,
    'num_true_negatives': 140496,
    'num_false_negatives': 123,
    'num_negatives': None,
    'precision': 0.6567519333729923,
    'recall': 0.8997555012224939,
    'f1': 0.7592847317744155,
    'accuracy': 0.9950808151791989,
    'negative_predictive_value': 0.9991252960126299}