"""
Classifies: CHEBI:17792 organohalogen compound
"""
"""
Classifies: Organohalogen compound
Definition: A compound containing at least one carbon-halogen bond (halogen = F, Cl, Br, I).
Improved approach: Select the main organic fragment as the one with the highest number of carbon atoms.
"""

from rdkit import Chem

def is_organohalogen_compound(smiles: str):
    """
    Determines if a molecule (main organic fragment) is an organohalogen compound based on its SMILES string.
    The function first filters out fragments lacking carbon atoms, then selects the fragment with the highest carbon count.
    Finally, it iterates over all bonds in that fragment to check for a bond between a carbon atom and a halogen atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the main organic fragment contains at least one carbon-halogen bond, False otherwise.
        str: Explanation for the classification.
    """
    # Try to parse the SMILES string using RDKit.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get all disconnected fragments as separate molecules.
    fragments = Chem.GetMolFrags(mol, asMols=True)
    
    # Filter fragments to include only those with at least one carbon atom.
    organic_frags = []
    for frag in fragments:
        if any(atom.GetAtomicNum() == 6 for atom in frag.GetAtoms()):
            organic_frags.append(frag)
    if not organic_frags:
        return False, "No organic fragment (with carbon atoms) found"
    
    # Select the fragment with the highest count of carbon atoms.
    def carbon_count(m):
        return sum(1 for atom in m.GetAtoms() if atom.GetAtomicNum() == 6)
    main_mol = max(organic_frags, key=carbon_count)
    
    # Define the halogen atomic numbers: F (9), Cl (17), Br (35), I (53)
    halogen_atomic_nums = {9, 17, 35, 53}
    
    # Iterate over all bonds in the main fragment.
    for bond in main_mol.GetBonds():
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()
        if (atom1.GetAtomicNum() == 6 and atom2.GetAtomicNum() in halogen_atomic_nums) or \
           (atom2.GetAtomicNum() == 6 and atom1.GetAtomicNum() in halogen_atomic_nums):
            return True, "Molecule contains a carbon-halogen bond on its main organic fragment"
    
    return False, "No carbon-halogen bond found in the main organic fragment"

