"""
Classifies: CHEBI:22315 alkaloid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_alkaloid(smiles):
    """
    Determines if a molecule is an alkaloid based on its SMILES string.
    An alkaloid is defined as a naturally occurring, basic nitrogen compound (mostly heterocyclic).
    Amino acids, peptides, proteins, nucleotides, nucleic acids, amino sugars, and antibiotics are
    not normally regarded as alkaloids. Compounds where nitrogen is exocyclic (e.g., dopamine, mescaline,
    serotonin) are usually classed as amines rather than alkaloids.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkaloid, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of nitrogen atoms
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]
    if not n_atoms:
        return False, "No nitrogen atoms found"

    # Check for basic nitrogen atoms
    basic_nitrogens = []
    for atom in n_atoms:
        if atom.GetFormalCharge() != 0:
            continue  # Exclude charged nitrogens (quaternary ammonium)
        if atom.GetHybridization() == Chem.rdchem.HybridizationType.SP3:
            # SP3 hybridized nitrogen is often basic
            basic_nitrogens.append(atom)
        elif atom.GetHybridization() == Chem.rdchem.HybridizationType.SP2:
            # For SP2 hybridized nitrogen, check if it's pyridine-like
            num_h = atom.GetTotalNumHs()
            if num_h == 1:
                basic_nitrogens.append(atom)

    if not basic_nitrogens:
        return False, "No basic nitrogen atoms found"

    # Exclude amino acids and peptides by detecting peptide bonds
    peptide_bond = Chem.MolFromSmarts("N[C;D2](=O)C")  # N-C(=O)-C pattern
    if mol.HasSubstructMatch(peptide_bond):
        return False, "Contains peptide bond, may be a peptide or protein"

    # Exclude nucleotides and nucleic acids by detecting nucleobases
    nucleic_acid_bases = [
        Chem.MolFromSmarts("c1nc[nH]c(=O)[nH]1"),  # Cytosine
        Chem.MolFromSmarts("c1cc(=O)[nH]c(=O)[nH]1"),  # Uracil/Thymine
        Chem.MolFromSmarts("c1ncnc2ncnn12"),  # Adenine
        Chem.MolFromSmarts("c1[nH]c2c(n1)nc(nc2)N"),  # Guanine
    ]
    for base in nucleic_acid_bases:
        if mol.HasSubstructMatch(base):
            return False, "Contains nucleic acid base"

    # Exclude amino sugars by detecting sugar rings with amino groups
    amino_sugar = Chem.MolFromSmarts("O[C@H]1[C@H](O)[C@@H](N)[C@@H](O)[C@H](O)[C@H]1O")  # Simple amino sugar pattern
    if mol.HasSubstructMatch(amino_sugar):
        return False, "Contains amino sugar moiety"

    # Exclude antibiotics - often contain characteristic lactone or glycopeptide structures
    antibiotic_patterns = [
        Chem.MolFromSmarts("C(=O)O[C@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O"),  # General lactone ring
        Chem.MolFromSmarts("C1=CNC(=O)N=C1"),  # Beta-lactam ring
    ]
    for pattern in antibiotic_patterns:
        if mol.HasSubstructMatch(pattern):
            return False, "Contains antibiotic-like structure"

    # Exclude certain functional groups associated with excluded classes
    excluded_groups = [
        Chem.MolFromSmarts("P(=O)(O)O"),  # Phosphate group in nucleotides
        Chem.MolFromSmarts("C=O"),        # Carbonyl group in amino acids and peptides
        Chem.MolFromSmarts("C#N"),        # Nitrile group
    ]
    for group in excluded_groups:
        if mol.HasSubstructMatch(group):
            group_name = group.GetProp("_Name") if mol.HasProp("_Name") else "Excluded group"
            return False, f"Contains {group_name}, may be an excluded compound"

    # Check if nitrogen is part of an amine group (exocyclic)
    amine_n = Chem.MolFromSmarts("[NX3;H2,H1;!$(NC=O)]")  # Primary or secondary amine nitrogen
    if mol.HasSubstructMatch(amine_n):
        # Exclude if nitrogen is exocyclic and not in a ring
        for match in mol.GetSubstructMatches(amine_n):
            atom = mol.GetAtomWithIdx(match[0])
            if not atom.IsInRing():
                return False, "Nitrogen is exocyclic, molecule may be an amine rather than an alkaloid"

    # At this point, we have a molecule with at least one basic nitrogen atom
    # that is not excluded by the other criteria
    return True, "Molecule is classified as an alkaloid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22315',
                          'name': 'alkaloid',
                          'definition': 'Any of the naturally occurring, basic '
                                        'nitrogen compounds (mostly '
                                        'heterocyclic) occurring mostly in the '
                                        'plant kingdom, but also found in '
                                        'bacteria, fungi, and animals. By '
                                        'extension, certain neutral compounds '
                                        'biogenetically related to basic '
                                        'alkaloids are also classed as '
                                        'alkaloids. Amino acids, peptides, '
                                        'proteins, nucleotides, nucleic acids, '
                                        'amino sugars and antibiotics are not '
                                        'normally regarded as alkaloids. '
                                        'Compounds in which the nitrogen is  '
                                        'exocyclic (dopamine, mescaline, '
                                        'serotonin, etc.) are usually classed '
                                        'as amines rather than alkaloids.',
                          'parents': ['CHEBI:35352'],
                          'xrefs': ['Wikipedia:Alkaloid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 82,
                           'log_lines_of_code': 4.406719247264253,
                           'indent_by_line': [   1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmarts',
                                                 'GetFormalCharge',
                                                 'GetTotalNumHs',
                                                 'append',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'IsInRing',
                                                 'GetSubstructMatches',
                                                 'HasProp',
                                                 'GetProp',
                                                 'GetHybridization',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum'],
                           'methods_called_count': 14,
                           'smarts_strings': [   'c1ncnc2ncnn12',
                                                 'C=O',
                                                 'C#N',
                                                 '"N[C;D2](=O)C")  # N-C(=O',
                                                 'c1[nH]c2c(n1)nc(nc2)N',
                                                 'O[C@H]1[C@H](O)[C@@H](N)[C@@H](O)[C@H](O)[C@H]1O',
                                                 'P(=O)(O)O',
                                                 'C1=CNC(=O)N=C1',
                                                 'c1cc(=O)[nH]c(=O)[nH]1',
                                                 'c1nc[nH]c(=O)[nH]1',
                                                 '[NX3;H2,H1;!$(NC=O)]',
                                                 'C(=O)O[C@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O'],
                           'smarts_strings_count': 12,
                           'defs': ['is_alkaloid(smiles):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No nitrogen atoms found"',
                                          'False, "No basic nitrogen atoms '
                                          'found"',
                                          'False, "Contains peptide bond, may '
                                          'be a peptide or protein"',
                                          'False, "Contains nucleic acid base"',
                                          'False, "Contains amino sugar '
                                          'moiety"',
                                          'False, "Contains antibiotic-like '
                                          'structure"',
                                          'False, f"Contains {group_name}, may '
                                          'be an excluded compound"',
                                          'False, "Nitrogen is exocyclic, '
                                          'molecule may be an amine rather '
                                          'than an alkaloid"',
                                          'True, "Molecule is classified as an '
                                          'alkaloid"'],
                           'returns_count': 10,
                           'complexity': 6.681343849452849},
    'message': '\n'
               'Attempt failed: F1 score of 0.07459295010234936 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C1CCN2C[C@@H]3C[C@H](C=C4CCCN[C@@H]34)[C@H]2C1 NAME: Aloperine '
               'REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: [H][C@@]12Cc3c[nH]c4cccc(c34)[C@@]1([H])C=C(C)CN2C '
               'NAME: agroclavine REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'O(C(CCl)=O)[C@H]1[C@]23[C@]([C@]4(N5[C@]([C@@H]1[C@@H](C4)[C@@H]([C@H]5O)CC)(C2)[H])[H])(N(C6=C3C=CC=C6)C)[H] '
               'NAME: lorajmine REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CN(C4)C(=O)C5=CN=CC=C5)S(=O)(=O)C)CO '
               'NAME: '
               "[(1R)-1-(hydroxymethyl)-7-methoxy-2-methylsulfonyl-1'-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]-(3-pyridinyl)methanone "
               'REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: O(C=1C2=C3C(N(CCC3=CC1OC)C(OC)=O)CC=4C2=CC=CC4)C '
               'NAME: N-Methoxycarbonyl-N-nornuciferine REASON: CORRECT '
               'Molecule is classified as an alkaloid\n'
               ' * SMILES: OC(=O)C1NC(C=2NC=3C(C2C1)=CC=CC3)CCC(O)=O NAME: '
               '3-Carboxy-2,3,4,9-tetrahydro-1H-pyrido[3,4-b]indole-1-propanoic '
               'acid REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: CC(=O)c1nc(cc2c3ccccc3[nH]c12)C(=O)NCCc1ccc(O)cc1 '
               'NAME: marinacarboline B REASON: CORRECT Molecule is classified '
               'as an alkaloid\n'
               ' * SMILES: C=12N(C=NC1N(C(N(C2=O)CCCC[C@H](O)C)=O)C)C NAME: '
               '(R)-lisofylline REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: OC(=O)c1ccc2C(=O)C3=C(NCCS3(=O)=O)C(=O)c2n1 NAME: '
               'ascidiathiazone A REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: COC1=C[C@]23CCN(C)[C@H](Cc4ccc(OC)c(O)c24)C3=CC1O '
               'NAME: salutaridinol REASON: CORRECT Molecule is classified as '
               'an alkaloid\n'
               ' * SMILES: '
               'C1(C(O[C@@]2([C@](O)([C@@]34[C@H](OC(C)=O)[C@@]([H])([C@H]([C@H]([C@@]3([C@@H](OC(=O)C)[C@H]2OC(C=5C=CC=CC5)=O)COC(=O)C)OC(=O)C)OC(C)=O)[C@@](COC(C6=C(C1C)C=CN=C6)=O)(C)O4)C)[H])=O)(O)C '
               'NAME: hypoglaunine C REASON: CORRECT Molecule is classified as '
               'an alkaloid\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CN(C4)C(=O)COC)C(=O)NC5CCCC5)CO '
               'NAME: '
               "(1S)-N-cyclopentyl-1-(hydroxymethyl)-7-methoxy-1'-(2-methoxy-1-oxoethyl)-9-methyl-2-spiro[1,3-dihydropyrido[3,4-b]indole-4,3'-azetidine]carboxamide "
               'REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: '
               'O=C1N[C@@H](CC2=CC=CC=C2)[C@H]3[C@@]14[C@H](OC(=O)C)C=C[C@](O)(C[C@H](CC=C[C@H]4C=C(C)[C@H]3C)C)C '
               'NAME: RKS-1778 REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               '[C@@]12(N3CC[C@H](O1)CCCCCC[C@H]4[C@@]5(O[C@H](CCCCCC[C@H]2CCC3)CCN5CCC4)[H])[H] '
               'NAME: xestospongin C REASON: CORRECT Molecule is classified as '
               'an alkaloid\n'
               ' * SMILES: COc1cc(CC2NCCc3cc(OC)c(O)cc23)ccc1O NAME: '
               'nororientaline REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               '[H]\\C(C)=C1/CN(C)[C@]2([H])Cc3c(CC[C@]1([H])[C@]2([H])C)[nH]c1ccccc31 '
               'NAME: vobasan REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@]3([H])C(=CN1CCC1=C2NC2=C1C=CC=C2)[C@H](C)OC=C3C(=O)OC '
               'NAME: cathenamine REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: Oc1ccc2c(c1)c1ccnc3ccc(=O)n2c13 NAME: '
               '10-hydroxycanthin-6-one REASON: CORRECT Molecule is classified '
               'as an alkaloid\n'
               ' * SMILES: C[C@@H]1C[C@H]2CC(=O)[C@H]3CCCN4CCC[C@]23C4=C1 '
               'NAME: Fawcettidine REASON: CORRECT Molecule is classified as '
               'an alkaloid\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)O)C)C1=NC(=C2NC3=C(C2=C1)C=C(O)C=C3)CCC(=O)N4[C@H](C(=O)O)CCC4 '
               'NAME: 6-hydroxymetatacarboline E REASON: CORRECT Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'CCCC(=O)N1CC2(C1)CN([C@H](C3=C2C4=C(N3C)C=C(C=C4)OC)CO)C(=O)NC5=CC(=CC=C5)F '
               'NAME: '
               "(1R)-N-(3-fluorophenyl)-1-(hydroxymethyl)-7-methoxy-9-methyl-1'-(1-oxobutyl)-2-spiro[1,3-dihydropyrido[3,4-b]indole-4,3'-azetidine]carboxamide "
               'REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C)CC5=CC(=CC=C5)OC)CO '
               'NAME: '
               "[(1S)-7-methoxy-2-[(3-methoxyphenyl)methyl]-9-methyl-1'-methylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol "
               'REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: '
               '[H][C@]12C[C@H](OC)C=C[C@]11c3cc4OCOc4cc3CO[C@]1(O)CN2C NAME: '
               'tazettine REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'COC1=CC2=C(C=C1)C3=C(N2)[C@H](N(CC34CCN(CC4)CC5=NC=CS5)C(=O)C6CCOCC6)CO '
               'NAME: '
               "[(1S)-1-(hydroxymethyl)-7-methoxy-1'-(2-thiazolylmethyl)-2-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,4'-piperidine]yl]-(4-oxanyl)methanone "
               'REASON: CORRECT Molecule is classified as an alkaloid\n'
               ' * SMILES: [H][C@]12Cc3ccccc3-c3c(OC)c(O)cc(CCN1)c23 NAME: '
               'R-(-)-asimilobine REASON: CORRECT Molecule is classified as an '
               'alkaloid\n'
               'False positives: SMILES: '
               'O1[C@@H](N2C=C(C(=O)NC2=O)CO)[C@H](O)[C@H](O)[C@H]1CO NAME: '
               '5-Hydroxymethyluridine REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'C1C[C@H]([C@H](O[C@H]1CC(=O)N2CCC3=CC=CC=C3C2)CO)NC(=O)C4CCOCC4 '
               'NAME: '
               'N-[(2S,3R,6R)-6-[2-(3,4-dihydro-1H-isoquinolin-2-yl)-2-oxoethyl]-2-(hydroxymethyl)-3-oxanyl]-4-oxanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: S1C(CC(N2CCCCC2)=CC1=S)(C)C NAME: '
               '6,6-dimethyl-4-piperidino-5,6-dihydro-2H-thiine-2-thione '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'CCS(=O)(=O)N1CCCCN2[C@@H](C1)[C@H]([C@@H]2CO)C3=CC=C(C=C3)C4=CC=CC(=C4)C#N '
               'NAME: '
               '3-[4-[(8R,9R,10R)-6-ethylsulfonyl-10-(hydroxymethyl)-1,6-diazabicyclo[6.2.0]decan-9-yl]phenyl]benzonitrile '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'O=C1N(O)C=CC(=C1[C@H]2[C@](C=C)(C[C@H](C)C[C@@H]2C)C)O NAME: '
               'Cordypyridone B REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'S(CC[C@@H]1NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](C(C)C)NC(CNC(C[C@H](OC1=O)[C@H](CCCCCC)C)=O)=O)CC(C)C)C)C '
               'NAME: Oryzamide C REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: CC(C)OCCCNC1=NC=NC2=C1C=NN2C3=CC=CC=C3 NAME: '
               '1-phenyl-N-(3-propan-2-yloxypropyl)-4-pyrazolo[3,4-d]pyrimidinamine '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'O=C1N2C(=NC3=C1C=CC=C3)[C@@]4(N5[C@@H]6N(C([C@@H]5C)=O)C7=C([C@]6(C[C@@H]2C(=O)N4)O)C=CC=C7)C '
               "NAME: 2'-epi-fumiquinazoline D REASON: WRONGLY CLASSIFIED "
               'Molecule is classified as an alkaloid\n'
               ' * SMILES: '
               'CCOC(=O)C1=C(COCCN)NC(C)=C([C@@H]1c1ccccc1Cl)C(=O)OC NAME: '
               '(S)-amlodipine REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'CCC(C)\\C=C(C)\\C=C/C(O)C(C)C(=O)NCC(=O)N\\C(=C/C)C(=O)N[C@@H]([C@H](C)N)C(=O)N[C@@H]([C@@H](C)[C@@H](C)C(N)=O)C(=O)N[C@@H]1[C@H](OC(=O)[C@@H]2C[C@@H](Cl)CCN2C(=O)[C@H](NC(=O)[C@H]([C@@H](C)O)N(C)C(=O)[C@H](C)NC(=O)CNC(=O)[C@@H](COC)NC1=O)[C@H](OC)c1ccc(O[C@@H]2O[C@@H](C)[C@H](O)[C@@H](O)[C@H]2O)cc1)C(C)C '
               'NAME: Mirabamide F REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)CN(C)C)C(=O)N(C[C@H]1OC)C)C)CC3=CC=CC=C3F '
               'NAME: '
               '2-(dimethylamino)-N-[(4R,7R,8S)-5-[(2-fluorophenyl)methyl]-8-methoxy-4,7,10-trimethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: O=C(NC(CC=1NC=NC1)C(O)=O)C(N)CCC(O)=O NAME: '
               'Glutamylhistidine REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: CCOC1=CC2=C(N)C3=C(C=C(NCC4=CC=CO4)C=C3)N=C2C=C1 '
               'NAME: 7-ethoxy-N(3)-(2-furanylmethyl)-3,9-acridinediamine '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: C1=CC=C(C=C1)COC2=CC=CC=C2C=NN3C(=NN=N3)N NAME: '
               '1-[(2-phenylmethoxyphenyl)methylideneamino]-5-tetrazolamine '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)[C@H](O)C '
               'NAME: Asn-Thr-Pro REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'COC1=C(C2=NC3=CC=CC=C3N=C2C=C1)NC(=O)C4=CC=C(C=C4)Cl NAME: '
               '4-chloro-N-(2-methoxy-1-phenazinyl)benzamide REASON: WRONGLY '
               'CLASSIFIED Molecule is classified as an alkaloid\n'
               ' * SMILES: '
               'C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@H](C)CO)C)CN(C)CC3=CC4=C(C=C3)OCO4 '
               'NAME: '
               '(3R,9S,10S)-9-[[1,3-benzodioxol-5-ylmethyl(methyl)amino]methyl]-16-(dimethylamino)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-13-one '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'COC1=CC=CC=C1CNC(=O)C[C@H]2CC[C@@H]3[C@@H](O2)COC[C@H](CN3CC4=CC=CC(=C4)C5=CC=NC=C5)O '
               'NAME: '
               '2-[(3S,6aR,8R,10aR)-3-hydroxy-1-[(3-pyridin-4-ylphenyl)methyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[(2-methoxyphenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'O=C1OCCCCC(NC(=O)C(NC(=O)C(NC(=O)C2NCCC2)CCC(=O)N)CC3=CC=C(O)C=C3)C(=O)NC(C(=O)NC(C(=O)NC(C(O)C)C(NC(C(NC(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CCCCO)=O)CCCCN)=O)CC5=CC=C(O)C=C5)=O)CCC(=O)O)C '
               'NAME: Maltacine B2b REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: '
               'CCCNC(=O)[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12 NAME: '
               "adenosine-5'-(N-propyl)carboxamide REASON: WRONGLY CLASSIFIED "
               'Molecule is classified as an alkaloid\n'
               ' * SMILES: '
               '[H]C12CC=CC1([H])C1=C(NC2C2=CC3=C(OCO3)C=C2Br)C=CC=C1 NAME: '
               'G-15 REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: '
               '(3R,12Z,15Z,18Z,21Z,24Z,27Z)-3-hydroxytriacontahexaenoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Molecule is classified as an '
               'alkaloid\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CSC=C4)[C@@H](C)CO '
               'NAME: LSM-9491 REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: Cc1cc2CCN(C(=O)Nc3ccc(Oc4cccnc4C)nc3)c2cc1C(F)(F)F '
               'NAME: SB 243213 REASON: WRONGLY CLASSIFIED Molecule is '
               'classified as an alkaloid\n'
               ' * SMILES: CSc1nc2ccccc2s1 NAME: '
               '2-methylthio-1,3-benzothiazole REASON: WRONGLY CLASSIFIED '
               'Molecule is classified as an alkaloid\n'
               'False negatives: SMILES: '
               'C\\C=C1/[C@@H]2Cc3[nH]c(=O)ccc3[C@@]1(N)CC(C)=C2 NAME: '
               'huperzine A REASON: MISSED No basic nitrogen atoms found\n'
               ' * SMILES: '
               'C=1(C(C(C=2C=3C=CC=CC3NC2)=C(O)C(=O)C1C=4C5=C(NC4)C=C(C=C5)CC=C(C)C)=O)O '
               'NAME: semicochliodinol B REASON: MISSED No basic nitrogen '
               'atoms found\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3([H])C(=CC[C@]4(C)[C@]([H])([C@H](O)C[C@@]34C)[C@H](C)N(C)C)C=C1CC[C@@H]([C@@H]2C)N(C)C '
               'NAME: 31-demethylbuxaminol REASON: MISSED No nitrogen atoms in '
               'ring (heterocycle)\n'
               ' * SMILES: '
               '[Cl-].O1C=2C(=CC3=CC=C4C(=C3C2)[N+](=CC5=C(OC)C(OC)=CC=C45)C)OC1 '
               'NAME: Chelerythrine chloride REASON: MISSED No basic nitrogen '
               'atoms found\n'
               ' * SMILES: COc1cc2c[n+]3CCc4cc(OC)c(OC)cc4-c3cc2cc1O NAME: '
               'Dehydrocorytenchine REASON: MISSED No basic nitrogen atoms '
               'found\n'
               ' * SMILES: CNCCC1=CC(OC)=C(OC)C(OC)=C1 NAME: N-methylmescaline '
               'REASON: MISSED No nitrogen atoms in ring (heterocycle)\n'
               ' * SMILES: OP(=O)(OC=1C2=C(C=CC1)NC=C2CCNC)O NAME: baeocystin '
               'REASON: MISSED No basic nitrogen atoms found\n'
               ' * SMILES: COc1ccc2c(c[n+](C)c3c4cc5OCOc5cc4ccc23)c1OC NAME: '
               'chelerythrine REASON: MISSED No basic nitrogen atoms found\n'
               ' * SMILES: '
               'C=1C=CC2=C(C1)C=3CC=[N+]4[C@](C3N2)(C[C@]5([C@@]([C@@H](OC=C5C(OC)=O)C)(C4)[H])[H])[H] '
               'NAME: dihydroserpentine(1+) REASON: MISSED No basic nitrogen '
               'atoms found\n'
               ' * SMILES: O(C=1C2=C[N+]=3CCC=4C(C3C=C2C=CC1O)=CC(O)=C(OC)C4)C '
               'NAME: stepharanine REASON: MISSED No basic nitrogen atoms '
               'found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'NCCO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O',
                                     'name': 'beta-D-Manp-(1->2)-beta-D-Manp-(1->2)-beta-D-Manp-O[CH2]2NH2',
                                     'reason': 'Nitrogen is exocyclic, '
                                               'molecule may be an amine '
                                               'rather than an alkaloid'},
                                 {   'smiles': '[H][C@@]12CCC(C)=C[C@@]1([H])C(C)(C)CCCC2=C',
                                     'name': '(1R,6R)-alpha-himachalene',
                                     'reason': 'No nitrogen atoms found'},
                                 {   'smiles': 'OC1(C2C(CC1OC(=O)C)C(=COC2OC(=O)CC(C)C)COC(=O)CC(C)C)COC(=O)CC(C)C',
                                     'name': '[6-Acetyloxy-7-hydroxy-1-(3-methylbutanoyloxy)-7-(3-methylbutanoyloxymethyl)-4a,5,6,7a-tetrahydro-1H-cyclopenta[c]pyran-4-yl]methyl '
                                             '3-methylbutanoate',
                                     'reason': 'No nitrogen atoms found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Contains Excluded group, may '
                                               'be an excluded compound'},
                                 {   'smiles': 'OC(=O)C(N)C=C',
                                     'name': '2-Amino-3-butenoic acid',
                                     'reason': 'Contains Excluded group, may '
                                               'be an excluded compound'},
                                 {   'smiles': 'C1C[C@H]([C@H](O[C@H]1CC(=O)N2CCC3=CC=CC=C3C2)CO)NC(=O)C4CCOCC4',
                                     'name': 'N-[(2S,3R,6R)-6-[2-(3,4-dihydro-1H-isoquinolin-2-yl)-2-oxoethyl]-2-(hydroxymethyl)-3-oxanyl]-4-oxanecarboxamide',
                                     'reason': 'Contains Excluded group, may '
                                               'be an excluded compound'},
                                 {   'smiles': 'O(C(C(O)COC=1C=2OC=CC2C=C3C1OC(=O)C=C3)(C)C)C(=O)/C(/C)=C\\C',
                                     'name': 'Tomasin',
                                     'reason': 'No nitrogen atoms found'},
                                 {   'smiles': 'C([C@H](N)C(=O)O)SS',
                                     'name': '3-disulfanyl-L-alanine',
                                     'reason': 'Contains Excluded group, may '
                                               'be an excluded compound'},
                                 {   'smiles': 'O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)C(C)C',
                                     'name': 'Ser-Val-Ile',
                                     'reason': 'Contains Excluded group, may '
                                               'be an excluded compound'},
                                 {   'smiles': 'S(OC[C@H]1OC(OC[C@H]2O[C@H](O)[C@H](NC(=O)C)[C@@H](OC3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O)(O)(=O)=O',
                                     'name': '[(2R,3S,4R,5R)-5-Acetamido-6-[[(2R,3R,4R,5R,6S)-5-acetamido-3,6-dihydroxy-4-[(3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methoxy]-3,4-dihydroxyoxan-2-yl]methyl '
                                             'hydrogen sulfate',
                                     'reason': 'Contains Excluded group, may '
                                               'be an excluded compound'}],
    'sample_false_negatives': [   {   'smiles': 'O(C(CCl)=O)[C@H]1[C@]23[C@]([C@]4(N5[C@]([C@@H]1[C@@H](C4)[C@@H]([C@H]5O)CC)(C2)[H])[H])(N(C6=C3C=CC=C6)C)[H]',
                                      'name': 'lorajmine',
                                      'reason': 'Contains Excluded group, may '
                                                'be an excluded compound'},
                                  {   'smiles': 'COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CN(C4)C(=O)C5=CN=CC=C5)S(=O)(=O)C)CO',
                                      'name': "[(1R)-1-(hydroxymethyl)-7-methoxy-2-methylsulfonyl-1'-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]-(3-pyridinyl)methanone",
                                      'reason': 'Contains Excluded group, may '
                                                'be an excluded compound'},
                                  {   'smiles': 'O(C=1C2=C3C(N(CCC3=CC1OC)C(OC)=O)CC=4C2=CC=CC4)C',
                                      'name': 'N-Methoxycarbonyl-N-nornuciferine',
                                      'reason': 'No basic nitrogen atoms '
                                                'found'},
                                  {   'smiles': 'OC(=O)C1NC(C=2NC=3C(C2C1)=CC=CC3)CCC(O)=O',
                                      'name': '3-Carboxy-2,3,4,9-tetrahydro-1H-pyrido[3,4-b]indole-1-propanoic '
                                              'acid',
                                      'reason': 'Contains Excluded group, may '
                                                'be an excluded compound'},
                                  {   'smiles': 'CC(=O)c1nc(cc2c3ccccc3[nH]c12)C(=O)NCCc1ccc(O)cc1',
                                      'name': 'marinacarboline B',
                                      'reason': 'Contains Excluded group, may '
                                                'be an excluded compound'},
                                  {   'smiles': 'C=12N(C=NC1N(C(N(C2=O)CCCC[C@H](O)C)=O)C)C',
                                      'name': '(R)-lisofylline',
                                      'reason': 'No basic nitrogen atoms '
                                                'found'},
                                  {   'smiles': 'OC(=O)c1ccc2C(=O)C3=C(NCCS3(=O)=O)C(=O)c2n1',
                                      'name': 'ascidiathiazone A',
                                      'reason': 'Contains Excluded group, may '
                                                'be an excluded compound'},
                                  {   'smiles': 'C\\C=C1/[C@@H]2Cc3[nH]c(=O)ccc3[C@@]1(N)CC(C)=C2',
                                      'name': 'huperzine A',
                                      'reason': 'Nitrogen is exocyclic, '
                                                'molecule may be an amine '
                                                'rather than an alkaloid'},
                                  {   'smiles': 'C=1(C(C(C=2C=3C=CC=CC3NC2)=C(O)C(=O)C1C=4C5=C(NC4)C=C(C=C5)CC=C(C)C)=O)O',
                                      'name': 'semicochliodinol B',
                                      'reason': 'Contains Excluded group, may '
                                                'be an excluded compound'},
                                  {   'smiles': 'C1(C(O[C@@]2([C@](O)([C@@]34[C@H](OC(C)=O)[C@@]([H])([C@H]([C@H]([C@@]3([C@@H](OC(=O)C)[C@H]2OC(C=5C=CC=CC5)=O)COC(=O)C)OC(=O)C)OC(C)=O)[C@@](COC(C6=C(C1C)C=CN=C6)=O)(C)O4)C)[H])=O)(O)C',
                                      'name': 'hypoglaunine C',
                                      'reason': 'No basic nitrogen atoms '
                                                'found'}],
    'attempt': 2,
    'reasoning': "After analyzing the previous code and the outcomes, it's "
                 'clear that the function is misclassifying certain molecules '
                 'due to overly strict criteria and some exclusions not being '
                 'properly implemented.\n'
                 '\n'
                 '**Issues identified:**\n'
                 '\n'
                 '1. **Overly strict on nitrogen in rings:** The previous code '
                 'requires nitrogen atoms to be in a ring (heterocyclic) to '
                 'classify a molecule as an alkaloid. However, the definition '
                 'states that alkaloids are "mostly heterocyclic," implying '
                 'that some alkaloids may have exocyclic nitrogen.\n'
                 '\n'
                 '2. **Excluding legitimate alkaloids:** Some compounds like '
                 '**huperzine A** and **semicochliodinol B** are being missed '
                 "because they don't have nitrogen in a ring, but they are "
                 'recognized alkaloids.\n'
                 '\n'
                 '3. **Incorrectly including non-alkaloids:** The function is '
                 'classifying amino acids, peptides, and other excluded '
                 "compounds as alkaloids because it's not effectively "
                 'filtering them out.\n'
                 '\n'
                 '**Improvements:**\n'
                 '\n'
                 '- **Relax the nitrogen criteria:** Include compounds with '
                 'nitrogen atoms regardless of their position (ring or '
                 'exocyclic) but ensure that the nitrogen is basic and not '
                 'part of functional groups commonly found in excluded '
                 'compounds.\n'
                 '\n'
                 '- **Improve exclusion of amino acids and peptides:** Enhance '
                 'the detection of peptide bonds and common amino acid '
                 'structures to exclude these molecules.\n'
                 '\n'
                 '- **Exclude known non-alkaloid structures:** Expand the '
                 'patterns used to detect and exclude nucleotides, nucleic '
                 'acids, amino sugars, and antibiotics.\n'
                 '\n'
                 '- **Check for natural occurrence and basicity:** While '
                 "natural occurrence can't be directly determined from SMILES, "
                 'we can focus on the presence of basic nitrogen atoms and '
                 'exclude quaternary ammonium ions which are not basic.\n'
                 '\n'
                 "- **Use functional group analysis:** Utilize RDKit's "
                 'functional group detection to identify key features '
                 'associated with alkaloids and excluded classes.\n'
                 '\n'
                 "Based on these considerations, here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 668,
    'num_false_positives': 4200,
    'num_true_negatives': 135916,
    'num_false_negatives': 1516,
    'num_negatives': None,
    'precision': 0.1372226787181594,
    'recall': 0.3058608058608059,
    'f1': 0.18944980147475896,
    'accuracy': 0.9598313422347153,
    'negative_predictive_value': 0.9889690901682286}