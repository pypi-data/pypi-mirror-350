from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Dict

import pandas as pd

from c3p.classifier import Classifier
from c3p.datamodel import SMILES_STRING


@dataclass
class Enricher:
    classifier: Optional[Classifier] = None
    default_background_structures: Optional[List[SMILES_STRING]] = None


    def enriched_classes(
            self,
            sample_structures: List[SMILES_STRING],
            background_structures: Optional[List[SMILES_STRING]] = None,
            sample_class_counts: Optional[Dict[str, int]] = None,
            background_class_counts: Optional[Dict[str, int]] = None,
    ) -> pd.DataFrame:
        """
        Calculate enriched classes for a given list of SMILES strings.

        Args:
            classifier: The classifier to use
            sample_structures: The list of SMILES strings in the sample
            background_structures: The background set of SMILES strings; use all if not specified
            sample_class_counts: The class counts for the sample; calc on the fly if not specified
            background_class_counts: The class counts for the background; calc on the fly if not specified

        Returns:
            A DataFrame with the enriched classes
        """
        from scipy.stats import fisher_exact
        num_in_sample = len(sample_structures)
        classifier = self.classifier
        if classifier:
            sample_classification_results = classifier.classify(sample_structures)
            class2members = defaultdict(set)
            for r in sample_classification_results:
                class2members[r.name].add(r.input_smiles)
            sample_class_counts = { c: len(class2members[c]) for c in sample_classes }
        if not sample_class_counts:
            raise ValueError("sample_class_counts must be provided if classifier is not set")
        if background_structures is None:
            # assumes cache is set
            background_structures = [x for x in classifier.cache]
        num_in_background = len(background_structures)
        if background_class_counts is None:
            background_class_counts = defaultdict(int)
            for r in classifier.classify(background_structures):
                background_class_counts[r.name] += 1

        enrichment_results = []
        for sample_class, sample_class_count in sample_class_counts.items():
            if sample_class_count < 2:
                continue
            background_class_count = background_class_counts[sample_class]

            # Create contingency table for Fisher's exact test
            contingency_table = [
                [sample_class_count, num_in_sample - sample_class_count],
                [background_class_count, num_in_background - background_class_count]
            ]

            # Calculate Fisher's exact test
            odds_ratio, p_value = fisher_exact(contingency_table, alternative='greater')

            # Calculate fold enrichment
            sample_fraction = sample_class_count / num_in_sample
            background_fraction = background_class_count / num_in_background
            fold_enrichment = sample_fraction / background_fraction if background_fraction > 0 else float('inf')

            enrichment_results.append({
                'class': sample_class,
                'sample_count': sample_class_count,
                'background_count': background_class_count,
                'sample_fraction': sample_fraction,
                'background_fraction': background_fraction,
                'fold_enrichment': fold_enrichment,
                'p_value': p_value,
                'odds_ratio': odds_ratio
            })

            # Create DataFrame and sort by p-value
            results_df = pd.DataFrame(enrichment_results)
            if not results_df.empty:
                results_df = results_df.sort_values('p_value')

            return results_df