# Example usage for testing (can be commented out in production):
if __name__ == "__main__":
    test_smiles = [
        "COc1ccc(cc1)C(=O)C(Br)CS(=O)(=O)c1ccc(C)cc1",    # 2-bromo-1-(4-methoxyphenyl)-3-[(4-methylphenyl)sulfonyl]-1-propanone
        "Oc1c(Cl)cc(Cl)cc1-c1ccccc1",                       # 2-Hydroxy-3,5-dichlorobiphenyl
        "C(O)(C(=O)CBr)=O",                                # 3-bromopyruvic acid
        "C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F",  # a false positive challenge case
        "Brn1ccc2ccccc12",                                # 1-bromoindole; challenge case
    ]
    
    for smi in test_smiles:
        result, reason = is_organohalogen_compound(smi)
        print(f"SMILES: {smi}\nResult: {result}, Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17792',
                          'name': 'organohalogen compound',
                          'definition': 'A compound containing at least one '
                                        'carbon-halogen bond (where X is a '
                                        'halogen atom).',
                          'parents': ['CHEBI:33285', 'CHEBI:37578'],
                          'xrefs': [   'KEGG:C01322',
                                       'MetaCyc:Organohalogen-Compounds'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 47,
                           'log_lines_of_code': 3.8501476017100584,
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
                                                 3,
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
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
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
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'append',
                                                 'GetMolFrags',
                                                 'GetEndAtom',
                                                 'GetBeginAtom',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'GetBonds'],
                           'methods_called_count': 8,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_organohalogen_compound(smiles: '
                                       'str):',
                                       'carbon_count(m):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No organic fragment (with '
                                          'carbon atoms) found"',
                                          'sum(1 for atom in m.GetAtoms() if '
                                          'atom.GetAtomicNum() == 6)',
                                          'True, "Molecule contains a '
                                          'carbon-halogen bond on its main '
                                          'organic fragment"',
                                          'False, "No carbon-halogen bond '
                                          'found in the main organic '
                                          'fragment"'],
                           'returns_count': 5,
                           'complexity': 4.370029520342012},
    'message': '\n'
               'Attempt failed: F1 score of 0.35446455354464557 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'COc1ccc(cc1)C(=O)C(Br)CS(=O)(=O)c1ccc(C)cc1 NAME: '
               '2-bromo-1-(4-methoxyphenyl)-3-[(4-methylphenyl)sulfonyl]-1-propanone '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: '
               'C=1(C=C(N(N1)CC(=O)N2CCC(CC2)C3=NC(=CS3)C=4C[C@@](ON4)(C=5C(=CC=CC5Cl)OS(C)(=O)=O)[H])C(F)F)C(F)F '
               'NAME: (R)-fluoxapiprolin REASON: CORRECT Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: Oc1c(Cl)cc(Cl)cc1-c1ccccc1 NAME: '
               '2-Hydroxy-3,5-dichlorobiphenyl REASON: CORRECT Molecule '
               'contains a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: C(O)(C(=O)CBr)=O NAME: 3-bromopyruvic acid REASON: '
               'CORRECT Molecule contains a carbon-halogen bond on its main '
               'organic fragment\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C#CC3=CC=C(C=C3)F)O[C@@H]1CN(C)C(=O)C)[C@@H](C)CO '
               'NAME: '
               'N-[[(2S,3R)-8-[2-(4-fluorophenyl)ethynyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylacetamide '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: '
               'CC[C@H](C)\\C=C\\C1=CC2=C(Cl)C(=O)[C@@]3(C)OC(=O)C(C(=O)[C@H](C)[C@@H](C)O)=C3C2=CO1 '
               "NAME: 4'-epichaetoviridin A REASON: CORRECT Molecule contains "
               'a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: C1(=CNC2=C1C=C(C=C2)Br)Br NAME: 3,5-dibromoindole '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: C1=CC(=CC(=C1)Cl)C=NC=NC2=CC(=CC=C2)Cl NAME: '
               "N'-(3-chlorophenyl)-N-[(3-chlorophenyl)methylidene]methanimidamide "
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: [H]C(C([O-])=O)=C(Cl)C([H])=C(Cl)C([O-])=O NAME: '
               '2,4-dichloromuconate(2-) REASON: CORRECT Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: ClC1=NC=CC(CO)=C1 NAME: '
               '(2-Chloro-4-pyridinyl)methanol REASON: CORRECT Molecule '
               'contains a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: FC(F)(F)C(=O)Nc1ccc2oc(=O)c3ccccc3c2c1 NAME: '
               '2,2,2-Trifluoro-N-(6-oxo-6H-dibenzo[b,d]pyran-2-yl)acetamide '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CC3=CC=C(C=C3)F)O[C@H]1CN(C)C(=O)C)[C@@H](C)CO '
               'NAME: '
               'N-[[(4R,5R)-8-[2-(4-fluorophenyl)ethynyl]-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methylacetamide '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: '
               'CN1[C@@H]2CC[C@H](O[C@@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)C4=CC(=C(C=C4)F)F)CC(=O)N[C@H]5CCN(C5)CC6=CC=CC=C6 '
               'NAME: '
               'N-[(2S,4aR,12aS)-5-methyl-6-oxo-2-[2-oxo-2-[[(3S)-1-(phenylmethyl)-3-pyrrolidinyl]amino]ethyl]-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-8-yl]-3,4-difluorobenzamide '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC(=CC=C3)OC)O[C@H]1CN(C)C(=O)C4=CC=CC=C4F)[C@@H](C)CO '
               'NAME: '
               '2-fluoro-N-[[(4R,5R)-2-[(2S)-1-hydroxypropan-2-yl]-8-(3-methoxyphenyl)-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methylbenzamide '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: '
               'CN1[C@H]2CC[C@H](O[C@@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)C4=CC(=C(C=C4)F)F)CC(=O)N5CCOCC5 '
               'NAME: '
               'N-[(2S,4aS,12aS)-5-methyl-2-[2-(4-morpholinyl)-2-oxoethyl]-6-oxo-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-8-yl]-3,4-difluorobenzamide '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: COC(=O)Nc1nc2cc(ccc2[nH]1)C(=O)c1ccc(F)cc1 NAME: '
               'flubendazole REASON: CORRECT Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: CC(C)[C@H](Br)C(=O)NC(N)=O NAME: (S)-bromisoval '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: COc1cc(Cl)c(OC)cc1Cl NAME: chloroneb REASON: '
               'CORRECT Molecule contains a carbon-halogen bond on its main '
               'organic fragment\n'
               ' * SMILES: FC(F)O[C@@H](F)C(F)(F)F NAME: (S)-desflurane '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: OC(=O)C(c1ccc(Cl)cc1)c1ccc(Cl)cc1 NAME: '
               'bis(4-chlorophenyl)acetic acid REASON: CORRECT Molecule '
               'contains a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'ClC1=C(Cl)[C@@]2(Cl)[C@@H]3[C@H]4C[C@@H](C=C4)[C@@H]3[C@@]1(Cl)C2(Cl)Cl '
               'NAME: Isodrin REASON: CORRECT Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: COC(=O)CC(NC(=O)C(NC(=O)OC(C)C)C(C)C)c1ccc(Cl)cc1 '
               'NAME: methyl '
               '3-(4-chlorophenyl)-3-{[N-(isopropoxycarbonyl)valyl]amino}propanoate '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: CCCC(C(=O)OCC)c1cc(O)cc(c1)-c1ccc(cc1)C(F)(F)F '
               'NAME: ethyl '
               "2-[5-hydroxy-4'-(trifluoromethyl)biphenyl-3-yl]pentanoate "
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               ' * SMILES: C=1OC(=CC1)[C@@]2(OC(N(C2)C(C(Cl)Cl)=O)(C)C)[H] '
               'NAME: (R)-furilazole REASON: CORRECT Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: C1=COC(=C1)CNS(=O)(=O)C2=C(C=C(C(=C2)C(=O)O)Cl)Cl '
               'NAME: 2,4-dichloro-5-(2-furanylmethylsulfamoyl)benzoic acid '
               'REASON: CORRECT Molecule contains a carbon-halogen bond on its '
               'main organic fragment\n'
               'False positives: SMILES: '
               'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F '
               'NAME: 10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO '
               'NAME: LSM-10936 REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'C1C[C@@H]([C@H](O[C@@H]1CCNC(=O)C2CC2)CO)NS(=O)(=O)C3=CC=CC(=C3)F '
               'NAME: '
               'N-[2-[(2S,5S,6S)-5-[(3-fluorophenyl)sulfonylamino]-6-(hydroxymethyl)-2-oxanyl]ethyl]cyclopropanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C1C[C@@H]([C@H](O[C@@H]1CC(=O)NCC2=CC(=C(C=C2)Cl)Cl)CO)NC(=O)C3=CN=CC=C3 '
               'NAME: '
               'N-[(2S,3S,6S)-6-[2-[(3,4-dichlorophenyl)methylamino]-2-oxoethyl]-2-(hydroxymethyl)-3-oxanyl]-3-pyridinecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'CCC(=O)N1CC2(CN(C2)CC3=CC=C(C=C3)F)C4=C([C@@H]1CO)N(C5=C4C=CC(=C5)OC)C '
               'NAME: '
               "1-[(1R)-1'-[(4-fluorophenyl)methyl]-1-(hydroxymethyl)-7-methoxy-9-methyl-2-spiro[1,3-dihydropyrido[3,4-b]indole-4,3'-azetidine]yl]-1-propanone "
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC=C(C=C3)C#N)O[C@@H]1CN(C)CC4=CC(=CC=C4)F)[C@H](C)CO '
               'NAME: '
               '4-[(4S,5S)-5-[[(3-fluorophenyl)methyl-methylamino]methyl]-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-8-yl]benzonitrile '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)Br)O[C@H]1CN(C)S(=O)(=O)C3=CC=C(C=C3)C)[C@H](C)CO '
               'NAME: '
               'N-[[(4R,5R)-8-bromo-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N,4-dimethylbenzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'ClC1=C2C(=COC(=C2)/C=C/[C@H]([C@H](O)C)C)[C@@H]3[C@H](C(=O)/C(=C/C)/C)C(O[C@@]3(C1=O)C)=O '
               'NAME: Chaetomugilin N REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'C[C@H](CN(CC1=CC=CC=C1Cl)[C@H](C)CO)[C@H](CN(C)C(=O)NC2=CC=C(C=C2)Cl)OC '
               'NAME: '
               '3-(4-chlorophenyl)-1-[(2R,3R)-4-[(2-chlorophenyl)methyl-[(2R)-1-hydroxypropan-2-yl]amino]-2-methoxy-3-methylbutyl]-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'BrC1=C(Br)C=CC(=C1)C=2C3=C(OCC2OC4=CC(O)=CC=C4)C(=CC=C3O)[C@@H](O)CN '
               'NAME: Ammonificin D REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'CCCNC(=O)N(C)C[C@H]1[C@@H](CN(C(=O)C2=CC(=CN=C2O1)Br)[C@@H](C)CO)C '
               'NAME: '
               '1-[[(2R,3R)-8-bromo-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-1-methyl-3-propylurea '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'N[C@@H](CCC(=O)N[C@@H](CSC1C=CC(Br)=CC1O)C(=O)NCC(O)=O)C(O)=O '
               'NAME: 3,4-Dihydro-3-hydroxy-4-S-glutathionyl bromobenzene '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC4=C(C=C3)OCO4)[C@H](C)CO)C)CN(C)CC5=CC(=C(C=C5)Cl)Cl '
               'NAME: '
               '1-(1,3-benzodioxol-5-yl)-3-[(3R,9R,10R)-9-[[(3,4-dichlorophenyl)methyl-methylamino]methyl]-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]urea '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'CC1=CC(=C(C=C1)OC)NC(=O)C2=C(N(N=N2)CC3=CC(=CC=C3)C(F)(F)F)N '
               'NAME: '
               '5-amino-N-(2-methoxy-5-methylphenyl)-1-[[3-(trifluoromethyl)phenyl]methyl]-4-triazolecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'S=C1N(C2=C(N1)C=CC=C2)C3CCN(CC3)CCCC(=O)C4=CC=C(C=C4)F NAME: '
               'timiperone REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'C1CCN(C1)CCNC(=O)C[C@@H]2C=C[C@@H]([C@@H](O2)CO)NC(=O)NC3=CC=C(C=C3)F '
               'NAME: '
               '2-[(2R,3S,6R)-3-[[(4-fluoroanilino)-oxomethyl]amino]-2-(hydroxymethyl)-3,6-dihydro-2H-pyran-6-yl]-N-[2-(1-pyrrolidinyl)ethyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'CC=CC1=CC=C(C=C1)[C@H]2[C@H](N(C23CN(C3)CCC(F)(F)F)C(=O)C4=CC=CC=N4)CO '
               'NAME: LSM-42179 REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'N(C(=O)C=1C(=NOC1C)C2=C(C=CC=C2F)Cl)[C@@H]([C@@]3(N[C@H](C(S3)(C)C)C(O)=O)[H])C(=O)NCCCC[C@@H](C(=O)O)N '
               'NAME: flucloxacilloyl-L-lysine REASON: WRONGLY CLASSIFIED '
               'Molecule contains a carbon-halogen bond on its main organic '
               'fragment\n'
               ' * SMILES: '
               'C1CC1CC(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@@H](O[C@@H]4CO)CC(=O)NCC5=C(C=CC(=C5)F)F '
               'NAME: '
               'N-[(1R,3R,4aS,9aR)-3-[2-[(2,5-difluorophenyl)methylamino]-2-oxoethyl]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               '[K+].[K+].[K+].[K+].[K+].[K+].[O-]C(=O)CN(CC([O-])=O)c1ccccc1OCCOc1cc(NC(=O)c2ccc3c(c2)C(=O)OC32c3cc(Cl)c([O-])cc3Oc3cc([O-])c(Cl)cc23)ccc1N(CC([O-])=O)CC([O-])=O '
               'NAME: calcium green 1 REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CCC(F)(F)F)O[C@H]1CN(C)CC3CC3)[C@@H](C)CO '
               'NAME: '
               'N-[(2R,3R)-2-[[cyclopropylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-4,4,4-trifluorobutanamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: CCOC(=O)C1=C(N=C(N=N1)C2=CC=C(C=C2)C)SC3=CC=CC=C3Cl '
               'NAME: '
               '5-[(2-chlorophenyl)thio]-3-(4-methylphenyl)-1,2,4-triazine-6-carboxylic '
               'acid ethyl ester REASON: WRONGLY CLASSIFIED Molecule contains '
               'a carbon-halogen bond on its main organic fragment\n'
               ' * SMILES: C1CCN(C1)C(C2=CC=C(C=C2)Br)C3=CC4=C(C=C3O)OCO4 '
               'NAME: '
               '6-[(4-bromophenyl)-(1-pyrrolidinyl)methyl]-1,3-benzodioxol-5-ol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C1C[C@@H](C/C(=C/C=C/2\\CCC[C@]3([C@]2(CC[C@]3([H])[C@](CCCC(C(F)(F)F)O)([H])C)[H])C)/C1=C)O '
               'NAME: '
               '(5Z,7E)-(3S)-26,26,26-trifluoro-27-nor-9,10-seco-5,7,10(19)-cholestatriene-3,25-diol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               ' * SMILES: '
               'C1[C@H]2[C@H]([C@H](N2C(=O)C3=CC=NC=C3)CO)C4=CC=CC=C4N1C(=O)NC5=CC(=CC=C5)Cl '
               'NAME: '
               '(1S,2aR,8bR)-N-(3-chlorophenyl)-1-(hydroxymethyl)-2-[oxo(pyridin-4-yl)methyl]-1,2a,3,8b-tetrahydroazeto[2,3-c]quinoline-4-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbon-halogen '
               'bond on its main organic fragment\n'
               'False negatives: SMILES: Cln1c(=O)n(Cl)c(=O)n(Cl)c1=O NAME: '
               '1,3,5-trichloro-1,3,5-triazinane-2,4,6-trione REASON: MISSED '
               'No carbon-halogen bond found in the main organic fragment\n'
               ' * SMILES: Brn1ccc2ccccc12 NAME: 1-bromoindole REASON: MISSED '
               'No carbon-halogen bond found in the main organic fragment\n'
               ' * SMILES: '
               'CC1=CC(C)=C(NC(=O)C2=CC(=CC(=C2)C#N)S(F)(F)(F)(F)F)C=C1N1C=CN2N=C(C=C12)C1=CC=CN=C1 '
               'NAME: BAY-826 REASON: MISSED No carbon-halogen bond found in '
               'the main organic fragment\n'
               ' * SMILES: [Zr](Cl)(C1C=CC=C1)(C2C=CC=C2)Cl NAME: Zirconocene '
               'dichloride REASON: MISSED No carbon-halogen bond found in the '
               'main organic fragment\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)O)CC1=CC=CC=C1)[C@H]2N(C(=O)[C@@H](NC(=O)[C@@H](N)[C@H](CC)C)CC=3NC=NC3)CCC2 '
               'NAME: Angiotensin (5-8) REASON: MISSED No carbon-halogen bond '
               'found in the main organic fragment\n'
               ' * SMILES: BrN1C(=O)CCC1=O NAME: N-bromosuccinimide REASON: '
               'MISSED No carbon-halogen bond found in the main organic '
               'fragment\n'
               ' * SMILES: O=c1cc(oc2c(cccc12)-c1ccccc1)N1CCOCC1 NAME: '
               'LY294002 REASON: MISSED No carbon-halogen bond found in the '
               'main organic fragment\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': 'O([C@@H]1O[C@H]([C@@H](O)[C@@H](O)[C@H]1O)C(O)=O)[C@H](CCCCC)[C@H](O)C/C=C\\CCCCCCCC(O)=O',
                                     'name': '12-O-D-Glucuronoside-13-hydroxyoctadec-9Z-enoate',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'},
                                 {   'smiles': '[O-]C(=O)OON=O',
                                     'name': 'nitrosoperoxycarbonate(1-)',
                                     'reason': 'No carbon-halogen bond found '
                                               'in the main organic fragment'}],
    'sample_false_negatives': [   {   'smiles': 'Cln1c(=O)n(Cl)c(=O)n(Cl)c1=O',
                                      'name': '1,3,5-trichloro-1,3,5-triazinane-2,4,6-trione',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic fragment'},
                                  {   'smiles': 'Brn1ccc2ccccc12',
                                      'name': '1-bromoindole',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic fragment'},
                                  {   'smiles': 'CC1=CC(C)=C(NC(=O)C2=CC(=CC(=C2)C#N)S(F)(F)(F)(F)F)C=C1N1C=CN2N=C(C=C12)C1=CC=CN=C1',
                                      'name': 'BAY-826',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic fragment'},
                                  {   'smiles': '[Zr](Cl)(C1C=CC=C1)(C2C=CC=C2)Cl',
                                      'name': 'Zirconocene dichloride',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic fragment'},
                                  {   'smiles': 'O=C(N[C@H](C(=O)O)CC1=CC=CC=C1)[C@H]2N(C(=O)[C@@H](NC(=O)[C@@H](N)[C@H](CC)C)CC=3NC=NC3)CCC2',
                                      'name': 'Angiotensin (5-8)',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic fragment'},
                                  {   'smiles': 'BrN1C(=O)CCC1=O',
                                      'name': 'N-bromosuccinimide',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic fragment'},
                                  {   'smiles': 'O=c1cc(oc2c(cccc12)-c1ccccc1)N1CCOCC1',
                                      'name': 'LY294002',
                                      'reason': 'No carbon-halogen bond found '
                                                'in the main organic '
                                                'fragment'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning. The previous attempt always took the '
                 'largest (by heavy‐atom count) fragment as “the main organic '
                 'fragment” and then scanned every bond looking for a '
                 'carbon–halogen connection. However, many false positives '
                 'arose because the largest fragment (or even some fragments) '
                 'might be inorganic, have atypical bonding, or even include '
                 'extraneous groups that contribute halogen atoms outside the '
                 '“organic” core. Also, a few false negatives resulted when '
                 'the main fragment chosen did not actually include the carbon '
                 'atoms that we wish to screen (for example if the largest '
                 'fragment was chosen purely by heavy‐atom count rather than '
                 'by presence of carbon). \n'
                 '\n'
                 'To improve the classification we now (1) filter out '
                 'nonorganic fragments (i.e. fragments with no carbon atoms) '
                 'and (2) select as the “main” fragment the one having the '
                 'most carbon atoms. This is more in line with the notion of '
                 'the “main organic fragment.” Then we iterate over all bonds '
                 'in that fragment to check if (and which) a carbon is '
                 'directly bound to a halogen (F, Cl, Br, I). In the code '
                 'below we also include inline comments for clarity.\n'
                 '\n'
                 'Below is the single Python code block implementing the '
                 'improvements:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3545,
    'num_false_positives': 12902,
    'num_true_negatives': 125846,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.21554082811454978,
    'recall': 0.9980292792792793,
    'f1': 0.3545177258862943,
    'accuracy': 0.9092832044975404,
    'negative_predictive_value': 0.999944379553924}