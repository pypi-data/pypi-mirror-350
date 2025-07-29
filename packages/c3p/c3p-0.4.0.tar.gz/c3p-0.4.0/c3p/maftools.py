from functools import lru_cache
from sqlite3 import adapters
from typing import Dict, Any, List

from oaklib import get_adapter, BasicOntologyInterface
from oaklib.interfaces import MappingProviderInterface

from c3p.chebi_classifier import ChEBIClassifier
from c3p.classifier import Classifier

SMILES = "smiles"
DATABASE_IDENTIFIER = "database_identifier"
DATABASE = "database"
TAXID = "taxid"
C3P_CLASSIFICATIONS = "c3p_classifications"
CHEBI_CLASSIFICATIONS = "chebi_classifications"

@lru_cache
def get_chebi_adapter() -> BasicOntologyInterface:
    return get_adapter("sqlite:obo:chebi")

@lru_cache
def get_mapping_adapter() -> MappingProviderInterface:
    adapter = get_chebi_adapter()
    if not isinstance(adapter, MappingProviderInterface):
        raise ValueError("Adapter does not support mapping")
    return adapter

def enrich_maf(objs: List[Dict[str, Any]], **kwargs)-> int:
    """
    Enrich a list of MAF rows with additional information.

    Args:
        objs:
        classifier:
        chebi_classifier:
        check:
        min_confidence:

    """
    n = 0
    for obj in objs:
        if C3P_CLASSIFICATIONS in obj:
            break
        enriched = enrich_maf_row(obj, **kwargs)
        if enriched:
            n += 1
    return n

def enrich_maf_row(obj: Dict[str, Any], classifier: Classifier, chebi_classifier: ChEBIClassifier = None, check=False, min_confidence=0.2) -> bool:
    """
    Enrich a MAF row with additional information.

    Example:

        >>> from c3p.classifier import Classifier
        >>> classifier = Classifier()
        >>> obj = {"smiles": "CCCCCCCCCCCCCC(O)CCCCCC"}
        >>> enrich_maf_row(obj, classifier, min_confidence=0.2)
        >>> chebi_adapter = get_chebi_adapter()
        >>> results = [chebi_adapter.label(c) for c in obj["classifications"]]
        >>> assert "fatty alcohol" in results

    Args:
        obj:
        classifier:
        chebi_classifier:
        check:
        min_confidence:

    Returns:
        true if the row was enriched

    """
    if not isinstance(obj, dict):
        print(f"Invalid object: {obj}")
        return False
    if C3P_CLASSIFICATIONS in obj:
        return False
    enriched = False
    taxid = obj.get(TAXID)
    if taxid:
        for alt_prefix in ["NCBITAXON:http://purl.bioontology.org/ontology/NCBITAXON/", "NEWT:", "NCBITaxon_", "NCBITAXON/", "NCBITaxon:", "http://purl.bioontology.org/ontology/NCBITAXON/", "NCBITaxon:xon_"]:
            taxid = taxid.replace(alt_prefix, "NCBITaxon")
        if taxid != obj[TAXID]:
            enriched = True
        obj[TAXID] = taxid
    smiles = obj.get(SMILES)
    if not smiles or check:
        adapter = get_chebi_adapter()
        chebi_id = obj.get(DATABASE_IDENTIFIER)
        if not chebi_id:
            db = obj.get(DATABASE, "")
            if db.startswith("HMDB"):
                hmdb_id = f"HMDB:{db}"
                obj["HMDB_ID"] = hmdb_id
                mapper = get_mapping_adapter()
                for m in mapper.sssom_mappings([hmdb_id]):
                    if m.subject_id.startswith("CHEBI"):
                        chebi_id = m.object_id
                        obj[DATABASE_IDENTIFIER] = chebi_id
                        enriched = True
                        break
        if chebi_id:
            m = adapter.entity_metadata_map(chebi_id)
            smiles_from_chebi = m.get("obo:chebi/smiles")
            if smiles and smiles_from_chebi and smiles != smiles_from_chebi:
                obj["smiles_mismatch"] = True
            if smiles_from_chebi:
                smiles = smiles_from_chebi
    if smiles != obj.get(SMILES):
        enriched = True
    obj[SMILES] = smiles
    if smiles:
        if not obj.get(C3P_CLASSIFICATIONS):
            # print(f"Classifying {smiles} using c3p")
            classifications = [c.class_id for c in classifier.classify(smiles) if c.is_match and c.confidence >= min_confidence]
            obj[C3P_CLASSIFICATIONS] = classifications
            enriched = True
        if chebi_classifier and not obj.get(CHEBI_CLASSIFICATIONS):
            # print(f"Classifying {smiles} using chebi")
            classifications = [c.class_id for c in chebi_classifier.classify(smiles) if c.is_match and c.confidence >= min_confidence]
            obj[CHEBI_CLASSIFICATIONS] = classifications
            enriched = True
    return enriched




