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


class FixedShapeMachine:
    """Validates text against the shape:  prefix + middle + suffix
    where `middle` is any non-empty run of characters (for now)."""

    def __init__(self, prefix: str, suffix: str) -> None:
        self.prefix = prefix
        self.suffix = suffix

    def accept(self, text: str) -> bool:
        """True if `text` is a prefix of SOME valid prefix+middle+suffix."""
        # Case A: still within/at the prefix region.
        #   -> reuse is_prefix_compatible(text, self.prefix)
        #
        # Case B: text has fully passed the prefix (len(text) > len(prefix)).
        #   The text must start with prefix (guaranteed if we got here legally),
        #   and the remainder after prefix is "middle so far, maybe into suffix".
        #   For now `middle` accepts anything, so the only thing that could make
        #   text INVALID is... nothing yet. Any continuation is still acceptable
        #   because middle is unconstrained and suffix could still come.
        #   -> so in case B, return True.
        #
        # TODO: implement the two cases.
        ...

    def is_complete(self, text: str) -> bool:
        """True if `text` is a COMPLETE valid prefix + (nonempty middle) + suffix."""
        # text must:
        #   - start with prefix
        #   - end with suffix
        #   - have at least one character of middle between them
        # TODO: express those three conditions. Watch the lengths so prefix and
        #       suffix don't overlap (text must be long enough to hold both
        #       plus a non-empty middle).
        ...

    def is_prefix_compatible(text: str, prefix: str) -> bool:
        if len(text) <= len(prefix):
            return prefix.startswith(text)
        return text.startswith(prefix)