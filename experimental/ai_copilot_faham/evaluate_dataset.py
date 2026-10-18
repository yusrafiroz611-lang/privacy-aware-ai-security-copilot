import json
from pathlib import Path

from ai import mask_sensitive_data

DATASET_PATH = Path("dataset/synthetic_pii.jsonl")


def main():
    total_expected = 0
    values_remaining = 0
    records_with_remaining_values = 0

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        records = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    for record in records:
        original_text = record["text"]
        result = mask_sensitive_data(original_text)
        masked_text = result["sanitized_text"]

        remaining = [
            value
            for value in record["expected_values"]
            if value.casefold() in masked_text.casefold()
        ]

        total_expected += len(record["expected_values"])
        values_remaining += len(remaining)

        if remaining:
            records_with_remaining_values += 1
            print(
                f"Potential masking miss in record {record['id']}: "
                f"{len(remaining)} expected value(s) remain"
            )

    protected = total_expected - values_remaining

    print("\n--- Evaluation Summary ---")
    print(f"Records evaluated: {len(records)}")
    print(f"Records with remaining values: {records_with_remaining_values}")
    print(f"Expected sensitive values: {total_expected}")
    print(f"Values no longer present: {protected}")
    print(f"Values still present: {values_remaining}")

    if total_expected:
        rate = protected / total_expected * 100
        print(f"Basic masking rate: {rate:.1f}%")
    else:
        print("No expected sensitive values to evaluate.")

    print(
        "Note: This metric does not prove all PII was detected "
        "or that the system is safe."
    )


if __name__ == "__main__":
    main()
