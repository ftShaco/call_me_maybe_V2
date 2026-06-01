import json
from pathlib import Path
from pydantic import ValidationError

from .models import FunctionDefinition, PromptEntry, InputError


def _read_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise InputError("Input file not found") from e
    except PermissionError as e:
        raise InputError(f"Permission denied, run 'chmod +r {path}'") from e
    except IsADirectoryError as e:
        raise InputError(f"Error occured, {path} is a directory") from e
    except json.JSONDecodeError as e:
        raise InputError(f"JSON file is malformed, unable to decode {e}")
    except OSError as e:
        raise InputError(f"Error occured with {path}. {e}")


def load_ft_definitions(path: Path) -> list[FunctionDefinition]:
    def_input = _read_json(path)
    if not isinstance(def_input, list):
        raise InputError(f"JSON file ({path}) is malformed , expecting "
                         "an array of function definitions")
    definitions = []
    for index, item in enumerate(def_input):
        try:
            validated = FunctionDefinition.model_validate(item)
            definitions.append(validated)
        except ValidationError as e:
            raise InputError(f"JSON file ({path}) is malformed, argument "
                             f"{index} can't be treated. {e}")
    if not definitions:
        raise InputError(f"JSON file ({path}) is empty, function "
                         "definitions are mandatory to run the program.")
    return definitions


def load_prompts(path: Path) -> list[PromptEntry]:
    prompt_input = _read_json(path)
    if not isinstance(prompt_input, list):
        raise InputError(f"JSON file ({path}) is malformed, expecting "
                         "an array of prompts")
    prompt_list = []
    for index, item in enumerate(prompt_input):
        try:
            prompt = PromptEntry.model_validate(item)
            prompt_list.append(prompt)
        except ValidationError as e:
            raise InputError(f"JSON file ({path}) is malformed, "
                             f"argument {index} can't be treated. {e}")
    return prompt_list
