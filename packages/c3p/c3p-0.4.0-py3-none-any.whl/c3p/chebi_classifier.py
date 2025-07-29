from collections import defaultdict
from dataclasses import field, dataclass
from typing import List, Iterator, Dict, Union

from oaklib import get_adapter
from semsql.sqla.relation_graph import EntailedEdge
from semsql.sqla.semsql import Statements
from sqlalchemy.orm import aliased

from c3p.classifier import Classifier
from c3p.datamodel import SMILES_STRING, ClassificationResult


@dataclass
class ChEBIClassifier(Classifier):
    """
    A classifier that uses ChEBI to classify SMILES strings.

    Example:

        >>> classifier = ChEBIClassifier()
        >>> results = list(classifier.classify("CCCCCCCCCCCCCC(O)CCCCCC"))
        >>> assert any(r.class_id == "CHEBI:CHEBI:24026" for r in results)

    """
    _smiles_to_parent_classes: Dict[str, List[str]] = field(default_factory=dict)

    @property
    def smiles_to_parent_classes(self) -> Dict[str, List[str]]:
        if not self._smiles_to_parent_classes:
            chebi_adapter = get_adapter("sqlite:obo:chebi")
            session = chebi_adapter.session
            child_smiles = aliased(Statements)
            q = session.query(
                child_smiles.value.label("smiles"),
                EntailedEdge.object.label("ancestor"),
            ).join(
                child_smiles,
                EntailedEdge.subject == child_smiles.subject,
            ).filter(
                EntailedEdge.predicate == "rdfs:subClassOf",
            ).filter(
                child_smiles.predicate == "obo:chebi/smiles",
            )
            d = defaultdict(list)
            for row in q:
                d[row.smiles].append(row.ancestor)
            self._smiles_to_parent_classes = d
        return self._smiles_to_parent_classes

    def classify_iter(self, smiles: Union[SMILES_STRING, List[SMILES_STRING]]) -> Iterator[ClassificationResult]:
        """
        Classify a SMILES string or list of SMILES strings using all programs in the given directory.

        Args:
            smiles:

        Returns:

        """
        if not isinstance(smiles, (list, set)):
            smiles = [smiles]
        ix = self.smiles_to_parent_classes
        for s in smiles:
            for parent in ix.get(s, []):
                yield ClassificationResult(
                    input_smiles=s,
                    class_id=parent,
                    confidence=1.0,
                    is_match=True,
                )
