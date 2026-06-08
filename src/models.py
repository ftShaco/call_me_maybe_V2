from pydantic import BaseModel
from enum import Enum, auto


class ParameterSpec(BaseModel):
    type: str


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterSpec]
    returns: ParameterSpec


class PromptEntry(BaseModel):
    prompt: str


class InputError(Exception):
    pass


class State(Enum):
    EXPECT_OBJECT_OPEN = auto()    # expect '{'
    EXPECT_NAME_KEY = auto()       # expect the literal "name"
    EXPECT_NAME_COLON = auto()     # expect ':'
    EXPECT_NAME_VALUE = auto()     # the function-name string (opaque for now)
    EXPECT_COMMA = auto()          # expect ',' between name and parameters
    EXPECT_PARAMS_KEY = auto()     # expect the literal "parameters"
    EXPECT_PARAMS_COLON = auto()   # expect ':'
    EXPECT_PARAMS_VALUE = auto()   # the parameters object (opaque for now)
    DONE = auto()                  # complete, valid output produced
