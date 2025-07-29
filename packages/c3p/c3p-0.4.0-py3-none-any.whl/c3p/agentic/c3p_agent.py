from dataclasses import dataclass

from c3p.datamodel import ChemicalClass
from c3p.learn import safe_name
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


@dataclass
class GeneratorDependencies:
    chemical_class: ChemicalClass

class ProgramResult(BaseModel):
    python_code: str = Field(
        ...,
        description=(
            "The python code that classifies the SMILES string." 
            "This code should be executable, i.e. all commentary should be included in the docstring."
            "Any example input or example usages should also be in the docstring."
        ))


code_agent = Agent(
    'openai:gpt-4o',
    deps_type=GeneratorDependencies,
    result_type=ProgramResult,
    system_prompt=(
        "Write a python function that uses rdkit to determine whether a SMILES string"
        " is a member of the specified chemical class.",
        "the function should return a pair of the form (bool, str) where the first element is"
        " whether the SMILES string is a member of the class and the second element is a message"
        " that describes the result; if it does not classify, state the reason (e.g. missing cyclic structure).\n",
    ),
)


@code_agent.system_prompt
async def add_chemical_class(ctx: RunContext[GeneratorDependencies]) -> str:
    cc = ctx.deps.chemical_class
    fn = "is_" + safe_name(cc.name)
    return f"The class is {cc.name} and the definition is: {cc.definition}. The function name should be {fn}."

@code_agent.tool
def run_code(ctx: RunContext[GeneratorDependencies]) -> ProgramResult:
    cc = ctx.deps.chemical_class
    fn = "is_" + safe_name(cc.name)
    run_code(fn, cc)

if __name__ == '__main__':
    cc = ChemicalClass(id='CH:1', name="Alkaloid", definition="A class of naturally occurring organic compounds that mostly contain basic nitrogen atoms.")
    deps = GeneratorDependencies(chemical_class=cc)
    result = code_agent.run_sync('classify', deps=deps)
    print(result)
    print("\n\n### Data ###\n")
    print(result.data.python_code)