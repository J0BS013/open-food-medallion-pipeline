from pathlib import Path

import pandas as pd

SILVER_DIR = Path("data/silver")


def clean_product(raw_data: dict, barcode: str) -> dict:
    product = raw_data.get("product", {})
    nutriments = product.get("nutriments", {})
    return {
        "barcode": barcode,
        "name": product.get("product_name", "").strip().title(),
        "brands": product.get("brands", "").lower().strip(),
        "categories": product.get("categories", "").split(",")[0].strip(),
        "nutriscore": product.get("nutriscore_grade", "").upper(),
        "energy_kcal": nutriments.get("energy-kcal_100g"),
        "fat": nutriments.get("fat_100g"),
        "sugars": nutriments.get("sugars_100g"),
        "proteins": nutriments.get("proteins_100g"),
    }


def save_cleaned(data: dict, barcode: str) -> Path:
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    path = SILVER_DIR / f"{barcode}.csv"
    pd.DataFrame([data]).to_csv(path, index=False)
    return path
