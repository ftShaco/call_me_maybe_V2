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


class FixedValidator:
    """A segment that must match a literal string exactly."""
    def __init__(self, literal: str) -> None:
        self.literal = literal

    def accept(self, middle: str) -> bool:
        return is_prefix_compatible(middle, self.literal)

    def is_complete(self, middle: str) -> bool:
        return middle == self.literal


class Coordinator:
    """Validates generated text against an ordered list of segments
    (alternating FixedValidator / value-validators) for a KNOWN function."""

    def __init__(self, segments: list) -> None:
        # segments: ordered list of validator objects, each with
        #           accept(middle) and is_complete(middle).
        self.segments = segments

    def _split(self, text: str):
        """Walk `text` across the segments. Return a list of (segment, chunk)
        pairs for the FULLY consumed leading segments, plus (current_segment,
        remaining_chunk) for the one we're currently inside.

        Strategy:
          - index into self.segments, position in text = 0
          - for each segment EXCEPT we must know if it's fixed (known length)
            or variable (runs until next fixed literal appears)...
        This is the fiddly part. For a FIRST version, exploit the alternating
        structure: segments at even indices are FIXED, odd indices are VARIABLE.
        TODO: implement the walk. (I'll help — see note below.)
        """
        ...

    def accept(self, text: str) -> bool:
        """True if `text` is a valid prefix of the full template."""
        # TODO: split text; every fully-consumed segment must have been complete,
        #       and the current segment must accept() its partial chunk.
        ...

    def is_complete(self, text: str) -> bool:
        """True if `text` is a complete valid output."""
        # TODO: all segments consumed AND last one complete.
        ...