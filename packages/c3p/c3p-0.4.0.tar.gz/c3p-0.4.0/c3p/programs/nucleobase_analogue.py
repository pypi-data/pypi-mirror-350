"""
Classifies: CHEBI:67142 nucleobase analogue
"""
"""
Classifies: nucleobase analogue – a molecule that can substitute for a normal nucleobase in nucleic acids.
Improved heuristic criteria:
  1. Must parse as a valid molecule.
  2. Molecular weight between 80 and 350 Da.
  3. Contains at least 2 nitrogen atoms.
  4. Contains a single nucleobase-like aromatic heterocycle defined as either:
     a) A six-membered aromatic ring with at least 2 nitrogen atoms (pyrimidine‐like),
         AND no additional nitrogen-containing aromatic rings in the molecule,
         OR
     b) A fused ring system (two rings that share at least 2 atoms) where one ring is six-membered 
         and the other is five-membered and the union of the two contains at least 3 nitrogen atoms (purine‐like).
  5. The candidate aromatic system must represent a significant portion (>=50%) of the heavy atoms 
     in the molecule (to reduce misclassification of molecules with extra aromatic substituents, sugars, etc.).
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_nucleobase_analogue(smiles: str):
    """
    Determines if a molecule is a nucleobase analogue based on its SMILES string.
    
    The heuristic criteria are:
      - Valid molecule and molecular weight between 80 and 350 Da.
      - Contains at least 2 nitrogen atoms.
      - Contains one nucleobase-like aromatic heterocycle, defined as:
           * Either a six-membered aromatic ring that contains ≥2 nitrogen atoms (pyrimidine-like)
           * OR a fused system of a six-membered ring and a five-membered ring sharing at least 2 atoms,
             with a union of at least 3 nitrogen atoms (purine-like).
      - The candidate heterocycle must represent at least 50% of the molecule’s heavy atoms.
      - The molecule should not contain additional unrelated nitrogen-containing aromatic systems.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule meets these criteria, False otherwise.
        str: Explanation of the decision.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check molecular weight (using exact weight)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 80 or mol_wt > 350:
        return False, f"Molecular weight {mol_wt:.1f} Da is not in the typical range (80-350 Da) for nucleobase analogues"
    
    # Count total nitrogen atoms
    total_nitrogens = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    if total_nitrogens < 2:
        return False, f"Found only {total_nitrogens} nitrogen atom(s); expected at least 2"
    
    # Get aromatic ring information from the molecule.
    ring_info = mol.GetRingInfo()
    aromatic_rings = []
    # We identify rings that are aromatic (all atoms aromatic) and record:
    # - set of atom indices in the ring
    # - ring size
    # - number of nitrogen atoms in the ring
    for ring in ring_info.AtomRings():
        if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            n_in_ring = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 7)
            aromatic_rings.append({
                "indices": set(ring),
                "size": len(ring),
                "n_count": n_in_ring
            })
    
    if not aromatic_rings:
        return False, "Molecule has no aromatic rings; nucleobase analogues are heterocyclic"
    
    candidate_type = None  # will be "pyrimidine" or "purine"
    candidate_atoms = set()  # indices for the candidate nucleobase heterocycle
    
    # First, search for a pyrimidine-like candidate: one single six-membered ring with at least 2 nitrogens.
    pyrimidine_candidates = [ring for ring in aromatic_rings if ring["size"] == 6 and ring["n_count"] >= 2]
    if len(pyrimidine_candidates) == 1:
        candidate_type = "pyrimidine-like"
        candidate_atoms = pyrimidine_candidates[0]["indices"]
    else:
        # If not found, try to find a purine-like candidate: a pair of fused rings (one 6-membered and one 5-membered)
        # sharing at least 2 atoms and with the union having at least 3 nitrogen atoms.
        n_arom = len(aromatic_rings)
        found_purine = False
        for i in range(n_arom):
            for j in range(i+1, n_arom):
                ring1 = aromatic_rings[i]
                ring2 = aromatic_rings[j]
                # Check that one ring is 6-membered and the other 5-membered.
                if not (((ring1["size"] == 6 and ring2["size"] == 5) or (ring1["size"] == 5 and ring2["size"] == 6))):
                    continue
                # For a fused system, the rings must share at least 2 atoms.
                if len(ring1["indices"].intersection(ring2["indices"])) < 2:
                    continue
                union_indices = ring1["indices"].union(ring2["indices"])
                union_nitrogens = sum(1 for idx in union_indices if mol.GetAtomWithIdx(idx).GetAtomicNum() == 7)
                if union_nitrogens >= 3:
                    candidate_type = "purine-like"
                    candidate_atoms = union_indices
                    found_purine = True
                    break
            if found_purine:
                break
    
    if candidate_type is None:
        return False, "Molecule does not contain a nucleobase-like aromatic heterocycle (neither pyrimidine-like nor purine-like)"
    
    # Now, ensure that the molecule does not contain extra independent heterocyclic aromatic rings.
    # We consider only rings that contain at least one nitrogen.
    nucleo_rings = [ring for ring in aromatic_rings if ring["n_count"] > 0]
    # For a pyrimidine-like candidate, we expect only one such ring.
    if candidate_type == "pyrimidine-like" and len(nucleo_rings) > 1:
        return False, "Molecule contains extra nitrogen-containing aromatic rings beyond the pyrimidine-like core"
    # For a purine-like candidate, we expect exactly two rings in the fused system.
    if candidate_type == "purine-like" and len(nucleo_rings) > 2:
        return False, "Molecule contains extra nitrogen-containing aromatic rings beyond the purine-like fused core"
    
    # Next, check what fraction of the heavy atoms are in the candidate nucleobase heterocycle.
    total_heavy = mol.GetNumHeavyAtoms()
    frac = len(candidate_atoms) / total_heavy
    if frac < 0.5:
        return False, f"Candidate heterocycle accounts for only {frac:.2f} fraction of heavy atoms (<0.5), suggesting additional substituents"
    
    return True, f"Molecule fits refined heuristic criteria as a nucleobase analogue ({candidate_type})."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:67142',
                          'name': 'nucleobase analogue',
                          'definition': 'A molecule that can substitute for a '
                                        'normal nucleobase in nucleic acids.',
                          'parents': ['CHEBI:33832'],
                          'xrefs': ['Wikipedia:Base_analog'],
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
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
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
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetNumHeavyAtoms',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'GetAtoms',
                                                 'union',
                                                 'GetIsAromatic',
                                                 'intersection',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_nucleobase_analogue(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight '
                                          '{mol_wt:.1f} Da is not in the '
                                          'typical range (80-350 Da) for '
                                          'nucleobase analogues"',
                                          'False, f"Found only '
                                          '{total_nitrogens} nitrogen atom(s); '
                                          'expected at least 2"',
                                          'False, "Molecule has no aromatic '
                                          'rings; nucleobase analogues are '
                                          'heterocyclic"',
                                          'False, "Molecule does not contain a '
                                          'nucleobase-like aromatic '
                                          'heterocycle (neither '
                                          'pyrimidine-like nor purine-like)"',
                                          'False, "Molecule contains extra '
                                          'nitrogen-containing aromatic rings '
                                          'beyond the pyrimidine-like core"',
                                          'False, "Molecule contains extra '
                                          'nitrogen-containing aromatic rings '
                                          'beyond the purine-like fused core"',
                                          'False, f"Candidate heterocycle '
                                          'accounts for only {frac:.2f} '
                                          'fraction of heavy atoms (<0.5), '
                                          'suggesting additional substituents"',
                                          'True, f"Molecule fits refined '
                                          'heuristic criteria as a nucleobase '
                                          'analogue ({candidate_type})."'],
                           'returns_count': 9,
                           'complexity': 6.308658956454001},
    'message': '\n'
               'Attempt failed: F1 score of 0.02890625 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: O=C1NC=CC(=N1)NC(=O)C NAME: '
               'N(4)-acetylcytosine REASON: CORRECT Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: Brc1c[nH]c(=O)[nH]c1=O NAME: 5-bromouracil REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: O=c1cn[nH]c(=O)[nH]1 NAME: 6-azauracil REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: C=1(C(=CNC(N1)=O)C)OC NAME: O(4)-methylthymine '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Nc1ncnc2[nH]nnc12 NAME: 8-azaadenine REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Cn1ccc(=O)[nH]c1=O NAME: 1-methyluracil REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: O=C1NC=2N(C=3NC=NC31)C=CN2 NAME: '
               'N(2),3-ethenoguanine REASON: CORRECT Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: O=c1cc[nH]c(=S)[nH]1 NAME: thiouracil REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: C=12C(=NC=NC1NCC(=O)N)NC=N2 NAME: '
               'N(6)-carbamoylmethyladenine REASON: CORRECT Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: C(CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)CCO NAME: '
               '6-[(4-hydroxybutyl)amino]-5-[(E)-(2-oxopropylidene)amino]uracil '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Nc1nc(=O)[nH]cc1C=O NAME: 5-formylcytosine REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: C=12C(NC=NC1NN=N2)=O NAME: 8-azahypoxanthine '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: C=12C(=NC=NC1N)NC(=N2)O NAME: 8-hydroxyadenine '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: C(CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)CO NAME: '
               '6-[(3-hydroxypropyl)amino]-5-[(E)-(2-oxopropylidene)amino]uracil '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Oc1ncnc2[nH]ncc12 NAME: allopurinol REASON: CORRECT '
               'Molecule fits refined heuristic criteria for a nucleobase '
               'analogue\n'
               ' * SMILES: O=c1[nH]cnc2nc[nH]c12 NAME: hypoxanthine REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: N1=C(C)C(NC(N1)=O)=O NAME: 6-azathymine REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Nc1nc(NO)c2nc[nH]c2n1 NAME: '
               '2-amino-6-hydroxyaminopurine REASON: CORRECT Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: C1=C(CCCC(CO)O)C(NC(N1)=O)=O NAME: '
               '5-(4,5-dihydroxypentyl)uracil REASON: CORRECT Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: Nc1ncc2nc[nH]c2n1 NAME: 2-aminopurine REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: '
               '[C@H](CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)([C@@H](CCO)O)O NAME: '
               '6-[(1,4-dideoxy-D-ribityl)amino]-5-[(E)-(2-oxopropylidene)amino]uracil '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Cn1c(=O)cc[nH]c1=O NAME: 3-methyluracil REASON: '
               'CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Nc1nc(=O)[nH]cc1CO NAME: 5-(hydroxymethyl)cytosine '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: '
               'C(CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)[C@@H]([C@@H](CO)O)O NAME: '
               '6-[(1,2-dideoxy-D-ribityl)amino]-5-[(E)-(2-oxopropylidene)amino]uracil '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: O=C1NC(=O)C(=CN1C)C NAME: 1,5-dimethyluracil '
               'REASON: CORRECT Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               'False positives: SMILES: '
               'NC1=NC(=O)C2=C(N1)N=CC(CNC1=CC=C(C=C1)C(O)=O)=N2 NAME: '
               '4-{[(2-amino-4-oxo-1,4-dihydropteridin-6-yl)methyl]amino}benzoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: O=C(O)C=1C2=NC=3C(=C(C=CC3OC)CO)N=C2C=CC1 NAME: '
               'LL-14I352beta REASON: WRONGLY CLASSIFIED Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: O=C1N(O)C(O)=C(C(=O)C2=CC=CC=C2)N=C1CC3=CC=CC=C3 '
               'NAME: Coelomycin REASON: WRONGLY CLASSIFIED Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: O=C1N(NC(=O)C=C1C)C2=CC=CC=C2 NAME: '
               '6-hydroxy-4-methyl-2-phenyl-2,3-dihydropyridazin-3-one REASON: '
               'WRONGLY CLASSIFIED Molecule fits refined heuristic criteria '
               'for a nucleobase analogue\n'
               ' * SMILES: '
               'CC1=CC2=NC3=C(C=C(N)C(C)=C3)[N+](C3=CC=CC=C3)=C2C=C1N NAME: '
               '3,7-diamino-2,8-dimethyl-5-phenylphenazin-5-ium REASON: '
               'WRONGLY CLASSIFIED Molecule fits refined heuristic criteria '
               'for a nucleobase analogue\n'
               ' * SMILES: CC#CC1=C(C)C2=C(C=C1)C(=O)NC(CSC1=NC=CC=N1)=N2 '
               'NAME: ITK7 REASON: WRONGLY CLASSIFIED Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: C1CCN(CC1)C2=C3C4=C(C=C2)C(=O)NN=C4C5=CC=CC=C5C3=O '
               'NAME: LSM-34582 REASON: WRONGLY CLASSIFIED Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: Nc1nc(=O)[nH]cc1F NAME: flucytosine REASON: WRONGLY '
               'CLASSIFIED Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)[C@@H]2O)c(=O)n1 '
               'NAME: cytarabine REASON: WRONGLY CLASSIFIED Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: CN1C2=C(C=C(C=C2)OC)C3=C1C(=O)N(C=N3)CCN4CCCC4 '
               'NAME: '
               '8-methoxy-5-methyl-3-[2-(1-pyrrolidinyl)ethyl]-4-pyrimido[5,4-b]indolone '
               'REASON: WRONGLY CLASSIFIED Molecule fits refined heuristic '
               'criteria for a nucleobase analogue\n'
               ' * SMILES: CCC(Nc1ncnc(C)c1Cl)c1ccc(OC(F)F)cc1 NAME: '
               '5-chloro-N-{1-[4-(difluoromethoxy)phenyl]propyl}-6-methylpyrimidin-4-amine '
               'REASON: WRONGLY CLASSIFIED Molecule fits refined heuristic '
               'criteria for a nucleobase analogue\n'
               ' * SMILES: [H+].NC(=N)NC(=O)c1nc(Cl)c(N)nc1N NAME: '
               'amiloride(1+) REASON: WRONGLY CLASSIFIED Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@H]2OP(O)(=O)O[C@@H]12 '
               "NAME: 2',3'-cyclic AMP REASON: WRONGLY CLASSIFIED Molecule "
               'fits refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: C1=CC=C2C(=C1)N=NN2OCC3=C(C=C(C=C3)Cl)Cl NAME: '
               '1-[(2,4-dichlorophenyl)methoxy]benzotriazole REASON: WRONGLY '
               'CLASSIFIED Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H]([C@@H]2OP([O-])(=O)O[C@H]12)n1ccc(=O)[nH]c1=O '
               "NAME: 2',3'-cyclic UMP(1-) REASON: WRONGLY CLASSIFIED Molecule "
               'fits refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'O1[C@@H](N2C3=NC=NC(=C3N=C2)N)[C@H](N)[C@@H]([C@H]1CO)O NAME: '
               "2'-amino-2'-deoxyadenosine REASON: WRONGLY CLASSIFIED Molecule "
               'fits refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'Cn1c(=O)ccn([C@@H]2O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]2O)c1=O '
               "NAME: N(3)-methyluridine 5'-monophosphate REASON: WRONGLY "
               'CLASSIFIED Molecule fits refined heuristic criteria for a '
               'nucleobase analogue\n'
               ' * SMILES: S([N-]C=1N=CC(=CN1)OCCOC)(=O)(=O)C2=CC=CC=C2 NAME: '
               'glymidine(1-) REASON: WRONGLY CLASSIFIED Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: C1=CC=C2C(=C1)N=NN2CC3=NN=C4N3N=C(S4)C5=CC=CS5 '
               'NAME: '
               '3-(1-benzotriazolylmethyl)-6-thiophen-2-yl-[1,2,4]triazolo[3,4-b][1,3,4]thiadiazole '
               'REASON: WRONGLY CLASSIFIED Molecule fits refined heuristic '
               'criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'Cc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=S)[nH]c1=O NAME: '
               '5-methyl-2-thiouridine REASON: WRONGLY CLASSIFIED Molecule '
               'fits refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'OC=1C2=NC=3C(=C(O)C=CC3)N=C2C(C/C=C(/CCC=C(C)C)\\C)=CC1 NAME: '
               'Geranylphenazinediol REASON: WRONGLY CLASSIFIED Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'O=C1N=C(N)C=CN1[C@@H]2O[C@H](C(=O)O)[C@H](O)C[C@H]2O NAME: '
               '(2S,3R,5R,6R)-6-(4-amino-2-oxopyrimidin-1-yl)-3,5-dihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Molecule fits refined '
               'heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: '
               'Nc1ccn([C@@H]2O[C@@H]3COP([O-])(=O)O[C@H]3[C@H]2O)c(=O)n1 '
               "NAME: 3',5'-cyclic CMP(1-) REASON: WRONGLY CLASSIFIED Molecule "
               'fits refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: O.C[C@H](Cn1cnc2c(N)ncnc12)OCP(O)(O)=O NAME: '
               'tenofovir hydrate REASON: WRONGLY CLASSIFIED Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               ' * SMILES: Cn1c2ncn(C[C@@H](O)CO)c2c(=O)n(C)c1=O NAME: '
               '(R)-dyphylline REASON: WRONGLY CLASSIFIED Molecule fits '
               'refined heuristic criteria for a nucleobase analogue\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Molecular weight 358.1 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Molecular weight 364.1 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Found only 0 nitrogen atom(s); '
                                               'expected at least 2'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Molecular weight 359.3 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Molecular weight 757.4 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Molecular weight 504.2 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Molecular weight 991.7 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Molecule has no aromatic '
                                               'rings; nucleobase analogues '
                                               'are heterocyclic'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Molecule has no aromatic '
                                               'rings; nucleobase analogues '
                                               'are heterocyclic'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Molecular weight 358.2 Da is '
                                               'not in the typical range '
                                               '(80-350 Da) for nucleobase '
                                               'analogues'}],
    'sample_false_negatives': [   {   'smiles': 'Nc1ncnc2[nH]nnc12',
                                      'name': '8-azaadenine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'O=C1NC=2N(C=3NC=NC31)C=CN2',
                                      'name': 'N(2),3-ethenoguanine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'C=12C(=NC=NC1NCC(=O)N)NC=N2',
                                      'name': 'N(6)-carbamoylmethyladenine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'C(CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)CCO',
                                      'name': '6-[(4-hydroxybutyl)amino]-5-[(E)-(2-oxopropylidene)amino]uracil',
                                      'reason': 'Candidate heterocycle '
                                                'accounts for only 0.32 '
                                                'fraction of heavy atoms '
                                                '(<0.5), suggesting additional '
                                                'substituents'},
                                  {   'smiles': 'C=12C(NC=NC1NN=N2)=O',
                                      'name': '8-azahypoxanthine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'C=12C(=NC=NC1N)NC(=N2)O',
                                      'name': '8-hydroxyadenine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'C(CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)CO',
                                      'name': '6-[(3-hydroxypropyl)amino]-5-[(E)-(2-oxopropylidene)amino]uracil',
                                      'reason': 'Candidate heterocycle '
                                                'accounts for only 0.33 '
                                                'fraction of heavy atoms '
                                                '(<0.5), suggesting additional '
                                                'substituents'},
                                  {   'smiles': 'Oc1ncnc2[nH]ncc12',
                                      'name': 'allopurinol',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'O=c1[nH]cnc2nc[nH]c12',
                                      'name': 'hypoxanthine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'},
                                  {   'smiles': 'Nc1nc(NO)c2nc[nH]c2n1',
                                      'name': '2-amino-6-hydroxyaminopurine',
                                      'reason': 'Molecule contains extra '
                                                'nitrogen-containing aromatic '
                                                'rings beyond the '
                                                'pyrimidine-like core'}],
    'attempt': 2,
    'reasoning': 'Below is one possible solution. In our reasoning we noted '
                 'that the original heuristic “flagged” many false positives '
                 'because many molecules had extra aromatic rings or '
                 'non‐nucleobase portions (for example, extra benzene '
                 'substituents or even sugar/phosphate groups) that made the '
                 'simple “nucleobase‐like” pattern too permissive. To improve '
                 'matters we now (a) still require a valid molecule; (b) '
                 'require the molecule’s weight be in the 80–350\u2005Da range '
                 'and have at least 2 nitrogen atoms; (c) try to “extract” a '
                 'single candidate nucleobase heterocycle using one of two '
                 'patterns: either a lone six‐membered aromatic ring '
                 '(pyrimidine‐like) with at least 2 nitrogens or a fused '
                 'system with one 6‐membered ring and one 5‐membered ring '
                 '(purine‐like) sharing at least 2 atoms and a union of at '
                 'least 3 nitrogens; (d) then we check that no extra '
                 'heteroaromatic rings exist beyond the candidate and (e) '
                 'finally we require that the candidate ring(s) constitute a '
                 'significant fraction of the heavy atoms (this helps weed out '
                 'nucleosides and added substituents). While this approach is '
                 'still heuristic (and might miss some edge cases), our aim is '
                 'to cut down on the false positives seen previously.\n'
                 '\n'
                 'Below is the complete Python code using rdkit:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 248,
    'num_true_negatives': 142015,
    'num_false_negatives': 22,
    'num_negatives': None,
    'precision': 0.057034220532319393,
    'recall': 0.40540540540540543,
    'f1': 0.1,
    'accuracy': 0.9981026001405482,
    'negative_predictive_value': 0.9998451107809937}