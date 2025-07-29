"""
Classifies: CHEBI:35366 fatty acid
"""
"""
Classifies: fatty acid
Definition: “Any acyclic aliphatic carboxylic acid. 
Natural fatty acids commonly have a chain of 4 to 28 carbons (usually unbranched), which may be saturated or unsaturated.”
The classifier now rejects molecules that are cyclic or that contain any nitrogen atoms (e.g. peptides).
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_fatty_acid(smiles: str):
    """
    Determines if a molecule is a fatty acid based on its SMILES string.
    For this classifier, a fatty acid must be:
      - A valid molecule,
      - Acyclic (no rings) and free of nitrogen atoms (to avoid peptides or amino-acid derivatives),
      - Have a free (undissociated) carboxylic acid group (–C(=O)OH),
      - Connected to a contiguous aliphatic chain (starting at the carbonyl carbon) of at least 4 carbons.
    
    Args:
        smiles (str): SMILES string for the molecule.
    
    Returns:
        bool: True if the molecule is classified as a fatty acid, False otherwise.
        str: An explanation for the classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Rule 1: Fatty acids are acyclic.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings and is not acyclic aliphatic"
        
    # Extra check: Do not allow nitrogen atoms (which usually indicate peptides or amino acid derivatives).
    if any(atom.GetAtomicNum() == 7 for atom in mol.GetAtoms()):
        return False, "Molecule contains nitrogen atoms indicating peptide or amino acid derivatives"
    
    # Rule 2: The molecule must contain a free carboxylic acid group.
    # SMARTS here covers a free (undissociated) carboxyl: carbonyl carbon (CX3) bonded to an –OH (OX2H).
    free_acid_smarts = "[CX3](=O)[OX2H]"
    free_acid = Chem.MolFromSmarts(free_acid_smarts)
    acid_matches = mol.GetSubstructMatches(free_acid)
    if not acid_matches:
        return False, "No free carboxyl (–C(=O)OH) group detected"
    
    # Helper function: From a given starting carbon atom, compute the length of the longest contiguous carbon chain.
    def longest_carbon_chain(atom, visited):
        max_length = 1  # counting the starting atom
        for nbr in atom.GetNeighbors():
            # Only follow carbon atoms that haven’t been visited
            if nbr.GetAtomicNum() == 6 and nbr.GetIdx() not in visited:
                new_visited = visited | {nbr.GetIdx()}
                chain_length = 1 + longest_carbon_chain(nbr, new_visited)
                if chain_length > max_length:
                    max_length = chain_length
        return max_length

    # Rule 3: For each acid candidate, compute the contiguous chain length from the carbonyl carbon.
    # With our SMARTS the first atom in the match is the carbonyl carbon.
    for match in acid_matches:
        carbon_idx = match[0]
        carbon_atom = mol.GetAtomWithIdx(carbon_idx)
        chain_length = longest_carbon_chain(carbon_atom, {carbon_idx})
        if chain_length >= 4:
            reason = (f"Found free acid group (–C(=O)OH) with a contiguous aliphatic chain of "
                      f"{chain_length} carbons starting at the carbonyl carbon.")
            return True, reason

    return False, "No candidate free acid group is attached to a long enough (>=4 carbons) aliphatic chain"

