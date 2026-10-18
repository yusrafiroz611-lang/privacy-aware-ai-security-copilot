import json
import random
from pathlib import Path

DATASET_PATH = Path("dataset/synthetic_pii.jsonl")
OUTPUT_DIR = Path("dataset/prepared")
RANDOM_SEED = 42


def load_dataset():
    records = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}"
                ) from exc

            if not isinstance(record.get("text"), str):
                raise ValueError(
                    f"Line {line_number}: text must be a string"
                )

            if not isinstance(record.get("expected_values"), list):
                raise ValueError(
                    f"Line {line_number}: expected_values must be a list"
                )

            records.append(record)

    if not records:
        raise ValueError("Dataset is empty.")

    return records


def main():
    records = load_dataset()
    random.Random(RANDOM_SEED).shuffle(records)

    split_index = max(1, int(len(records) * 0.75))
    if len(records) > 1:
        split_index = min(split_index, len(records) - 1)

    dev_records = records[:split_index]
    test_records = records[split_index:]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, items in [
        ("dev.jsonl", dev_records),
        ("test.jsonl", test_records),
    ]:
        output_path = OUTPUT_DIR / name

        with output_path.open("w", encoding="utf-8") as file:
            for item in items:
                file.write(json.dumps(item) + "\n")

        print(f"Saved {len(items)} records to {output_path}")


if __name__ == "__main__":
    main()
