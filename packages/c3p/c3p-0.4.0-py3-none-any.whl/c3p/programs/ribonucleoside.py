"""
Classifies: CHEBI:18254 ribonucleoside
"""
"""
Classifies: any nucleoside where the sugar component is D-ribose (ribonucleoside)
Definition: A ribonucleoside has a nucleobase linked via a glycosidic bond to a D-ribofuranose unit.
This implementation first excludes compounds with phosphorus (to avoid nucleotides), then searches
for common ribose SMARTS patterns, making sure that at least one atom in the matched sugar is bonded
to an aromatic nitrogen (as a proxy for the nucleobase attachment). Finally, if SMARTS do not match,
a heuristic is used to find a five-membered ring (1 oxygen, 4 carbons) that is directly linked to an aromatic N.
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ribonucleoside(smiles: str):
    """
    Determines if a molecule is a ribonucleoside (i.e. a nucleoside with a D-ribose sugar)
    based on its SMILES string.

    Approaches:
      1. Reject molecules containing phosphorus (to avoid nucleotides and phosphorylated species).
      2. Attempt to match common SMARTS patterns of ribose providers and verify that at least one atom 
         in the matched substructure is directly bonded to an aromatic nitrogen (nucleobase signature).
      3. If SMARTS matching fails, search the molecule for any five-membered ring with 1 oxygen & 4 carbons,
         then check for a direct bond from one of the ring carbons to a nitrogen (with aromatic character).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classified as a ribonucleoside, False otherwise.
        str: Explanation/reason for the classification.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject if molecule contains phosphorus (P, atomic number 15), likely part of a nucleotide.
    if any(atom.GetAtomicNum() == 15 for atom in mol.GetAtoms()):
        return False, "Molecule contains phosphorus; likely a nucleotide rather than a nucleoside"
    
    # First approach: use common SMARTS for a ribose substructure.
    # Pattern 1: common unmodified ribofuranose unit.
    ribose_smarts1 = "[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O"
    pattern1 = Chem.MolFromSmarts(ribose_smarts1)
    if pattern1 is None:
        return False, "Error creating SMARTS pattern for ribose (pattern1)"
    # Pattern 2: variant (e.g., for 2'-O-methyl nucleosides).
    ribose_smarts2 = "CO[C@@H]1[C@H](O)[C@@H](CO)O[C@H]1"
    pattern2 = Chem.MolFromSmarts(ribose_smarts2)
    if pattern2 is None:
        return False, "Error creating SMARTS pattern for ribose (pattern2)"
    
    # Helper function to check if a substruct match is linked to an aromatic nitrogen (nucleobase).
    def sugar_attached_to_nucleobase(match):
        for idx in match:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                # Only consider neighbors not in the sugar match.
                if nbr.GetIdx() not in match and nbr.GetAtomicNum() == 7 and nbr.GetIsAromatic():
                    return True
        return False

    # Check pattern 1.
    matches1 = mol.GetSubstructMatches(pattern1)
    for match in matches1:
        if sugar_attached_to_nucleobase(match):
            return True, "Matched common D-ribose pattern (unmodified ribofuranose) attached to a nucleobase"
    # Check pattern 2.
    matches2 = mol.GetSubstructMatches(pattern2)
    for match in matches2:
        if sugar_attached_to_nucleobase(match):
            return True, "Matched common D-ribose pattern with 2'-O-methyl modification attached to a nucleobase"
    
    # Second approach: heuristic search for five-membered ribofuranose rings.
    # Use an explicit hydrogen-added molecule for better perception.
    mol_with_H = Chem.AddHs(mol)
    ring_info = mol_with_H.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) == 5:
            # Count the number of oxygen and carbon atoms.
            oxygen_idxs = []
            carbon_idxs = []
            for idx in ring:
                atom = mol_with_H.GetAtomWithIdx(idx)
                if atom.GetAtomicNum() == 8:
                    oxygen_idxs.append(idx)
                elif atom.GetAtomicNum() == 6:
                    carbon_idxs.append(idx)
            # Ribofuranose: exactly one oxygen, four carbons.
            if len(oxygen_idxs) == 1 and len(carbon_idxs) == 4:
                # For each carbon in the ring, check if it is bonded to an external aromatic nitrogen.
                for idx in carbon_idxs:
                    atom = mol_with_H.GetAtomWithIdx(idx)
                    for nbr in atom.GetNeighbors():
                        # Verify the neighboring atom is outside the ring.
                        if nbr.GetIdx() not in ring and nbr.GetAtomicNum() == 7 and nbr.GetIsAromatic():
                            return True, "Found five-membered ribofuranose ring attached to a nucleobase nitrogen"
    return False, "No ribose moiety attached to a nucleobase found"

