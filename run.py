# run.py

from substrate.primitive_api import PrimitiveAPI, ValidOp, ContextFrame
from substrate.collapse_primitives import NoSame, NoDiff, CompositeCollapse

class SimpleTelemetry:
    def ingest(self, raw):
        prev, curr = raw
        return ContextFrame(previous=prev, current=curr)

class DummyAscent:
    def apply(self, frame, payload):
        frame.value = payload
        return frame

def build_api():
    # Collapse primitives
    collapse = {
        "nodiff": NoDiff(),
        "nosame": NoSame(),
        "composite": CompositeCollapse([NoDiff(), NoSame()])
    }

    # Ascent primitives
    ascent = {
        "dummy": DummyAscent()
    }

    # Telemetry
    telemetry = SimpleTelemetry()

    # Collapse validator
    valid_op = ValidOp(collapse)

    # Build API instance
    return PrimitiveAPI(
        collapse_primitives=collapse,
        ascent_primitives=ascent,
        telemetry=telemetry,
        valid_op=valid_op
    )

if __name__ == "__main__":
    api = build_api()

    print("SAFE CASE:")
    print(api.run("dummy", raw=(None, [2])))

    print("\nCOLLAPSE CASE (NoDiff triggers):")
    try:
        api.run("dummy", raw=(10, 20))
    except Exception as e:
        print("Collapsed:", e)

    print("\nCOLLAPSE CASE (NoSame triggers):")
    try:
        api.run("dummy", raw=([1], [1]))
    except Exception as e:
        print("Collapsed:", e)
