def is_prefix_compatible(text: str, prefix: str) -> bool:
    if len(text) <= len(prefix):
        return prefix.startswith(text)
    return text.startswith(prefix)


class NameValidator:
    """Validates the function-name value against a closed set of names.
    Operates on the MIDDLE only (the chars between the quotes), not the quotes.
    """

    def __init__(self, names: list[str]) -> None:
        self.names = names

    def accept(self, middle: str) -> bool:
        return any(name.startswith(middle) for name in self.names)

    def is_complete(self, middle: str) -> bool:
        return middle in self.names


class StringValidator:
    """Validates a JSON string value's MIDDLE (chars between the quotes).
    For now: accept any character EXCEPT an unescaped double-quote (which would
    end the string) and control chars. Keep it simple — no escape handling yet.
    """

    def accept(self, middle: str) -> bool:
        return '"' not in middle

    def is_complete(self, middle: str) -> bool:
        return self.accept(middle)


class NumberValidator:
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
