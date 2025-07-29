import logging
import time
from collections import defaultdict
from dataclasses import field, dataclass
from typing import List, Iterator, Set

from requests_cache import CachedSession

from c3p.classifier import Classifier
from c3p.datamodel import SMILES_STRING, ClassificationResult, Dataset, EvaluationResult, Result, ChemicalClass, \
    ResultSet, Outcome
from c3p.learn import get_positive_and_negative_validate_instances

logger = logging.getLogger(__name__)

CHEBIFIER_BASE_URL = "https://chebifier.hastingslab.org/api"


@dataclass
class ChebifierClient(Classifier):
    session: CachedSession = field(
        default_factory=lambda: CachedSession(
            'requests_cache.sqlite',
            backend='sqlite',
            expire_after=3600 * 24 * 300,
            allowable_methods=('GET', 'POST'),
        )
    )

    def classify(self, smiles: SMILES_STRING) -> List[ClassificationResult]:
        return list(self.classify_iter(smiles))


    def classify_iter(self, smiles: SMILES_STRING) -> Iterator[ClassificationResult]:
        url = f"{CHEBIFIER_BASE_URL}/classify"
        data = {
            "smiles": smiles,
            "ontology": True,
        }
        time.sleep(0.01)
        response = self.session.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        for id, n in result["ontology"]["nodes"].items():
            if n.get("artificial", False):
                continue
            yield ClassificationResult(
                input_smiles=smiles,
                class_id=id,
                class_name=n["lbl"],
                is_match=True,
                confidence=1.0
            )

    def classify_dataset(self, dataset: Dataset) -> List[EvaluationResult]:
        validation_examples = set(dataset.validation_examples)
        class_ids = {cc.id for cc in dataset.classes}
        smiles_to_class_ids = defaultdict(set)
        print(f"Cache location: {self.session.cache.db_path}")
        logger.info(f"Indexing")
        n = 0
        for cc in dataset.classes:
            n += 1
            if n % 100 == 0:
                print(f"Indexed {n} / {len(dataset.classes)} classes; {cc.name}")
            for s in validation_examples.intersection(cc.all_positive_examples):
                smiles_to_class_ids[s].add(cc.id)
        predictions_by_class = defaultdict(set)
        n = 0
        for smiles in validation_examples:
            n += 1
            if n % 100 == 0:
                print(f"Classifying {n} / {len(validation_examples)} :: {smiles}")
            logger.debug(f"Classifying {smiles}")
            try:
                results = self.classify(smiles)
            except Exception as e:
                logger.error(f"Error classifying {smiles}")
                logger.error(e)
                continue
            result_ids = {r.class_id for r in results}
            eval_result_ids = result_ids.intersection(class_ids)
            for cid in eval_result_ids:
                predictions_by_class[cid].add(smiles)
        logger.debug(f"Predictions by class: {predictions_by_class}")
        ers = []
        for cid, predicted_smiles in predictions_by_class.items():
            cls = dataset.get_chemical_class_by_id(cid)
            cls_lite = cls.lite_copy()
            pos_exs, neg_exs = get_positive_and_negative_validate_instances(cls, dataset)
            pos = {s.smiles for s in pos_exs}
            neg = {s.smiles for s in neg_exs}
            logger.debug(f"ACTUAL POS: {pos}")
            logger.debug(f"ACTUAL NEG: {neg}")
            logger.debug(f"PREDICTED: {predicted_smiles}")
            true_positives = predicted_smiles.intersection(pos)
            logger.debug(f"TRUE POS: {true_positives}")
            false_positives = predicted_smiles - pos
            false_negatives = pos - predicted_smiles
            true_negatives = neg - predicted_smiles
            logger.info(f"{cid} {len(predicted_smiles)}")

            def outcomes(smiles_list: Set[str]):
                return [Outcome(smiles=x) for x in smiles_list]

            result = Result(
                chemical_class=cls_lite,
                code="",
                num_true_positives=len(true_positives),
                num_false_positives=len(false_positives),
                num_false_negatives=len(false_negatives),
                num_true_negatives=len(true_negatives),
                true_positives=outcomes(true_positives),
                false_positives=outcomes(false_positives),
                sample_true_negatives=outcomes(true_negatives)[:10],
                sample_false_negatives=outcomes(false_negatives)[:10],
                best=True,
            )
            result.calculate()
            er = EvaluationResult(
                train_results=ResultSet(results=[]),
                test_result=result
            )
            ers.append(er)
        return ers


