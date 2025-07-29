from typing import Union, Literal, Tuple, Any
import pandas as pd
import numpy as np

AveragingStrategy = Literal["micro", "macro"]


def _extract_counts(data: Union[pd.Series, pd.DataFrame]) -> Tuple[float, float, float, float]:
    """
    Extract confusion matrix counts from a row or series.

    Returns:
        Tuple of (true_positives, true_negatives, false_positives, false_negatives)
    """
    return (
        data['num_true_positives'],
        data['num_true_negatives'],
        data['num_false_positives'],
        data['num_false_negatives']
    )


def _calculate_base_metrics(tp: float, tn: float, fp: float, fn: float) -> pd.Series:
    """
    Calculate classification metrics from confusion matrix counts.
    Handles zero division cases gracefully.
    """
    total = tp + tn + fp + fn

    # Avoid division by zero warnings by handling edge cases
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    metrics = pd.Series({
        # Basic counts
        'total': total,
        'positives': tp + fp,
        'negatives': tn + fn,
        'actual_positives': tp + fn,
        'actual_negatives': tn + fp,

        # Core metrics
        'accuracy': (tp + tn) / total if total > 0 else 0,
        'precision': precision,
        'recall': recall,
        'specificity': specificity,

        # Additional metrics
        'f1': 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0,
        'false_positive_rate': fp / (tn + fp) if (tn + fp) > 0 else 0,
        'negative_predictive_value': tn / (tn + fn) if (tn + fn) > 0 else 0,
    })

    metrics['balanced_accuracy'] = (metrics['recall'] + metrics['specificity']) / 2

    return metrics


def calculate_all_outcome_stats(
        data: pd.DataFrame,
        index: Any = 0,
) -> pd.DataFrame:
    """
    Calculate both micro and macro metrics and return them in a single DataFrame
    with clearly labeled columns.

    Args:
        data: DataFrame containing confusion matrix counts

    Returns:
        DataFrame with two columns for each metric (micro_* and macro_*)

    Examples:

        >>> df = pd.DataFrame({
        ...     'num_true_positives': [10, 5],
        ...     'num_true_negatives': [20, 15],
        ...     'num_false_positives': [5, 3],
        ...     'num_false_negatives': [3, 2]
        ... })
        >>> comparison = calculate_all_outcome_stats(df)
        >>> all(comparison['micro_total'] == comparison['macro_total'])
        True
    """
    micro_stats = calculate_stats(data, strategy="micro")
    macro_stats = calculate_stats(data, strategy="macro")

    # Convert to DataFrame for easier manipulation
    stats_df = pd.DataFrame({
                                f'micro_{col}': micro_stats[col] for col in micro_stats.index
                            } | {
                                f'macro_{col}': macro_stats[col] for col in macro_stats.index
                            }, index=[index])

    return stats_df


