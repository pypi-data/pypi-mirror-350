"""
Classifies: CHEBI:27283 very long-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_very_long_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is a very long-chain fatty acid based on its SMILES string.
    A very long-chain fatty acid is a fatty acid with a carbon chain greater than C22.
    Ultra-long-chain fatty acids are a subset with chain length > C27.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a very long-chain fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group or its deprotonated form
    acid_pattern = Chem.MolFromSmarts("C(=O)[O;H1,-1]")
    acid_matches = mol.GetSubstructMatches(acid_pattern)
    if not acid_matches:
        return False, "No carboxylic acid group found"
    

    max_chain_length = 0
    for acid_match in acid_matches:
        carbonyl_carbon_idx = acid_match[0]
        
        # Get the carbon adjacent to the carbonyl carbon
        neighbors = mol.GetAtomWithIdx(carbonyl_carbon_idx).GetNeighbors()
        chain_start_carbons = [neighbor for neighbor in neighbors if neighbor.GetSymbol() == 'C']
        
        current_max_len = 0
        for start_carbon in chain_start_carbons:
            visited_atoms = {carbonyl_carbon_idx, start_carbon.GetIdx()} # keep track of visited atoms including carbonyl
            current_chain_length = 1
            
            
            queue = [(start_carbon.GetIdx(), 1, visited_atoms)] # start from the neighboring C, keeping track of visited atoms, and current length
           
            
            while queue:
              current_idx, current_len, current_visited = queue.pop(0)
              
              max_len_from_here = current_len
              
              
              neighbors = mol.GetAtomWithIdx(current_idx).GetNeighbors()
              
              next_carbons = []
              for neighbor in neighbors:
                neighbor_idx = neighbor.GetIdx()
                if neighbor.GetSymbol() == "C" and neighbor_idx not in current_visited:
                      
                  ring_info = mol.GetRingInfo()
                  if not ring_info.IsAtomInRingOfSize(neighbor_idx, 3) and not ring_info.IsAtomInRingOfSize(neighbor_idx, 4) and not ring_info.IsAtomInRingOfSize(neighbor_idx, 5) and not ring_info.IsAtomInRingOfSize(neighbor_idx, 6):
                      next_carbons.append( (neighbor_idx, current_len + 1, set(current_visited) | {neighbor_idx}) )
              
              
              
              if not next_carbons: #we reached the end of the chain
                
                current_max_len = max(current_max_len, current_len)
              else:
                  queue.extend(next_carbons)
            
            current_max_len += 1 # account for carbonyl C
            max_chain_length = max(max_chain_length, current_max_len)



    if max_chain_length > 27:
        return True, f"Ultra-long-chain fatty acid (C={max_chain_length})"
    elif max_chain_length > 22:
        return True, f"Very long-chain fatty acid (C={max_chain_length})"
    else:
        return False, f"Not a very long-chain fatty acid (C={max_chain_length})"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27283',
                          'name': 'very long-chain fatty acid',
                          'definition': 'A fatty acid which has a chain length '
                                        'greater than C22. Very long-chain '
                                        'fatty acids which have a chain length '
                                        'greater than C27 are also known as '
                                        'ultra-long-chain fatty acids.',
                          'parents': ['CHEBI:35366'],
                          'xrefs': ['LIPID_MAPS_instance:LMFA01010025'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 52,
                           'log_lines_of_code': 3.9512437185814275,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetSubstructMatches',
                                                 'GetNeighbors',
                                                 'MolFromSmarts',
                                                 'pop',
                                                 'extend',
                                                 'append',
                                                 'GetSymbol',
                                                 'IsAtomInRingOfSize',
                                                 'MolFromSmiles',
                                                 'GetIdx',
                                                 'GetAtomWithIdx',
                                                 'GetRingInfo'],
                           'methods_called_count': 12,
                           'smarts_strings': ['C(=O)[O;H1,-1]'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_very_long_chain_fatty_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No carboxylic acid group '
                                          'found"',
                                          'True, f"Ultra-long-chain fatty acid '
                                          '(C={max_chain_length})"',
                                          'True, f"Very long-chain fatty acid '
                                          '(C={max_chain_length})"',
                                          'False, f"Not a very long-chain '
                                          'fatty acid (C={max_chain_length})"'],
                           'returns_count': 5,
                           'complexity': 5.190248743716285},
    'message': '\n'
               'Attempt failed: F1 score of 0.1850582590815627 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCC(O)=O NAME: '
               '(15Z,18Z,21Z,24Z,27Z)-triacontapentaenoic acid REASON: CORRECT '
               'Ultra-long-chain fatty acid (C=29)\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCCCCCC(C)C NAME: '
               'Isopentacosanoic acid REASON: CORRECT Very long-chain fatty '
               'acid (C=23)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-{(1R)-1-hydroxy-12-[(1R,2S)-2-{14-[(1R,2S)-2-icosylcyclopropyl]tetradecyl}cyclopropyl]dodecyl}hexacosanoic '
               'acid REASON: CORRECT Ultra-long-chain fatty acid (C=53)\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCCCCCCCCC([2H])([2H])[2H] '
               'NAME: Cerotic acid(d3) REASON: CORRECT Very long-chain fatty '
               'acid (C=25)\n'
               ' * SMILES: O=C(O)C[C@@H](OC)CCCCCCCCCCCCCCCCCCCCC NAME: '
               '3-Methoxytetracosanoic acid REASON: CORRECT Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCCCC[C@H](O)[C@@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-16-{(1S,2R)-2-[(19S,20S)-19-hydroxy-20-methyloctatriacontyl]cyclopropyl}hexadecyl]hexacosanoic '
               'acid REASON: CORRECT Ultra-long-chain fatty acid (C=58)\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCC[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxylignoceric acid REASON: CORRECT Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: OC(=O)CCC\\C=C\\CC\\C=C\\CCCCCC\\C=C\\CCCCCCCC '
               'NAME: 5,9,17-hexacosatrienoic acid REASON: CORRECT Very '
               'long-chain fatty acid (C=25)\n'
               ' * SMILES: '
               'O=C(O)CCCCCCCC(O)C(O)CC(O)C(O)CC(O)C(O)C/C=C/CCCCCCCCC NAME: '
               '(E)-9,10,12,13,15,16-hexahydroxyoctacos-18-enoic acid REASON: '
               'CORRECT Very long-chain fatty acid (C=27)\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCC(O)=O '
               'NAME: (15Z,18Z,21Z,24Z)-triacontatetraenoic acid REASON: '
               'CORRECT Ultra-long-chain fatty acid (C=29)\n'
               ' * SMILES: OC(=O)CCC/C=C\\CC/C=C\\CCCCCCCCC/C=C\\CCCCCC NAME: '
               '27:3(5Z,9Z,20Z) REASON: CORRECT Very long-chain fatty acid '
               '(C=26)\n'
               ' * SMILES: OC(=O)CCC/C=C\\CC/C=C\\CCCCCCCCCCCCC(C)C NAME: '
               '23-methyl-5Z,9Z-tetracosadienoic acid REASON: CORRECT Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'triacontanoic acid REASON: CORRECT Ultra-long-chain fatty acid '
               '(C=29)\n'
               ' * SMILES: Br/C(/CC/C=C\\CCCCCCCCCCCCCCC)=C/CCCC(O)=O NAME: '
               '6-bromo-pentacosa-5E,9Z-dienoic acid REASON: CORRECT Very '
               'long-chain fatty acid (C=24)\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: tetracosanoic '
               'acid REASON: CORRECT Very long-chain fatty acid (C=23)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCCCC(O)=O '
               'NAME: (19Z,22Z,25Z,28Z,31Z)-tetratriacontapentaenoic acid '
               'REASON: CORRECT Ultra-long-chain fatty acid (C=33)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCCC(O)=O '
               'NAME: (18Z,21Z,24Z,27Z,30Z,33Z)-hexatriacontahexaenoic acid '
               'REASON: CORRECT Ultra-long-chain fatty acid (C=35)\n'
               ' * SMILES: CCCCCCCCCCCCCCCC\\C=C/CC\\C=C/CCCC(O)=O NAME: '
               '(5Z,9Z)-5,9-hexacosadienoic acid REASON: CORRECT Very '
               'long-chain fatty acid (C=25)\n'
               ' * SMILES: OC(=O)\\C=C\\C=C\\C=C\\CCCCCCCCCCCCCCCCCCCCCC NAME: '
               'Nonacosa-trienoic acid REASON: CORRECT Ultra-long-chain fatty '
               'acid (C=28)\n'
               ' * SMILES: [H]C(CCCCCCCCCCCCCCCCCCCCCCC)=C([H])C(O)=O NAME: '
               '2-hexacosenoic acid REASON: CORRECT Very long-chain fatty acid '
               '(C=25)\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'heptacosanoic acid REASON: CORRECT Very long-chain fatty acid '
               '(C=26)\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCC(O)C(O)=O NAME: '
               '(13Z,16Z,19Z,22Z)-2-hydroxyoctacosatetraenoic acid REASON: '
               'CORRECT Very long-chain fatty acid (C=27)\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'Tetracosanedioic acid REASON: CORRECT Very long-chain fatty '
               'acid (C=23)\n'
               ' * SMILES: Br/C(/CC/C=C\\CCCCCCCCCCCCCC)=C/CCCC(O)=O NAME: '
               '6-bromo-tetracosa-5E,9Z-dienoic acid REASON: CORRECT Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCC/C=C\\CCCCCC NAME: '
               '20Z-heptacosenoic acid REASON: CORRECT Very long-chain fatty '
               'acid (C=26)\n'
               'False positives: SMILES: '
               'C(CCCCCCCCC1C(CCCCCCCCCCC2C(CCCCCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](C([O-])=O)CCCCCCCCCCCCCCCCCCCCCCCC)C2)C1)CCCCCCCCC '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-22-{2-[10-(2-octadecylcyclopropyl)decyl]cyclopropyl}docosyl]hexacosanoate '
               'REASON: WRONGLY CLASSIFIED Ultra-long-chain fatty acid (C=57)\n'
               ' * SMILES: '
               'O=C1OC(C(C(O)CC=CC(O)CC(O)CC(O)C(C(O)C(C(O)CC(O)CC(O)CC(O)C(C=C(C(C(C=CC(C(C=CCCC(C(C(C(CCC=C1C)C)O)C)O)C)O)C)O)C)O[C@H]2O[C@@H]([C@@H](O)[C@@H]([C@@H]2O)O)CO)C)C)C)CCC(=O)O '
               'NAME: Oasomycin C REASON: WRONGLY CLASSIFIED Ultra-long-chain '
               'fatty acid (C=45)\n'
               ' * SMILES: '
               'O=C(O)/C(=C/C[C@H](OC(=O)C)[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](OC(=O)C)CC4)(C)C)C[C@H]3O)C)CC2)(C)[C@H](C1)O)C)C)/C '
               'NAME: '
               '(22S,24E)-3beta,22-diacetoxy-7alpha,15alpha-dihydroxylanosta-8,24-dien-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Very long-chain fatty acid '
               '(C=23)\n'
               ' * SMILES: '
               'O([C@@H]1[C@@]([C@]2([C@@]3([C@@]4(C3)[C@]([C@]5([C@](CC4)(C(CC5)[C@@H]([C@]6(OC(=O)C(=CC6)C)[H])C)C)C)(CC2)[H])CC1)[H])(C)C(O)=O)[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO '
               'NAME: '
               '(1S,3R,6S,7S,8R,11S,12S,16R)-7,12,16-Trimethyl-15-[(1S)-1-[(2S)-5-methyl-6-oxo-2,3-dihydropyran-2-yl]ethyl]-6-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxypentacyclo[9.7.0.01,3.03,8.012,16]octadecane-7-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Very long-chain fatty acid '
               '(C=23)\n'
               ' * SMILES: '
               'O=C(O)/C(=C/CC[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4(C(C([C@@H](OC(=O)C)CC4)(C)C)C[C@H]3O)C)CC2)(C)[C@H](C1)OC(=O)C)C)C)/C '
               'NAME: Ganoderique acid W REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: '
               'O(C1C(C2C(C3C(C4(C(C5C(CC4)(CCC(C5)(C)C)C(OC6OC(C(O)C(O)C6O)COC7OC(C(O)C(O)C7O)CO)=O)=CC3)C)(CC2)C)(CC1)C)(C)C(O)=O)C8OC(C(O)C(O)C8O)CO '
               'NAME: '
               '4,6a,6b,11,11,14b-Hexamethyl-3-{[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy}-8a-({[3,4,5-trihydroxy-6-({[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy}methyl)oxan-2-yl]oxy}carbonyl)-1,2,3,4,4a,5,6,6a,6b,7,8,8a,9,10,11,12,12a,14,14a,14b-icosahydropicene-4-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Very long-chain fatty acid '
               '(C=23)\n'
               ' * SMILES: '
               'C(CCCCCC1C(C1)CCCCCCCCCCC[C@@H](O)[C@H](C(O)=O)CCCCCCCCCCCCCCCCCCCCCCCC)CCCCCCCCC2C(C2)CCCCCCCCCCCCCCCCCCCC '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-12-{2-[14-(2-icosylcyclopropyl)tetradecyl]cyclopropyl}dodecyl]hexacosanoic '
               'acid REASON: WRONGLY CLASSIFIED Ultra-long-chain fatty acid '
               '(C=53)\n'
               ' * SMILES: '
               'C1=2NC(C=C3N=C(C=C4NC(=CC5=NC(=C1)C(=C5CCC(=O)[O-])CC(=O)[O-])C(=C4CC(=O)[O-])CCC(=O)[O-])C(=C3CC(=O)[O-])CCC(=O)[O-])=C(C2CC(=O)[O-])CCC(=O)[O-] '
               'NAME: uroporphyrin III(8-) REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=24)\n'
               ' * SMILES: '
               'OC(CC/C=C/[C@@]1(C=CC[C@]2(O1)O[C@]3(CC2)[C@@H](C[C@@]4([C@](O3)(C[C@](O4)([C@H]([C@@]5(O[C@@]([C@H]([C@H](C5)O)C)(C(=C)C[C@@]67C[C@H](C[C@@H](O6)[C@@]8([C@](O7)(C[C@]9(O8)[C@H](C[C@H](CN9)C)C)[H])[H])C)[H])O)O)[H])[H])[H])C)[H])=O '
               'NAME: Azaspiracid-5 REASON: WRONGLY CLASSIFIED '
               'Ultra-long-chain fatty acid (C=39)\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cccc3C(C4c5cccc(O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)c5C(=O)c5c(O)cc(cc45)C(O)=O)c4cc(cc(O)c4C(=O)c23)C(O)=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: sennoside REASON: WRONGLY CLASSIFIED Very long-chain '
               'fatty acid (C=26)\n'
               ' * SMILES: '
               'O=C1C2=C3[C@@](O)([C@@H](OC(=O)C)[C@]4([C@]2(C(=O)C[C@@H]4[C@@H](CCC=C(C(=O)O)C)C)C)C)C5CC([C@@](C(C1)[C@@]35C)(CO)C)=O '
               'NAME: Ganoleucoin AA REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: '
               'O=C(O)C(=CC[C@H](O)[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@H](O)CC4)(C)C)CC3)C)CC2)(C)CC1)C)C)C '
               'NAME: Astraeusin O REASON: WRONGLY CLASSIFIED Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCC([O-])=O '
               'NAME: (15Z,18Z,21Z,24Z,27Z)-triacontapentaenoate REASON: '
               'WRONGLY CLASSIFIED Ultra-long-chain fatty acid (C=29)\n'
               ' * SMILES: '
               'O=C1C([C@]2([C@@]3([C@@]4(C3)[C@]([C@]5([C@](CC4)([C@](CC5)([C@@H](CC/C=C(\\C)/C(O)=O)C)[H])C)C)(CC2)[H])CC1)[H])(C)C '
               'NAME: Mangiferonic acid REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=24)\n'
               ' * SMILES: CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC(O)=O NAME: '
               'Samuelssonic acid REASON: WRONGLY CLASSIFIED Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3([C@@H]1OC(=O)C)C)/C(=C\\C(=O)CC(C(=O)O)C)/C)C)[C@@H](O)C[C@@H]4[C@@]2(CCC(C4(C)C)=O)C '
               'NAME: '
               '12beta-Acetoxy-7beta-hydroxy-3,11,15,23-tetraoxo-5alpha-lanosta-8,20-dien-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Very long-chain fatty acid '
               '(C=23)\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@]([C@@H](O)[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CC/C=C(\\C)/C(O)=O)C)[H])[H])C '
               'NAME: '
               '3alpha,6alpha,7alpha,12alpha-Tetrahydroxy-5beta-cholest-24-en-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Very long-chain fatty acid '
               '(C=23)\n'
               ' * SMILES: '
               'O=C(O)C=C(C=CC1OC2(OC(C(C)CC2)CC=C(C=CC(O)C(C=CC(=O)O)C)C)CCC1(OC(=O)CCC(=O)O)CCCC)C '
               'NAME: Reveromycin A REASON: WRONGLY CLASSIFIED Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: '
               'O=C(O)[C@@H]([C@@]1(O[C@@]([C@@H](CC)[C@H]([C@@H]1C)O)([C@@H]([C@@H](O)[C@H](C(=O)[C@H]([C@H]2O[C@@]([C@@]3(O[C@]([C@@H](O)CCC)(CC)C[C@H]3C)O)(C)C[C@@H]2C)CC)C)C)C)O)CC '
               'NAME: Inostamycin REASON: WRONGLY CLASSIFIED Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: '
               'OC(CC(/C=C/[C@@]1(C=C(C[C@]2(O1)O[C@]3(CC2)[C@@H](C[C@@]4([C@](O3)(C[C@](O4)([C@H]([C@@]5(O[C@@]([C@H](CC5)C)(C(=C)C[C@@]67C[C@H](C[C@@H](O6)[C@@]8([C@](O7)(C[C@]9(O8)[C@H](C[C@H](CN9)C)C)[H])[H])C)[H])O)O)[H])[H])[H])C)C)[H])O)=O '
               'NAME: Azaspiracid-9 REASON: WRONGLY CLASSIFIED '
               'Ultra-long-chain fatty acid (C=39)\n'
               ' * SMILES: '
               'O=C(O)C1=CC(=C(O)C=C1)C/C=C(/CC/C=C(/CCC(=O)[C@](O)(CCC/C(=C\\CC(=O)O)/C)C)\\C)\\C '
               'NAME: Erythrolic acid B REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: '
               'C[C@H]1C=CC=CC=CC=CC=CC=CC=C[C@@H](C[C@@H]2[C@@H]([C@H](C[C@](O2)(C[C@H](C[C@H]([C@@H](CC[C@H](C[C@H](CC(=O)O[C@H]([C@@H]([C@@H]1O)C)C)O)O)O)O)O)O)O)C(=O)O)O[C@H]3[C@H]([C@H]([C@@H]([C@H](O3)C)O)N)O '
               'NAME: LSM-5443 REASON: WRONGLY CLASSIFIED Very long-chain '
               'fatty acid (C=23)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3([C@@H](O)CC(C3(C1)C)C(CC(=O)CC(C(=O)O)C)C)C)[C@@H](O)CC4C2(CC[C@@H](C4(C)C)O)C '
               'NAME: Ganoderic acid D REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: '
               'O=C1C=C2[C@@](O)(C(=O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@]4([C@]1([C@@H](/C(=C/C(=O)C[C@@H](C(=O)O)C)/C)C[C@H]4O)C)C '
               'NAME: Applanoic acid B REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=23)\n'
               ' * SMILES: '
               'O[C@H]1C=2[C@]3([C@@]([C@](CC3)([C@@H](CC/C=C(\\C)/C(O)=O)C)[H])(CCC2[C@@]4([C@](C([C@H](O)CC4)(C)C)(C1)[H])C)C)C '
               'NAME: Ganoderic acid U REASON: WRONGLY CLASSIFIED Very '
               'long-chain fatty acid (C=23)\n'
               'False negatives: SMILES: '
               'OC(=O)\\C=C\\C=C\\C=C\\C=C\\C=C\\CCCCCCCCCCC NAME: '
               'Docosa-2,4,6,8,10-pentaenoic acid REASON: MISSED Not a very '
               'long-chain fatty acid (C=21)\n'
               ' * SMILES: '
               'OC(C(O)C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\C/C=C\\CCC(O)=O NAME: '
               '13,14-DiHDPE REASON: MISSED Not a very long-chain fatty acid '
               '(C=21)\n'
               ' * SMILES: '
               'OC(C(O)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\CCC(O)=O NAME: '
               '7,8-DiHDPE REASON: MISSED Not a very long-chain fatty acid '
               '(C=21)\n'
               ' * SMILES: '
               'ClC1=C(O[C@@H]2O[C@H]([C@@H](O)[C@H]([C@H]2O)O)C)C=3C(=CC(C)=C(C3)O)C(=C1NC(=O)\\C=C/C=C\\C=C\\[C@@H]([C@@H](O)CC(=O)/C(=C/C[C@H](O)/C=C/[C@@H]([C@H](O)[C@H](/C=C(/C(=O)O)\\C)C)C)/C)C)O '
               'NAME: Naphthomycinoside REASON: MISSED Not a very long-chain '
               'fatty acid (C=22)\n'
               ' * SMILES: OC(=O)CCC/C=C\\CCCCCC/C=C\\C/C=C\\CCCCC NAME: '
               'Eranthic acid REASON: MISSED Not a very long-chain fatty acid '
               '(C=21)\n'
               ' * SMILES: C(CCCCCCCCC(O)=O)CC/C=C/C/C=C/CCCCC NAME: '
               '13,16-docosadienoic acid REASON: MISSED Not a very long-chain '
               'fatty acid (C=21)\n'
               ' * SMILES: OC(=O)CCCCC/C=C\\C/C=C\\C\\C=C\\CCCCCCCC NAME: '
               '(all-Z)-7,10,13-Docosatrienoic acid REASON: MISSED Not a very '
               'long-chain fatty acid (C=21)\n'
               ' * SMILES: OC(=O)CCCCCCCCCCC/C=C/CCCCCCCC NAME: '
               'trans-Brassidic acid REASON: MISSED Not a very long-chain '
               'fatty acid (C=21)\n'
               ' * SMILES: OC(=O)[C@H](C[C@H](CCCCCCCCCCCCCCCCCCC)C)C NAME: '
               'Mycosanoic  acid (C25) REASON: MISSED Not a very long-chain '
               'fatty acid (C=22)\n'
               ' * SMILES: OC(=O)CCC/C=C\\CCCCCCC(CCCC(CCCC(C)C)C)C NAME: '
               '22:1(5Z)(13Me,17Me,21Me) REASON: MISSED Not a very long-chain '
               'fatty acid (C=21)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'OC(=O)\\C=C\\C=C\\C=C\\C=C\\C=C\\CCCCCCCCCCC',
                                      'name': 'Docosa-2,4,6,8,10-pentaenoic '
                                              'acid',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\C/C=C\\CCC(O)=O',
                                      'name': '13,14-DiHDPE',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\CCC(O)=O',
                                      'name': '7,8-DiHDPE',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(=O)CCC/C=C\\CCCCCC/C=C\\C/C=C\\CCCCC',
                                      'name': 'Eranthic acid',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'C(CCCCCCCCC(O)=O)CC/C=C/C/C=C/CCCCC',
                                      'name': '13,16-docosadienoic acid',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(=O)CCCCCCCCCCCCCCCCCCCCC1=CC=CC=C1',
                                      'name': '21-phenyl heneicosanoic acid',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=21)'},
                                  {   'smiles': 'OC(=O)CCCCC/C=C\\C/C=C\\C\\C=C\\CCCCCCCC',
                                      'name': '(all-Z)-7,10,13-Docosatrienoic '
                                              'acid',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(=O)CCCCCCCCCCC/C=C/CCCCCCCC',
                                      'name': 'trans-Brassidic acid',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(=O)CCC/C=C\\CCCCCCC(CCCC(CCCC(C)C)C)C',
                                      'name': '22:1(5Z)(13Me,17Me,21Me)',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'},
                                  {   'smiles': 'OC(=O)CCCCC/C=C\\CCCCCCCCCCCCCC',
                                      'name': '22:1(7Z)',
                                      'reason': 'Not a very long-chain fatty '
                                                'acid (C=22)'}],
    'attempt': 3,
    'reasoning': "Okay, let's analyze the previous attempt and the provided "
                 'outcomes to improve the `is_very_long_chain_fatty_acid` '
                 'function.\n'
                 '\n'
                 '**Analysis of the Previous Attempt:**\n'
                 '\n'
                 '1.  **Correctly Identifies Many VL-CFA and UL-CFA:** The '
                 'code was able to correctly classify most of the very '
                 'long-chain fatty acids (VL-CFA) and ultra-long-chain fatty '
                 'acids (UL-CFA). It correctly identifies the carboxylic acid '
                 'group and the carbon chain.\n'
                 '\n'
                 '2.  **False Positives:** The most significant problem is the '
                 'presence of false positives. These are molecules that the '
                 'function classified as VL-CFA or UL-CFA, but actually '
                 "aren't. Many of these false positives come from complicated "
                 'molecules with multiple rings and sometimes even sugars or '
                 'other functional groups. The core issue seems to be that the '
                 'chain length detection algorithm is not sufficiently "smart" '
                 'about identifying *the* main fatty acid chain. It seems to '
                 'sometimes count carbons that are part of rings or branches '
                 'as part of the main chain, leading to inflated carbon counts '
                 'and incorrect classification. Some of the false positives '
                 'also include deprotonated acids, which the code can identify '
                 'as well.\n'
                 '\n'
                 '3.  **False Negatives:** There are a few false negatives, '
                 'all of which are molecules with a carbon chain length of 21 '
                 'or 22, which are being missed. The code is correctly '
                 'identifying the acid group but it incorrectly calculates the '
                 'carbon chain length. This is often due to branching and '
                 'double bond detection which is not being handled well by the '
                 'recursion. It looks like some of the double bonds are '
                 'causing the code to stop the recursion early.\n'
                 '\n'
                 '**Proposed Improvements:**\n'
                 '\n'
                 '1.  **More Robust Chain Detection:**\n'
                 '    *   **Avoid recursion:** Recursion can lead to problems '
                 'in complex molecules. An iterative approach might be more '
                 'robust.\n'
                 '    *   **Start from the carboxyl carbon:** We should start '
                 'our chain search from the carbon *adjacent* to the carbonyl '
                 'carbon, and then trace out the longest path without looping '
                 'back on itself.\n'
                 '    *   **Prioritize linear chains:** When there is '
                 'branching, prioritize following the most linear path that '
                 'leads away from the acid group.\n'
                 '    *   **Consider unsaturation:** Do not let double bonds '
                 'stop the carbon chain tracking.\n'
                 '2.  **Explicitly Handle Methyl groups:** Do not count methyl '
                 'groups as part of the main chain length.\n'
                 '3.  **Ignore Rings**: When the chain tracker meets a ring, '
                 'do not count the carbons in that ring as part of the main '
                 'chain length.\n'
                 '4. **Explicitly Handle -C(O)=O**: The carboxylic carbon has '
                 'to be included in the chain length.\n'
                 '5.  **Handle acid anions:**  The SMILES code can also be of '
                 'anionic carboxylic acids, such as "CC(=O)[O-]". The smarts '
                 'pattern should be able to capture both acids and anions.\n'
                 '\n'
                 "Let's implement these improvements in the code.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 145,
    'num_false_positives': 161,
    'num_true_negatives': 141938,
    'num_false_negatives': 56,
    'num_negatives': None,
    'precision': 0.4738562091503268,
    'recall': 0.7213930348258707,
    'f1': 0.571992110453649,
    'accuracy': 0.9984750527055517,
    'negative_predictive_value': 0.9996056171387523}