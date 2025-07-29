"""
Classifies: CHEBI:134045 polychlorinated dibenzodioxines and related compounds
"""
"""
Classifies: polychlorinated dibenzodioxines and related compounds (persistent organic pollutants)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polychlorinated_dibenzodioxines_and_related_compounds(smiles: str):
    """
    Determines if a molecule belongs to polychlorinated dibenzodioxines and related compounds.
    These are organochlorine/bromine compounds with dioxin, dibenzofuran, or biphenyl cores,
    where ALL substituents on the core rings are halogens (Cl/Br).
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES"

    # Must contain at least two chlorine or bromine atoms
    halogen_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() in [17, 35])
    if halogen_count < 2:
        return False, f"Insufficient halogens ({halogen_count} found, minimum 2)"

    # Core structure patterns
    dioxin_core = Chem.MolFromSmarts('O1c2ccccc2Oc2ccccc12')  # Dibenzodioxin
    furan_core = Chem.MolFromSmarts('c1ccc2c(c1)oc1ccccc12')  # Dibenzofuran
    biphenyl_core = Chem.MolFromSmarts('c1ccccc1-c2ccccc2')   # Biphenyl

    # Check each core pattern for valid substitution
    for core in [dioxin_core, furan_core, biphenyl_core]:
        matches = mol.GetSubstructMatches(core)
        for match in matches:
            core_atoms = set(match)
            valid = True
            
            # Check all substituents on core's aromatic atoms are Cl/Br
            for atom_idx in match:
                atom = mol.GetAtomWithIdx(atom_idx)
                if not atom.GetIsAromatic():
                    continue  # Only check aromatic positions
                    
                for neighbor in atom.GetNeighbors():
                    # Skip core-internal bonds
                    if neighbor.GetIdx() in core_atoms:
                        continue
                        
                    # Substituents must be Cl/Br
                    if neighbor.GetAtomicNum() not in [17, 35]:
                        valid = False
                        break
                
                if not valid:
                    break
            
            if valid:
                core_type = "dioxin" if core == dioxin_core else \
                            "dibenzofuran" if core == furan_core else "biphenyl"
                return True, f"Halogenated {core_type} core with all substituents as Cl/Br"

    return False, "No valid dioxin/dibenzofuran/biphenyl core with halogen-only substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134045',
                          'name': 'polychlorinated dibenzodioxines and related '
                                  'compounds',
                          'definition': 'Organochlorine compounds that are '
                                        'polychlorinated dibenzodioxines and '
                                        'structurally related entities that '
                                        'are persistant organic pollutants. '
                                        'These include polychlorinated '
                                        'dibenzofurans as well as '
                                        'polychlorinated and polybrominated '
                                        'biphenyls  They vary widely in their '
                                        'toxicity, but their toxic mode of '
                                        'action is through the aryl '
                                        'hydrocarbon receptor.',
                          'parents': ['CHEBI:17792'],
                          'xrefs': [   'Wikipedia:Dioxins_and_dioxin-like_compounds'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 42,
                           'log_lines_of_code': 3.7376696182833684,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 4,
                                                 4,
                                                 5,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 0,
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetIdx',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'GetIsAromatic',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'GetNeighbors',
                                                 'GetAtoms'],
                           'methods_called_count': 9,
                           'smarts_strings': [   'c1ccc2c(c1)oc1ccccc12',
                                                 'O1c2ccccc2Oc2ccccc12',
                                                 'c1ccccc1-c2ccccc2'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_polychlorinated_dibenzodioxines_and_related_compounds(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES"',
                                          'False, f"Insufficient halogens '
                                          '({halogen_count} found, minimum 2)"',
                                          'True, f"Halogenated {core_type} '
                                          'core with all substituents as '
                                          'Cl/Br"',
                                          'False, "No valid '
                                          'dioxin/dibenzofuran/biphenyl core '
                                          'with halogen-only substituents"'],
                           'returns_count': 4,
                           'complexity': 4.747533923656674},
    'message': '\n'
               'Attempt failed: F1 score of 0.6490066225165563 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: Clc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl '
               "NAME: 2,3,3',4,5-pentachlorobiphenyl REASON: CORRECT "
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Clc1cc2c3cc(Cl)c(Cl)c(Cl)c3oc2c(Cl)c1Cl NAME: '
               '2,3,4,6,7,8-Hexachlorodibenzofuran REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc(Cl)cc(c1)-c1cc(Cl)cc(Cl)c1 NAME: '
               "3,3',5,5'-tetrachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1ccccc1-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',4,5-tetrachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: ClC=1C(C=2C(Cl)=CC(Cl)=C(Cl)C2)=CC(Cl)=C(Cl)C1Cl '
               'NAME: PCB180 REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc2oc3cc(Cl)c(Cl)cc3c2cc1Cl NAME: '
               '2,3,7,8-Tetrachlorodibenzofuran REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1c(Cl)c(Cl)c(-c2ccccc2)c(Cl)c1Cl NAME: '
               '2,3,4,5,6-pentachlorobiphenyl REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1ccc(Cl)c(c1Cl)-c1c(Cl)ccc(Cl)c1Cl NAME: '
               "2,2',3,3',6,6'-hexachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1ccc(cc1)-c1cc(Cl)c(Cl)c(Cl)c1Cl NAME: '
               "2,3,4,4',5-Pentachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(C3=C(O)C(Cl)=CC(=C3)Cl)=CC(=C1O)Cl '
               'NAME: Ambigol E REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc2c(oc3c(Cl)c(Cl)c(Cl)c(Cl)c23)c(Cl)c1Cl NAME: '
               '1,2,3,4,6,7,8-Heptachlorodibenzofuran REASON: CORRECT '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin J REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin I REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(O)=CC(=C1C3=C(O)C(Cl)=CC(=C3)Cl)Cl '
               'NAME: Ambigol D REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1cc(Cl)c(Cl)c(Cl)c1 NAME: '
               "3,3',4,4',5-pentachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc2oc3c(Cl)c(Cl)c(Cl)c(Cl)c3c2c(Cl)c1Cl NAME: '
               '1,2,3,4,7,8,9-Heptachlorodibenzofuran REASON: CORRECT '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Clc1ccc(cc1Cl)-c1ccc(Cl)c(Cl)c1Cl NAME: '
               "2,3,4,3',4'-Pentachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc2Oc3cc(Cl)c(Cl)cc3Oc2cc1Cl NAME: '
               '2,3,7,8-tetrachlorodibenzodioxine REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: ClC1=C(C=2C(Cl)=CC(Cl)=C(Cl)C2)C=CC(Cl)=C1Cl NAME: '
               'PCB138 REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc2Oc3c(Cl)c(Cl)c(Cl)c(Cl)c3Oc2c(Cl)c1Cl NAME: '
               '1,2,3,4,6,7,8-Heptachlorodibenzodioxin REASON: CORRECT '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Clc1cc(Cl)c(Cl)c(c1)-c1cc(Cl)cc(Cl)c1Cl NAME: '
               "2,2',3,3',5,5'-hexachlorobiphenyl REASON: CORRECT Halogenated "
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc(Cl)c(Cl)c(-c2ccccc2)c1Cl NAME: '
               '2,3,5,6-tetrachlorobiphenyl REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin D REASON: CORRECT Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Clc1cc2Oc3c(Cl)c(Cl)c(Cl)c(Cl)c3Oc2cc1Cl NAME: '
               '1,2,3,4,7,8-Hexachlorodibenzodioxin REASON: CORRECT '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Clc1c(Cl)c(Cl)c2Oc3c(Cl)c(Cl)c(Cl)c(Cl)c3Oc2c1Cl '
               'NAME: 1,2,3,4,6,7,8,9-Octachlorodibenzo-p-dioxin REASON: '
               'CORRECT Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               'False positives: SMILES: '
               'Oc1c(Cl)cc(c(Cl)c1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "2,2',3,4',5,5'-Hexachloro-4-biphenylol REASON: WRONGLY "
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Oc1ccc(c(Cl)c1)-c1c(Cl)cc(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',4',6'-tetrachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'CN[C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C(O)=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)(NCc3ccc(cc3)-c3ccc(Cl)cc3)[C@H](O)[C@H](C)O1)c(Cl)c2 '
               'NAME: Chlorobiphenyl-vancomycin REASON: WRONGLY CLASSIFIED '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Oc1c(Br)cc(Br)cc1-c1cc(Br)cc(Br)c1OP(O)(O)=O NAME: '
               'Bromofenofos REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C '
               'NAME: Formicamycin H REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               '[NH3+][C@@H]1c2ccc(OS([O-])(=O)=O)c(Oc3cc(O)cc(c3)[C@@H]3NC(=O)[C@H](Cc4ccc(Oc5cc6cc(Oc7ccc(cc7Cl)[C@@H](O)[C@@H]7NC(=O)[C@H](NC(=O)[C@@H]6NC3=O)c3cc(Cl)c(O)c(c3)-c3c(O)cc(O)cc3[C@@H](NC7=O)C([O-])=O)c5[O-])c(Cl)c4)NC1=O)c2 '
               'NAME: A47934(2-) REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C=C2OC3=C(O)C=CC(=C3)[C@H](NC)C(N[C@@H]4C(N[C@@H](C1=C2)C(=O)N[C@@H]5C(=O)N[C@H]6C(=O)N[C@H](C(=O)N[C@H](C(=O)O)C=7C(C8=CC6=CC(Cl)=C8O[C@H]9O[C@@H]([C@H](O)[C@H]([C@H]9O)O)CO)=C(O)C=C(O)C7)[C@H](O[C@@H]%10O[C@@H](C(=O)O)[C@H](O)[C@H]([C@H]%10NC(=O)CCCCCC(C)C)O)C%11=CC(=C(OC=%12C=C5C=C(OC%13=C(C=C([C@H]4O)C=C%13)Cl)C%12O[C@H]%14O[C@H]([C@H](O)[C@H]([C@H]%14O)O)CO)C(Cl)=C%11)Cl)=O)=O '
               'NAME: MM 55266 REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Oc1ccc(cc1)-c1c(Cl)c(Cl)c(O)c(Cl)c1Cl NAME: '
               "2,3,5,6-tetrachloro-1,1'-biphenyl-4,4'-diol REASON: WRONGLY "
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'CN1[C@@H](Cc2ccc(Oc3cc4cc(-c5ccc6c(NC(=O)C6(O)C[C@@H](NC(=O)C(=O)c6cc(Cl)c(O)c(Cl)c6)C(=O)N[C@@H](C(=O)N[C@H]4C(=O)N[C@@H](C1=O)c1cc(Cl)c(O)c(Cl)c1)c1cc(Cl)c(O)c(Cl)c1)c5)c3O)cc2)C(=O)N[C@@H](C(O)=O)c1ccc(O)cc1 '
               'NAME: complestatin B REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               '[H][C@]1(Cc2ccc(Oc3cc4cc(-c5ccc6C(C[C@@H](NC(=O)C(=O)c7cc(Cl)c(O)c(Cl)c7)C(=O)N[C@@H](C(=O)N[C@@]4([H])C(=O)N[C@@H](C(=O)N1C)c1cc(Cl)c(O)c(Cl)c1)c1cc(Cl)c(O)c(Cl)c1)C(=O)Nc6c5)c3O)cc2)C(=O)N[C@@H](C(O)=O)c1ccc(O)cc1 '
               'NAME: complestatin A REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'CCCCN(CCCC)CC(O)c1cc(Cl)cc2\\C(=C/c3ccc(Cl)cc3)c3cc(Cl)ccc3-c12 '
               'NAME: lumefantrine REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Oc1c(Cl)c(Cl)c(c(Cl)c1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',3,4',5,5',6-heptachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'OP(O)(O)=O.OP(O)(O)=O.CN[C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O[C@H]5C[C@](C)(N)[C@@H](O)[C@H](C)O5)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C(O)=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)(NCc3ccc(cc3)-c3ccc(Cl)cc3)[C@@H](O)[C@H](C)O1)c(Cl)c2 '
               'NAME: oritavancin bisphosphate REASON: WRONGLY CLASSIFIED '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: Oc1c(Cl)cc(cc1Cl)-c1ccc(Cl)cc1 NAME: '
               "4,3',5'-Trichloro-4'-biphenol REASON: WRONGLY CLASSIFIED "
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'C[C@@H]1O[C@H](C[C@](C)(NCc2ccc(cc2)-c2ccc(Cl)cc2)[C@@H]1O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1Oc1c2Oc3ccc(cc3Cl)[C@@H](O)[C@@H](N)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H]3c(c2)cc1Oc1ccc(cc1Cl)[C@@H](O)[C@@H]1NC(=O)[C@H](NC3=O)c2ccc(O)c(c2)-c2c(O)cc(O)cc2[C@H](NC1=O)C(O)=O '
               'NAME: Chlorobiphenyl-desleucyl-vancomycin REASON: WRONGLY '
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'N[C@@H]1c2ccc(O)c(Oc3cc(O)cc(c3)[C@@H]3NC(=O)[C@H](Cc4ccc(Oc5cc6cc(Oc7ccc(cc7Cl)[C@@H](O)[C@@H]7NC(=O)[C@H](NC(=O)[C@@H]6NC3=O)c3cc(Cl)c(O)c(c3)-c3c(O)cc(O)cc3[C@@H](NC7=O)C(O)=O)c5O)c(Cl)c4)NC1=O)c2 '
               'NAME: A41030A REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C(C)C(=C1O)C=2C3=C(O)C=4C(=O)C5=C(O)C(Cl)=C(OC)C=C5C(C4C=C3C(Cl)=C(C2)O)(C)C '
               'NAME: Streptovertimycin H REASON: WRONGLY CLASSIFIED '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'CS(=O)(=O)c1cc(Cl)c(cc1Cl)-c1cc(Cl)c(cc1Cl)S(C)(=O)=O NAME: '
               "2,2',5,5'-tetrachloro-4,4'-bis(methylsulfonyl)biphenyl REASON: "
               'WRONGLY CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl '
               'core with aromatic-bound halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C(C)C(=C1O)C=2C3=C(O)C=4C(=O)C5=C(O)C(Cl)=C(OC)C=C5C(C4C=C3C=C(C2)O)(C)C '
               'NAME: Streptovertimycin F REASON: WRONGLY CLASSIFIED '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'CN[C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O[C@H]5C[C@](C)(N)[C@@H](O)[C@H](C)O5)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C(O)=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)(NCc3ccc(cc3)-c3ccc(Cl)cc3)[C@@H](O)[C@H](C)O1)c(Cl)c2 '
               'NAME: oritavancin REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Oc1c(Cl)cc(cc1Cl)-c1cc(Cl)ccc1Cl NAME: '
               "4-hydroxy-2',3,5,5'-tetrachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               '[H][C@@]12NC(=O)[C@H](NC(=O)[C@@H](Cc3c[nH]c4cc(ccc34)-c3cc1cc(Oc1ccc(C[C@H](N(C)C(=O)[C@H](NC2=O)c2cc(Cl)c(O)c(Cl)c2)C(=O)N[C@@H](C(O)=O)c2ccc(O)cc2)cc1)c3O)NC(=O)C(=O)c1cc(Cl)c(O)c(Cl)c1)c1cc(Cl)c(O)c(Cl)c1 '
               'NAME: chloropeptin II REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: '
               'CN1[C@@H](Cc2ccc(Oc3cc4cc(-c5ccc6c(C[C@@H](NC(=O)C(=O)c7cc(Cl)c(O)c(Cl)c7)C(=O)N[C@@H](C(=O)N[C@H]4C(=O)N[C@@H](C1=O)c1cc(Cl)c(O)c(Cl)c1)c1cc(Cl)c(O)c(Cl)c1)c[nH]c6c5)c3O)cc2)C(=O)N[C@@H](C(O)=O)c1ccc(O)cc1 '
               'NAME: isocomplestatin REASON: WRONGLY CLASSIFIED Halogenated '
               'dioxin/dibenzofuran/biphenyl core with aromatic-bound '
               'halogens\n'
               ' * SMILES: Oc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl NAME: '
               "4-Hydroxy-2,2',4',5,5'-pentachlorobiphenyl REASON: WRONGLY "
               'CLASSIFIED Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               ' * SMILES: '
               'ClC1=C(O)C(Cl)=C2C(C3=CC4=C(Cl)C(O)=CC(=C4C(=C3C(C2=C1O)=O)O)C5=C(OC)C=C(O)C(=C5C)Cl)(C)C '
               'NAME: Naphthacemycin B12 REASON: WRONGLY CLASSIFIED '
               'Halogenated dioxin/dibenzofuran/biphenyl core with '
               'aromatic-bound halogens\n'
               'False negatives: SMILES: Clc1ccc(cc1)-c1ccc(Cl)cc1 NAME: '
               "4,4'-dichlorobiphenyl REASON: MISSED Insufficient halogens (2 "
               'found, minimum 3)\n'
               ' * SMILES: Clc1cc(Cl)cc(c1)-c1ccccc1 NAME: '
               '3,5-dichlorobiphenyl REASON: MISSED Insufficient halogens (2 '
               'found, minimum 3)\n'
               " * SMILES: Clc1ccc(cc1)-c1ccccc1Cl NAME: 2,4'-dichlorobiphenyl "
               'REASON: MISSED Insufficient halogens (2 found, minimum 3)\n'
               ' * SMILES: Clc1cccc(Cl)c1-c1ccccc1 NAME: 2,6-dichlorobiphenyl '
               'REASON: MISSED Insufficient halogens (2 found, minimum 3)\n'
               ' * SMILES: '
               'ClC1=C(OC)C=C(C2=C(OC)C=C(OC)C(=C2C)Cl)C3=C1C[C@@H]4C(C=5C=C(O)C=C(C5C([C@@]4(C3=O)O)=O)O)(C)C '
               'NAME: Formicamycin Q REASON: MISSED Insufficient halogens (2 '
               'found, minimum 3)\n'
               ' * SMILES: Clc1ccc(Cl)c(c1)-c1ccccc1 NAME: '
               '2,5-dichlorobiphenyl REASON: MISSED Insufficient halogens (2 '
               'found, minimum 3)\n'
               ' * SMILES: '
               'OC1=C(C=C(C=C1[N+]([O-])=O)Cl)C2=C(O)C([N+](=O)[O-])=CC(=C2)Cl '
               'NAME: niclofolan REASON: MISSED Insufficient halogens (2 '
               'found, minimum 3)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCO[C@@H]1[C@H]([C@@H](C=C(O1)C(=O)NCC#C)C2CC2)CCCO',
                                     'name': '(2S,3S,4R)-4-cyclopropyl-2-ethoxy-3-(3-hydroxypropyl)-N-prop-2-ynyl-3,4-dihydro-2H-pyran-6-carboxamide',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'CCN(CC)CCCN1C(C(C(=O)C1=O)C(=O)C2=CC3=C(O2)C(=CC=C3)OC)C4=CC=NC=C4',
                                     'name': 'LSM-33458',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'C1=CC=NC(=C1)CC(=O)N[C@H]2C=C[C@@H](O[C@H]2CO)CC(=O)NCCC3=CC=NC=C3',
                                     'name': '2-[(2R,3S,6S)-2-(hydroxymethyl)-3-[[1-oxo-2-(2-pyridinyl)ethyl]amino]-3,6-dihydro-2H-pyran-6-yl]-N-(2-pyridin-4-ylethyl)acetamide',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'O=C(O)C1=C(NC(=O)CN(C(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](N(C(=O)[C@@H](N(C(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](N(C(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](N)C)[C@@H](O)C)C)[C@@H](O)C)C)C(C)C)C(C)C)C)C(C)C)C)C(C)C)C)C(C)C)C(CC)C)C)C(C)C)C)C=CC=C1',
                                     'name': 'Dictyonamide A',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'SC[C@H](NC(=O)[C@@H](N)CCCCN)C(=O)N[C@@H](CCC(=O)N)C(O)=O',
                                     'name': 'Lys-Cys-Gln',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)[C@@H](C(=O)N[C@@H](CCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(N(C1=C)C)=O)C(=O)O)=O)C)C=CC(=C[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)C)=O)C)CCCC3=CC=C(O)C=C3)C',
                                     'name': '(5R,8S,11R,12S,15S,18S,19S,22R)-15-[3-(diaminomethylideneamino)propyl]-8-[3-(4-hydroxyphenyl)propyl]-18-[(5S,6S)-6-methoxy-3,5-dimethyl-7-phenylhepta-1,3-dienyl]-1,5,12,19-tetramethyl-2-methylidene-3,6,9,13,16,20,25-heptaoxo-1,4,7,10,14,17,21-heptazacyclopentacosane-11,22-dicarboxylic '
                                             'acid',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'C1CCN(C1)CC(=O)NC2=CC=C(C=C2)OC3=CC=C(C=C3)NC(=O)CN4CCCC4',
                                     'name': 'N-[4-[4-[[1-oxo-2-(1-pyrrolidinyl)ethyl]amino]phenoxy]phenyl]-2-(1-pyrrolidinyl)acetamide',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC(=O)N)C(O)=O)C',
                                     'name': 'Tyr-Asn-Met',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'CCC(=O)N[C@H]1CC[C@@H](O[C@@H]1CO)CC(=O)OC',
                                     'name': '2-[(2R,5S,6S)-6-(hydroxymethyl)-5-(1-oxopropylamino)-2-oxanyl]acetic '
                                             'acid methyl ester',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)CC3=CC=CC=C3)[C@H](C)CO)C)CN(C)C(=O)NC(C)C',
                                     'name': 'N-[(3R,9S,10S)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-9-[[methyl-[oxo-(propan-2-ylamino)methyl]amino]methyl]-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]-2-phenylacetamide',
                                     'reason': 'Insufficient halogens (0 '
                                               'found, minimum 2)'}],
    'sample_false_negatives': [   {   'smiles': 'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(C3=C(O)C(Cl)=CC(=C3)Cl)=CC(=C1O)Cl',
                                      'name': 'Ambigol E',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin J',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(O)C(Cl)=C2C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C(C2=C1O)=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin I',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(O)=CC(=C1C3=C(O)C(Cl)=CC(=C3)Cl)Cl',
                                      'name': 'Ambigol D',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(O)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin D',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(OC)C=C(C2=C(OC)C=C(OC)C(=C2C)Cl)C3=C1C[C@@H]4C(C=5C=C(O)C=C(C5C([C@@]4(C3=O)O)=O)O)(C)C',
                                      'name': 'Formicamycin Q',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(O)C=2C(=O)[C@]3(O)C(=O)C4=C(C5=C(OC)C=C(OC)C(=C5C)Cl)C=C(OC)C(=C4C[C@@H]3C(C2C=C1O)(C)C)Cl',
                                      'name': 'Formicamycin F',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'BrC1=C(O)C(Cl)=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin L',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'OC1=C(C=C(C=C1[N+]([O-])=O)Cl)C2=C(O)C([N+](=O)[O-])=CC(=C2)Cl',
                                      'name': 'niclofolan',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'},
                                  {   'smiles': 'ClC1=C(O)C=C(O)C2=C1C([C@H]3CC=4C(Cl)=C(OC)C=C(C4C([C@]3(C2=O)O)=O)C5=C(OC)C=C(OC)C(=C5C)Cl)(C)C',
                                      'name': 'Formicamycin E',
                                      'reason': 'No valid '
                                                'dioxin/dibenzofuran/biphenyl '
                                                'core with halogen-only '
                                                'substituents'}],
    'attempt': 2,
    'reasoning': '',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 46,
    'num_false_positives': 0,
    'num_true_negatives': 142244,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.8214285714285714,
    'f1': 0.9019607843137255,
    'accuracy': 0.9999297259311314,
    'negative_predictive_value': 0.9999297032069397}