from substrate.primitive_api import CollapsePrimitive, CollapseViolation

class NoSame(CollapsePrimitive):
    """
    Collapse rule: forbids identity persistence.
    If any element in the new frame matches an element in the previous frame,
    collapse is triggered.
    """

    def check(self, frame):
        prev = frame.previous
        curr = frame.current

        if prev is None:
            return  # Nothing to compare against

        # If ANY element in curr is identical to ANY element in prev → collapse
        for x in curr:
            if x in prev:
                raise CollapseViolation("NoSame: identity persistence detected")

class NoDiff(CollapsePrimitive):
    """
    Collapse rule: forbids identity change.
    If previous != current, collapse is triggered.
    """

    def check(self, frame):
        prev = frame.previous
        curr = frame.current

        # If either is missing, no collapse
        if prev is None or curr is None:
            return

        # If they differ, collapse
        if prev != curr:
            raise CollapseViolation(f"NoDiff: change detected ({prev} → {curr})")

from substrate.primitive_api import CollapsePrimitive, CollapseViolation

class CompositeCollapse(CollapsePrimitive):
    """
    Runs multiple collapse primitives in order.
    Short-circuits on the first CollapseViolation.
    """

    def __init__(self, rules):
        self.rules = rules

    def check(self, frame):
        for rule in self.rules:
            rule.check(frame)


