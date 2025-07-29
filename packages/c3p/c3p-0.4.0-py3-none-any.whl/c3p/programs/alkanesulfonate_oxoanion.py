"""
Classifies: CHEBI:134249 alkanesulfonate oxoanion
"""
"""
Classifies: CHEBI: alkanesulfonate oxoanion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alkanesulfonate_oxoanion(smiles: str):
    """
    Determines if a molecule is an alkanesulfonate oxoanion based on its SMILES string.
    An alkanesulfonate oxoanion is characterized by the presence of at least one sulfonate group (-SO3-)
    attached to a carbon atom, with the carbon potentially being part of a chain or other simple groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkanesulfonate oxoanion, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for the sulfonate group pattern (-SO3-)
    sulfonate_pattern = Chem.MolFromSmarts("[SX4](=[OX1])(=[OX1])([OX1-])")
    if not mol.HasSubstructMatch(sulfonate_pattern):
        return False, "No sulfonate group (-SO3-) found"

    # Check if the sulfonate group is attached to a carbon atom
    sulfonate_carbon_pattern = Chem.MolFromSmarts("[CX4][SX4](=[OX1])(=[OX1])([OX1-])")
    if not mol.HasSubstructMatch(sulfonate_carbon_pattern):
        return False, "Sulfonate group not attached to a carbon atom"

    # Check that the carbon attached to the sulfonate is part of a simple alkyl chain
    # and not part of a ring or conjugated system
    sulfonate_carbon = mol.GetSubstructMatch(sulfonate_carbon_pattern)[0]
    carbon_atom = mol.GetAtomWithIdx(sulfonate_carbon)
    if carbon_atom.IsInRing():
        return False, "Sulfonate group attached to a carbon in a ring"
    if carbon_atom.GetHybridization() != Chem.HybridizationType.SP3:
        return False, "Sulfonate group attached to a non-SP3 hybridized carbon"

    # Check for the presence of at least one carbon atom in the molecule
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 1:
        return False, "No carbon atoms found in the molecule"

    # Check for the presence of at least one oxygen atom in the molecule
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count < 3:
        return False, "Insufficient oxygen atoms for a sulfonate group"

    # Check for the presence of at least one sulfur atom in the molecule
    s_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 16)
    if s_count < 1:
        return False, "No sulfur atom found in the molecule"

    # Check for the presence of a negative charge on the sulfonate group
    negative_charge_count = sum(1 for atom in mol.GetAtoms() if atom.GetFormalCharge() == -1)
    if negative_charge_count < 1:
        return False, "No negative charge found on the sulfonate group"

    # Check for invalid functional groups (e.g., thiols, sulfides, complex structures)
    invalid_functional_groups = ["[SX2]", "[SX1]", "[c]", "[C]=[C]", "[C]#[C]"]
    for group in invalid_functional_groups:
        pattern = Chem.MolFromSmarts(group)
        if mol.HasSubstructMatch(pattern):
            return False, f"Molecule contains invalid functional group: {group}"

    return True, "Contains a sulfonate group (-SO3-) attached to a simple carbon chain or other groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134249',
                          'name': 'alkanesulfonate oxoanion',
                          'definition': 'An alkanesulfonate in which the '
                                        'carbon at position 1 is attached to '
                                        'R, which can represent hydrogens, a '
                                        'carbon chain, or other groups.',
                          'parents': ['CHEBI:33554'],
                          'xrefs': ['MetaCyc:Alkanesulfonates'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.3975903614457831 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C(C(NCCS([O-])(=O)=O)=O)CCCCCCCCCCCC '
               'NAME: N-tetradecanoyltaurine(1-) REASON: CORRECT Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               'C(=C/[C@H](C/C=C\\CCCCC)OO)\\C=C/C/C=C\\CCCC(=O)NCCS([O-])(=O)=O '
               'NAME: '
               'N-[12(S)-hydroperoxy-(5Z,8Z,10E,14Z)-icosatetraenoyl]taurine(1-) '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: C(CS([O-])(=O)=O)NC(C)=O NAME: acetyltaurine(1-) '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: NCCS([O-])(=O)=O NAME: 2-aminoethanesulfonate '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: CCCCCCCCCCCCCCCCS([O-])(=O)=O NAME: '
               'hexadecane-1-sulfonate REASON: CORRECT Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: FC(S([O-])(=O)=O)(F)F NAME: triflate REASON: '
               'CORRECT Contains a sulfonate group (-SO3-) attached to a '
               'carbon chain or other groups\n'
               ' * SMILES: O[C@H](CS([O-])(=O)=O)C([O-])=O NAME: '
               '(S)-3-sulfonatolactate(2-) REASON: CORRECT Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: OC(CS([O-])(=O)=O)C=O NAME: 3-sulfolactaldehyde(1-) '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: '
               '[Na+].[H]C(=C([H])C([H])=C([H])C1=[N+](CCCCS([O-])(=O)=O)c2ccc3ccccc3c2C1(C)C)C([H])=C([H])C([H])=C1N(CCCCS([O-])(=O)=O)c2ccc3ccccc3c2C1(C)C '
               'NAME: indocyanine green REASON: CORRECT Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: '
               'C(CCC)C[C@@H](/C=C/C=C\\C/C=C\\C/C=C\\CCCC(NCCS([O-])(=O)=O)=O)OO '
               'NAME: '
               'N-[15(S)-hydroperoxy-(5Z,8Z,11Z,13E)-icosatetraenoyl]taurine(1-) '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: [O-]S(C[C@@H](C(=O)[H])O)(=O)=O NAME: '
               'D-3-sulfolactaldehyde(1-) REASON: CORRECT Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: [H][N+]([H])(CCS([O-])(=O)=O)CC(N)=O NAME: '
               '2-[(2-amino-2-oxoethyl)ammonio]ethanesulfonate REASON: CORRECT '
               'Contains a sulfonate group (-SO3-) attached to a carbon chain '
               'or other groups\n'
               ' * SMILES: CC(C)S([O-])(=O)=O NAME: propane-2-sulfonate '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: OCC(O)CS([O-])(=O)=O NAME: 3-sulfopropanediol(1-) '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: [O-]C(=O)CS([O-])(=O)=O NAME: sulfonatoacetate '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: C(C(NCCS([O-])(=O)=O)=O)CCCCCCCCCCCCCCCCCCCCCC '
               'NAME: N-tetracosanoyltaurine(1-) REASON: CORRECT Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: CCCCS([O-])(=O)=O NAME: butane-1-sulfonate REASON: '
               'CORRECT Contains a sulfonate group (-SO3-) attached to a '
               'carbon chain or other groups\n'
               ' * SMILES: [O-]S(C[C@H](C(=O)CO)O)(=O)=O NAME: '
               '4-deoxy-4-sulfo-D-erythrulose(1-) REASON: CORRECT Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: CC(=O)NCCCS([O-])(=O)=O NAME: acamprosate(1-) '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: C(C(NCCS([O-])(=O)=O)=O)CCCCCCCCCCCCCCCCCCCCC NAME: '
               'N-tricosanoyltaurine(1-) REASON: CORRECT Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: [H]C(=O)CS([O-])(=O)=O NAME: sulfonatoacetaldehyde '
               'REASON: CORRECT Contains a sulfonate group (-SO3-) attached to '
               'a carbon chain or other groups\n'
               ' * SMILES: [H][N+](CCO)(CCO)CCS([O-])(=O)=O NAME: '
               '2-[bis(2-hydroxyethyl)ammonio]ethanesulfonate REASON: CORRECT '
               'Contains a sulfonate group (-SO3-) attached to a carbon chain '
               'or other groups\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(NCCS([O-])(=O)=O)=O '
               'NAME: N-arachidonoyltaurine(1-) REASON: CORRECT Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: [O-]S(C[C@H]([C@@H](O)C=O)O)(=O)=O NAME: '
               '4-deoxy-4-sulfo-D-erythrose(1-) REASON: CORRECT Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: CS([O-])(=O)=O NAME: methanesulfonate REASON: '
               'CORRECT Contains a sulfonate group (-SO3-) attached to a '
               'carbon chain or other groups\n'
               'False positives: SMILES: '
               '[H][N+]([H])(CCS([O-])(=O)=O)C(CO)(CO)CO NAME: '
               'N-tris(hydroxymethyl)methyl-2-ammonioethanesulfonate REASON: '
               'WRONGLY CLASSIFIED Contains a sulfonate group (-SO3-) attached '
               'to a carbon chain or other groups\n'
               ' * SMILES: [NH3+]CCCS([O-])(=O)=O NAME: 3-aminopropanesulfonic '
               'acid zwitterion REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               '[C@H]1(O)[C@H](O)O[C@H](CS([O-])(=O)=O)[C@H]([C@@H]1O)O NAME: '
               '6-sulfo-beta-D-quinovose(1-) REASON: WRONGLY CLASSIFIED '
               'Contains a sulfonate group (-SO3-) attached to a carbon chain '
               'or other groups\n'
               ' * SMILES: [Na+].OCCN1CCN(CC1)CCS([O-])(=O)=O NAME: sodium '
               '2-[4-(2-hydroxyethyl)piperazin-1-yl]ethanesulfonate REASON: '
               'WRONGLY CLASSIFIED Contains a sulfonate group (-SO3-) attached '
               'to a carbon chain or other groups\n'
               ' * SMILES: '
               'C1[C@H](C[C@@]2([C@](C1)([C@@]3([C@@]([C@@H]([C@H]2O)OS([O-])(=O)=O)([C@@]4([H])[C@@](CC3)(C)[C@](CC4)([C@@H](CCC(NCCS([O-])(=O)=O)=O)C)[H])[H])[H])C)[H])O '
               'NAME: tauro-alpha-muricholate 7-sulfate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains a sulfonate group (-SO3-) attached to a '
               'carbon chain or other groups\n'
               ' * SMILES: '
               '[H+].[H]C(=C([H])C1=[N+](CCCCS([O-])(=O)=O)c2ccc(cc2C1(C)C)C(O)=O)C1=C(Cl)C(CCC1)=C([H])C([H])=C1N(CCCCS([O-])(=O)=O)c2ccc(cc2C1(C)C)C(O)=O '
               'NAME: NIR-820 dye REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               'c1ccc(cc1)[S+](c1ccccc1)c1ccccc1.OC1C2CC3CC1CC(C3)(C2)OC(=O)C(F)(F)S([O-])(=O)=O '
               'NAME: triphenylsulfonium '
               '4-hydroxy-1-adamantyloxycarbonyldifluoromethanesulfonate '
               'REASON: WRONGLY CLASSIFIED Contains a sulfonate group (-SO3-) '
               'attached to a carbon chain or other groups\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)COC(=O)CCCCCCC(=O)N(C)CCS([O-])(=O)=O)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])C[C@H](C)C2=CC(=O)C=C[C@]12C '
               'NAME: methylprednisolone 21-suleptanic acid ester(1-) REASON: '
               'WRONGLY CLASSIFIED Contains a sulfonate group (-SO3-) attached '
               'to a carbon chain or other groups\n'
               ' * SMILES: '
               '[C@H]1(O)C(=O)O[C@H](CS([O-])(=O)=O)[C@H]([C@@H]1O)O NAME: '
               '6-deoxy-6-sulfoglucono-1,5-lactone(1-) REASON: WRONGLY '
               'CLASSIFIED Contains a sulfonate group (-SO3-) attached to a '
               'carbon chain or other groups\n'
               ' * SMILES: '
               'CN1c2ccccc2C(C)(C)\\C1=C/C=C/c1cc[n+](CCCS([O-])(=O)=O)c2ccccc12 '
               'NAME: dimethylindole red REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: CCCCCCCCCCCCCC[N+](C)(C)CCCS([O-])(=O)=O NAME: '
               'Zwittergent 3-14 REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               '[Na+].[Na+].[Na+].[H]C(=C([H])c1cc([o+]c2cc(ccc12)N(CCCS([O-])(=O)=O)CCCS([O-])(=O)=O)C(C)(C)C)C([H])=C1N(CCCC(O)=O)c2ccc(cc2C1(C)CCCS([O-])(=O)=O)S([O-])(=O)=O '
               'NAME: DY-634 REASON: WRONGLY CLASSIFIED Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(=O)NCCS([O-])(=O)=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@H](C2)OS([O-])(=O)=O '
               'NAME: taurolithocholic acid sulfate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains a sulfonate group (-SO3-) attached to a '
               'carbon chain or other groups\n'
               ' * SMILES: '
               '[Na+].[Na+].[Na+].[H]C(=C([H])c1cc([o+]c2cc3N(CCCS([O-])(=O)=O)C(C)(C)C=C(CS([O-])(=O)=O)c3cc12)-c1ccccc1)C([H])=C1N(CCCS([O-])(=O)=O)c2ccc(cc2C1(C)CCCC(O)=O)S([O-])(=O)=O '
               'NAME: DY-678 REASON: WRONGLY CLASSIFIED Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: '
               'S([O-])(=O)(=O)CCNC(=O)CC[C@H]([C@@]1([C@@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)(CC2)[H])[H])(CC1)[H])C)[H])C.[Na+] '
               'NAME: Sodium taurolithocholate REASON: WRONGLY CLASSIFIED '
               'Contains a sulfonate group (-SO3-) attached to a carbon chain '
               'or other groups\n'
               ' * SMILES: '
               '[Na+].[Na+].[Na+].[H]C(=C([H])C([H])=C1N(CCCS([O-])(=O)=O)c2ccc(cc2C1(C)CCCC(O)=O)S([O-])(=O)=O)C([H])=C([H])c1cc([o+]c2cc(ccc12)N(CCCS([O-])(=O)=O)CCCS([O-])(=O)=O)C(C)(C)C '
               'NAME: DY-734 REASON: WRONGLY CLASSIFIED Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(NCCS([O-])(=O)=O)=O)C)[H])C)O)[H])C '
               'NAME: tauroursocholate REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               'O.[Na+].CN(CS([O-])(=O)=O)c1c(C)n(C)n(-c2ccccc2)c1=O NAME: '
               'Sulpyrine REASON: WRONGLY CLASSIFIED Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: '
               '[H]C(C=C([H])C1=[N+](CCCCS([O-])(=O)=O)c2ccc(cc2C1(C)C)S([O-])(=O)=O)=CC([H])=C1N(CCCCS([O-])(=O)=O)c2ccc(cc2C1(C)C)C(O)=O '
               'NAME: NIR-4(2-) REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               '[C@@H]1(O)C(O)O[C@H](CS([O-])(=O)=O)[C@H]([C@@H]1O)O NAME: '
               '6-sulfo-D-rhamnose(1-) REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: '
               '[Na+].[Na+].[H]C(=C([H])c1cc([o+]c2cc3N(CCCS([O-])(=O)=O)C(C)(C)C=C(C)c3cc12)C(C)(C)C)C([H])=C1N(CCCS([O-])(=O)=O)c2ccc(cc2C1(C)CCCC(O)=O)S([O-])(=O)=O '
               'NAME: DY-652 REASON: WRONGLY CLASSIFIED Contains a sulfonate '
               'group (-SO3-) attached to a carbon chain or other groups\n'
               ' * SMILES: CS([O-])(=O)=O.C[n+]1ccccc1\\C=N\\O NAME: '
               'pralidoxime mesylate REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               ' * SMILES: CC(CCCCCCCCCCCC([C@@H]([NH3+])CS(=O)(=O)[O-])=O)C '
               'NAME: 2-amino-3-oxo-15-methylhexadecane-1-sulfonate REASON: '
               'WRONGLY CLASSIFIED Contains a sulfonate group (-SO3-) attached '
               'to a carbon chain or other groups\n'
               ' * SMILES: '
               '[Na+].O=S(=O)(C([C@H](C[C@H]1C(NCC1)=O)NC([C@H](CC(C)C)NC(=O)OC2CCN(CC2)C(=O)OC(C)(C)C)=O)O)[O-] '
               'NAME: '
               'Sodium;(2S)-1-hydroxy-2-[[(2S)-4-methyl-2-[[1-[(2-methylpropan-2-yl)oxycarbonyl]piperidin-4-yl]oxycarbonylamino]pentanoyl]amino]-3-[(3S)-2-oxopyrrolidin-3-yl]propane-1-sulfonate '
               'REASON: WRONGLY CLASSIFIED Contains a sulfonate group (-SO3-) '
               'attached to a carbon chain or other groups\n'
               ' * SMILES: '
               '[H]C(=C([H])C([H])=C1N(CCCS([O-])(=O)=O)c2ccc(cc2C1(C)CCCC(O)=O)S([O-])(=O)=O)C([H])=C([H])c1cc(c2ccc(cc2[o+]1)N(CC)CCCS([O-])(=O)=O)C(C)(C)C '
               'NAME: DY-782(2-) REASON: WRONGLY CLASSIFIED Contains a '
               'sulfonate group (-SO3-) attached to a carbon chain or other '
               'groups\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)C[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:1(13Z)/16:1(9Z)/18:4(6Z,9Z,12Z,15Z))',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'O1C2C(C3(C(C4C(C5(C(CC4)CC(OC6OC(C(OC7OC(C(O)C(O)C7O)C)C(O)C6O)COC8OC(C(O)C(O)C8O)CO)CC5)C)CC3)C2)C)C(C19OCC(CC9)C)C',
                                     'name': 'Desglucoparillin',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': '[C@H]1(O)C(O)O[C@H](C=O)[C@H]([C@@H]1O)O',
                                     'name': '6-dehydro-D-glucose',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'C1=CC(=CC=C1NC2=C(C=NC=C2)S(=O)(=O)N)Cl',
                                     'name': '4-(4-chloroanilino)-3-pyridinesulfonamide',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'C=1([NH+]=C(C=C(N1)NCC=2ON=C(N2)C(N)=O)C(C)C)N',
                                     'name': '2-amino-4-{[(3-carbamoyl-1,2,4-oxadiazol-5-yl)methyl]amino}-6-isopropylpyrimidin-1-ium',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]([C@@H]1O)CO)O)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO',
                                     'name': '(2R,3S,4S,5S,6R)-2-[(2S,3R,4S,5S,6R)-2,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-4-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)S(=O)(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@@H](O[C@@H]4CO)CC(=O)O',
                                     'name': '2-[(1R,3R,4aS,9aR)-1-(hydroxymethyl)-6-[(4-methoxyphenyl)sulfonylamino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]acetic '
                                             'acid',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'O=C(C=1NC=CC1)[C@@H]2[C@@H](C=C[C@H]3[C@H]2CCC3)C=CC=C([C@@H]4O[C@@H]([C@H](C(=O)O)C)CC[C@@H]4C)CC',
                                     'name': 'A83094A',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'C[C@H](O)[C@H](O)[C@@H](O)C(=O)COP(O)(O)=O',
                                     'name': 'L-rhamnulose 1-phosphate',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'},
                                 {   'smiles': 'COc1ccc(\\C=C\\C(=O)N[C@H](CCCNC(N)=N)C(O)=O)cc1Br',
                                     'name': 'subereamine A',
                                     'reason': 'No sulfonate group (-SO3-) '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C(=C/[C@H](C/C=C\\CCCCC)OO)\\C=C/C/C=C\\CCCC(=O)NCCS([O-])(=O)=O',
                                      'name': 'N-[12(S)-hydroperoxy-(5Z,8Z,10E,14Z)-icosatetraenoyl]taurine(1-)',
                                      'reason': 'Molecule contains invalid '
                                                'functional group: [C]=[C]'},
                                  {   'smiles': '[Na+].[H]C(=C([H])C([H])=C([H])C1=[N+](CCCCS([O-])(=O)=O)c2ccc3ccccc3c2C1(C)C)C([H])=C([H])C([H])=C1N(CCCCS([O-])(=O)=O)c2ccc3ccccc3c2C1(C)C',
                                      'name': 'indocyanine green',
                                      'reason': 'Molecule contains invalid '
                                                'functional group: [c]'},
                                  {   'smiles': 'C(CCC)C[C@@H](/C=C/C=C\\C/C=C\\C/C=C\\CCCC(NCCS([O-])(=O)=O)=O)OO',
                                      'name': 'N-[15(S)-hydroperoxy-(5Z,8Z,11Z,13E)-icosatetraenoyl]taurine(1-)',
                                      'reason': 'Molecule contains invalid '
                                                'functional group: [C]=[C]'},
                                  {   'smiles': 'C(CCC)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(NCCS([O-])(=O)=O)=O',
                                      'name': 'N-arachidonoyltaurine(1-)',
                                      'reason': 'Molecule contains invalid '
                                                'functional group: [C]=[C]'}],
    'attempt': 3,
    'reasoning': 'The previous code had a high number of false positives, '
                 'indicating that the classification criteria were too broad. '
                 'The main issue was that the code only checked for the '
                 'presence of a sulfonate group attached to a carbon atom, '
                 'without considering the broader context of the molecule. '
                 'This led to the misclassification of molecules that '
                 'contained sulfonate groups but were not alkanesulfonate '
                 'oxoanions.\n'
                 '\n'
                 'To improve the classification, we need to refine the '
                 'criteria to ensure that the sulfonate group is part of an '
                 'alkanesulfonate structure. This can be done by:\n'
                 '\n'
                 '1. **Ensuring the sulfonate group is attached to a carbon '
                 'chain**: We should check that the carbon attached to the '
                 'sulfonate group is part of a chain or a simple alkyl group, '
                 'rather than being part of a complex structure like a ring or '
                 'a conjugated system.\n'
                 '\n'
                 '2. **Excluding complex structures**: We should exclude '
                 'molecules where the sulfonate group is part of a more '
                 'complex structure, such as a ring or a conjugated system, '
                 'which are not typical of alkanesulfonate oxoanions.\n'
                 '\n'
                 '3. **Checking for additional functional groups**: We should '
                 'ensure that the molecule does not contain other functional '
                 'groups that would disqualify it from being an '
                 'alkanesulfonate oxoanion.\n'
                 '\n'
                 'Here is the revised code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 29,
    'num_false_positives': 77,
    'num_true_negatives': 142190,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.27358490566037735,
    'recall': 0.8787878787878788,
    'f1': 0.4172661870503597,
    'accuracy': 0.9994307800421645,
    'negative_predictive_value': 0.9999718694178376}