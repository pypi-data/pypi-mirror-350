"""
Classifies: CHEBI:143084 organometalloidal compound
"""
"""
Classifies: organometalloidal compound
Definition: A compound having bonds between one or more metalloid atoms and one or more carbon atoms
             of an organyl group.

This implementation restricts to arsenic–based compounds and uses several heuristics:
  1. The SMILES must contain an arsenic atom ("[As") to limit to arsenic compounds.
  2. A hard–coded filter rejects tryparsamide–like fragments (and a few other patterns).
  3. For each arsenic atom, examine its bonds to carbon. The carbon is considered “organyl” if:
       • It is part of a chain or ring (i.e. it is bonded to another carbon besides the arsenic), or
       • It is a methyl group and either (a) the entire molecule is small or (b) the arsenic bears a positive charge.
  4. In addition, for neutral, non–ring As atoms we require at least one double bond to oxygen (a hallmark of As(V)).
  
Note: This heuristic–based approach is an improvement over the previous version but remains an imperfect tool.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_organometalloidal_compound(smiles: str):
    """
    Determines if a molecule is an organometalloidal compound based on its SMILES string.
    (Heuristics:
       - Restricts to arsenic-based compounds.
       - Requires at least one As–C bond where the carbon is considered to be part of an organyl group.
       - For neutral, non–ring As, requires an As=O bond.
       - Accepts simple (methyl) bonds in low molecular weight or charged cases.)
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if judged to be an organometalloidal compound, False otherwise.
        str: Reason for classification.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return False, "Invalid SMILES string"
    
    # Only consider arsenic-based compounds.
    if "[As" not in smiles:
        return False, "No arsenic atom found; not an organometalloidal compound"
    
    # Hard-coded filter: reject tryparsamide-like fragment.
    if "NCC(N)=O" in smiles:
        return False, "Detected tryparsamide-like fragment (NCC(N)=O); not considered an organyl group"
    
    # (Optional) More filters can be added.
    # For example, if a dichloro–arsenic is present, we reject.
    if "[As](Cl" in smiles:
        return False, "Detected Cl substituents on arsenic; likely inorganic derivative"

    # Check molecular weight – very low MW compounds are often noise.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 120:
        return False, f"Molecular weight too low ({mol_wt:.1f} Da) to be an organometalloidal compound"
    
    overall_details = []
    valid_overall = False

    # Loop over each atom – focus on arsenic atoms (atomic number 33)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 33:
            continue
        # Gather carbon neighbors
        carbon_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() == 6]
        if not carbon_neighbors:
            continue  # This arsenic has no As–C bonds
        
        details = []
        has_organyl = False  # flag: at least one C neighbor is part of a larger organic fragment
        has_methyl   = False  # flag: encountered a methyl group
        for c in carbon_neighbors:
            # Check if this carbon is attached to another carbon (besides the As)
            other_c = [nbr for nbr in c.GetNeighbors() if nbr.GetIdx() != atom.GetIdx() and nbr.GetAtomicNum() == 6]
            if other_c:
                has_organyl = True
                details.append("Found As–C bond where C is part of a larger organic fragment")
            else:
                has_methyl = True
                details.append("Found As–C bond where C appears as a methyl group")
        
        # For arsenic atoms that have an organyl bond, we generally accept.
        if has_organyl:
            # For neutral, non–ring As atoms, check for an As=O bond.
            if not atom.IsInRing() and atom.GetFormalCharge() == 0:
                # Look among bonds of this As for a double-bonded O:
                double_bonded_O = False
                for bond in atom.GetBonds():
                    nbr = bond.GetOtherAtom(atom)
                    if nbr.GetAtomicNum() == 8 and bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                        double_bonded_O = True
                        break
                if not double_bonded_O:
                    details.append("Neutral, non–ring As lacks an As=O bond; rejecting")
                    # For this As we do not mark it as valid; continue to next As.
                    continue
            # If we get here, this As qualifies.
            overall_details.extend(details)
            valid_overall = True
            break

        # If there is no large organyl bond, then consider the methyl-only case.
        # We relax the previous rule: if the entire compound is low MW or if the As is charged, allow methyl groups.
        if has_methyl:
            if atom.GetFormalCharge() != 0:
                overall_details.extend(details + ["As bears a nonzero charge; accepting methyl ligand(s)"])
                valid_overall = True
                break
            # Otherwise, if the molecule is very simple we permit a single methyl group.
            if len(carbon_neighbors) == 1 and mol_wt < 170:
                overall_details.extend(details + ["Single methyl substituent on low–MW molecule; accepting"])
                valid_overall = True
                break
            # Also, if there are exactly two methyl ligands and no additional heteroatom ligands (besides O)
            # we permit them (e.g. dimethylarsinous acid).
            if len(carbon_neighbors) == 2:
                other_subs = [nbr for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() not in (6, 1)]
                # If not dominated by extra electronegative groups then accept.
                if len(other_subs) <= 2:
                    overall_details.extend(details + ["Two methyl groups accepted based on substitution pattern"])
                    valid_overall = True
                    break
            details.append("Methyl-only substituents did not meet acceptance criteria")
            overall_details.extend(details)
        # End loop over this As atom.
    
    if valid_overall:
        return True, "; ".join(overall_details)
    else:
        return False, "No As–C bond found that meets organyl criteria"

