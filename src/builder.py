# ABOUTME: Builds a Coordinator (segment list) for a given function definition.
# ABOUTME: Encodes the fixed JSON skeleton around the variable value regions.

from .validators import (
    FixedValidator, NameValidator, StringValidator, NumberValidator,
)
from .coordinator import Coordinator


def build_coordinator(function, all_names: list[str]) -> Coordinator:
    """Build a Coordinator for ONE known function.

    `function` is a FunctionDefinition (has .name and .parameters dict).
    `all_names` is the closed set of valid function names (for the name value).
    """
    segments = []
    fixed_literals = []

    def add_fixed(literal: str) -> None:
        fixed_literals.append(literal)
        segments.append(FixedValidator(literal))

    def add_variable(validator) -> None:
        fixed_literals.append(None)
        segments.append(validator)

    # {"name": "<NAME>"
    add_fixed('{"name": "')
    add_variable(NameValidator(all_names))
    # ", "parameters": {
    if not function.parameters:
        add_fixed('", "parameters": {}}')
        return Coordinator(segments, fixed_literals)

    add_fixed('", "parameters": {')
    first = True
    for arg_name, spec in function.parameters.items():
        if spec.type == "string":
            # "<key>": "<value>"
            prefix = ('' if first else ', ') + f'"{arg_name}": "'
            add_fixed(prefix)
            add_variable(StringValidator())
            add_fixed('"')
        else:  # number
            prefix = ('' if first else ', ') + f'"{arg_name}": '
            add_fixed(prefix)
            add_variable(NumberValidator())
        first = False
    add_fixed('}}')

    return Coordinator(segments, fixed_literals)
