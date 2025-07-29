import random
from pathlib import Path
from typing import List, Optional, Annotated

import pandas as pd
import typer

from c3p.datamodel import Dataset, Config
from c3p.dumper import result_as_dict
from c3p.learn import learn_ontology_iter

app = typer.Typer(help="CHEBI learn.")

import logging

# Set up logger
logger = logging.getLogger()  # Get root logger


def configure_logging(verbosity: int):
    """Configure logging based on verbosity level"""
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Configure handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Set up logger
    logger.setLevel(level)
    logger.addHandler(handler)


def verbose_option(f):
    """Decorator to add verbose option to commands"""
    return typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Verbosity level: -v for INFO, -vv for DEBUG",
    )(f)

app = typer.Typer()


@app.command()
def learn_classes(
        class_names: Optional[List[str]] = typer.Argument(..., help="class name"),
        exclude_class_names: Optional[List[str]] = typer.Option(None, "--exclude", "-X", help="class names to exclude"),
        dataset_path: Path = typer.Option(None, "--dataset", "-d", help="path to dataset"),
        working_dir: Path = typer.Option(None, "--workdir", "-w", help="path to workdir"),
        model_name: Optional[str] = typer.Option(None, "--model", "-m", help="model name"),
        max_negative: Optional[int] = typer.Option(None, "--max-negative", "-n", help="max negative examples"),
        randomize_order: Annotated[bool, typer.Option(..., "--randomize-order/--no-randomize-order", help="randomize order")] = False,
        mapped_only: Annotated[bool, typer.Option("--mapped-only/--no-mapped-only", "-x/--no-x")] = False,
        use_the_force: Annotated[bool, typer.Option("--use-the-force/--no-use-the-force", )] = False,
        max_attempts: Optional[int] = typer.Option(None, "--max-attempts", "-a", help="max attempts"),
        f1_threshold: Optional[float] = typer.Option(None, "--f1-threshold", "-f", help="f1 threshold"),
        exclude_definitions: Optional[bool] = typer.Option(None, "--exclude-definitions/--no-exclude-definitions",  help="exclude definitions"),
        experiment_local_name: Optional[str] = typer.Option(None, "--experiment-local-name", "-e", help="experiment local name"),
        verbose: Annotated[int, verbose_option] = 0
) -> None:
    """
    Learn program classifiers from a dataset.

    The dataset should have been created beforehand.

    To learn all classes in the dataset use '-':

        c3p-learn -m gpt-4o --dataset dataset.json -w results -

    """
    n = 0
    configure_logging(verbose)
    with open(dataset_path, "r") as f:
        dataset = Dataset.model_validate_json(f.read())
        print(f"Classes: {len(dataset.classes)} Instances: {len(dataset.structures)}")

    logger.info(f"Structures: {len(dataset.structures)}")
    if class_names == ["-"]:
        class_names = None
    config = Config(
        llm_model_name=model_name,
        max_negative_to_test=max_negative,
        experiment_local_name=experiment_local_name
    )
    if exclude_definitions:
        config.use_definitions = False
    if max_attempts:
        config.max_attempts = max_attempts
    if f1_threshold:
        config.f1_threshold = f1_threshold
    if use_the_force:
        config.use_the_force = True

    if randomize_order:
        random.shuffle(dataset.classes)

    objs = []
    for rset in learn_ontology_iter(dataset, config,
                                    include_only=class_names,
                                    exclude=exclude_class_names,
                                    mapped_only=mapped_only, working_dir=working_dir):
        # print(rset.model_dump_json(indent=2))
        obj = result_as_dict(rset.best_result)
        br = rset.best_result
        num = br.num_true_positives + br.num_false_negatives
        print(f"Class: {br.chemical_class.name} F1: {br.f1} N={num}")
        objs.append(obj)
    df = pd.DataFrame(objs)
    df["num_examples"] = df.num_true_positives + df.num_false_negatives
    print(df.describe())



if __name__ == "__main__":
    app()