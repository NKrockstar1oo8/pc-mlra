# tests_metrices/loaders/dataset_loader.py

import json
from pathlib import Path
from typing import List, Dict


def load_dataset(relative_path: str) -> List[Dict]:
    """
    Load dataset using path relative to tests_metrices directory,
    regardless of where script is executed from.
    """
    base_dir = Path(__file__).resolve().parent.parent
    dataset_path = base_dir / relative_path

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {dataset_path}"
        )

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Dataset must be a list of test cases")

    return data
