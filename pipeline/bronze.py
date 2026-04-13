import json
from pathlib import Path

import requests

BRONZE_DIR = Path("data/bronze")


HEADERS = {"User-Agent": "OpenFoodMedallionPipeline/1.0 (github.com/open-food-medallion-pipeline)"}


def fetch_product(barcode: str) -> dict:
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("status") == 0:
        raise ValueError(f"Product not found for barcode {barcode}")
    return data


def save_raw(data: dict, barcode: str) -> Path:
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    path = BRONZE_DIR / f"{barcode}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path