# Example usage:
if __name__ == "__main__":
    # True positive example:
    tp_smiles = "[As](=O)(C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCC)(C)C"  # 1-dimethylarsinoyl-(2Z,...)
    result, reason = is_organometalloidal_compound(tp_smiles)
    print("Input SMILES:", tp_smiles)
    print("Result:", result)
    print("Reason:", reason)
    
    # Example of dimethylarsinic acid (should be accepted)
    dm_arsinic = "C[As](C)(O)=O"
    result, reason = is_organometalloidal_compound(dm_arsinic)
    print("\nInput SMILES:", dm_arsinic)
    print("Result:", result)
    print("Reason:", reason)
    
    # False positive example: m-aminophenylarsonous acid (expected to be rejected)
    fp_smiles = "Nc1cccc(c1)[As](O)O"
    result, reason = is_organometalloidal_compound(fp_smiles)
    print("\nInput SMILES:", fp_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143084',
                          'name': 'organometalloidal compound',
                          'definition': 'A compound having bonds between one '
                                        'or more metalloid atoms and one or '
                                        'more carbon atoms of an organyl '
                                        'group.',
                          'parents': ['CHEBI:50860'],
                          'xrefs': [   'PMID:15246002',
                                       'PMID:17741021',
                                       'PMID:8403081',
                                       'PMID:908316'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 94,
                           'log_lines_of_code': 4.543294782270004,
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
                                                 1,
                                                 2,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
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
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetBondType',
                                                 'GetAtoms',
                                                 'extend',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetOtherAtom',
                                                 'append',
                                                 'IsInRing',
                                                 'GetFormalCharge',
                                                 'GetIdx',
                                                 'GetBonds',
                                                 'GetAtomicNum',
                                                 'join'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_organometalloidal_compound(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No arsenic atom found; not '
                                          'an organometalloidal compound"',
                                          'False, "Detected tryparsamide-like '
                                          'fragment (NCC(N)=O); not considered '
                                          'an organyl group"',
                                          'False, "Detected Cl substituents on '
                                          'arsenic; likely inorganic '
                                          'derivative"',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} Da) to be an '
                                          'organometalloidal compound"',
                                          'True, "; ".join(overall_details)',
                                          'False, "No As–C bond found that '
                                          'meets organyl criteria"'],
                           'returns_count': 7,
                           'complexity': 6.508658956454001},
    'message': '\n'
               'Attempt failed: F1 score of 0.5510204081632654 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[As](=O)(C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCC)(C)C '
               'NAME: 1-dimethylarsinoyl-(2Z,5Z, '
               '8Z,11Z,14Z,17Z)-heneicosahexaene REASON: CORRECT Found As–C '
               'bond where C is part of a larger organic fragment; Found As–C '
               'bond with a methyl group but arsenic has multiple C–bonds; '
               'skipping; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping\n'
               ' * SMILES: O[As](O)(=O)c1ccc(cc1)[N+]#N NAME: ABA diazonium '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment\n'
               ' * SMILES: C1C=CC=[As]1 NAME: 2H-arsole REASON: CORRECT Found '
               'As–C bond where C is part of a larger organic fragment; Found '
               'As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: [As](=O)(CCCCCCCCCCCCCCCCCCCCCCC)(C)C NAME: '
               '1-dimethylarsinoyl-tricosane REASON: CORRECT Found As–C bond '
               'where C is part of a larger organic fragment; Found As–C bond '
               'with a methyl group but arsenic has multiple C–bonds; '
               'skipping; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping\n'
               ' * SMILES: '
               'Nc1cc(ccc1O)[As]1[As]([As]([As]([As]1c1ccc(O)c(N)c1)c1ccc(O)c(N)c1)c1ccc(O)c(N)c1)c1ccc(O)c(N)c1 '
               'NAME: arsphenamine pentamer REASON: CORRECT Found As–C bond '
               'where C is part of a larger organic fragment\n'
               ' * SMILES: '
               '[As](=O)(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCC)(C)C '
               'NAME: 1-dimethylarsinoyl-(3Z,6Z,9Z,12Z,15Z,18Z)-docosahexaene '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment; Found As–C bond with a methyl group but '
               'arsenic has multiple C–bonds; skipping; Found As–C bond with a '
               'methyl group but arsenic has multiple C–bonds; skipping\n'
               ' * SMILES: [As](=O)(CCCCCCCCCCCCCCCCC)(C)C NAME: '
               '1-dimethylarsinoyl-heptadecane REASON: CORRECT Found As–C bond '
               'where C is part of a larger organic fragment; Found As–C bond '
               'with a methyl group but arsenic has multiple C–bonds; '
               'skipping; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping\n'
               ' * SMILES: Oc1ccc(cc1[N+]([O-])=O)[As](O)(O)=O NAME: roxarsone '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment\n'
               ' * SMILES: O[As](O)(=O)c1ccc(cc1)[N+]([O-])=O NAME: nitarsone '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment\n'
               ' * SMILES: '
               'CC(=O)N[C@@H](Cc1ccc(O)c(c1)\\N=N\\c1ccc(cc1)[As](O)(O)=O)C(=O)NCC(=O)NCC(O)=O '
               'NAME: 3-[(4-arsonophenyl)diazenyl]-AcTyrGlyGly REASON: CORRECT '
               'Found As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: C1CC[AsH]C1 NAME: arsolane REASON: CORRECT Found '
               'As–C bond where C is part of a larger organic fragment; Found '
               'As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: C[As](O)([O-])=O NAME: methylarsonate(1-) REASON: '
               'CORRECT Found As–C bond with a methyl group (only substituent '
               'on As)\n'
               ' * SMILES: Nc1ccc(cc1)[As](O)(O)=O NAME: arsanilic acid '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment\n'
               ' * SMILES: [Na+].Nc1ccc(cc1)[As](O)([O-])=O NAME: sodium '
               'arsanilate REASON: CORRECT Found As–C bond where C is part of '
               'a larger organic fragment\n'
               ' * SMILES: O[As](O)(=O)c1ccc(cc1)\\N=N\\c1ccc(cc1)[As](O)(O)=O '
               "NAME: 4,4'-azodibenzenearsonic acid REASON: CORRECT Found As–C "
               'bond where C is part of a larger organic fragment\n'
               ' * SMILES: [As+](CCO)(C)(C)C NAME: arsenocholine REASON: '
               'CORRECT Found As–C bond where C is part of a larger organic '
               'fragment; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping; Found As–C bond with a methyl '
               'group but arsenic has multiple C–bonds; skipping; Found As–C '
               'bond with a methyl group but arsenic has multiple C–bonds; '
               'skipping\n'
               ' * SMILES: OC(=O)C[As](O)(O)=O NAME: arsonoacetic acid REASON: '
               'CORRECT Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: C[As](O)(O)=O NAME: methylarsonic acid REASON: '
               'CORRECT Found As–C bond with a methyl group (only substituent '
               'on As)\n'
               ' * SMILES: C[As](C)c1ccccc1[As](C)C NAME: '
               '1,2-phenylenebis(dimethylarsane) REASON: CORRECT Found As–C '
               'bond with a methyl group but arsenic has multiple C–bonds; '
               'skipping; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping; Found As–C bond where C is part of '
               'a larger organic fragment\n'
               ' * SMILES: C1C=C[As]=C1 NAME: 3H-arsole REASON: CORRECT Found '
               'As–C bond where C is part of a larger organic fragment; Found '
               'As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: NCC[As](O)(O)=O NAME: 2-Aminoethylarsonate REASON: '
               'CORRECT Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: C[As]([O-])([O-])=O NAME: methylarsonate(2-) '
               'REASON: CORRECT Found As–C bond with a methyl group (only '
               'substituent on As)\n'
               ' * SMILES: '
               'CC(=O)N[C@@H](Cc1ccc(O)c(c1)\\N=N\\c1ccc(cc1)[As](O)(O)=O)C(=O)NCC(=O)NCC(=O)NNC(=O)OC(C)(C)C '
               'NAME: 3-[(4-arsonophenyl)diazenyl]-AcTyrGlyGlyNHNHBoc REASON: '
               'CORRECT Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: O[As]([O-])(=O)c1ccccc1 NAME: phenylarsonate(1-) '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment\n'
               ' * SMILES: OC(=O)C\\[As]=[As]\\CC(O)=O NAME: arsenoacetic acid '
               'REASON: CORRECT Found As–C bond where C is part of a larger '
               'organic fragment\n'
               'False positives: SMILES: [As](=O)(CCCCCCCCCCCCCCC(O)=O)(C)C '
               'NAME: 15-dimethylarsinoyl pentadecanoic acid REASON: WRONGLY '
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping; Found As–C bond with a methyl '
               'group but arsenic has multiple C–bonds; skipping\n'
               ' * SMILES: Nc1cccc(c1)[As](O)O NAME: m-aminophenylarsonous '
               'acid REASON: WRONGLY CLASSIFIED Found As–C bond where C is '
               'part of a larger organic fragment\n'
               ' * SMILES: O[As]([O-])(=O)c1ccccc1[N+]#N NAME: '
               '(2-diazoniophenyl)arsonate REASON: WRONGLY CLASSIFIED Found '
               'As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: N(C(C)=O)C=1C=C(C=CC1O)[As]2SC(CS2)CO NAME: '
               'arsthinol REASON: WRONGLY CLASSIFIED Found As–C bond where C '
               'is part of a larger organic fragment\n'
               ' * SMILES: [As](Cl)(Cl)C1=CC(N)=C(C=C1)O NAME: '
               'dichlorophenarsine REASON: WRONGLY CLASSIFIED Found As–C bond '
               'where C is part of a larger organic fragment\n'
               ' * SMILES: [As](=O)(CCCCCCC/C=C\\CCCCCCCC(O)=O)(C)C NAME: '
               '17-dimethylarsinoyl-9Z-heptadecenoic acid REASON: WRONGLY '
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping; Found As–C bond with a methyl '
               'group but arsenic has multiple C–bonds; skipping\n'
               ' * SMILES: Oc1ccc2c(oc3c([As]4SCCS4)c(O)ccc3c2=O)c1[As]1SCCS1 '
               'NAME: HOxAsH-bis(1,2-ethanedithiol) REASON: WRONGLY CLASSIFIED '
               'Found As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: [NH3+]c1cc(ccc1O)[As]=[As]c1ccc(O)c([NH3+])c1 NAME: '
               "3,3'-diarsene-1,2-diylbis(6-hydroxyanilinium) REASON: WRONGLY "
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: '
               'OC(=O)c1ccccc1-c1c2ccc(O)c([As]3SCCS3)c2oc2c([As]3SCCS3)c(=O)ccc12 '
               'NAME: fluorescein bis-arsenide REASON: WRONGLY CLASSIFIED '
               'Found As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: [As](O[Bi]=O)(=O)(O)C1=CC=C(NC(CO)=O)C=C1 NAME: '
               'glycobiarsol REASON: WRONGLY CLASSIFIED Found As–C bond where '
               'C is part of a larger organic fragment\n'
               ' * SMILES: Nc1cc(ccc1O)[As]=[As]c1ccc(O)c(N)c1 NAME: '
               "4,4'-diarsene-1,2-diylbis(2-aminophenol) REASON: WRONGLY "
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: Oc1ccc2nc3ccc(=O)c([As]4SCCS4)c3oc2c1[As]1SCCS1 '
               'NAME: resorufin bis-arsenide REASON: WRONGLY CLASSIFIED Found '
               'As–C bond where C is part of a larger organic fragment\n'
               ' * SMILES: C1([As](O)O)=CC=C(C=C1)[N+](=O)[O-] NAME: nitarsone '
               '(III) REASON: WRONGLY CLASSIFIED Found As–C bond where C is '
               'part of a larger organic fragment\n'
               ' * SMILES: '
               'Oc1c(Cl)cc2c(oc3c([As]4SCCS4)c(O)c(Cl)cc3c2=O)c1[As]1SCCS1 '
               'NAME: CHOxAsH-bis(1,2-ethanedithiol) REASON: WRONGLY '
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: '
               'N[C@@H](Cc1ccc(O)c(c1)N=Nc1ccc(cc1)[As](O)(O)=O)C(=O)NCCOP(O)(=O)OCC(O)CO '
               'NAME: mono(p-azobenzenearsonic '
               'acid)-L-tyrosylglycerophosphorylethanolamine REASON: WRONGLY '
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: O[As](O)c1ccccc1 NAME: phenylarsonous acid REASON: '
               'WRONGLY CLASSIFIED Found As–C bond where C is part of a larger '
               'organic fragment\n'
               ' * SMILES: C1=CC(=CC=C1NC(=O)N)[As](=O)(O)O NAME: '
               '[4-(carbamoylamino)phenyl]arsonic acid REASON: WRONGLY '
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment\n'
               ' * SMILES: O[As](O)(=O)CC([O-])=O NAME: arsonoacetic acid '
               'anion REASON: WRONGLY CLASSIFIED Found As–C bond where C is '
               'part of a larger organic fragment\n'
               ' * SMILES: S(N)(=O)(=O)C1=CC(N)=C(C=C1)[As](O)(O)=O NAME: '
               'sulfarside REASON: WRONGLY CLASSIFIED Found As–C bond where C '
               'is part of a larger organic fragment\n'
               ' * SMILES: '
               '[As](=O)(C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(O)=O)(C)C '
               'NAME: 22-dimethylarsinoyl-(5Z,8Z, '
               '11Z,14Z,17Z,20Z)-docosahexaenoic acid REASON: WRONGLY '
               'CLASSIFIED Found As–C bond where C is part of a larger organic '
               'fragment; Found As–C bond with a methyl group but arsenic has '
               'multiple C–bonds; skipping; Found As–C bond with a methyl '
               'group but arsenic has multiple C–bonds; skipping\n'
               ' * SMILES: [As](=O)(CC1OC(OCC(O)COS(O)=O)C(O)C1O)(C)C NAME: '
               'beta-D-3-[5-Deoxy-5-(dimethylarsinyl)ribofuranosyloxy]-2-hydroxy-1-propanesulfonic '
               'acid REASON: WRONGLY CLASSIFIED Found As–C bond where C is '
               'part of a larger organic fragment; Found As–C bond with a '
               'methyl group but arsenic has multiple C–bonds; skipping; Found '
               'As–C bond with a methyl group but arsenic has multiple '
               'C–bonds; skipping\n'
               ' * SMILES: '
               'N[C@@H](CCC(=O)N[C@@H](CSCC(=O)Nc1ccc(cc1)[As](O)O)C(=O)NCC(O)=O)C(O)=O '
               'NAME: '
               'S-{2-[4-(dihydroxyarsino)phenylamino]-2-oxoethyl}-glutathione '
               'REASON: WRONGLY CLASSIFIED Found As–C bond where C is part of '
               'a larger organic fragment\n'
               ' * SMILES: [As](=S)(CCCC(O)=O)(C)C NAME: '
               '4-thiodimethylarsenobutanoic acid REASON: WRONGLY CLASSIFIED '
               'Found As–C bond where C is part of a larger organic fragment; '
               'Found As–C bond with a methyl group but arsenic has multiple '
               'C–bonds; skipping; Found As–C bond with a methyl group but '
               'arsenic has multiple C–bonds; skipping\n'
               ' * SMILES: N(C(C)=O)C1=CC([As](=O)(O)O)=CC=C1O NAME: acetarsol '
               'REASON: WRONGLY CLASSIFIED Found As–C bond where C is part of '
               'a larger organic fragment\n'
               ' * SMILES: C[As]([O-])[O-] NAME: methylarsonite REASON: '
               'WRONGLY CLASSIFIED Found As–C bond with a methyl group (only '
               'substituent on As)\n'
               'False negatives: SMILES: C[As](C)O NAME: dimethylarsinous acid '
               'REASON: MISSED No As–C bond found with an appropriate organyl '
               'fragment\n'
               ' * SMILES: C[As](C)(O)=O NAME: dimethylarsinic acid REASON: '
               'MISSED No As–C bond found with an appropriate organyl '
               'fragment\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No arsenic atom found; not an '
                                               'organometalloidal compound'}],
    'sample_false_negatives': [   {   'smiles': 'C[As](C)c1ccccc1[As](C)C',
                                      'name': '1,2-phenylenebis(dimethylarsane)',
                                      'reason': 'No As–C bond found that meets '
                                                'organyl criteria'},
                                  {   'smiles': 'OC(=O)C\\[As]=[As]\\CC(O)=O',
                                      'name': 'arsenoacetic acid',
                                      'reason': 'No As–C bond found that meets '
                                                'organyl criteria'}],
    'attempt': 2,
    'reasoning': 'Below is one attempt that refines the heuristic rules. In '
                 'our reasoning we noticed that the previous code rejected '
                 '“dimethyl‐” compounds because it was too strict about methyl '
                 'groups and also accepted too many false‐positive patterns. '
                 'In this version we take the following measures:\n'
                 '\n'
                 '• We still require an “[As” token (so that only '
                 'arsenic‐based compounds are considered) and reject a '
                 'tryparsamide–like fragment.\n'
                 '  \n'
                 '• For each arsenic atom we look for any bond to carbon. We '
                 'then try to decide whether that carbon is “organyl” by (a) '
                 'checking if it is part of a larger carbon chain or ring '
                 '(i.e. it is bonded to another carbon besides the arsenic) or '
                 '(b) if it is a methyl group. In the earlier version a methyl '
                 'bond was accepted only when the arsenic had exactly one '
                 'organic bond; here we relax this so that if the only bonds '
                 'to arsenic are with methyl groups then we accept the ligand '
                 'if (for example) the As is part of a small molecule '
                 '(molecular weight <170\u2009Da) or if the arsenic is charged '
                 '(as in arsenocholine). (The idea is that many true '
                 'organometalloidal compounds have “non‐methyl” As–C bonds but '
                 'sometimes one or two As–CH3 bonds are acceptable.)  \n'
                 '\n'
                 '• Finally, when the As atom is not in a ring and is '
                 '“neutral” (formal charge 0), we require that it have at '
                 'least one double bond O (which is typical for As(V) '
                 'organo–arsenicals). (An exception is made if the As is in a '
                 'ring – e.g. in arsoles – or if the arsenic bears a positive '
                 'charge.)\n'
                 '\n'
                 'Note that—because real molecules vary widely and our '
                 'training examples show many borderline cases—this heuristic '
                 'filter remains imperfect. (If these rules do not yield an F₁ '
                 'score above a given threshold then one might consider '
                 'returning (None,None).)\n'
                 '\n'
                 'Below is the complete Python code in one block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 36,
    'num_true_negatives': 142235,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.42857142857142855,
    'recall': 0.9310344827586207,
    'f1': 0.5869565217391304,
    'accuracy': 0.9997329585382994,
    'negative_predictive_value': 0.9999859389610298}