# ABOUTME: Coordinator walks generated text across an ordered segment list.
# ABOUTME: Alternating fixed/variable segments; delegates validation to each.


class Coordinator:
    """Validates text against an ordered list of segment validators.

    Convention: segments alternate FIXED (even indices) and VARIABLE (odd).
    A FIXED segment is a FixedValidator with a known literal length.
    A VARIABLE segment runs until the NEXT fixed literal begins to appear.
    """

    def __init__(self, segments: list, fixed_literals: list) -> None:
        self.segments = segments
        self.fixed_literals = fixed_literals

    def _split(self, text: str):
        """Walk `text` across segments.

        Returns a tuple (ok, consumed, cur_idx, cur_chunk):
          ok        : False if text diverged from the template (invalid)
          consumed  : list of (seg_idx, chunk) fully-consumed leading segments
          cur_idx   : index of the segment we are currently inside
          (or len(segments))
          cur_chunk : the partial chunk consumed by the current segment
        """
        consumed = []
        pos = 0
        n = len(self.segments)
        for idx in range(n):
            literal = self.fixed_literals[idx]
            remaining = text[pos:]
            if literal is not None:
                if len(remaining) < len(literal):
                    # we're still inside this fixed literal
                    if not literal.startswith(remaining):
                        return (False, consumed, idx, remaining)
                    return (True, consumed, idx, remaining)
                # enough text to (maybe) cover the whole literal
                if not remaining.startswith(literal):
                    return (False, consumed, idx, remaining[:len(literal)])
                consumed.append((idx, literal))
                pos += len(literal)
            else:
                # VARIABLE segment: runs until the next fixed literal appears.
                next_literal = (
                    self.fixed_literals[idx + 1] if idx + 1 < n else None
                )
                if next_literal is None:
                    # last segment is variable: it takes the rest
                    return (True, consumed, idx, remaining)
                # The variable ends where the next fixed literal begins.
                # The next literal may be fully present, or only its start may
                # have appeared at the tail of `remaining` (boundary in flux).
                cut = remaining.find(next_literal)
                if cut != -1:
                    # next literal fully present: variable is everything
                    # before it
                    chunk = remaining[:cut]
                    consumed.append((idx, chunk))
                    pos += cut
                    continue
                # next literal not fully present: check whether the TAIL of
                # `remaining` has begun matching the start of next_literal.
                boundary = None
                max_overlap = min(len(remaining), len(next_literal))
                for k in range(max_overlap, 0, -1):
                    if next_literal.startswith(remaining[-k:]):
                        boundary = len(remaining) - k
                        break
                if boundary is None:
                    # next literal has NOT begun: whole remaining is still this
                    # variable's partial, and we are CURRENTLY inside it.
                    return (True, consumed, idx, remaining)
                # next literal has begun at `boundary`: close the variable
                # here.
                chunk = remaining[:boundary]
                consumed.append((idx, chunk))
                pos += boundary
                # remainder (partial next literal) handled by next iteration.
        # consumed every segment exactly
        return (True, consumed, n, "")

    def accept(self, text: str) -> bool:
        ok, consumed, cur_idx, cur_chunk = self._split(text)
        if not ok:
            return False
        # every fully-consumed segment must have been a complete, valid value
        for idx, chunk in consumed:
            if not self.segments[idx].is_complete(chunk):
                return False
        # the segment we're currently inside must accept its partial
        if cur_idx < len(self.segments):
            return self.segments[cur_idx].accept(cur_chunk)
        return True

    def is_complete(self, text: str) -> bool:
        ok, consumed, cur_idx, cur_chunk = self._split(text)
        if not ok:
            return False
        # all segments consumed, each complete
        if cur_idx != len(self.segments):
            # still inside a segment: complete only if that segment is the last
            # and is itself complete with its chunk
            if cur_idx == len(self.segments) - 1 and \
               self.segments[cur_idx].is_complete(cur_chunk):
                pass
            else:
                return False
        for idx, chunk in consumed:
            if not self.segments[idx].is_complete(chunk):
                return False
        if cur_idx < len(self.segments):
            return self.segments[cur_idx].is_complete(cur_chunk)
        return True
