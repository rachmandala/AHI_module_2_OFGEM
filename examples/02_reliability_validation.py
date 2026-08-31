from ahi_module_2.core.reliability_engine import ReliabilityEngine

engine = ReliabilityEngine()

test_ahis = [
    1,
    2,
    4,
    5,
    6,
    8,
    10
]

print("\nPOF VALIDATION")
print("=" * 50)

for ahi in test_ahis:

    pof = engine.calculate_probability_of_failure(ahi)

    print(
        f"AHI={ahi:4.1f}  -->  PoF={pof:.6f}"
    )