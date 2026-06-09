# ABOUTME: Prefix/value validators for constrained JSON decoding.
# ABOUTME: Each validator answers accept(partial) and is_complete(partial).

def is_prefix_compatible(text: str, prefix: str) -> bool:
    """True if `text` could still grow into something starting
    with `prefix`."""
    if len(text) <= len(prefix):
        return prefix.startswith(text)
    return text.startswith(prefix)


class FixedValidator:
    """A segment that must match a fixed literal string exactly."""

    def __init__(self, literal: str) -> None:
        self.literal = literal

    def accept(self, middle: str) -> bool:
        return is_prefix_compatible(middle, self.literal)

    def is_complete(self, middle: str) -> bool:
        return middle == self.literal


class NameValidator:
    """Validates a value constrained to a closed set of names."""

    def __init__(self, names: list[str]) -> None:
        self.names = names

    def accept(self, middle: str) -> bool:
        return any(name.startswith(middle) for name in self.names)

    def is_complete(self, middle: str) -> bool:
        return middle in self.names


class StringValidator:
    """Validates a JSON string value's middle (chars between the quotes)."""

    def accept(self, middle: str) -> bool:
        return '"' not in middle

    def is_complete(self, middle: str) -> bool:
        return self.accept(middle)


class NumberValidator:
    """Validates a JSON number value's middle (sign, digits, single dot)."""

    def accept(self, middle: str) -> bool:
        seen_dot = False
        for i, c in enumerate(middle):
            if c == '-':
                if i != 0:
                    return False
            elif c == '.':
                if seen_dot or i == 0:
                    return False
                seen_dot = True
            elif not c.isdigit():
                return False
        return True

    def is_complete(self, middle: str) -> bool:
        return len(middle) > 0 and middle[-1].isdigit() and self.accept(middle)
