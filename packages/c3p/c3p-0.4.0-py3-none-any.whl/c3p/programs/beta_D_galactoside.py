"""
Classifies: CHEBI:28034 beta-D-galactoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_beta_D_galactoside(smiles: str):
    """
    Determines if a molecule is a beta-D-galactoside based on its SMILES string.
    A beta-D-galactoside contains a D-galactose ring with beta-configuration at its anomeric center.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-D-galactoside, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a SMARTS pattern for the D-galactose pyranose ring (without specifying anomeric configuration)
    galactose_ring_pattern = Chem.MolFromSmarts("O[C@H]1[C@@H](O)[C@@H](O)[C@H](CO)O[C@@H]1*")
    matches = mol.GetSubstructMatches(galactose_ring_pattern)
    if not matches:
        return False, "No D-galactose ring found"
    
    # Iterate over the matches and check for beta anomeric configuration
    for match in matches:
      # The first atom in the pattern is the ring oxygen.
      ring_oxygen = match[0]
      # The carbon attached to the ring oxygen is at index 1 in the pattern
      anomeric_carbon = match[1]
      
      # Get the RDKit atom object from the index
      anomeric_carbon_atom = mol.GetAtomWithIdx(anomeric_carbon)

      #Get the chiral tag for the anomeric carbon atom. If the carbon is not chiral it returns a non-chiral tag.
      chiral_tag = anomeric_carbon_atom.GetChiralTag()

      if chiral_tag == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
          # It is beta
          return True, "Contains a beta-D-galactoside moiety"
          
    return False, "Not a beta-D-galactoside, based on anomeric carbon stereochemistry"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28034',
                          'name': 'beta-D-galactoside',
                          'definition': 'Any D-galactoside having '
                                        'beta-configuration at its anomeric '
                                        'centre.',
                          'parents': ['CHEBI:20961'],
                          'xrefs': ['KEGG:C00602'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 27,
                           'log_lines_of_code': 3.295836866004329,
                           'indent_by_line': [   1,
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
                                                 0,
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
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 4,
                           'smarts_strings': [   'O[C@H]1[C@@H](O)[C@@H](O)[C@H](CO)O[C@@H]1*'],
                           'smarts_strings_count': 1,
                           'defs': ['is_beta_D_galactoside(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No D-galactose ring found"',
                                          'False, "Not a beta-D-galactoside, '
                                          'based on anomeric carbon '
                                          'stereochemistry"'],
                           'returns_count': 3,
                           'complexity': 2.659167373200866},
    'message': '\n'
               'Attempt failed: F1 score of 0.005999347896967721 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C(/C=C/C1=CC=C(C=C1)O)(=O)C(O)[C@@H](O)CO[C@H]2[C@H](O)[C@@H](O)[C@@H](O)[C@H](O2)CO '
               'NAME: coumaroyl 3-beta-D-galactosyl-sn-glycerol REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)cc2)c(O)c3=O)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: kaempferol 7-O-beta-D-galactopyranoside REASON: CORRECT '
               'Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H](O)[C@H]([C@H](O1)CO)O)O)OC=2C=CC=3C=C(C=CC3C2)Br '
               'NAME: 6-bromo-2-naphthyl beta-D-galactoside REASON: CORRECT '
               'Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc3c(O)cc(O)cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](OC(=O)c2cc(O)c(O)c(O)c2)[C@@H](O)[C@H]1O '
               "NAME: cyanidin 3-O-(2''-O-galloyl-beta-D-galactopyranoside) "
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](OC(O)[C@@H]1O)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Galp-(1->3)-D-Galp REASON: CORRECT Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@@H]1O[C@H](COC(=O)CCCCCCCCC)[C@H](O)[C@H](O)[C@H]1O)[C@H](C)CCCC(C)C '
               'NAME: cholesteryl 6-O-decanoyl-beta-D-galactoside REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'CCSSCCCCCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](OC)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: methyl '
               '6-O-[15-(ethyldisulfanyl)pentadecanoyl]-beta-D-galactoside '
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[H][C@]1(O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)Oc1c[nH]c2ccc(Br)c(Cl)c12 '
               'NAME: 5-bromo-4-chloro-3-indolyl beta-D-galactoside REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O=C(C)OC[C@@H]1[C@@H]([C@@H]([C@H]([C@H](OC)O1)O)O)OC(C)=O '
               'NAME: methyl 4,6-di-O-acetyl-beta-D-galactoside REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H](O[C@@H]1CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: beta-D-Galp-(1->3)-[beta-D-Glcp-(1->4)]-beta-D-Glcp '
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O NAME: '
               'methyl beta-D-galactoside REASON: CORRECT Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'CCSSCCCCCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](Oc2ccccc2)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: phenyl '
               '6-O-[15-(ethyldisulfanyl)pentadecanoyl]-beta-D-galactoside '
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@@H]1O[C@H](COC(=O)CCCCC)[C@H](O)[C@H](O)[C@H]1O)[C@H](C)CCCC(C)C '
               'NAME: cholesteryl 6-O-hexanoyl-beta-D-galactoside REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)CO)[C@@H]2[C@@H](O)C(OC[C@H]2O)O '
               'NAME: beta-D-Galp-(1->3)-D-Xylp REASON: CORRECT Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)cc2)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: kaempferol 3-O-beta-D-galactoside REASON: CORRECT '
               'Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@@H]1O[C@H](COC(C)=O)[C@H](O)[C@H](O)[C@H]1O)[C@H](C)CCCC(C)C '
               'NAME: cholesteryl 6-O-acetyl-beta-D-galactoside REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(O)=O)O)OS(=O)(=O)O)O)O)C=3C=CC(=CC3)CCNC(CCCS)=O '
               'NAME: '
               'beta-D-GlcA3S-(1->3)-beta-D-Gal-OC6H4-4-[CH2]2NHC(O)[CH2]3SH '
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(O)=O)O)O)O)O)C=3C=CC(=CC3)OC '
               'NAME: beta-D-GlcA-(1->3)-beta-D-Gal-OC6H4-4-OMe REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O1[C@H]([C@H](NC(=O)C)[C@@H](O)CC1(O)C(O)=O)[C@H](O)[C@H](O)CO[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Galp-(1->9)-Neup5Ac REASON: CORRECT Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'Nc1nc2n(cc(CN[C@H]3C=C[C@H](O)[C@@H]3O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)c2c(=O)[nH]1)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O '
               "NAME: O-5''-beta-D-galactosylqueuosine REASON: CORRECT "
               'Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@@H]1O[C@H](COC(=O)CCCCCCCCCCCCCCC)[C@H](O)[C@H](O)[C@H]1O)[C@H](C)CCCC(C)C '
               'NAME: cholesteryl 6-O-palmitoyl-beta-D-galactoside REASON: '
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'CC\\C=C/CC1C(CCCCCCCC(=O)OC[C@H](CO[C@@H]2O[C@H](CO[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H](O)[C@H]2O)OC(=O)CCCCCCCC2C=CC(=O)C2C\\C=C/CC)C=CC1=O '
               'NAME: arabidopside D REASON: CORRECT Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O[C@H]1[C@@H](COC(=O)c2ccc(O)cc2)O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)c(O)c2)[C@H](O)[C@H]1O '
               "NAME: quercetin 3-(6''-p-hydroxybenzoylgalactoside) REASON: "
               'CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](OC(O)[C@H](NC(=O)C)[C@H]1O)CO[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: beta-D-Galp-(1->4)-[beta-D-Glcp-(1->6)]-D-GlcpNAc '
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)OP(O[C@@](CO)(CO)[H])(O)=O)O[C@H]2[C@@H]([C@@H]([C@H]([C@@H](O2)C)O)O)O)OC '
               'NAME: methyl '
               'alpha-L-rhamnosyl-(1->2)-3-(2-glycerylphospho)-beta-D-galactoside '
               'REASON: CORRECT Contains a beta-D-galactoside moiety\n'
               'False positives: SMILES: '
               'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               '[H][C@@]12CC(C)(C)C[C@@H](O)[C@]1(C)CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C(O)=O)[C@](C)(CO)[C@]3([H])CC[C@@]12C '
               'NAME: soyasapogenol B 3-O-beta-glucuronide REASON: WRONGLY '
               'CLASSIFIED Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O1[C@@H](OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1CO '
               'NAME: beta-D-Galp-(1->6)-beta-D-GlcpNAc REASON: WRONGLY '
               'CLASSIFIED Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@H]2[C@@H](O[C@H](CO)[C@H](O)[C@@H]2O[C@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)O[C@@H]2[C@H](O)[C@@H](O)[C@H](O)O[C@@H]2CO)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-D-GalpNAc-(1->3)-[alpha-L-Fucp-(1->2)]-beta-D-Galp-(1->4)-beta-D-Galp '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O)[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@H](O)[C@H]5O)CO)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@@H]6O)CO)[C@H](O)[C@H]3NC(=O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-5-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5R)-3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'CC(=O)NC1C(O)C(OC2OC(CO)C(O)C(OC3OC(CO)C(O)C(OC4OC(CO)C(O)C(O)C4O)C3NC(C)=O)C2O)C(CO)OC1OC1C(O)C(CO)OC(OC2C(O)C(O)C(O)OC2CO)C1O '
               'NAME: '
               'beta-D-galactopyranosyl-(1->3)-2-acetamido-2-deoxy-beta-D-glucopyranosyl-(1->3)-beta-D-galactopyranosyl-(1->4)-2-acetamido-2-deoxy-beta-D-glucopyranosyl-(1->3)-beta-D-galactopyranosyl-(1->4)-D-glucopyranose '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@H]1OC=2C=C3C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)=CC(O)=CC3=[O+]C2C5=CC(OC)=C(O)C=C5)COC(=O)C=CC6=CC(O)=C(O)C=C6)[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)COC(=O)C=CC8=CC(OC)=C(O)C=C8 '
               'NAME: Peonidin-3-caffeoyl-feruloyl sophoroside-5-glucoside '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O(C=1C=CC(=CC1OC)[C@H]2OC3=CC(=CC(=C3C(C2)=O)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)[C@@H]5OC[C@@]([C@@]5([H])O)(CO)O '
               'NAME: viscumneoside I REASON: WRONGLY CLASSIFIED Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO '
               'NAME: CID 91850566 REASON: WRONGLY CLASSIFIED Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O(C1C(OC(=O)/C=C/C2=CC(OC)=C(O)C=C2)C(OC(OCCC3=CC(O)=C(OC)C=C3)C1O)CO)C4OC(C(O)C(O)C4OC5OCC(O)C(O)C5O)C '
               'NAME: Leonoside B REASON: WRONGLY CLASSIFIED Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O1C23C(O)(C4(CC1(O)C(C2=O)(C(=CC4=O)C(COC5OC(C(O)C(O)C5O)CO)C)C)C)CCC(C3O)C '
               'NAME: Cinncassiol C1 19-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains a beta-D-galactoside moiety\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1OC(C2=CC=CC=C2)C#N)CO NAME: '
               '(S)-2-Hydroxy-2-phenylacetonitrile O-b-D-allopyranoside '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@@H]3O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@@H]6O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O)CO)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=C(O)C=C(C=C2)/C=C\\C3=CC(O)=CC(O)=C3)CO '
               "NAME: Piceatannol 4'-glucoside REASON: WRONGLY CLASSIFIED "
               'Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O1C2(C3(C(C4(C(CC3=O)C(O)(C)C)C(O)CC(OC4)=O)CCC2(C(OC5OC(C(O)C(O)C5O)CO)C=6C=COC6)C)C)C1C(O)=O '
               'NAME: Ichangic acid 17-beta-D-glucopyranoside REASON: WRONGLY '
               'CLASSIFIED Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O1[C@@H](O[C@@H]2[C@@](O)(C[C@@H](N[C@@H]3C=C([C@@H](O)[C@H]([C@H]3O)O)CO)[C@H]([C@H]2O)O)CO)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O '
               'NAME: Validamycin G REASON: WRONGLY CLASSIFIED Contains a '
               'beta-D-galactoside moiety\n'
               ' * SMILES: O1C(C(O)C(O)C(O)C1O)CO NAME: hexopyranose REASON: '
               'WRONGLY CLASSIFIED Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O)[C@H]3NC(=O)C)CO)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H]9O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-5-[(2S,3R,4S,5S,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3CO[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)C)O)O[C@@H]([C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@@H]5O)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5S,6R)-2-[(2S,3S,4S,5R,6R)-2-[(2R,3S,4R,5R,6R)-5-acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-4,6-dihydroxy-2-[[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-4-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O1[C@@H](OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2O)[C@H](NC(=O)C)[C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O)[C@H]1CO '
               'NAME: '
               'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-2,5-dihydroxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(=O)CO)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(C)=O)[C@H](O)O[C@@H]2CO)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO '
               'NAME: alpha-Neup5Gc-(2->3)-beta-D-Galp-(1->4)-beta-D-GlcNAcp '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-[[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a beta-D-galactoside '
               'moiety\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)cc2)c(O)c3=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: kaempferol 7-O-beta-D-glucopyranoside REASON: WRONGLY '
               'CLASSIFIED Contains a beta-D-galactoside moiety\n'
               ' * SMILES: '
               '[H][C@]12COC(=O)[C@]1([H])[C@H](C1=CC(OC)=C(O)C(OC)=C1)C1=C(C=C3OCOC3=C1)[C@H]2O[C@@H]1O[C@]2([H])CO[C@]([H])(O[C@@]2([H])[C@H](O)[C@H]1O)C1=CC=CS1 '
               'NAME: teniposide REASON: WRONGLY CLASSIFIED Contains a '
               'beta-D-galactoside moiety\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No D-galactose ring found'},
                                 {   'smiles': 'CC(C(=O)NN=C(C1=CC=CC=C1)C2=CC=CC=C2)NC3CCCCC3',
                                     'name': '2-(cyclohexylamino)-N-[(diphenylmethylene)amino]propanamide',
                                     'reason': 'No D-galactose ring found'}],
    'sample_false_negatives': [   {   'smiles': 'C(/C=C/C1=CC=C(C=C1)O)(=O)C(O)[C@@H](O)CO[C@H]2[C@H](O)[C@@H](O)[C@@H](O)[C@H](O2)CO',
                                      'name': 'coumaroyl '
                                              '3-beta-D-galactosyl-sn-glycerol',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)cc2)c(O)c3=O)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'kaempferol '
                                              '7-O-beta-D-galactopyranoside',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](Oc2cc3c(O)cc(O)cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](OC(=O)c2cc(O)c(O)c(O)c2)[C@@H](O)[C@H]1O',
                                      'name': 'cyanidin '
                                              "3-O-(2''-O-galloyl-beta-D-galactopyranoside)",
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'CCSSCCCCCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](OC)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'methyl '
                                              '6-O-[15-(ethyldisulfanyl)pentadecanoyl]-beta-D-galactoside',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'O=C(C)OC[C@@H]1[C@@H]([C@@H]([C@H]([C@H](OC)O1)O)O)OC(C)=O',
                                      'name': 'methyl '
                                              '4,6-di-O-acetyl-beta-D-galactoside',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'CCSSCCCCCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](Oc2ccccc2)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'phenyl '
                                              '6-O-[15-(ethyldisulfanyl)pentadecanoyl]-beta-D-galactoside',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)cc2)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'kaempferol '
                                              '3-O-beta-D-galactoside',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'O[C@H]1[C@@H](COC(=O)c2ccc(O)cc2)O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)c(O)c2)[C@H](O)[C@H]1O',
                                      'name': 'quercetin '
                                              "3-(6''-p-hydroxybenzoylgalactoside)",
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](Oc2cc3c(O)cc(O)cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](O)[C@@H](O)[C@H]1O',
                                      'name': 'cyanidin 3-O-beta-D-galactoside',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'},
                                  {   'smiles': 'O1[C@@H](O[C@H]([C@@H](NC(=O)C)CO)[C@H](O)[C@H](O)CO)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1CO',
                                      'name': '2-acetamido-2-deoxy-3-O-beta-D-galactopyranosyl-D-glucitol',
                                      'reason': 'Not a beta-D-galactoside, '
                                                'based on anomeric carbon '
                                                'stereochemistry'}],
    'attempt': 2,
    'reasoning': "Okay, let's analyze the previous attempt and the results to "
                 'figure out how to improve the `is_beta_D_galactoside` '
                 'function.\n'
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 '1.  **The Core Issue:** The main problem is that the '
                 'previous code was too strict in its definition of a '
                 'beta-D-galactoside. It was looking for a specific SMARTS '
                 'pattern `[C@H]1([O])[C@@H](O)[C@@H](O)[C@H](CO)O[C@@H]1*` '
                 'that explicitly includes `[C@H]1([O])`. This requires a '
                 'specific stereochemistry at the anomeric carbon AND requires '
                 'that oxygen to be directly attached to the anomeric carbon.\n'
                 '    *   The provided examples showed that the oxygen linked '
                 'to the anomeric carbon is NOT always a hydroxyl group. It '
                 'may be a glycosidic bond to another molecule.\n'
                 '    *   This caused many *false negatives*, where molecules '
                 'that *are* beta-D-galactosides were not identified because '
                 'of different bonding at the anomeric position, with that '
                 'oxygen being part of some other group.\n'
                 '\n'
                 '2.  **False Positives**: Some false positives also exist, '
                 'probably due to the fact that a molecule containing a '
                 'beta-D-galactoside may have other D-galactoside rings (that '
                 'are not beta), or contain other carbohydrate moieties, like '
                 'glucose or rhamnose, that could be mistaken for a '
                 'beta-D-galactoside when not looking at the anomeric '
                 'configuration with more precision.\n'
                 '    *   The previous version only checked if there was *any* '
                 'beta-D-galactoside substructure. It did not check if the '
                 'molecule only contained a beta-D-galactoside.\n'
                 '\n'
                 '3. **Step-by-step Refinement**\n'
                 '    * First, we need to make sure that the anomeric carbon '
                 'has the correct beta configuration, but accept that the '
                 'oxygen is part of some other group. The SMARTS pattern '
                 'should be adjusted to '
                 '`[C@H]1([OX2])[C@@H](O)[C@@H](O)[C@H](CO)O[C@@H]1` to '
                 'reflect that the oxygen is a bivalent oxygen. We should '
                 'enforce that only this oxygen is connected to the anomeric '
                 'carbon.\n'
                 '    * Then, we should check for each possible anomeric bond '
                 'to verify if it is indeed the beta configuration we are '
                 'looking for.\n'
                 '    * The molecule does not have to *only* contain '
                 'beta-D-galactosides, so we must not check for that.\n'
                 '\n'
                 '**Revised Strategy:**\n'
                 '\n'
                 '1.  **Identify D-galactose:** First identify the D-galactose '
                 'pyranose ring using '
                 '`O[C@H]1[C@@H](O)[C@@H](O)[C@H](CO)O[C@@H]1*` as before.\n'
                 '2.  **Check for beta anomeric carbon**\n'
                 '    *   Iterate over all instances of the D-galactose '
                 'pyranose ring.\n'
                 '    *  For every match, get the anomeric carbon atom (the '
                 'one attached to the ring oxygen and the oxygen external to '
                 'the ring).\n'
                 "    *   Check that the stereochemistry of this carbon is '@' "
                 'using `GetChiralTag()` method.\n'
                 '\n'
                 '**Code Implementation:**',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 35,
    'num_false_positives': 10601,
    'num_true_negatives': 131653,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.003290710793531403,
    'recall': 0.7608695652173914,
    'f1': 0.006553079947575361,
    'accuracy': 0.9254251581166549,
    'negative_predictive_value': 0.9999164540041318}