from substrate.primitive_api import ContextFrame, CollapseViolation
from substrate.collapse_primitives import NoDiff, NoSame, CompositeCollapse


def test_composite_allows_safe_frame():
    """Composite should allow when all rules pass."""
    comp = CompositeCollapse([NoDiff(), NoSame()])
    frame = ContextFrame(previous=[1], current=[2])  # NoSame passes, NoDiff passes
    comp.check(frame)  # Should not raise


def test_composite_triggers_first_violation():
    """Composite should collapse on the first failing rule."""
    comp = CompositeCollapse([NoDiff(), NoSame()])
    frame = ContextFrame(previous=10, current=20)  # NoDiff fails immediately

    try:
        comp.check(frame)
        assert False, "CollapseViolation expected"
    except CollapseViolation:
        pass


def test_composite_triggers_second_rule():
    """Composite should collapse on later rules if earlier ones pass."""
    comp = CompositeCollapse([NoDiff(), NoSame()])
    frame = ContextFrame(previous=[1], current=[1])  # NoDiff passes, NoSame fails

    try:
        comp.check(frame)
        assert False, "CollapseViolation expected"
    except CollapseViolation:
        pass
