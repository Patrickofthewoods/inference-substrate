# substrate/primitive_api.py

class ContextFrame:
    """
    Simple container used only by collapse tests.
    PrimitiveAPI does NOT use this.
    """
    def __init__(self, previous=None, current=None):
        self.previous = previous
        self.current = current


class CollapseViolation(Exception):
    pass


class CollapsePrimitive:
    def check(self, frame):
        raise NotImplementedError


class AscentPrimitive:
    def apply(self, frame, payload):
        raise NotImplementedError


class TelemetryOperator:
    """
    PrimitiveAPI uses dict-based frames because DummyTelemetry returns dicts.
    """
    def ingest(self, raw):
        return {"raw": raw}


class ValidOp:
    def __init__(self, collapse_rules):
        self.collapse_rules = collapse_rules

    def enforce(self, frame):
        for name, rule in self.collapse_rules.items():
            if rule.check(frame):
                raise CollapseViolation(f"Collapse triggered: {name}")

class PrimitiveAPI:
    def __init__(self, collapse_primitives, ascent_primitives, telemetry, valid_op):
        self.collapse_primitives = collapse_primitives
        self.ascent_primitives = ascent_primitives
        self.telemetry = telemetry
        self.valid_op = valid_op

    def run(self, primitive_name, raw):
        # Step 1: telemetry → frame (dict)
        frame = self.telemetry.ingest(raw)

        # Step 2: collapse enforcement
        self.valid_op.enforce(frame)

        # Step 3: ascent primitive
        primitive = self.ascent_primitives[primitive_name]
        return primitive.apply(frame, raw)

    def register_collapse(self, name, primitive):
        self.collapse_primitives[name] = primitive
        self.valid_op = ValidOp(self.collapse_primitives)

    def register_ascent(self, name, primitive):
        self.ascent_primitives[name] = primitive

    def register_telemetry(self, telemetry):
        self.telemetry = telemetry
