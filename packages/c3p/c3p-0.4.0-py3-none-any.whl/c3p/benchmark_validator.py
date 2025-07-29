from pathlib import Path
from typing import List

import yaml

from c3p.datamodel import ChemicalStructure, ChemicalClass, ResultSet, EvaluationResult
from tests.input.programs.thioester import smiles


def runner_header(name="C3PO") -> dict:
    return {
        "name": name,
        "template": "binary_with_explanation",
        "templates": {
            "binary_with_explanation": {
                "system": "Is the provided statement true? Return YES, NO, or OTHER, followed by an explanation.",
                "prompt": "{input}",
                "metrics": ["qa_with_explanation"],
            },
        },
        "matrix": {
            "hyperparameters": {
                "model": ["gpt-4o"],
            },
        },
    }


def create_runner_case(structure: ChemicalStructure, chemical_class: ChemicalClass, ideal="YES") -> dict:
    """Create a test case for the LLM runner."""
    return {
        "input": f"The structure known as {structure.name} (with SMILES '{structure.smiles}') is a type of {chemical_class.name} (defined as '{chemical_class.definition}').",
        "original_input": {
            "structure_name": structure.name,
            "smiles": structure.smiles,
            "chemical_class_name": chemical_class.name,
            "chemical_class_id": chemical_class.id,
        },
        "ideal": ideal,
    }

def write_runner_cases(result_sets: List[ResultSet], output_path: Path, min_f1=0.8, max_examples=3):
    """Write test cases for the LLM runner."""
    cases = []
    for rs in result_sets:
        br = rs.best_result
        if br.f1 >= min_f1:
            # the generated eval assumes that CHEBI is correct, so FP=NO, FN=YES.
            # however, we want to look for cases where the LLM disagrees (and hence
            # agrees with the program)
            if br.false_positives:
                for tp in br.false_positives[:max_examples]:
                    cases.append(create_runner_case(ChemicalStructure(name=tp.name, smiles=tp.smiles),
                                                    br.chemical_class,
                                                    ideal="NO"))
            if br.sample_false_negatives:
                for tp in br.sample_false_negatives[:max_examples]:
                    cases.append(create_runner_case(ChemicalStructure(name=tp.name, smiles=tp.smiles),
                                                    br.chemical_class,
                                                    ideal="YES"))
    obj = runner_header()
    obj["cases"] = cases
    with open(output_path, "w") as f:
        f.write(yaml.dump(obj, sort_keys=False))

def write_runner_cases_from_eval_dir(working_dir: Path, name="runner", **kwargs):
    rsets = []
    for fn in working_dir.glob("*.json"):
        er = EvaluationResult.model_validate_json(fn.read_text())
        rsets.append(er.train_results)
    runner_conf_dir = working_dir.parent / "llm_runners"
    runner_conf_dir.mkdir(exist_ok=True, parents=True)
    write_runner_cases(rsets, runner_conf_dir / f"{name}.yaml", **kwargs)

