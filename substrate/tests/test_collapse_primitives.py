import pytest
from substrate.primitive_api import ContextFrame, CollapseViolation
from substrate.collapse_primitives import NoSame

def test_no_same_triggers_on_identity_persistence():
    prev = ["A", "B"]
    curr = ["B", "C"]  # "B" persists → collapse

    frame = ContextFrame(previous=prev, current=curr)
    rule = NoSame()

    with pytest.raises(CollapseViolation):
        rule.check(frame)

def test_no_same_allows_fresh_elements():
    prev = ["A", "B"]
    curr = ["C", "D"]  # No overlap → allowed

    frame = ContextFrame(previous=prev, current=curr)
    rule = NoSame()

    rule.check(frame)  # Should NOT raise