# Example tests:
if __name__ == '__main__':
    test_set = [
        # True positives (fatty acids)
        ("OC(=O)CCCCCCCCCCC=C", "12-tridecenoic acid"),
        ("C(C(O)=O)C/C=C\\C[C@H](\\C=C\\C=C/C=C/C=C/[C@H]([C@@H](C/C=C\\CC)O)O)O", "aspirin-triggered resolvin D2"),
        ("O=C(O)[C@H]([C@@H](C(=O)O)C)CCCCCCCC", "Sphaeric acid"),
        ("O[C@H](CCC)C/C=C\\C/C=C\\CCCCCCCC(O)=O", "Avenoleic acid"),
        ("OC(=O)C=CC=CC=CCCCCCCCCCCCCCCCCC", "Tetracosatrienoic acid"),
        ("CC(C)C[C@@H](O)C(O)=O", "(R)-2-hydroxy-4-methylpentanoic acid"),
        ("CCCCCC\\C=C/CCCCCC(O)=O", "cis-tetradec-7-enoic acid"),
        ("OC(=O)CCCCCCCCCCC/C=C/CC", "13-hexadecenoic acid"),
        ("C(O)(=O)CCCCCCCCC(CCCCCCCCC)=O", "10-oxo-nonadecanoic acid"),
        ("OC(=O)CCCN(N=O)CCC", "4-[nitroso(propyl)amino]butanoic acid"),
        ("CCCCCCCCCC(O)CCC(O)=O", "4-hydroxylauric acid"),
        ("OC(=O)CCC(CCCC)CC", "4-Ethyloctanoic acid"),
        ("O=C(CCCCCCCC(O)=O)/C=C/C=C\\C/C=C\\CC", "9-OxoOTrE"),
        ("OC(=O)CCC#C/C=C\\C=C\\CCCCCCCCCC#CCCC", "6Z,8E-tricosdien-4,19-diynoic acid"),
        ("CCC=CCC=CCC=CCC=CCCC(=O)O", "4,7,10,13-hexadecatetraenoic acid"),
        ("OC(=O)CCCCCCC/C=C\\CCCCCCCCCC/C=C\\CCCCCC", "28:2(9Z,21Z)"),
        ("C(/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)=C\\[C@H]([C@H](CCCC(O)=O)O)O", "(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoic acid"),
        ("C(C(O)=O)C/C=C\\C/C=C\\C/C=C\\C\\C=C/C=C/C(C/C=C\\CC)=O", "(4Z,7Z,10Z,13Z,15E,19Z)-17-oxodocosahexaenoic acid"),
        ("OC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", "Hentriacontanoic acid"),
        ("OC(=O)[C@H](C[C@H](CCCCCCCCCCCCCCCCCC)C)C", "Mycosanoic acid (C24)"),
        ("OC(CCCCCC(O)=O)C#CCCCCCCCC", "7-hydroxy-10-heptadecen-8-ynoic acid"),
        ("CCCCCC[C@@H](O)\\C=C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O", "15(R)-HETE"),
        ("[H]\\C(C)=C\\C(O)=O", "isocrotonic acid"),
        # False positives (should be rejected)
        ("OC1C(C(C(=O)C1)C/C=C\\C/C=C\\CC)/C=C/C(O)C/C=C\\CCC(O)=O", "7-hydroxy-D4-neuroprostane"),
        ("CC\\C(CC[C@H]1O[C@@]1(C)CC)=C/CC\\C(C)=C\\C(O)=O", "juvenile hormone I acid"),
        ("O=C(O)/C=C/C=C/C=C/C=C/[C@@]1([C@@H](C(=C[C@H]2[C@H]1CC[C@@H]([C@@H]2O)C)CO)/C(=C/C)/C)C", "Janthinopolyenemycin B"),
        ("O1C(C1)(C(OC(=O)C(O)C(CC)C)/C=C/C=C/C=C/C(O)=O)C", "AF Toxin II"),
        ("Cl.OC(=O)CCCN1CCC(=CC1)C2=CC=CC=C2", "4-[4-phenyl-3,6-dihydro-1(2H)-pyridinyl]butanoic acid hydrochloride"),
        ("CCCCCC/C=C\\C/C=C\\CCCCCCCCCCCCC(O)=O", "Prenateic acid"),
    ]
    
    for smi, name in test_set:
        result, explanation = is_fatty_acid(smi)
        print(f"SMILES: {smi}\nName: {name}\nResult: {result}\nExplanation: {explanation}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35366',
                          'name': 'fatty acid',
                          'definition': 'Any aliphatic monocarboxylic acid '
                                        'derived from or contained in '
                                        'esterified form in an animal or '
                                        'vegetable fat, oil or wax. Natural '
                                        'fatty acids commonly have a chain of '
                                        '4 to 28 carbons (usually unbranched '
                                        'and even-numbered), which may be '
                                        'saturated or unsaturated. By '
                                        'extension, the term is sometimes used '
                                        'to embrace all acyclic aliphatic '
                                        'carboxylic acids.',
                          'parents': ['CHEBI:18059', 'CHEBI:25384'],
                          'xrefs': [   'KEGG:C00162',
                                       'PMID:14287444',
                                       'PMID:14300208',
                                       'PMID:14328676',
                                       'Wikipedia:Fatty_acid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 87,
                           'log_lines_of_code': 4.465908118654584,
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
                                                 1,
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
                                                 2,
                                                 2,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
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
                                                 3,
                                                 3,
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetIdx',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'OC',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 11,
                           'smarts_strings': ['free_acid_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_fatty_acid(smiles: str):',
                                       'longest_carbon_chain(atom, visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains rings and '
                                          'is not acyclic aliphatic"',
                                          'False, "Molecule contains nitrogen '
                                          'atoms indicating peptide or amino '
                                          'acid derivatives"',
                                          'False, "No free carboxyl (–C(=O)OH) '
                                          'group detected"',
                                          'max_length',
                                          'True, reason',
                                          'False, "No candidate free acid '
                                          'group is attached to a long enough '
                                          '(>=4 carbons) aliphatic chain"'],
                           'returns_count': 7,
                           'complexity': 5.893181623730916},
    'message': '\n'
               'Attempt failed: F1 score of 0.45722561290989966 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: OC(=O)CCCCCCCCCCC=C NAME: '
               '12-tridecenoic acid REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 13 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C[C@H](\\C=C\\C=C/C=C/C=C/[C@H]([C@@H](C/C=C\\CC)O)O)O '
               'NAME: aspirin-triggered resolvin D2 REASON: CORRECT Found free '
               'acid group (–C(=O)OH) with a contiguous aliphatic chain of 22 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: O=C(O)[C@H]([C@@H](C(=O)O)C)CCCCCCCC NAME: Sphaeric '
               'acid REASON: CORRECT Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 10 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: O[C@H](CCC)C/C=C\\C/C=C\\CCCCCCCC(O)=O NAME: '
               'Avenoleic acid REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 18 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: OC(=O)C=CC=CC=CCCCCCCCCCCCCCCCCC NAME: '
               'Tetracosatrienoic acid REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 24 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: C(CCCCCCC[C@H]([C@H](CCCCCCCC)O)O)(=O)O NAME: '
               '(9R,10S)-dihydroxyoctadecanoic acid REASON: CORRECT Found free '
               'acid group (–C(=O)OH) with a contiguous aliphatic chain of 18 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CC(C)C[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxy-4-methylpentanoic acid REASON: CORRECT Found '
               'free acid group (–C(=O)OH) with a contiguous aliphatic chain '
               'of 5 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CCCCCC\\C=C/CCCCCC(O)=O NAME: cis-tetradec-7-enoic '
               'acid REASON: CORRECT Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 14 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: OC(=O)CCCCCCCCCCC/C=C/CC NAME: 13-hexadecenoic acid '
               'REASON: CORRECT Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 16 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: C(O)(=O)CCCCCCCCC(CCCCCCCCC)=O NAME: '
               '10-oxo-nonadecanoic acid REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 19 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: OC(=O)CCCN(N=O)CCC NAME: '
               '4-[nitroso(propyl)amino]butanoic acid REASON: CORRECT Found '
               'free acid group (–C(=O)OH) with a contiguous aliphatic chain '
               'of 4 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CCCCCCCCC(O)CCC(O)=O NAME: 4-hydroxylauric acid '
               'REASON: CORRECT Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 12 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: OC(=O)CCC(CCCC)CC NAME: 4-Ethyloctanoic acid '
               'REASON: CORRECT Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 8 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: O=C(CCCCCCCC(O)=O)/C=C/C=C\\C/C=C\\CC NAME: '
               '9-OxoOTrE REASON: CORRECT Found free acid group (–C(=O)OH) '
               'with a contiguous aliphatic chain of 18 carbons starting at '
               'the carbonyl carbon.\n'
               ' * SMILES: OC(=O)CCC#C/C=C\\C=C\\CCCCCCCCCC#CCCC NAME: '
               '6Z,8E-tricosdien-4,19-diynoic acid REASON: CORRECT Found free '
               'acid group (–C(=O)OH) with a contiguous aliphatic chain of 23 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CCC=CCC=CCC=CCC=CCCC(=O)O NAME: '
               '4,7,10,13-hexadecatetraenoic acid REASON: CORRECT Found free '
               'acid group (–C(=O)OH) with a contiguous aliphatic chain of 16 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: OC(=O)CCCCCCC/C=C\\CCCCCCCCCC/C=C\\CCCCCC NAME: '
               '28:2(9Z,21Z) REASON: CORRECT Found free acid group (–C(=O)OH) '
               'with a contiguous aliphatic chain of 28 carbons starting at '
               'the carbonyl carbon.\n'
               ' * SMILES: '
               'C(/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)=C\\[C@H]([C@H](CCCC(O)=O)O)O '
               'NAME: '
               '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoic '
               'acid REASON: CORRECT Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 20 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C/C=C\\C/C=C\\C\\C=C/C=C/C(C/C=C\\CC)=O NAME: '
               '(4Z,7Z,10Z,13Z,15E,19Z)-17-oxodocosahexaenoic acid REASON: '
               'CORRECT Found free acid group (–C(=O)OH) with a contiguous '
               'aliphatic chain of 22 carbons starting at the carbonyl '
               'carbon.\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC NAME: '
               'Hentriacontanoic acid REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 31 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: OC(=O)[C@H](C[C@H](CCCCCCCCCCCCCCCCCC)C)C NAME: '
               'Mycosanoic acid (C24) REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 22 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: OC(CCCCCC(O)=O)C#CCCCCCCCC NAME: '
               '7-hydroxy-10-heptadecen-8-ynoic acid REASON: CORRECT Found '
               'free acid group (–C(=O)OH) with a contiguous aliphatic chain '
               'of 17 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CCCCC[C@@H](O)\\C=C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 15(R)-HETE REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 20 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC(O)=O)C NAME: Sebacic acid '
               'monomethyl ester REASON: CORRECT Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 10 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: [H]\\C(C)=C\\C(O)=O NAME: isocrotonic acid REASON: '
               'CORRECT Found free acid group (–C(=O)OH) with a contiguous '
               'aliphatic chain of 4 carbons starting at the carbonyl carbon.\n'
               'False positives: SMILES: '
               'O=C(N[C@H](C(=O)N[C@@H](CC(O)=O)C(O)=O)CO)[C@@H](N)[C@H](CC)C '
               'NAME: Ile-Ser-Asp REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N[C@@H](C(C)C)C(O)=O)CO)[C@@H](N)CCCCN NAME: '
               'Lys-Ser-Val REASON: WRONGLY CLASSIFIED Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 4 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CCC(O)=O)C(O)=O)C '
               'NAME: Thr-Glu-Thr REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 5 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)C(C)C)CCCN=C(N)N '
               'NAME: Val-Arg-Leu REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 5 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: OC(CCC(C)C)CC(O)=O NAME: 3-hydroxy-isoheptanoic '
               'acid REASON: WRONGLY CLASSIFIED Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 7 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O(C(C[N+](C)(C)C)CC(O)=O)C(=O)CCCCCCCC/C=C/C=C/CCCCC NAME: '
               'ACar 18:2 REASON: WRONGLY CLASSIFIED Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 4 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCCN=C(N)N)C(=O)N[C@@H](CC(O)=O)C(O)=O '
               'NAME: Arg-Cys-Asp REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CCC(O)=O '
               'NAME: Ser-Glu-Asn REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: OC(=O)\\C=C\\C(O)=C\\C=O NAME: '
               '(2E,4Z)-4-hydroxy-6-oxohexa-2,4-dienoic acid REASON: WRONGLY '
               'CLASSIFIED Found free acid group (–C(=O)OH) with a contiguous '
               'aliphatic chain of 6 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O[C@@H]([C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC(C)C)C(O)=O)C)C '
               'NAME: Thr-Ala-Leu REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 5 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCSC)CCCN=C(N)N)C(O)=O)C '
               'NAME: Met-Arg-Met REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'C[C@@H](O)C(=O)SC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O '
               'NAME: (R)-S-lactoylglutathione REASON: WRONGLY CLASSIFIED '
               'Found free acid group (–C(=O)OH) with a contiguous aliphatic '
               'chain of 5 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CN)CO)C(C)C NAME: '
               'Gly-Ser-Val REASON: WRONGLY CLASSIFIED Found free acid group '
               '(–C(=O)OH) with a contiguous aliphatic chain of 4 carbons '
               'starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O=NN(O)CCC[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)CNC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](O)C(=O)O)CO)[C@H](O)C)CCCN(O)N=O)CO)C(=O)O '
               'NAME: Megapolibactin F REASON: WRONGLY CLASSIFIED Found free '
               'acid group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: O=C(NC(CCC(=O)N)C(O)=O)CCCCCCC/C=C/C\\C=C\\CCCCC '
               'NAME: N-Linoleoyl Glutamine REASON: WRONGLY CLASSIFIED Found '
               'free acid group (–C(=O)OH) with a contiguous aliphatic chain '
               'of 5 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H]([C@H](O)C)C(O)=O '
               'NAME: Glu-Cys-Thr REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 5 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CCCC(N)C(O)=O NAME: 2-aminopentanoic acid REASON: '
               'WRONGLY CLASSIFIED Found free acid group (–C(=O)OH) with a '
               'contiguous aliphatic chain of 5 carbons starting at the '
               'carbonyl carbon.\n'
               ' * SMILES: O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)CN)CCC(O)=O '
               'NAME: Gly-Glu-Val REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: OC(CC(N)C(O)=O)C(O)=O NAME: '
               '(4R)-4-Hydroxy-L-glutamic acid REASON: WRONGLY CLASSIFIED '
               'Found free acid group (–C(=O)OH) with a contiguous aliphatic '
               'chain of 5 carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O=C(O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCCC(CC)C)CCC(=O)O)CC(C)C)CC(C)C)C(C)C)CC(=O)O)CC(C)C)CC(C)C '
               'NAME: Gageostatin A REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 5 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)C(C)C)CCCN=C(N)N '
               'NAME: Val-Arg-Lys REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 6 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N)C(O)=O)C '
               'NAME: Asp-Gln-Met REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 4 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: CCCCCC/C=C\\C/C=C\\CCCCCCCCCCCCC(O)=O NAME: '
               'Prenateic acid REASON: WRONGLY CLASSIFIED Found free acid '
               'group (–C(=O)OH) with a contiguous aliphatic chain of 24 '
               'carbons starting at the carbonyl carbon.\n'
               ' * SMILES: OC(CCCCCCCCCC/C=C\\CCC)=O NAME: Criegeenic acid '
               'REASON: WRONGLY CLASSIFIED Found free acid group (–C(=O)OH) '
               'with a contiguous aliphatic chain of 16 carbons starting at '
               'the carbonyl carbon.\n'
               ' * SMILES: '
               'CC(=O)NC(CS[C@H](\\C=C\\C=C\\C=C/C\\C=C/CCCCC(O)=O)[C@@H](O)CCCC(O)=O)C(O)=O '
               'NAME: omega-Carboxy-N-acetyl-LTE4 REASON: WRONGLY CLASSIFIED '
               'Found free acid group (–C(=O)OH) with a contiguous aliphatic '
               'chain of 20 carbons starting at the carbonyl carbon.\n'
               'False negatives: SMILES: '
               'OC1C(C(C(=O)C1)C/C=C\\C/C=C\\CC)/C=C/C(O)C/C=C\\CCC(O)=O NAME: '
               '7-hydroxy-D4-neuroprostane REASON: MISSED Molecule contains '
               'rings and is not acyclic aliphatic\n'
               ' * SMILES: CC\\C(CC[C@H]1O[C@@]1(C)CC)=C/CC\\C(C)=C\\C(O)=O '
               'NAME: juvenile hormone I acid REASON: MISSED Molecule contains '
               'rings and is not acyclic aliphatic\n'
               ' * SMILES: '
               'O=C(O)/C=C/C=C/C=C/C=C/[C@@]1([C@@H](C(=C[C@H]2[C@H]1CC[C@@H]([C@@H]2O)C)CO)/C(=C/C)/C)C '
               'NAME: Janthinopolyenemycin B REASON: MISSED Molecule contains '
               'rings and is not acyclic aliphatic\n'
               ' * SMILES: O1C(C1)(C(OC(=O)C(O)C(CC)C)/C=C/C=C/C=C/C(O)=O)C '
               'NAME: AF Toxin II REASON: MISSED Molecule contains rings and '
               'is not acyclic aliphatic\n'
               ' * SMILES: Cl.OC(=O)CCCN1CCC(=CC1)C2=CC=CC=C2 NAME: '
               '4-[4-phenyl-3,6-dihydro-1(2H)-pyridinyl]butanoic acid '
               'hydrochloride REASON: MISSED Molecule contains rings and is '
               'not acyclic aliphatic\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/CC1OC1CCCC(O)=O NAME: '
               '5,6-EET REASON: MISSED Molecule contains rings and is not '
               'acyclic aliphatic\n'
               ' * SMILES: O1C(CCCCC)=C(C(=C1\\C=C\\CCCCCCCCC(O)=O)C)C NAME: '
               '12,15-Epoxy-13,14-dimethyleicosa-10,12,14-trienoic acid '
               'REASON: MISSED Molecule contains rings and is not acyclic '
               'aliphatic\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C/C=C\\C/C=C\\CC1C(C/C=C\\C/C=C\\CC)O1 NAME: '
               '(4Z,7Z,10Z,16Z,19Z)-13,14-epoxydocosapentaenoic acid REASON: '
               'MISSED Molecule contains rings and is not acyclic aliphatic\n'
               ' * SMILES: O=C1OC(\\C(=C/C(=C/C(=O)O)/C)\\C)=CC(=C1C)OC NAME: '
               '4Z-Infectopyrone REASON: MISSED Molecule contains rings and is '
               'not acyclic aliphatic\n'
               ' * SMILES: OC(=O)CCCC[C@H]1CCSS1 NAME: (S)-lipoic acid REASON: '
               'MISSED Molecule contains rings and is not acyclic aliphatic\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Molecule contains rings and is '
                                               'not acyclic aliphatic'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No free carboxyl (–C(=O)OH) '
                                               'group detected'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Molecule contains rings and is '
                                               'not acyclic aliphatic'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No free carboxyl (–C(=O)OH) '
                                               'group detected'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Molecule contains rings and is '
                                               'not acyclic aliphatic'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule contains rings and is '
                                               'not acyclic aliphatic'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Molecule contains rings and is '
                                               'not acyclic aliphatic'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecule contains rings and is '
                                               'not acyclic aliphatic'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No free carboxyl (–C(=O)OH) '
                                               'group detected'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No free carboxyl (–C(=O)OH) '
                                               'group detected'}],
    'sample_false_negatives': [   {   'smiles': 'OC1C(C(C(=O)C1)C/C=C\\C/C=C\\CC)/C=C/C(O)C/C=C\\CCC(O)=O',
                                      'name': '7-hydroxy-D4-neuroprostane',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'CC\\C(CC[C@H]1O[C@@]1(C)CC)=C/CC\\C(C)=C\\C(O)=O',
                                      'name': 'juvenile hormone I acid',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'O=C(O)/C=C/C=C/C=C/C=C/[C@@]1([C@@H](C(=C[C@H]2[C@H]1CC[C@@H]([C@@H]2O)C)CO)/C(=C/C)/C)C',
                                      'name': 'Janthinopolyenemycin B',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'O1C(C1)(C(OC(=O)C(O)C(CC)C)/C=C/C=C/C=C/C(O)=O)C',
                                      'name': 'AF Toxin II',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'Cl.OC(=O)CCCN1CCC(=CC1)C2=CC=CC=C2',
                                      'name': '4-[4-phenyl-3,6-dihydro-1(2H)-pyridinyl]butanoic '
                                              'acid hydrochloride',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'OC(=O)CCCN(N=O)CCC',
                                      'name': '4-[nitroso(propyl)amino]butanoic '
                                              'acid',
                                      'reason': 'Molecule contains nitrogen '
                                                'atoms indicating peptide or '
                                                'amino acid derivatives'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/CC1OC1CCCC(O)=O',
                                      'name': '5,6-EET',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'O1C(CCCCC)=C(C(=C1\\C=C\\CCCCCCCCC(O)=O)C)C',
                                      'name': '12,15-Epoxy-13,14-dimethyleicosa-10,12,14-trienoic '
                                              'acid',
                                      'reason': 'Molecule contains rings and '
                                                'is not acyclic aliphatic'},
                                  {   'smiles': 'OC(=O)CCCCCCCCCCCCC.OCCN(CCO)CCO',
                                      'name': 'Triethanolamine myristate',
                                      'reason': 'Molecule contains nitrogen '
                                                'atoms indicating peptide or '
                                                'amino acid derivatives'},
                                  {   'smiles': 'N[C@H](C(=O)O)CS[C@H](/C=C/C=C/C=C\\C/C=C\\CCC(O)=O)[C@H](C/C=C\\C/C=C\\CC)O',
                                      'name': '(13R)-S-cysteinyl-(14S)-hydroxy-(4Z,7Z,9E,11E,16Z,19Z)-docosahexaenoic '
                                              'acid',
                                      'reason': 'Molecule contains nitrogen '
                                                'atoms indicating peptide or '
                                                'amino acid derivatives'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'We examined the previous fatty‐acid classifier and observed '
                 'that while it correctly identified many fatty acids (true '
                 'positives), it also marked many peptides (or amino‐acid '
                 'derivatives) as fatty acids. In many false‐positive cases '
                 'the routine found a free carboxylic acid group (–C(=O)OH) '
                 'and then computed a contiguous carbon chain of at least four '
                 'carbons—even though that chain belonged to a peptide '
                 'C‐terminus rather than an aliphatic fatty acid. In order to '
                 'improve the precision we now add extra rules. First, since '
                 '“acyclic aliphatic” fatty acids should not contain rings or '
                 'heteroatoms (especially nitrogen), we now explicitly reject '
                 '(or “flag”) molecules that contain rings or any nitrogen '
                 'atoms. (Peptides will have one or more amide bonds and '
                 'nitrogen atoms.) This extra nitrogen filter combined with '
                 'the existing requirements (validity, acyclic, free carboxyl '
                 'group, and enough contiguous carbon atoms from the carbonyl '
                 'carbon) should reduce the false positives and improve '
                 'performance.\n'
                 '\n'
                 'Below is the complete single-code-block Python solution '
                 'using RDKit:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2119,
    'num_false_positives': 921,
    'num_true_negatives': 138543,
    'num_false_negatives': 717,
    'num_negatives': None,
    'precision': 0.6970394736842105,
    'recall': 0.747179125528914,
    'f1': 0.7212389380530974,
    'accuracy': 0.9884891075193254,
    'negative_predictive_value': 0.994851357173632}