# Example usage:
if __name__ == "__main__":
    # Test a few examples:
    examples = {
        "1-methyladenosine": "Cn1cnc2n(cnc2c1=N)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O",
        "3,4-dihydrozebularine": "OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=CCNC1=O",
        "nucleocidin": "NC1=C2N=CN([C@@H]3O[C@](F)(COS(N)(=O)=O)[C@@H](O)[C@H]3O)C2=NC=N1",
        "cytidine": "Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)n1",
        "5'-deoxyadenosine": "C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12",  # should be false as deoxy sugar
        "ATP (should be rejected)": "Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O"
    }
    for name, smi in examples.items():
        result, reason = is_ribonucleoside(smi)
        print(f"{name}: {result} ({reason})")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18254',
                          'name': 'ribonucleoside',
                          'definition': 'Any nucleoside where the sugar '
                                        'component is D-ribose.',
                          'parents': ['CHEBI:33838', 'CHEBI:47019'],
                          'xrefs': ['KEGG:C00911'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 89,
                           'log_lines_of_code': 4.48863636973214,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'GetAtoms',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetIsAromatic',
                                                 'AddHs',
                                                 'GetSubstructMatches',
                                                 'GetRingInfo',
                                                 'append',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'items'],
                           'methods_called_count': 14,
                           'smarts_strings': [   'ribose_smarts2',
                                                 'ribose_smarts1'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_ribonucleoside(smiles: str):',
                                       'sugar_attached_to_nucleobase(match):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains '
                                          'phosphorus; likely a nucleotide '
                                          'rather than a nucleoside"',
                                          'False, "Error creating SMARTS '
                                          'pattern for ribose (pattern1)"',
                                          'False, "Error creating SMARTS '
                                          'pattern for ribose (pattern2)"',
                                          'True',
                                          'False',
                                          'True, "Matched common D-ribose '
                                          'pattern (unmodified ribofuranose) '
                                          'attached to a nucleobase"',
                                          'True, "Matched common D-ribose '
                                          "pattern with 2'-O-methyl "
                                          'modification attached to a '
                                          'nucleobase"',
                                          'True, "Found five-membered '
                                          'ribofuranose ring attached to a '
                                          'nucleobase nitrogen"',
                                          'False, "No ribose moiety attached '
                                          'to a nucleobase found"'],
                           'returns_count': 10,
                           'complexity': 7.4977272739464285},
    'message': '\n'
               'Attempt failed: F1 score of 0.04719101123595506 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'Cn1cnc2n(cnc2c1=N)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O NAME: '
               '1-methyladenosine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=CCNC1=O NAME: '
               '3,4-dihydrozebularine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)n1 '
               'NAME: cytidine REASON: CORRECT Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               'COC(=O)Cc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=S)[nH]c1=O '
               'NAME: 5-methoxycarbonylmethyl-2-thiouridine REASON: CORRECT '
               'Matched common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'COc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)[nH]c1=O NAME: '
               '5-methoxyuridine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CNCc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)[nH]c1=O NAME: '
               '5-methylaminomethyluridine REASON: CORRECT Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CONCc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=S)[nH]c1=O NAME: '
               '5-methoxyaminomethyl-2-thiouridine REASON: CORRECT Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CC(=O)N[C@H]1[C@@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)O[C@H](CC(O)[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H]1O '
               'NAME: UDP-N-acetyltunicamine-uracil REASON: CORRECT Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CC(=O)C1(N)NC(=O)N(C=C1)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: 4-acetylcytidine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C\\C(CO)=C\\CNc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: 9-ribosyl-cis-zeatin REASON: CORRECT Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'N1=CN=C2C(=C1N)C(=CN2[C@H]3[C@H](O)[C@H](O)[C@H](O3)CO)C#N '
               'NAME: toyocamycin REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CO[C@@H]1[C@H](O)[C@@H](CO)O[C@H]1n1cnc2c1nc(N)[nH]c2=O NAME: '
               "2'-O-methylguanosine REASON: CORRECT Matched common D-ribose "
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: CO[C@@H]1[C@H](O)[C@@H](CO)O[C@H]1n1ccc(=O)[nH]c1=O '
               "NAME: 2'-O-methyluridine REASON: CORRECT Matched common "
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'COC(=O)COc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)[nH]c1=O '
               'NAME: methyl uridin-5-yloxyacetate REASON: CORRECT Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: adenosine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'Cn1c(N)nc2n(cnc2c1=O)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O NAME: '
               '1-methylguanosine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CNC=1NC(C=2[N+](=CN([C@H]3[C@H](O)[C@H](O)[C@@H](CO)O3)C2N1)C)=O '
               'NAME: N(2),N(7)-dimethylguanosine REASON: CORRECT Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CO[C@@H]1[C@H](O)[C@@H](CO)O[C@H]1n1cc(C)c(=O)[nH]c1=O NAME: '
               "2'-O-methyl-5-methyluridine REASON: CORRECT Matched common "
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: CNc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: N(6)-methyladenosine REASON: CORRECT Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: COc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: 6-O-methylinosine REASON: CORRECT Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C[C@@H](O)[C@@H]1N\\C(OC1=O)=N/c1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: cyclic N(6)-threonylcarbamoyladenosine REASON: CORRECT '
               'Matched common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C\\C(CO)=C/CNc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               'NAME: 9-ribosyl-trans-zeatin REASON: CORRECT Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'COC(=O)Cc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)[nH]c1=O '
               'NAME: 5-methoxycarbonylmethyluridine REASON: CORRECT Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CN1CN=c2n(cnc2=C1N)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O NAME: '
               '1-methyl-2-hydroadenosine REASON: CORRECT Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=S '
               'NAME: 2-thiouridine REASON: CORRECT Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               'False positives: SMILES: '
               'S(C(=O)C(CCCC(CCCC(C)C)C)C)CCNC(=O)CCNC(=O)C(O)C(COP(OP(OCC1OC(N2C3=NC=NC(N)=C3N=C2)C(O)C1OP(O)(O)=O)(O)=O)(O)=O)(C)C '
               'NAME: (2S,6R,10R)-Trimethyl-hendecanoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#36-CoA REASON: WRONGLY CLASSIFIED Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: CC1(O[C@@H]2[C@H]([C@H](OC2O1)C(CO)O)OCCCN(C)C)C '
               'NAME: '
               '1-[(5R,6S,6aR)-6-[3-(dimethylamino)propoxy]-2,2-dimethyl-3a,5,6,6a-tetrahydrofuro[2,3-d][1,3]dioxol-5-yl]ethane-1,2-diol '
               'REASON: WRONGLY CLASSIFIED Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               '[H][C@]1(O[C@](C[C@H](O)[C@@H]1NC(C)=O)(OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)C([O-])=O)[C@@H](NC(C)=O)[C@H](C)O '
               'NAME: CMP-pseudaminate REASON: WRONGLY CLASSIFIED Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C[C@](O)(CO)[C@H](O)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O '
               'NAME: 4-CDP-2-C-methyl-D-erythritol REASON: WRONGLY CLASSIFIED '
               'Matched common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(N)=NC=N3)N=C2)O[C@@H]([C@H]([C@H]1O)OP(=O)([O-])[O-])COP(O[C@@H]4[C@H](O[C@@H](N5C6=C(C(N)=NC=N6)N=C5)[C@@H]4O)COP(O[C@@H]7[C@H](O[C@@H](N8C9=C(C(=O)NC(=N9)N)N=C8)[C@@H]7O)CO)([O-])=O)(=O)[O-] '
               "NAME: G[3'-5']pA[3'-5']pAp[3'](4-) REASON: WRONGLY CLASSIFIED "
               'Matched common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#36-CoA(4-) REASON: WRONGLY CLASSIFIED Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'NCCCCCCNc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: N(6)-(6-aminohexyl)-cAMP REASON: WRONGLY CLASSIFIED '
               'Matched common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#34-CoA REASON: WRONGLY CLASSIFIED Matched common '
               'D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CSc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O '
               "NAME: 6-Methylthiopurine 5'-monophosphate ribonucleotide "
               'REASON: WRONGLY CLASSIFIED Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]1O '
               'NAME: ATP REASON: WRONGLY CLASSIFIED Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'Cc1cn([C@@H]2O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]2O)c(=O)nc1N '
               "NAME: 5-methylcytidine 5'-monophosphate REASON: WRONGLY "
               'CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bhas#22-CoA(4-) REASON: WRONGLY CLASSIFIED Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'C[C@H](NC(=O)[C@@H](C)O[C@H]1[C@H](O)[C@@H](CO)OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@@H]1NC(C)=O)C(=O)N[C@H](CCC(O)=O)C(=O)NCCCC[C@@H](N)C(O)=O '
               'NAME: '
               'N(6)-(UDP-N-acetylmuramoyl-L-alanyl-D-alpha-glutamyl)-D-lysine '
               'REASON: WRONGLY CLASSIFIED Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](C)[C@@H](CC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CC[C@H](C[C@]7(C[C@H]([C@]6([C@@]5(CC4)[H])[H])O)[H])O)C)[H])C)[H])(C)[H])O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: '
               '(24R,25R)-3alpha,7alpha,24-trihydroxy-5beta-cholestan-26-oyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]7O[C@@H]([C@H](O)[C@H]7O)CO)CO[C@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@@H](O)[C@@H]8O)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5S,6S)-6-[[(2R,3R,4S,5S,6S)-6-[(2R,3S,4R,5R,6S)-5-Acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-[(2R,3S,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3R,4R,5R)-3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]oxy-3-hydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               '[H][C@]1(Nc2c(N[C@H]1C)nc(N)[nH]c2=O)[C@@H](C)Nc1ccc(C[C@H](O)[C@H](O)[C@H](O)CO[C@H]2O[C@H](COP([O-])(=O)O[C@@H](CCC([O-])=O)C([O-])=O)[C@@H](O)[C@H]2O)cc1 '
               'NAME: 5,6,7,8-tetrahydromethanopterin(3-) REASON: WRONGLY '
               'CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O '
               "NAME: adenosine 3',5'-bismonophosphate REASON: WRONGLY "
               'CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (7Z,10Z,13Z,16Z,19Z)-docosapentaenoyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: P(OCC1OC(N2C(=O)NC(=O)C=C2)C(O)C1O)(O)(O)=O NAME: '
               '1-(5-O-Phosphonopentofuranosyl)-2,4(1H,3H)-pyrimidinedione '
               'REASON: WRONGLY CLASSIFIED Matched common D-ribose pattern '
               '(unmodified ribofuranose)\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(O)=O)O[C@H]([C@@H]1O)n1cnc2c1nc[nH]c2=O '
               'NAME: IMP REASON: WRONGLY CLASSIFIED Matched common D-ribose '
               'pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1OP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=O)C([O-])=O '
               'NAME: UDP-2-acetamido-2-deoxy-alpha-D-glucuronate(3-) REASON: '
               'WRONGLY CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: '
               'NCCOP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O '
               'NAME: CDP-ethanolamine REASON: WRONGLY CLASSIFIED Matched '
               'common D-ribose pattern (unmodified ribofuranose)\n'
               ' * SMILES: '
               'P(=O)([O-])(OC[C@H]([C@@H](O)[C@H](CN1C2=NC(=O)NC(C2(NC3=C1C=C(C)C(=C3)C)OO)=O)O)O)OP(=O)(OC[C@H]4O[C@@H](N5C6=C(C(=NC=N6)N)N=C5)[C@@H]([C@@H]4O)O)[O-] '
               'NAME: FADH2-C4alpha-hydroperoxide(2-) REASON: WRONGLY '
               'CLASSIFIED Matched common D-ribose pattern (unmodified '
               'ribofuranose)\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-undecenoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Matched common D-ribose pattern (unmodified ribofuranose)\n'
               'False negatives: SMILES: '
               'NC1=C2N=CN([C@@H]3O[C@](F)(COS(N)(=O)=O)[C@@H](O)[C@H]3O)C2=NC=N1 '
               'NAME: nucleocidin REASON: MISSED No D-ribose moiety '
               '(ribonucleoside sugar) found\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CCC(=O)c2cccc(c2)C(O)=O)[C@@H](O)[C@H]1O '
               'NAME: aminodeoxyfutalosine REASON: MISSED No D-ribose moiety '
               '(ribonucleoside sugar) found\n'
               ' * SMILES: '
               'C[C@H](CNC(=O)CC[C@]1(C)[C@@H](CC(N)=O)[C@H]2N3C1=C(C)C1=[N+]4C(=CC5=[N+]6C(=C(C)C7=[N+]([C@]2(C)[C@@](C)(CC(N)=O)[C@@H]7CCC(N)=O)[Co--]346C[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@](C)(CC(N)=O)[C@@H]5CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O)OP(O)(O)=O '
               'NAME: adenosylcobinamide phosphate REASON: MISSED No D-ribose '
               'moiety (ribonucleoside sugar) found\n'
               ' * SMILES: '
               'CN(C)c1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](N)[C@H]1O NAME: '
               "3'-amino-3'-deoxy-N(6),N(6)-dimethyladenosine REASON: MISSED "
               'No D-ribose moiety (ribonucleoside sugar) found\n'
               ' * SMILES: C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               "NAME: 5'-deoxyadenosine REASON: MISSED No D-ribose moiety "
               '(ribonucleoside sugar) found\n'
               ' * SMILES: '
               'C[Se+](CC[C@H](N)C(O)=O)C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               'NAME: L-adenosylselenomethionine REASON: MISSED No D-ribose '
               'moiety (ribonucleoside sugar) found\n'
               ' * SMILES: '
               'CNC(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(NCc3ccc(N)c(I)c3)ncnc12 '
               "NAME: 3-iodo-4-aminobenzyl-5'-N-methylcarboxamidoadenosine "
               'REASON: MISSED No D-ribose moiety (ribonucleoside sugar) '
               'found\n'
               ' * SMILES: '
               '[H]C(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 NAME: '
               "5'-dehydroadenosine REASON: MISSED No D-ribose moiety "
               '(ribonucleoside sugar) found\n'
               ' * SMILES: CCSC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 '
               "NAME: 5'-ethylthioadenosine REASON: MISSED No D-ribose moiety "
               '(ribonucleoside sugar) found\n'
               ' * SMILES: '
               'CCCCCOC(=O)Nc1nc(=O)n(cc1F)[C@@H]1O[C@H](C)[C@@H](O)[C@H]1O '
               'NAME: capecitabine REASON: MISSED No D-ribose moiety '
               '(ribonucleoside sugar) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No ribose moiety attached to a '
                                               'nucleobase found'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Molecule contains phosphorus; '
                                               'likely a nucleotide rather '
                                               'than a nucleoside'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=CCNC1=O',
                                      'name': '3,4-dihydrozebularine',
                                      'reason': 'No ribose moiety attached to '
                                                'a nucleobase found'},
                                  {   'smiles': 'C[C@H](CNC(=O)CC[C@]1(C)[C@@H](CC(N)=O)[C@H]2N3C1=C(C)C1=[N+]4C(=CC5=[N+]6C(=C(C)C7=[N+]([C@]2(C)[C@@](C)(CC(N)=O)[C@@H]7CCC(N)=O)[Co--]346C[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@](C)(CC(N)=O)[C@@H]5CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O)OP(O)(O)=O',
                                      'name': 'adenosylcobinamide phosphate',
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely a nucleotide rather '
                                                'than a nucleoside'},
                                  {   'smiles': 'CC(=O)N[C@H]1[C@@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)O[C@H](CC(O)[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@@H]1O',
                                      'name': 'UDP-N-acetyltunicamine-uracil',
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely a nucleotide rather '
                                                'than a nucleoside'},
                                  {   'smiles': 'CC(=O)C1(N)NC(=O)N(C=C1)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O',
                                      'name': '4-acetylcytidine',
                                      'reason': 'No ribose moiety attached to '
                                                'a nucleobase found'},
                                  {   'smiles': 'C[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)C(O)=O',
                                      'name': "L-lactyl-2-diphospho-5'-guanosine",
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely a nucleotide rather '
                                                'than a nucleoside'},
                                  {   'smiles': 'N[C@@H](CCCCNc1nc(=N)ccn1[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O)C(O)=O',
                                      'name': 'lysidine monophosphate',
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely a nucleotide rather '
                                                'than a nucleoside'},
                                  {   'smiles': 'OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1CCC(=O)NC1=O',
                                      'name': 'dihydrouridine',
                                      'reason': 'No ribose moiety attached to '
                                                'a nucleobase found'},
                                  {   'smiles': 'NC(CCN1C(=O)CCN([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)C1=O)C(O)=O',
                                      'name': '3-(3-amino-3-carboxypropyl)-5,6-dihydrouridine',
                                      'reason': 'No ribose moiety attached to '
                                                'a nucleobase found'},
                                  {   'smiles': 'CN(C)c1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(NCCCC[C@H](NC(C)=O)C(O)=O)N2CCOCC2)[C@@H](O)[C@H]1O',
                                      'name': 'alpha-N-acetyllysine-N(6),N(6)-dimethyladenosine '
                                              "5'-phosphomorpholidate",
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely a nucleotide rather '
                                                'than a nucleoside'},
                                  {   'smiles': '[H][C@@]12[C@H](CC(N)=O)[C@@](C)(CCC(=O)NC[C@@H](C)OP(O)(=O)OP(O)(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)n3cnc4c3nc(N)[nH]c4=O)C3=C(C)C4=[N+]5C(=CC6=[N+]7C(=C(C)C8=[N+]([C@]1(C)[C@@](C)(CC(N)=O)[C@@H]8CCC(N)=O)[Co--]57(C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc5c(N)ncnc15)N23)[C@@](C)(CC(N)=O)[C@@H]6CCC(N)=O)C(C)(C)[C@@H]4CCC(N)=O',
                                      'name': 'adenosylcobinamide guanosyl '
                                              'diphosphate',
                                      'reason': 'Molecule contains phosphorus; '
                                                'likely a nucleotide rather '
                                                'than a nucleoside'}],
    'attempt': 1,
    'reasoning': 'Below is our reasoning and the complete Python code in a '
                 'single code block.\n'
                 '\n'
                 'Reasoning:\n'
                 '──────────────────────────────\n'
                 'The previous attempt simply looked for ribose‐like SMARTS '
                 'fragments or any five‐membered ring with one oxygen and four '
                 'carbons. However, many molecules (such as CoA derivatives, '
                 'nucleotides, or other ribose‐containing fragments) can '
                 '“falsely” match the pattern even when they are not '
                 'nucleosides. Moreover, several ribonucleosides (even ones '
                 'with modifications) were missed because their sugar '
                 'substructure did not match the strict SMARTS strings. In '
                 'order to improve the classification we take the following '
                 'steps:\n'
                 '\n'
                 '1. First, we reject molecules that contain phosphorus, since '
                 'nucleotides or phosphorylated species (for example, ATP, '
                 'CMP, CoA‐derivatives) are not nucleosides.\n'
                 '2. We then try to match common ribose SMARTS patterns '
                 '(unmodified or 2′‑O‑methyl) but we add an extra check that '
                 'some atom in the matching substructure is directly connected '
                 'to an aromatic nitrogen (a minimal “nucleobase” signature). '
                 'This helps avoid cases where a free ribose or similar sugar '
                 'exists but the sugar is not part of a nucleoside.\n'
                 '3. If the common patterns fail, we use a heuristic: look for '
                 'any five‐membered ring with exactly one oxygen and four '
                 'carbons (a ribofuranose ring candidate). Then, for each such '
                 'candidate, we check whether one of its carbon atoms (which '
                 'may be the anomeric carbon) is bonded to a nitrogen atom '
                 '(with aromatic character) that is outside the ring. Such a '
                 'bond is the classic glycosidic linkage found in '
                 'ribonucleosides.\n'
                 '4. If none of these tests pass, we conclude that no correct '
                 'D‑ribose attached to a nucleobase was found.\n'
                 '\n'
                 'This approach (although still heuristic) helps bring down '
                 'false positives (by checking that the sugar is actually '
                 '“linked” to a nucleobase) while still catching many '
                 'ribonucleosides even if the common SMARTS are modified.\n'
                 '\n'
                 'Below is the complete code.\n'
                 '\n'
                 '──────────────────────────────',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 114,
    'num_false_positives': 580,
    'num_true_negatives': 141596,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.1642651296829971,
    'recall': 0.9193548387096774,
    'f1': 0.27872860635696817,
    'accuracy': 0.9958538299367533,
    'negative_predictive_value': 0.9999293815233817}