"""
Classifies: CHEBI:60027 polymer
"""
"""
Classifies: A polymer is defined as a mixture composed of macromolecules of different kinds,
which may be differentiated by composition, length, degree of branching etc.
This improved heuristic attempts to disregard small counterions and salts by requiring that
each fragment be “macromolecular” (e.g., above a certain molecular weight and heavy-atom count)
and by discarding fragments that are very small relative to the largest fragment.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polymer(smiles: str):
    """
    Determines if a given SMILES string represents a polymer – that is, a mixture of distinct
    macromolecular components.

    Heuristic improvements:
      1. Parse the SMILES and split it into disconnected fragments.
      2. Discard fragments that are too small to be considered macromolecules (require MW >= 200 Da
         and at least 10 heavy atoms).
      3. Discard fragments that, although meeting the basic criteria, are much smaller than the largest fragment.
         (For example, if one fragment is small enough to be a counterion, it will be ignored.)
      4. Among the remaining fragments, generate canonical SMILES and check whether there are at least
         two distinct entities.
         (If the mixture only contains multiple copies of the same fragment, it is more likely a salt than a polymer.)

    Args:
        smiles (str): SMILES string representing the substance.

    Returns:
        bool: True if classified as a polymer, False otherwise.
        str: Explanation for the classification decision.
    """

    # Parse the input; if invalid, return immediately.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Split the molecule into disconnected fragments.
    fragments = Chem.GetMolFrags(mol, asMols=True)

    # Allowed atomic numbers for common organic macromolecules
    allowed_atomic_nums = {1, 6, 7, 8, 9, 15, 16, 17, 35, 53}

    # Define a function that checks the “macromolecular” quality of a fragment.
    def is_macromolecular(frag):
        # Calculate molecular weight and count heavy atoms (exclude hydrogens)
        mw = rdMolDescriptors.CalcExactMolWt(frag)
        heavy_atoms = sum(1 for atom in frag.GetAtoms() if atom.GetAtomicNum() > 1)
        # Discard if below thresholds
        if mw < 200 or heavy_atoms < 10:
            return False
        # Disqualify a fragment if it contains atoms outside our allowed set.
        for atom in frag.GetAtoms():
            if atom.GetAtomicNum() not in allowed_atomic_nums:
                return False
        return True

    # First, filter fragments using the basic macromolecular criteria.
    candidate_frags = [frag for frag in fragments if is_macromolecular(frag)]
    if not candidate_frags:
        return False, "No fragment qualifies as a macromolecule based on MW and heavy atom count"

    # Now, determine the maximum MW among these candidates.
    frag_mws = [rdMolDescriptors.CalcExactMolWt(frag) for frag in candidate_frags]
    max_mw = max(frag_mws)

    # Discard fragments that are very small relative to the largest fragment
    # Here, we demand that the fragment's MW be at least 60% of the max; otherwise it is likely a counterion.
    filtered_frags = []
    for frag, mw in zip(candidate_frags, frag_mws):
        if mw >= 0.6 * max_mw:
            filtered_frags.append(frag)

    # If fewer than 2 remain, it is not a mixture of distinct macromolecules.
    if len(filtered_frags) < 2:
        return False, ("Does not meet the criteria for a polymer "
                       "(fewer than two sufficiently large macromolecular fragments)")

    # Create a set of canonical SMILES from the filtered fragments to check for chemical distinctness.
    unique_frag_smiles = set(Chem.MolToSmiles(frag, canonical=True) for frag in filtered_frags)
    if len(unique_frag_smiles) >= 2:
        return True, ("Detected a mixture of at least two distinct macromolecular components "
                      "(each with MW >=200 Da, at least 10 heavy atoms, and not much smaller than the largest fragment)")
    else:
        # If the fragments are chemically identical, this is more likely a salt than a polymer.
        return False, ("Multiple large fragments were found but they appear chemically identical; "
                       "this is more likely a salt rather than a polymer mixture")

# Example usage (uncomment to test):
# test_smiles = "C=1(N(C(N=C(N1)N)(C)C)C=2C=CC(=CC2)Cl)N.C3=CC=CC4=C3C=C(C(=C4CC=5C6=C(C=C(C5O)C(=O)O)C=CC=C6)O)C(=O)O.C=7(N(C(N=C(N7)N)(C)C)C=8C=CC(=CC8)Cl)N"
# result, reason = is_polymer(test_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:60027',
                          'name': 'polymer',
                          'definition': 'A polymer is a mixture, which is '
                                        'composed of macromolecules of '
                                        'different kinds and which may be '
                                        'differentiated by composition, '
                                        'length, degree of branching etc..',
                          'parents': ['CHEBI:60004'],
                          'xrefs': ['Wikipedia:Polymer'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 65,
                           'log_lines_of_code': 4.174387269895637,
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
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 0],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetMolFrags',
                                                 'MolToSmiles',
                                                 'CalcExactMolWt'],
                           'methods_called_count': 7,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_polymer(smiles: str):',
                                       'is_macromolecular(frag):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False',
                                          'False',
                                          'True',
                                          'False, "No fragment qualifies as a '
                                          'macromolecule based on MW and heavy '
                                          'atom count"',
                                          'False, ("Does not meet the criteria '
                                          'for a polymer "',
                                          'True, ("Detected a mixture of at '
                                          'least two distinct macromolecular '
                                          'components "',
                                          'False, ("Multiple large fragments '
                                          'were found but they appear '
                                          'chemically identical; "'],
                           'returns_count': 8,
                           'complexity': 5.034877453979127},
    'message': '\n'
               'Attempt failed: F1 score of 0.024691358024691357 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C=1(N(C(N=C(N1)N)(C)C)C=2C=CC(=CC2)Cl)N.C3=CC=CC4=C3C=C(C(=C4CC=5C6=C(C=C(C5O)C(=O)O)C=CC=C6)O)C(=O)O.C=7(N(C(N=C(N7)N)(C)C)C=8C=CC(=CC8)Cl)N '
               'NAME: Cycloguanil pamoate REASON: CORRECT Detected a mixture '
               'of at least two distinct macromolecular components (each with '
               'molecular weight >=150 Da, at least 5 heavy atoms, and '
               'composed of common organic elements)\n'
               ' * SMILES: '
               'C=1C=C2C(N(C3=C2CN(C)CC3)CC4=CC=CC=C4)=CC1.C5=CC=C6C(=C5S(O)(=O)=O)C=CC=C6S(O)(=O)=O.C=7C=C8C(N(C9=C8CN(C)CC9)CC%10=CC=CC=C%10)=CC7 '
               'NAME: Mebhydrolin napadisilate REASON: CORRECT Detected a '
               'mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               'False positives: SMILES: '
               'O[C@@H]([C@H](O)C(O)=O)C(O)=O.Oc1ccc2C[C@H]3N(CC[C@@]4(CCCC[C@@]34O)c2c1)CC1CCC1 '
               'NAME: butorphanol D-tartrate REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'OC[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O.OC[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O.Clc1ccc(NC(=N)NC(=N)NCCCCCCNC(=N)NC(=N)Nc2ccc(Cl)cc2)cc1 '
               'NAME: chlorhexidine gluconate REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'N[C@@H](CCC(=O)N[C@@H](CS)C(=O)NCC(O)=O)C(O)=O.CCCCC[C@H](O)\\C=C\\[C@H]1C=CC(=O)[C@@H]1CCCCCCC(O)=O '
               'NAME: Gsh-prostaglandin A1 REASON: WRONGLY CLASSIFIED Detected '
               'a mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'OC(=O)CC(O)(CC(O)=O)C(O)=O.C[C@@H]1CCN(C[C@@H]1N(C)c1ncnc2[nH]ccc12)C(=O)CC#N '
               'NAME: tofacitinib citrate REASON: WRONGLY CLASSIFIED Detected '
               'a mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               '[C@]12([C@@]([C@@]3(C[C@]1(CC3)[H])[H])(C(N(C2=O)CCCCN4CCN(CC4)C5=NC=CC=N5)=O)[H])[H].C(=O)(O)C(CC(=O)O)(CC(=O)O)O '
               'NAME: tandospirone citrate REASON: WRONGLY CLASSIFIED Detected '
               'a mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'C=1C(=CC=CN1)C(=O)OCCN(CC)CC.C(CC(O)=O)(CC(O)=O)(C(O)=O)O '
               'NAME: Nicametate citrate REASON: WRONGLY CLASSIFIED Detected a '
               'mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)S(O)(=O)=O.C[C@H]1CC[C@H](CN1C(=O)C=C)NC1=C2C=CNC2=NC=N1 '
               'NAME: ritlecitinib tosylate REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'COc1cc(ccc1[N+]#N)[N+]([O-])=O.OS(=O)(=O)c1cccc2c(cccc12)S([O-])(=O)=O '
               'NAME: fast red B REASON: WRONGLY CLASSIFIED Detected a mixture '
               'of at least two distinct macromolecular components (each with '
               'molecular weight >=150 Da, at least 5 heavy atoms, and '
               'composed of common organic elements)\n'
               ' * SMILES: '
               'C1=C(C=CC(=C1)CNC(N(C2CCN(CC2)C)CC3=CC=C(C=C3)F)=O)OCC(C)C.OC([C@@H]([C@H](C(O)=O)O)O)=O.C1=C(C=CC(=C1)CNC(N(C2CCN(CC2)C)CC3=CC=C(C=C3)F)=O)OCC(C)C '
               'NAME: pimavanserin tartrate REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'C1=CC=CC(C[C@@H](C[C@@H]([C@@H](NC(=O)COC=2C(=CC=CC2C)C)CC3=CC=CC=C3)O)NC(=O)[C@H](C(C)C)N4CCCNC4=O)=C1.[C@H](CC1=CC=CC=C1)(C[C@@H]([C@H](CC2=CC=CC=C2)NC(OCC3=CN=CS3)=O)O)NC([C@@H](NC(N(CC=4N=C(C(C)C)SC4)C)=O)C(C)C)=O '
               'NAME: Kaletra REASON: WRONGLY CLASSIFIED Detected a mixture of '
               'at least two distinct macromolecular components (each with '
               'molecular weight >=150 Da, at least 5 heavy atoms, and '
               'composed of common organic elements)\n'
               ' * SMILES: '
               '[Gd+3].CNC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO.CNC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO.OC(=O)CN(CCN(CCN(CC(O)=O)CC([O-])=O)CC([O-])=O)CC([O-])=O '
               'NAME: gadopentetate dimeglumine REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'C12=CC=CC3=C1C(C4C(C2(C)C)CCC(C4[N+]#[C-])(C)C=C)=CN3.C1=CC=CC2=C1C(C3C(C(C)=C)CCC(C3[N+]#[C-])(C)C=C)=CN2 '
               'NAME: hapalindole REASON: WRONGLY CLASSIFIED Detected a '
               'mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'OC(=O)CC(O)(CC(O)=O)C(O)=O.CCCc1nn(C)c2c1nc([nH]c2=O)-c1cc(ccc1OCC)S(=O)(=O)N1CCN(C)CC1 '
               'NAME: sildenafil citrate REASON: WRONGLY CLASSIFIED Detected a '
               'mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'CN1C(=O)C2=C(N=C(N2)Cl)N(C1=O)C(=O)O.CN(C)CCOC(C1=CC=CC=C1)C2=CC=CC=C2 '
               'NAME: 8-chloro-1-methyl-2,6-dioxo-7H-purine-3-carboxylic acid '
               '2-(diphenylmethyl)oxy-N,N-dimethylethanamine REASON: WRONGLY '
               'CLASSIFIED Detected a mixture of at least two distinct '
               'macromolecular components (each with molecular weight >=150 '
               'Da, at least 5 heavy atoms, and composed of common organic '
               'elements)\n'
               ' * SMILES: '
               '[O-]S(=O)(=O)c1ccccc1.[O-]S(=O)(=O)c1ccccc1.COc1ccc(CC2c3cc(OC)c(OC)cc3CC[N+]2(C)CCC(=O)OCCCCCOC(=O)CC[N+]2(C)CCc3cc(OC)c(OC)cc3C2Cc2ccc(OC)c(OC)c2)cc1OC '
               'NAME: atracurium besylate REASON: WRONGLY CLASSIFIED Detected '
               'a mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'CN1[C@]2(CC[C@]1([H])[C@@]([C@](C2)(C3=CC=CC=C3)[H])([H])C(=O)OC)[H].C(C(C(=O)O)O)(C(=O)O)O '
               'NAME: D-CPT tartrate REASON: WRONGLY CLASSIFIED Detected a '
               'mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'C[C@H]([C@@H]1CC[C@H]([C@H](O1)O[C@@H]2[C@H](C[C@H]([C@@H]([C@H]2O)O[C@@H]3[C@@H]([C@H]([C@@](CO3)(C)O)NC)O)N)N)N)N.C[C@H]([C@@H]1CC[C@H]([C@H](O1)O[C@@H]2[C@H](C[C@H]([C@@H]([C@H]2O)O[C@@H]3[C@@H]([C@H]([C@@](CO3)(C)O)NC)O)N)N)N)NC.C[C@@]1(CO[C@@H]([C@@H]([C@H]1NC)O)O[C@H]2[C@@H](C[C@@H]([C@H]([C@@H]2O)O[C@@H]3[C@@H](CC[C@H](O3)CN)N)N)N)O '
               'NAME: '
               '(2R,3R,4R,5R)-2-[(1S,2S,3R,4S,6R)-4,6-diamino-3-[[(2R,3R,6S)-3-amino-6-[(1R)-1-aminoethyl]-2-oxanyl]oxy]-2-hydroxycyclohexyl]oxy-5-methyl-4-(methylamino)oxane-3,5-diol '
               '(2R,3R,4R,5R)-2-[(1S,2S,3R,4S,6R)-4,6-diamino-3-[[(2R,3R,6S)-3-amino-6-(aminomethyl)-2-oxanyl]oxy]-2-hydroxycyclohexyl]oxy-5-methyl-4-(methylamino)oxane-3,5-diol '
               '(2R,3R,4R,5R)-2-[(1S,2S,3R,4S,6R)-4,6-diamino-3-[[(2R,3R,6S)-3-amino-6-[(1R)-1-(methylamino)ethyl]-2-oxanyl]oxy]-2-hydroxycyclohexyl]oxy-5-methyl-4-(methylamino)oxane-3,5-diol '
               'REASON: WRONGLY CLASSIFIED Detected a mixture of at least two '
               'distinct macromolecular components (each with molecular weight '
               '>=150 Da, at least 5 heavy atoms, and composed of common '
               'organic elements)\n'
               ' * SMILES: '
               'CCCCC[C@H](O)\\C=C\\[C@H]1[C@H](O)CC(=O)[C@@H]1CCCCCCC(O)=O.OC[C@H]1O[C@@H]2O[C@@H]3[C@@H](CO)O[C@H](O[C@@H]4[C@@H](CO)O[C@H](O[C@@H]5[C@@H](CO)O[C@H](O[C@@H]6[C@@H](CO)O[C@H](O[C@@H]7[C@@H](CO)O[C@H](O[C@H]1[C@H](O)[C@H]2O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O '
               'NAME: Alprostadil alfadex REASON: WRONGLY CLASSIFIED Detected '
               'a mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'N[C@@H](CCCNC(N)=N)C(O)=O.C[C@H](CS)C(=O)N1C[C@H](C[C@H]1C(O)=O)Sc1ccccc1 '
               'NAME: zofenoprilat arginine REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'Cc1ccc(cc1)S([O-])(=O)=O.Cc1ccc(cc1)S([O-])(=O)=O.Cc1ccc(cc1)S([O-])(=O)=O.Cc1ccc(cc1)S([O-])(=O)=O.C[n+]1ccc(cc1)-c1c2ccc(n2)c(-c2cc[n+](C)cc2)c2ccc([nH]2)c(-c2cc[n+](C)cc2)c2ccc(n2)c(-c2cc[n+](C)cc2)c2ccc1[nH]2 '
               'NAME: meso-tetrakis(N-methyl-4-pyridyl)porphine '
               'tetrakis(p-toluenesulfonate) REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'O[C@H]([C@@H](O)C(O)=O)C(O)=O.CN(C)C(=O)Cc1c(nc2ccc(C)cn12)-c1ccc(C)cc1.CN(C)C(=O)Cc1c(nc2ccc(C)cn12)-c1ccc(C)cc1 '
               'NAME: zolpidem tartrate REASON: WRONGLY CLASSIFIED Detected a '
               'mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: CCCC(C)c1cccc(OC(=O)NC)c1.CCC(CC)c1cccc(OC(=O)NC)c1 '
               'NAME: Bufencarb REASON: WRONGLY CLASSIFIED Detected a mixture '
               'of at least two distinct macromolecular components (each with '
               'molecular weight >=150 Da, at least 5 heavy atoms, and '
               'composed of common organic elements)\n'
               ' * SMILES: '
               '[O-]S(=O)(=O)c1ccccc1.[O-]S(=O)(=O)c1ccccc1.COc1ccc(C[C@@H]2c3cc(OC)c(OC)cc3CC[N@+]2(C)CCC(=O)OCCCCCOC(=O)CC[N@@+]2(C)CCc3cc(OC)c(OC)cc3[C@H]2Cc2ccc(OC)c(OC)c2)cc1OC '
               'NAME: cisatracurium besylate REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               ' * SMILES: '
               'CNC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO.OC(=O)c1ccc2nc(oc2c1)-c1cc(Cl)cc(Cl)c1 '
               'NAME: tafamidis meglumine REASON: WRONGLY CLASSIFIED Detected '
               'a mixture of at least two distinct macromolecular components '
               '(each with molecular weight >=150 Da, at least 5 heavy atoms, '
               'and composed of common organic elements)\n'
               ' * SMILES: '
               'C1(C2(C(OCC)=O)CCCN(CC2)C)=CC=CC=C1.C(CC(O)=O)(CC(O)=O)(C(O)=O)O '
               'NAME: Ethoheptazine citrate REASON: WRONGLY CLASSIFIED '
               'Detected a mixture of at least two distinct macromolecular '
               'components (each with molecular weight >=150 Da, at least 5 '
               'heavy atoms, and composed of common organic elements)\n'
               'False negatives: SMILES: '
               'C1(=C(C=C2C(=C1)C3=C(N2)[C@]4(C[C@@]5(C(=CO[C@H]([C@@]5(CN4CC3)[H])C)C(OCCN(C)C)=O)[H])[H])OC)OC.Cl.Cl '
               'NAME: Dimethylaminoethyl reserpilinate dihydrochloride REASON: '
               'MISSED Does not meet the criteria for a polymer (fewer than '
               'two distinct macromolecular fragments)\n'
               ' * SMILES: '
               'C1CNCCN1.OC(CC(CC(=O)O)(O)C(=O)O)=O.C2CNCCN2.C3CNCCN3.OC(CC(CC(=O)O)(O)C(=O)O)=O '
               'NAME: Piperazine citrate REASON: MISSED Multiple large '
               'fragments were found but they appear chemically identical; '
               'this is more likely a salt rather than a polymer mixture\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC/C=C\\CCCCCCCCCCCCC/C=C/CCCCCCCCCCCCCCCCCC(C(C(=O)O)CCCCCCCCCCCCCCCCCCCCCC)O '
               'NAME: alpha-Semegma mycolic acid REASON: MISSED Does not meet '
               'the criteria for a polymer (fewer than two distinct '
               'macromolecular fragments)\n'
               ' * SMILES: '
               '[N+](O)(=O)[O-].C=1C=C2C(C(C=3[C@@](C[C@]4([H])[C@](C3O)(C(=O)C(=C(O)[C@H]4N(C)C)C(=O)NCN5CCCC5)O)([H])[C@]2(C)O)=O)=C(C1)O.O.[N+](O)(=O)[O-].C=6C=C7C(C(C=8[C@@](C[C@]9([H])[C@](C8O)(C(=O)C(=C(O)[C@H]9N(C)C)C(=O)NCN%10CCCC%10)O)([H])[C@]7(C)O)=O)=C(C6)O.O.O '
               'NAME: Rolitetracycline nitrate REASON: MISSED Multiple large '
               'fragments were found but they appear chemically identical; '
               'this is more likely a salt rather than a polymer mixture\n'
               ' * SMILES: '
               'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O '
               'NAME: ditrans,polycis-octaprenyl diphosphate REASON: MISSED '
               'Does not meet the criteria for a polymer (fewer than two '
               'distinct macromolecular fragments)\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H](OC([C@@H]1NC(C)=O)OP(OP(OC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)(O)=O)(O)=O)CO)O[C@H]2[C@@H]([C@H]([C@H](O)[C@H](O2)CO)O)NC(C)=O)OC(C(N[C@H](C(NC(CCC(N[C@H](C(N[C@@H](C(N[C@@H](C(O)=O)C)=O)C)=O)CCCCNC([C@@H](NC([C@@H](N)C)=O)C)=O)=O)C(O)=O)=O)C)=O)C '
               'NAME: '
               'Undecaprenyl-diphospho-N-acetylmuramoyl-(N-acetylglucosamine)-L-alanyl-gamma-D-glutamyl-L-lysyl-(L-alanyl-L-alanyl)-D-alanyl-D-alanine '
               'REASON: MISSED Does not meet the criteria for a polymer (fewer '
               'than two distinct macromolecular fragments)\n'
               ' * SMILES: '
               '[As](=O)([O-])([O-])[O-].[Ca+2].[Ca+2].[Ca+2].[As](=O)([O-])([O-])[O-] '
               'NAME: Calcium arsenate REASON: MISSED Does not meet the '
               'criteria for a polymer (fewer than two distinct macromolecular '
               'fragments)\n'
               ' * SMILES: '
               'C1=CC(=C2C(=C1O)N=CC=C2)C(=O)C.S(=O)(=O)(O)O.C3=CC(=C4C(=C3O)N=CC=C4)C(=O)C '
               'NAME: Quinacetol sulfate REASON: MISSED Multiple large '
               'fragments were found but they appear chemically identical; '
               'this is more likely a salt rather than a polymer mixture\n'
               ' * SMILES: '
               'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O '
               'NAME: ditrans,polycis-hexaprenyl diphosphate REASON: MISSED '
               'Does not meet the criteria for a polymer (fewer than two '
               'distinct macromolecular fragments)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\Cc1ccccc1O '
               'NAME: 2-all-trans-heptaprenylphenol REASON: MISSED Does not '
               'meet the criteria for a polymer (fewer than two distinct '
               'macromolecular fragments)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'No fragment qualifies as a '
                                               'macromolecule based on MW and '
                                               'heavy atom count'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'Does not meet the criteria for '
                                               'a polymer (fewer than two '
                                               'sufficiently large '
                                               'macromolecular fragments)'}],
    'sample_false_negatives': [   {   'smiles': 'C1(=C(C=C2C(=C1)C3=C(N2)[C@]4(C[C@@]5(C(=CO[C@H]([C@@]5(CN4CC3)[H])C)C(OCCN(C)C)=O)[H])[H])OC)OC.Cl.Cl',
                                      'name': 'Dimethylaminoethyl '
                                              'reserpilinate dihydrochloride',
                                      'reason': 'Does not meet the criteria '
                                                'for a polymer (fewer than two '
                                                'sufficiently large '
                                                'macromolecular fragments)'},
                                  {   'smiles': 'C1CNCCN1.OC(CC(CC(=O)O)(O)C(=O)O)=O.C2CNCCN2.C3CNCCN3.OC(CC(CC(=O)O)(O)C(=O)O)=O',
                                      'name': 'Piperazine citrate',
                                      'reason': 'No fragment qualifies as a '
                                                'macromolecule based on MW and '
                                                'heavy atom count'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCC/C=C\\CCCCCCCCCCCCC/C=C/CCCCCCCCCCCCCCCCCC(C(C(=O)O)CCCCCCCCCCCCCCCCCCCCCC)O',
                                      'name': 'alpha-Semegma mycolic acid',
                                      'reason': 'Does not meet the criteria '
                                                'for a polymer (fewer than two '
                                                'sufficiently large '
                                                'macromolecular fragments)'},
                                  {   'smiles': '[N+](O)(=O)[O-].C=1C=C2C(C(C=3[C@@](C[C@]4([H])[C@](C3O)(C(=O)C(=C(O)[C@H]4N(C)C)C(=O)NCN5CCCC5)O)([H])[C@]2(C)O)=O)=C(C1)O.O.[N+](O)(=O)[O-].C=6C=C7C(C(C=8[C@@](C[C@]9([H])[C@](C8O)(C(=O)C(=C(O)[C@H]9N(C)C)C(=O)NCN%10CCCC%10)O)([H])[C@]7(C)O)=O)=C(C6)O.O.O',
                                      'name': 'Rolitetracycline nitrate',
                                      'reason': 'Multiple large fragments were '
                                                'found but they appear '
                                                'chemically identical; this is '
                                                'more likely a salt rather '
                                                'than a polymer mixture'},
                                  {   'smiles': 'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O',
                                      'name': 'ditrans,polycis-octaprenyl '
                                              'diphosphate',
                                      'reason': 'Does not meet the criteria '
                                                'for a polymer (fewer than two '
                                                'sufficiently large '
                                                'macromolecular fragments)'},
                                  {   'smiles': '[C@@H]1([C@@H]([C@H](OC([C@@H]1NC(C)=O)OP(OP(OC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\C)/CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)(O)=O)(O)=O)CO)O[C@H]2[C@@H]([C@H]([C@H](O)[C@H](O2)CO)O)NC(C)=O)OC(C(N[C@H](C(NC(CCC(N[C@H](C(N[C@@H](C(N[C@@H](C(O)=O)C)=O)C)=O)CCCCNC([C@@H](NC([C@@H](N)C)=O)C)=O)=O)C(O)=O)=O)C)=O)C',
                                      'name': 'Undecaprenyl-diphospho-N-acetylmuramoyl-(N-acetylglucosamine)-L-alanyl-gamma-D-glutamyl-L-lysyl-(L-alanyl-L-alanyl)-D-alanyl-D-alanine',
                                      'reason': 'Does not meet the criteria '
                                                'for a polymer (fewer than two '
                                                'sufficiently large '
                                                'macromolecular fragments)'},
                                  {   'smiles': '[As](=O)([O-])([O-])[O-].[Ca+2].[Ca+2].[Ca+2].[As](=O)([O-])([O-])[O-]',
                                      'name': 'Calcium arsenate',
                                      'reason': 'No fragment qualifies as a '
                                                'macromolecule based on MW and '
                                                'heavy atom count'},
                                  {   'smiles': 'C1=CC(=C2C(=C1O)N=CC=C2)C(=O)C.S(=O)(=O)(O)O.C3=CC(=C4C(=C3O)N=CC=C4)C(=O)C',
                                      'name': 'Quinacetol sulfate',
                                      'reason': 'No fragment qualifies as a '
                                                'macromolecule based on MW and '
                                                'heavy atom count'},
                                  {   'smiles': 'C(\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)C\\C(\\C)=C/CC\\C(\\C)=C/CC\\C(\\C)=C/COP(OP(O)(O)=O)(O)=O',
                                      'name': 'ditrans,polycis-hexaprenyl '
                                              'diphosphate',
                                      'reason': 'Does not meet the criteria '
                                                'for a polymer (fewer than two '
                                                'sufficiently large '
                                                'macromolecular fragments)'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\Cc1ccccc1O',
                                      'name': '2-all-trans-heptaprenylphenol',
                                      'reason': 'Does not meet the criteria '
                                                'for a polymer (fewer than two '
                                                'sufficiently large '
                                                'macromolecular fragments)'}],
    'attempt': 3,
    'reasoning': 'Below is one way to improve the heuristic. In the original '
                 'code the “large‐fragment” cutoff was too lenient so that '
                 'common inorganic counterions (or salts) were passing the '
                 'filter. Also, the code did not account for the relative size '
                 'differences among fragments. A possible improvement is to '
                 '(a) require a higher minimum molecular weight and heavy‐atom '
                 'count (since a “macromolecule” should be fairly large) and '
                 '(b) remove fragments that are very small relative to the '
                 'largest fragment (since counterions are usually much '
                 'smaller). For example, we may require each fragment to have '
                 '(roughly) MW ≥200 Da and at least 10 heavy atoms and then '
                 'discard any fragment whose MW is less than about 60% of the '
                 'largest fragment’s MW. Finally, we count the fragments (by '
                 'canonical SMILES) and if at least two distinct (and large '
                 'enough) fragments remain, we classify the input as a polymer '
                 '(i.e. a mixture of macromolecules). \n'
                 '\n'
                 'Below is the complete Python code implementing this improved '
                 'heuristic:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 41,
    'num_true_negatives': 142228,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.046511627906976744,
    'recall': 0.06451612903225806,
    'f1': 0.05405405405405405,
    'accuracy': 0.9995080815179199,
    'negative_predictive_value': 0.9997961435992605}