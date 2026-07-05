# run.py

from substrate.primitive_api import PrimitiveAPI, TelemetryOperator, CollapseViolation
from substrate.collapse_primitives import (
    KramersAscent,
    CTMCAscent,
    ThresholdAscent,
    RegimeMismatchRule
)

def build_api():
    # Instantiate the refined API
    api = PrimitiveAPI(
        ascent_primitives={},
        telemetry=TelemetryOperator(),
        collapse_primitives={}
    )

    # Register ascent-only primitives
    api.register_ascent("kramers", KramersAscent())
    api.register_ascent("ctmc", CTMCAscent())

    # Register ascent + collapse for threshold domain
    api.register_ascent("threshold", ThresholdAscent())
    api.register_collapse("threshold_regime", RegimeMismatchRule())

    return api


if __name__ == "__main__":
    api = build_api()

    print("KRAMERS:")
    print(api.run("kramers", raw={"x": 1.0}))

    print("\nCTMC:")
    print(api.run("ctmc", raw={"rate": 0.2}))

    print("\nTHRESHOLD (safe):")
    print(api.run("threshold", raw={"signal": 0.9}))

    print("\nTHRESHOLD (collapse case):")
    try:
        api.run("threshold", raw={"signal": -999})  # invalid regime
    except CollapseViolation as e:
        print("Collapsed:", e)
