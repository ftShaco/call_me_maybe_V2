class FixedShapeMachine:
    """Validates text against the shape:  prefix + middle + suffix
    where `middle` is any non-empty run of characters (for now)."""

    def __init__(self, prefix: str, suffix: str) -> None:
        self.prefix = prefix
        self.suffix = suffix

    def accept(self, text: str) -> bool:
        """True if `text` is a prefix of SOME valid prefix+middle+suffix."""
        if len(text) <= len(self.prefix):
            return self.is_prefix_compatible(text, self.prefix)
        else:
            return True

    def is_complete(self, text: str) -> bool:
        """True if `text` is a COMPLETE valid prefix + middle + suffix."""
        if len(text) <= len(self.prefix) + len(self.suffix):
            return False
        if (self.is_prefix_compatible(text, self.prefix) and
                self.is_suffix_compatible(text, self.suffix)):
            return True
        return False

    @staticmethod
    def name_still_reachable(middle: str, names: list[str]) -> bool:
        return any(name.startswith(middle) for name in names)

    @staticmethod
    def name_is_complete(middle: str, names: list[str]) -> bool:
        return middle in names

    @staticmethod
    def is_prefix_compatible(text: str, prefix: str) -> bool:
        if len(text) <= len(prefix):
            return prefix.startswith(text)
        return text.startswith(prefix)

    @staticmethod
    def is_suffix_compatible(text: str, suffix: str) -> bool:
        if len(text) <= len(suffix):
            return suffix.endswith(text)
        return text.endswith(suffix)
