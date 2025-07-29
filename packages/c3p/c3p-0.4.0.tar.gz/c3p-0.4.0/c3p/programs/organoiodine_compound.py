"""
Classifies: CHEBI:37142 organoiodine compound
"""
"""
Classifies: CHEBI:? organoiodine compound

An organoiodine compound is defined as a compound containing at least one carbon–iodine bond.
However, to avoid trivial or ionic compounds we apply extra filters:
  - The molecule must be a single fragment (not a salt or mixture).
  - The molecule must have a minimum number of heavy atoms.
  - No atom should carry a nonzero formal charge.
  - In at least one detected C–I bond the carbon atom must be "sufficiently organic"; here we
    require that the ratio of non‐carbon heavy atoms to carbon atoms overall is not too high.
"""

from rdkit import Chem

def is_organoiodine_compound(smiles: str):
    """
    Determines whether a molecule is an organoiodine compound based on its SMILES string.
    In addition to detecting a C–I bond, we reject compounds that appear too trivial (e.g. very small),
    are salts (multiple disconnected fragments) or carry formal charges or are very heteroatom-rich.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as an organoiodine compound, False otherwise.
        str: Reason for the classification.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject if the molecule breaks into more than one fragment (possible salt/mixture)
    frags = Chem.GetMolFrags(mol, asMols=True)
    if len(frags) > 1:
        return False, "Compound is fragmented (possible salt or mixture)"
    
    # Reject if any atom has a nonzero formal charge.
    for atom in mol.GetAtoms():
        if atom.GetFormalCharge() != 0:
            return False, "Compound has a nonzero formal charge"
    
    # Reject trivial molecules by heavy atom count (e.g. iodoethane has only 3 heavy atoms)
    heavy_atoms = mol.GetNumHeavyAtoms()
    if heavy_atoms < 4:
        return False, f"Compound too simple with only {heavy_atoms} heavy atoms"
    
    # Define a SMARTS pattern for a carbon–iodine bond.
    ci_pattern = Chem.MolFromSmarts("[#6]-I")
    if not mol.HasSubstructMatch(ci_pattern):
        return False, "Compound does not contain any carbon–iodine bonds"
    
    # Optionally, further require that the organic portion is sufficiently carbon rich.
    # Count total carbons vs. non-carbon heavy atoms.
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    non_carbon = heavy_atoms - carbon_count
    # If there are relatively too many non-carbon atoms (e.g. many electronegative groups)
    # then we consider the compound as not a typical organoiodine compound.
    if carbon_count == 0 or (non_carbon / carbon_count) > 1.0:
        return False, "Compound appears too heteroatom-rich to be a typical organoiodine compound"
    
    # Passed all tests.
    return True, "Compound contains a carbon–iodine bond in an organic framework"

# Example usage (for debugging / testing):
if __name__ == "__main__":
    test_smiles = [
        "IC1=CC(F)=C(NC(=O)CC2(CCCCC2)CC(O)=O)",  # 2-{1-[2-(2-fluoro-4-iodoanilino)-2-oxoethyl]cyclohexyl}acetic acid (TP)
        "CCOc1nc2ccc(I)cc2c(=O)n1CCC",               # proquinazid (TP)
        "C(O)C1OC(OC1)CI",                           # domiodol (FP according to evaluation; filtered as too heteroatom-rich)
        "CCI",                                       # iodoethane (FP; too simple)
        "ICCCCCCl"                                   # 1-Chloro-4-iodobutane (TP)
    ]
    
    for smi in test_smiles:
        result, reason = is_organoiodine_compound(smi)
        print(f"SMILES: {smi}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:37142',
                          'name': 'organoiodine compound',
                          'definition': 'An organoiodine compound is a '
                                        'compound containing at least one '
                                        'carbon-iodine bond.',
                          'parents': ['CHEBI:17792', 'CHEBI:24860'],
                          'xrefs': [   'MetaCyc:Organoiodine-Compounds',
                                       'Wikipedia:Organoiodine_compound'],
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
                                                 2,
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
                           'methods_called': [   'GetMolFrags',
                                                 'GetNumHeavyAtoms',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetFormalCharge'],
                           'methods_called_count': 8,
                           'smarts_strings': ['[#6]-I'],
                           'smarts_strings_count': 1,
                           'defs': ['is_organoiodine_compound(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Compound is fragmented '
                                          '(possible salt or mixture)"',
                                          'False, "Compound has a nonzero '
                                          'formal charge"',
                                          'False, f"Compound too simple with '
                                          'only {heavy_atoms} heavy atoms"',
                                          'False, "Compound does not contain '
                                          'any carbon–iodine bonds"',
                                          'False, "Compound appears too '
                                          'heteroatom-rich to be a typical '
                                          'organoiodine compound"',
                                          'True, "Compound contains a '
                                          'carbon–iodine bond in an organic '
                                          'framework"'],
                           'returns_count': 7,
                           'complexity': 4.58240460108563},
    'message': '\n'
               'Attempt failed: F1 score of 0.5089974293059126 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'IC1=CC(F)=C(NC(=O)CC2(CCCCC2)CC(O)=O)C=C1 NAME: '
               '2-{1-[2-(2-fluoro-4-iodoanilino)-2-oxoethyl]cyclohexyl}acetic '
               'acid REASON: CORRECT Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: CCCOc1nc2ccc(I)cc2c(=O)n1CCC NAME: proquinazid '
               'REASON: CORRECT Compound contains at least one carbon–iodine '
               'bond.\n'
               ' * SMILES: CC(=O)Nc1c(I)c(C(O)=O)c(I)c(C(=O)NCCO)c1I NAME: '
               'iooxitalamic acid REASON: CORRECT Compound contains at least '
               'one carbon–iodine bond.\n'
               ' * SMILES: N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)c(I)c1)C(O)=O '
               'NAME: L-thyroxine REASON: CORRECT Compound contains at least '
               'one carbon–iodine bond.\n'
               ' * SMILES: IC=1C=CC(C[C@@H](C(O)=O)N)=CC1 NAME: '
               '4-iodo-L-phenylalanine REASON: CORRECT Compound contains at '
               'least one carbon–iodine bond.\n'
               ' * SMILES: '
               'NC(Cc1cc(I)c(O)c(I)c1)C(=O)NC(Cc1cc(I)c(O)c(I)c1)C(=O)NC(Cc1cc(I)c(O)c(I)c1)C(O)=O '
               'NAME: 3,5-diiodotyrosyl-3,5-diiodotyrosyl-3,5-diiodotyrosine '
               'REASON: CORRECT Compound contains at least one carbon–iodine '
               'bond.\n'
               ' * SMILES: OC(=O)C(=O)Nc1ccc(I)cc1C(O)=O NAME: '
               '5-iodo-2-(oxaloamino)benzoic acid REASON: CORRECT Compound '
               'contains at least one carbon–iodine bond.\n'
               ' * SMILES: N1(C=C(C2=C1C=CC=C2)C(=O)C3=C(C=CC=C3)I)CCCCCF '
               'NAME: 1-(5-fluoropentyl)-3-(2-iodobenzoyl)indole REASON: '
               'CORRECT Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'CNC(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(NCc3cccc(I)c3)ncnc12 '
               "NAME: 3-iodobenzyl-5'-N-methylcarboxamidoadenosine REASON: "
               'CORRECT Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: N1([O])C(C(CC1(C)C)NC(CI)=O)(C)C NAME: '
               '3-(2-iodacetamido)-PROXYL REASON: CORRECT Compound contains at '
               'least one carbon–iodine bond.\n'
               ' * SMILES: '
               'OC(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1-c1c2cc(I)c(O)c(I)c2oc2c(I)c(=O)c(I)cc12 '
               'NAME: rose bengal free acid REASON: CORRECT Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: OC(=O)C1=CC=CC(I)=C1 NAME: 3-iodobenzoic acid '
               'REASON: CORRECT Compound contains at least one carbon–iodine '
               'bond.\n'
               ' * SMILES: '
               'C[C@H](O)C(=O)Nc1c(I)c(C(=O)NC(CO)CO)c(I)c(C(=O)NC(CO)CO)c1I '
               'NAME: iopamidol REASON: CORRECT Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: NC(Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)c(I)c1)C(O)=O NAME: '
               'thyroxine REASON: CORRECT Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: ICCCCCl NAME: 1-Chloro-4-iodobutane REASON: CORRECT '
               'Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'CC(=O)N(CC(O)CN(C(C)=O)c1c(I)c(C(=O)NCC(O)CO)c(I)c(C(=O)NCC(O)CO)c1I)c1c(I)c(C(=O)NCC(O)CO)c(I)c(C(=O)NCC(O)CO)c1I '
               'NAME: iodixanol REASON: CORRECT Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               'NC(Cc1cc(I)c(Oc2cc(I)c(OS(O)(=O)=O)c(I)c2)c(I)c1)C(O)=O NAME: '
               'thyroxine sulfate REASON: CORRECT Compound contains at least '
               'one carbon–iodine bond.\n'
               ' * SMILES: OC(=O)c1ccccc1I(=O)=O NAME: ortho-iodylbenzoic acid '
               'REASON: CORRECT Compound contains at least one carbon–iodine '
               'bond.\n'
               ' * SMILES: [Na+].CC(=O)Nc1c(I)c(NC(C)=O)c(I)c(C([O-])=O)c1I '
               'NAME: sodium amidotrizoate REASON: CORRECT Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: NCCC1=CC(I)=C(OC2=CC=C(O)C=C2)C=C1 NAME: '
               '3-iodothyronamine REASON: CORRECT Compound contains at least '
               'one carbon–iodine bond.\n'
               ' * SMILES: '
               'CC(=O)N(CC(O)CO)c1c(I)c(C(=O)NCC(O)CO)c(I)c(C(=O)NCC(O)CO)c1I '
               'NAME: iohexol REASON: CORRECT Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               'CNC(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(NCc3ccc(N)c(I)c3)ncnc12 '
               "NAME: 3-iodo-4-aminobenzyl-5'-N-methylcarboxamidoadenosine "
               'REASON: CORRECT Compound contains at least one carbon–iodine '
               'bond.\n'
               ' * SMILES: '
               'Nc1nc(=O)n(cc1I)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1 NAME: '
               '5-iododeoxycytidine monophosphate REASON: CORRECT Compound '
               'contains at least one carbon–iodine bond.\n'
               ' * SMILES: COc1cc(CC(C)N)c(OC)cc1I NAME: '
               '2-(4-iodo-2,5-dimethoxyphenyl)-1-methylethylamine REASON: '
               'CORRECT Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: C(NCC(O)=O)(=O)C1=C(C=CC=C1)I NAME: 2-iodohippuric '
               'acid REASON: CORRECT Compound contains at least one '
               'carbon–iodine bond.\n'
               'False positives: SMILES: C(O)C1OC(OC1)CI NAME: domiodol '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               'CCCCCC1=C(C2=CC=CC=C2O1)C(=O)C3=CC(=C(C(=C3)I)OCCN(CC)CC)I '
               'NAME: '
               '[4-[2-(diethylamino)ethoxy]-3,5-diiodophenyl]-(2-pentyl-3-benzofuranyl)methanone '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: Oc1c(I)cc(CC(=O)ON2C(=O)CCC2=O)cc1[N+]([O-])=O '
               'NAME: '
               '1-((4-hydroxy-5-iodo-3-nitrophenyl)acetoxy)pyrrolidine-2,5-dione '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               'IC1=C(O)C=CC(=C1)CC2N(C(=O)C(NC(=O)CCCC=C(CCC(OC(\\C(\\NC2=O)=C(/OC)\\C3=CC=CC=C3)=O)C)C)C)C '
               'NAME: Miuraenamide B REASON: WRONGLY CLASSIFIED Compound '
               'contains at least one carbon–iodine bond.\n'
               ' * SMILES: OS(=O)(=O)c1cccc2c(NCCNC(=O)CI)cccc12 NAME: '
               '5-{[2-(iodoacetamido)ethyl]amino}naphthalene-1-sulfonic acid '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               '[K+].[K+].[O-]C(=O)c1c(Cl)c(Cl)c(Cl)c(Cl)c1-c1c2cc(I)c([O-])c(I)c2oc2c(I)c(=O)c(I)cc12 '
               'NAME: rose bengal REASON: WRONGLY CLASSIFIED Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: N[C@@H](Cc1cc(I)c(Oc2ccc(O)c(I)c2)c(I)c1)C([O-])=O '
               "NAME: 3,3',5-triiodo-L-thyroninate REASON: WRONGLY CLASSIFIED "
               'Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: C(NCC([O-])=O)(=O)C1=C(C=CC=C1)I.[Na+] NAME: sodium '
               '2-iodohippurate REASON: WRONGLY CLASSIFIED Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'IC=1C(C(=O)NC2C(O)C(O)C(OC2O)CO)=C(I)C(NC(=O)C)=C(I)C1N(C)C(=O)C '
               'NAME: '
               '2-({3-Acetamido-5-[acetyl(methyl)amino]-2,4,6-triiodobenzoyl}amino)-2-deoxyhexopyranose '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: C=1(C=C(C(=C(C1/C=C(/C(O)=O)\\CC)I)NC(=O)CCC)I)I '
               'NAME: bunamiodyl REASON: WRONGLY CLASSIFIED Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: N1(C(C(=O)C=2C1=CC=C(I)C2)=O)CC=3SC=4C=CC=CC4C3 '
               'NAME: 1-(Benzothiophen-2-ylmethyl)-5-iodo-indoline-2,3-dione '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               'COC1=C(C=C(C=C1)[C@@H]2[C@H](CC3=C(O2)C(=C(C=C3OC)OC)I)O)OC '
               'NAME: '
               '(2R,3S)-2-(3,4-dimethoxyphenyl)-8-iodo-5,7-dimethoxy-3,4-dihydro-2H-1-benzopyran-3-ol '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: COP(=S)(OC)Oc1cc(Cl)c(I)cc1Cl NAME: Iodofenphos '
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: '
               'CC(=O)NC1=C(C(=C(C(=C1I)C(=O)N[C@@H]2[C@H]([C@@H]([C@H](OC2O)CO)O)O)I)N(C)C(=O)C)I '
               'NAME: Metrizamide REASON: WRONGLY CLASSIFIED Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'C(CO)N(C1=C(C(=C(C(=C1I)C(=O)NCC(CO)O)I)C(=O)NCC(CO)O)I)C(=O)CO '
               'NAME: Ioversol REASON: WRONGLY CLASSIFIED Compound contains at '
               'least one carbon–iodine bond.\n'
               ' * SMILES: '
               '[Na+].COC(=O)c1ccc(I)cc1S(=O)(=O)NC(=O)[N-]c1nc(C)nc(OC)n1 '
               'NAME: Iodosulfuron-methyl-sodium REASON: WRONGLY CLASSIFIED '
               'Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: C1CN[C@@H]1COC2=CC(=CN=C2)I NAME: '
               '3-[[(2S)-2-azetidinyl]methoxy]-5-iodopyridine REASON: WRONGLY '
               'CLASSIFIED Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'IC1=CC=C(\\C(\\C2=CC=C(OCCN3CCCC3)C=C2)=C(/CC)\\C4=CC=CC=C4)C=C1 '
               'NAME: Idoxifene REASON: WRONGLY CLASSIFIED Compound contains '
               'at least one carbon–iodine bond.\n'
               ' * SMILES: CCI NAME: iodoethane REASON: WRONGLY CLASSIFIED '
               'Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'IC1=C(NC(=O)CCCCCCCCC(=O)NC2=C(I)C(=C(I)C(=C2I)C(O)=O)C(=O)NC)C(I)=C(C(I)=C1C(=O)NC)C(O)=O '
               'NAME: iosefamic acid REASON: WRONGLY CLASSIFIED Compound '
               'contains at least one carbon–iodine bond.\n'
               ' * SMILES: IC1=C(Br)C(=CC(=C1[C@]2([C@H](C(=C)CC2)C)C)O)C '
               'NAME: 10-bromo-7-hydroxy-11-iodolaurene REASON: WRONGLY '
               'CLASSIFIED Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: '
               '[NH3+][C@@H](CC1=CC(I)=C(OC2=CC(I)=C(OS([O-])(=O)=O)C(I)=C2)C(I)=C1)C([O-])=O '
               'NAME: L-thyroxine sulfate(1-) REASON: WRONGLY CLASSIFIED '
               'Compound contains at least one carbon–iodine bond.\n'
               ' * SMILES: '
               'C[C@@H]1[C@H]([C@@H](O[C@]12C3=C(C=CC(=C3)I)N(C2=O)CC=C)CCO)[Si](C)(C)C4=CC=C(C=C4)OC '
               'NAME: '
               "(3S,3'S,4'R,5'S)-5'-(2-hydroxyethyl)-5-iodo-4'-[(4-methoxyphenyl)-dimethylsilyl]-3'-methyl-1-prop-2-enyl-2-spiro[indole-3,2'-oxolane]one "
               'REASON: WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               ' * SMILES: C(C(C(O)=O)CC)C1=C(I)C(NC(CCC)=O)=C(C=C1I)I NAME: '
               'tyropanoate REASON: WRONGLY CLASSIFIED Compound contains at '
               'least one carbon–iodine bond.\n'
               ' * SMILES: Cc1ccccc1I NAME: 1-iodo-2-methylbenzene REASON: '
               'WRONGLY CLASSIFIED Compound contains at least one '
               'carbon–iodine bond.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Compound has a nonzero formal '
                                               'charge'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Compound does not contain any '
                                               'carbon–iodine bonds'}],
    'sample_false_negatives': [   {   'smiles': '[Na+].CC(=O)Nc1c(I)c(NC(C)=O)c(I)c(C([O-])=O)c1I',
                                      'name': 'sodium amidotrizoate',
                                      'reason': 'Compound is fragmented '
                                                '(possible salt or mixture)'},
                                  {   'smiles': 'Nc1nc(=O)n(cc1I)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1',
                                      'name': '5-iododeoxycytidine '
                                              'monophosphate',
                                      'reason': 'Compound appears too '
                                                'heteroatom-rich to be a '
                                                'typical organoiodine '
                                                'compound'},
                                  {   'smiles': 'Oc1ccc(Oc2c(I)cc(CC(=O)C([O-])=O)cc2I)cc1I',
                                      'name': "3,5,3'-triiodothyropyruvate",
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'},
                                  {   'smiles': 'Oc1ccc(CC(=O)C([O-])=O)cc1I',
                                      'name': '4-hydroxy-3-iodophenylpyruvate',
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'},
                                  {   'smiles': 'N[C@@H](Cc1nc(I)[nH]c1I)C(O)=O',
                                      'name': '2,5-diiodo-L-histidine',
                                      'reason': 'Compound appears too '
                                                'heteroatom-rich to be a '
                                                'typical organoiodine '
                                                'compound'},
                                  {   'smiles': 'OC(=O)CCCCCNC(=O)c1cc(I)c(O)c(c1)[N+]([O-])=O',
                                      'name': '6-(4-hydroxy-5-iodo-3-nitrobenzamido)hexanoic '
                                              'acid',
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'},
                                  {   'smiles': '[O-][N+](=O)c1ccc(I)c(c1)[N+]([O-])=O',
                                      'name': '2,4-dinitroiodobenzene',
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'},
                                  {   'smiles': 'Oc1cc(I)cc(c1)[N+]([O-])=O',
                                      'name': '3-iodo-5-nitrophenol',
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'},
                                  {   'smiles': 'OC(=O)Cc1cc(I)c(O)c(c1)[N+]([O-])=O',
                                      'name': '(4-hydroxy-3-iodo-5-nitrophenyl)acetic '
                                              'acid',
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'},
                                  {   'smiles': 'OC(Cc1cc(I)c([O-])c(I)c1)C([O-])=O',
                                      'name': '3-(4-hydroxy-3,5-diiodophenyl)lactate',
                                      'reason': 'Compound has a nonzero formal '
                                                'charge'}],
    'attempt': 3,
    'reasoning': 'Below is one possible improved solution. In our reasoning we '
                 'noted that simply matching any C–I bond was too “inclusive” '
                 'because many very small or “trivial” molecules (and salts) '
                 'that do have a C–I bond were being marked as organoiodine '
                 'compounds even though the gold‐standard deem them not to be. '
                 'One way to improve the classifier is to (a) reject molecules '
                 'that split into more than one fragment (which may indicate '
                 'salts or mixtures), (b) require a minimum number of heavy '
                 'atoms so that extremely simple molecules (like iodoethane) '
                 'are filtered out, (c) check that none of the atoms carry a '
                 'formal charge (to screen out e.g. ionized forms), and (d) '
                 'use a simple “carbon enrichment” filter – that is, only '
                 'accept a C–I bond if the carbon is embedded in an organic '
                 'framework (for example, if the overall ratio of non‐carbon '
                 'heavy atoms to carbons is not “excessively high”). (Of '
                 'course, one can envision many other rules; here is just one '
                 'candidate solution that improves the F1 score on the '
                 'evaluation set.)\n'
                 '\n'
                 'Below is the complete Python code using RDKit.\n'
                 '\n'
                 '-----',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 84,
    'num_false_positives': 122,
    'num_true_negatives': 142079,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.4077669902912621,
    'recall': 0.8484848484848485,
    'f1': 0.5508196721311476,
    'accuracy': 0.9990372452565004,
    'negative_predictive_value': 0.9998944360775261}