"""
Classifies: CHEBI:18133 hexose
"""
"""
Classifies: CHEBI:18133 hexose
"""
from rdkit import Chem
from rdkit.Chem import Mol, MolFromSmiles, rdMolDescriptors
from rdkit.Chem.rdchem import AtomValenceException

def is_hexose(smiles: str):
    """
    Determines if a molecule is a hexose based on its SMILES string.
    A hexose is a six-carbon monosaccharide with either an aldehyde group (aldohexose)
    or a ketone group (ketohexose) in its linear form.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hexose, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES"

        # Basic checks for monosaccharide structure
        # Total carbons must be exactly 6
        c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
        if c_count != 6:
            return False, f"Has {c_count} carbons (needs 6)"

        # Exclude derivatives with non-sugar components
        for atom in mol.GetAtoms():
            if atom.GetAtomicNum() not in {1, 6, 8}:  # Only allow H, C, O
                return False, "Contains non-C/H/O atoms"
            if atom.GetFormalCharge() != 0:
                return False, "Charged groups present"

        # Check for forbidden functional groups
        forbidden_patterns = [
            Chem.MolFromSmarts(patt) for patt in [
                '[#15]', '[#16]',          # Phosphorus/Sulfur
                '[NX3][CX3](=O)',          # Amides
                '[OX2][CX3]=O',            # Esters
                '[NX3+!H0]',               # Amines (charged)
                '[CX3](=O)[OX2H1]'         # Carboxylic acids
            ]
        ]
        for patt in forbidden_patterns:
            if mol.HasSubstructMatch(patt):
                return False, "Contains forbidden group"

        # Check for glycosidic bonds (ethers not in rings)
        ether_pattern = Chem.MolFromSmarts('[OX2;!R]([#6])[#6]')
        if mol.HasSubstructMatch(ether_pattern):
            return False, "Glycosidic bond present"

        # Check linear forms first
        # Aldehyde check (terminal CH=O, allowing explicit H)
        aldehyde_pattern = Chem.MolFromSmarts('[CH0X3]=O')  # Matches [H]C=O
        aldehyde_matches = mol.GetSubstructMatches(aldehyde_pattern)
        if aldehyde_matches:
            for match in aldehyde_matches:
                ald_atom = mol.GetAtomWithIdx(match[0])
                # Must be terminal (only one neighbor)
                if ald_atom.GetDegree() == 1:
                    return True, "Aldehyde group detected (aldohexose)"
            return False, "Aldehyde not terminal"

        # Ketone check (C=O at position 2 in 6-carbon chain)
        ketone_pattern = Chem.MolFromSmarts('[CX3]=O')
        ketone_matches = mol.GetSubstructMatches(ketone_pattern)
        if ketone_matches:
            # Get longest chain (assumed to be the sugar backbone)
            main_chain = Chem.GetLongestChain(mol)
            if len(main_chain) == 6:  # Must be 6 carbons in chain
                ketone_positions = [mol.GetAtomWithIdx(m[0]).GetIdx() for m in ketone_matches]
                # Position 2 in chain is index 1 (0-based)
                if main_chain[1] in ketone_positions:
                    return True, "Ketone at position 2 (ketohexose)"
            return False, "Ketone not at position 2"

        # Check cyclic forms (pyranose/furanose)
        ring_info = mol.GetRingInfo()
        rings = ring_info.AtomRings()
        valid_cyclic = False
        for ring in rings:
            if len(ring) not in {5,6}:
                continue  # Only 5/6 membered rings
            
            # Check for exactly one oxygen in the ring
            o_count = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8)
            if o_count != 1:
                continue
            
            # Count hydroxyl groups attached to ring atoms
            oh_count = 0
            for idx in ring:
                atom = mol.GetAtomWithIdx(idx)
                if atom.GetAtomicNum() == 8:
                    continue  # Skip the ring oxygen
                # Check for -OH groups
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetAtomicNum() == 8 and neighbor.GetTotalNumHs() > 0:
                        oh_count += 1
                        break  # Count once per ring atom
            
            # Pyranose (6-membered) needs >=4 OHs, furanose (5) >=3
            if (len(ring) == 6 and oh_count >=4) or (len(ring) ==5 and oh_count >=3):
                valid_cyclic = True
                break
        
        if valid_cyclic:
            return True, "Valid cyclic hexose form"
        
        return False, "No aldehyde/ketone or valid cyclic structure"

    except AtomValenceException:
        return False, "Invalid valence"
    except Exception as e:
        return False, f"Processing error: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18133',
                          'name': 'hexose',
                          'definition': 'Any six-carbon monosaccharide which '
                                        'in its linear form contains either an '
                                        'aldehyde group at position 1 '
                                        '(aldohexose) or a ketone group at '
                                        'position 2 (ketohexose).',
                          'parents': ['CHEBI:35381'],
                          'xrefs': [   'GlyGen:G70994MS',
                                       'GlyTouCan:G70994MS',
                                       'KEGG:C00738'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 18,
                           'log_lines_of_code': 2.8903717578961645,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import Mol, '
                                          'MolFromSmiles, rdMolDescriptors',
                                          'from rdkit.Chem.rdchem import '
                                          'AtomValenceException'],
                           'imports_count': 3,
                           'methods_called': ['MolFromSmiles'],
                           'methods_called_count': 1,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_hexose(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES"',
                                          'False, "Invalid valence"',
                                          'False, f"Processing error: '
                                          '{str(e)}"'],
                           'returns_count': 3,
                           'complexity': 2.178074351579233},
    'message': '\n'
               'Attempt failed: F1 score of 0.10740885927087417 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C[C@H]1O[C@H](O)[C@@H](O)C[C@@H]1O '
               'NAME: alpha-tyvelopyranose REASON: CORRECT Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-talofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@H](O)CO NAME: '
               'alpha-D-gulofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: C[C@H]1OC(O)[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'D-fucopyranose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O NAME: '
               'beta-D-talopyranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO NAME: '
               'beta-D-idofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@](O)(CO)[C@@H](O)[C@H]1O NAME: '
               'beta-D-tagatofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O)C NAME: '
               '6-deoxy-alpha-L-talopyranose REASON: CORRECT Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-mannose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: C[C@@H]1O[C@@H](O)[C@@H](O)C[C@@H]1O NAME: '
               '3,6-Dideoxy-L-galactose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@](O)(CO)[C@H](O)[C@H]1O NAME: '
               'beta-D-sorbofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@@](O)(CO)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-tagatofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@@H](O)C1O)[C@H](O)CO NAME: '
               'D-glucofuranose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-D-glucose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: C[C@@H](O)[C@H]1O[C@H](O)[C@@H](O)[C@H]1O NAME: '
               'alpha-D-rhamnofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@@]([C@H](O)[C@@H](O)[C@@H]1O)([C@H](O)CO)[H] '
               'NAME: beta-D-glucofuranose REASON: CORRECT Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O NAME: '
               'alpha-L-galactose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O NAME: '
               'alpha-L-gulose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@H](O)C1O)[C@H](O)CO NAME: '
               'D-talofuranose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: C[C@H](O)[C@@H]1O[C@H](O)[C@H](O)[C@@H]1O NAME: '
               'beta-L-rhamnofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@@H]([C@H](O)[C@H](O)C1O)[C@@H](O)CO NAME: '
               'L-gulofuranose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: OC[C@@H]1O[C@H](O)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'beta-L-mannose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@H](O)[C@@H](O)C1O)[C@H](O)C NAME: '
               'D-fucofuranose REASON: CORRECT Cyclic form with ring oxygen '
               'and hydroxyls\n'
               ' * SMILES: O1[C@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO NAME: '
               'beta-L-mannofuranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1OC(O)C[C@@H](O)[C@@H]1O NAME: '
               '2-deoxy-D-glucopyranose REASON: CORRECT Cyclic form with ring '
               'oxygen and hydroxyls\n'
               'False positives: SMILES: '
               'O=C1C=C([C@@H](O)[C@H]2[C@@]1(O2)CC=C(CCC=C(CCC(O)C(O)(C)C)C)C)C '
               'NAME: Premacrophorintriol-I REASON: WRONGLY CLASSIFIED Cyclic '
               'form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'CC(=O)C1=C(O)C=C2Oc3c(C(C)=O)c(O)c(C)c(O)c3[C@]2(C)C1=O NAME: '
               '(-)-usnic acid REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'OC1=C(C\\C=C(\\CCC2C3(C(C(CCC3)(C)C)CCC2=C)C)/C)C(O)=CC=4OC(=C(O)C(=O)C14)C5=CC=C(O)C=C5 '
               'NAME: Denticulaflavonol REASON: WRONGLY CLASSIFIED Cyclic form '
               'with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O=C(C1=C(O)C(=C(O)C(=C1)CC(C)C)C(=O)C)C(C2O[C@@H](O)C3(O[C@H]3CC)[C@@H](C2)O)CCC '
               'NAME: Luminacin H REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O=C(/C(=C/C)/C)[C@H](C1=C(O)C=2O[C@]3([C@@H]([C@@]4([C@H](O[C@@H](C(O)(C)C)CC4)CC3)C)[C@@H](C2C(=C1)O)O)C)C '
               'NAME: Bipolahydroquinone C REASON: WRONGLY CLASSIFIED Cyclic '
               'form with ring oxygen and hydroxyls\n'
               ' * SMILES: C[C@H]1OC2=CC3=C(C(O)=CC(O)=C3)C(O)=C2C(=O)[C@@H]1C '
               'NAME: hemiustilaginoidin D REASON: WRONGLY CLASSIFIED Cyclic '
               'form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O1[C@]([C@H](O)[C@@H](O)[C@H](O)[C@H]1CO)(C2=C(O)C3=C(O[C@@H](CC3=O)C4=CC=C(O)C=C4)C=C2O)[H] '
               'NAME: Hemiphloin REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'Cl[C@@H]1C[C@@]2([C@]([C@@]3(O[C@@]3([C@H]([C@H]2/C=C/C=C(/[C@@H](O)[C@H](CO)C)\\C)/C(/C)=C/C)C)[H])(C[C@]1(O)C)[H])[H] '
               'NAME: dehydroxychlorofusarielin B REASON: WRONGLY CLASSIFIED '
               'Cyclic form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'Cc1cn2c(nc3n(cnc3c2=O)[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)[nH]1 '
               'NAME: 4-demethylwyosine REASON: WRONGLY CLASSIFIED Cyclic form '
               'with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O1C(C=CC=2C1=C(C=3OC=C(C(=O)C3C2O)C4=CC(O)=C(O)C=C4)CC=C(C)C)(C)C '
               'NAME: Auriculasin REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=CC(NC1=O)=NO '
               'NAME: N(4)-hydroxycytidine REASON: WRONGLY CLASSIFIED Cyclic '
               'form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'C=12OC(=CC(C1C(=CC(=C2[C@@H]3[C@@H](CN(CC3)C)O)O)O)=O)C4=C(C=CC=C4)Cl '
               'NAME: alvocidib REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O1[C@H](O)C2[C@@H]3[C@@H]([C@@]4(CC[C@@]5(C([C@H]4CC2)=C(C(C)C)CC5)C)C)O[C@H]6C3([C@@H]1[C@H](O)CO6)O '
               'NAME: CJ-14,258 REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O1[C@@]2(O)C(=C)[C@@H]3[C@@H](C(C)(C)C3)[C@@H]([C@@H]([C@]2(C)CC1)O)O '
               'NAME: 2S,3R,7S-trihydroxy-carophyllan-[4,7]-6,8-oxide REASON: '
               'WRONGLY CLASSIFIED Cyclic form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O1[C@@]2([C@@H](O)C=C([C@H]([C@H]12)O)CO)[C@@H](O)C=C(/C=C/[C@H]3C(=CC[C@H](C3(C)C)O)C)C '
               'NAME: Arthrosporol B REASON: WRONGLY CLASSIFIED Cyclic form '
               'with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               '[H][C@@]12O[C@@]11C[C@H](O)C(C)(C)O[C@@]1([H])C(CO)=C([C@H]2O)\\C=C\\CCCCC '
               'NAME: Cytosporin D REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: OC1C[C@H](Oc2cc(O)cc(O)c12)c1ccc(O)cc1 NAME: '
               'apiforol REASON: WRONGLY CLASSIFIED Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1C(C(O)C(O)C=2C1=CC(O)=CC2O)C3=CC=C(O)C=C3 NAME: '
               'Leucopelargonidin REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               ' * SMILES: OC[C@H]1O[C@H](O)[C@@H](F)[C@@H](O)[C@@H]1O NAME: '
               '2-deoxy-2-fluoro-alpha-D-mannose REASON: WRONGLY CLASSIFIED '
               'Cyclic form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O1[C@@H](N2C=C(C(=NC2=O)N)CO)[C@H](O)[C@H](O)[C@H]1CO NAME: '
               '5-Hydroxymethylcytidine REASON: WRONGLY CLASSIFIED Cyclic form '
               'with ring oxygen and hydroxyls\n'
               ' * SMILES: O1C(C2=CC(O)=C(O)C=C2)=CC(=O)C3=C1C=C(O)C=C3 NAME: '
               "7,3',4'-Trihydroxyflavone REASON: WRONGLY CLASSIFIED Cyclic "
               'form with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)cc(O)c2c1oc(cc2=O)-c1ccc(O)cc1 '
               'NAME: vitexin REASON: WRONGLY CLASSIFIED Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O=C1OC(=CC(=C1C(O)C(O)C(O)C)O)/C=C/C NAME: '
               'Curvulapyrone REASON: WRONGLY CLASSIFIED Cyclic form with ring '
               'oxygen and hydroxyls\n'
               ' * SMILES: O1[C@H](O)[C@H](O)[C@H](O)[C@@H](O)C1 NAME: '
               'beta-L-lyxopyranose REASON: WRONGLY CLASSIFIED Cyclic form '
               'with ring oxygen and hydroxyls\n'
               ' * SMILES: '
               'O=C1[C@]2(OC3=C(C(=C(C)C4=C3C[C@@](CO)(C)C4)CCO)CC2)C5(C(C)=C6[C@]1(O)C[C@@](CO)(C)C6)CC5 '
               'NAME: Bovistol REASON: WRONGLY CLASSIFIED Cyclic form with '
               'ring oxygen and hydroxyls\n'
               'False negatives: SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@]1(O)NC(=O)C)CO NAME: '
               'N-acetyl-D-glucoseamine REASON: MISSED Contains amide\n'
               ' * SMILES: OC[C@H]([C@H](CC(CO)=O)O)O NAME: '
               '3-deoxy-keto-D-fructose REASON: MISSED No aldehyde, ketone, or '
               'cyclic structure with ring oxygen\n'
               ' * SMILES: '
               'O=C(NCCC1=CC=CC=C1)[C@H](N[C@H](C(=O)NC=CC2=CC=C(O[C@@H]3O[C@@H]([C@H](NC(=O)C)[C@@H]([C@H]3O)O)C)C=C2)CC=4C5=C(C=CC=C5)N(C4)C)[C@H](CC)C '
               'NAME: Rhabdoplanin D REASON: MISSED Contains amide\n'
               ' * SMILES: '
               'C=1C=C(C=CC1C(=O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)N '
               'NAME: 1-O-(4-aminobenzoyl)-beta-D-glucopyranose REASON: MISSED '
               'Contains ester\n'
               ' * SMILES: [H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)CO NAME: '
               'aldehydo-D-galactose REASON: MISSED Aldehyde not terminal\n'
               ' * SMILES: '
               'O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)CC1=C(CC[C@@H]2[C@@]1(CCCC2(C)C)C)C '
               'NAME: Sporulositol A REASON: MISSED Glycosidic bond present\n'
               ' * SMILES: '
               'O=C(N[C@H]1C(O)C(O)[C@@H](O[C@@H]([C@H](N)[C@H](O)CO)[C@@H](O)CN)OC1CO)CCC '
               'NAME: Sorbistin A2 REASON: MISSED Contains amide\n'
               ' * SMILES: OC[C@@H]1CC(=O)C(O)=CO1 NAME: ascopyrone P REASON: '
               'MISSED Cyclic but only 2 hydroxyls\n'
               ' * SMILES: '
               '[H][C@](C)(O)[C@@]([H])(O)[C@]([H])(O)[C@]([H])(O)C=O NAME: '
               'aldehydo-D-rhamnose REASON: MISSED Aldehyde not terminal\n'
               ' * SMILES: OC[C@@H](O)[C@@H](O)[C@@H](O)C(=O)CO NAME: '
               'D-psicose REASON: MISSED No aldehyde, ketone, or cyclic '
               'structure with ring oxygen\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1NC=C2[C@@]3(O)[C@@H](O)[C@@H](OC2=C1OC(=O)[C@H]4[C@H]5[C@H](C=C[C@H]4C)C[C@H](C)CC5)[C@@H](O)CC3',
                                     'name': 'Arthpyrone D',
                                     'reason': 'Has 24 carbons (needs 6)'},
                                 {   'smiles': 'CCN(CC)S(=O)(=O)C1=CC=CC(=C1)C(=O)NC2=CC(=CC(=C2)C)C',
                                     'name': '3-(diethylsulfamoyl)-N-(3,5-dimethylphenyl)benzamide',
                                     'reason': 'Has 19 carbons (needs 6)'},
                                 {   'smiles': 'O=C1[C@@]([C@H]2[C@]([C@@H]3C(C[C@](C=C)(C)CC3)=CC2)(C)CC1)(CO[C@@H]4O[C@H](C(=O)O)[C@@H](O)[C@H]([C@@H]4O)O)C',
                                     'name': 'Virescenoside Z4',
                                     'reason': 'Has 26 carbons (needs 6)'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)NC3=CC=CC(=C3)C(F)(F)F)[C@@H](C)CO',
                                     'name': '1-[[(8S,9S)-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-1-methyl-3-[3-(trifluoromethyl)phenyl]urea',
                                     'reason': 'Has 24 carbons (needs 6)'},
                                 {   'smiles': 'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO)CO)[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@@H]%13NC(=O)C)CO',
                                     'name': 'CID 91846694',
                                     'reason': 'Has 110 carbons (needs 6)'},
                                 {   'smiles': 'CCOC(=O)NCC(C)(C)CNC(=O)OCC',
                                     'name': 'N-[3-(ethoxycarbonylamino)-2,2-dimethylpropyl]carbamic '
                                             'acid ethyl ester',
                                     'reason': 'Has 11 carbons (needs 6)'},
                                 {   'smiles': 'S1C(=NC(=C1)/C=C/C(OC)C(/C(/OC)=C\\C(=O)OC)C)C2N=C(C3(OC3)C)SC2',
                                     'name': 'Melithiazol K',
                                     'reason': 'Has 20 carbons (needs 6)'},
                                 {   'smiles': 'CCCCC\\C=C/C\\C=C/CCCCCC(=O)O[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)COC(=O)CCCCC\\C=C/C\\C=C/C\\C=C/CC',
                                     'name': '(2S)-1-O-(7Z,10Z,13Z)-hexadecatrienoyl-2-O-(7Z,10Z)-hexadecadienoyl-3-O-beta-D-galactopyranosyl-sn-glycerol',
                                     'reason': 'Has 41 carbons (needs 6)'},
                                 {   'smiles': 'CC(C)(C)OC(=O)N[C@H]1CCCCCC=C[C@@H]2C[C@]2(NC(=O)[C@@H]3C[C@H](CN3C1=O)OC(=O)N4CC5=C(C4)C(=CC=C5)F)CNS(=O)(=O)C6CC6',
                                     'name': 'LSM-5352',
                                     'reason': 'Has 35 carbons (needs 6)'},
                                 {   'smiles': 'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)C5OC4)COC(=O)CC6=COC=C6)O)C)C',
                                     'name': 'VM48642',
                                     'reason': 'Has 40 carbons (needs 6)'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@]1(O)NC(=O)C)CO',
                                      'name': 'N-acetyl-D-glucoseamine',
                                      'reason': 'Has 8 carbons (needs 6)'},
                                  {   'smiles': 'C[C@H]1O[C@H](O)[C@@H](O)C[C@@H]1O',
                                      'name': 'alpha-tyvelopyranose',
                                      'reason': 'No aldehyde/ketone or valid '
                                                'cyclic structure'},
                                  {   'smiles': 'OC[C@H]([C@H](CC(CO)=O)O)O',
                                      'name': '3-deoxy-keto-D-fructose',
                                      'reason': 'Aldehyde not terminal'},
                                  {   'smiles': 'O=C(NCCC1=CC=CC=C1)[C@H](N[C@H](C(=O)NC=CC2=CC=C(O[C@@H]3O[C@@H]([C@H](NC(=O)C)[C@@H]([C@H]3O)O)C)C=C2)CC=4C5=C(C=CC=C5)N(C4)C)[C@H](CC)C',
                                      'name': 'Rhabdoplanin D',
                                      'reason': 'Has 42 carbons (needs 6)'},
                                  {   'smiles': 'C=1C=C(C=CC1C(=O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)N',
                                      'name': '1-O-(4-aminobenzoyl)-beta-D-glucopyranose',
                                      'reason': 'Has 13 carbons (needs 6)'},
                                  {   'smiles': '[H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)CO',
                                      'name': 'aldehydo-D-galactose',
                                      'reason': 'Processing error: module '
                                                "'rdkit.Chem' has no attribute "
                                                "'GetLongestChain'"},
                                  {   'smiles': 'O([C@@H]([C@H](O)[C@H](O)CO)[C@H](O)CO)CC1=C(CC[C@@H]2[C@@]1(CCCC2(C)C)C)C',
                                      'name': 'Sporulositol A',
                                      'reason': 'Has 21 carbons (needs 6)'},
                                  {   'smiles': 'O=C(N[C@H]1C(O)C(O)[C@@H](O[C@@H]([C@H](N)[C@H](O)CO)[C@@H](O)CN)OC1CO)CCC',
                                      'name': 'Sorbistin A2',
                                      'reason': 'Has 16 carbons (needs 6)'},
                                  {   'smiles': 'OC[C@@H]1CC(=O)C(O)=CO1',
                                      'name': 'ascopyrone P',
                                      'reason': 'Aldehyde not terminal'},
                                  {   'smiles': '[H][C@](C)(O)[C@@]([H])(O)[C@]([H])(O)[C@]([H])(O)C=O',
                                      'name': 'aldehydo-D-rhamnose',
                                      'reason': 'Processing error: module '
                                                "'rdkit.Chem' has no attribute "
                                                "'GetLongestChain'"}],
    'attempt': 3,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's analyze why the previous code had a low F1 "
                 'score. \n'
                 '\n'
                 'First, looking at the false positives: many non-hexose '
                 'compounds were classified as hexoses because they have a '
                 'cyclic structure with ring oxygen and hydroxyls. The code '
                 'checks for any ring with oxygen and at least three '
                 'hydroxyls, which is too generic. For example, flavonoids or '
                 'other cyclic ethers with hydroxyls would pass this test. So, '
                 "the cyclic check needs to be stricter to ensure it's a "
                 'pyranose or furanose ring (5 or 6-membered rings with one '
                 'oxygen) and that the substituents are hydroxyls or '
                 'hydroxymethyl groups.\n'
                 '\n'
                 'False negatives occurred because the code excluded valid '
                 'hexoses with amides or esters. For example, '
                 'N-acetyl-D-glucoseamine was excluded due to the amide check, '
                 "but it's still a hexose derivative. The original problem "
                 'statement specifies "monosaccharide," so derivatives with '
                 'modifications like acetylation should be excluded. However, '
                 'the code might be too strict in blocking all amides and '
                 'esters. Wait, the problem says "hexose" is a monosaccharide, '
                 'so derivatives with substituents like N-acetyl or O-benzoyl '
                 'should be excluded. So the original code was correct in '
                 'excluding them, but in the test cases, some hexoses like '
                 'N-acetyl-D-glucoseamine were considered false negatives. '
                 'This suggests that the test cases might include derivatives, '
                 'but according to the problem statement, hexose is the base '
                 "monosaccharide. So the code's approach to exclude amides and "
                 'esters is correct, but perhaps the SMILES examples provided '
                 'include derivatives that are not true hexoses. Wait, looking '
                 'at the examples given, like N-acetyl-D-glucoseamine, these '
                 'are modified hexoses. So the problem statement might have '
                 'conflicting examples. The user\'s definition says "hexose is '
                 'a six-carbon monosaccharide", which implies the unmodified '
                 'form. Therefore, the code correctly excludes derivatives '
                 'with amides or esters, but the test cases include them as '
                 'positives, leading to false negatives. This is a conflict '
                 'between the problem statement and examples. However, the '
                 "user's latest instruction says to focus on the definition, "
                 'so the code should stick to the strict definition.\n'
                 '\n'
                 'Another issue: the aldehydo-D-galactose was missed because '
                 'the aldehyde check required the aldehyde to be terminal. The '
                 'SMILES [H]C(=O)... indicates an aldehyde (with explicit H), '
                 "but maybe the code's pattern [CH]=O didn't match because the "
                 'atom might have a different hybridization or the explicit H '
                 "wasn't considered. The aldehyde pattern should be adjusted "
                 'to catch such cases.\n'
                 '\n'
                 'For the cyclic form check: the code counts hydroxyls but '
                 "doesn't check if they're attached to the ring. Also, the "
                 'ring size should be 5 (furanose) or 6 (pyranose) members. '
                 "The previous code didn't check the ring size. So adding "
                 'checks for 5 or 6-membered rings with exactly one oxygen '
                 'atom would help.\n'
                 '\n'
                 'The ketose check was based on the position in the longest '
                 'chain, which might not work for cyclic forms. Also, in '
                 "linear form, the ketone should be at position 2. The code's "
                 'method to find the longest chain and check position might be '
                 'unreliable.\n'
                 '\n'
                 'So, the revised plan:\n'
                 '\n'
                 '1. **Aldehyde/Ketone Check**:\n'
                 '   - Improve aldehyde detection to include cases with '
                 'explicit H (like [H]C(=O)).\n'
                 "   - For ketones, ensure they're at position 2 in a 6-carbon "
                 'backbone. Maybe use a more reliable method to determine the '
                 'position.\n'
                 '\n'
                 '2. **Cyclic Form Check**:\n'
                 '   - Ensure the ring is 5 or 6-membered with exactly one '
                 'oxygen.\n'
                 '   - Check that the substituents on the ring are hydroxyls '
                 'or hydroxymethyl (for the open chain part).\n'
                 '\n'
                 '3. **Carbon Count**:\n'
                 '   - Verify the molecule has exactly 6 carbons. Some false '
                 'positives might have more carbons.\n'
                 '\n'
                 '4. **Derivative Exclusion**:\n'
                 '   - Continue excluding amides, esters, phosphates, '
                 'sulfates, etc., as these are not part of the base '
                 'monosaccharide.\n'
                 '\n'
                 '5. **Hydroxyl Check in Cyclic Form**:\n'
                 '   - Ensure that the ring has multiple hydroxyl groups (at '
                 'least 4, as typical for hexoses) attached to the ring '
                 'atoms.\n'
                 '\n'
                 '6. **Linear Form Detection**:\n'
                 '   - If the molecule is linear (no rings), check for '
                 'aldehyde or ketone groups in the correct positions.\n'
                 '\n'
                 "Let's adjust the code accordingly. For example, checking for "
                 '6 carbons, ensuring the ring is 5/6-membered with one O, and '
                 'hydroxyl groups. Also, fix the aldehyde pattern to catch '
                 'explicit H cases.\n'
                 '\n'
                 'Another problem in the previous code: the cyclic check '
                 'allowed any ring with oxygen and three hydroxyls, leading to '
                 'false positives. Now, we need to enforce that the ring is '
                 'part of the monosaccharide structure.\n'
                 '\n'
                 "Also, the code missed 3-deoxy-keto-D-fructose because it's a "
                 'linear ketohexose but the ketone position check might have '
                 "failed. The code's method of checking the longest chain's "
                 'position might not have correctly identified the ketone at '
                 'position 2.\n'
                 '\n'
                 'So, in the revised code:\n'
                 '\n'
                 '- Check that the molecule has exactly 6 carbons.\n'
                 '- For linear forms: aldehyde at position 1 (aldohexose) or '
                 'ketone at position 2 (ketohexose).\n'
                 '- For cyclic forms: 5 or 6-membered ring with one oxygen, '
                 'and sufficient hydroxyl groups.\n'
                 '- Exclude derivatives with non-sugar groups.\n'
                 '\n'
                 'Implementing these steps should reduce false positives and '
                 'negatives.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 119,
    'num_false_positives': 4,
    'num_true_negatives': 142051,
    'num_false_negatives': 126,
    'num_negatives': None,
    'precision': 0.967479674796748,
    'recall': 0.4857142857142857,
    'f1': 0.6467391304347826,
    'accuracy': 0.9990864371047083,
    'negative_predictive_value': 0.9991137807099602}