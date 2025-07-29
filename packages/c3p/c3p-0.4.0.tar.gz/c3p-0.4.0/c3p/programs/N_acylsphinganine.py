"""
Classifies: CHEBI:31488 N-acylsphinganine
"""
"""
Classifies: N-acylsphinganine
A ceramide consisting of sphinganine in which one of the amino hydrogens 
is substituted by a fatty acyl group.
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_N_acylsphinganine(smiles: str):
    """
    Determines if a molecule is an N-acylsphinganine based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-acylsphinganine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Core structural requirements:
    # 1. Strict sphinganine core with correct stereochemistry
    # [C@H] and [C@@H] enforce specific stereochemistry
    # No double bonds in the core (distinguishes from sphingosine)
    sphinganine_core = Chem.MolFromSmarts("[CH2X4][C@H]([OX2H1])[C@H]([NX3H1])[CH2X4][OX2H1]")
    if not mol.HasSubstructMatch(sphinganine_core):
        return False, "Missing characteristic sphinganine core structure with correct stereochemistry"

    # 2. N-acyl group (amide) directly attached to the sphinganine core
    amide_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[#6]")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    
    # Check if any amide is properly connected to the sphinganine nitrogen
    valid_amide = False
    for match in amide_matches:
        amide_c = mol.GetAtomWithIdx(match[0])
        for neighbor in amide_c.GetNeighbors():
            if neighbor.GetAtomicNum() == 7:  # Nitrogen
                valid_amide = True
                break
    if not valid_amide:
        return False, "No N-acyl group properly connected to sphinganine core"

    # 3. Verify no extra hydroxyl groups on the core
    # (distinguishes from phytosphingosine which has an extra OH)
    core_carbons = mol.GetSubstructMatches(sphinganine_core)[0]
    for c_idx in core_carbons:
        carbon = mol.GetAtomWithIdx(c_idx)
        oh_count = sum(1 for n in carbon.GetNeighbors() 
                      if n.GetAtomicNum() == 8 and n.GetTotalNumHs() == 1)
        if carbon.GetHybridization() == Chem.HybridizationType.SP3 and oh_count > 1:
            return False, "Extra hydroxyl groups found on core (might be phytosphingosine)"

    # 4. Check for long alkyl chains
    # One attached to the amide (fatty acyl) and one as the sphinganine tail
    alkyl_chain = Chem.MolFromSmarts("[CX4][CX4][CX4][CX4][CX4][CX4]")
    chain_matches = len(mol.GetSubstructMatches(alkyl_chain))
    if chain_matches < 2:
        return False, "Missing required long alkyl chains"

    # 5. Basic composition checks
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)

    if c_count < 16:
        return False, f"Too few carbons ({c_count}) for N-acylsphinganine"
    if n_count != 1:
        return False, f"Must have exactly 1 nitrogen, found {n_count}"
    if o_count < 3:
        return False, f"Must have at least 3 oxygens, found {o_count}"

    # 6. Check for unsaturation in the core region
    # (to distinguish from sphingosine derivatives)
    double_bond = Chem.MolFromSmarts("C=C")
    if mol.HasSubstructMatch(double_bond):
        # Check if double bond is in the core region
        db_matches = mol.GetSubstructMatches(double_bond)
        core_atoms = set(mol.GetSubstructMatches(sphinganine_core)[0])
        for match in db_matches:
            if match[0] in core_atoms or match[1] in core_atoms:
                return False, "Contains double bond in core region (might be sphingosine derivative)"

    # The molecule passed all tests
    base_reason = "Valid N-acylsphinganine with correct core structure and stereochemistry"
    
    # Note if it's a glycosylated variant
    sugar_pattern = Chem.MolFromSmarts("[CH1,2]1[OH1,CH2][CH1][CH1][CH1][OH1,CH2]1")
    if mol.HasSubstructMatch(sugar_pattern):
        return True, base_reason + " (glycosylated variant)"
    
    return True, base_reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:31488',
                          'name': 'N-acylsphinganine',
                          'definition': 'A ceramide consisting of sphinganine '
                                        'in which one of the amino hydrogens '
                                        'is substituted by a fatty acyl group.',
                          'parents': ['CHEBI:139048', 'CHEBI:82829'],
                          'xrefs': ['KEGG:C12126', 'LIPID_MAPS_class:LMSP0202'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.40476190476190477 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-octacosanoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCCCC NAME: '
               'N-tetradecanoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)C(O)CCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyhexadecanoyl)sphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: D-galactosyl-N-tetracosanoylsphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-tetracosanoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyhexacosanoyl)sphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxydocosanoyl)sphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               '[C@]([C@@](CCCCCCCCCCCCCCC)(O)[H])(NC(=O)CCCCCCCCCCCCCC)([H])CO '
               'NAME: Cer(d18:0/15:0) REASON: CORRECT Contains sphinganine '
               'core with N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-eicosanoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC '
               'NAME: alpha-D-galactosyl-N-tetradecanoylsphinganine REASON: '
               'CORRECT Contains sphinganine core with N-acyl group and '
               'required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-triacontanoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-(11Z)-icosenoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(CCCCCCCCCCC/C=C\\CCCCCCCC)=O '
               'NAME: N-(13Z-docosenoyl)-sphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)[C@H](O)CCCCCCCCCCC '
               'NAME: '
               '1-alpha-D-glucuronosyl-N-[(2R)-2-hydroxytridecanoyl]sphinganine '
               'REASON: CORRECT Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyeicosanoyl)sphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: D-glucosyl-N-tetracosanoylsphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               "NAME: beta-D-glucosyl-(1<->1')-N-octadecanoylsphinganine "
               'REASON: CORRECT Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)C(O)CCCCCCCCCCCC NAME: '
               'N-(2-hydroxytetradecanoyl)sphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: N-[(15Z)-tetracosenoyl]sphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCCCC '
               'NAME: D-galactosyl-N-hexadecanoylsphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC NAME: '
               'N-octodecanoylsphinganine REASON: CORRECT Contains sphinganine '
               'core with N-acyl group and required hydroxyl groups\n'
               ' * SMILES: CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCC '
               'NAME: N-dodecanoylsphinganine REASON: CORRECT Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: 1-O-(alpha-D-galactopyranosyl)-N-hexacosanoylsphinganine '
               'REASON: CORRECT Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxytriacontanoyl)sphinganine REASON: CORRECT '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O)NC(=O)CCCCCCCCCCCCC '
               'NAME: '
               '1-O-(alpha-D-glucopyranuronosyl)-N-tetradecanoyldihydrosphingosine '
               'REASON: CORRECT Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               'False positives: SMILES: '
               'O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCC)=O '
               'NAME: 1-O-(alpha-D-galactosyl)-N-undecanoylphytosphingosine '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'C(CCCCCCCCCCCCCCC)(=O)N[C@H]([C@@H](/C=C/CCCCCCCCC(CC)C)O)CO '
               'NAME: N-hexadecanoyl-14-methylhexadecasphingosine REASON: '
               'WRONGLY CLASSIFIED Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCCCC=2C=CC(=CC2)C(C)(C)C)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O '
               'NAME: '
               '1-O-{4-O-[3-(4-tert-butylphenyl)propyl]-alpha-D-galactosyl}-N-hexacosanoylphytosphingosine '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCC)\\C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)CCCCCCCCCCCCCC/C=C\\CCCCCC '
               'NAME: Catacerebroside A REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyhexacosanoyl)eicosasphinganine REASON: '
               'WRONGLY CLASSIFIED Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCCCC '
               'NAME: N-(tetracosanoyl)eicosasphinganine REASON: WRONGLY '
               'CLASSIFIED Contains sphinganine core with N-acyl group and '
               'required hydroxyl groups\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO)[C@@H]2O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO '
               'NAME: '
               'N-[(2S,3R,4S,5R)-4-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-1,3,5,6-tetrahydroxyhexan-2-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               '[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(CO[C@@H]1O[C@@H]([C@@H]([C@@H]([C@H]1O)OS(=O)(=O)O)O)CO)NC([C@H](O)CCCCCCCCCCCCCCCCCCCCCC)=O '
               'NAME: '
               '1-(3-O-sulfo-beta-D-galactosyl)-N-[(2R)-2-hydroxylignoceroyl]sphingosine '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)CCCCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxydocosanoyl)eicosasphinganine REASON: WRONGLY '
               'CLASSIFIED Contains sphinganine core with N-acyl group and '
               'required hydroxyl groups\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\CCCC(=O)NCCO)/C=C/[C@@H](O)CCCCC '
               'NAME: PGE2 ethanolamide REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'O1[C@@H]2[C@@](O)(C[C@H](NC(=O)/C=C/C=C/C=C/[C@@H](C[C@@H](C/C(=C/[C@@H](CC)C)/C)C)C)CO)C(=O)C=C[C@H]12 '
               'NAME: (+)-scyphostatin REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OCC(NC(=O)C(O)CCCCCCCCCCCCCC)C(O)/C=C/CCCCCCCCCCCCC)CO '
               'NAME: AS 1-5 REASON: WRONGLY CLASSIFIED Contains sphinganine '
               'core with N-acyl group and required hydroxyl groups\n'
               ' * SMILES: O=C(N[C@@H](CO)C)C1OC1CC/C=C/CCCCCCCCCCCCC NAME: '
               'Besarhanamide A REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OCC(NC(=O)C(O)CCCCCCCCCCCC)C(O)/C=C/CC/C=C/CCCCCCCCCC)CO '
               'NAME: Lucyobroside REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCCCC '
               "NAME: beta-D-galactosyl-(1<->1')-N-hexadecanoylsphinganine "
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)/C=C/CC\\C=C(\\CCCCCCCCC)/C)CO '
               'NAME: Cerebroside B REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O)NC(=O)[C@H](O)CCCCCCCCCCCCCCCCC '
               'NAME: alpha-glucuronosylceramide REASON: WRONGLY CLASSIFIED '
               'Contains sphinganine core with N-acyl group and required '
               'hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)C(O)CCCCCCCCCCCCCCCC '
               'NAME: N-(2-hydroxyoctadecanoyl)eicosasphinganine REASON: '
               'WRONGLY CLASSIFIED Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@H](OC[C@H]2O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H](O)[C@@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3OC4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO)[C@@H]2O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO '
               'NAME: '
               'N-[(2S,3R,4S,5R)-4-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-4-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-1,3,5,6-tetrahydroxyhexan-2-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCCCCC)\\C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)CCCCCCCCCCCCC '
               'NAME: Allantoside REASON: WRONGLY CLASSIFIED Contains '
               'sphinganine core with N-acyl group and required hydroxyl '
               'groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCC '
               'NAME: Man-beta1-6-Ins-1-P-Cer(t18:0/2,3-OH-24:0) REASON: '
               'WRONGLY CLASSIFIED Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               ' * SMILES: '
               'S(OC1[C@@H](O)[C@H](O[C@@H](OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)C1O)CO)(O)(=O)=O '
               "NAME: (3'-SulfO)galbeta-cer(D18:1/20:0) REASON: WRONGLY "
               'CLASSIFIED Contains sphinganine core with N-acyl group and '
               'required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCNC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: N-arachidonoyl-1-oleoyl-sn-glycero-3-phosphoethanolamine '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: N-tetracosanoyl-4-hydroxy-15-methylhexadecasphinganine '
               'REASON: WRONGLY CLASSIFIED Contains sphinganine core with '
               'N-acyl group and required hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: beta-D-galactosyl-N-octadecanoylsphingosine REASON: '
               'WRONGLY CLASSIFIED Contains sphinganine core with N-acyl group '
               'and required hydroxyl groups\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'Cc1cc(C)c2Cc3c(C)cc(C)c(Cc4c(C)cc(C)c(Cc5c(C)cc(C)c(Cc1c2C)c5C)c4C)c3C',
                                     'name': '4,6,10,12,16,18,22,24,25,26,27,28-dodecamethylcalix[4]arene',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'O=C1C(=C2C=C3[C@]([C@@H](C(C)C)[C@@H]([C@H]3O)OC(=O)C)(C)CC[C@]2(C)CC1)COC(=O)C',
                                     'name': 'Dahliane E',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Glu-Thr-Leu',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'CCOc1ccc(NC(=O)C(C)O)cc1',
                                     'name': 'p-Lactophenetide',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@@H](O)[C@H]([C@H]4OC)O)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=CC=C7',
                                     'name': "3'-epi-5'-methoxy-K252d",
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'O=C(OC1C(O)C(OC(C1O)CO)OCC2OC(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(O)C(C2O)O)CCCCCCCCCCCCCCC',
                                     'name': '[(2S)-2-hexadecanoyloxy-3-[(2S,3R,4S,5S,6R)-6-[[(2S,3R,4S,5S,6R)-4-hexadecanoyloxy-3,5-dihydroxy-6-(hydroxymethyl)tetrahydropyran-2-yl]oxymethyl]-3,4,5-trihydroxy-tetrahydropyran-2-yl]oxy-propyl] '
                                             '(9E,12E,15E)-octadeca-9,12,15-trienoate',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C=C2C(=O)C3=C1[C@@H]([C@@H](O)[C@]([C@@H]3O)(O)C)C',
                                     'name': 'Altersolanol G',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(=O)CO)C([O-])=O)[C@H](O)[C@H](O)CO',
                                     'name': 'N-glycoloyl-alpha-neuraminate',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\CCC(O)=O',
                                     'name': '10,11-DiHDPE',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'},
                                 {   'smiles': '[Na+].[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C([O-])=O',
                                     'name': 'cephalexin sodium',
                                     'reason': 'Missing characteristic '
                                               'sphinganine core structure '
                                               'with correct stereochemistry'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC',
                                      'name': 'D-galactosyl-N-tetracosanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC',
                                      'name': 'alpha-D-galactosyl-N-tetradecanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)[C@H](O)CCCCCCCCCCC',
                                      'name': '1-alpha-D-glucuronosyl-N-[(2R)-2-hydroxytridecanoyl]sphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COC1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC',
                                      'name': 'D-glucosyl-N-tetracosanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC',
                                      'name': "beta-D-glucosyl-(1<->1')-N-octadecanoylsphinganine",
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC[C@@H](O)[C@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCCCC',
                                      'name': 'D-galactosyl-N-hexadecanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC',
                                      'name': '1-O-(alpha-D-galactopyranosyl)-N-hexacosanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO[C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O)NC(=O)CCCCCCCCCCCCC',
                                      'name': '1-O-(alpha-D-glucopyranuronosyl)-N-tetradecanoyldihydrosphingosine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)C[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC',
                                      'name': '1-O-(3-deoxy-alpha-D-galactopyranosyl)-N-hexacosanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct stereochemistry'},
                                  {   'smiles': 'O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)COC(=O)CCC=2C=CC=CC2)O)O)O)C[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O',
                                      'name': '1-O-[6-O-(3-phenylpropanoyl)-alpha-D-galactopyranosyl]-N-hexacosanoylsphinganine',
                                      'reason': 'Missing characteristic '
                                                'sphinganine core structure '
                                                'with correct '
                                                'stereochemistry'}],
    'attempt': 3,
    'reasoning': 'Looking at the outcomes, the main issue is that the program '
                 "has too many false positives - it's incorrectly classifying "
                 'many related compounds as N-acylsphinganines. The key issues '
                 'appear to be:\n'
                 '\n'
                 "1. The program isn't strict enough about the sphinganine "
                 "core structure. It's accepting molecules with similar "
                 'features (like sphingosine derivatives that have double '
                 "bonds) but aren't true sphinganines.\n"
                 '\n'
                 '2. The pattern matching is too permissive, especially around '
                 'stereochemistry. N-acylsphinganines have specific '
                 'stereochemistry that should be enforced.\n'
                 '\n'
                 "3. The program doesn't properly distinguish between "
                 'sphinganine and related compounds like phytosphingosine '
                 '(which has an extra OH group).\n'
                 '\n'
                 "Here's an improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 24,
    'num_false_positives': 41,
    'num_true_negatives': 142225,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.36923076923076925,
    'recall': 0.7058823529411765,
    'f1': 0.4848484848484848,
    'accuracy': 0.9996416022487702,
    'negative_predictive_value': 0.9999296938165712}