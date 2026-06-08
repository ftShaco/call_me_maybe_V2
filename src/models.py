from pydantic import BaseModel


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
