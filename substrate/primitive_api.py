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
    def apply(self, frame, raw):
        raise NotImplementedError


class TelemetryOperator:
    """
    PrimitiveAPI uses dict-based frames because DummyTelemetry returns dicts.
    """
    def ingest(self, raw):
        return {"raw": raw}


class PrimitiveAPI:
    """
    Refined architecture:
    - Ascent primitives are required.
    - Collapse primitives are optional.
    - ValidOp removed (collapse rules run directly if present).
    - API runs cleanly with or without collapse.
    """
    def __init__(self, ascent_primitives=None, telemetry=None, collapse_primitives=None):
        self.ascent_primitives = ascent_primitives or {}
        self.collapse_primitives = collapse_primitives or {}
        self.telemetry = telemetry or TelemetryOperator()

    def has_collapse(self):
        return len(self.collapse_primitives) > 0

    def run(self, primitive_name, raw):
        # Step 1: telemetry → frame (dict)
        frame = self.telemetry.ingest(raw)

        # Step 2: optional collapse enforcement
        if self.has_collapse():
            for name, rule in self.collapse_primitives.items():
                if rule.check(frame):
                    raise CollapseViolation(f"Collapse triggered: {name}")

        # Step 3: required ascent primitive
        primitive = self.ascent_primitives[primitive_name]
        return primitive.apply(frame, raw)

    def register_collapse(self, name, primitive):
        self.collapse_primitives[name] = primitive

    def register_ascent(self, name, primitive):
        self.ascent_primitives[name] = primitive

    def register_telemetry(self, telemetry):
        self.telemetry = telemetry
