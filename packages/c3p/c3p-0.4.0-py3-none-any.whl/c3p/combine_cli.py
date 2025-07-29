from collections import defaultdict
from pathlib import Path
from typing import List, Optional, Annotated

import typer

from c3p.cli import configure_logging, verbose_option
from c3p.datamodel import Dataset, Config, ResultSet
from c3p.dumper import write_programs
from c3p.learn import safe_name

app = typer.Typer(help="Combine to make an ensemble model.")

import logging

# Set up logger
logger = logging.getLogger()  # Get root logger


app = typer.Typer()


@app.command()
def combine(
        dirs: Optional[List[str]] = typer.Argument(..., help="directory name"),
        output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="output directory"),
        min_runs: Optional[int] = typer.Option(None, "--min-runs", "-m", help="minimum number of runs"),
        verbose: Annotated[int, verbose_option] = 0
) -> None:
    """
    Evaluate a model on a dataset using a single class.
    """
    n = 0
    configure_logging(verbose)
    by_chem = defaultdict(list)
    by_expt = defaultdict(list)
    for d in dirs:
        if "ensembl" in d:
            continue
        p = Path(d) / "cache"
        for fn in p.glob("*.json"):
            rset = ResultSet.model_validate_json(fn.read_text())
            experiment_name = Path(d).name
            rset.experiment_name = experiment_name
            cn = rset.best_result.chemical_class.name
            by_chem[cn].append(rset)
            by_expt[experiment_name].append(rset)
    new_rsets = []
    for cn, rsets in by_chem.items():
        if min_runs is not None and len(rsets) < min_runs:
            logger.warning(f"Skipping {cn} due to insufficient runs")
            continue
        best_f1 = -1
        best_rset = None
        all_f1s = []
        for rset in rsets:
            all_f1s.append(rset.best_result.f1)
            if rset.best_result.f1 > best_f1:
                best_f1 = rset.best_result.f1
                best_rset = rset
        if not best_rset:
            raise AssertionError(f"No best result for {cn}")
        new_rsets.append(best_rset)
        if output_dir:
            p = Path(output_dir) / "cache"
            p.mkdir(exist_ok=True, parents=True)
            safe_cn = safe_name(cn)
            fn = p / f"{safe_cn}.json"
            fn.write_text(best_rset.model_dump_json(indent=2))
        logger.info(f"Class: {cn} F1: {best_rset.best_result.f1} vs {all_f1s}")
    for e, rsets in by_expt.items():
        logger.info(f"Experiment: {e} Runs: {len(rsets)}")
    best_by_expr = defaultdict(int)
    for rset in new_rsets:
        best_by_expr[rset.experiment_name] += 1
    for e, n in best_by_expr.items():
        logger.info(f"Num {e}: {n}")




if __name__ == "__main__":
    app()