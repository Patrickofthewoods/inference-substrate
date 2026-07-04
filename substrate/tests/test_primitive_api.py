# tests/test_primitive_api.py

from substrate.primitive_api import (
    PrimitiveAPI, CollapsePrimitive, AscentPrimitive,
    TelemetryOperator, ValidOp, CollapseViolation
)


# ------------------------------------------------------------
# Dummy collapse primitive (always triggers)
# ------------------------------------------------------------
class DummyCollapse(CollapsePrimitive):
    name = "DummyCollapse"
    def check(self, payload):
        return True


# ------------------------------------------------------------
# Dummy ascent primitive (returns payload)
# ------------------------------------------------------------
class DummyAscent(AscentPrimitive):
    name = "DummyAscent"
    def apply(self, frame, payload):
        frame["applied"] = True
        frame["payload"] = payload
        return frame


# ------------------------------------------------------------
# Dummy telemetry (wraps raw in dict)
# ------------------------------------------------------------
class DummyTelemetry(TelemetryOperator):
    def ingest(self, raw):
        return {"raw": raw}


def test_primitive_api():
    collapse = {"dummy": DummyCollapse()}
    ascent = {"dummy": DummyAscent()}
    telemetry = DummyTelemetry()
    valid_op = ValidOp(collapse)

    api = PrimitiveAPI(
        collapse_primitives=collapse,
        ascent_primitives=ascent,
        telemetry=telemetry,
        valid_op=valid_op
    )

    # Collapse should trigger
    try:
        api.run("dummy", raw=123)
        assert False, "CollapseViolation expected"
    except CollapseViolation:
        pass
