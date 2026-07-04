# tests/test_nodiff.py

from substrate.primitive_api import ContextFrame, CollapseViolation
from substrate.collapse_primitives import NoDiff


def test_nodiff_allows_identical_values():
    """NoDiff should NOT collapse when previous == current."""
    rule = NoDiff()
    frame = ContextFrame(previous=10, current=10)

    # Should not raise
    rule.check(frame)


def test_nodiff_collapses_on_change():
    """NoDiff should collapse when previous != current."""
    rule = NoDiff()
    frame = ContextFrame(previous=10, current=20)

    try:
        rule.check(frame)
        assert False, "CollapseViolation expected"
    except CollapseViolation:
        pass


def test_nodiff_ignores_missing_previous():
    """If previous is None, NoDiff should not collapse."""
    rule = NoDiff()
    frame = ContextFrame(previous=None, current=5)

    # Should not raise
    rule.check(frame)


def test_nodiff_ignores_missing_current():
    """If current is None, NoDiff should not collapse."""
    rule = NoDiff()
    frame = ContextFrame(previous=5, current=None)

    # Should not raise
    rule.check(frame)