def calculate_stats(
        data: Union[pd.Series, pd.DataFrame],
        strategy: AveragingStrategy = "micro"
) -> pd.Series:
    """
    Calculate classification metrics using either micro or macro averaging.

    Args:
        data: Input data containing confusion matrix counts.
             If Series: should contain num_true_positives, num_true_negatives,
                       num_false_positives, num_false_negatives
             If DataFrame: each row should contain the above columns
        strategy: Either "micro" (default) or "macro" averaging
                 - micro: aggregate all counts first, then calculate metrics
                 - macro: calculate metrics per row, then average

    Returns:
        pd.Series containing calculated metrics

    Raises:
        ValueError: If strategy is invalid or required columns are missing

    Examples:
        >>> # Single class example
        >>> single_class = pd.Series({
        ...     'num_true_positives': 10,
        ...     'num_true_negatives': 20,
        ...     'num_false_positives': 5,
        ...     'num_false_negatives': 3
        ... })
        >>> metrics = calculate_stats(single_class)
        >>> print(metrics['accuracy'].round(2), metrics['precision'].round(2), metrics['recall'].round(2))
        0.79 0.67 0.77

        >>> # Multi-class example
        >>> multi_class = pd.DataFrame({
        ...     'num_true_positives': [10, 5],
        ...     'num_true_negatives': [20, 15],
        ...     'num_false_positives': [5, 3],
        ...     'num_false_negatives': [3, 2]
        ... })
        >>> # Micro-averaging (default)
        >>> micro_metrics = calculate_stats(multi_class)
        >>> print(micro_metrics['accuracy'].round(2), micro_metrics['precision'].round(2))
        0.79 0.65

        >>> macro_metrics = calculate_stats(multi_class, strategy="macro")
        >>> print(macro_metrics['f1'].round(2), macro_metrics['precision'].round(2))
        0.69 0.65

        >>> # Error cases
        >>> try:
        ...     calculate_stats(pd.Series(), strategy="invalid")
        ... except ValueError as e:
        ...     print(str(e))
        Strategy must be either 'micro' or 'macro'

        >>> try:
        ...     calculate_stats(pd.DataFrame())
        ... except ValueError as e:
        ...     print(str(e))
        Missing required columns: ['num_true_positives', 'num_true_negatives', 'num_false_positives', 'num_false_negatives']
    """
    required_cols = [
        'num_true_positives', 'num_true_negatives',
        'num_false_positives', 'num_false_negatives'
    ]

    # Input validation
    if strategy not in ["micro", "macro"]:
        raise ValueError("Strategy must be either 'micro' or 'macro'")

    if isinstance(data, pd.Series):
        missing_cols = [col for col in required_cols if col not in data.index]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        # Single row case - both strategies are equivalent
        return _calculate_base_metrics(*_extract_counts(data))

    # DataFrame case
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if len(data) == 0:
        # Return zeros for empty DataFrame
        return _calculate_base_metrics(0, 0, 0, 0)

    if strategy == "micro":
        # Sum counts first, then calculate metrics
        totals = data[required_cols].sum()
        return _calculate_base_metrics(*_extract_counts(totals))
    else:  # macro averaging
        # Calculate metrics for each row, then average
        row_metrics = []
        for _, row in data.iterrows():
            metrics = _calculate_base_metrics(*_extract_counts(row))
            row_metrics.append(metrics)

        # Average all metrics
        macro_metrics = pd.concat(row_metrics, axis=1).T.mean()
        max_metrics = pd.concat(row_metrics, axis=1).T.max()

        # Keep the total counts from micro averaging for consistency
        totals = data[required_cols].sum()
        macro_metrics['total'] = totals.sum()
        macro_metrics['positives'] = totals['num_true_positives'] + totals['num_false_positives']
        macro_metrics['negatives'] = totals['num_true_negatives'] + totals['num_false_negatives']
        macro_metrics['actual_positives'] = totals['num_true_positives'] + totals['num_false_negatives']
        macro_metrics['actual_negatives'] = totals['num_true_negatives'] + totals['num_false_positives']
        macro_metrics['num_rows'] = len(data)
        macro_metrics['max_f1'] = max_metrics['f1']
        macro_metrics['max_precision'] = max_metrics['precision']
        macro_metrics['max_recall'] = max_metrics['recall']
        macro_metrics['max_accuracy'] = max_metrics['accuracy']
        if 'f1' in data.columns:
            macro_metrics['max_num_f1_above_0_99'] = sum(data['f1'] > 0.99)
            macro_metrics['max_num_f1_above_0_95'] = sum(data['f1'] > 0.95)
            macro_metrics['max_num_f1_above_0_80'] = sum(data['f1'] > 0.80)
            macro_metrics['pct_f1_above_0_99'] = sum(data['f1'] > 0.99) / len(data)
            macro_metrics['pct_f1_above_0_95'] = sum(data['f1'] > 0.95) / len(data)
            macro_metrics['pct_f1_above_0_80'] = sum(data['f1'] > 0.80) / len(data)

        return macro_metrics.round(4)

def calculate_grouped_stats(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
    """
    Calculate classification metrics for each group in a DataFrame,

    e.g. grouped_by method

    Args:
        df: DataFrame containing confusion matrix counts
        group_by: Column name to group by

    Returns:
        DataFrame containing metrics for each group
    """
    if group_by not in df.columns:
        raise ValueError(f"Group column '{group_by}' not found in DataFrame")

        # Calculate metrics for each group
    group_metrics = []
    for name, group in df.groupby(group_by):
        metrics = calculate_all_outcome_stats(group, index=name)
        metrics.name = name
        group_metrics.append(metrics)

    # Combine all group metrics into a single DataFrame
    return pd.concat(group_metrics).round(3)


def assign_ranks_per_group(df: pd.DataFrame, group_by: str, metric="f1", col_name="rank"):
    """

    Example:

        >>> df = pd.DataFrame({"G": [1, 1, 2, 2, 3, 3],
        ...                    "chemical": ["a", "b", "a", "b", "a", "b"],
        ...                    "f1": [1,0, 1, 0, 0, 1],
        ... })
        >>> assign_ranks_per_group(df, group_by="G")
        >>> int(df[(df["chemical"] == "a") & (df["G"] == 1)]["rank"])
        1
        >>> int(df[(df["chemical"] == "a") & (df["G"] == 2)]["rank"])
        2

    Args:
        df:
        group_by:

    Returns:

    """
    for name, group in df.groupby(group_by):
        df.loc[group.index, col_name] = group[metric].rank(method='min', ascending=False)